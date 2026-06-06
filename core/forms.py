from django import forms
from .models import Client, Interaction


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'nom', 'prenom', 'email', 'telephone',
            'adresse', 'ville', 'code_postal', 'pays',
            'statut', 'categorie', 'entreprise',
            'chiffre_affaires', 'date_naissance', 'notes'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du client'
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom du client'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemple.com'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+33 6 00 00 00 00'
            }),
            'adresse': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse complète'
            }),
            'ville': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ville'
            }),
            'code_postal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '75000'
            }),
            'pays': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'France'
            }),
            'statut': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'categorie': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'entreprise': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de l\'entreprise'
            }),
            'chiffre_affaires': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'date_naissance': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notes supplémentaires...'
            }),
        }
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'email': 'Email',
            'telephone': 'Téléphone',
            'adresse': 'Adresse',
            'ville': 'Ville',
            'code_postal': 'Code Postal',
            'pays': 'Pays',
            'statut': 'Statut',
            'categorie': 'Catégorie',
            'entreprise': 'Entreprise',
            'chiffre_affaires': "Chiffre d'affaires (€)",
            'date_naissance': 'Date de naissance',
            'notes': 'Notes',
        }


class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['type_interaction', 'date', 'description', 'utilisateur']
        widgets = {
            'type_interaction': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description de l\'interaction...'
            }),
            'utilisateur': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de l\'utilisateur'
            }),
        }


class ClientSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'search-input',
            'placeholder': 'Rechercher un client...',
            'id': 'searchInput'
        })
    )
    statut = forms.ChoiceField(
        required=False,
        choices=[('', 'Tous les statuts')] + Client.STATUT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-select'})
    )
    categorie = forms.ChoiceField(
        required=False,
        choices=[('', 'Toutes catégories')] + Client.CATEGORIE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-select'})
    )
