/* ── LOGIN JS ─────────────────────────────────────────── */

// ── Particules animées ──
(function createParticles() {
  var container = document.getElementById('particles');
  if (!container) return;
  var colors = ['#ff4e42', '#ff6b63', '#ff8880', 'rgba(255,78,66,0.3)'];
  for (var i = 0; i < 20; i++) {
    (function(i) {
      var p = document.createElement('div');
      p.classList.add('particle');
      var size = Math.random() * 6 + 2;
      p.style.cssText = [
        'width:' + size + 'px',
        'height:' + size + 'px',
        'left:' + Math.random() * 100 + '%',
        'background:' + colors[Math.floor(Math.random() * colors.length)],
        'animation-duration:' + (Math.random() * 10 + 8) + 's',
        'animation-delay:' + Math.random() * 8 + 's'
      ].join(';');
      container.appendChild(p);
    })(i);
  }
})();

// ── Toggle password ──
function togglePassword() {
  var input = document.getElementById('password');
  var icon = document.getElementById('eyeIcon');
  if (input.type === 'password') {
    input.type = 'text';
    icon.innerHTML = '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>';
  } else {
    input.type = 'password';
    icon.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>';
  }
}

// ── Loading state ──
var loginForm = document.getElementById('loginForm');
if (loginForm) {
  loginForm.addEventListener('submit', function() {
    var btn = document.getElementById('btnLogin');
    var text = btn.querySelector('.btn-text');
    var loader = document.getElementById('btnLoader');
    btn.disabled = true;
    text.style.display = 'none';
    loader.style.display = 'flex';
  });
}

// ── Auto-dismiss messages ──
setTimeout(function() {
  var messages = document.querySelectorAll('.alert');
  messages.forEach(function(msg) {
    msg.style.transition = 'opacity .4s ease';
    msg.style.opacity = '0';
    setTimeout(function() { if (msg.parentElement) msg.remove(); }, 400);
  });
}, 5000);
