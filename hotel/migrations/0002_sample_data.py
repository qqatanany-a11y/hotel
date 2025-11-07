from django .db import migrations 
from django .utils import timezone 

def create_sample_data (apps ,schema_editor ):
    RoomType =apps .get_model ('hotel','RoomType')
    Room =apps .get_model ('hotel','Room')
    HotelSettings =apps .get_model ('hotel','HotelSettings')
    AdditionalService =apps .get_model ('hotel','AdditionalService')

    room_types_data =[
    {
    'name':'single',
    'description':'Comfortable single room with all basic amenities',
    'base_price':45.00 ,
    'max_occupancy':1 ,
    'amenities':'Air Conditioning, Free WiFi, Television, Private Bathroom'
    },
    {
    'name':'double',
    'description':'Spacious double room with beautiful view',
    'base_price':65.00 ,
    'max_occupancy':2 ,
    'amenities':'Air Conditioning, Free WiFi, Television, Private Bathroom, Mini Bar'
    },
    {
    'name':'triple',
    'description':'Triple room suitable for friends or small family',
    'base_price':85.00 ,
    'max_occupancy':3 ,
    'amenities':'Air Conditioning, Free WiFi, Television, Private Bathroom, Mini Bar, Work Desk'
    },
    {
    'name':'family',
    'description':'Large family room with separate seating area',
    'base_price':120.00 ,
    'max_occupancy':4 ,
    'amenities':'Air Conditioning, Free WiFi, Television, Private Bathroom, Mini Bar, Seating Area, Room Service'
    },
    {
    'name':'suite',
    'description':'Luxury suite with separate bedroom and living room',
    'base_price':180.00 ,
    'max_occupancy':2 ,
    'amenities':'Air Conditioning, Free WiFi, Television, Private Bathroom, Mini Bar, Separate Living Room, Room Service, Jacuzzi'
    }
    ]

    for room_type_data in room_types_data :
        room_type ,created =RoomType .objects .get_or_create (
        name =room_type_data ['name'],
        defaults =room_type_data 
        )

    room_numbers =[
    (101 ,1 ,'single'),(102 ,1 ,'single'),(103 ,1 ,'double'),(104 ,1 ,'double'),
    (201 ,2 ,'double'),(202 ,2 ,'double'),(203 ,2 ,'triple'),(204 ,2 ,'triple'),
    (301 ,3 ,'family'),(302 ,3 ,'family'),(303 ,3 ,'suite'),(304 ,3 ,'suite'),
    (401 ,4 ,'suite'),(402 ,4 ,'suite'),(403 ,4 ,'family'),(404 ,4 ,'triple'),
    ]

    for room_num ,floor ,room_type_name in room_numbers :
        try :
            room_type =RoomType .objects .get (name =room_type_name )
            Room .objects .get_or_create (
            room_number =str (room_num ),
            defaults ={
            'room_type':room_type ,
            'floor':floor ,
            'status':'available',
            'is_active':True 
            }
            )
        except RoomType .DoesNotExist :
            pass 

    HotelSettings .objects .get_or_create (
    id =1 ,
    defaults ={
    'name':'Golden Amman Hotel',
    'description':'Luxury hotel in the heart of Amman offering the best hospitality services and comfortable accommodation',
    'address':'Queen Rania Street, Amman, Jordan',
    'phone':'+962-6-1234567',
    'email':'info@ammanhotel.jo',
    'currency':'JOD',
    'tax_rate':16.00 
    }
    )

    services_data =[
    {'name':'Room Breakfast','description':'Luxury breakfast meal served in your room','price':15.00 ,'icon':'utensils'},
    {'name':'Airport Transport Service','description':'Comfortable transport to and from the airport','price':25.00 ,'icon':'car'},
    {'name':'Laundry Service','description':'Washing and ironing clothes','price':10.00 ,'icon':'tshirt'},
    {'name':'Swimming Pool Access','description':'Access to swimming pool and spa area','price':8.00 ,'icon':'swimming-pool'},
    ]

    for service_data in services_data :
        AdditionalService .objects .get_or_create (
        name =service_data ['name'],
        defaults =service_data 
        )


def reverse_sample_data (apps ,schema_editor ):
    pass 


class Migration (migrations .Migration ):
    dependencies =[
    ('hotel','0001_initial'),
    ]

    operations =[
    migrations .RunPython (create_sample_data ,reverse_sample_data ),
    ]