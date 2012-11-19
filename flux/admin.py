from django.contrib import admin

from flux import models

class AccountAdmin(admin.ModelAdmin):
    pass
class FluxAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.Flux, FluxAdmin)
