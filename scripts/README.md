# Scripts de generación de páginas

Estos scripts generan páginas del sitio de forma reproducible. Requieren **Python 3**.
Las rutas se calculan solas (relativas a la carpeta del repo), así que basta con ejecutarlos.

## Qué hace cada uno

| Script | Qué genera |
|--------|------------|
| `generate_rich.py` | Regenera las páginas de **servicios** (contenido, schema, FAQ, enlaces internos). Usa `overrides.txt` para títulos/descripciones corregidos. Solo toca páginas con su firma; no modifica las hechas a mano. |
| `generate_blog.py` | Reprocesa los **posts del blog** auto-generados (contenido + FAQ + schema). Incluye `TITLE_FIX` y `DESC_FIX` con correcciones. |
| `generate_new_articles.py` | Crea/actualiza los **11 artículos cornerstone** (uno por categoría + uno general). El contenido está dentro del script. |
| `generate_blog_pages.py` | Genera las **páginas de listado del blog**: `index.html`, `pagina-N.html` y `categoria-*.html` (con paginación). Léelo después de añadir o quitar artículos. |

## Flujo recomendado al añadir un artículo nuevo al blog

1. Crea el archivo `blog/mi-articulo.html` (o añádelo a `generate_new_articles.py` si quieres mantenerlo versionado).
2. Ejecuta:
   ```bash
   python scripts/generate_blog_pages.py
   ```
   Esto recalcula categorías y paginación e incluye el artículo en los listados.
3. Añade la URL del nuevo artículo a `sitemap.xml` (y cualquier página de listado nueva que se haya creado, p. ej. `pagina-9.html`).

## Notas

- `generate_blog_pages.py` borra y regenera `pagina-*.html` y `categoria-*.html` en cada corrida (son derivados).
- Datos del negocio importantes ya reflejados: la protección **anticorrosiva dura ~1 año** (luego se repinta), el **mantenimiento bimensual es gratuito**, y el precio **sube cuando hay zonas podridas por óxido que se reemplazan con soldadura**.
- La categoría del blog "Protección Anticorrosiva" se define en `generate_blog_pages.py` (dict `CAT`).
