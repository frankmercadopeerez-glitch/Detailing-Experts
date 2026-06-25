# -*- coding: utf-8 -*-
"""Anade breadcrumb visible + 'Articulos relacionados' (enlaces blog->blog) a los
posts del blog generados. Idempotente: se puede re-ejecutar tras anadir articulos."""
import os, re, glob, html
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "blog")
def esc(s): return html.escape(s, quote=True)

CAT_LABEL = {
 "anticorrosiva":"Protección Anticorrosiva","ppf":"PPF","ceramic":"Ceramic Coating",
 "detailing":"Detailing","polarizado":"Polarizado","wrap":"Wrap","pdr":"PDR",
 "pintura":"Latonería y Pintura","mantenimiento":"Mantenimiento","guias":"Guías y Modelos"}
CAT_URL = {
 "anticorrosiva":"categoria-anticorrosiva.html","ppf":"categoria-ppf.html",
 "ceramic":"categoria-ceramic-coating.html","detailing":"categoria-detailing.html",
 "polarizado":"categoria-polarizado.html","wrap":"categoria-wrap.html","pdr":"categoria-pdr.html",
 "pintura":"categoria-latoneria-pintura.html","mantenimiento":"categoria-mantenimiento.html",
 "guias":"categoria-guias.html"}

def detect(slug, title):
    s=(slug+" "+title).lower()
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

def clean_title(raw):
    m=re.search(r"<title>(.*?)</title>", raw, re.S)
    t=(m.group(1).strip() if m else "")
    t=re.sub(r"\s*\|\s*(Blog\s*)?Detailing Experts.*$","",t).strip()
    return re.sub(r"\s+"," ",t)

def main():
    listing=re.compile(r"^(index|pagina-\d+|categoria-)")
    posts={}
    for p in sorted(glob.glob(os.path.join(BLOG,"*.html"))):
        fn=os.path.basename(p); slug=fn[:-5]
        if fn=="index.html" or listing.match(slug): continue
        raw=open(p,encoding="utf-8",errors="ignore").read()
        posts[slug]={"raw":raw,"title":clean_title(raw),"cat":None,"injectable":'class="container post-content"' in raw}
    for slug,d in posts.items():
        d["cat"]=detect(slug,d["title"])
    bycat=defaultdict(list)
    for slug,d in posts.items():
        bycat[d["cat"]].append(slug)

    done=0
    for slug,d in posts.items():
        if not d["injectable"]: continue
        raw=d["raw"]
        # quitar inyecciones previas (idempotencia)
        raw=re.sub(r"<!--BC-->.*?<!--/BC-->","",raw,flags=re.S)
        raw=re.sub(r"<!--REL-->.*?<!--/REL-->","",raw,flags=re.S)
        cat=d["cat"]
        # breadcrumb visible (3 niveles, coincide con el schema BreadcrumbList)
        bc=(f'<!--BC--><nav class="breadcrumb" aria-label="Ruta de navegación">'
            f'<a href="../index.html">Inicio</a><span class="breadcrumb__sep">›</span>'
            f'<a href="index.html">Blog</a><span class="breadcrumb__sep">›</span>'
            f'<a href="{CAT_URL[cat]}">{esc(CAT_LABEL[cat])}</a><span class="breadcrumb__sep">›</span>'
            f'<span aria-current="page">{esc(d["title"])}</span></nav><!--/BC-->')
        # relacionados: 3 de la misma categoria (sin el actual); rellenar si faltan
        rel=[s for s in bycat[cat] if s!=slug]
        if len(rel)<3:
            extra=[s for s in posts if s!=slug and s not in rel]
            rel=rel+extra
        rel=rel[:3]
        cards=""
        for r in rel:
            cards+=(f'<a class="feature-item" style="text-decoration:none;display:block;" href="{r}.html">'
                    f'<span class="blog-card__cat" style="margin-bottom:.6rem;">{esc(CAT_LABEL[posts[r]["cat"]])}</span>'
                    f'<h3 class="feature-item__title" style="font-size:var(--text-lg);">{esc(posts[r]["title"])}</h3>'
                    f'<span style="color:var(--clr-accent);font-weight:600;font-size:.9rem;">Leer artículo →</span></a>')
        relsec=(f'<!--REL--><section class="section section--alt"><div class="container">'
                f'<div class="section-header centered"><span class="section-label">Sigue leyendo</span>'
                f'<h2 class="section-title">Artículos relacionados</h2></div>'
                f'<div class="feature-grid">{cards}</div></div></section><!--/REL-->')
        # inyectar breadcrumb tras el contenedor del articulo
        raw=raw.replace('<div class="container post-content">',
                        '<div class="container post-content">\n    '+bc,1)
        # inyectar relacionados antes del CTA
        raw=raw.replace('<section class="cta-section">', relsec+'\n\n<section class="cta-section">',1)
        open(os.path.join(BLOG,slug+".html"),"w",encoding="utf-8").write(raw)
        done+=1
    print(f"Posts mejorados (breadcrumb + relacionados): {done}")

if __name__=="__main__":
    main()
