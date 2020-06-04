from django.contrib import admin
from .models import (
    Expert, 
    Practice, 
    Firm, 
    Office,
    Profile
)

admin.site.register(Expert)
admin.site.register(Firm)
admin.site.register(Office)
admin.site.register(Practice)
admin.site.register(Profile)