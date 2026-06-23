# -*- coding: utf-8 -*-
"""Genera el blog con URLs ESTATICAS separadas: index + paginacion + pagina por categoria.
Cada pagina es un HTML real e indexable, con navegacion por enlaces (sin depender de JS)."""
import os, re, glob, html, json, math
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "blog")
PAGE_SIZE = 9
BASEURL = "https://detailingexperts.com/blog/"

def esc(s): return html.escape(s, quote=True)

# canonical -> (etiqueta, url-slug, H1, intro SEO, title, meta description)
CATS = ["anticorrosiva","ppf","ceramic","detailing","polarizado","wrap","pdr","pintura","mantenimiento","guias"]
CAT = {
 "anticorrosiva": ("Protección Anticorrosiva","anticorrosiva","Protección Anticorrosiva: Artículos y Guías",
    "Todo sobre la protección anticorrosiva en Cartagena: cómo el salitre ataca tu vehículo, precios, tratamiento de óxido y mantenimiento preventivo.",
    "Artículos sobre Protección Anticorrosiva en Cartagena | Blog Detailing Experts",
    "Guías y consejos sobre protección anticorrosiva para vehículos en Cartagena: salitre, óxido, precios y mantenimiento."),
 "ppf": ("PPF","ppf","PPF Paint Protection Film: Artículos y Guías",
    "Guías sobre PPF en Cartagena: qué protege, cobertura parcial o completa, autorreparación, precios y comparativas.",
    "Artículos sobre PPF (Paint Protection Film) en Cartagena | Blog Detailing Experts",
    "Todo sobre Paint Protection Film en Cartagena: protección contra piedras y rayones, precios y comparativas."),
 "ceramic": ("Ceramic Coating","ceramic-coating","Ceramic Coating: Artículos y Guías",
    "Aprende sobre ceramic coating en Cartagena: durabilidad, efecto hidrofóbico, protección UV, precios y diferencias con la cera.",
    "Artículos sobre Ceramic Coating en Cartagena | Blog Detailing Experts",
    "Guías sobre ceramic coating en Cartagena: brillo, hidrofobicidad, durabilidad y precios."),
 "detailing": ("Detailing","detailing","Detailing Automotriz: Artículos y Guías",
    "Consejos de detailing en Cartagena: corrección de pintura, limpieza profunda de interior, diferencias con el autolavado y precios.",
    "Artículos sobre Detailing Automotriz en Cartagena | Blog Detailing Experts",
    "Guías de detailing premium en Cartagena: corrección de pintura, interior, precios y mantenimiento."),
 "polarizado": ("Polarizado","polarizado","Polarizado Automotriz: Artículos y Guías",
    "Información sobre polarizado en Cartagena: legalidad en Colombia, rechazo de calor, protección UV y precios.",
    "Artículos sobre Polarizado Automotriz en Cartagena | Blog Detailing Experts",
    "Guías sobre polarizado de vidrios en Cartagena: legalidad, calor, UV y precios."),
 "wrap": ("Wrap","wrap","Wrap Vinílico: Artículos y Guías",
    "Todo sobre el wrap vinílico en Cartagena: cambio de color, acabados, reversibilidad, durabilidad y precios.",
    "Artículos sobre Wrap Vinílico en Cartagena | Blog Detailing Experts",
    "Guías sobre wrap vinílico en Cartagena: cambio de color, acabados, reversibilidad y precios."),
 "pdr": ("PDR","pdr","PDR – Reparación sin Pintura: Artículos y Guías",
    "Conoce el PDR (Paintless Dent Repair) en Cartagena: reparación de abolladuras sin repintar, conservando la pintura original.",
    "Artículos sobre PDR (Reparación sin Pintura) en Cartagena | Blog Detailing Experts",
    "Guías sobre PDR en Cartagena: reparación de abolladuras sin pintura, ventajas y casos."),
 "pintura": ("Latonería y Pintura","latoneria-pintura","Latonería y Pintura: Artículos y Guías",
    "Guías de latonería y pintura en Cartagena: reparación de golpes, igualación de color, óxido y acabados de fábrica.",
    "Artículos sobre Latonería y Pintura en Cartagena | Blog Detailing Experts",
    "Guías sobre latonería y pintura en Cartagena: golpes, óxido, igualación de color y precios."),
 "mantenimiento": ("Mantenimiento","mantenimiento","Mantenimiento Automotriz: Artículos y Guías",
    "Aprende a mantener tu vehículo en Cartagena: planes preventivos, renovación de protecciones y cuidado en clima costero.",
    "Artículos sobre Mantenimiento Automotriz en Cartagena | Blog Detailing Experts",
    "Guías de mantenimiento preventivo automotriz en Cartagena: planes, protecciones y cuidado costero."),
 "guias": ("Guías y Modelos","guias","Guías por Modelo y Comparativas",
    "Guías de cuidado por modelo de vehículo y comparativas de servicios para ayudarte a elegir la mejor protección en Cartagena.",
    "Guías por Modelo y Comparativas de Servicios | Blog Detailing Experts",
    "Guías por modelo de auto y comparativas de servicios de protección automotriz en Cartagena."),
}
TODOS_META = ("Todos","Blog: Tips y Guías de Cuidado Automotriz",
    "Guías prácticas sobre protección, detailing, polarizado y precios para el exigente clima costero de Cartagena. Filtra por la categoría que te interese.",
    "Blog Detailing Experts | Cuidado Automotriz en Cartagena",
    "Artículos y guías sobre detailing, protección anticorrosiva, PPF, ceramic coating y polarizado para tu vehículo en Cartagena.")

def detect_cat(slug, title):
    s = (slug + " " + title).lower()
    if "ppf" in s: return "ppf"
    if "ceramic" in s: return "ceramic"
    if "wrap" in s: return "wrap"
    if "polariz" in s or "tintado" in s: return "polarizado"
    if "pdr" in s: return "pdr"
    if "anticorros" in s or "oxidacion" in s or "oxida" in s or "salitre" in s or "galvaniz" in s: return "anticorrosiva"
    if "latoneria" in s or "rayones" in s or "manchas" in s or "compound" in s or "polish" in s or "pintura" in s: return "pintura"
    if "detailing" in s or "lavado" in s or "pulida" in s: return "detailing"
    if "mantenimiento" in s: return "mantenimiento"
    return "guias"

def url_for(view, page):
    if view == "todos":
        return "index.html" if page == 1 else f"pagina-{page}.html"
    slug = CAT[view][1]
    return f"categoria-{slug}.html" if page == 1 else f"categoria-{slug}-{page}.html"

def collect():
    posts = []
    listing_re = re.compile(r"^(index|pagina-\d+|categoria-)")
    for path in sorted(glob.glob(os.path.join(BLOG, "*.html"))):
        fn = os.path.basename(path); slug = fn[:-5]
        if fn == "index.html" or listing_re.match(slug):  # excluir paginas de listado
            continue
        raw = open(path, encoding="utf-8", errors="ignore").read()
        mt = re.search(r"<title>(.*?)</title>", raw, re.S)
        title = (mt.group(1).strip() if mt else slug)
        title = re.sub(r"\s*\|\s*(Blog\s*)?Detailing Experts.*$", "", title).strip()
        md = re.search(r'name="description"\s+content="(.*?)"', raw, re.S)
        desc = (md.group(1).strip() if md else title)
        mi = re.search(r'(https://images\.unsplash\.com/[^"?]+)', raw)
        img_id = mi.group(1).split("/")[-1] if mi else "photo-1607860108855-64acf2078ed9"
        posts.append({"slug":slug,"title":title,"desc":desc,"img_id":img_id,"cat":detect_cat(slug,title)})
    posts.sort(key=lambda p: p["title"].lower())
    return posts

def card_html(p, label):
    img = f"https://images.unsplash.com/{p['img_id']}?auto=format&fit=crop&w=800&q=80"
    excerpt = p["desc"]
    if len(excerpt) > 160:
        excerpt = excerpt[:157].rsplit(" ", 1)[0] + "…"
    return f'''          <article class="blog-card">
            <a href="{p['slug']}.html" class="blog-card__img-wrap" aria-hidden="true" tabindex="-1">
              <img src="{img}" alt="{esc(p['title'])}" loading="lazy" width="800" height="200">
            </a>
            <div class="blog-card__body">
              <span class="blog-card__cat">{esc(label)}</span>
              <h2 class="blog-card__title"><a href="{p['slug']}.html">{esc(p['title'])}</a></h2>
              <p class="blog-card__excerpt">{esc(excerpt)}</p>
              <a href="{p['slug']}.html" class="blog-card__link">Leer artículo →</a>
            </div>
          </article>'''

def nav_html(active_view):
    chips = []
    cls = "blog-filter-btn active" if active_view == "todos" else "blog-filter-btn"
    chips.append(f'<a class="{cls}" href="index.html">Todos</a>')
    for c in CATS:
        cls = "blog-filter-btn active" if active_view == c else "blog-filter-btn"
        chips.append(f'<a class="{cls}" href="{url_for(c,1)}">{esc(CAT[c][0])}</a>')
    return "\n          ".join(chips)

def pagination_html(view, page, total_pages):
    if total_pages <= 1:
        return ""
    parts = []
    # prev
    if page > 1:
        parts.append(f'<a class="blog-page-link" href="{url_for(view,page-1)}" rel="prev" aria-label="Anterior">‹</a>')
    else:
        parts.append('<span class="blog-page-link is-disabled" aria-hidden="true">‹</span>')
    for i in range(1, total_pages+1):
        if i == page:
            parts.append(f'<span class="blog-page-link active" aria-current="page">{i}</span>')
        else:
            parts.append(f'<a class="blog-page-link" href="{url_for(view,i)}">{i}</a>')
    if page < total_pages:
        parts.append(f'<a class="blog-page-link" href="{url_for(view,page+1)}" rel="next" aria-label="Siguiente">›</a>')
    else:
        parts.append('<span class="blog-page-link is-disabled" aria-hidden="true">›</span>')
    return '<nav class="blog-pagination" aria-label="Paginación">\n      ' + "\n      ".join(parts) + '\n    </nav>'

def render_page(view, page, total_pages, page_posts, label_for_cards):
    if view == "todos":
        _, h1, intro, title_base, desc = TODOS_META
        label = "Todos"
    else:
        label, _, h1, intro, title_base, desc = CAT[view]
    url = url_for(view, page)
    canon = BASEURL + url
    if page > 1:
        title = f"{title_base} – Página {page}"
        desc = f"{desc} Página {page}."
    else:
        title = title_base
    # rel prev/next
    rellinks = ""
    if page > 1:
        rellinks += f'\n<link rel="prev" href="{BASEURL+url_for(view,page-1)}">'
    if page < total_pages:
        rellinks += f'\n<link rel="next" href="{BASEURL+url_for(view,page+1)}">'

    breadcrumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Inicio","item":"https://detailingexperts.com/"},
        {"@type":"ListItem","position":2,"name":"Blog","item":BASEURL+"index.html"}]}
    if view != "todos":
        breadcrumb["itemListElement"].append({"@type":"ListItem","position":3,"name":label,"item":BASEURL+url_for(view,1)})

    cards = "\n".join(card_html(p, CAT[p["cat"]][0]) for p in page_posts)
    intro_p = f'<p class="hero__desc" style="max-width:660px;">{esc(intro)}</p>' if page == 1 else \
              f'<p class="hero__desc" style="max-width:660px;">Página {page} de artículos. {esc(intro)}</p>'

    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canon}">{rellinks}
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="https://images.unsplash.com/photo-1607860108855-64acf2078ed9?auto=format&fit=crop&w=1200&q=80">
<link rel="preconnect" href="https://images.unsplash.com">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/style.min.css">
<script type="application/ld+json">{json.dumps(breadcrumb, ensure_ascii=False)}</script>
</head>
<body>
<div id="nav-placeholder"></div>

<header class="page-hero page-hero--sm">
  <div class="page-hero__overlay" aria-hidden="true" style="background:linear-gradient(135deg,rgba(8,12,24,0.9) 40%,rgba(0,204,255,0.08) 100%);"></div>
  <div class="page-hero__content">
    <span class="section-label">Blog · Detailing Experts</span>
    <h1 class="hero__title" style="max-width:780px;">{esc(h1)}</h1>
    {intro_p}
  </div>
</header>

<section class="section" id="blog-list">
  <div class="container">
    <nav class="blog-filters" aria-label="Categorías del blog">
          {nav_html(view)}
    </nav>

    <div class="blog-grid">
{cards}
    </div>

    {pagination_html(view, page, total_pages)}
  </div>
</section>

<section class="cta-section">
  <div class="container" style="position:relative;z-index:1;text-align:center;">
    <h2 class="section-title" style="color:var(--clr-white);margin-bottom:1rem;">¿Listo para <span class="highlight">Cuidar tu Auto</span>?</h2>
    <p class="cta-section__desc" style="margin-inline:auto;">Pon en práctica lo que aprendiste. Cotiza el servicio que necesitas hoy.</p>
    <a href="https://wa.me/573016501515?text=Hola%2C%20le%C3%AD%20su%20blog%20y%20quiero%20cotizar%20un%20servicio." class="btn btn-whatsapp btn-lg" target="_blank" rel="noopener noreferrer"><img src="../images/whatsapp-logo.png" alt="" aria-hidden="true" class="btn__icon" width="20" height="20">Cotizar ahora</a>
  </div>
</section>

<div id="footer-placeholder"></div>
<script>window.basePath = "../";</script>
<script src="../js/components.js" defer></script>
<script src="../js/main.js" defer></script>
</body>
</html>'''

def main():
    posts = collect()
    by_cat = defaultdict(list)
    for p in posts:
        by_cat[p["cat"]].append(p)

    written = []
    # limpiar paginas de listado viejas (pagina-*, categoria-*) antes de regenerar
    for old in glob.glob(os.path.join(BLOG, "pagina-*.html")) + glob.glob(os.path.join(BLOG, "categoria-*.html")):
        os.remove(old)

    def emit(view, view_posts):
        total = max(1, math.ceil(len(view_posts)/PAGE_SIZE))
        for page in range(1, total+1):
            chunk = view_posts[(page-1)*PAGE_SIZE: page*PAGE_SIZE]
            htmlout = render_page(view, page, total, chunk, None)
            fn = url_for(view, page)
            with open(os.path.join(BLOG, fn), "w", encoding="utf-8") as f:
                f.write(htmlout)
            written.append(fn)

    emit("todos", posts)
    for c in CATS:
        if by_cat.get(c):
            emit(c, by_cat[c])

    # devolver lista de urls para sitemap
    print("Paginas de listado generadas:", len(written))
    for w in written: print("  ", w)
    # guardar lista para el sitemap
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "listing_urls.txt"), "w", encoding="utf-8") as f:
        for w in written:
            f.write("blog/"+w+"\n")

if __name__ == "__main__":
    main()
