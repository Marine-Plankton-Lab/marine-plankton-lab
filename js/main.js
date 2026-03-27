/* ============================================================
   Marine Plankton Lab — Main JavaScript
   ============================================================ */

// ---- Navbar scroll ----
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 40);
  });
}

// ---- Mobile nav toggle ----
const toggle = document.getElementById('nav-toggle');
const navLinks = document.getElementById('nav-links');
if (toggle && navLinks) {
  toggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
  });
  document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => navLinks.classList.remove('open'));
  });
}

// ---- Smooth scroll ----
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const offset = 80;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

// ---- Active nav highlight ----
const sections = document.querySelectorAll('[id]');
const navItems = document.querySelectorAll('.nav-links a[href^="#"]');
const highlightNav = () => {
  let current = '';
  sections.forEach(sec => {
    if (window.scrollY >= sec.offsetTop - 120) current = sec.id;
  });
  navItems.forEach(a => {
    a.classList.remove('active');
    if (a.getAttribute('href') === `#${current}`) a.classList.add('active');
  });
};
window.addEventListener('scroll', highlightNav, { passive: true });

// ---- Fade-in on scroll ----
const fadeEls = document.querySelectorAll('.fade-in');
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.10 });
fadeEls.forEach(el => observer.observe(el));

// Hero els visible immediately
document.querySelectorAll('.hero .fade-in').forEach(el => {
  setTimeout(() => el.classList.add('visible'), 120);
});

// ---- Counter animation ----
const counts = document.querySelectorAll('.count');
const counterObs = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const el = entry.target;
    const target = parseInt(el.dataset.target, 10);
    let current = 0;
    const step = target / 50;
    const timer = setInterval(() => {
      current += step;
      if (current >= target) { el.textContent = target; clearInterval(timer); }
      else el.textContent = Math.floor(current);
    }, 28);
    counterObs.unobserve(el);
  });
}, { threshold: 0.5 });
counts.forEach(el => counterObs.observe(el));

// ---- Particle generator ----
function createParticles() {
  const container = document.getElementById('particles');
  if (!container) return;
  for (let i = 0; i < 20; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    const size = Math.random() * 60 + 16;
    p.style.cssText = `
      width: ${size}px; height: ${size}px;
      left: ${Math.random() * 100}%;
      animation-duration: ${Math.random() * 12 + 10}s;
      animation-delay: ${Math.random() * -16}s;
    `;
    container.appendChild(p);
  }
}
createParticles();

// ---- Interactive Plankton Canvas ----
function initPlanktonCanvas() {
  const canvas = document.getElementById('plankton-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let width, height;
  let planktons = [];
  const mouse = { x: -1000, y: -1000, radius: 180 };
  let exploding = false;

  function resize() {
    const rect = canvas.getBoundingClientRect();
    width = rect.width;
    height = rect.height;
    const dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    ctx.scale(dpr, dpr);
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
  }

  window.addEventListener('resize', resize);

  // Mouse tracking relative to canvas
  window.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
  });
  window.addEventListener('mouseleave', () => {
    mouse.x = -1000;
    mouse.y = -1000;
  });

  // Click → explode
  window.addEventListener('click', () => {
    exploding = true;
    setTimeout(() => { exploding = false; }, 120);
  });

  class Plankton {
    constructor() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.baseVx = (Math.random() - 0.5) * 1.0;
      this.baseVy = (Math.random() - 0.5) * 1.0;
      this.vx = this.baseVx;
      this.vy = this.baseVy;

      this.size = Math.random() * 2 + 1.5;

      // Types: 0 = dot, 1 = diatom, 2 = dinoflagellate
      this.type = Math.floor(Math.random() * 3);
      this.angle = Math.random() * Math.PI * 2;
      this.spin = (Math.random() - 0.5) * 0.05;

      // Colors: bioluminescent blue/cyan
      const colors = ['#00B4D8', '#90E0EF', '#48CAE4', '#CAF0F8'];
      this.color = colors[Math.floor(Math.random() * colors.length)];
      this.maxGlow = Math.random() * 15 + 10;
      this.glow = 0;
    }

    update() {
      this.angle += this.spin;

      let dx = mouse.x - this.x;
      let dy = mouse.y - this.y;
      let dist = Math.sqrt(dx * dx + dy * dy);
      let angleToMouse = Math.atan2(dy, dx);

      if (exploding && dist < mouse.radius * 2.5) {
        // Burst outward on click
        let force = (mouse.radius * 2.5 - dist) / (mouse.radius * 2.5);
        this.vx -= Math.cos(angleToMouse) * force * 18;
        this.vy -= Math.sin(angleToMouse) * force * 18;
        this.glow = this.maxGlow;
      } else if (!exploding && dist < mouse.radius) {
        // Attract toward mouse on hover
        let force = (mouse.radius - dist) / mouse.radius;
        this.vx += Math.cos(angleToMouse) * force * 0.8;
        this.vy += Math.sin(angleToMouse) * force * 0.8;
        this.glow = this.maxGlow * force * 1.5;

        // Cap attract speed
        let speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
        if (speed > 5) {
          this.vx = (this.vx / speed) * 5;
          this.vy = (this.vy / speed) * 5;
        }
      } else {
        // Drift back to normal
        this.vx += (this.baseVx - this.vx) * 0.02;
        this.vy += (this.baseVy - this.vy) * 0.02;
        this.glow = Math.max(0, this.glow - 0.8);
      }

      this.x += this.vx;
      this.y += this.vy;

      // Wrap around
      if (this.x < -20) this.x = width + 20;
      if (this.x > width + 20) this.x = -20;
      if (this.y < -20) this.y = height + 20;
      if (this.y > height + 20) this.y = -20;
    }

    draw() {
      ctx.save();
      ctx.translate(this.x, this.y);
      ctx.rotate(this.angle);

      ctx.shadowBlur = this.glow > 2 ? this.glow : 2;
      ctx.shadowColor = this.color;
      ctx.fillStyle = this.color;
      ctx.globalAlpha = Math.min(1, 0.3 + (this.glow / this.maxGlow) * 0.7);

      ctx.beginPath();

      if (this.type === 0) {
        ctx.arc(0, 0, this.size, 0, Math.PI * 2);
        ctx.fill();
      } else if (this.type === 1) {
        ctx.ellipse(0, 0, this.size * 2, this.size * 0.8, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = 'rgba(255,255,255,0.5)';
        ctx.fillRect(-this.size, -this.size * 0.1, this.size * 2, this.size * 0.2);
      } else {
        ctx.arc(0, 0, this.size * 1.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 0.8;
        ctx.beginPath();
        ctx.arc(0, 0, this.size * 1.8, -Math.PI / 4, Math.PI / 4);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(0, this.size);
        ctx.quadraticCurveTo(this.size, this.size * 3, -this.size, this.size * 5);
        ctx.stroke();
      }

      ctx.restore();
    }
  }

  function init() {
    resize();
    planktons = [];
    const numPlankton = window.innerWidth > 768 ? 400 : 160;
    for (let i = 0; i < numPlankton; i++) {
      planktons.push(new Plankton());
    }
    window.requestAnimationFrame(animate);
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);
    for (let p of planktons) {
      p.update();
      p.draw();
    }

    // Connect particles near mouse
    for (let i = 0; i < planktons.length; i++) {
      for (let j = i + 1; j < planktons.length; j++) {
        let dx = planktons[i].x - planktons[j].x;
        let dy = planktons[i].y - planktons[j].y;
        let distSq = dx * dx + dy * dy;
        if (distSq < 4000) {
          let dMouse1 = Math.pow(mouse.x - planktons[i].x, 2) + Math.pow(mouse.y - planktons[i].y, 2);
          let dMouse2 = Math.pow(mouse.x - planktons[j].x, 2) + Math.pow(mouse.y - planktons[j].y, 2);
          let radSq = mouse.radius * mouse.radius;

          if (dMouse1 < radSq || dMouse2 < radSq) {
            ctx.beginPath();
            ctx.strokeStyle = planktons[i].color;
            ctx.globalAlpha = 0.2 * (1 - distSq / 4000) * (planktons[i].glow / planktons[i].maxGlow);
            ctx.lineWidth = 1;
            ctx.moveTo(planktons[i].x, planktons[i].y);
            ctx.lineTo(planktons[j].x, planktons[j].y);
            ctx.stroke();
          }
        }
      }
    }
    window.requestAnimationFrame(animate);
  }

  setTimeout(init, 100);
}

document.addEventListener('DOMContentLoaded', initPlanktonCanvas);

// ---- Email Anti-Spam ----
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.em-lock').forEach(el => {
    try {
      const decoded = atob(el.dataset.em);
      if (el.tagName === 'A') {
        el.href = 'mailto:' + decoded;
        if (el.innerText.trim() === '') el.innerText = decoded;
      } else {
        el.innerText = decoded;
      }
    } catch(e) {}
  });
  document.querySelectorAll('.enc-text').forEach(el => {
    try { el.innerText = atob(el.dataset.val); } catch(e) {}
  });
  document.querySelectorAll('.enc-link').forEach(el => {
    try {
      el.href = (el.dataset.prefix || '') + atob(el.dataset.val);
      el.innerText = el.dataset.text ? atob(el.dataset.text) : atob(el.dataset.val);
    } catch(e) {}
  });
});
