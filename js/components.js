/**
 * Detailing Experts — Shared Components
 * Injects header and footer into every page.
 * Set `window.basePath` BEFORE loading this script:
 *   - Root pages:   <script>window.basePath = '';</script>
 *   - Sub-folders:  <script>window.basePath = '../';</script>
 */

(function () {
  const base = window.basePath || "";

  /* ─── Inject Barlow Condensed font ──────────────────────────── */
  if (!document.querySelector('link[href*="Barlow+Condensed"]')) {
    const fontLink = document.createElement("link");
    fontLink.rel = "stylesheet";
    fontLink.href =
      "https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,700;0,800;0,900;1,700&display=swap";
    document.head.appendChild(fontLink);
  }

  /* ─── Inject favicon ─────────────────────────────────────────── */
  if (!document.querySelector('link[rel="icon"]')) {
    const favicon = document.createElement("link");
    favicon.rel = "icon";
    favicon.type = "image/png";
    favicon.href = base + "images/favicon-circle.png";
    document.head.appendChild(favicon);
  }

  /* ─── Navigation HTML ───────────────────────────────────────── */
  const navHTML = `
<nav class="nav" id="main-nav" role="navigation" aria-label="Navegación principal">
  <div class="nav__container">

    <a href="${base}index.html" class="nav__logo" aria-label="Detailing Experts – Inicio">
      <img src="${base}images/Detailing%20(4).PNG" alt="" aria-hidden="true" class="nav__logo-mark-img">
      <div class="nav__logo-text">
        <span class="nav__logo-name">Detailing Experts</span>
        <span class="nav__logo-tagline">Cartagena · Premium</span>
      </div>
    </a>

    <ul class="nav__links" role="list">
      <li><a href="${base}index.html"              class="nav__link" data-page="home">Inicio</a></li>
      <li><a href="${base}servicios/index.html"    class="nav__link" data-page="servicios">Servicios</a></li>
      <li><a href="${base}blog/index.html"         class="nav__link" data-page="blog">Blog</a></li>
      <li><a href="${base}nosotros.html"           class="nav__link" data-page="nosotros">Nosotros</a></li>
      <li><a href="${base}contacto.html"           class="nav__link" data-page="contacto">Contacto</a></li>
    </ul>

    <div class="nav__actions">
      <a href="https://wa.me/573016501515?text=Hola%2C%20me%20interesa%20cotizar%20un%20servicio."
         class="nav__cta" target="_blank" rel="noopener noreferrer" aria-label="Cotizar por WhatsApp">
        <img src="${base}images/whatsapp-logo.png" alt="" aria-hidden="true" class="nav__cta-icon">
        <span>Cotizar</span>
      </a>
    </div>

    <button class="nav__hamburger" id="nav-hamburger" aria-label="Abrir menú" aria-expanded="false" aria-controls="mobile-nav">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>

<div class="nav__mobile" id="mobile-nav" role="dialog" aria-modal="true" aria-label="Menú móvil">
  <a href="${base}index.html"              class="nav__mobile-link" data-page="home">Inicio</a>
  <a href="${base}servicios/index.html"    class="nav__mobile-link" data-page="servicios">Servicios</a>
  <a href="${base}blog/index.html"         class="nav__mobile-link" data-page="blog">Blog</a>
  <a href="${base}nosotros.html"           class="nav__mobile-link" data-page="nosotros">Nosotros</a>
  <a href="${base}contacto.html"           class="nav__mobile-link" data-page="contacto">Contacto</a>
  <a href="https://wa.me/573016501515?text=Hola%2C%20me%20interesa%20cotizar%20un%20servicio."
      class="btn btn-outline-white btn-lg" target="_blank" rel="noopener noreferrer" style="margin-top:1rem;">
      <img src="${base}images/whatsapp-logo.png" alt="" aria-hidden="true" class="btn__icon">
      Cotizar ahora
  </a>
</div>`;

  /* ─── Footer HTML ───────────────────────────────────────────── */
  const footerHTML = `
<footer class="footer" role="contentinfo">
  <div class="container">
    <div class="footer__grid">

      <!-- Brand -->
      <div class="footer__brand">
        <a href="${base}index.html" class="footer__logo" aria-label="Detailing Experts – Inicio">
          <div class="footer__logo-mark" aria-hidden="true">EX</div>
          <span class="footer__logo-name">Detailing Experts</span>
        </a>
        <p class="footer__tagline">El arte del detalle, a detalle.</p>
        <p class="footer__desc">
          Especialistas en protección premium de automóviles en Cartagena de Indias.
          Fundada en 2024 por expertos con más de 10 años en el sector automotriz.
        </p>
        <div class="footer__social" role="list" aria-label="Redes sociales">
          <a href="https://www.instagram.com/detailingexperts.x/" target="_blank" rel="noopener noreferrer"
             class="footer__social-link" aria-label="Instagram" role="listitem">
            <img src="${base}images/instagram-logo.png" alt="" aria-hidden="true">
            <span class="footer__social-text">Instagram</span>
          </a>
          <a href="https://www.facebook.com/" target="_blank" rel="noopener noreferrer"
             class="footer__social-link" aria-label="Facebook" role="listitem">
            <img src="${base}images/logo-facebook.png" alt="" aria-hidden="true">
            <span class="footer__social-text">Facebook</span>
          </a>
          <a href="https://x.com/" target="_blank" rel="noopener noreferrer"
             class="footer__social-link" aria-label="X" role="listitem">
            <img src="${base}images/X.png" alt="" aria-hidden="true">
            <span class="footer__social-text">X</span>
          </a>
          <a href="https://wa.me/573016501515" target="_blank" rel="noopener noreferrer"
             class="footer__social-link" aria-label="WhatsApp" role="listitem">
            <img src="${base}images/whatsapp-logo.png" alt="" aria-hidden="true">
            <span class="footer__social-text">WhatsApp</span>
          </a>
        </div>
      </div>

      <!-- Servicios -->
      <div>
        <h3 class="footer__heading">Servicios</h3>
        <ul class="footer__links" role="list">
          <li><a href="${base}servicios/detailing-premium.html"          class="footer__link">Detailing Premium</a></li>
          <li><a href="${base}servicios/ppf.html"                        class="footer__link">Paint Protection Film</a></li>
          <li><a href="${base}servicios/proteccion-anticorrosiva.html"   class="footer__link">Protección Anticorrosiva</a></li>
          <li><a href="${base}servicios/polarizados.html"                class="footer__link">Polarizados</a></li>
          <li><a href="${base}servicios/wrap.html"                       class="footer__link">Wrap Vinílico</a></li>
          <li><a href="${base}servicios/pdr.html"                        class="footer__link">PDR – Sin Repintar</a></li>
          <li><a href="${base}servicios/latoneria-pintura.html"          class="footer__link">Latonería y Pintura</a></li>
        </ul>
      </div>

      <!-- Navegación -->
      <div>
        <h3 class="footer__heading">Navegación</h3>
        <ul class="footer__links" role="list">
          <li><a href="${base}index.html"           class="footer__link">Inicio</a></li>
          <li><a href="${base}servicios/index.html" class="footer__link">Todos los Servicios</a></li>
          <li><a href="${base}blog/index.html"      class="footer__link">Blog</a></li>
          <li><a href="${base}nosotros.html"        class="footer__link">Nosotros</a></li>
          <li><a href="${base}contacto.html"        class="footer__link">Contacto</a></li>
        </ul>
      </div>

      <!-- Contacto -->
      <div>
        <h3 class="footer__heading">Contacto</h3>
        <div class="footer__contact-item">
          <span class="footer__contact-icon" aria-hidden="true">📍</span>
          <p class="footer__contact-text">
            Cl. 31 #52-20, Progreso<br>
            Cartagena de Indias, Bolívar<br>
            <em style="font-size:0.8em;opacity:0.8">Frente a la Plaza de Toros</em>
          </p>
        </div>
        <div class="footer__contact-item">
          <span class="footer__contact-icon" aria-hidden="true">🕐</span>
          <p class="footer__contact-text">
            Lunes – Sábado: 8:00 am – 6:00 pm<br>
            Domingos: Previa cita
          </p>
        </div>
      </div>

    </div><!-- /footer__grid -->

    <div class="footer__bottom">
      <p class="footer__copyright">
        © 2025 Detailing Experts · Todos los derechos reservados · Cartagena de Indias, Colombia
      </p>
      <ul class="footer__bottom-links" role="list">
        <li><a href="${base}contacto.html" class="footer__bottom-link">Contacto</a></li>
        <li><a href="${base}blog/index.html" class="footer__bottom-link">Blog</a></li>
        <li><a href="${base}sitemap.xml" class="footer__bottom-link">Sitemap</a></li>
      </ul>
    </div>
  </div>
</footer>`;

  /* ─── WhatsApp floating button ──────────────────────────────── */
  const waFloat = `
<a href="https://wa.me/573016501515?text=Hola%2C%20me%20interesa%20cotizar%20un%20servicio."
   class="whatsapp-float" target="_blank" rel="noopener noreferrer"
   aria-label="Contactar por WhatsApp">
  <div class="whatsapp-float__pulse" aria-hidden="true"></div>
  <img src="${base}images/WhatsApp.svg.webp" alt="WhatsApp" width="62" height="62" loading="lazy">
</a>`;

  /* ─── Inject components ─────────────────────────────────────── */
  document.addEventListener("DOMContentLoaded", function () {
    const navSlot = document.getElementById("nav-placeholder");
    const footerSlot = document.getElementById("footer-placeholder");

    if (navSlot) navSlot.outerHTML = navHTML;
    if (footerSlot) footerSlot.outerHTML = footerHTML + waFloat;

    // Mark active nav link
    const path = window.location.pathname.toLowerCase();
    const segments = path.split("/").filter(Boolean);
    const inServicios = segments.includes("servicios");
    const inBlog = segments.includes("blog");
    const isHomePath =
      segments.length === 0 ||
      (segments.length === 1 && segments[0] === "index.html");
    document.querySelectorAll("[data-page]").forEach((el) => {
      const page = el.dataset.page;
      const active =
        (page === "home" && isHomePath && !inServicios && !inBlog) ||
        (page === "servicios" && inServicios) ||
        (page === "blog" && inBlog) ||
        (page === "nosotros" && path.includes("nosotros")) ||
        (page === "contacto" && path.includes("contacto"));
      if (active) el.classList.add("active");
    });
  });
})();
