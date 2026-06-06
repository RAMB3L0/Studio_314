from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Sum, Count, Avg
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import datetime, timedelta
import csv

from .models import Client, Interaction
from .forms import ClientForm, InteractionForm, ClientSearchForm


# ─── AUTH ────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue, {user.get_full_name() or user.username} !')
            return redirect('home')
        else:
            messages.error(request, 'Identifiants incorrects. Veuillez réessayer.')
    
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('login')


# ─── HOME ────────────────────────────────────────────────────────────────────

@login_required
def home_view(request):
    return render(request, 'core/home.html', {
        'active_section': 'accueil'
    })


# ─── PARTIALS (chargées dynamiquement) ───────────────────────────────────────

@login_required
def accueil_partial(request):
    total_clients = Client.objects.count()
    clients_actifs = Client.objects.filter(statut='actif').count()
    clients_vip = Client.objects.filter(statut='vip').count()
    ca_total = Client.objects.aggregate(total=Sum('chiffre_affaires'))['total'] or 0
    
    # Derniers clients ajoutés
    derniers_clients = Client.objects.order_by('-date_creation')[:5]
    
    # Répartition par statut
    repartition_statut = Client.objects.values('statut').annotate(count=Count('id'))
    
    # Interactions récentes
    interactions_recentes = Interaction.objects.order_by('-date')[:5]
    
    # Clients par mois (6 derniers mois)
    now = timezone.now()
    clients_par_mois = []
    for i in range(5, -1, -1):
        mois = now - timedelta(days=30 * i)
        count = Client.objects.filter(
            date_creation__year=mois.year,
            date_creation__month=mois.month
        ).count()
        clients_par_mois.append({
            'mois': mois.strftime('%b %Y'),
            'count': count
        })
    
    context = {
        'total_clients': total_clients,
        'clients_actifs': clients_actifs,
        'clients_vip': clients_vip,
        'ca_total': ca_total,
        'derniers_clients': derniers_clients,
        'repartition_statut': repartition_statut,
        'interactions_recentes': interactions_recentes,
        'clients_par_mois': clients_par_mois,
    }
    return render(request, 'core/partials/accueil.html', context)


@login_required
def database_partial(request):
    form = ClientSearchForm(request.GET)
    clients = Client.objects.all()
    
    if form.is_valid():
        q = form.cleaned_data.get('q')
        statut = form.cleaned_data.get('statut')
        categorie = form.cleaned_data.get('categorie')
        
        if q:
            clients = clients.filter(
                Q(nom__icontains=q) |
                Q(prenom__icontains=q) |
                Q(email__icontains=q) |
                Q(telephone__icontains=q) |
                Q(ville__icontains=q) |
                Q(entreprise__icontains=q)
            )
        if statut:
            clients = clients.filter(statut=statut)
        if categorie:
            clients = clients.filter(categorie=categorie)
    
    # Pagination
    paginator = Paginator(clients, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'clients': page_obj,
        'form': form,
        'total': clients.count(),
        'paginator': paginator,
        'page_obj': page_obj,
    }
    return render(request, 'core/partials/database.html', context)


@login_required
def statistiques_partial(request):
    total_clients = Client.objects.count()
    ca_total = Client.objects.aggregate(total=Sum('chiffre_affaires'))['total'] or 0
    ca_moyen = Client.objects.aggregate(avg=Avg('chiffre_affaires'))['avg'] or 0
    
    # Par statut
    par_statut = list(Client.objects.values('statut').annotate(
        count=Count('id'),
        ca=Sum('chiffre_affaires')
    ))
    
    # Par catégorie
    par_categorie = list(Client.objects.values('categorie').annotate(
        count=Count('id')
    ))
    
    # Par ville (top 5)
    par_ville = list(Client.objects.values('ville').annotate(
        count=Count('id')
    ).exclude(ville__isnull=True).exclude(ville='').order_by('-count')[:5])
    
    # Évolution mensuelle (12 mois)
    now = timezone.now()
    evolution = []
    for i in range(11, -1, -1):
        mois = now - timedelta(days=30 * i)
        count = Client.objects.filter(
            date_creation__year=mois.year,
            date_creation__month=mois.month
        ).count()
        ca = Client.objects.filter(
            date_creation__year=mois.year,
            date_creation__month=mois.month
        ).aggregate(total=Sum('chiffre_affaires'))['total'] or 0
        evolution.append({
            'mois': mois.strftime('%b %Y'),
            'count': count,
            'ca': float(ca)
        })
    
    # Top clients par CA
    top_clients = Client.objects.order_by('-chiffre_affaires')[:5]
    
    # Interactions par type
    interactions_par_type = list(Interaction.objects.values('type_interaction').annotate(
        count=Count('id')
    ))
    
    context = {
        'total_clients': total_clients,
        'ca_total': ca_total,
        'ca_moyen': ca_moyen,
        'par_statut': par_statut,
        'par_categorie': par_categorie,
        'par_ville': par_ville,
        'evolution': evolution,
        'top_clients': top_clients,
        'interactions_par_type': interactions_par_type,
        'clients_actifs': Client.objects.filter(statut='actif').count(),
        'clients_vip': Client.objects.filter(statut='vip').count(),
        'nouveaux_ce_mois': Client.objects.filter(
            date_creation__year=now.year,
            date_creation__month=now.month
        ).count(),
    }
    return render(request, 'core/partials/statistiques.html', context)


@login_required
def about_partial(request):
    return render(request, 'core/partials/about.html')


@login_required
def parametres_partial(request):
    return render(request, 'core/partials/parametres.html')


@login_required
def systeme_partial(request):
    import platform
    import django
    context = {
        'python_version': platform.python_version(),
        'django_version': django.get_version(),
        'os_info': f"{platform.system()} {platform.release()}",
        'total_clients': Client.objects.count(),
        'total_interactions': Interaction.objects.count(),
    }
    return render(request, 'core/partials/systeme.html', context)


# ─── CRUD CLIENT ─────────────────────────────────────────────────────────────

@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, f'Client {client.get_full_name()} créé avec succès !')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': f'Client {client.get_full_name()} créé avec succès !'})
            return redirect('home')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                errors = {field: list(errs) for field, errs in form.errors.items()}
                return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = ClientForm()
    
    return render(request, 'core/partials/client_form.html', {
        'form': form,
        'action': 'Créer',
        'title': 'Nouveau Client'
    })


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    interactions = client.interactions.order_by('-date')[:10]
    interaction_form = InteractionForm()
    
    return render(request, 'core/partials/client_detail.html', {
        'client': client,
        'interactions': interactions,
        'interaction_form': interaction_form,
    })


@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, f'Client {client.get_full_name()} mis à jour avec succès !')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': f'Client {client.get_full_name()} mis à jour !'})
            return redirect('home')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                errors = {field: list(errs) for field, errs in form.errors.items()}
                return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = ClientForm(instance=client)
    
    return render(request, 'core/partials/client_form.html', {
        'form': form,
        'client': client,
        'action': 'Modifier',
        'title': f'Modifier — {client.get_full_name()}'
    })


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        name = client.get_full_name()
        client.delete()
        messages.success(request, f'Client {name} supprimé avec succès.')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': f'Client {name} supprimé.'})
        return redirect('home')
    
    return render(request, 'core/partials/client_confirm_delete.html', {'client': client})


@login_required
def client_export_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="clients_hellfire.csv"'
    response.write('\ufeff')  # BOM pour Excel
    
    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'ID', 'Nom', 'Prénom', 'Email', 'Téléphone',
        'Adresse', 'Ville', 'Code Postal', 'Pays',
        'Statut', 'Catégorie', 'Entreprise',
        "Chiffre d'affaires", 'Date de naissance',
        'Date de création', 'Notes'
    ])
    
    clients = Client.objects.all().order_by('nom', 'prenom')
    for c in clients:
        writer.writerow([
            c.id, c.nom, c.prenom, c.email, c.telephone or '',
            c.adresse or '', c.ville or '', c.code_postal or '', c.pays or '',
            c.get_statut_display(), c.get_categorie_display(), c.entreprise or '',
            c.chiffre_affaires,
            c.date_naissance.strftime('%d/%m/%Y') if c.date_naissance else '',
            c.date_creation.strftime('%d/%m/%Y %H:%M'),
            c.notes or ''
        ])
    
    return response


# ─── INTERACTIONS ─────────────────────────────────────────────────────────────

@login_required
def interaction_create(request, client_pk):
    client = get_object_or_404(Client, pk=client_pk)
    
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.client = client
            interaction.utilisateur = request.user.get_full_name() or request.user.username
            interaction.save()
            messages.success(request, 'Interaction ajoutée avec succès !')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('client_detail', pk=client_pk)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    
    return redirect('client_detail', pk=client_pk)


@login_required
def interaction_delete(request, pk):
    interaction = get_object_or_404(Interaction, pk=pk)
    client_pk = interaction.client.pk
    
    if request.method == 'POST':
        interaction.delete()
        messages.success(request, 'Interaction supprimée.')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('client_detail', pk=client_pk)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


# ─── API JSON ─────────────────────────────────────────────────────────────────

@login_required
def api_stats(request):
    """Endpoint JSON pour les graphiques dynamiques."""
    now = timezone.now()
    
    par_statut = list(Client.objects.values('statut').annotate(count=Count('id')))
    par_categorie = list(Client.objects.values('categorie').annotate(count=Count('id')))
    
    evolution = []
    for i in range(11, -1, -1):
        mois = now - timedelta(days=30 * i)
        count = Client.objects.filter(
            date_creation__year=mois.year,
            date_creation__month=mois.month
        ).count()
        evolution.append({'mois': mois.strftime('%b %Y'), 'count': count})
    
    return JsonResponse({
        'par_statut': par_statut,
        'par_categorie': par_categorie,
        'evolution': evolution,
        'total': Client.objects.count(),
        'ca_total': float(Client.objects.aggregate(t=Sum('chiffre_affaires'))['t'] or 0),
    })
