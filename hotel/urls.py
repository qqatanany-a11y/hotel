from django .urls import path 
from django .contrib .auth import views as auth_views 
from .import views 

urlpatterns =[
path ('',views .home ,name ='home'),
path ('rooms/',views .room_types ,name ='room_types'),
path ('rooms/<int:room_type_id>/',views .room_detail ,name ='room_detail'),
path ('search/',views .search_rooms ,name ='search_rooms'),
path ('about/',views .about ,name ='about'),
path ('contact/',views .contact ,name ='contact'),

path ('book/<int:room_id>/',views .book_room ,name ='book_room'),
path ('booking/<str:booking_id>/',views .booking_detail ,name ='booking_detail'),
path ('payment/<str:booking_id>/',views .payment_page ,name ='payment_page'),
path ('my-bookings/',views .my_bookings ,name ='my_bookings'),
path ('cancel-booking/<str:booking_id>/',views .cancel_booking ,name ='cancel_booking'),

path ('register/',views .register ,name ='register'),
path ('login/',auth_views .LoginView .as_view (template_name ='registration/login.html'),name ='login'),
path ('logout/',auth_views .LogoutView .as_view (http_method_names =['get','post']),name ='logout'),
path ('profile/',views .profile ,name ='profile'),

path ('password-reset/',
auth_views .PasswordResetView .as_view (template_name ='registration/password_reset.html'),
name ='password_reset'),
path ('password-reset/done/',
auth_views .PasswordResetDoneView .as_view (template_name ='registration/password_reset_done.html'),
name ='password_reset_done'),
path ('reset/<uidb64>/<token>/',
auth_views .PasswordResetConfirmView .as_view (template_name ='registration/password_reset_confirm.html'),
name ='password_reset_confirm'),
path ('reset/done/',
auth_views .PasswordResetCompleteView .as_view (template_name ='registration/password_reset_complete.html'),
name ='password_reset_complete'),

path ('admin-panel/',views .admin_dashboard ,name ='admin_dashboard'),
path ('admin-panel/bookings/',views .admin_bookings ,name ='admin_bookings'),
path ('admin-panel/booking/<str:booking_id>/',views .admin_booking_detail ,name ='admin_booking_detail'),
path ('admin-panel/add-booking/',views .admin_add_booking ,name ='admin_add_booking'),
path ('admin-panel/rooms/',views .admin_rooms ,name ='admin_rooms'),
path ('admin-panel/guests/',views .admin_guests ,name ='admin_guests'),
path ('admin-panel/reports/',views .admin_reports ,name ='admin_reports'),

path ('api/room-availability/',views .api_room_availability ,name ='api_room_availability'),
]