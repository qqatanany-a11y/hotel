


from django .db import migrations ,models 


class Migration (migrations .Migration ):

    dependencies =[
    ('hotel','0002_sample_data'),
    ]

    operations =[
    migrations .AlterField (
    model_name ='guest',
    name ='nationality',
    field =models .CharField (default ='Jordanian',max_length =50 ,verbose_name ='Nationality'),
    ),
    migrations .AlterField (
    model_name ='hotelsettings',
    name ='address',
    field =models .TextField (default ='Amman, Jordan',verbose_name ='Address'),
    ),
    migrations .AlterField (
    model_name ='hotelsettings',
    name ='currency',
    field =models .CharField (default ='JOD',max_length =3 ,verbose_name ='Currency'),
    ),
    migrations .AlterField (
    model_name ='hotelsettings',
    name ='email',
    field =models .EmailField (default ='info@ammanhotel.jo',max_length =254 ,verbose_name ='Email'),
    ),
    migrations .AlterField (
    model_name ='hotelsettings',
    name ='name',
    field =models .CharField (default ='Golden Amman Hotel',max_length =200 ,verbose_name ='Hotel Name'),
    ),
    migrations .AlterField (
    model_name ='hotelsettings',
    name ='phone',
    field =models .CharField (default ='+962-6-1234567',max_length =50 ,verbose_name ='Phone'),
    ),
    migrations .AlterField (
    model_name ='hotelsettings',
    name ='tax_rate',
    field =models .DecimalField (decimal_places =2 ,default =16.0 ,max_digits =5 ,verbose_name ='Tax Rate'),
    ),
    ]
