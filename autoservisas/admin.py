from django.contrib import admin
from .models import (Modelis, Klientas, Gamintojas, Car,
                     Paslaugos, Uzsakymas, PaslaugaUzsakymas, UzsakymasReview, Profile)


class PaslaugaUzsakymasInline(admin.TabularInline):
    model = PaslaugaUzsakymas
    extra = 1
    fields = ('paslauga', 'paslaugu_kiekis')


class UzsakymasAdmin(admin.ModelAdmin):
    list_display = ('data', 'uzsakovas', 'due_back', 'status', 'bendra_kaina', 'display_cars')
    list_editable = ('uzsakovas', 'due_back')
    fieldsets = (
        ('Data', {'fields': ['data', 'due_back']}),
        # ('Grąžinimo data', {'fields': ['due_back']}),
        ('Status', {'fields': ['status']}),
        ('Automobilis', {'fields': ['automobilis']}),
        ('Užsakovas', {'fields': ['uzsakovas']}),
        # klientas field ... ffffffff
    )
    inlines = (PaslaugaUzsakymasInline,)


class CarAdmin(admin.ModelAdmin):
    list_display = ('klientas', 'modelis', 'autonr')
    list_filter = ('klientas__f_name', 'modelis__modelis')
    search_fields = ('autonr', 'modelis__gamintojas__gamintojas')


class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ('paslauga', 'kaina')


admin.site.register(Modelis)
admin.site.register(Klientas)
admin.site.register(Gamintojas)
admin.site.register(Car, CarAdmin)
admin.site.register(Paslaugos, PaslaugaAdmin)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(PaslaugaUzsakymas)
admin.site.register(UzsakymasReview)
admin.site.register(Profile)
