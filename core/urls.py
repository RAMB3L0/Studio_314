from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.login_view, name='login_redirect'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Home (SPA shell)
    path('home/', views.home_view, name='home'),

    # Partials (chargées via AJAX)
    path('partials/accueil/', views.accueil_partial, name='accueil'),
    path('partials/database/', views.database_partial, name='database'),
    path('partials/statistiques/', views.statistiques_partial, name='statistiques'),
    path('partials/about/', views.about_partial, name='about'),
    path('partials/parametres/', views.parametres_partial, name='parametres'),
    path('partials/systeme/', views.systeme_partial, name='systeme'),

    # CRUD Clients
    path('clients/new/', views.client_create, name='client_create'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    path('clients/<int:pk>/edit/', views.client_edit, name='client_edit'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),
    path('clients/export/csv/', views.client_export_csv, name='client_export_csv'),

    # Interactions
    path('clients/<int:client_pk>/interactions/new/', views.interaction_create, name='interaction_create'),
    path('interactions/<int:pk>/delete/', views.interaction_delete, name='interaction_delete'),

    # API
    path('api/stats/', views.api_stats, name='api_stats'),
]
