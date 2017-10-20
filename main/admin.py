from django.contrib import admin
from main.models import SourceSet, UserSet, FormStatusSet, PTSet, SHSet, CLSet, CCSet

class SourceSetView(admin.ModelAdmin):
    list_display = ('id', 'ehub_id', 'type', 'email', 'commission', 'name', 'contact_num', 'rating', 'datetime')
    readonly_fields = ['password']

class UserSetView(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'email', 'name', 'dob', 'gender', 'contact_num', 'datetime')
    readonly_fields = ['password']

class FormStatusSetView(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'form_type_object', 'status', 'last_modified', 'datetime')

class PTSetView(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'source_id', 'course', 'fee', 'fee_type', 'seats_left', 'is_link_active', 'last_date_to_apply', 'datetime')

class SHSetView(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'source_id', 'till_class', 'fee', 'fee_type', 'seats_left', 'is_link_active', 'last_date_to_apply', 'datetime')

admin.site.register(SourceSet, SourceSetView)
admin.site.register(UserSet, UserSetView)
admin.site.register(FormStatusSet, FormStatusSetView)
admin.site.register(PTSet, PTSetView)
admin.site.register(SHSet, SHSetView)
admin.site.register(CLSet, PTSetView)
admin.site.register(CCSet, PTSetView)