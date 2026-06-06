# Studio 314 — Gestion de Clients Django

Application web CRUD complète de gestion de clients, construite avec Django, HTML, CSS et JavaScript.

###Installation & Lancement

### 1. Prérequis
- Python 3.10+
- pip
- Django

### 3. Setup initial (migrations + données de démo)

```bash
python3 manage.py migrate
python3 manage.py makemigrations core
python3 manage.py migrate
python3 setup.py
```

Ce script va :
- Appliquer les migrations (`makemigrations` + `migrate`)
- Créer un compte admin (`admin` / `admin123`)
- Générer des données de démonstration (8 clients, plusieurs interactions)

### 4. Démarrer le serveur

```bash
python manage.py runserver
```

### 5. Accéder à l'application

- **Application** : http://127.0.0.1:8000/login/
- **Admin Django** : http://127.0.0.1:8000/admin/
- **Identifiants** : `admin` / `admin123`

---

## 📁 Architecture du projet

```
django_app/
├── manage.py
├── setup.py                    ← Script d'initialisation
├── requirements.txt
├── HellFire/                   ← Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── core/                       ← Application principale
    ├── models.py               ← Modèles Client & Interaction
    ├── views.py                ← Vues CRUD + API
    ├── urls.py                 ← Routes URL
    ├── forms.py                ← Formulaires Django
    ├── admin.py                ← Interface admin
    ├── templates/
    │   └── core/
    │       ├── login.html      ← Page de connexion
    │       ├── home.html       ← Shell SPA principal
    │       └── partials/       ← Sections chargées en AJAX
    │           ├── accueil.html
    │           ├── database.html
    │           ├── statistiques.html
    │           ├── client_form.html
    │           ├── client_detail.html
    │           ├── client_confirm_delete.html
    │           ├── about.html
    │           ├── parametres.html
    │           └── systeme.html
    └── static/
        └── core/
            ├── css/
            │   ├── login.css
            │   ├── home.css
            │   ├── accueil.css
            │   ├── database.css
            │   └── statistiques.css
            └── js/
                ├── login.js
                ├── home.js
                ├── database.js
                └── statistiques.js
```

---

## ✨ Fonctionnalités

### Gestion Clients (CRUD)
- ✅ **Créer** un client (formulaire multi-sections)
- ✅ **Lire** la liste avec pagination et filtres
- ✅ **Modifier** tous les champs d'un client
- ✅ **Supprimer** avec confirmation
- ✅ **Voir** la fiche détaillée d'un client

### Champs Client
- Identité : Nom, Prénom, Email, Téléphone, Date de naissance
- Adresse : Rue, Ville, Code postal, Pays
- Commercial : Statut (Actif/Inactif/Prospect/VIP), Catégorie, Entreprise, CA
- Notes libres

### Interactions
- Ajout d'interactions par client (Appel, Email, Réunion, Visite, Autre)
- Historique complet avec date, description et utilisateur
- Suppression d'interaction

### Recherche & Filtres
- Recherche globale (nom, prénom, email, téléphone, ville, entreprise)
- Filtre par statut
- Filtre par catégorie
- Pagination (10 par page)

### Export
- Export CSV de tous les clients (compatible Excel, UTF-8 BOM)

### Statistiques & Graphiques (Chart.js)
- Évolution mensuelle (12 mois)
- Répartition par statut (pie/doughnut)
- Répartition par catégorie (barre horizontale)
- Types d'interactions
- Top 5 villes
- Top 5 clients par CA
- KPIs : Total clients, CA total, CA moyen, nouveaux du mois

### Interface SPA
- Navigation sans rechargement de page (AJAX)
- Modal pour création/modification/suppression
- Sidebar réductible avec persistance (localStorage)
- Toasts de notification
- Horloge temps réel
- Mode sombre (dark theme)
- Design responsive mobile

---

## 🔐 Sécurité

- Authentification Django intégrée
- CSRF protection sur tous les formulaires
- Décorateur `@login_required` sur toutes les vues protégées
- Validation côté serveur (formulaires Django)
