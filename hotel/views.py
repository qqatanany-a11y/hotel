from django .shortcuts import render ,redirect ,get_object_or_404 
from django .contrib .auth import login 
from django .contrib .auth .decorators import login_required ,user_passes_test 
from django .contrib import messages 
from django .utils .translation import gettext_lazy as _ 
from django .utils .translation import gettext as __ 
from django .core .paginator import Paginator 
from django .db .models import Q ,Count ,Sum 
from django .db import transaction 
from django .http import JsonResponse ,HttpResponseForbidden 
from django .urls import reverse 
from datetime import date ,timedelta 
from decimal import Decimal 
from .models import (
RoomType ,Room ,Guest ,Booking ,BookingService ,
AdditionalService ,Payment ,HotelSettings 
)
from .forms import (
CustomUserCreationForm ,GuestProfileForm ,RoomSearchForm ,
BookingForm ,ContactForm ,BookingStatusForm ,AdminBookingForm 
)
from datetime import date 
from django .core .mail import send_mail 
from django .template .loader import render_to_string 
from django .conf import settings 
from django .db .models import Q ,Count ,Sum ,Min 
from django .utils import timezone 


def home (request ):
    today =date .today ()

    hotel_settings =HotelSettings .get_settings ()
    room_types =RoomType .objects .all ()[:6 ]

    total_rooms =Room .objects .filter (is_active =True ).count ()

    available_rooms =Room .objects .filter (is_active =True ,status ='available').count ()

    active_bookings_count =Booking .objects .filter (
    status ='confirmed',
    check_in_date__lte =today ,
    check_out_date__gt =today ).count ()
    available_rooms =total_rooms -active_bookings_count 

    happy_customers =Guest .objects .count ()
    context ={
    'hotel_settings':hotel_settings ,
    'room_types':room_types ,
    'total_rooms':total_rooms ,
    'available_rooms':available_rooms ,
    'happy_customers':happy_customers ,
    'search_form':RoomSearchForm (),
    }
    return render (request ,'hotel/home.html',context )


def room_types (request ):
    room_types =RoomType .objects .all ().order_by ('base_price')
    return render (request ,'hotel/room_types.html',{'room_types':room_types })


def room_detail (request ,room_type_id ):
    room_type =get_object_or_404 (RoomType ,id =room_type_id )
    available_rooms =Room .objects .filter (
    room_type =room_type ,
    is_active =True ,
    status ='available'
    ).count ()

    context ={
    'room_type':room_type ,
    'available_rooms':available_rooms ,
    'amenities':room_type .get_amenities_list (),
    }
    return render (request ,'hotel/room_detail.html',context )


def search_rooms (request ):
    from django .db .models import Count ,Sum ,Min 

    if not request.GET:
        form = RoomSearchForm()
        return render(request, 'hotel/search_rooms.html', {'form': form})
    form =RoomSearchForm (request .GET or None )
    grouped_rooms =[]
    search_performed =False 

    if request .GET and form .is_valid ():
        search_performed =True 
        check_in_date =form .cleaned_data ['check_in_date']
        check_out_date =form .cleaned_data ['check_out_date']
        room_type =form .cleaned_data .get ('room_type')
        adults =form .cleaned_data ['adults']
        children =form .cleaned_data ['children']
        total_guests =adults +children 


        queryset =Room .objects .filter (
        is_active =True ,
        status ='available',
        room_type__max_occupancy__gte =total_guests 
        ).select_related ('room_type')


        if room_type :
            queryset =queryset .filter (room_type =room_type )


        available_rooms =[]
        for room in queryset :
            if room .is_available_for_dates (check_in_date ,check_out_date ):
                available_rooms .append (room .id )

        grouped_rooms =(
        Room .objects 
        .filter (id__in =available_rooms )
        .values ('room_type__id','room_type__name','floor')
        .annotate (
        total_rooms =Count ('id'),
        base_price =Sum ('room_type__base_price')/Count ('id'),
        first_room_id =Min ('id')
        )
        .filter (first_room_id__isnull =False )
        .order_by ('room_type__name','floor')
        )


        request .session ['search_data']={
        'check_in_date':check_in_date .isoformat (),
        'check_out_date':check_out_date .isoformat (),
        'adults':adults ,
        'children':children ,
        }

    context ={
    'form':form ,
    'grouped_rooms':grouped_rooms ,
    'search_performed':search_performed ,
    }
    return render (request ,'hotel/search_rooms.html',context )


    request .session ['search_data']={
    'check_in_date':check_in_date .isoformat (),
    'check_out_date':check_out_date .isoformat (),
    'adults':adults ,
    'children':children ,
    }

    context ={
    'form':form ,
    'grouped_rooms':grouped_rooms ,
    'search_performed':search_performed ,
    }
    return render (request ,'hotel/search_rooms.html',context )



@login_required 
def book_room (request ,room_id ):
    room =get_object_or_404 (Room ,id =room_id ,is_active =True ,status ='available')

    search_data = request.session.get('search_data')
    if not search_data and request.method != 'POST':
        return redirect('search_rooms')

    try :
        guest =request .user .guest 
    except Guest .DoesNotExist :
        messages .warning (request ,_ ('Please complete your profile information first'))
        return redirect ('profile')

    if request .method =='POST':
        form =BookingForm (request .POST ,room =room )
        if form .is_valid ():
            with transaction .atomic ():
                booking =form .save (commit =False )
                booking .guest =guest 
                booking .room =room 

                nights =(booking .check_out_date -booking .check_in_date ).days 
                booking .total_amount =room .room_type .base_price *nights 

                booking .save ()

                additional_services =form .cleaned_data .get ('additional_services')
                if additional_services :
                    for service in additional_services :
                        BookingService .objects .create (
                        booking =booking ,
                        service =service ,
                        quantity =1 
                        )
                        booking .total_amount +=service .price 

                booking .save ()

                Payment .objects .create (
                booking =booking ,
                amount =booking .total_amount ,
                payment_method ='pending',
                status ='pending'
                )

                messages .success (request ,_ ('Booking created successfully! Booking ID: {}').format (booking .booking_id ))
                return redirect ('booking_detail',booking_id =booking .booking_id )
    else :
        initial_data ={}
        if search_data :
            initial_data ={
            'check_in_date':search_data ['check_in_date'],
            'check_out_date':search_data ['check_out_date'],
            'adults':search_data ['adults'],
            'children':search_data ['children'],
            }
        form =BookingForm (initial =initial_data ,room =room )

    estimated_price =None 
    if search_data :
        nights =(date .fromisoformat (search_data ['check_out_date'])-
        date .fromisoformat (search_data ['check_in_date'])).days 
        estimated_price =room .room_type .base_price *nights 

    context ={
    'room':room ,
    'form':form ,
    'additional_services':AdditionalService .objects .filter (is_active =True ),
    'estimated_price':estimated_price ,
    }
    return render (request ,'hotel/book_room.html',context )


@login_required 
def booking_detail (request ,booking_id ):
    booking =get_object_or_404 (Booking ,booking_id =booking_id )


    if booking .status =='pending':
        elapsed_time =timezone .now ()-booking .created_at 
        if elapsed_time >timedelta (minutes =10 ):
            booking .status ='cancelled'
            booking .save ()
            messages .warning (request ,_ ('Your booking was automatically cancelled because payment was not completed within 10 minutes.'))
            return redirect ('my_bookings')

    if not (booking .guest .user ==request .user or request .user .is_staff ):
        return HttpResponseForbidden (_ ('You are not authorized to view this booking'))

    services =BookingService .objects .filter (booking =booking ).select_related ('service')
    payments =Payment .objects .filter (booking =booking ).order_by ('-created_at')

    context ={
    'booking':booking ,
    'services':services ,
    'payments':payments ,
    }
    return render (request ,'hotel/booking_detail.html',context )


@login_required 
def my_bookings (request ):
    try :
        guest =request .user .guest 
        bookings =Booking .objects .filter (guest =guest ).order_by ('-created_at')

        status_filter =request .GET .get ('status')
        if status_filter :
            bookings =bookings .filter (status =status_filter )

        paginator =Paginator (bookings ,10 )
        page_number =request .GET .get ('page')
        page_obj =paginator .get_page (page_number )

        context ={
        'page_obj':page_obj ,
        'status_filter':status_filter ,
        'status_choices':Booking .STATUS_CHOICES ,
        }
        return render (request ,'hotel/my_bookings.html',context )

    except Guest .DoesNotExist :
        messages .warning (request ,_ ('Please complete your profile information first'))
        return redirect ('profile')


@login_required 
def cancel_booking (request ,booking_id ):
    booking =get_object_or_404 (Booking ,booking_id =booking_id ,guest__user =request .user )

    if not booking .can_cancel ():
        messages .error (request ,_ ('This booking cannot be cancelled'))
        return redirect ('booking_detail',booking_id =booking_id )

    if request .method =='POST':
        booking .status ='cancelled'
        booking .save ()
        messages .success (request ,_ ('Booking cancelled successfully'))
        return redirect ('my_bookings')

    return render (request ,'hotel/cancel_booking.html',{'booking':booking })


def register (request ):
    if request .method =='POST':
        form =CustomUserCreationForm (request .POST )
        if form .is_valid ():
            user =form .save ()
            Guest .objects .create (
            user =user ,
            phone ='',
            national_id =None ,
            nationality ='Jordanian'
            )
            login (request ,user )
            messages .success (request ,_ ('Account created successfully! Please complete your profile information'))
            return redirect ('profile')
    else :
        form =CustomUserCreationForm ()

    return render (request ,'registration/register.html',{'form':form })


@login_required 
def profile (request ):
    try :
        guest =request .user .guest 
    except Guest .DoesNotExist :
        guest =Guest .objects .create (
        user =request .user ,
        phone ='',
        national_id =None ,
        nationality ='Jordanian'
        )

    if request .method =='POST':
        form =GuestProfileForm (request .POST ,instance =guest )
        if form .is_valid ():
            form .save ()
            messages .success (request ,_ ('Changes saved successfully'))
            return redirect ('profile')
    else :
        form =GuestProfileForm (instance =guest )

    return render (request ,'hotel/profile.html',{'form':form ,'guest':guest })


def contact (request ):
    hotel_settings =HotelSettings .get_settings ()

    if request .method =='POST':
        form =ContactForm (request .POST )
        if form .is_valid ():
            messages .success (request ,_ ('Your message has been sent successfully. We will contact you soon'))
            return redirect ('contact')
    else :
        form =ContactForm ()

    context ={
    'form':form ,
    'hotel_settings':hotel_settings ,
    }
    return render (request ,'hotel/contact.html',context )


def about (request ):
    hotel_settings =HotelSettings .get_settings ()
    return render (request ,'hotel/about.html',{'hotel_settings':hotel_settings })


def is_staff (user ):
    return user .is_staff 


@user_passes_test (is_staff )
def admin_dashboard (request ):
    today =date .today ()

    total_rooms =Room .objects .filter (is_active =True ).count ()

    active_bookings_count =Booking .objects .filter (
    status ='confirmed',
    check_in_date__lte =today ,
    check_out_date__gt =today 
    ).count ()

    available_rooms =total_rooms -active_bookings_count 

    maintenance_rooms =Room .objects .filter (is_active =True ,status ='maintenance').count ()
    out_of_order_rooms =Room .objects .filter (is_active =True ,status ='out_of_order').count ()

    occupied_rooms =active_bookings_count 

    total_revenue =Payment .objects .filter (
    status ='completed'
    ).aggregate (total =Sum ('amount'))['total']or 0 

    daily_revenue =Payment .objects .filter (
    status ='completed',
    created_at__date =today 
    ).aggregate (total =Sum ('amount'))['total']or 0 

    monthly_revenue =Payment .objects .filter (
    status ='completed',
    created_at__month =today .month ,
    created_at__year =today .year 
    ).aggregate (total =Sum ('amount'))['total']or 0 

    today_checkins =Booking .objects .filter (
    check_in_date =today ,
    status__in =['confirmed','checked_in']
    ).count ()

    today_checkouts =Booking .objects .filter (
    check_out_date =today ,
    status ='checked_in'
    ).count ()

    pending_bookings =Booking .objects .filter (status ='pending').count ()
    confirmed_bookings =Booking .objects .filter (status ='confirmed').count ()
    total_bookings =Booking .objects .count ()

    recent_bookings =Booking .objects .select_related (
    'guest__user','room__room_type'
    ).order_by ('-created_at')[:10 ]

    occupancy_rate =0 
    if total_rooms >0 :
        occupancy_rate =round ((occupied_rooms /total_rooms )*100 ,1 )

    context ={
    'total_rooms':total_rooms ,
    'available_rooms':available_rooms ,
    'occupied_rooms':occupied_rooms ,
    'maintenance_rooms':maintenance_rooms ,
    'out_of_order_rooms':out_of_order_rooms ,
    'occupancy_rate':occupancy_rate ,

    'total_revenue':total_revenue ,
    'daily_revenue':daily_revenue ,
    'monthly_revenue':monthly_revenue ,

    'today_checkins':today_checkins ,
    'today_checkouts':today_checkouts ,

    'total_bookings':total_bookings ,
    'pending_bookings':pending_bookings ,
    'confirmed_bookings':confirmed_bookings ,
    'recent_bookings':recent_bookings ,
    }
    return render (request ,'hotel/admin/dashboard.html',context )

@user_passes_test (is_staff )
def admin_bookings (request ):
    bookings =Booking .objects .select_related (
    'guest__user','room__room_type'
    ).order_by ('-created_at')

    status_filter =request .GET .get ('status')
    if status_filter :
        bookings =bookings .filter (status =status_filter )

    date_filter =request .GET .get ('date')
    if date_filter :
        bookings =bookings .filter (check_in_date =date_filter )

    search =request .GET .get ('search')
    if search :
        bookings =bookings .filter (
        Q (booking_id__icontains =search )|
        Q (guest__user__first_name__icontains =search )|
        Q (guest__user__last_name__icontains =search )|
        Q (room__room_number__icontains =search )
        )

    paginator =Paginator (bookings ,20 )
    page_number =request .GET .get ('page')
    page_obj =paginator .get_page (page_number )

    context ={
    'page_obj':page_obj ,
    'status_choices':Booking .STATUS_CHOICES ,
    'status_filter':status_filter ,
    'date_filter':date_filter ,
    'search':search ,
    }
    return render (request ,'hotel/admin/bookings.html',context )


@user_passes_test (is_staff )
def admin_booking_detail (request ,booking_id ):
    booking =get_object_or_404 (Booking ,booking_id =booking_id )

    if request .method =='POST':
        form =BookingStatusForm (request .POST ,instance =booking )
        if form .is_valid ():
            form .save ()
            messages .success (request ,_ ('Booking status updated'))
            return redirect ('admin_booking_detail',booking_id =booking_id )
    else :
        form =BookingStatusForm (instance =booking )

    services =BookingService .objects .filter (booking =booking ).select_related ('service')
    payments =Payment .objects .filter (booking =booking ).order_by ('-created_at')

    context ={
    'booking':booking ,
    'form':form ,
    'services':services ,
    'payments':payments ,
    }
    return render (request ,'hotel/admin/booking_detail.html',context )


@user_passes_test (is_staff )
def admin_add_booking (request ):
    if request .method =='POST':
        form =AdminBookingForm (request .POST )
        if form .is_valid ():
            with transaction .atomic ():
                booking =form .save (commit =False )

                nights =(booking .check_out_date -booking .check_in_date ).days 
                booking .total_amount =booking .room .room_type .base_price *nights 

                booking .save ()

                additional_services =form .cleaned_data .get ('additional_services')
                if additional_services :
                    for service in additional_services :
                        BookingService .objects .create (
                        booking =booking ,
                        service =service ,
                        quantity =1 
                        )
                        booking .total_amount +=service .price 

                booking .save ()

                Payment .objects .create (
                booking =booking ,
                amount =booking .total_amount ,
                payment_method ='pending',
                status ='pending'
                )

                messages .success (request ,_ ('Booking created successfully! Booking ID: {}').format (booking .booking_id ))
                return redirect ('admin_booking_detail',booking_id =booking .booking_id )
    else :
        form =AdminBookingForm ()

    context ={
    'form':form ,
    'additional_services':AdditionalService .objects .filter (is_active =True ),
    }
    return render (request ,'hotel/admin/add_booking.html',context )


@user_passes_test (is_staff )
def admin_rooms (request ):
    rooms =Room .objects .select_related ('room_type').order_by ('floor','room_number')

    status_filter =request .GET .get ('status')
    if status_filter :
        rooms =rooms .filter (status =status_filter )

    room_type_filter =request .GET .get ('room_type')
    if room_type_filter :
        rooms =rooms .filter (room_type_id =room_type_filter )

    floor_filter =request .GET .get ('floor')
    if floor_filter :
        rooms =rooms .filter (floor =floor_filter )

    context ={
    'rooms':rooms ,
    'room_types':RoomType .objects .all (),
    'status_choices':Room .STATUS_CHOICES ,
    'floors':Room .objects .values_list ('floor',flat =True ).distinct ().order_by ('floor'),
    'status_filter':status_filter ,
    'room_type_filter':room_type_filter ,
    'floor_filter':floor_filter ,
    }
    return render (request ,'hotel/admin/rooms.html',context )


@user_passes_test (is_staff )
def admin_guests (request ):
    guests =Guest .objects .select_related ('user').order_by ('-created_at')

    search =request .GET .get ('search')
    if search :
        guests =guests .filter (
        Q (user__first_name__icontains =search )|
        Q (user__last_name__icontains =search )|
        Q (user__email__icontains =search )|
        Q (phone__icontains =search )|
        Q (national_id__icontains =search )
        )

    paginator =Paginator (guests ,20 )
    page_number =request .GET .get ('page')
    page_obj =paginator .get_page (page_number )

    context ={
    'page_obj':page_obj ,
    'search':search ,
    }
    return render (request ,'hotel/admin/guests.html',context )


@user_passes_test (is_staff )
def admin_reports (request ):
    from django .db .models import Count ,Sum ,Avg 
    from django .utils import timezone 

    room_stats ={
    'total':Room .objects .filter (is_active =True ).count (),
    'available':Room .objects .filter (is_active =True ,status ='available').count (),
    'occupied':Room .objects .filter (is_active =True ,status ='occupied').count (),
    'maintenance':Room .objects .filter (is_active =True ,status ='maintenance').count (),
    'out_of_order':Room .objects .filter (is_active =True ,status ='out_of_order').count (),
    }

    booking_stats =Booking .objects .aggregate (
    total =Count ('id'),
    pending =Count ('id',filter =Q (status ='pending')),
    confirmed =Count ('id',filter =Q (status ='confirmed')),
    checked_in =Count ('id',filter =Q (status ='checked_in')),
    checked_out =Count ('id',filter =Q (status ='checked_out')),
    cancelled =Count ('id',filter =Q (status ='cancelled')),
    )

    revenue_stats =Payment .objects .filter (status ='completed').aggregate (
    total =Sum ('amount'),
    count =Count ('id'),
    average =Avg ('amount')
    )

    popular_room_types =RoomType .objects .annotate (
    booking_count =Count ('room__bookings')
    ).order_by ('-booking_count')[:5 ]

    context ={
    'room_stats':room_stats ,
    'booking_stats':booking_stats ,
    'revenue_stats':revenue_stats ,
    'popular_room_types':popular_room_types ,
    }
    return render (request ,'hotel/admin/reports.html',context )


@user_passes_test (is_staff )
def api_room_availability (request ):
    check_in =request .GET .get ('check_in')
    check_out =request .GET .get ('check_out')
    room_type_id =request .GET .get ('room_type')

    if not check_in or not check_out :
        return JsonResponse ({'error':'Missing required parameters'},status =400 )

    try :
        from datetime import datetime 
        check_in_date =datetime .strptime (check_in ,'%Y-%m-%d').date ()
        check_out_date =datetime .strptime (check_out ,'%Y-%m-%d').date ()
    except ValueError :
        return JsonResponse ({'error':'Invalid date format'},status =400 )

    rooms =Room .objects .filter (is_active =True ,status ='available')

    if room_type_id :
        rooms =rooms .filter (room_type_id =room_type_id )

    available_rooms =[]
    for room in rooms :
        if room .is_available_for_dates (check_in_date ,check_out_date ):
            available_rooms .append ({
            'id':room .id ,
            'room_number':room .room_number ,
            'room_type':room .room_type .get_name_display (),
            'floor':room .floor ,
            'base_price':float (room .room_type .base_price )
            })
            return JsonResponse ({'rooms':available_rooms })


@login_required 
def payment_page (request ,booking_id ):
    """صفحة الدفع للحجز"""
    booking =get_object_or_404 (Booking ,
    booking_id =booking_id ,
    guest__user =request .user )

    if booking .status !='pending':
        messages .error (request ,_ ('This booking cannot be paid for.'))
        return redirect ('booking_detail',booking_id =booking_id )

    if request .method =='POST':
        payment_method =request .POST .get ('payment_method')


        card_number =request .POST .get ('card_number')
        expiry_date =request .POST .get ('expiry_date')
        cvv =request .POST .get ('cvv')

        if payment_method in ['credit_card','cash','visa']:

            payment =Payment .objects .create (
            booking =booking ,
            amount =booking .total_amount ,
            payment_method =payment_method ,
            status ='completed'
            )


            booking .status ='confirmed'
            booking .save ()


            try :
                send_booking_confirmation_email (booking ,payment )
                messages .success (request ,_ ('Payment completed successfully! Your booking is now confirmed. A confirmation email has been sent to you.'))
            except Exception as e :
                print ("Error sending email:",e )
                messages .warning (request ,_ ('There was an issue sending the confirmation email, but your booking is confirmed.'))

            return redirect ('booking_detail',booking_id =booking_id )
        else :
            messages .error (request ,_ ('Please select a valid payment method.'))

    context ={
    'booking':booking ,
    }
    return render (request ,'hotel/payment.html',context )

def send_booking_confirmation_email (booking ,payment ):
    """إرسال إيميل تأكيد الحجز"""
    subject =f'Booking Confirmation - {booking.booking_id}'


    context ={
    'booking':booking ,
    'payment':payment ,
    'guest_name':booking .guest .get_full_name (),
    'hotel_name':getattr (settings ,'HOTEL_NAME','Hotel'),
    'hotel_address':getattr (settings ,'HOTEL_ADDRESS',''),
    'hotel_phone':getattr (settings ,'HOTEL_PHONE',''),
    'hotel_email':getattr (settings ,'HOTEL_EMAIL',''),
    }


    html_message =render_to_string ('email/booking_confirmation.html',context )


    plain_message =f"""
Booking Confirmation - {booking.booking_id}

Dear {booking.guest.get_full_name()},

Your booking has been confirmed!

Booking Details:
- Booking ID: {booking.booking_id}
- Room: {booking.room.room_type.get_name_display()} (Room {booking.room.room_number})
- Check-in: {booking.check_in_date}
- Check-out: {booking.check_out_date}
- Total Amount: ${booking.total_amount}

Thank you for choosing our hotel!
    """


    send_mail (
    subject =subject ,
    message =plain_message ,
    from_email =settings .DEFAULT_FROM_EMAIL ,
    recipient_list =[booking .guest .user .email ],
    html_message =html_message ,
    fail_silently =False ,
    )
