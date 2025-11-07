from django .contrib import admin 
from .models import RoomType ,Room ,Guest ,Booking ,BookingService ,AdditionalService ,Payment ,HotelSettings 



@admin .register (RoomType )
class RoomTypeAdmin (admin .ModelAdmin ):
    list_display =['name','base_price','max_occupancy']
    list_filter =['name']
    search_fields =['name','description']


@admin .register (Room )
class RoomAdmin (admin .ModelAdmin ):
    list_display =['room_number','room_type','floor','status','is_active']
    list_filter =['room_type','floor','status','is_active']
    search_fields =['room_number']
    list_editable =['status']


@admin .register (Guest )
class GuestAdmin (admin .ModelAdmin ):
    list_display =['user','phone','nationality','created_at']
    list_filter =['nationality','created_at']
    search_fields =['user__username','user__email','phone','national_id']


@admin .register (Booking )
class BookingAdmin (admin .ModelAdmin ):
    list_display =['booking_id','guest','room','check_in_date','check_out_date','status','total_amount']
    list_filter =['status','check_in_date','created_at']
    search_fields =['booking_id','guest__user__username']
    readonly_fields =['booking_id']


@admin .register (BookingService )
class BookingServiceAdmin (admin .ModelAdmin ):
    list_display =['booking','service','quantity','total_price']


@admin .register (AdditionalService )
class AdditionalServiceAdmin (admin .ModelAdmin ):
    list_display =['name','price','is_active']
    list_filter =['is_active']
    list_editable =['is_active']


@admin .register (Payment )
class PaymentAdmin (admin .ModelAdmin ):
    list_display =['booking','amount','payment_method','status','created_at']
    list_filter =['payment_method','status','created_at']


@admin .register (HotelSettings )
class HotelSettingsAdmin (admin .ModelAdmin ):
    list_display =['name','currency','tax_rate']

    def has_add_permission (self ,request ):
        return not HotelSettings .objects .exists ()

    def has_delete_permission (self ,request ,obj =None ):
        return False 

admin .site .site_header ="Hotel Management"
admin .site .site_title ="Hotel Management"
admin .site .index_title ="Hotel Management"
