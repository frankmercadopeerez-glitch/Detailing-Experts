# -*- coding: utf-8 -*-
"""Regenera las paginas delgadas de servicios con contenido rico y completo."""
import os, re, html, hashlib, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERV = os.path.join(ROOT, "servicios")

# ---- Metadatos por servicio --------------------------------------------------
SERVICES = {
    "anticorrosiva": {
        "name": "Protección Anticorrosiva",
        "hub": "proteccion-anticorrosiva.html",
        "stype": "Protección anticorrosiva automotriz",
        "img": "photo-1597007030739-6d2e7172ee5a",
        "label": "Anticorrosiva",
        "intro": "La protección anticorrosiva aplica un recubrimiento especializado sobre la carrocería, los bajos y las zonas ocultas del vehículo para frenar el avance del óxido. En Cartagena, donde el salitre del mar y la humedad atacan el metal todo el año, es la inversión que más prolonga la vida útil de tu auto.",
        "intro2": "Antes de aplicar cualquier producto inspeccionamos el vehículo en busca de oxidación existente. Si encontramos puntos afectados los tratamos primero; y cuando hay zonas podridas o perforadas por el óxido, se reemplazan con soldadura antes de proteger. Solo entonces aplicamos la capa protectora, garantizando que el problema no siga creciendo por debajo.",
        "benefits": [
            ("Frena el óxido", "Detiene la corrosión activa y previene su aparición en chasis, bajos y cavidades internas."),
            ("Resiste el salitre", "Formulada para el ambiente marino de Cartagena, soporta humedad y sal constantes."),
            ("Mantenimiento gratis", "Incluye revisión y mantenimiento bimensual sin costo para conservar la protección."),
        ],
        "faq": [
            ("¿Cuánto cuesta la protección anticorrosiva?", "El precio depende del tamaño del vehículo y de su estado. Un auto compacto en buen estado parte desde 1.2M y un SUV o camioneta desde 1.5M. El costo sube cuando hay zonas podridas por el óxido que deben reemplazarse con soldadura: lo evaluamos y cotizamos sin compromiso."),
            ("¿Qué pasa si mi auto ya tiene partes oxidadas?", "Lo evaluamos primero. El óxido superficial se lija y neutraliza; pero cuando hay zonas podridas o perforadas, esas partes se reemplazan con soldadura antes de aplicar la protección. Ese trabajo adicional aumenta el costo según la extensión del daño."),
            ("¿Cuánto dura la protección anticorrosiva?", "La protección dura alrededor de 1 año, momento en que se recomienda repintar para renovarla. Para conservarla en óptimas condiciones incluimos un mantenimiento bimensual totalmente gratuito."),
            ("¿La protección es visible?", "Ofrecemos versión transparente (deja ver el metal o la pintura) y convencional (acabado tipo cera bajo el chasis). Te asesoramos según la zona y el resultado que buscas."),
            ("¿El mantenimiento tiene costo?", "No. El mantenimiento bimensual de la protección anticorrosiva es gratuito: revisamos el estado y reforzamos las zonas que lo necesiten sin cobrarte."),
        ],
    },
    "ceramic": {
        "name": "Ceramic Coating",
        "hub": "ceramic-coating-cartagena.html",
        "stype": "Recubrimiento cerámico automotriz",
        "img": "photo-1607860108855-64acf2078ed9",
        "label": "Ceramic Coating",
        "intro": "El ceramic coating es un recubrimiento líquido a base de dióxido de silicio (SiO₂) que se adhiere a la pintura creando una capa dura, hidrofóbica y brillante. Repele el agua, el polvo y el salitre, y hace que lavar el auto sea mucho más fácil.",
        "intro2": "En el clima costero de Cartagena, donde el sol y la sal degradan la pintura rápidamente, el ceramic coating actúa como un escudo invisible que mantiene el color vivo y el brillo intacto durante años. Antes de aplicarlo descontaminamos y corregimos la superficie para que el resultado sea impecable.",
        "benefits": [
            ("Brillo espejo duradero", "Realza el color y la profundidad de la pintura con un acabado que dura años, no semanas."),
            ("Efecto hidrofóbico", "El agua y el salitre resbalan sin adherirse, reduciendo manchas y facilitando el lavado."),
            ("Protección UV", "Bloquea la radiación solar que decolora y oxida la pintura bajo el sol de Cartagena."),
        ],
        "faq": [
            ("¿Cuánto cuesta el ceramic coating?", "Depende del tamaño del vehículo y del estado de la pintura. Autos compactos parten desde 800K, sedanes desde 1.2M y SUVs desde 1.5M. Si la pintura necesita corrección previa, lo incluimos en la cotización."),
            ("¿Cuánto dura el ceramic coating?", "Entre 2 y 5 años según el producto aplicado y el mantenimiento. Con lavados adecuados y una revisión periódica conserva sus propiedades por mucho más tiempo que una cera tradicional."),
            ("¿Es mejor que la cera o el sellador?", "Sí. La cera dura semanas; el ceramic coating dura años, ofrece mayor dureza (hasta 9H), mejor repelencia al agua y protección UV muy superior."),
            ("¿Necesita mantenimiento?", "Solo lavados regulares con productos de pH neutro. Ofrecemos un mantenimiento profesional opcional para renovar la capa hidrofóbica y maximizar la duración."),
            ("¿Elimina los rayones?", "El ceramic coating protege, pero no rellena rayones profundos. Si tu pintura tiene micro-rayones, hacemos una corrección previa para que el acabado quede perfecto."),
        ],
    },
    "ppf": {
        "name": "Paint Protection Film (PPF)",
        "hub": "ppf.html",
        "stype": "Instalación de Paint Protection Film",
        "img": "photo-1552519507-da3b142c6e3d",
        "label": "PPF",
        "intro": "El PPF (Paint Protection Film) es una película de uretano transparente que se instala sobre la pintura para protegerla físicamente de piedras, rayones, impactos y contaminantes. Es la barrera más resistente del mercado y muchas de sus referencias son autorreparables con el calor.",
        "intro2": "En carreteras y zonas costeras como Cartagena, el PPF evita los típicos picotazos de piedra en el capó y el desgaste por salitre, manteniendo la pintura original intacta. Al ser transparente, conserva el aspecto de fábrica del vehículo mientras lo protege por completo.",
        "benefits": [
            ("Resistencia a impactos", "Absorbe el golpe de piedras y gravilla que de otro modo astillarían la pintura."),
            ("Autorreparable", "Las referencias premium sellan micro-rayones con el calor del sol o agua caliente."),
            ("Invisible", "Película transparente que protege sin alterar el color ni el brillo original."),
        ],
        "faq": [
            ("¿Cuánto cuesta el PPF?", "Según la cobertura: un kit frontal (capó, paragolpes y espejos) parte desde 2M, y la cobertura completa del vehículo desde 4M. Cotizamos a medida según el modelo y las zonas que quieras proteger."),
            ("¿El PPF se nota una vez instalado?", "No. Es una película transparente de alta claridad. Una vez instalada y curada es prácticamente invisible y mantiene el acabado de fábrica."),
            ("¿De verdad se autorrepara?", "Las referencias premium sí: los micro-rayones superficiales desaparecen con el calor. Los cortes profundos no, pero la película evita que lleguen a la pintura."),
            ("¿Cuánto dura el PPF?", "Entre 5 y 10 años según la calidad de la película y el mantenimiento. Ofrecemos garantía sobre la instalación."),
            ("¿Puedo combinar PPF con ceramic coating?", "Sí, es la combinación ideal: el PPF protege del impacto físico y el ceramic coating sobre la película aporta hidrofobicidad y brillo. Te armamos un paquete con ambos."),
        ],
    },
    "wrap": {
        "name": "Wrap Vinílico",
        "hub": "wrap.html",
        "stype": "Instalación de wrap vinílico",
        "img": "photo-1583267746897-2cf415887172",
        "label": "Wrap",
        "intro": "El wrap vinílico envuelve la carrocería con láminas de vinilo de alta calidad para cambiar el color o el acabado del vehículo sin pintarlo. Disponible en cientos de colores y texturas —mate, brillante, satinado, carbono, cromo— y es totalmente reversible.",
        "intro2": "Además de transformar la estética, el vinilo protege la pintura original de rayones y del sol, conservando su valor. Cuando decides retirarlo, la pintura de fábrica queda intacta. Es la forma más versátil y segura de personalizar tu auto en Cartagena.",
        "benefits": [
            ("Cientos de colores", "Mate, brillante, satinado, carbono, cromo y más. Personalización total a tu gusto."),
            ("100% reversible", "Se retira sin dañar la pintura original, conservando el valor de reventa."),
            ("Protege la pintura", "El vinilo actúa como capa sacrificable frente a rayones, sol y salitre."),
        ],
        "faq": [
            ("¿Cuánto cuesta el wrap vinílico?", "Un wrap parcial (capó, techo o detalles) parte desde 1.2M y un cambio de color completo desde 3M, según el tamaño del vehículo y el tipo de vinilo elegido."),
            ("¿El wrap daña la pintura?", "No. Al contrario, la protege. Cuando se retira correctamente la pintura original queda intacta, siempre que esté en buen estado al momento de instalar."),
            ("¿Cuánto dura el vinilo?", "Entre 5 y 7 años con buen mantenimiento. Los vinilos premium soportan bien el sol y el salitre de Cartagena."),
            ("¿Cuánto tarda la instalación?", "Un wrap parcial toma de 4 a 6 horas; un cambio de color completo, de 2 a 3 días según la complejidad del vehículo."),
            ("¿Puedo lavar el auto normalmente?", "Sí, con lavado a mano y productos suaves. Evita hidrolavadoras a alta presión muy cerca de los bordes del vinilo."),
        ],
    },
    "polarizado": {
        "name": "Polarizado Automotriz",
        "hub": "polarizados.html",
        "stype": "Tintado de vidrios automotriz",
        "img": "photo-1568605117036-5fe5e7bab0b7",
        "label": "Polarizado",
        "intro": "El polarizado automotriz consiste en instalar láminas de control solar en los vidrios para bloquear la radiación UV, reducir el calor interior y aportar privacidad. Una buena lámina marca la diferencia entre un interior fresco y uno sofocante bajo el sol de Cartagena.",
        "intro2": "Nuestras láminas rechazan hasta el 99% de los rayos UV y reducen notablemente el calor, protegiendo la tapicería y a los ocupantes. Instalamos sin burbujas y respetando la normativa colombiana de visibilidad (70% VLT en el parabrisas y vidrios delanteros).",
        "benefits": [
            ("Bloquea 99% UV", "Protege tu piel y evita que la tapicería se decolore y se reseque con el sol."),
            ("Interior más fresco", "Reduce el calor que entra al habitáculo, bajando la temperatura varios grados."),
            ("Privacidad y seguridad", "Dificulta la visión desde el exterior y ayuda a contener los vidrios ante un impacto."),
        ],
        "faq": [
            ("¿Cuánto cuesta el polarizado?", "Depende del número de vidrios y del tipo de lámina. Un auto compacto parte desde 500K y un SUV con más superficie desde 800K. Las láminas de mayor rechazo de calor tienen un valor superior."),
            ("¿El polarizado es legal en Colombia?", "Sí, siempre que respete la visibilidad mínima: 70% VLT en parabrisas y vidrios delanteros. Instalamos cumpliendo la norma para evitarte multas."),
            ("¿Cuánto dura la lámina?", "Las láminas de calidad duran muchos años sin despegarse ni tornarse moradas. Ofrecemos garantía sobre el material y la instalación."),
            ("¿Queda con burbujas?", "No. Trabajamos en ambiente controlado y con técnica profesional para un acabado uniforme, sin burbujas ni pliegues."),
            ("¿Cuánto tiempo toma?", "La instalación completa toma de 2 a 4 horas según el vehículo. Lo entregas en la mañana y lo recoges el mismo día."),
        ],
    },
    "detailing": {
        "name": "Detailing Premium",
        "hub": "detailing-premium.html",
        "stype": "Detailing automotriz premium",
        "img": "photo-1607860108855-64acf2078ed9",
        "label": "Detailing",
        "intro": "El detailing es la limpieza y restauración profunda del vehículo, por dentro y por fuera, a un nivel que ningún autolavado alcanza. Incluye descontaminación, corrección de pintura, limpieza detallada del interior y un sellado protector final.",
        "intro2": "Más que dejar el auto limpio, el detailing devuelve el brillo y la sensación de vehículo nuevo. En Cartagena, donde el polvo, el salitre y la humedad ensucian rápido, un detailing periódico mantiene tu inversión impecable y protegida.",
        "benefits": [
            ("Corrección de pintura", "Eliminamos micro-rayones y marcas de swirl para recuperar un brillo profundo y uniforme."),
            ("Interior impecable", "Limpieza y desinfección de tapicería, plásticos y vidrios, eliminando olores y bacterias."),
            ("Sellado protector", "Aplicamos una capa de protección que conserva el resultado por más tiempo."),
        ],
        "faq": [
            ("¿Cuánto cuesta el detailing?", "Un detailing básico parte desde 500K, e incluye lavado profundo, aspirado y brillo. El detailing premium con corrección de pintura y sellado parte desde 1.5M, según el tamaño y el estado del vehículo."),
            ("¿En qué se diferencia de un autolavado?", "Un autolavado limpia la superficie; el detailing descontamina, corrige la pintura, detalla cada rincón del interior y aplica protección. El resultado y la duración no se comparan."),
            ("¿Cada cuánto debo hacer detailing?", "Para mantener el auto impecable recomendamos un detailing completo cada 4 a 6 meses, con lavados de mantenimiento entre cada uno."),
            ("¿Incluye limpieza de motor?", "Podemos incluir la limpieza y el tratamiento anticorrosivo del compartimento del motor como servicio adicional desde 350K."),
            ("¿Cuánto tiempo toma?", "Un detailing completo toma entre 4 y 8 horas según el estado del vehículo. En algunos casos se entrega al día siguiente."),
        ],
    },
    "pintura": {
        "name": "Latonería y Pintura",
        "hub": "latoneria-pintura.html",
        "stype": "Latonería y pintura automotriz",
        "img": "photo-1597007030739-6d2e7172ee5a",
        "label": "Latonería y Pintura",
        "intro": "El servicio de latonería y pintura repara golpes, abolladuras, rayones profundos y zonas oxidadas, devolviendo a la carrocería su forma y su acabado original. Trabajamos con igualación de color computarizada para que la reparación sea imperceptible.",
        "intro2": "Cuando el daño llega al metal, actuar a tiempo evita que el óxido se extienda. Reparamos, tratamos la zona contra la corrosión y repintamos con acabado de fábrica. En Cartagena, además, sellamos contra el salitre para que el problema no reaparezca.",
        "benefits": [
            ("Igualación de color", "Sistema computarizado que replica el color exacto de tu vehículo para una reparación invisible."),
            ("Tratamiento anti-óxido", "Neutralizamos y sellamos la zona afectada antes de pintar para frenar la corrosión."),
            ("Acabado de fábrica", "Recuperamos la superficie original con brillo y textura uniformes."),
        ],
        "faq": [
            ("¿Cuánto cuesta reparar un golpe o rayón?", "Depende de la extensión y la profundidad del daño. Un rayón superficial parte desde 200K; una reparación con latonería y repintado de un panel, desde 800K. Evaluamos sin compromiso."),
            ("¿Cómo sé si mi auto tiene óxido bajo la pintura?", "Burbujas, manchas marrones o rojizas y zonas que se levantan son señales. Hacemos una evaluación gratuita para determinar la extensión y el tratamiento."),
            ("¿La reparación se nota?", "No. Con la igualación de color computarizada y el acabado profesional, la zona reparada queda idéntica al resto de la carrocería."),
            ("¿Tratan el óxido antes de pintar?", "Siempre. Lijamos, neutralizamos y sellamos la zona oxidada antes de aplicar la pintura, para que el problema no vuelva a aparecer."),
            ("¿Cuánto tarda la reparación?", "Según el alcance, de 1 a 4 días. Te damos un tiempo estimado al momento de cotizar."),
        ],
    },
    "mantenimiento": {
        "name": "Mantenimiento Automotriz",
        "hub": "mantenimiento-automotriz-cartagena.html",
        "stype": "Mantenimiento y protección automotriz",
        "img": "photo-1597007030739-6d2e7172ee5a",
        "label": "Mantenimiento",
        "intro": "El mantenimiento preventivo conserva las protecciones de tu vehículo en óptimas condiciones a lo largo del tiempo. Revisamos el estado de la pintura, el recubrimiento cerámico, las zonas tratadas contra el óxido y renovamos lo que haga falta.",
        "intro2": "En el ambiente salino de Cartagena, el mantenimiento periódico es lo que marca la diferencia entre un auto que se conserva impecable durante años y uno que se deteriora. Un plan preventivo cuesta una fracción de lo que costaría reparar el daño acumulado.",
        "benefits": [
            ("Prolonga las protecciones", "Renueva la capa hidrofóbica y anticorrosiva para que sigan trabajando al 100%."),
            ("Previene daños costosos", "Detecta a tiempo óxido, manchas o desgaste antes de que se conviertan en reparaciones mayores."),
            ("Conserva el valor", "Un vehículo bien mantenido conserva su aspecto y su precio de reventa."),
        ],
        "faq": [
            ("¿Qué incluye el mantenimiento?", "Lavado técnico, revisión del estado de la pintura y las protecciones, renovación de la capa hidrofóbica y verificación de zonas anticorrosivas. Adaptamos el plan a tu vehículo."),
            ("¿Cada cuánto se hace?", "La revisión bimensual de mantenimiento de la protección anticorrosiva es gratuita. Para un cuidado integral ofrecemos planes semestrales que incluyen lavado técnico y renovación de las protecciones."),
            ("¿Vale la pena el plan preventivo?", "Sí. Cuesta mucho menos que reparar el daño acumulado por salitre y sol, y mantiene tu auto siempre presentable."),
            ("¿Sirve si no tengo ceramic ni anticorrosiva?", "Sí. Hacemos una evaluación inicial y te recomendamos qué protecciones conviene aplicar y cómo mantenerlas."),
            ("¿Cuánto tiempo toma cada visita?", "Una visita de mantenimiento estándar toma de 1 a 2 horas."),
        ],
    },
    "pdr": {
        "name": "PDR – Reparación sin Pintura",
        "hub": "pdr.html",
        "stype": "Reparación de abolladuras sin pintura (PDR)",
        "img": "photo-1597007030739-6d2e7172ee5a",
        "label": "PDR",
        "intro": "El PDR (Paintless Dent Repair) repara abolladuras sin necesidad de repintar, masajeando el metal desde el interior del panel hasta devolverle su forma original. Es más rápido, más económico y conserva la pintura de fábrica.",
        "intro2": "Es ideal para golpes de granizo, abolladuras de parqueadero y bollos sin pintura dañada. Al no repintar, no hay diferencias de color ni riesgo de afectar el valor del vehículo. Evaluamos si tu abolladura es candidata a PDR sin compromiso.",
        "benefits": [
            ("Conserva la pintura original", "Sin repintar: el color y el acabado de fábrica permanecen intactos."),
            ("Más rápido y económico", "Muchas abolladuras se resuelven el mismo día a una fracción del costo de latonería."),
            ("Sin masilla", "Se devuelve la forma al metal sin rellenos, manteniendo la integridad del panel."),
        ],
        "faq": [
            ("¿Cuánto cuesta el PDR?", "Depende del tamaño, la profundidad y la ubicación de la abolladura. Las abolladuras pequeñas parten desde 150K. Evaluamos cada caso y cotizamos sin compromiso."),
            ("¿Cualquier abolladura se puede reparar con PDR?", "No todas. Funciona cuando la pintura está intacta y el metal no está demasiado estirado. Si la pintura está dañada, recomendamos latonería y pintura."),
            ("¿Queda algún rastro?", "Bien ejecutado, el PDR devuelve la forma original sin rastro visible y sin afectar la pintura."),
            ("¿Sirve para daños de granizo?", "Sí, es el método ideal para múltiples abolladuras de granizo, conservando la pintura de fábrica."),
            ("¿Cuánto tarda?", "Muchas reparaciones se completan el mismo día, según la cantidad y complejidad de las abolladuras."),
        ],
    },
}

DEFAULT_SERVICE = {
    "name": "Protección Automotriz",
    "hub": "index.html",
    "stype": "Servicio de protección automotriz",
    "img": "photo-1503376780353-7e6692767b70",
    "label": "Servicios",
    "intro": "En Detailing Experts protegemos y embellecemos tu vehículo con servicios premium pensados para el exigente clima costero de Cartagena. Cada tratamiento se realiza con productos profesionales y mano de obra especializada.",
    "intro2": "El salitre, el sol y la humedad de Cartagena deterioran los vehículos más rápido que en cualquier otra ciudad. Por eso aplicamos soluciones diseñadas específicamente para este ambiente, con garantía y asesoría personalizada.",
    "benefits": [
        ("Calidad profesional", "Productos premium y técnicos especializados para un resultado garantizado."),
        ("Pensado para Cartagena", "Soluciones formuladas para resistir el salitre y el sol intenso de la costa."),
        ("Asesoría personalizada", "Te recomendamos exactamente lo que tu vehículo necesita, sin venderte de más."),
    ],
    "faq": [
        ("¿Cuánto cuesta el servicio?", "El precio varía según el vehículo y el estado en que se encuentra. Hacemos una evaluación gratuita y te entregamos una cotización personalizada sin compromiso."),
        ("¿Atienden mi modelo de vehículo?", "Sí, trabajamos con todo tipo de vehículos: autos, SUVs, camionetas y más. Adaptamos cada servicio al modelo específico."),
        ("¿Ofrecen garantía?", "Sí, todos nuestros servicios de protección incluyen garantía. Te explicamos las condiciones al momento de cotizar."),
        ("¿Cuánto tiempo toma?", "Depende del servicio. Muchos se entregan el mismo día; los más complejos pueden tomar 24-48 horas."),
        ("¿Dónde están ubicados?", "En la Cl. 31 #52-32, Progreso, frente a la Plaza de Toros, Cartagena de Indias. Atendemos toda la ciudad."),
    ],
}

# SVG icons (stroke, currentColor)
ICONS = [
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v5c0 4.5-3 7.8-7 9-4-1.2-7-4.5-7-9V6l7-3z"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3s6 5.5 6 10a6 6 0 0 1-12 0c0-4.5 6-10 6-10z"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M5 19l2-2M17 7l2-2"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l2.4 6.9H22l-6 4.3 2.3 7L12 16.9 5.7 20.2 8 13.2l-6-4.3h7.6z"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>',
]

WA = "https://wa.me/573016501515"

def detect_service(slug, title):
    s = slug.lower()
    # order matters
    if "ceramic" in s: return "ceramic"
    if "ppf" in s: return "ppf"
    if "wrap" in s: return "wrap"
    if "polarizad" in s: return "polarizado"
    if "anticorros" in s: return "anticorrosiva"
    if "pdr" in s: return "pdr"
    if "detailing" in s: return "detailing"
    if "mantenimiento" in s: return "mantenimiento"
    if any(k in s for k in ["pintura","oxida","oxidacion","latoneria","rayones","manchas","golpe","desgastada","abolladura"]): return "pintura"
    # title fallback
    t = title.lower()
    for k in ["ceramic","ppf","wrap","polariz","anticorros","detailing","pdr","mantenimiento","pintura"]:
        if k in t:
            return detect_service(k, "")
    return None

STOPWORDS = {"en","de","la","el","los","las","para","y","con","tu","cartagena",
             "automotriz","automotrices","premium","profesional","vehiculo","vehículo",
             "auto","carro","protección","proteccion"}

def extract_subject(title, service_name):
    """Saca la parte distintiva del titulo (modelo/barrio/situacion)."""
    t = title
    # quitar el nombre del servicio
    for w in service_name.split():
        t = re.sub(r"(?i)\b"+re.escape(w)+r"\b", " ", t)
    t = re.sub(r"(?i)\bcartagena\b", " ", t)
    t = re.sub(r"\s+", " ", t).strip(" -–·,")
    # limpiar palabras vacias al inicio
    words = [w for w in t.split() if w.lower() not in {"en","de","para","la","el","los","las","y","con"}]
    subj = " ".join(words).strip()
    return subj

def esc(s):
    return html.escape(s, quote=True)

def jsonesc(s):
    return s.replace("\\","\\\\").replace('"','\\"')

def build_related(slug, service_key, all_by_service):
    """Devuelve hasta 4 enlaces internos relacionados (mismo servicio) + hub."""
    sibs = [p for p in all_by_service.get(service_key, []) if p["slug"] != slug]
    # deterministic pick
    h = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    picks = []
    if sibs:
        for i in range(min(3, len(sibs))):
            picks.append(sibs[(h + i*7) % len(sibs)])
    # dedupe
    seen, out = set(), []
    for p in picks:
        if p["slug"] not in seen:
            seen.add(p["slug"]); out.append(p)
    return out

def load_overrides():
    """slug -> (title, desc) para paginas con titulo corrupto."""
    ov = {}
    op = os.path.join(os.path.dirname(os.path.abspath(__file__)), "overrides.txt")
    if os.path.exists(op):
        for line in open(op, encoding="utf-8"):
            line = line.rstrip("\n")
            if not line.strip(): continue
            parts = line.split("|")
            if len(parts) >= 3:
                ov[parts[0]] = (parts[1].strip(), parts[2].strip())
    return ov

def main():
    OVERRIDES = load_overrides()
    import urllib.parse
    # Detectar las paginas generadas por este script (firma unica) o aun delgadas
    SIG = "Solicita tu cotización sin compromiso"
    thin_list = []
    for path in sorted(glob.glob(os.path.join(SERV, "*.html"))):
        raw = open(path, encoding="utf-8", errors="ignore").read()
        if "BreadcrumbList" not in raw or SIG in raw:
            thin_list.append(os.path.basename(path))

    # Parse all thin pages
    pages = []
    for fn in thin_list:
        path = os.path.join(SERV, fn)
        if not os.path.exists(path): continue
        raw = open(path, encoding="utf-8", errors="ignore").read()
        mt = re.search(r"<title>(.*?)</title>", raw, re.S)
        title_full = mt.group(1).strip() if mt else fn
        title = re.sub(r"\s*\|\s*Detailing Experts.*$", "", title_full).strip()
        md = re.search(r'name="description"\s+content="(.*?)"', raw, re.S)
        desc = md.group(1).strip() if md else title
        mi = re.search(r'(https://images\.unsplash\.com/[^"?]+)', raw)
        img_id = None
        if mi:
            img_id = mi.group(1).split("/")[-1]
        mw = re.search(r'wa\.me/573016501515\?text=([^"]+)', raw)
        wa_text = mw.group(1) if mw else "Hola%2C%20quiero%20cotizar"
        slug = fn[:-5]
        # corregir paginas corruptas con datos correctos
        if slug in OVERRIDES:
            title, desc = OVERRIDES[slug]
            img_id = None  # usar imagen por servicio
            wa_text = urllib.parse.quote(f"Hola, quiero información sobre {title}")
        svc = detect_service(slug, title)
        pages.append({"fn":fn,"slug":slug,"title":title,"desc":desc,"img_id":img_id,"wa":wa_text,"svc":svc})

    # group by service for internal linking
    all_by_service = {}
    for p in pages:
        all_by_service.setdefault(p["svc"], []).append(p)

    for p in pages:
        meta = SERVICES.get(p["svc"], DEFAULT_SERVICE)
        write_page(p, meta, all_by_service)

    print(f"Regeneradas {len(pages)} paginas de servicios.")

def write_page(p, meta, all_by_service):
    title = p["title"]
    desc = p["desc"]
    slug = p["slug"]
    img_id = p["img_id"] or meta["img"]
    img1400 = f"https://images.unsplash.com/{img_id}?auto=format&fit=crop&w=1400&q=80"
    img1200 = f"https://images.unsplash.com/{img_id}?auto=format&fit=crop&w=1200&q=80"
    wa = p["wa"]
    canon = f"https://detailingexperts.com/servicios/{slug}.html"

    benefits = meta["benefits"]
    faq = meta["faq"]

    subject = extract_subject(title, meta["name"])
    # frase de sujeto para tejer en el cuerpo
    if subject and subject.lower() not in meta["name"].lower():
        subj_phrase = f" para {subject}"
        intro_lead = f"Esta es nuestra página de {meta['name']}{subj_phrase} en Cartagena. {meta['intro']}"
        h2_intro = f"{meta['name']}{subj_phrase}: lo que debes saber"
    else:
        subj_phrase = ""
        intro_lead = meta["intro"]
        h2_intro = f"¿Qué es {meta['name']} y por qué importa en Cartagena?"
    h2_benefits = f"Beneficios de {meta['name']}{subj_phrase}"
    h2_process = "Cómo trabajamos, paso a paso"
    h2_faq = "Preguntas frecuentes"

    # Breadcrumb + Service + FAQ schema
    breadcrumb = {
        "@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"Inicio","item":"https://detailingexperts.com/"},
            {"@type":"ListItem","position":2,"name":"Servicios","item":"https://detailingexperts.com/servicios/index.html"},
            {"@type":"ListItem","position":3,"name":esc(title),"item":canon},
        ]}
    import json
    bc_json = json.dumps(breadcrumb, ensure_ascii=False)
    service_json = json.dumps({
        "@context":"https://schema.org","@type":"Service",
        "name":title,"serviceType":meta["stype"],
        "provider":{"@type":"AutoRepair","name":"Detailing Experts","image":"https://detailingexperts.com/images/Detailing%20(4).PNG","url":"https://detailingexperts.com","telephone":"+57 301 6501515","priceRange":"$$$","address":{"@type":"PostalAddress","streetAddress":"Cl. 31 #52-32, Progreso","addressLocality":"Cartagena de Indias","addressRegion":"Bolívar","addressCountry":"CO"}},
        "areaServed":{"@type":"City","name":"Cartagena de Indias"},
        "url":canon
    }, ensure_ascii=False)
    faq_json = json.dumps({
        "@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]
    }, ensure_ascii=False)

    # benefit feature items
    feat_html = "\n".join(
        f'<div class="feature-item"><div class="feature-item__icon">{ICONS[i%len(ICONS)]}</div>'
        f'<h3 class="feature-item__title">{esc(bt)}</h3>'
        f'<p class="feature-item__desc">{esc(bd)}</p></div>'
        for i,(bt,bd) in enumerate(benefits)
    )

    # process steps (universal, service woven)
    steps = [
        ("Evaluación gratuita", f"Inspeccionamos tu vehículo y detectamos su estado real antes de recomendar el {meta['name'].lower()} adecuado."),
        ("Preparación", "Limpiamos y descontaminamos la superficie. Si hay óxido o daños previos, los tratamos primero."),
        ("Aplicación profesional", f"Ejecutamos el servicio con productos premium y técnica especializada, cuidando cada detalle."),
        ("Entrega y garantía", "Revisamos el resultado contigo, te explicamos el cuidado y respaldamos el trabajo con garantía."),
    ]
    steps_html = "\n".join(
        f'<div class="process-step"><div class="process-step__number"></div>'
        f'<h3 class="process-step__title">{esc(st)}</h3>'
        f'<p class="process-step__desc">{esc(sd)}</p></div>'
        for st,sd in steps
    )

    # FAQ visible (matches schema)
    faq_html = "\n".join(
        f'<div class="card" style="padding:1.75rem;"><h3 style="color:var(--clr-accent);font-size:var(--text-xl);margin-bottom:.6rem;">{esc(q)}</h3>'
        f'<p style="color:var(--clr-text-2);line-height:1.8;max-width:none;">{esc(a)}</p></div>'
        for q,a in faq
    )

    # related internal links
    rel = build_related(slug, p["svc"], all_by_service)
    rel_cards = ""
    for r in rel:
        rel_cards += (f'<a class="feature-item" style="text-decoration:none;display:block;" href="{r["slug"]}.html">'
                      f'<h3 class="feature-item__title" style="font-size:var(--text-lg);">{esc(r["title"])}</h3>'
                      f'<p class="feature-item__desc">{esc(r["desc"][:90])}…</p>'
                      f'<span style="color:var(--clr-accent);font-weight:600;font-size:.9rem;">Ver servicio →</span></a>')
    # always add hub + all services
    hub = meta["hub"]
    rel_cards += (f'<a class="feature-item" style="text-decoration:none;display:block;" href="{hub}">'
                  f'<h3 class="feature-item__title" style="font-size:var(--text-lg);">{esc(meta["name"])} en Cartagena</h3>'
                  f'<p class="feature-item__desc">Conoce nuestro servicio principal de {esc(meta["name"].lower())} con todos los detalles.</p>'
                  f'<span style="color:var(--clr-accent);font-weight:600;font-size:.9rem;">Ver servicio →</span></a>')

    html_out = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} | Detailing Experts</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:title" content="{esc(title)} | Detailing Experts">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="https://detailingexperts.com/images/og-default.png">
<meta property="og:locale" content="es_CO">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="https://detailingexperts.com/images/og-default.png">
<link rel="preconnect" href="https://images.unsplash.com">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,700;0,800;0,900;1,700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/style.min.css">
<script type="application/ld+json">{bc_json}</script>
<script type="application/ld+json">{service_json}</script>
<script type="application/ld+json">{faq_json}</script>
</head>
<body>
<div id="nav-placeholder"></div>

<header class="page-hero page-hero--sm">
  <div class="page-hero__bg">
    <img src="{img1400}" alt="{esc(title)}" loading="eager" fetchpriority="high" width="1400" height="933">
  </div>
  <div class="page-hero__overlay" aria-hidden="true"></div>
  <div class="page-hero__content">
    <span class="section-label">{esc(meta["label"])} · Cartagena</span>
    <h1 class="hero__title" style="max-width:860px;">{esc(title)}</h1>
    <p class="hero__desc" style="max-width:700px;">{esc(desc)}</p>
    <div class="hero__actions">
      <a href="{WA}?text={wa}" class="btn btn-primary btn-lg" target="_blank" rel="noopener noreferrer"><img src="../images/whatsapp-logo.png" alt="" aria-hidden="true" class="btn__icon" width="20" height="20">Cotizar por WhatsApp</a>
      <a href="index.html" class="btn btn-outline btn-lg">Ver todos los servicios</a>
    </div>
  </div>
</header>

<section class="section">
  <div class="container" style="max-width:880px;">
    <span class="section-label">El servicio</span>
    <h2 class="section-title" style="margin-bottom:1.25rem;">{esc(h2_intro)}</h2>
    <p class="lead" style="margin-bottom:1.25rem;">{esc(intro_lead)}</p>
    <p style="margin-bottom:1.25rem;">{esc(meta["intro2"])}</p>
    <ul style="color:var(--clr-text-2);line-height:1.9;padding-left:1.25rem;list-style:disc;">
      <li>Atención especializada para el clima costero de Cartagena de Indias.</li>
      <li>Evaluación previa sin costo y cotización transparente, sin sorpresas.</li>
      <li>Productos profesionales y garantía sobre el trabajo realizado.</li>
    </ul>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-header centered">
      <span class="section-label">Beneficios</span>
      <h2 class="section-title">{esc(h2_benefits)}</h2>
    </div>
    <div class="feature-grid">
      {feat_html}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header centered">
      <span class="section-label">Proceso</span>
      <h2 class="section-title">{esc(h2_process)}</h2>
    </div>
    <div class="process-steps">
      {steps_html}
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container" style="max-width:880px;">
    <div class="section-header centered">
      <span class="section-label">Dudas</span>
      <h2 class="section-title">{esc(h2_faq)}</h2>
    </div>
    <div style="display:grid;gap:1.25rem;">
      {faq_html}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header centered">
      <span class="section-label">Sigue explorando</span>
      <h2 class="section-title">Servicios relacionados</h2>
    </div>
    <div class="feature-grid">
      {rel_cards}
    </div>
  </div>
</section>

<section class="cta-section">
  <div class="container" style="position:relative;z-index:1;text-align:center;">
    <span class="cta-section__eyebrow">Detailing Experts · Cartagena</span>
    <h2 class="cta-section__title" style="color:var(--clr-white);">Solicita tu cotización sin compromiso</h2>
    <p class="cta-section__desc">Cuéntanos sobre tu vehículo y te asesoramos sobre la mejor solución. Estamos en la Cl. 31 #52-32, Progreso, frente a la Plaza de Toros.</p>
    <div class="cta-section__actions">
      <a href="{WA}?text={wa}" class="btn btn-whatsapp btn-lg" target="_blank" rel="noopener noreferrer"><img src="../images/whatsapp-logo.png" alt="" aria-hidden="true" class="btn__icon" width="20" height="20">Escríbenos por WhatsApp</a>
      <a href="../contacto.html" class="btn btn-outline-white btn-lg">Ver datos de contacto</a>
    </div>
  </div>
</section>

<div id="footer-placeholder"></div>
<script>window.basePath = "../";</script>
<script src="../js/components.js" defer></script>
<script src="../js/main.js" defer></script>
</body>
</html>'''

    with open(os.path.join(SERV, p["fn"]), "w", encoding="utf-8") as f:
        f.write(html_out)

if __name__ == "__main__":
    main()
