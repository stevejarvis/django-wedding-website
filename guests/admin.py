from django.contrib import admin
from .models import Guest, Party


class GuestInline(admin.TabularInline):
    model = Guest
    fields = ('first_name', 'last_name', 'email', 'is_attending', 'has_plus_one', 'plus_one_attending', 'is_child', 'home_address')
    readonly_fields = ('first_name', 'last_name', 'email')


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'save_the_date_sent', 'invitation_sent', 'is_attending')
    list_filter = ('category', 'is_attending')
    inlines = [GuestInline]


class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'party', 'email', 'is_attending', 'plus_one_attending')
    list_filter = ('is_attending', 'is_child', 'has_plus_one')


admin.site.register(Party, PartyAdmin)
admin.site.register(Guest, GuestAdmin)
