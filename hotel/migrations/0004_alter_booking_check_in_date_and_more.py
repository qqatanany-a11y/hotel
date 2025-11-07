


from django .db import migrations ,models 


class Migration (migrations .Migration ):

    dependencies =[
    ('hotel','0003_alter_guest_nationality_alter_hotelsettings_address_and_more'),
    ]

    operations =[
    migrations .AlterField (
    model_name ='booking',
    name ='check_in_date',
    field =models .DateField (verbose_name ='Arrival Date'),
    ),
    migrations .AlterField (
    model_name ='booking',
    name ='check_out_date',
    field =models .DateField (verbose_name ='Departure Date'),
    ),
    migrations .AlterField (
    model_name ='booking',
    name ='updated_at',
    field =models .DateTimeField (auto_now =True ,verbose_name ='Last Update'),
    ),
    migrations .AlterField (
    model_name ='hotelsettings',
    name ='name',
    field =models .CharField (default ='Amman Golden Hotel',max_length =200 ,verbose_name ='Hotel Name'),
    ),
    migrations .AlterField (
    model_name ='room',
    name ='status',
    field =models .CharField (choices =[('available','Available'),('occupied','Occupied'),('maintenance','Maintenance'),('out_of_order','Out of Order')],default ='available',max_length =20 ,verbose_name ='Status'),
    ),
    migrations .AlterField (
    model_name ='roomtype',
    name ='name',
    field =models .CharField (choices =[('single','Single Room'),('double','Double Room'),('triple','Triple Room'),('quad','Quadruple Room'),('suite','Suite'),('deluxe','Deluxe Room'),('family','Family Room')],max_length =50 ,unique =True ,verbose_name ='Type Name'),
    ),
    ]
