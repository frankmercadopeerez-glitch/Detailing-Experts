/**
 * Detailing Experts — Main JavaScript
 * Scroll effects · Mobile menu · Reveal animations · Counter animation
 */

(function () {
  "use strict";

  /* ─── Nav scroll effect ──────────────────────────────────────── */
  const nav = document.getElementById("main-nav");
  if (nav) {
    const onScroll = () => {
      nav.classList.toggle("scrolled", window.scrollY > 40);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ─── Mobile menu ────────────────────────────────────────────── */
  document.addEventListener("click", function (e) {
    const btn = document.getElementById("nav-hamburger");
    const mobileNav = document.getElementById("mobile-nav");
    if (!btn || !mobileNav) return;

    if (e.target.closest("#nav-hamburger")) {
      const open = btn.classList.toggle("open");
      mobileNav.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", open);
      document.body.style.overflow = open ? "hidden" : "";
    } else if (!e.target.closest("#mobile-nav")) {
      btn.classList.remove("open");
      mobileNav.classList.remove("open");
      btn.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    }
  });

  // Close mobile nav on link click
  document.addEventListener("click", function (e) {
    if (e.target.closest("#mobile-nav a")) {
      const btn = document.getElementById("nav-hamburger");
      const mobileNav = document.getElementById("mobile-nav");
      if (btn) btn.classList.remove("open");
      if (mobileNav) mobileNav.classList.remove("open");
      document.body.style.overflow = "";
    }
  });

  /* ─── Reveal on scroll ───────────────────────────────────────── */
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("revealed");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" },
  );

  document
    .querySelectorAll(".reveal")
    .forEach((el) => revealObserver.observe(el));

  /* ─── Counter animation ──────────────────────────────────────── */
  function animateCounter(el) {
    const target = parseFloat(el.dataset.count || el.textContent);
    const suffix = el.dataset.suffix || "";
    const duration = 1800;
    const start = performance.now();

    const tick = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3); // ease-out-cubic
      const value = target * ease;
      el.textContent =
        (Number.isInteger(target) ? Math.round(value) : value.toFixed(1)) +
        suffix;
      if (progress < 1) requestAnimationFrame(tick);
    };

    requestAnimationFrame(tick);
  }

  const counterObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          counterObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.5 },
  );

  document
    .querySelectorAll("[data-count]")
    .forEach((el) => counterObserver.observe(el));

  /* ─── Smooth anchor scroll ───────────────────────────────────── */
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", function (e) {
      const id = this.getAttribute("href").slice(1);
      const target = document.getElementById(id);
      if (!target) return;
      e.preventDefault();
      const offset = 90;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: "smooth" });
    });
  });

  /* ─── Contact form ───────────────────────────────────────────── */
  const contactForm = document.getElementById("contact-form");
  if (contactForm) {
    contactForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const nombre = encodeURIComponent(this.nombre?.value || "");
      const servicio = encodeURIComponent(this.servicio?.value || "");
      const mensaje = encodeURIComponent(this.mensaje?.value || "");
      const text = `Hola, soy ${nombre}. Me interesa el servicio de ${servicio}. ${mensaje}`;
      window.open(
        `https://wa.me/573016501515?text=${text}`,
        "_blank",
        "noopener,noreferrer",
      );
    });
  }

  /* ─── Lazy load images ───────────────────────────────────────── */
  if ("loading" in HTMLImageElement.prototype) {
    document.querySelectorAll('img[loading="lazy"]').forEach((img) => {
      if (img.dataset.src) img.src = img.dataset.src;
    });
  } else {
    const lazyObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && entry.target.dataset.src) {
          entry.target.src = entry.target.dataset.src;
          lazyObserver.unobserve(entry.target);
        }
      });
    });
    document
      .querySelectorAll("img[data-src]")
      .forEach((img) => lazyObserver.observe(img));
  }
})();
