/* ── STATISTIQUES JS (Chart.js) ──────────────────────── */

var CHART_COLORS = {
  red:    '#ff4e42',
  blue:   '#60a5fa',
  green:  '#34d399',
  yellow: '#fbbf24',
  purple: '#a78bfa',
  orange: '#fb923c',
  pink:   '#f472b6',
  cyan:   '#22d3ee',
  muted:  '#7a7a90'
};

var PALETTE = [
  CHART_COLORS.red, CHART_COLORS.blue, CHART_COLORS.green,
  CHART_COLORS.yellow, CHART_COLORS.purple, CHART_COLORS.orange,
  CHART_COLORS.pink, CHART_COLORS.cyan
];

var chartDefaults = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: { color: '#e8e8f0', font: { family: 'Inter, sans-serif', size: 12 }, boxWidth: 12, padding: 16 }
    },
    tooltip: {
      backgroundColor: '#1c1c22',
      borderColor: '#2a2a35',
      borderWidth: 1,
      titleColor: '#e8e8f0',
      bodyColor: '#7a7a90',
      padding: 12
    }
  }
};

var activeCharts = {};

function destroyChart(id) {
  if (activeCharts[id]) {
    activeCharts[id].destroy();
    delete activeCharts[id];
  }
}

// ── ACCUEIL Charts ──
function initAccueilCharts(evolutionData, statutData) {
  // Graphique évolution (bar)
  var ctxEvo = document.getElementById('chartEvolution');
  if (ctxEvo) {
    destroyChart('chartEvolution');
    activeCharts['chartEvolution'] = new Chart(ctxEvo, {
      type: 'bar',
      data: {
        labels: evolutionData.map(function(d) { return d.mois; }),
        datasets: [{
          label: 'Nouveaux clients',
          data: evolutionData.map(function(d) { return d.count; }),
          backgroundColor: 'rgba(255,78,66,0.3)',
          borderColor: CHART_COLORS.red,
          borderWidth: 2,
          borderRadius: 6,
          borderSkipped: false
        }]
      },
      options: Object.assign({}, chartDefaults, {
        scales: {
          x: { ticks: { color: CHART_COLORS.muted }, grid: { color: 'rgba(42,42,53,0.8)' } },
          y: {
            ticks: { color: CHART_COLORS.muted, stepSize: 1 },
            grid: { color: 'rgba(42,42,53,0.8)' },
            beginAtZero: true
          }
        }
      })
    });
  }

  // Graphique statut (doughnut)
  var ctxStat = document.getElementById('chartStatut');
  if (ctxStat && statutData && statutData.length > 0) {
    destroyChart('chartStatut');
    var statLabels = { actif: 'Actif', inactif: 'Inactif', prospect: 'Prospect', vip: 'VIP' };
    var statColors = { actif: CHART_COLORS.green, inactif: CHART_COLORS.muted, prospect: CHART_COLORS.yellow, vip: CHART_COLORS.purple };

    activeCharts['chartStatut'] = new Chart(ctxStat, {
      type: 'doughnut',
      data: {
        labels: statutData.map(function(d) { return statLabels[d.statut] || d.statut; }),
        datasets: [{
          data: statutData.map(function(d) { return d.count; }),
          backgroundColor: statutData.map(function(d) { return (statColors[d.statut] || CHART_COLORS.blue) + '99'; }),
          borderColor: statutData.map(function(d) { return statColors[d.statut] || CHART_COLORS.blue; }),
          borderWidth: 2
        }]
      },
      options: Object.assign({}, chartDefaults, {
        cutout: '70%',
        plugins: Object.assign({}, chartDefaults.plugins, {
          legend: { display: false }
        })
      })
    });

    // Légende manuelle
    var legendEl = document.getElementById('statutLegend');
    if (legendEl) {
      legendEl.innerHTML = '';
      statutData.forEach(function(d, i) {
        var item = document.createElement('div');
        item.className = 'legend-item';
        item.innerHTML = '<span class="legend-dot" style="background:' + (statColors[d.statut] || PALETTE[i]) + '"></span>' +
                         '<span>' + (statLabels[d.statut] || d.statut) + ' (' + d.count + ')</span>';
        legendEl.appendChild(item);
      });
    }
  }
}

// ── STATS Charts ──
function initStatsCharts(evolution, parStatut, parCategorie, interactions) {
  var statLabels = { actif: 'Actif', inactif: 'Inactif', prospect: 'Prospect', vip: 'VIP' };
  var catLabels = { particulier: 'Particulier', entreprise: 'Entreprise', association: 'Association', administration: 'Administration' };
  var intLabels = { appel: 'Appel', email: 'Email', reunion: 'Réunion', visite: 'Visite', autre: 'Autre' };
  var statColors = { actif: CHART_COLORS.green, inactif: CHART_COLORS.muted, prospect: CHART_COLORS.yellow, vip: CHART_COLORS.purple };

  // Évolution (line)
  var ctxEvo = document.getElementById('chartEvolutionStats');
  if (ctxEvo) {
    destroyChart('chartEvolutionStats');
    activeCharts['chartEvolutionStats'] = new Chart(ctxEvo, {
      type: 'line',
      data: {
        labels: evolution.map(function(d) { return d.mois; }),
        datasets: [{
          label: 'Nouveaux clients',
          data: evolution.map(function(d) { return d.count; }),
          borderColor: CHART_COLORS.red,
          backgroundColor: 'rgba(255,78,66,0.08)',
          borderWidth: 2.5,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: CHART_COLORS.red,
          pointBorderColor: '#1c1c22',
          pointBorderWidth: 2,
          pointRadius: 4
        }]
      },
      options: Object.assign({}, chartDefaults, {
        scales: {
          x: { ticks: { color: CHART_COLORS.muted, maxTicksLimit: 8 }, grid: { color: 'rgba(42,42,53,0.6)' } },
          y: {
            ticks: { color: CHART_COLORS.muted, stepSize: 1 },
            grid: { color: 'rgba(42,42,53,0.6)' },
            beginAtZero: true
          }
        }
      })
    });
  }

  // Par statut (pie)
  var ctxStatut = document.getElementById('chartStatutStats');
  if (ctxStatut && parStatut && parStatut.length > 0) {
    destroyChart('chartStatutStats');
    activeCharts['chartStatutStats'] = new Chart(ctxStatut, {
      type: 'pie',
      data: {
        labels: parStatut.map(function(d) { return statLabels[d.statut] || d.statut; }),
        datasets: [{
          data: parStatut.map(function(d) { return d.count; }),
          backgroundColor: parStatut.map(function(d, i) { return (statColors[d.statut] || PALETTE[i]) + 'cc'; }),
          borderColor: parStatut.map(function(d, i) { return statColors[d.statut] || PALETTE[i]; }),
          borderWidth: 2
        }]
      },
      options: chartDefaults
    });
  }

  // Par catégorie (bar horizontal)
  var ctxCat = document.getElementById('chartCategorieStats');
  if (ctxCat && parCategorie && parCategorie.length > 0) {
    destroyChart('chartCategorieStats');
    activeCharts['chartCategorieStats'] = new Chart(ctxCat, {
      type: 'bar',
      data: {
        labels: parCategorie.map(function(d) { return catLabels[d.categorie] || d.categorie; }),
        datasets: [{
          label: 'Clients',
          data: parCategorie.map(function(d) { return d.count; }),
          backgroundColor: PALETTE.map(function(c) { return c + '99'; }),
          borderColor: PALETTE,
          borderWidth: 2,
          borderRadius: 6
        }]
      },
      options: Object.assign({}, chartDefaults, {
        indexAxis: 'y',
        scales: {
          x: { ticks: { color: CHART_COLORS.muted, stepSize: 1 }, grid: { color: 'rgba(42,42,53,0.6)' }, beginAtZero: true },
          y: { ticks: { color: CHART_COLORS.muted }, grid: { display: false } }
        },
        plugins: Object.assign({}, chartDefaults.plugins, { legend: { display: false } })
      })
    });
  }

  // Interactions (doughnut)
  var ctxInter = document.getElementById('chartInteractions');
  if (ctxInter && interactions && interactions.length > 0) {
    destroyChart('chartInteractions');
    activeCharts['chartInteractions'] = new Chart(ctxInter, {
      type: 'doughnut',
      data: {
        labels: interactions.map(function(d) { return intLabels[d.type_interaction] || d.type_interaction; }),
        datasets: [{
          data: interactions.map(function(d) { return d.count; }),
          backgroundColor: PALETTE.map(function(c) { return c + '99'; }),
          borderColor: PALETTE,
          borderWidth: 2
        }]
      },
      options: Object.assign({}, chartDefaults, {
        cutout: '60%',
        plugins: Object.assign({}, chartDefaults.plugins, {
          legend: { position: 'bottom', labels: chartDefaults.plugins.legend.labels }
        })
      })
    });
  }
}

// ── Barre de villes ──
function initVilleBars() {
  var items = document.querySelectorAll('.ville-item');
  if (items.length === 0) return;
  var counts = [];
  items.forEach(function(item) {
    var countEl = item.querySelector('.ville-count');
    counts.push(parseInt(countEl ? countEl.textContent.trim() : '0', 10));
  });
  var max = Math.max.apply(null, counts) || 1;
  items.forEach(function(item, i) {
    var bar = item.querySelector('.ville-bar');
    if (bar) bar.style.width = (counts[i] / max * 100) + '%';
  });
}
