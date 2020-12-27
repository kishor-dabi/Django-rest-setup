from django.contrib import admin

# Register your models here.
from .models import User, UserManager, Part, Car, Doctor, DoctorType

# admin.site.register(UserManager)
admin.site.register(User)
# admin.site.register(UserProfile)
admin.site.register(Part)
admin.site.register(Car)
admin.site.register(Doctor)
admin.site.register(DoctorType)