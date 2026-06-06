from django.contrib import admin
from .models import Client, Interaction


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'email', 'telephone', 'statut', 'categorie', 'ville', 'chiffre_affaires', 'date_creation']
    list_filter = ['statut', 'categorie', 'pays']
    search_fields = ['nom', 'prenom', 'email', 'telephone', 'ville', 'entreprise']
    readonly_fields = ['date_creation', 'date_modification']
    ordering = ['-date_creation']
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'email', 'telephone', 'date_naissance')
        }),
        ('Adresse', {
            'fields': ('adresse', 'ville', 'code_postal', 'pays')
        }),
        ('Informations commerciales', {
            'fields': ('statut', 'categorie', 'entreprise', 'chiffre_affaires')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ['client', 'type_interaction', 'date', 'utilisateur']
    list_filter = ['type_interaction']
    search_fields = ['client__nom', 'client__prenom', 'description']
    ordering = ['-date']
