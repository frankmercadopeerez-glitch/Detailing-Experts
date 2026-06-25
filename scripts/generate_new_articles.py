# -*- coding: utf-8 -*-
"""Crea 11 articulos nuevos del blog, ricos y orientados a las preguntas frecuentes
de los clientes (uno por categoria + uno general)."""
import os, json, html

BLOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "blog")
def esc(s): return html.escape(s, quote=True)

WA = "https://wa.me/573016501515?text=Hola%2C%20le%C3%AD%20su%20blog%20y%20quiero%20cotizar"

# Cada articulo: slug, img, title, desc, lead, secs[(h2,[parrafos])], faq[(q,a)], links[(txt,href)], hub
ARTICLES = [
{
 "slug":"guia-proteger-auto-salitre-cartagena","img":"photo-1503376780353-7e6692767b70",
 "title":"Cómo Proteger tu Auto del Salitre en Cartagena: Guía Completa 2026",
 "desc":"Guía completa para proteger tu vehículo del salitre y la humedad de Cartagena: anticorrosiva, ceramic coating, PPF, polarizado y mantenimiento. Qué necesita cada auto y cuánto cuesta.",
 "lead":"Cartagena es hermosa, pero su clima es de los más duros para un vehículo: el salitre del mar, la humedad y el sol atacan la carrocería todos los días. En esta guía te explicamos, paso a paso, cómo proteger tu auto y qué servicio conviene según tu caso.",
 "secs":[
   ("¿Por qué el clima de Cartagena daña tanto los autos?",["El aire costero lleva sal en suspensión que se deposita sobre el metal y la pintura. Con la humedad tropical, esa sal acelera la oxidación y deja manchas blancas difíciles de quitar. A esto se suma un sol intenso que decolora la pintura y reseca el interior.","Por eso, un auto en Cartagena necesita protecciones pensadas específicamente para el ambiente marino, no las mismas que servirían en el interior del país."]),
   ("Las 5 protecciones que más cuidan tu auto",["<strong>Protección anticorrosiva:</strong> frena el óxido en chasis, bajos y cavidades; es la base para que el auto dure. <strong>Ceramic coating:</strong> sella la pintura, repele el agua y el salitre y mantiene el brillo. <strong>PPF:</strong> protege físicamente la pintura de piedras y rayones. <strong>Polarizado:</strong> bloquea el UV y baja el calor interior. <strong>Detailing y mantenimiento:</strong> conservan el resultado en el tiempo."]),
   ("¿Por dónde empezar según tu presupuesto?",["Si tu prioridad es evitar el óxido, empieza por la protección anticorrosiva. Si quieres conservar el brillo y facilitar el lavado, el ceramic coating es la mejor relación costo-beneficio. Para autos nuevos o de alto valor, combinar PPF + ceramic es la protección más completa.","En una evaluación gratuita revisamos tu vehículo y te recomendamos el orden ideal sin venderte de más."]),
 ],
 "faq":[
   ("¿Qué protección es la más importante en Cartagena?","La protección anticorrosiva, porque evita el problema más costoso y difícil de revertir: el óxido. Sobre esa base, el ceramic coating cuida la pintura del salitre y el sol."),
   ("¿Cuánto cuesta proteger bien un auto?","Depende del vehículo y de lo que elijas. Una anticorrosiva parte desde 1.2M y un ceramic coating desde 800K. Armamos paquetes combinados con mejor precio según tu presupuesto."),
   ("¿Cada cuánto debo renovar las protecciones?","Cada protección tiene su ritmo: el ceramic dura 2-5 años, la anticorrosiva alrededor de 1 año (luego se recomienda repintar) y el polarizado es permanente. Te damos un plan de mantenimiento personalizado."),
   ("¿Atienden todos los barrios de Cartagena?","Sí. Atendemos toda la ciudad desde nuestra sede en la Cl. 31 #52-32, Progreso, frente a la Plaza de Toros."),
 ],
 "links":[("Protección Anticorrosiva","../servicios/proteccion-anticorrosiva.html"),("Ceramic Coating en Cartagena","../servicios/ceramic-coating-cartagena.html"),("Paint Protection Film (PPF)","../servicios/ppf.html"),("Todos los servicios","../servicios/index.html")],
 "hub":"../servicios/index.html",
},
{
 "slug":"proteccion-anticorrosiva-precio-duracion-cartagena","img":"photo-1597007030739-6d2e7172ee5a",
 "title":"Protección Anticorrosiva en Cartagena: Precio, Duración y Cómo Funciona",
 "desc":"Todo sobre la protección anticorrosiva en Cartagena: cómo funciona, cuánto cuesta, cuánto dura (alrededor de 1 año), el mantenimiento bimensual gratuito y qué pasa cuando hay óxido con soldadura.",
 "lead":"La protección anticorrosiva es la inversión que más prolonga la vida de un auto en Cartagena. Aquí respondemos las preguntas que más nos hacen los clientes: cómo funciona, cuánto cuesta, cuánto dura y qué pasa cuando ya hay óxido.",
 "secs":[
   ("¿Cómo funciona la protección anticorrosiva?",["Aplicamos un recubrimiento especializado sobre la carrocería, los bajos del chasis y las cavidades ocultas donde se acumula la sal. Esa capa crea una barrera que frena el avance del óxido y previene su aparición.","Antes de aplicarla inspeccionamos el vehículo: el óxido superficial se lija y neutraliza, y cuando hay zonas podridas o perforadas por la corrosión, esas partes se reemplazan con soldadura antes de proteger."]),
   ("¿Cuánto cuesta y por qué varía el precio?",["El precio parte desde 1.2M en autos compactos y desde 1.5M en SUV o camionetas. El factor que más cambia el costo es el estado del vehículo: cuando hay zonas podridas por el óxido que deben reemplazarse con soldadura, ese trabajo adicional aumenta el valor según la extensión del daño.","Por eso siempre hacemos una evaluación gratuita antes de cotizar: así sabes exactamente qué incluye tu presupuesto."]),
   ("¿Cuánto dura y cómo se mantiene?",["La protección anticorrosiva dura alrededor de 1 año, momento en que se recomienda repintar para renovarla. Para conservarla en óptimas condiciones incluimos un mantenimiento bimensual totalmente gratuito, en el que revisamos el estado y reforzamos las zonas que lo necesiten.","Aprovechar ese mantenimiento gratis es la mejor forma de que la protección trabaje al 100% durante todo el año."]),
 ],
 "faq":[
   ("¿Cuánto cuesta la protección anticorrosiva en Cartagena?","Desde 1.2M en autos compactos y desde 1.5M en SUV o camionetas. El precio sube cuando hay zonas podridas por el óxido que deben reemplazarse con soldadura."),
   ("¿Cuánto dura la protección anticorrosiva?","Alrededor de 1 año. Pasado ese tiempo se recomienda repintar para renovar la protección."),
   ("¿El mantenimiento tiene costo?","No. El mantenimiento bimensual de la protección anticorrosiva es totalmente gratuito: revisamos y reforzamos las zonas que lo necesiten sin cobrarte."),
   ("¿Qué pasa si mi carro ya tiene óxido?","El óxido superficial se lija y neutraliza. Si hay zonas podridas o perforadas, se reemplazan con soldadura antes de aplicar la protección; ese trabajo aumenta el costo según el daño."),
   ("¿La protección anticorrosiva se ve?","Tenemos versión transparente (no altera el color) y convencional (acabado tipo cera para los bajos). Te asesoramos según la zona."),
 ],
 "links":[("Protección Anticorrosiva","../servicios/proteccion-anticorrosiva.html"),("Precio de anticorrosiva","../servicios/precio-anticorrosiva-cartagena.html"),("Anticorrosiva + reparación de óxido","../servicios/anticorrosiva-reparacion-leve.html")],
 "hub":"../servicios/proteccion-anticorrosiva.html",
},
{
 "slug":"ppf-preguntas-frecuentes-cartagena","img":"photo-1552519507-da3b142c6e3d",
 "title":"PPF en Cartagena: 7 Preguntas Frecuentes Antes de Instalarlo",
 "desc":"Resolvemos las dudas más comunes sobre el PPF (Paint Protection Film) en Cartagena: qué protege, si se nota, si se autorrepara, cuánto cuesta y cuánto dura.",
 "lead":"El PPF es la protección física más resistente para la pintura, pero antes de instalarlo los clientes siempre tienen las mismas dudas. Aquí las respondemos todas para que decidas con información clara.",
 "secs":[
   ("¿Qué es y qué protege el PPF?",["El PPF (Paint Protection Film) es una película de uretano transparente que se instala sobre la pintura. Absorbe el impacto de piedras y gravilla, evita rayones y resiste el salitre, manteniendo intacta la pintura de fábrica.","Es la mejor opción para las zonas de mayor impacto: capó, paragolpes, espejos y faros."]),
   ("¿Cobertura parcial o completa?",["Un kit frontal protege las zonas que más sufren y parte desde 2M. La cobertura completa blinda todo el vehículo desde 4M. Para la mayoría de los autos en ciudad, una cobertura frontal resuelve el 90% del riesgo de picotazos.","Si tu auto es nuevo o de alto valor, vale la pena evaluar la cobertura completa o combinarla con ceramic coating."]),
 ],
 "faq":[
   ("¿El PPF se nota una vez instalado?","No. Es una película transparente de alta claridad; una vez instalada mantiene el aspecto de fábrica del vehículo."),
   ("¿De verdad se autorrepara?","Las referencias premium sí: los micro-rayones superficiales desaparecen con el calor del sol o agua caliente. Los cortes profundos no, pero la película evita que lleguen a la pintura."),
   ("¿Cuánto cuesta el PPF en Cartagena?","Un kit frontal parte desde 2M y la cobertura completa desde 4M, según el modelo y las zonas a proteger."),
   ("¿Cuánto dura el PPF?","Entre 5 y 10 años según la calidad de la película y el mantenimiento. Ofrecemos garantía sobre la instalación."),
   ("¿Puedo combinar PPF con ceramic coating?","Sí, es la combinación ideal: el PPF protege del impacto y el ceramic aporta hidrofobicidad y brillo sobre la película."),
 ],
 "links":[("Paint Protection Film (PPF)","../servicios/ppf.html"),("Precio de PPF","../servicios/precio-ppf-cartagena.html"),("PPF vs Ceramic Coating","../servicios/wrap-vs-ppf-comparativa.html")],
 "hub":"../servicios/ppf.html",
},
{
 "slug":"ceramic-coating-preguntas-frecuentes-cartagena","img":"photo-1607860108855-64acf2078ed9",
 "title":"Ceramic Coating en Cartagena: Todo lo que Preguntan los Clientes",
 "desc":"Las preguntas frecuentes sobre ceramic coating en Cartagena: cuánto dura, si es mejor que la cera, cuánto cuesta, si elimina rayones y qué mantenimiento necesita.",
 "lead":"El ceramic coating es uno de los servicios más solicitados en Cartagena por el salitre y el sol. Estas son las preguntas que más nos hacen antes de aplicarlo.",
 "secs":[
   ("¿Por qué el ceramic coating funciona tan bien en Cartagena?",["El ceramic coating crea una capa dura e hidrofóbica sobre la pintura: el agua y el salitre resbalan sin adherirse, y la radiación UV que decolora la pintura queda bloqueada. En un clima costero, eso se traduce en un auto que conserva el brillo y se ensucia menos.","Además, lavar el vehículo se vuelve mucho más fácil porque la suciedad no se queda pegada."]),
   ("Preparación: el secreto de un buen resultado",["Para que el coating quede impecable, primero descontaminamos la pintura y, si tiene micro-rayones, hacemos una corrección. El coating se aplica sobre una superficie perfecta y sella ese resultado por años."]),
 ],
 "faq":[
   ("¿Cuánto dura el ceramic coating en Cartagena?","Entre 2 y 5 años según el producto y el mantenimiento. Con lavados de pH neutro conserva sus propiedades por mucho más tiempo que una cera."),
   ("¿Es mejor que la cera tradicional?","Sí. La cera dura semanas; el ceramic coating dura años, ofrece mayor dureza, mejor repelencia al agua y una protección UV muy superior."),
   ("¿Cuánto cuesta el ceramic coating?","Desde 800K en autos compactos, 1.2M en sedanes y 1.5M en SUV. Si la pintura necesita corrección previa, se incluye en la cotización."),
   ("¿El ceramic coating elimina los rayones?","No los rellena, pero protege. Si tu pintura tiene micro-rayones, hacemos una corrección previa para que el acabado quede perfecto."),
   ("¿Qué mantenimiento necesita?","Solo lavados regulares con productos suaves. Ofrecemos un mantenimiento profesional opcional para renovar la capa hidrofóbica."),
 ],
 "links":[("Ceramic Coating en Cartagena","../servicios/ceramic-coating-cartagena.html"),("Precio de ceramic coating","../servicios/precio-ceramic-coating-cartagena.html"),("Cera vs Ceramic Coating","../servicios/cera-vs-ceramic-diferencias.html")],
 "hub":"../servicios/ceramic-coating-cartagena.html",
},
{
 "slug":"cada-cuanto-detailing-cartagena","img":"photo-1607860108855-64acf2078ed9",
 "title":"¿Cada Cuánto Hacer Detailing en Cartagena? Guía y Frecuencias",
 "desc":"Cada cuánto conviene hacer detailing en Cartagena según el uso del auto, qué incluye un detailing completo y en qué se diferencia de un autolavado. Precios y recomendaciones.",
 "lead":"El detailing devuelve el aspecto de auto nuevo, pero ¿cada cuánto conviene hacerlo en una ciudad como Cartagena? Depende del uso y la exposición al salitre. Te lo explicamos.",
 "secs":[
   ("¿Qué incluye un detailing completo?",["Un detailing profundo va mucho más allá de un lavado: incluye descontaminación de la pintura, corrección de micro-rayones, limpieza detallada del interior (tapicería, plásticos, vidrios) y un sellado protector final.","El resultado es un auto impecable por dentro y por fuera, con brillo y protección que duran."]),
   ("Frecuencia recomendada según tu caso",["Para un auto de uso diario en Cartagena recomendamos un detailing completo cada 4 a 6 meses, con lavados de mantenimiento entre cada uno. Si el vehículo se expone al mar o se parquea al aire libre, conviene acercarse al rango de 4 meses.","Si solo lo usas ocasionalmente, cada 6 meses suele ser suficiente."]),
 ],
 "faq":[
   ("¿Cada cuánto debo hacer detailing?","Para mantener el auto impecable, un detailing completo cada 4 a 6 meses, con lavados de mantenimiento entre cada uno."),
   ("¿En qué se diferencia del autolavado?","El autolavado limpia la superficie; el detailing descontamina, corrige la pintura, detalla el interior y aplica protección. El resultado y la duración no se comparan."),
   ("¿Cuánto cuesta el detailing en Cartagena?","Un detailing básico parte desde 500K y el premium con corrección de pintura y sellado desde 1.5M, según el tamaño y estado del vehículo."),
   ("¿El detailing incluye el interior?","Sí. Limpiamos y desinfectamos tapicería, plásticos y vidrios, eliminando olores y devolviendo el aspecto de nuevo."),
 ],
 "links":[("Detailing Premium en Cartagena","../servicios/detailing-premium.html"),("Precio de detailing","../servicios/precio-detailing-cartagena.html"),("Detailing vs autolavado","../servicios/detailing-casero-vs-profesional.html")],
 "hub":"../servicios/detailing-premium.html",
},
{
 "slug":"polarizado-precio-legalidad-cartagena","img":"photo-1568605117036-5fe5e7bab0b7",
 "title":"Polarizado en Cartagena: Precio, Legalidad y Beneficios (FAQ)",
 "desc":"Preguntas frecuentes sobre el polarizado automotriz en Cartagena: cuánto cuesta, qué es legal en Colombia (70% VLT), cuánto reduce el calor y si queda con burbujas.",
 "lead":"El polarizado es casi obligatorio en Cartagena por el calor y el sol, pero hay que hacerlo bien y dentro de la ley. Resolvemos las dudas más frecuentes.",
 "secs":[
   ("Beneficios reales del polarizado en el Caribe",["Una buena lámina de control solar bloquea hasta el 99% de los rayos UV, reduce notablemente el calor dentro del habitáculo y aporta privacidad. Además protege la tapicería de decolorarse y resecarse con el sol.","La diferencia entre una lámina económica y una de calidad se nota sobre todo en el rechazo de calor."]),
   ("Legalidad: lo que debes saber",["En Colombia la norma exige una visibilidad mínima del 70% VLT en el parabrisas y los vidrios delanteros. Instalamos cumpliendo la regulación para que evites comparendos y conserves la seguridad al conducir de noche."]),
 ],
 "faq":[
   ("¿Cuánto cuesta el polarizado en Cartagena?","Desde 500K en autos compactos y desde 800K en SUV, según el número de vidrios y el tipo de lámina."),
   ("¿Cuánto polarizado es legal en Colombia?","Se exige al menos 70% VLT (visibilidad) en parabrisas y vidrios delanteros. Instalamos cumpliendo la norma."),
   ("¿Cuánto reduce el calor?","Una buena lámina baja varios grados la temperatura interior y bloquea hasta el 99% del UV."),
   ("¿Queda con burbujas?","No. Trabajamos en ambiente controlado y con técnica profesional para un acabado uniforme, sin burbujas ni pliegues."),
   ("¿Cuánto tiempo toma la instalación?","Entre 2 y 4 horas según el vehículo. Lo entregas en la mañana y lo recoges el mismo día."),
 ],
 "links":[("Polarizado Automotriz","../servicios/polarizados.html"),("Precio de polarizado","../servicios/precio-polarizado-cartagena.html"),("Polarizado legal en Colombia","polarizado-legal-colombia.html")],
 "hub":"../servicios/polarizados.html",
},
{
 "slug":"wrap-vinilico-preguntas-frecuentes-cartagena","img":"photo-1583267746897-2cf415887172",
 "title":"Wrap Vinílico en Cartagena: Dudas Frecuentes Antes de Cambiar el Color",
 "desc":"Preguntas frecuentes sobre el wrap vinílico en Cartagena: si daña la pintura, cuánto dura, cuánto cuesta, cuánto tarda la instalación y cómo se cuida.",
 "lead":"El wrap vinílico permite cambiar el color de tu auto sin pintarlo y de forma reversible. Antes de decidirte, estas son las preguntas que más nos hacen.",
 "secs":[
   ("¿Qué es el wrap y por qué es tan versátil?",["El wrap envuelve la carrocería con láminas de vinilo de alta calidad para cambiar el color o el acabado: mate, brillante, satinado, carbono, cromo y cientos de colores. Y es totalmente reversible.","Además de transformar la estética, el vinilo protege la pintura original de rayones y del sol."]),
   ("Reversible y seguro para tu pintura",["Al retirarse correctamente, la pintura de fábrica queda intacta (siempre que esté en buen estado al instalar). Por eso el wrap es la forma más segura de personalizar sin perder valor de reventa."]),
 ],
 "faq":[
   ("¿El wrap daña la pintura?","No. Al retirarse correctamente la pintura original queda intacta, y mientras está puesto la protege de rayones y sol."),
   ("¿Cuánto dura el wrap vinílico?","Entre 5 y 7 años con buen mantenimiento. Los vinilos premium resisten bien el sol y el salitre de Cartagena."),
   ("¿Cuánto cuesta el wrap?","Un wrap parcial parte desde 1.2M y un cambio de color completo desde 3M, según el tamaño del vehículo y el tipo de vinilo."),
   ("¿Cuánto tarda la instalación?","Un wrap parcial toma de 4 a 6 horas; un cambio de color completo, de 2 a 3 días según la complejidad."),
   ("¿Cómo se cuida el vinilo?","Lavado a mano con productos suaves; evita hidrolavadoras a alta presión cerca de los bordes."),
 ],
 "links":[("Wrap Vinílico en Cartagena","../servicios/wrap.html"),("Precio de wrap","../servicios/precio-wrap-cartagena.html"),("Wrap vs PPF","../servicios/wrap-vs-ppf-comparativa.html")],
 "hub":"../servicios/wrap.html",
},
{
 "slug":"pdr-que-abolladuras-se-reparan-cartagena","img":"photo-1597007030739-6d2e7172ee5a",
 "title":"PDR en Cartagena: ¿Qué Abolladuras se Pueden Reparar sin Pintar?",
 "desc":"Qué es el PDR (reparación de abolladuras sin pintura) en Cartagena, qué golpes se pueden reparar, cuáles no, cuánto cuesta y por qué conserva la pintura original.",
 "lead":"El PDR repara abolladuras sin repintar, conservando la pintura de fábrica. Pero no todas las abolladuras son candidatas. Te explicamos cuándo funciona y cuándo no.",
 "secs":[
   ("¿Cómo funciona el PDR?",["El PDR (Paintless Dent Repair) devuelve la forma al metal masajeándolo desde el interior del panel, sin masilla y sin repintar. Como no se toca la pintura, no hay diferencias de color ni riesgo de afectar el valor del vehículo.","Es más rápido y económico que la latonería tradicional, y muchas reparaciones se resuelven el mismo día."]),
   ("¿Qué abolladuras sí y cuáles no?",["Funciona muy bien cuando la pintura está intacta y el metal no está demasiado estirado: golpes de parqueadero, abolladuras de granizo y bollos sin pintura dañada. No es la opción cuando la pintura está partida o rota: en esos casos recomendamos latonería y pintura."]),
 ],
 "faq":[
   ("¿Qué abolladuras se pueden reparar con PDR?","Las que tienen la pintura intacta y el metal no muy estirado: golpes de parqueadero, granizo y bollos sin pintura dañada."),
   ("¿Cuándo no sirve el PDR?","Cuando la pintura está partida o el metal muy deformado. Ahí recomendamos latonería y pintura."),
   ("¿Cuánto cuesta el PDR en Cartagena?","Las abolladuras pequeñas parten desde 150K. Evaluamos cada caso y cotizamos sin compromiso."),
   ("¿Queda algún rastro?","Bien ejecutado, el PDR devuelve la forma original sin rastro visible y sin afectar la pintura."),
   ("¿Sirve para daños de granizo?","Sí, es el método ideal para múltiples abolladuras de granizo conservando la pintura de fábrica."),
 ],
 "links":[("PDR – Reparación sin Pintura","../servicios/pdr.html"),("PDR en Bocagrande","../servicios/pdr-bocagrande-cartagena.html"),("Latonería y Pintura","../servicios/latoneria-pintura.html")],
 "hub":"../servicios/pdr.html",
},
{
 "slug":"latoneria-pintura-oxido-soldadura-cartagena","img":"photo-1597007030739-6d2e7172ee5a",
 "title":"Latonería y Pintura en Cartagena: Óxido, Soldadura y Precios",
 "desc":"Cómo funciona la latonería y pintura en Cartagena: reparación de golpes y óxido, cuándo se necesita soldadura, igualación de color y precios orientativos.",
 "lead":"Cuando el daño llega al metal, actuar a tiempo evita que el óxido se extienda. Te explicamos cómo reparamos golpes y zonas oxidadas, cuándo hace falta soldadura y cuánto cuesta.",
 "secs":[
   ("Cuándo el óxido obliga a soldar",["El óxido superficial se lija, neutraliza y sella. Pero cuando la corrosión ya perforó o pudrió una zona de la carrocería, esa parte debe cortarse y reemplazarse con soldadura antes de repintar. Es la única forma de detener el daño de raíz.","Por eso el precio de una reparación con óxido varía tanto: depende de cuánto metal haya que recuperar o reemplazar."]),
   ("Acabado idéntico al de fábrica",["Trabajamos con igualación de color computarizada para que la zona reparada quede idéntica al resto de la carrocería. Y en Cartagena, además, tratamos la zona contra la corrosión antes de pintar para que el problema no reaparezca."]),
 ],
 "faq":[
   ("¿Cuánto cuesta reparar un golpe o rayón?","Un rayón superficial parte desde 200K; la reparación con latonería y repintado de un panel desde 800K, según la extensión del daño."),
   ("¿Cuándo se necesita soldadura?","Cuando el óxido pudrió o perforó una zona de la carrocería. Esa parte se reemplaza con soldadura antes de repintar; ese trabajo aumenta el costo."),
   ("¿La reparación se nota?","No. Con la igualación de color computarizada y el acabado profesional, la zona reparada queda idéntica al resto."),
   ("¿Tratan el óxido antes de pintar?","Siempre. Lijamos, neutralizamos y, si hace falta, soldamos antes de aplicar la pintura para que el óxido no vuelva."),
 ],
 "links":[("Latonería y Pintura","../servicios/latoneria-pintura.html"),("Pintura oxidada: cómo repararla","../servicios/pintura-oxidada-reparar-cartagena.html"),("Protección Anticorrosiva","../servicios/proteccion-anticorrosiva.html")],
 "hub":"../servicios/latoneria-pintura.html",
},
{
 "slug":"mantenimiento-preventivo-auto-cartagena-guia","img":"photo-1597007030739-6d2e7172ee5a",
 "title":"Mantenimiento Preventivo del Auto en Cartagena: Qué Incluye y Cada Cuánto",
 "desc":"Guía del mantenimiento preventivo automotriz en Cartagena: qué incluye, cada cuánto hacerlo, el mantenimiento bimensual gratuito de la anticorrosiva y los planes semestrales.",
 "lead":"En el clima salino de Cartagena, el mantenimiento preventivo es lo que marca la diferencia entre un auto que se conserva impecable durante años y uno que se deteriora. Te contamos qué incluye y con qué frecuencia conviene.",
 "secs":[
   ("Por qué el mantenimiento preventivo cuesta menos que reparar",["Renovar a tiempo las protecciones cuesta una fracción de lo que costaría reparar el daño acumulado por el salitre y el sol. Un plan preventivo detecta a tiempo el óxido, las manchas o el desgaste antes de que se conviertan en reparaciones mayores."]),
   ("Qué incluye y cada cuánto",["El mantenimiento incluye lavado técnico, revisión del estado de la pintura y las protecciones, renovación de la capa hidrofóbica y verificación de las zonas anticorrosivas. La revisión bimensual de la protección anticorrosiva es gratuita; para un cuidado integral ofrecemos planes semestrales más completos.","Adaptamos la frecuencia al uso de tu vehículo y a las protecciones que tenga aplicadas."]),
 ],
 "faq":[
   ("¿El mantenimiento bimensual tiene costo?","La revisión bimensual de la protección anticorrosiva es gratuita. Para un cuidado integral ofrecemos planes semestrales más completos."),
   ("¿Qué incluye el mantenimiento?","Lavado técnico, revisión de pintura y protecciones, renovación de la capa hidrofóbica y verificación de zonas anticorrosivas."),
   ("¿Cada cuánto se hace?","La revisión bimensual es gratuita; además recomendamos un cuidado integral semestral. Ajustamos la frecuencia a tu uso."),
   ("¿Vale la pena el plan preventivo?","Sí. Cuesta mucho menos que reparar el daño por salitre y sol, y mantiene tu auto siempre presentable."),
 ],
 "links":[("Mantenimiento Automotriz","../servicios/mantenimiento-automotriz-cartagena.html"),("Mantenimiento de anticorrosiva","../servicios/mantenimiento-anticorrosiva.html"),("Mantenimiento semestral","../servicios/mantenimiento-semestral-vehiculo.html")],
 "hub":"../servicios/mantenimiento-automotriz-cartagena.html",
},
{
 "slug":"que-proteccion-elegir-segun-vehiculo-cartagena","img":"photo-1503376780353-7e6692767b70",
 "title":"Qué Protección Elegir según tu Vehículo en Cartagena",
 "desc":"Guía para elegir la protección ideal según tu vehículo en Cartagena: auto nuevo, usado, compacto, SUV, camioneta de trabajo o auto de lujo. Recomendaciones y presupuestos.",
 "lead":"No todos los autos necesitan lo mismo. Un compacto urbano, una camioneta de trabajo y un auto de lujo tienen prioridades distintas. Esta guía te ayuda a elegir la protección correcta según tu vehículo.",
 "secs":[
   ("Según el tipo de vehículo",["<strong>Auto compacto urbano:</strong> polarizado + ceramic coating cubren lo esencial (calor, UV y brillo) con buen presupuesto. <strong>SUV o camioneta familiar:</strong> suma protección anticorrosiva por la exposición de los bajos. <strong>Camioneta de trabajo (pickup):</strong> anticorrosiva reforzada y, si quieres cuidar la pintura de piedras, PPF frontal. <strong>Auto nuevo o de lujo:</strong> PPF + ceramic coating es la protección más completa."]),
   ("Según el estado y la antigüedad",["Un auto nuevo conviene protegerlo desde el primer año, antes de que el salitre actúe. En un auto usado, primero evaluamos si hay óxido para tratarlo (incluso con soldadura si hay zonas podridas) y luego protegemos. Te damos el orden ideal en una evaluación gratuita."]),
 ],
 "faq":[
   ("¿Qué protección necesita un auto nuevo?","Idealmente PPF + ceramic coating para conservar la pintura de fábrica, más polarizado y anticorrosiva preventiva."),
   ("¿Y un auto usado con algo de óxido?","Primero se trata el óxido (con soldadura si hay zonas podridas) y luego se aplica la anticorrosiva y el ceramic para proteger."),
   ("¿Cuál es la protección con mejor relación costo-beneficio?","El ceramic coating, porque cuida la pintura del salitre y el sol y facilita el lavado, con una inversión moderada."),
   ("¿Pueden recomendarme según mi modelo?","Sí. Cuéntanos el modelo y el uso de tu auto y te damos una recomendación y un presupuesto personalizado sin compromiso."),
 ],
 "links":[("Todos los servicios","../servicios/index.html"),("Protección Anticorrosiva","../servicios/proteccion-anticorrosiva.html"),("Ceramic Coating","../servicios/ceramic-coating-cartagena.html"),("Paint Protection Film (PPF)","../servicios/ppf.html")],
 "hub":"../servicios/index.html",
},
]

def render(a):
    slug=a["slug"]; title=a["title"]; desc=a["desc"]
    canon=f"https://detailingexperts.com/blog/{slug}.html"
    img12=f"https://images.unsplash.com/{a['img']}?auto=format&fit=crop&w=1200&q=80"
    img14=f"https://images.unsplash.com/{a['img']}?auto=format&fit=crop&w=1400&q=80"
    secs=""
    for h,ps in a["secs"]:
        secs+=f"<h2>{esc(h)}</h2>\n"
        for p in ps:
            secs+=f"<p>{p}</p>\n"  # ya contiene HTML controlado (strong)
    faqv=""
    for q,ans in a["faq"]:
        faqv+=(f'<div class="card" style="padding:1.5rem;margin-bottom:1rem;">'
               f'<h3 style="color:var(--clr-accent);font-size:var(--text-lg);margin-bottom:.5rem;">{esc(q)}</h3>'
               f'<p style="max-width:none;">{esc(ans)}</p></div>')
    links="".join(f'<li><a href="{href}" style="color:var(--clr-accent);">{esc(t)}</a></li>' for t,href in a["links"])
    blogposting={"@context":"https://schema.org","@type":"BlogPosting","headline":title,"description":desc,"image":img12,
        "author":{"@type":"Organization","name":"Detailing Experts"},
        "publisher":{"@type":"Organization","name":"Detailing Experts","logo":{"@type":"ImageObject","url":"https://detailingexperts.com/images/Detailing%20(4).PNG"},"url":"https://detailingexperts.com"},
        "datePublished":"2026-06-03","dateModified":"2026-06-03","mainEntityOfPage":{"@type":"WebPage","@id":canon}}
    breadcrumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Inicio","item":"https://detailingexperts.com/"},
        {"@type":"ListItem","position":2,"name":"Blog","item":"https://detailingexperts.com/blog/index.html"},
        {"@type":"ListItem","position":3,"name":title,"item":canon}]}
    faqschema={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":ans}} for q,ans in a["faq"]]}
    return f'''<!doctype html>
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
<script type="application/ld+json">{json.dumps(faqschema, ensure_ascii=False)}</script>
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
    <p class="lead" style="color:var(--clr-text-1);font-weight:500;margin-bottom:2rem;">{esc(a['lead'])}</p>

    {secs}

    <h2>Preguntas frecuentes</h2>
    {faqv}

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
      <a href="{WA}" class="btn btn-whatsapp btn-lg" target="_blank" rel="noopener noreferrer"><img src="../images/whatsapp-logo.png" alt="" aria-hidden="true" class="btn__icon" width="20" height="20">Cotizar por WhatsApp</a>
      <a href="{a['hub']}" class="btn btn-outline-white btn-lg">Ver el servicio</a>
    </div>
  </div>
</section>

<div id="footer-placeholder"></div>
<script>window.basePath = "../";</script>
<script src="../js/components.js" defer></script>
<script src="../js/main.js" defer></script>
</body>
</html>'''

def main():
    for a in ARTICLES:
        with open(os.path.join(BLOG, a["slug"]+".html"), "w", encoding="utf-8") as f:
            f.write(render(a))
    print(f"Articulos nuevos creados: {len(ARTICLES)}")
    for a in ARTICLES: print("  ", a["slug"]+".html")

if __name__ == "__main__":
    main()
