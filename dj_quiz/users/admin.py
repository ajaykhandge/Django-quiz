from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Participant

# Register your models here.
class ParticipantInline(admin.StackedInline):
    model = Participant
    can_delete = False
    verbose_name_plural = 'participant'

class UserAdmin(BaseUserAdmin):
    inlines = (ParticipantInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Participant)

 