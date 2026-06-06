/* ── HOME / SPA JS ───────────────────────────────────── */

var currentSection = 'accueil';
var sidebarCollapsed = false;

// ── Horloge ──
function updateClock() {
  var el = document.getElementById('topbarTime');
  if (!el) return;
  var now = new Date();
  var pad = function(n) { return n < 10 ? '0' + n : n; };
  el.textContent = pad(now.getHours()) + ':' + pad(now.getMinutes()) + ':' + pad(now.getSeconds());
}
setInterval(updateClock, 1000);
updateClock();

// ── Chargement de section ──
function loadSection(section, url) {
  var contentArea = document.getElementById('contentArea');
  var loading = document.getElementById('loadingScreen');

  // Afficher loader
  contentArea.innerHTML = '<div class="loading-screen" id="loadingScreen"><div class="loader-ring"></div><p>Chargement...</p></div>';

  fetch(url, {
    headers: { 'X-Requested-With': 'XMLHttpRequest' }
  })
  .then(function(r) {
    if (!r.ok) throw new Error('Erreur ' + r.status);
    return r.text();
  })
  .then(function(html) {
    contentArea.innerHTML = html;
    currentSection = section;

    // Mettre à jour la nav active
    document.querySelectorAll('.nav-item').forEach(function(item) {
      item.classList.toggle('active', item.dataset.section === section);
    });

    // Mettre à jour breadcrumb
    var labels = {
      accueil: 'Accueil', database: 'Base de données',
      statistiques: 'Statistiques', parametres: 'Paramètres',
      systeme: 'Système', about: 'À propos'
    };
    var bc = document.getElementById('bcPage');
    if (bc) bc.textContent = labels[section] || section;

    // Ré-exécuter les scripts inline
    var scripts = contentArea.querySelectorAll('script');
    scripts.forEach(function(s) {
      var ns = document.createElement('script');
      ns.textContent = s.textContent;
      document.body.appendChild(ns);
      document.body.removeChild(ns);
    });
  })
  .catch(function(err) {
    contentArea.innerHTML = '<div class="loading-screen"><p style="color:#ff6b63">Erreur de chargement : ' + err.message + '</p></div>';
  });
}

// ── Navigation ──
document.querySelectorAll('.nav-item[data-url]').forEach(function(item) {
  item.addEventListener('click', function(e) {
    e.preventDefault();
    loadSection(this.dataset.section, this.dataset.url);
    // Fermer le menu mobile
    var sidebar = document.getElementById('sidebar');
    if (sidebar.classList.contains('mobile-open')) {
      sidebar.classList.remove('mobile-open');
    }
  });
});

// ── Sidebar toggle ──
function toggleSidebar() {
    document.getElementById('layout').classList.toggle('collapsed');
}


var sidebarToggle = document.getElementById('sidebarToggle');
if (sidebarToggle) {
  sidebarToggle.addEventListener('click', function() {
    var sidebar = document.getElementById('sidebar');
    sidebarCollapsed = !sidebarCollapsed;
    sidebar.classList.toggle('collapsed', sidebarCollapsed);
    var main = document.getElementById('mainContent');
    if (main) main.classList.toggle('shifted', sidebarCollapsed);
    localStorage.setItem('sidebarCollapsed', sidebarCollapsed);
  });
}

// ── Mobile menu ──
var mobileMenuBtn = document.getElementById('mobileMenuBtn');
if (mobileMenuBtn) {
  mobileMenuBtn.addEventListener('click', function() {
    document.getElementById('sidebar').classList.toggle('mobile-open');
  });
}

// ── Restaurer état sidebar ──
(function restoreSidebar() {
  var stored = localStorage.getItem('sidebarCollapsed');
  if (stored === 'true') {
    var sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.classList.add('collapsed');
    sidebarCollapsed = true;
  }
})();

// ── Nouveau client (modal) ──
/*var btnNewClient = document.getElementById('btnNewClient');
if (btnNewClient) {
  btnNewClient.addEventListener('click', function() {
    loadModal('/clients/new/', 'Nouveau Client');
  });
} */

// ── "Voir tout" link dans accueil ──
document.addEventListener('click', function(e) {
  var link = e.target.closest('.link-voir-tout[data-section]');
  if (link) {
    e.preventDefault();
    loadSection(link.dataset.section, link.dataset.url);
  }
});

// ── Modal ──
function loadModal(url, title) {
  var overlay = document.getElementById('modalOverlay');
  var container = document.getElementById('modalContainer');
  var body = document.getElementById('modalBody');
  var titleEl = document.getElementById('modalTitle');

  overlay.style.display = 'flex';
  titleEl.textContent = title || '';
  body.innerHTML = '<div class="loading-screen" style="height:200px"><div class="loader-ring"></div></div>';

  fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
  .then(function(r) { return r.text(); })
  .then(function(html) {
    body.innerHTML = html;
    // Exécuter les scripts
    body.querySelectorAll('script').forEach(function(s) {
      var ns = document.createElement('script');
      ns.textContent = s.textContent;
      document.body.appendChild(ns);
      document.body.removeChild(ns);
    });
  })
  .catch(function(err) {
    body.innerHTML = '<p style="color:#ff6b63">Erreur: ' + err.message + '</p>';
  });
}

function closeModal() {
  var overlay = document.getElementById('modalOverlay');
  if (overlay) overlay.style.display = 'none';
  var body = document.getElementById('modalBody');
  if (body) body.innerHTML = '';
}

// Fermer modal en cliquant à l'extérieur
var modalOverlay = document.getElementById('modalOverlay');
if (modalOverlay) {
  modalOverlay.addEventListener('click', function(e) {
    if (e.target === this) closeModal();
  });
}
var modalClose = document.getElementById('modalClose');
if (modalClose) {
  modalClose.addEventListener('click', closeModal);
}

// ── Toast ──
function showToast(msg, type) {
  var container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  var toast = document.createElement('div');
  toast.className = 'toast toast-' + (type || 'info');
  var icons = { success: '✓', error: '✕', info: 'ℹ', warning: '⚠' };
  toast.innerHTML = '<span>' + (icons[type] || 'ℹ') + '</span> ' + msg;
  container.appendChild(toast);
  setTimeout(function() {
    toast.style.transition = 'opacity .3s, transform .3s';
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(20px)';
    setTimeout(function() { if (toast.parentElement) toast.remove(); }, 300);
  }, 3500);
}

// ── CRUD helpers (accessibles globalement) ──
function loadClientDetail(pk) {
  closeModal();
  loadModal('/clients/' + pk + '/', 'Fiche Client');
  document.getElementById('modalTitle').textContent = 'Fiche Client';
}
function loadClientEdit(pk) {
  closeModal();
  loadModal('/clients/' + pk + '/edit/', 'Modifier le client');
}
function confirmDeleteClient(pk, name) {
  closeModal();
  loadModal('/clients/' + pk + '/delete/', 'Supprimer — ' + name);
}

function submitClientForm(form) {
  var data = new FormData(form);
  var btn = document.getElementById('btnSubmit');
  if (btn) { btn.disabled = true; btn.textContent = 'Enregistrement...'; }

  fetch(form.action, {
    method: 'POST',
    body: data,
    headers: { 'X-Requested-With': 'XMLHttpRequest' }
  })
  .then(function(r) { return r.json(); })
  .then(function(res) {
    if (res.success) {
      closeModal();
      showToast(res.message, 'success');
      setTimeout(function() {
        loadSection(currentSection,
          currentSection === 'database' ? '/partials/database/' :
          currentSection === 'accueil'  ? '/partials/accueil/'  :
          '/partials/' + currentSection + '/');
      }, 600);
    } else {
      // Afficher les erreurs dans le formulaire
      if (btn) { btn.disabled = false; btn.textContent = 'Enregistrer'; }
      showToast('Veuillez corriger les erreurs.', 'error');
      if (res.errors) {
        Object.keys(res.errors).forEach(function(field) {
          var input = form.querySelector('[name=' + field + ']');
          if (input) {
            var err = document.createElement('span');
            err.className = 'field-error';
            err.textContent = res.errors[field].join(', ');
            input.parentElement.appendChild(err);
          }
        });
      }
    }
  })
  .catch(function() {
    if (btn) { btn.disabled = false; }
    showToast('Erreur lors de l\'enregistrement.', 'error');
  });
}

// ── Auto-dismiss flash messages ──
setTimeout(function() {
  var flashes = document.querySelectorAll('.flash');
  flashes.forEach(function(f) {
    f.style.transition = 'opacity .4s, transform .4s';
    f.style.opacity = '0';
    f.style.transform = 'translateY(-8px)';
    setTimeout(function() { if (f.parentElement) f.remove(); }, 400);
  });
}, 4000);

// ── Chargement initial ──
document.addEventListener('DOMContentLoaded', function() {
  loadSection('accueil', '/partials/accueil/');
});
