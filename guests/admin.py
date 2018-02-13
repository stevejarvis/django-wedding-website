from django.contrib import admin
from .models import Guest, Party


class GuestInline(admin.TabularInline):
    model = Guest
    fields = ('first_name', 'last_name', 'email', 'is_attending', 'is_child')
    readonly_fields = ('first_name', 'last_name', 'email')


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'relation', 'save_the_date_sent', 'invitation_sent', 'rehearsal_dinner', 'is_attending')
    list_filter = ('relation', 'is_attending', 'rehearsal_dinner')
    inlines = [GuestInline]


class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'party', 'email', 'is_attending', 'is_child')
    list_filter = ('is_attending', 'is_child', 'party__rehearsal_dinner')


admin.site.register(Party, PartyAdmin)
admin.site.register(Guest, GuestAdmin)
