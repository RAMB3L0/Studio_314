from django.db import models
from django.utils import timezone


class Client(models.Model):
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('prospect', 'Prospect'),
        ('vip', 'VIP'),
    ]

    CATEGORIE_CHOICES = [
        ('particulier', 'Particulier'),
        ('entreprise', 'Entreprise'),
        ('association', 'Association'),
        ('administration', 'Administration'),
    ]

    # Informations personnelles
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    email = models.EmailField(unique=True, verbose_name="Email")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    
    # Adresse
    adresse = models.CharField(max_length=255, blank=True, null=True, verbose_name="Adresse")
    ville = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ville")
    code_postal = models.CharField(max_length=10, blank=True, null=True, verbose_name="Code Postal")
    pays = models.CharField(max_length=100, default="France", verbose_name="Pays")
    
    # Informations commerciales
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='actif', verbose_name="Statut")
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, default='particulier', verbose_name="Catégorie")
    entreprise = models.CharField(max_length=200, blank=True, null=True, verbose_name="Entreprise")
    
    # Financier
    chiffre_affaires = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Chiffre d'affaires (€)")
    
    # Dates
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    date_naissance = models.DateField(blank=True, null=True, verbose_name="Date de naissance")
    
    # Notes
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"

    def get_adresse_complete(self):
        parts = []
        if self.adresse:
            parts.append(self.adresse)
        if self.code_postal and self.ville:
            parts.append(f"{self.code_postal} {self.ville}")
        elif self.ville:
            parts.append(self.ville)
        if self.pays:
            parts.append(self.pays)
        return ", ".join(parts) if parts else "—"


class Interaction(models.Model):
    TYPE_CHOICES = [
        ('appel', 'Appel téléphonique'),
        ('email', 'Email'),
        ('reunion', 'Réunion'),
        ('visite', 'Visite'),
        ('autre', 'Autre'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='interactions', verbose_name="Client")
    type_interaction = models.CharField(max_length=20, choices=TYPE_CHOICES, default='appel', verbose_name="Type")
    date = models.DateTimeField(default=timezone.now, verbose_name="Date")
    description = models.TextField(verbose_name="Description")
    utilisateur = models.CharField(max_length=100, blank=True, null=True, verbose_name="Utilisateur")

    class Meta:
        verbose_name = "Interaction"
        verbose_name_plural = "Interactions"
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_type_interaction_display()} - {self.client} - {self.date.strftime('%d/%m/%Y')}"
