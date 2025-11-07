


from django .db import migrations ,models 


class Migration (migrations .Migration ):

    dependencies =[
    ('hotel','0004_alter_booking_check_in_date_and_more'),
    ]

    operations =[
    migrations .AlterField (
    model_name ='booking',
    name ='status',
    field =models .CharField (choices =[('pending','Waiting for payment'),('confirmed','Confirmed'),('checked_in','Checked In'),('checked_out','Checked Out'),('cancelled','Cancelled'),('no_show','No Show')],default ='pending',max_length =20 ,verbose_name ='Booking Status'),
    ),
    migrations .AlterField (
    model_name ='payment',
    name ='status',
    field =models .CharField (choices =[('pending','Waiting for payment'),('completed','Completed'),('failed','Failed'),('refunded','Refunded')],default ='pending',max_length =20 ,verbose_name ='Payment Status'),
    ),
    ]
