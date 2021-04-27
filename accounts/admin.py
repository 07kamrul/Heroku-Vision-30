from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Profile)
admin.site.register(Member)
admin.site.register(Amount)
admin.site.register(Deposite)
admin.site.register(TotalCost)
admin.site.register(TermsConditions)
admin.site.register(Slider)
admin.site.register(Notice)
admin.site.register(Gallery)
admin.site.register(AboutUs)
admin.site.register(Vision)