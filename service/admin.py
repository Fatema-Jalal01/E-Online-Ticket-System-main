from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from service.models import Bus,Air,Train,Bususer,userinfo,Seat,Trainseat,Account,Planeseat,bus_payment,train_payment,air_payment
class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Accounts'

class CustomizedUserAdmin(UserAdmin):
    inlines = (AccountInline, )


admin.site.register (Bus)
admin.site.register (Air)
admin.site.register (Train)
admin.site.register (Bususer)
admin.site.register (userinfo)
admin.site.register (Seat)
admin.site.register (Trainseat)
admin.site.register (bus_payment)
admin.site.register (Planeseat)
admin.site.register (train_payment)
admin.site.register (air_payment)



admin.site.unregister(User)
admin.site.register (User,CustomizedUserAdmin)



