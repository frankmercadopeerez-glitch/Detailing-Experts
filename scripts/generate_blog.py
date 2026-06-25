# -*- coding: utf-8 -*-
"""Enriquece los blog posts delgados con articulos completos, FAQ y enlaces internos."""
import os, re, glob, json, html, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "blog")

def esc(s): return html.escape(s, quote=True)

# Hechos por servicio para tejer en los articulos
FACTS = {
    "anticorrosiva": {
        "name":"protección anticorrosiva","hub":"../servicios/proteccion-anticorrosiva.html",
        "price":"desde 1.2M en autos compactos y desde 1.5M en SUV y camionetas (sube cuando hay zonas podridas por óxido que se reemplazan con soldadura)",
        "dura":"alrededor de 1 año, cuando se recomienda repintar para renovarla; con mantenimiento bimensual gratuito",
        "links":[("Protección Anticorrosiva en Cartagena","../servicios/proteccion-anticorrosiva.html"),
                 ("Precio de protección anticorrosiva","../servicios/precio-anticorrosiva-cartagena.html"),
                 ("Anticorrosiva + reparación de óxido","../servicios/anticorrosiva-reparacion-leve.html")],
        "secs":[
            ("¿Por qué el salitre de Cartagena ataca tu carro?","El aire costero de Cartagena lleva sal en suspensión que se deposita sobre el metal y, con la humedad, acelera la oxidación. Las zonas más afectadas son los bajos del chasis, el interior de las puertas y las cavidades ocultas donde se acumula la sal."),
            ("Qué incluye el tratamiento","Antes de aplicar el recubrimiento inspeccionamos el vehículo. El óxido superficial se lija y neutraliza; cuando hay zonas podridas o perforadas por la corrosión, se reemplazan con soldadura antes de proteger. Luego aplicamos la capa anticorrosiva en carrocería, bajos y cavidades internas para crear una barrera contra la humedad y la sal."),
            ("Duración y mantenimiento gratuito","La protección anticorrosiva dura alrededor de 1 año, momento en que se recomienda repintar para renovarla. Para conservarla incluimos un mantenimiento bimensual totalmente gratuito, en el que revisamos y reforzamos las zonas que lo necesiten."),
        ],
        "faq":[
            ("¿Cuánto cuesta la protección anticorrosiva?","Va desde 1.2M en autos compactos y desde 1.5M en SUV o camionetas. El precio sube cuando hay zonas podridas por el óxido que deben reemplazarse con soldadura; lo evaluamos y cotizamos sin compromiso."),
            ("¿Cuánto dura y cada cuánto se renueva?","Dura alrededor de 1 año, cuando se recomienda repintar para renovar la protección. El mantenimiento bimensual para conservarla es totalmente gratuito."),
            ("¿Sirve si mi carro ya tiene óxido?","Sí. El óxido superficial se trata antes de proteger; y si hay zonas podridas o perforadas, esas partes se reemplazan con soldadura para detener el daño antes de aplicar la anticorrosiva."),
        ],
    },
    "ceramic": {
        "name":"ceramic coating","hub":"../servicios/ceramic-coating-cartagena.html",
        "price":"desde 800K en compactos, 1.2M en sedanes y 1.5M en SUV",
        "dura":"entre 2 y 5 años",
        "links":[("Ceramic Coating en Cartagena","../servicios/ceramic-coating-cartagena.html"),
                 ("Precio de ceramic coating","../servicios/precio-ceramic-coating-cartagena.html"),
                 ("Ceramic vs cera: diferencias","../servicios/cera-vs-ceramic-diferencias.html")],
        "secs":[
            ("Qué es el ceramic coating","Es un recubrimiento líquido a base de SiO₂ que se adhiere a la pintura formando una capa dura, hidrofóbica y brillante. Repele el agua, el polvo y el salitre, y facilita enormemente el lavado del vehículo."),
            ("Por qué dura más que la cera","Mientras una cera tradicional dura semanas, el ceramic coating dura años. Ofrece mayor dureza (hasta 9H), mejor repelencia al agua y una protección UV muy superior, clave bajo el sol intenso de Cartagena."),
            ("Preparación antes de aplicar","Para un resultado impecable descontaminamos la pintura y, si tiene micro-rayones, hacemos una corrección previa. El coating se aplica sobre una superficie perfecta para sellar el brillo por años."),
        ],
        "faq":[
            ("¿Cuánto cuesta el ceramic coating?","Desde 800K en autos compactos, 1.2M en sedanes y 1.5M en SUV. Si la pintura necesita corrección previa, se incluye en la cotización."),
            ("¿Cuánto dura?","Entre 2 y 5 años según el producto y el mantenimiento. Con lavados de pH neutro conserva sus propiedades por mucho más tiempo."),
            ("¿Es mejor que la cera?","Sí. Dura años en lugar de semanas, protege más contra el UV y el salitre, y mantiene el brillo con mucho menos esfuerzo."),
        ],
    },
    "ppf": {
        "name":"PPF (Paint Protection Film)","hub":"../servicios/ppf.html",
        "price":"desde 2M un kit frontal y desde 4M la cobertura completa",
        "dura":"entre 5 y 10 años",
        "links":[("Paint Protection Film (PPF)","../servicios/ppf.html"),
                 ("Precio de PPF en Cartagena","../servicios/precio-ppf-cartagena.html"),
                 ("PPF vs Ceramic Coating","../servicios/wrap-vs-ppf-comparativa.html")],
        "secs":[
            ("Qué protege el PPF","El PPF es una película de uretano transparente que absorbe el impacto de piedras y gravilla, evita rayones y resiste el salitre. Es la barrera física más resistente del mercado y muchas referencias son autorreparables con el calor."),
            ("Cobertura parcial o completa","Un kit frontal (capó, paragolpes y espejos) protege las zonas de mayor impacto; la cobertura completa blinda todo el vehículo. Te recomendamos la opción según tu tipo de uso y presupuesto."),
            ("PPF + ceramic, la dupla ideal","Combinar PPF con ceramic coating ofrece lo mejor de ambos mundos: protección física contra impactos y un acabado hidrofóbico y brillante sobre la película."),
        ],
        "faq":[
            ("¿Cuánto cuesta el PPF?","Un kit frontal parte desde 2M y la cobertura completa desde 4M, según el modelo y las zonas a proteger."),
            ("¿Se nota la película?","No. Es transparente y de alta claridad; una vez instalada mantiene el aspecto de fábrica del vehículo."),
            ("¿De verdad se autorrepara?","Las referencias premium sellan los micro-rayones con el calor del sol o agua caliente. Los cortes profundos no, pero la película evita que lleguen a la pintura."),
        ],
    },
    "wrap": {
        "name":"wrap vinílico","hub":"../servicios/wrap.html",
        "price":"desde 1.2M un wrap parcial y desde 3M un cambio de color completo",
        "dura":"entre 5 y 7 años",
        "links":[("Wrap Vinílico en Cartagena","../servicios/wrap.html"),
                 ("Precio de wrap vinílico","../servicios/precio-wrap-cartagena.html"),
                 ("Wrap vs PPF","../servicios/wrap-vs-ppf-comparativa.html")],
        "secs":[
            ("Qué es el wrap vinílico","Es el recubrimiento de la carrocería con láminas de vinilo para cambiar el color o el acabado sin pintar. Disponible en cientos de colores y texturas —mate, brillante, satinado, carbono, cromo— y totalmente reversible."),
            ("Personalización sin riesgo","Al ser reversible, puedes transformar tu auto y volver al color original cuando quieras, sin afectar la pintura de fábrica. Además, el vinilo protege la pintura de rayones y sol."),
            ("Cuidado del vinilo","Recomendamos lavado a mano con productos suaves y evitar hidrolavadoras a alta presión cerca de los bordes. Con buen cuidado, el vinilo luce impecable durante años."),
        ],
        "faq":[
            ("¿Cuánto cuesta el wrap?","Un wrap parcial parte desde 1.2M y un cambio de color completo desde 3M, según el tamaño del vehículo y el tipo de vinilo."),
            ("¿Daña la pintura?","No. Al retirarse correctamente, la pintura original queda intacta, siempre que esté en buen estado al instalar."),
            ("¿Cuánto dura?","Entre 5 y 7 años con buen mantenimiento. Los vinilos premium resisten bien el sol y el salitre."),
        ],
    },
    "polarizado": {
        "name":"polarizado automotriz","hub":"../servicios/polarizados.html",
        "price":"desde 500K en autos compactos y desde 800K en SUV",
        "dura":"muchos años sin despegarse ni tornarse morado",
        "links":[("Polarizado Automotriz","../servicios/polarizados.html"),
                 ("Precio de polarizado","../servicios/precio-polarizado-cartagena.html"),
                 ("Polarizado legal en Colombia","polarizado-legal-colombia.html")],
        "secs":[
            ("Para qué sirve el polarizado","Las láminas de control solar bloquean hasta el 99% de los rayos UV, reducen el calor interior y aportan privacidad. En el clima de Cartagena, marcan la diferencia entre un interior fresco y uno sofocante."),
            ("Legalidad en Colombia","La norma exige una visibilidad mínima del 70% VLT en parabrisas y vidrios delanteros. Instalamos cumpliendo la regulación para que evites multas y conserves la seguridad."),
            ("Instalación profesional","Trabajamos en ambiente controlado para un acabado uniforme, sin burbujas ni pliegues, con láminas de calidad que ofrecen garantía."),
        ],
        "faq":[
            ("¿Cuánto cuesta el polarizado?","Desde 500K en autos compactos y desde 800K en SUV, según el número de vidrios y el tipo de lámina."),
            ("¿Es legal en Colombia?","Sí, siempre que respete el 70% VLT en parabrisas y vidrios delanteros. Instalamos cumpliendo la norma."),
            ("¿Queda con burbujas?","No. La técnica profesional y el ambiente controlado garantizan un acabado uniforme y duradero."),
        ],
    },
    "detailing": {
        "name":"detailing","hub":"../servicios/detailing-premium.html",
        "price":"desde 500K el detailing básico y desde 1.5M el premium con corrección",
        "dura":"varios meses según el mantenimiento",
        "links":[("Detailing Premium en Cartagena","../servicios/detailing-premium.html"),
                 ("Precio de detailing","../servicios/precio-detailing-cartagena.html"),
                 ("Detailing vs autolavado","../servicios/detailing-casero-vs-profesional.html")],
        "secs":[
            ("Qué es el detailing","Es la limpieza y restauración profunda del vehículo, por dentro y por fuera, a un nivel que ningún autolavado alcanza: descontaminación, corrección de pintura, limpieza detallada del interior y sellado protector."),
            ("Más que limpieza","El detailing devuelve el brillo y la sensación de auto nuevo. En Cartagena, donde el polvo y el salitre ensucian rápido, un detailing periódico mantiene tu inversión impecable y protegida."),
            ("Cada cuánto hacerlo","Para conservar el auto impecable, recomendamos un detailing completo cada 4 a 6 meses, con lavados de mantenimiento entre cada uno."),
        ],
        "faq":[
            ("¿Cuánto cuesta el detailing?","Un detailing básico parte desde 500K y el premium con corrección de pintura y sellado desde 1.5M, según el tamaño y estado del vehículo."),
            ("¿En qué se diferencia del autolavado?","El autolavado limpia la superficie; el detailing descontamina, corrige la pintura, detalla el interior y aplica protección. El resultado y la duración no se comparan."),
            ("¿Incluye interior?","Sí. Limpiamos y desinfectamos tapicería, plásticos y vidrios, eliminando olores y devolviendo el aspecto de nuevo."),
        ],
    },
    "pintura": {
        "name":"latonería y pintura","hub":"../servicios/latoneria-pintura.html",
        "price":"desde 200K un rayón superficial y desde 800K la reparación de un panel",
        "dura":"permanente con tratamiento anticorrosivo",
        "links":[("Latonería y Pintura","../servicios/latoneria-pintura.html"),
                 ("Pintura oxidada: cómo repararla","../servicios/pintura-oxidada-reparar-cartagena.html"),
                 ("Reparación de óxido + anticorrosiva","../servicios/anticorrosiva-reparacion-leve.html")],
        "secs":[
            ("Cuándo actuar","Burbujas, manchas marrones o rojizas y zonas que se levantan indican óxido bajo la pintura. Actuar a tiempo evita que la corrosión se extienda y encarezca la reparación."),
            ("El proceso de reparación","Reparamos la zona, tratamos el metal contra la corrosión y repintamos con igualación de color computarizada para que la reparación sea imperceptible. En Cartagena sellamos contra el salitre para que el problema no reaparezca."),
            ("Acabado de fábrica","Con la igualación de color y el acabado profesional, la zona reparada queda idéntica al resto de la carrocería, conservando el valor del vehículo."),
        ],
        "faq":[
            ("¿Cuánto cuesta reparar un golpe o rayón?","Un rayón superficial parte desde 200K; la reparación con latonería y repintado de un panel desde 800K, según la extensión del daño."),
            ("¿Cómo sé si hay óxido bajo la pintura?","Burbujas y manchas rojizas son señales. Hacemos una evaluación gratuita para determinar la extensión y el tratamiento."),
            ("¿Tratan el óxido antes de pintar?","Siempre. Lijamos, neutralizamos y sellamos la zona oxidada antes de pintar, para que no vuelva a aparecer."),
        ],
    },
    "mantenimiento": {
        "name":"mantenimiento automotriz","hub":"../servicios/mantenimiento-automotriz-cartagena.html",
        "price":"la revisión bimensual es gratuita; con planes semestrales para un cuidado integral",
        "dura":"continuo con plan preventivo",
        "links":[("Mantenimiento Automotriz","../servicios/mantenimiento-automotriz-cartagena.html"),
                 ("Mantenimiento de anticorrosiva","../servicios/mantenimiento-anticorrosiva.html"),
                 ("Mantenimiento semestral","../servicios/mantenimiento-semestral-vehiculo.html")],
        "secs":[
            ("Por qué el mantenimiento preventivo","En el ambiente salino de Cartagena, el mantenimiento periódico es lo que conserva tu auto impecable durante años. Cuesta una fracción de lo que costaría reparar el daño acumulado."),
            ("Qué incluye","Lavado técnico, revisión del estado de la pintura y las protecciones, renovación de la capa hidrofóbica y verificación de zonas anticorrosivas. Adaptamos el plan a tu vehículo."),
            ("Planes disponibles","La revisión bimensual de mantenimiento es gratuita. Para un cuidado integral ofrecemos planes semestrales que incluyen lavado técnico y renovación de protecciones. Te recomendamos la frecuencia según el uso de tu auto."),
        ],
        "faq":[
            ("¿Cada cuánto se hace el mantenimiento?","La revisión bimensual es gratuita. Para un cuidado más completo ofrecemos planes semestrales que incluyen lavado técnico y renovación de protecciones."),
            ("¿Vale la pena el plan preventivo?","Sí. Cuesta mucho menos que reparar el daño por salitre y sol, y mantiene tu auto siempre presentable."),
            ("¿Sirve sin ceramic ni anticorrosiva?","Sí. Evaluamos tu vehículo y te recomendamos qué protecciones conviene aplicar y cómo mantenerlas."),
        ],
    },
}
DEFAULT = FACTS["detailing"]

def detect(slug, title):
    s = (slug+" "+title).lower()
    if "ceramic" in s: return "ceramic"
    if "ppf" in s: return "ppf"
    if "wrap" in s: return "wrap"
    if "polariz" in s: return "polarizado"
    if "anticorros" in s or "oxidacion" in s or "oxida" in s or "salitre" in s: return "anticorrosiva"
    if "mantenimiento" in s: return "mantenimiento"
    if "pintura" in s or "latoneria" in s or "rayones" in s: return "pintura"
    if "detailing" in s or "lavado" in s or "pulida" in s: return "detailing"
    return "detailing"

# Titulos corregidos (gramaticales y con sentido) para posts auto-generados
TITLE_FIX = {
    "proteccion-pintura-clima-salitre": "¿Qué Protección de Pintura Elegir para el Clima Salitre de Cartagena?",
    "ceramic-coating-transparente-invisible": "Ceramic Coating Transparente vs Invisible: ¿Cuáles Son las Diferencias?",
    "detailing-interior-vs-exterior": "Detailing Interior vs Exterior: ¿Cuál Priorizar?",
    "detailing-vs-lavado-profesional": "Detailing vs Lavado Profesional: Diferencias y Resultados",
    "kia-picanto-protecciones-costo": "Kia Picanto: ¿Protecciones Básicas o Premium? Cuál Elegir",
    "mantenimiento-anticorrosiva-necesidad": "¿Es Necesario el Mantenimiento Bimensual de la Protección Anticorrosiva?",
    "mantenimiento-preventivo-mensual": "Plan de Mantenimiento Preventivo del Vehículo en Cartagena",
    "oxidacion-marina-prevencion": "Oxidación Marina en Cartagena: Cómo Identificarla y Prevenirla",
    "ppf-cobertura-estrategia": "PPF: Cobertura Frontal vs Completa, Análisis de Costo-Beneficio",
    "ppf-vs-ceramic-coating-comparativa": "PPF vs Ceramic Coating 2026: ¿Cuál es Más Barato en Cartagena?",
    "ppf-garantia-fabricante-afecta": "¿El PPF Afecta la Garantía de Fábrica de tu Auto?",
    "paquete-completo-ahorro": "Paquete Completo de Servicios: Precio Total vs Individual",
    "polarizado-legal-colombia": "Polarizado Legal en Colombia: Cómo Cumplir el 70% VLT",
    "oxidacion-reparacion-costos-desglose": "Oxidación Leve, Moderada o Severa: Precios de Reparación en Cartagena",
    "oxidacion-reparacion-previa": "¿Es Necesaria la Reparación de Óxido Antes de la Anticorrosiva?",
    "toyota-hilux-servicios-precios": "Toyota Hilux: Servicios Recomendados y Precios en Cartagena",
    "auto-nuevo-vs-usado-proteccion": "Vehículo Nuevo vs Usado: ¿Cuál Necesita Más Protección?",
    "wrap-vinilico-reversible-retiro": "Wrap Vinílico Reversible: Cómo Retirarlo Sin Dañar la Pintura",
    "ceramic-coating-nuevo-vs-restauracion": "Ceramic Coating: ¿Auto Nuevo o con Restauración Previa?",
    "precio-anticorrosiva-toyota-fortuner": "Anticorrosiva Transparente vs Convencional para Toyota Fortuner: Precios",
    "mazda-cx5-vs-toyota-rav4-proteccion": "Mazda CX-5 vs Toyota RAV4: ¿Cuál Necesita Más Protección?",
    "ceramic-coating-cuanto-dura-cartagena": "¿Cuánto Dura el Ceramic Coating en Cartagena?",
    "wrap-cuanto-tarda-instalacion": "¿Cuánto Tarda la Instalación del Wrap Vinílico?",
    "anticorrosiva-mazda-cx5-precio": "Precio de Protección Anticorrosiva para Mazda CX-5 en Cartagena",
    "anticorrosiva-para-moto-cartagena": "Protección Anticorrosiva para Motos en Cartagena",
    "precio-ceramic-coating-por-tamano": "Precio del Ceramic Coating según el Tamaño del Auto",
    "ppf-merece-la-pena-carro-viejo": "PPF en un Carro Viejo: ¿Merece la Pena?",
    "salitre-como-destruye-pintura": "Cómo el Salitre Destruye la Pintura de tu Auto",
    "auto-antes-de-vender-proteger": "Antes de Vender tu Auto: Protecciones que Suben el Precio",
    "toyota-prado-servicios-completos": "Toyota Prado: Servicios Completos y Precios en Cartagena",
    "oxidacion-debajo-auto-prevenir": "Oxidación Debajo del Auto: Cómo Prevenirla",
    "polarizado-carros-electricos-cartagena": "Polarizado para Carros Eléctricos en Cartagena",
    "precios-detailing-colombia-2026": "Precios de Detailing en Colombia 2026",
    "mantenimiento-ceramic-cada-cuanto": "Mantenimiento del Ceramic Coating: ¿Cada Cuánto?",
    "guia-completa-proteccion-kia-sportage": "Guía Completa de Protección para Kia Sportage en Cartagena",
    "precio-completo-todos-servicios-auto": "Precio Completo: Todos los Servicios para tu Auto",
    "detailing-post-temporada-lluvias": "Detailing Después de la Temporada de Lluvias en Cartagena",
    "como-mantener-pintura-cartagena": "Cómo Mantener la Pintura Perfecta en Cartagena",
    "costo-reparacion-oxidacion-severa": "Cuánto Cuesta Reparar un Auto con Oxidación Severa en Cartagena",
    "servicio-mantenimiento-bimensual": "Servicio de Mantenimiento Bimensual Gratuito en Cartagena",
}

# Descripciones corregidas (datos del negocio)
DESC_FIX = {
    "servicio-mantenimiento-bimensual": "La revisión bimensual de mantenimiento de la protección anticorrosiva es gratuita: revisamos y reforzamos las zonas que lo necesiten para conservar tu vehículo en el clima costero de Cartagena.",
    "mantenimiento-anticorrosiva-necesidad": "¿Vale la pena el mantenimiento bimensual de la protección anticorrosiva? Es gratuito y conserva la protección; te explicamos por qué conviene aprovecharlo.",
    "precio-anticorrosiva-toyota-fortuner": "Diferencias de precio entre la anticorrosiva transparente y convencional para Toyota Fortuner, qué incluye cada una y cuándo conviene cada opción en Cartagena.",
}

def main():
    count = 0
    for path in sorted(glob.glob(os.path.join(BLOG,"*.html"))):
        raw = open(path, encoding="utf-8", errors="ignore").read()
        # reprocesar tanto los delgados como los ya enriquecidos por este script
        if "Información Detallada" not in raw and 'class="container post-content"' not in raw:
            continue
        fn = os.path.basename(path); slug = fn[:-5]
        mt = re.search(r"<title>(.*?)</title>", raw, re.S)
        title_full = (mt.group(1).strip() if mt else slug)
        title = re.sub(r"\s*\|\s*Blog Detailing Experts.*$","",title_full).strip()
        title = re.sub(r"\s*\|\s*Detailing Experts.*$","",title).strip()
        title = re.sub(r"\s+", " ", title)
        # aplicar titulo corregido si existe
        if slug in TITLE_FIX:
            title = TITLE_FIX[slug]
        md = re.search(r'name="description"\s+content="(.*?)"', raw, re.S)
        desc = md.group(1).strip() if md else title
        if slug in DESC_FIX:
            desc = DESC_FIX[slug]
        mi = re.search(r'(https://images\.unsplash\.com/[^"?]+)', raw)
        img_id = mi.group(1).split("/")[-1] if mi else "photo-1607860108855-64acf2078ed9"
        key = detect(slug, title)
        write_post(fn, slug, title, desc, img_id, FACTS.get(key, DEFAULT))
        count += 1
    print(f"Blog posts reprocesados: {count}")

def write_post(fn, slug, title, desc, img_id, f):
    canon = f"https://detailingexperts.com/blog/{slug}.html"
    img12 = f"https://images.unsplash.com/{img_id}?auto=format&fit=crop&w=1200&q=80"
    img14 = f"https://images.unsplash.com/{img_id}?auto=format&fit=crop&w=1400&q=80"

    secs_html = ""
    for h,p in f["secs"]:
        secs_html += f"<h2>{esc(h)}</h2>\n<p>{esc(p)}</p>\n"
    # intro lead
    lead = f"{esc(title)}. En esta guía te explicamos lo esencial sobre {f['name']} en Cartagena: qué incluye, cuánto cuesta y cómo cuidamos tu vehículo en el exigente clima costero."
    # list
    li = "".join(f"<li>{esc(x)}</li>" for x in [
        f"Precio orientativo: {f['price']}.",
        f"Duración estimada: {f['dura']}.",
        "Evaluación previa gratuita y cotización sin compromiso.",
        "Atención en toda Cartagena, frente a la Plaza de Toros (Progreso).",
    ])
    # internal links
    links = "".join(f'<li><a href="{href}" style="color:var(--clr-accent);">{esc(txt)}</a></li>' for txt,href in f["links"])
    # FAQ
    faq_vis = ""
    for q,a in f["faq"]:
        faq_vis += (f'<div class="card" style="padding:1.5rem;margin-bottom:1rem;">'
                    f'<h3 style="color:var(--clr-accent);font-size:var(--text-lg);margin-bottom:.5rem;">{esc(q)}</h3>'
                    f'<p style="max-width:none;">{esc(a)}</p></div>')
    faq_schema = {"@context":"https://schema.org","@type":"FAQPage",
                  "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in f["faq"]]}
    blogposting = {"@context":"https://schema.org","@type":"BlogPosting","headline":title,
                   "description":desc,"image":img12,
                   "author":{"@type":"Organization","name":"Detailing Experts"},
                   "publisher":{"@type":"Organization","name":"Detailing Experts","logo":{"@type":"ImageObject","url":"https://detailingexperts.com/images/Detailing%20(4).PNG"},"url":"https://detailingexperts.com"},
                   "datePublished":"2026-06-03","dateModified":"2026-06-03",
                   "mainEntityOfPage":{"@type":"WebPage","@id":canon}}
    breadcrumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Inicio","item":"https://detailingexperts.com/"},
        {"@type":"ListItem","position":2,"name":"Blog","item":"https://detailingexperts.com/blog/index.html"},
        {"@type":"ListItem","position":3,"name":title,"item":canon}]}

    out = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} | Blog Detailing Experts</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="article">
<meta property="og:url" content="{canon}">
<meta property="og:title" content="{esc(title)} | Detailing Experts">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="https://detailingexperts.com/images/og-default.png">
<meta property="og:locale" content="es_CO">
<meta property="article:published_time" content="2026-06-03">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="https://detailingexperts.com/images/og-default.png">
<link rel="preconnect" href="https://images.unsplash.com">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,700;0,800;0,900;1,700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/style.min.css">
<script type="application/ld+json">{json.dumps(blogposting, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(breadcrumb, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>
</head>
<body>
<div id="nav-placeholder"></div>

<header class="page-hero page-hero--sm">
  <div class="page-hero__bg">
    <img src="{img14}" alt="{esc(title)}" loading="eager" fetchpriority="high" width="1400" height="933">
  </div>
  <div class="page-hero__overlay" aria-hidden="true"></div>
  <div class="page-hero__content">
    <span class="section-label">Blog · Detailing Experts</span>
    <h1 class="hero__title" style="max-width:840px;">{esc(title)}</h1>
    <p class="hero__desc" style="max-width:680px;">{esc(desc)}</p>
  </div>
</header>

<article class="section">
  <div class="container post-content">
    <p class="lead" style="color:var(--clr-text-1);font-weight:500;margin-bottom:2rem;">{lead}</p>

    {secs_html}

    <div style="background:rgba(0,204,255,0.07);border-left:4px solid var(--clr-accent);padding:1.25rem 1.5rem;border-radius:0 var(--radius-md) var(--radius-md) 0;margin:2rem 0;">
      <strong style="color:var(--clr-accent);">En resumen:</strong>
      <ul style="margin-top:.5rem;">{li}</ul>
    </div>

    <h2>Preguntas frecuentes</h2>
    {faq_vis}

    <h2>Servicios relacionados</h2>
    <ul>{links}</ul>
  </div>
</article>

<section class="cta-section">
  <div class="container" style="position:relative;z-index:1;text-align:center;">
    <span class="cta-section__eyebrow">Detailing Experts · Cartagena</span>
    <h2 class="cta-section__title" style="color:var(--clr-white);">¿Listo para proteger tu vehículo?</h2>
    <p class="cta-section__desc">Escríbenos por WhatsApp con los datos de tu auto y te damos una cotización sin compromiso.</p>
    <div class="cta-section__actions">
      <a href="https://wa.me/573016501515?text=Hola%2C%20le%C3%AD%20el%20blog%20y%20quiero%20cotizar" class="btn btn-whatsapp btn-lg" target="_blank" rel="noopener noreferrer"><img src="../images/whatsapp-logo.png" alt="" aria-hidden="true" class="btn__icon" width="20" height="20">Cotizar por WhatsApp</a>
      <a href="{f['hub']}" class="btn btn-outline-white btn-lg">Ver el servicio</a>
    </div>
  </div>
</section>

<div id="footer-placeholder"></div>
<script>window.basePath = "../";</script>
<script src="../js/components.js" defer></script>
<script src="../js/main.js" defer></script>
</body>
</html>'''
    with open(os.path.join(BLOG, fn), "w", encoding="utf-8") as fo:
        fo.write(out)

if __name__ == "__main__":
    main()
