from django import forms 
from django .contrib .auth .forms import UserCreationForm 
from django .contrib .auth .models import User 
from django .utils .translation import gettext_lazy as _ 
from django .core .exceptions import ValidationError 
from crispy_forms .helper import FormHelper 
from crispy_forms .layout import Layout ,Row ,Column ,Submit ,HTML 
from crispy_forms .bootstrap import FormActions 
from datetime import date ,timedelta 
from .models import Guest ,Booking ,Room ,RoomType ,AdditionalService 
from email_validator import validate_email ,EmailNotValidError 
import dns .resolver 

class CustomUserCreationForm (UserCreationForm ):
    email =forms .EmailField (required =True )

    class Meta :
        model =User 
        fields =("username","email","password1","password2")

    def clean_email (self ):
        email =self .cleaned_data .get ('email')


        try :

            valid =validate_email (email )
            email =valid .email 
        except EmailNotValidError :
            raise forms .ValidationError (_ ("Please enter a valid email address."))


        try :
            domain =email .split ('@')[1 ]
            mx_records =dns .resolver .resolve (domain ,'MX')
            if not mx_records :
                raise forms .ValidationError (_ ("This email domain does not exist."))
        except (dns .resolver .NXDOMAIN ,dns .resolver .NoAnswer ,Exception ):
            raise forms .ValidationError (_ ("This email domain does not exist or cannot receive emails."))


        if User .objects .filter (email =email ).exists ():
            raise forms .ValidationError (_ ("An account with this email already exists."))

        return email 

class GuestProfileForm (forms .ModelForm ):
    class Meta :
        model =Guest 
        fields =['phone','national_id','nationality','date_of_birth',
        'address','emergency_contact','emergency_phone']
        labels ={
        'phone':_ ('Phone Number'),
        'national_id':_ ('National ID'),
        'nationality':_ ('Nationality'),
        'date_of_birth':_ ('Date of Birth'),
        'address':_ ('Address'),
        'emergency_contact':_ ('Emergency Contact'),
        'emergency_phone':_ ('Emergency Phone'),
        }
        widgets ={
        'phone':forms .TextInput (attrs ={
        'class':'form-control',
        'maxlength':'10',
        'inputmode':'numeric',
        'oninput':'this.value=this.value.replace(/[^0-9]/g,"").slice(0,10);',
        'title':_ ('Phone number must be exactly 10 digits')
        }),
        'national_id':forms .TextInput (attrs ={
        'class':'form-control',
        'maxlength':'12',
        'inputmode':'numeric',
        'oninput':'this.value=this.value.replace(/[^0-9]/g,"").slice(0,12);',
        'title':_ ('National ID must be exactly 12 digits')
        }),
        'nationality':forms .TextInput (attrs ={'class':'form-control'}),
        'date_of_birth':forms .DateInput (attrs ={'class':'form-control','type':'date'}),
        'address':forms .Textarea (attrs ={'class':'form-control','rows':3 }),
        'emergency_contact':forms .TextInput (attrs ={'class':'form-control'}),
        'emergency_phone':forms .TextInput (attrs ={
        'class':'form-control',
        'maxlength':'10',
        'inputmode':'numeric',
        'oninput':'this.value=this.value.replace(/[^0-9]/g,"").slice(0,10);',
        'title':_ ('Emergency phone must be exactly 10 digits')
        }),
        }

    def __init__ (self ,*args ,**kwargs ):
        super ().__init__ (*args ,**kwargs )
        self .helper =FormHelper ()
        self .helper .layout =Layout (
        Row (
        Column ('phone',css_class ='form-group col-md-6 mb-0'),
        Column ('national_id',css_class ='form-group col-md-6 mb-0'),
        css_class ='form-row'
        ),
        Row (
        Column ('nationality',css_class ='form-group col-md-6 mb-0'),
        Column ('date_of_birth',css_class ='form-group col-md-6 mb-0'),
        css_class ='form-row'
        ),
        'address',
        Row (
        Column ('emergency_contact',css_class ='form-group col-md-6 mb-0'),
        Column ('emergency_phone',css_class ='form-group col-md-6 mb-0'),
        css_class ='form-row'
        ),
        FormActions (
        Submit ('submit',_ ('Save Changes'),css_class ='btn btn-primary')
        )
        )


    def clean_phone (self ):
        phone =self .cleaned_data .get ('phone','')
        if not phone .isdigit ():
            raise ValidationError (_ ("Phone number must contain digits only."))
        if len (phone )!=10 :
            raise ValidationError (_ ("Phone number must be exactly 10 digits long."))
        return phone 


    def clean_national_id (self ):
        national_id =self .cleaned_data .get ('national_id','')
        if not national_id .isdigit ():
            raise ValidationError (_ ("National ID must contain digits only."))
        if len (national_id )!=12 :
            raise ValidationError (_ ("National ID must be exactly 12 digits long."))
        return national_id 


    def clean_emergency_phone (self ):
        emergency_phone =self .cleaned_data .get ('emergency_phone','')
        if not emergency_phone .isdigit ():
            raise ValidationError (_ ("Emergency phone must contain digits only."))
        if len (emergency_phone )!=10 :
            raise ValidationError (_ ("Emergency phone must be exactly 10 digits long."))
        return emergency_phone 

class RoomSearchForm (forms .Form ):
    check_in_date =forms .DateField (
    label =_ ('Arrival Date'),
    widget =forms .DateInput (attrs ={'class':'form-control','type':'date'}),
    initial =lambda :date .today ()
    )
    check_out_date =forms .DateField (
    label =_ ('Departure Date'),
    widget =forms .DateInput (attrs ={'class':'form-control','type':'date'}),
    initial =lambda :date .today ()+timedelta (days =1 )
    )
    room_type =forms .ModelChoiceField (
    queryset =RoomType .objects .all (),
    label =_ ('Room Type'),
    required =False ,
    empty_label =_ ('All Types'),
    widget =forms .Select (attrs ={'class':'form-control'})
    )
    adults =forms .IntegerField (
    label =_ ('Adults'),
    min_value =1 ,
    max_value =10 ,
    initial =1 ,
    widget =forms .NumberInput (attrs ={'class':'form-control'})
    )
    children =forms .IntegerField (
    label =_ ('Children'),
    min_value =0 ,
    max_value =10 ,
    initial =0 ,
    widget =forms .NumberInput (attrs ={'class':'form-control'})
    )

    def __init__ (self ,*args ,**kwargs ):
        super ().__init__ (*args ,**kwargs )
        self .helper =FormHelper ()
        self .helper .form_method ='get'
        self .helper .layout =Layout (
        Row (
        Column ('check_in_date',css_class ='form-group col-md-3 mb-0'),
        Column ('check_out_date',css_class ='form-group col-md-3 mb-0'),
        Column ('room_type',css_class ='form-group col-md-3 mb-0'),
        Column (
        HTML ('<label>&nbsp;</label>'),
        Submit ('search',_ ('Search'),css_class ='btn btn-primary btn-block'),
        css_class ='form-group col-md-3 mb-0'
        ),
        css_class ='form-row'
        ),
        Row (
        Column ('adults',css_class ='form-group col-md-6 mb-0'),
        Column ('children',css_class ='form-group col-md-6 mb-0'),
        css_class ='form-row'
        )
        )

    def clean (self ):
        cleaned_data =super ().clean ()
        check_in_date =cleaned_data .get ('check_in_date')
        check_out_date =cleaned_data .get ('check_out_date')

        if check_in_date and check_out_date :
            if check_in_date <date .today ():
                raise ValidationError (_ ('Arrival date cannot be in the past'))
            if check_out_date <=check_in_date :
                raise ValidationError (_ ('Departure date must be after arrival date'))

            if (check_out_date -check_in_date ).days >30 :
                raise ValidationError (_ ('Maximum booking period is 30 days'))

        return cleaned_data 


class BookingForm (forms .ModelForm ):
    additional_services =forms .ModelMultipleChoiceField (
    queryset =AdditionalService .objects .filter (is_active =True ),
    label =_ ('Additional Services'),
    required =False ,
    widget =forms .CheckboxSelectMultiple (attrs ={'class':'form-check-input'})
    )

    class Meta :
        model =Booking 
        fields =['check_in_date','check_out_date','adults','children','special_requests']
        labels ={
        'check_in_date':_ ('Arrival Date'),
        'check_out_date':_ ('Departure Date'),
        'adults':_ ('Adults'),
        'children':_ ('Children'),
        'special_requests':_ ('Special Requests'),
        }
        widgets ={
        'check_in_date':forms .DateInput (attrs ={'class':'form-control','type':'date'}),
        'check_out_date':forms .DateInput (attrs ={'class':'form-control','type':'date'}),
        'adults':forms .NumberInput (attrs ={'class':'form-control','min':1 }),
        'children':forms .NumberInput (attrs ={'class':'form-control','min':0 }),
        'special_requests':forms .Textarea (attrs ={'class':'form-control','rows':3 }),
        }

    def __init__ (self ,*args ,**kwargs ):
        self .room =kwargs .pop ('room',None )
        super ().__init__ (*args ,**kwargs )

        if self .room :
            self .fields ['adults'].widget .attrs ['max']=self .room .room_type .max_occupancy 

        self .helper =FormHelper ()
        self .helper .layout =Layout (
        Row (
        Column ('check_in_date',css_class ='form-group col-md-6 mb-0'),
        Column ('check_out_date',css_class ='form-group col-md-6 mb-0'),
        css_class ='form-row'
        ),
        Row (
        Column ('adults',css_class ='form-group col-md-6 mb-0'),
        Column ('children',css_class ='form-group col-md-6 mb-0'),
        css_class ='form-row'
        ),
        'special_requests',
        HTML ('<h5 class="mt-3">Additional Services</h5>'),
        'additional_services',
        FormActions (
        Submit ('submit',_ ('Confirm Booking'),css_class ='btn btn-success btn-lg')
        )
        )

    def clean (self ):
        cleaned_data =super ().clean ()
        check_in_date =cleaned_data .get ('check_in_date')
        check_out_date =cleaned_data .get ('check_out_date')
        adults =cleaned_data .get ('adults')
        children =cleaned_data .get ('children')

        if check_in_date and check_out_date :
            if check_in_date <date .today ():
                raise ValidationError (_ ('Arrival date cannot be in the past'))
            if check_out_date <=check_in_date :
                raise ValidationError (_ ('Departure date must be after arrival date'))

            if (check_out_date -check_in_date ).days >30 :
                raise ValidationError (_ ('Maximum booking period is 30 days'))

        if self .room and adults and children :
            total_guests =adults +children 
            if total_guests >self .room .room_type .max_occupancy :
                raise ValidationError (
                _ ('Number of guests exceeds room maximum capacity ({})').format (
                self .room .room_type .max_occupancy 
                )
                )

            if not self .room .is_available_for_dates (check_in_date ,check_out_date ):
                raise ValidationError (_ ('Room is not available for these dates'))

        return cleaned_data 


class ContactForm (forms .Form ):
    name =forms .CharField (
    label =_ ('Name'),
    max_length =100 ,
    widget =forms .TextInput (attrs ={'class':'form-control'})
    )
    email =forms .EmailField (
    label =_ ('Email'),
    widget =forms .EmailInput (attrs ={'class':'form-control'})
    )
    subject =forms .CharField (
    label =_ ('Subject'),
    max_length =200 ,
    widget =forms .TextInput (attrs ={'class':'form-control'})
    )
    message =forms .CharField (
    label =_ ('Message'),
    widget =forms .Textarea (attrs ={'class':'form-control','rows':5 })
    )

    def __init__ (self ,*args ,**kwargs ):
        super ().__init__ (*args ,**kwargs )
        self .helper =FormHelper ()
        self .helper .layout =Layout (
        Row (
        Column ('name',css_class ='form-group col-md-6 mb-0'),
        Column ('email',css_class ='form-group col-md-6 mb-0'),
        css_class ='form-row'
        ),
        'subject',
        'message',
        FormActions (
        Submit ('submit',_ ('Send Message'),css_class ='btn btn-primary')
        )
        )


class BookingStatusForm (forms .ModelForm ):
    class Meta :
        model =Booking 
        fields =['status']
        widgets ={
        'status':forms .Select (attrs ={'class':'form-control'})
        }


class AdminBookingForm (forms .ModelForm ):
    guest =forms .ModelChoiceField (
    queryset =Guest .objects .all (),
    label =_ ('Guest'),
    widget =forms .Select (attrs ={'class':'form-control'})
    )
    room =forms .ModelChoiceField (
    queryset =Room .objects .filter (is_active =True ,status ='available'),
    label =_ ('Room'),
    widget =forms .Select (attrs ={'class':'form-control'})
    )
    additional_services =forms .ModelMultipleChoiceField (
    queryset =AdditionalService .objects .filter (is_active =True ),
    label =_ ('Additional Services'),
    required =False ,
    widget =forms .CheckboxSelectMultiple ()
    )

    class Meta :
        model =Booking 
        fields =['guest','room','check_in_date','check_out_date','adults','children','special_requests','status']
        widgets ={
        'check_in_date':forms .DateInput (attrs ={'class':'form-control','type':'date'}),
        'check_out_date':forms .DateInput (attrs ={'class':'form-control','type':'date'}),
        'adults':forms .NumberInput (attrs ={'class':'form-control'}),
        'children':forms .NumberInput (attrs ={'class':'form-control'}),
        'special_requests':forms .Textarea (attrs ={'class':'form-control','rows':3 }),
        'status':forms .Select (attrs ={'class':'form-control'}),
        }

    def clean (self ):
        cleaned_data =super ().clean ()
        check_in_date =cleaned_data .get ('check_in_date')
        check_out_date =cleaned_data .get ('check_out_date')
        room =cleaned_data .get ('room')
        adults =cleaned_data .get ('adults')
        children =cleaned_data .get ('children')

        if check_in_date and check_out_date :
            if check_out_date <=check_in_date :
                raise ValidationError (_ ('Departure date must be after arrival date'))

        if room and adults and children :
            total_guests =adults +children 
            if total_guests >room .room_type .max_occupancy :
                raise ValidationError (
                _ ('Number of guests exceeds room maximum capacity')
                )

            if not room .is_available_for_dates (check_in_date ,check_out_date ):
                raise ValidationError (_ ('Room is not available for these dates'))

        return cleaned_data 