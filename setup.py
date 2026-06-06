"""
Script de configuration initiale pour HellFire CRM.
Lance-le avec : python setup.py

Il appliquera les migrations et créera un superutilisateur par défaut.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HellFire.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User

print("=" * 50)
print("  HellFire CRM — Configuration initiale")
print("=" * 50)

# Migrations
print("\n[1/3] Application des migrations...")
call_command('migrate', verbosity=1)

# Superutilisateur par défaut
print("\n[2/3] Création du compte administrateur...")
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@hellfire.crm',
        password='admin123',
        first_name='Admin',
        last_name='HellFire'
    )
    print("  ✓ Compte admin créé (login: admin / mot de passe: admin123)")
else:
    print("  → Compte admin déjà existant.")

# Données de démo
print("\n[3/3] Génération de données de démo...")
from core.models import Client, Interaction
from django.utils import timezone
from decimal import Decimal
import random

if Client.objects.count() == 0:
    clients_data = [
        {'nom': 'Dupont', 'prenom': 'Jean', 'email': 'jean.dupont@example.com', 'telephone': '0601020304',
         'adresse': '12 Rue de la Paix', 'ville': 'Paris', 'code_postal': '75001', 'pays': 'France',
         'statut': 'actif', 'categorie': 'particulier', 'chiffre_affaires': Decimal('15000.00'),
         'notes': 'Client fidèle depuis 2020.'},
        {'nom': 'Martin', 'prenom': 'Sophie', 'email': 'sophie.martin@corp.fr', 'telephone': '0611223344',
         'adresse': '5 Avenue des Champs-Élysées', 'ville': 'Paris', 'code_postal': '75008',
         'pays': 'France', 'statut': 'vip', 'categorie': 'entreprise', 'entreprise': 'Martin Corp',
         'chiffre_affaires': Decimal('85000.00'), 'notes': 'Partenaire stratégique.'},
        {'nom': 'Bernard', 'prenom': 'Luc', 'email': 'luc.bernard@gmail.com', 'telephone': '0699887766',
         'adresse': '3 Rue du Commerce', 'ville': 'Lyon', 'code_postal': '69002', 'pays': 'France',
         'statut': 'prospect', 'categorie': 'particulier', 'chiffre_affaires': Decimal('0.00')},
        {'nom': 'Dubois', 'prenom': 'Marie', 'email': 'marie.dubois@entreprise.com', 'telephone': '0677665544',
         'adresse': '8 Rue de la République', 'ville': 'Marseille', 'code_postal': '13001',
         'pays': 'France', 'statut': 'actif', 'categorie': 'entreprise', 'entreprise': 'Dubois SARL',
         'chiffre_affaires': Decimal('42000.00')},
        {'nom': 'Petit', 'prenom': 'Paul', 'email': 'paul.petit@association.org', 'telephone': '0655443322',
         'adresse': '15 Allée des Roses', 'ville': 'Toulouse', 'code_postal': '31000', 'pays': 'France',
         'statut': 'actif', 'categorie': 'association', 'chiffre_affaires': Decimal('8500.00')},
        {'nom': 'Moreau', 'prenom': 'Claire', 'email': 'claire.moreau@mairie.fr', 'telephone': '0644332211',
         'adresse': '1 Place de la Mairie', 'ville': 'Bordeaux', 'code_postal': '33000', 'pays': 'France',
         'statut': 'inactif', 'categorie': 'administration', 'chiffre_affaires': Decimal('12000.00')},
        {'nom': 'Simon', 'prenom': 'Thomas', 'email': 'thomas.simon@tech.io', 'telephone': '0633221100',
         'adresse': '22 Rue de l\'Innovation', 'ville': 'Lille', 'code_postal': '59000', 'pays': 'France',
         'statut': 'vip', 'categorie': 'entreprise', 'entreprise': 'Tech.IO', 'chiffre_affaires': Decimal('120000.00')},
        {'nom': 'Laurent', 'prenom': 'Emma', 'email': 'emma.laurent@startup.fr', 'telephone': '0622110099',
         'adresse': '9 Quai de la Loire', 'ville': 'Nantes', 'code_postal': '44000', 'pays': 'France',
         'statut': 'prospect', 'categorie': 'entreprise', 'entreprise': 'StartupFR', 'chiffre_affaires': Decimal('3200.00')},
    ]

    created_clients = []
    for data in clients_data:
        c = Client.objects.create(**data)
        created_clients.append(c)
        print(f"  ✓ Client créé : {c.get_full_name()}")

    # Interactions de démo
    types = ['appel', 'email', 'reunion', 'visite', 'autre']
    descriptions = [
        "Discussion sur les besoins futurs du client.",
        "Envoi du devis révisé suite à la réunion.",
        "Présentation des nouveaux services.",
        "Visite des locaux pour audit de besoins.",
        "Relance suite au dernier contact.",
        "Signature du contrat annuel.",
        "Point mensuel de suivi de satisfaction.",
    ]
    for client in created_clients[:5]:
        for j in range(random.randint(1, 3)):
            Interaction.objects.create(
                client=client,
                type_interaction=random.choice(types),
                description=random.choice(descriptions),
                utilisateur='Admin HellFire',
                date=timezone.now() - timezone.timedelta(days=random.randint(0, 90))
            )
    print(f"  ✓ Interactions de démo créées.")
else:
    print(f"  → {Client.objects.count()} clients déjà présents, pas de données de démo.")

print("\n" + "=" * 50)
print("  ✓ Configuration terminée !")
print(f"  → Démarrez le serveur : python manage.py runserver")
print(f"  → Accédez à : http://127.0.0.1:8000/login/")
print(f"  → Login: admin | Mot de passe: admin123")
print("=" * 50 + "\n")
