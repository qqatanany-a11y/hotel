


from django .conf import settings 
import django .core .validators 
from django .db import migrations ,models 
import django .db .models .deletion 


class Migration (migrations .Migration ):

    initial =True 

    dependencies =[
    migrations .swappable_dependency (settings .AUTH_USER_MODEL ),
    ]

    operations =[
    migrations .CreateModel (
    name ='AdditionalService',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('name',models .CharField (max_length =100 ,verbose_name ='Service Name')),
    ('description',models .TextField (blank =True ,verbose_name ='Description')),
    ('price',models .DecimalField (decimal_places =2 ,max_digits =8 ,verbose_name ='Price')),
    ('is_active',models .BooleanField (default =True ,verbose_name ='Active')),
    ('icon',models .CharField (blank =True ,help_text ='Font Awesome icon name',max_length =50 ,verbose_name ='Icon')),
    ],
    options ={
    'verbose_name':'Additional Service',
    'verbose_name_plural':'Additional Services',
    'ordering':['name'],
    },
    ),
    migrations .CreateModel (
    name ='Booking',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('booking_id',models .CharField (editable =False ,max_length =20 ,unique =True ,verbose_name ='Booking ID')),
    ('check_in_date',models .DateField (verbose_name ='Check-in Date')),
    ('check_out_date',models .DateField (verbose_name ='Check-out Date')),
    ('adults',models .PositiveIntegerField (default =1 ,validators =[django .core .validators .MinValueValidator (1 )],verbose_name ='Adults')),
    ('children',models .PositiveIntegerField (default =0 ,validators =[django .core .validators .MinValueValidator (0 )],verbose_name ='Children')),
    ('total_amount',models .DecimalField (decimal_places =2 ,max_digits =10 ,verbose_name ='Total Amount')),
    ('status',models .CharField (choices =[('pending','Pending'),('confirmed','Confirmed'),('checked_in','Checked In'),('checked_out','Checked Out'),('cancelled','Cancelled'),('no_show','No Show')],default ='pending',max_length =20 ,verbose_name ='Booking Status')),
    ('special_requests',models .TextField (blank =True ,verbose_name ='Special Requests')),
    ('created_at',models .DateTimeField (auto_now_add =True ,verbose_name ='Booking Date')),
    ('updated_at',models .DateTimeField (auto_now =True ,verbose_name ='Last Updated')),
    ],
    options ={
    'verbose_name':'Booking',
    'verbose_name_plural':'Bookings',
    'ordering':['-created_at'],
    },
    ),
    migrations .CreateModel (
    name ='HotelSettings',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('name',models .CharField (max_length =200 ,verbose_name ='Hotel Name')),
    ('description',models .TextField (blank =True ,verbose_name ='Description')),
    ('address',models .TextField (verbose_name ='Address')),
    ('phone',models .CharField (max_length =50 ,verbose_name ='Phone')),
    ('email',models .EmailField (max_length =254 ,verbose_name ='Email')),
    ('website',models .URLField (blank =True ,verbose_name ='Website')),
    ('check_in_time',models .TimeField (default ='14:00',verbose_name ='Check-in Time')),
    ('check_out_time',models .TimeField (default ='12:00',verbose_name ='Check-out Time')),
    ('currency',models .CharField (default ='SAR',max_length =3 ,verbose_name ='Currency')),
    ('tax_rate',models .DecimalField (decimal_places =2 ,default =15.0 ,max_digits =5 ,verbose_name ='Tax Rate')),
    ('logo',models .ImageField (blank =True ,null =True ,upload_to ='hotel/',verbose_name ='Logo')),
    ],
    options ={
    'verbose_name':'Hotel Settings',
    'verbose_name_plural':'Hotel Settings',
    },
    ),
    migrations .CreateModel (
    name ='RoomType',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('name',models .CharField (choices =[('single','Single Room'),('double','Double Room'),('triple','Triple Room'),('quad','Quad Room'),('suite','Suite'),('deluxe','Deluxe Room'),('family','Family Room')],max_length =50 ,unique =True ,verbose_name ='Type Name')),
    ('description',models .TextField (blank =True ,verbose_name ='Description')),
    ('base_price',models .DecimalField (decimal_places =2 ,max_digits =10 ,verbose_name ='Base Price')),
    ('max_occupancy',models .PositiveIntegerField (verbose_name ='Maximum Occupancy')),
    ('image',models .ImageField (blank =True ,null =True ,upload_to ='room_types/',verbose_name ='Image')),
    ('amenities',models .TextField (help_text ='Enter amenities separated by commas',verbose_name ='Amenities')),
    ],
    options ={
    'verbose_name':'Room Type',
    'verbose_name_plural':'Room Types',
    'ordering':['base_price'],
    },
    ),
    migrations .CreateModel (
    name ='Room',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('room_number',models .CharField (max_length =10 ,unique =True ,verbose_name ='Room Number')),
    ('floor',models .PositiveIntegerField (verbose_name ='Floor')),
    ('status',models .CharField (choices =[('available','Available'),('occupied','Occupied'),('maintenance','Under Maintenance'),('out_of_order','Out of Order')],default ='available',max_length =20 ,verbose_name ='Status')),
    ('is_active',models .BooleanField (default =True ,verbose_name ='Active')),
    ('notes',models .TextField (blank =True ,verbose_name ='Notes')),
    ('room_type',models .ForeignKey (on_delete =django .db .models .deletion .CASCADE ,to ='hotel.roomtype',verbose_name ='Room Type')),
    ],
    options ={
    'verbose_name':'Room',
    'verbose_name_plural':'Rooms',
    'ordering':['floor','room_number'],
    },
    ),
    migrations .CreateModel (
    name ='Payment',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('amount',models .DecimalField (decimal_places =2 ,max_digits =10 ,verbose_name ='Amount')),
    ('payment_method',models .CharField (choices =[('cash','Cash'),('card','Credit Card'),('bank_transfer','Bank Transfer'),('online','Online Payment')],max_length =20 ,verbose_name ='Payment Method')),
    ('status',models .CharField (choices =[('pending','Pending'),('completed','Completed'),('failed','Failed'),('refunded','Refunded')],default ='pending',max_length =20 ,verbose_name ='Payment Status')),
    ('transaction_id',models .CharField (blank =True ,max_length =100 ,verbose_name ='Transaction ID')),
    ('notes',models .TextField (blank =True ,verbose_name ='Notes')),
    ('created_at',models .DateTimeField (auto_now_add =True ,verbose_name ='Payment Date')),
    ('booking',models .ForeignKey (on_delete =django .db .models .deletion .CASCADE ,related_name ='payments',to ='hotel.booking',verbose_name ='Booking')),
    ],
    options ={
    'verbose_name':'Payment',
    'verbose_name_plural':'Payments',
    'ordering':['-created_at'],
    },
    ),
    migrations .CreateModel (
    name ='Guest',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('phone',models .CharField (max_length =20 ,verbose_name ='Phone Number')),
    ('national_id',models .CharField (blank =True ,max_length =20 ,null =True ,unique =True ,verbose_name ='National ID')),
    ('nationality',models .CharField (max_length =50 ,verbose_name ='Nationality')),
    ('date_of_birth',models .DateField (blank =True ,null =True ,verbose_name ='Date of Birth')),
    ('address',models .TextField (blank =True ,verbose_name ='Address')),
    ('emergency_contact',models .CharField (blank =True ,max_length =100 ,verbose_name ='Emergency Contact')),
    ('emergency_phone',models .CharField (blank =True ,max_length =20 ,verbose_name ='Emergency Phone')),
    ('created_at',models .DateTimeField (auto_now_add =True ,verbose_name ='Registration Date')),
    ('user',models .OneToOneField (on_delete =django .db .models .deletion .CASCADE ,to =settings .AUTH_USER_MODEL ,verbose_name ='User')),
    ],
    options ={
    'verbose_name':'Guest',
    'verbose_name_plural':'Guests',
    'ordering':['-created_at'],
    },
    ),
    migrations .AddField (
    model_name ='booking',
    name ='guest',
    field =models .ForeignKey (on_delete =django .db .models .deletion .CASCADE ,related_name ='bookings',to ='hotel.guest',verbose_name ='Guest'),
    ),
    migrations .AddField (
    model_name ='booking',
    name ='room',
    field =models .ForeignKey (on_delete =django .db .models .deletion .CASCADE ,related_name ='bookings',to ='hotel.room',verbose_name ='Room'),
    ),
    migrations .CreateModel (
    name ='BookingService',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('quantity',models .PositiveIntegerField (default =1 ,verbose_name ='Quantity')),
    ('total_price',models .DecimalField (decimal_places =2 ,max_digits =8 ,verbose_name ='Total Price')),
    ('booking',models .ForeignKey (on_delete =django .db .models .deletion .CASCADE ,related_name ='services',to ='hotel.booking',verbose_name ='Booking')),
    ('service',models .ForeignKey (on_delete =django .db .models .deletion .CASCADE ,to ='hotel.additionalservice',verbose_name ='Service')),
    ],
    options ={
    'verbose_name':'Booking Service',
    'verbose_name_plural':'Booking Services',
    'unique_together':{('booking','service')},
    },
    ),
    ]
