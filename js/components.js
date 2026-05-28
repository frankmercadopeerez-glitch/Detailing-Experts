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
    favicon.type = "image/svg+xml";
    favicon.href = base + "favicon.svg";
    document.head.appendChild(favicon);
  }

  /* ─── Navigation HTML ───────────────────────────────────────── */
  const navHTML = `
<nav class="nav" id="main-nav" role="navigation" aria-label="Navegación principal">
  <div class="nav__container">

    <a href="${base}index.html" class="nav__logo" aria-label="Detailing Experts – Inicio">
      <div class="nav__logo-mark" aria-hidden="true">EX</div>
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
        📲 Cotizar
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
     class="btn btn-primary btn-lg" target="_blank" rel="noopener noreferrer" style="margin-top:1rem;">
     📲 Cotizar ahora
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
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
            </svg>
          </a>
          <a href="https://www.tiktok.com/@detailing.experts" target="_blank" rel="noopener noreferrer"
             class="footer__social-link" aria-label="TikTok" role="listitem">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1V9.01a6.33 6.33 0 00-.79-.05 6.34 6.34 0 00-6.34 6.34 6.34 6.34 0 006.34 6.34 6.34 6.34 0 006.33-6.34V8.97a8.27 8.27 0 004.84 1.55V7.08a4.86 4.86 0 01-1.07-.39z"/>
            </svg>
          </a>
          <a href="https://wa.me/573016501515" target="_blank" rel="noopener noreferrer"
             class="footer__social-link" aria-label="WhatsApp" role="listitem">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
            </svg>
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
          <span class="footer__contact-icon" aria-hidden="true">📞</span>
          <p class="footer__contact-text">
            <a href="tel:+573016501515">+57 301 6501515</a>
          </p>
        </div>
        <div class="footer__contact-item">
          <span class="footer__contact-icon" aria-hidden="true">💬</span>
          <p class="footer__contact-text">
            <a href="https://wa.me/573016501515" target="_blank" rel="noopener noreferrer">WhatsApp Directo</a>
          </p>
        </div>
        <div class="footer__contact-item">
          <span class="footer__contact-icon" aria-hidden="true">📸</span>
          <p class="footer__contact-text">
            <a href="https://www.instagram.com/detailingexperts.x/" target="_blank" rel="noopener noreferrer">@detailingexperts.x</a>
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
    const path = window.location.pathname;
    document.querySelectorAll("[data-page]").forEach((el) => {
      const page = el.dataset.page;
      const active =
        (page === "home" &&
          (path.endsWith("index.html") || path.endsWith("/"))) ||
        (page === "servicios" && path.includes("/servicios/")) ||
        (page === "blog" && path.includes("/blog/")) ||
        (page === "nosotros" && path.includes("nosotros")) ||
        (page === "contacto" && path.includes("contacto"));
      if (active) el.classList.add("active");
    });
  });
})();
