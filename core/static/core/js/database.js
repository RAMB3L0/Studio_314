/* ── DATABASE JS ─────────────────────────────────────── */

// Filtre en temps réel côté client (complément de la recherche serveur)
document.addEventListener('input', function(e) {
  if (e.target && e.target.id === 'searchInput') {
    var q = e.target.value.toLowerCase().trim();
    var rows = document.querySelectorAll('.db-row');
    if (rows.length === 0) return;
    rows.forEach(function(row) {
      var text = row.textContent.toLowerCase();
      row.style.display = q === '' || text.includes(q) ? '' : 'none';
    });
  }
});

// Ajout de l'attribut id au champ de recherche généré par Django
document.addEventListener('DOMContentLoaded', function() {
  var searchInput = document.querySelector('input[name="q"]');
  if (searchInput && !searchInput.id) {
    searchInput.id = 'searchInput';
  }
});

// Highlight de ligne au survol
document.addEventListener('mouseover', function(e) {
  var row = e.target.closest('.db-row');
  if (row) row.style.cursor = 'default';
});

// Double-clic pour voir le détail
document.addEventListener('dblclick', function(e) {
  var row = e.target.closest('.db-row');
  if (row && typeof loadClientDetail === 'function') {
    var pk = row.dataset.pk;
    if (pk) loadClientDetail(pk);
  }
});

// Sélection de ligne au clic (visuel uniquement)
document.addEventListener('click', function(e) {
  var row = e.target.closest('.db-row');
  if (row && !e.target.closest('button') && !e.target.closest('a')) {
    document.querySelectorAll('.db-row.selected').forEach(function(r) { r.classList.remove('selected'); });
    row.classList.add('selected');
  }
});
