from django.contrib import admin

# Register your models here.
class scoopAdmin(admin.ModelAdmin):
    search_fields = ['id_detalle_actividad', 'horometro', 'numero_cucharas','material','toneladas']
    list_display = ('id_detalle_actividad', 'horometro', 'numero_cucharas','material','toneladas')

admin.site.register(models.operador,operadorAdmin)