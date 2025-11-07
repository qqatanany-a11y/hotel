from django .db import models 
from django .contrib .auth .models import User 
from django .urls import reverse 
from django .utils .translation import gettext_lazy as _ 
from django .core .validators import MinValueValidator ,MaxValueValidator 


class RoomType (models .Model ):
    ROOM_TYPES =[
    ('single',_ ('Single Room')),
    ('double',_ ('Double Room')),
    ('triple',_ ('Triple Room')),
    ('quad',_ ('Quadruple Room')),
    ('suite',_ ('Suite')),
    ('deluxe',_ ('Deluxe Room')),
    ('family',_ ('Family Room')),
    ]

    name =models .CharField (_ ('Type Name'),max_length =50 ,choices =ROOM_TYPES ,unique =True )
    description =models .TextField (_ ('Description'),blank =True )
    base_price =models .DecimalField (_ ('Base Price'),max_digits =10 ,decimal_places =2 )
    max_occupancy =models .PositiveIntegerField (_ ('Maximum Occupancy'))
    image =models .ImageField (_ ('Image'),upload_to ='room_types/',blank =True ,null =True )
    amenities =models .TextField (_ ('Amenities'),help_text =_ ('Enter amenities separated by commas'))

    class Meta :
        verbose_name =_ ('Room Type')
        verbose_name_plural =_ ('Room Types')
        ordering =['base_price']

    def __str__ (self ):
        return self .get_name_display ()

    def get_amenities_list (self ):
        if self .amenities :
            return [amenity .strip ()for amenity in self .amenities .split (',')]
        return []


class Room (models .Model ):
    STATUS_CHOICES =[
    ('available',_ ('Available')),
    ('occupied',_ ('Occupied')),
    ('maintenance',_ ('Maintenance')),
    ('out_of_order',_ ('Out of Order')),
    ]

    room_number =models .CharField (_ ('Room Number'),max_length =10 ,unique =True )
    room_type =models .ForeignKey (RoomType ,on_delete =models .CASCADE ,verbose_name =_ ('Room Type'))
    floor =models .PositiveIntegerField (_ ('Floor'))
    status =models .CharField (_ ('Status'),max_length =20 ,choices =STATUS_CHOICES ,default ='available')
    is_active =models .BooleanField (_ ('Active'),default =True )
    notes =models .TextField (_ ('Notes'),blank =True )

    class Meta :
        verbose_name =_ ('Room')
        verbose_name_plural =_ ('Rooms')
        ordering =['floor','room_number']

    def __str__ (self ):
        return f"{_('Room')} {self.room_number} - {self.room_type}"

    def is_available_for_dates (self ,check_in ,check_out ):
        if self .status !='available'or not self .is_active :
            return False 

        overlapping_bookings =self .bookings .filter (
        status__in =['confirmed','checked_in'],
        check_in_date__lt =check_out ,
        check_out_date__gt =check_in 
        )
        return not overlapping_bookings .exists ()


class Guest (models .Model ):
    user =models .OneToOneField (User ,on_delete =models .CASCADE ,verbose_name =_ ('User'))
    phone =models .CharField (_ ('Phone Number'),max_length =20 )
    national_id =models .CharField (_ ('National ID'),max_length =20 ,unique =True ,null =True ,blank =True )
    nationality =models .CharField (_ ('Nationality'),max_length =50 ,default ='Jordanian')
    date_of_birth =models .DateField (_ ('Date of Birth'),null =True ,blank =True )
    address =models .TextField (_ ('Address'),blank =True )
    emergency_contact =models .CharField (_ ('Emergency Contact'),max_length =100 ,blank =True )
    emergency_phone =models .CharField (_ ('Emergency Phone'),max_length =20 ,blank =True )
    created_at =models .DateTimeField (_ ('Registration Date'),auto_now_add =True )

    class Meta :
        verbose_name =_ ('Guest')
        verbose_name_plural =_ ('Guests')
        ordering =['-created_at']

    def __str__ (self ):
        return f"{self.user.get_full_name() or self.user.username}"

    def get_full_name (self ):
        return self .user .get_full_name ()or self .user .username 


class AdditionalService (models .Model ):
    name =models .CharField (_ ('Service Name'),max_length =100 )
    description =models .TextField (_ ('Description'),blank =True )
    price =models .DecimalField (_ ('Price'),max_digits =8 ,decimal_places =2 )
    is_active =models .BooleanField (_ ('Active'),default =True )
    icon =models .CharField (_ ('Icon'),max_length =50 ,blank =True ,
    help_text =_ ('Font Awesome icon name'))

    class Meta :
        verbose_name =_ ('Additional Service')
        verbose_name_plural =_ ('Additional Services')
        ordering =['name']

    def __str__ (self ):
        return self .name 


class Booking (models .Model ):
    STATUS_CHOICES =[
    ('pending',_ ('Waiting for payment')),
    ('confirmed',_ ('Confirmed')),
    ('checked_in',_ ('Checked In')),
    ('checked_out',_ ('Checked Out')),
    ('cancelled',_ ('Cancelled')),
    ('no_show',_ ('No Show')),
    ]

    booking_id =models .CharField (_ ('Booking ID'),max_length =20 ,unique =True ,editable =False )
    guest =models .ForeignKey (Guest ,on_delete =models .CASCADE ,verbose_name =_ ('Guest'),related_name ='bookings')
    room =models .ForeignKey (Room ,on_delete =models .CASCADE ,verbose_name =_ ('Room'),related_name ='bookings')
    check_in_date =models .DateField (_ ('Arrival Date'))
    check_out_date =models .DateField (_ ('Departure Date'))
    adults =models .PositiveIntegerField (_ ('Adults'),default =1 ,validators =[MinValueValidator (1 )])
    children =models .PositiveIntegerField (_ ('Children'),default =0 ,validators =[MinValueValidator (0 )])
    total_amount =models .DecimalField (_ ('Total Amount'),max_digits =10 ,decimal_places =2 )
    status =models .CharField (_ ('Booking Status'),max_length =20 ,choices =STATUS_CHOICES ,default ='pending')
    special_requests =models .TextField (_ ('Special Requests'),blank =True )
    created_at =models .DateTimeField (_ ('Booking Date'),auto_now_add =True )
    updated_at =models .DateTimeField (_ ('Last Update'),auto_now =True )

    class Meta :
        verbose_name =_ ('Booking')
        verbose_name_plural =_ ('Bookings')
        ordering =['-created_at']

    def __str__ (self ):
        return f"{_('Booking')} {self.booking_id} - {self.guest}"

    def save (self ,*args ,**kwargs ):
        if not self .booking_id :
            import uuid 
            self .booking_id =f"BK{str(uuid.uuid4())[:8].upper()}"
        super ().save (*args ,**kwargs )
        if self .status =='checked_in'and self .room .status !='occupied':
            self .room .status ='occupied'
            self .room .save ()
        elif self .status in ['checked_out','cancelled']and self .room .status =='occupied':
            self .room .status ='available'
            self .room .save ()

    def get_nights (self ):
        return (self .check_out_date -self .check_in_date ).days 

    def get_total_guests (self ):
        return self .adults +self .children 

    def can_cancel (self ):
        return self .status in ['pending','confirmed']


class BookingService (models .Model ):
    booking =models .ForeignKey (Booking ,on_delete =models .CASCADE ,verbose_name =_ ('Booking'),related_name ='services')
    service =models .ForeignKey (AdditionalService ,on_delete =models .CASCADE ,verbose_name =_ ('Service'))
    quantity =models .PositiveIntegerField (_ ('Quantity'),default =1 )
    total_price =models .DecimalField (_ ('Total Price'),max_digits =8 ,decimal_places =2 )

    class Meta :
        verbose_name =_ ('Booking Service')
        verbose_name_plural =_ ('Booking Services')
        unique_together =['booking','service']

    def __str__ (self ):
        return f"{self.booking.booking_id} - {self.service.name}"

    def save (self ,*args ,**kwargs ):
        self .total_price =self .service .price *self .quantity 
        super ().save (*args ,**kwargs )


class Payment (models .Model ):
    PAYMENT_STATUS =[
    ('pending',_ ('Waiting for payment')),
    ('completed',_ ('Completed')),
    ('failed',_ ('Failed')),
    ('refunded',_ ('Refunded')),
    ]

    PAYMENT_METHOD =[
    ('cash',_ ('Cash')),
    ('card',_ ('Credit Card')),
    ('bank_transfer',_ ('Bank Transfer')),
    ('online',_ ('Online Payment')),
    ]

    booking =models .ForeignKey (Booking ,on_delete =models .CASCADE ,verbose_name =_ ('Booking'),related_name ='payments')
    amount =models .DecimalField (_ ('Amount'),max_digits =10 ,decimal_places =2 )
    payment_method =models .CharField (_ ('Payment Method'),max_length =20 ,choices =PAYMENT_METHOD )
    status =models .CharField (_ ('Payment Status'),max_length =20 ,choices =PAYMENT_STATUS ,default ='pending')
    transaction_id =models .CharField (_ ('Transaction ID'),max_length =100 ,blank =True )
    notes =models .TextField (_ ('Notes'),blank =True )
    created_at =models .DateTimeField (_ ('Payment Date'),auto_now_add =True )

    class Meta :
        verbose_name =_ ('Payment')
        verbose_name_plural =_ ('Payments')
        ordering =['-created_at']

    def __str__ (self ):
        return f"{_('Payment')} {self.amount} - {self.booking.booking_id}"


class HotelSettings (models .Model ):
    name =models .CharField (_ ('Hotel Name'),max_length =200 ,default ='Amman Golden Hotel')
    description =models .TextField (_ ('Description'),blank =True )
    address =models .TextField (_ ('Address'),default ='Amman, Jordan')
    phone =models .CharField (_ ('Phone'),max_length =50 ,default ='+962-6-1234567')
    email =models .EmailField (_ ('Email'),default ='info@ammanhotel.jo')
    website =models .URLField (_ ('Website'),blank =True )
    check_in_time =models .TimeField (_ ('Check-in Time'),default ='14:00')
    check_out_time =models .TimeField (_ ('Check-out Time'),default ='12:00')
    currency =models .CharField (_ ('Currency'),max_length =3 ,default ='JOD')
    tax_rate =models .DecimalField (_ ('Tax Rate'),max_digits =5 ,decimal_places =2 ,default =16.00 )
    logo =models .ImageField (_ ('Logo'),upload_to ='hotel/',blank =True ,null =True )

    class Meta :
        verbose_name =_ ('Hotel Settings')
        verbose_name_plural =_ ('Hotel Settings')

    def __str__ (self ):
        return self .name 

    def save (self ,*args ,**kwargs ):
        if not self .pk and HotelSettings .objects .exists ():
            raise ValueError (_ ('Only one hotel settings instance can exist'))
        super ().save (*args ,**kwargs )

    @classmethod 
    def get_settings (cls ):
        settings ,created =cls .objects .get_or_create (id =1 )
        return settings 
