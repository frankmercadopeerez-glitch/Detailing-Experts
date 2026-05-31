$files = @(
  @{f="servicios/detailing-premium.html";t="Detailing Premium Cartagena | Limpieza Profunda | Detailing Experts";d="Detailing premium en Cartagena: limpieza profunda, corrección de pintura y protección. Tu auto como recién salido del concesionario.";i="https://images.unsplash.com/photo-1607860108855-64acf2078ed9?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/servicios/detailing-premium.html"},
  @{f="servicios/ppf.html";t="PPF Cartagena | Paint Protection Film | Detailing Experts";d="Paint Protection Film en Cartagena. Película invisible que protege la pintura de rayones, impactos y UV.";i="https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/servicios/ppf.html"},
  @{f="servicios/polarizados.html";t="Polarizados Cartagena | Instalación Profesional | Detailing Experts";d="Polarizado de carros en Cartagena. Sin burbujas. Bloquea 99% UV, reduce calor hasta 60%.";i="https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/servicios/polarizados.html"},
  @{f="servicios/pdr.html";t="PDR Cartagena | Reparación de Abolladuras Sin Pintura | Detailing Experts";d="PDR en Cartagena. Eliminamos abolladuras sin repintar, conservando la pintura original y el valor del vehículo.";i="https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/servicios/pdr.html"},
  @{f="servicios/wrap.html";t="Wrap Vinílico Cartagena | Cambio de Color | Detailing Experts";d="Wrap vinílico en Cartagena. Cambia el color, personaliza y protege la pintura original con viniles de alta calidad.";i="https://images.unsplash.com/photo-1583267746897-2cf415887172?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/servicios/wrap.html"},
  @{f="servicios/latoneria-pintura.html";t="Latonería y Pintura Cartagena | Reparación de Carrocería | Detailing Experts";d="Latonería y pintura en Cartagena. Acabados que igualan perfectamente el color original de tu vehículo.";i="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/servicios/latoneria-pintura.html"},
  @{f="servicios/toyota-cartagena.html";t="Especialistas Toyota Cartagena | Detailing Experts";d="Hilux, Prado, Land Cruiser y Fortuner: detailing, PPF, anticorrosiva y polarizados con +10 años de experiencia.";i="https://images.unsplash.com/photo-1559416523-140ddc3d238c?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/servicios/toyota-cartagena.html"},
  @{f="servicios/mantenimiento-automotriz-cartagena.html";t="Mantenimiento Automotriz Cartagena | Detailing Experts";d="Mantenimiento integral para el clima marino de Cartagena. Anticorrosiva, detailing, PPF y polarizados.";i="https://images.unsplash.com/photo-1520340356584-f9917d1eea6f?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/servicios/mantenimiento-automotriz-cartagena.html"},
  @{f="servicios/ceramic-coating-cartagena.html";t="Ceramic Coating Cartagena | Cristalizado de Pintura | Detailing Experts";d="Ceramic coating en Cartagena. Hidrofóbico, anti-salitre, anti-UV. Brillo que dura 2-5 años.";i="https://images.unsplash.com/photo-1607860108855-64acf2078ed9?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/servicios/ceramic-coating-cartagena.html"},
  @{f="servicios/anticorrosiva-bocagrande.html";t="Anticorrosiva en Bocagrande Cartagena | Detailing Experts";d="Anticorrosiva en Bocagrande. El salitre marino destruye el chasis — protegemos bajos y cavidades.";i="https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/servicios/anticorrosiva-bocagrande.html"},
  @{f="servicios/polarizados-manga-cartagena.html";t="Polarizados Manga y Bocagrande Cartagena | Detailing Experts";d="Polarizado en Manga y Bocagrande. Reducción de calor 60%, protección UV total, instalación profesional.";i="https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/servicios/polarizados-manga-cartagena.html"},
  @{f="servicios/ppf-bocagrande-cartagena.html";t="PPF en Bocagrande Cartagena | Detailing Experts";d="PPF en Bocagrande. Arena, salitre y gravilla rayan tu pintura. El PPF la protege de forma invisible.";i="https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/servicios/ppf-bocagrande-cartagena.html"},
  @{f="blog/proteccion-anticorrosiva-cartagena.html";t="Por qué tu Auto Necesita Anticorrosiva en Cartagena | Detailing Experts";d="El salitre marino destruye la carrocería. Descubre por qué la anticorrosiva es esencial en Cartagena.";i="https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/blog/proteccion-anticorrosiva-cartagena.html"},
  @{f="blog/pdr-reparacion-golpes-sin-pintura.html";t="PDR: Elimina Golpes sin Pintura | Detailing Experts Cartagena";d="PDR: la técnica que elimina abolladuras sin pintura. Cómo funciona y cuándo aplica.";i="https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/blog/pdr-reparacion-golpes-sin-pintura.html"},
  @{f="blog/ppf-paint-protection-film-cartagena.html";t="¿Qué es el PPF y por qué los Autos de Lujo lo Usan? | Detailing Experts";d="Paint Protection Film: la armadura invisible para la pintura. Todo lo que necesitas saber.";i="https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/blog/ppf-paint-protection-film-cartagena.html"},
  @{f="blog/detailing-premium-cartagena.html";t="Guía Completa de Detailing Automotriz en Cartagena | Detailing Experts";d="Qué es el detailing, qué incluye y cuándo hacerlo. La guía definitiva para dueños de autos en Cartagena.";i="https://images.unsplash.com/photo-1607860108855-64acf2078ed9?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/blog/detailing-premium-cartagena.html"},
  @{f="blog/polarizado-de-vidrios-cartagena.html";t="Polarizado de Carros en Cartagena: Todo lo que Necesitas Saber | Detailing Experts";d="Tipos, legalidad y reducción de calor. La guía completa de polarizados en Cartagena.";i="https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/blog/polarizado-de-vidrios-cartagena.html"},
  @{f="blog/detailing-premium-bocagrande-cartagena.html";t="Detailing Premium en Bocagrande Cartagena | Detailing Experts";d="Detailing para autos expuestos al salitre marino en Bocagrande y Castillogrande.";i="https://images.unsplash.com/photo-1607860108855-64acf2078ed9?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/blog/detailing-premium-bocagrande-cartagena.html"},
  @{f="blog/proteccion-anticorrosiva-manga-cartagena.html";t="Protección Anticorrosiva en Manga Cartagena | Detailing Experts";d="Cómo frenar el salitre en Manga con protección anticorrosiva preventiva.";i="https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/blog/proteccion-anticorrosiva-manga-cartagena.html"},
  @{f="blog/ppf-bocagrande-cartagena.html";t="PPF en Bocagrande Cartagena: Protección Invisible | Detailing Experts";d="PPF para autos premium en Bocagrande: protección invisible contra salitre y gravilla.";i="https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/blog/ppf-bocagrande-cartagena.html"},
  @{f="blog/wrap-manga-cartagena.html";t="Wrap Vinílico en Manga Cartagena | Detailing Experts";d="Cambia el color de tu vehículo sin repintar en Manga. Acabados premium en wrap.";i="https://images.unsplash.com/photo-1583267746897-2cf415887172?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/blog/wrap-manga-cartagena.html"},
  @{f="blog/ppf-vs-ceramic-coating.html";t="PPF vs Ceramic Coating en Cartagena | Detailing Experts";d="Dos tecnologías distintas para proteger tu pintura. Cuál te conviene en el clima de Cartagena.";i="https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/blog/ppf-vs-ceramic-coating.html"},
  @{f="blog/polarizado-legal-colombia.html";t="¿Cuánto Polarizado es Legal en Colombia? Guía 2026 | Detailing Experts";d="Normativa de polarizados en Colombia: porcentajes por vidrio y cómo instalar legalmente.";i="https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/blog/polarizado-legal-colombia.html"},
  @{f="blog/mantenimiento-preventivo-cartagena.html";t="Mantenimiento Preventivo del Carro en Cartagena | Detailing Experts";d="Qué revisar y cada cuánto en el clima marino de Cartagena para proteger tu vehículo.";i="https://images.unsplash.com/photo-1520340356584-f9917d1eea6f?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/blog/mantenimiento-preventivo-cartagena.html"},
  @{f="blog/toyota-cartagena-cuidados.html";t="Cómo Cuidar tu Toyota en Cartagena | Detailing Experts";d="Guía de anticorrosiva, PPF, detailing y polarizados para Toyota Hilux, Prado y Land Cruiser.";i="https://images.unsplash.com/photo-1559416523-140ddc3d238c?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/blog/toyota-cartagena-cuidados.html"},
  @{f="blog/cuanto-cuesta-ppf-cartagena.html";t="¿Cuánto Cuesta el PPF en Cartagena? | Detailing Experts";d="Factores que determinan el precio del PPF y por qué es una inversión que vale la pena.";i="https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/blog/cuanto-cuesta-ppf-cartagena.html"},
  @{f="blog/detailing-vs-autolavado.html";t="Detailing vs Autolavado en Cartagena | Detailing Experts";d="El autolavado limpia. El detailing restaura, corrige y protege. Descubre la diferencia real.";i="https://images.unsplash.com/photo-1607860108855-64acf2078ed9?auto=format&fit=crop&w=1200&q=80";u="https://detailingexperts.com/blog/detailing-vs-autolavado.html"}
)

$ogTemplate = @'
    <!-- Open Graph -->
    <meta property="og:type" content="website" />
    <meta property="og:url" content="URL_PLACEHOLDER" />
    <meta property="og:title" content="TITLE_PLACEHOLDER" />
    <meta property="og:description" content="DESC_PLACEHOLDER" />
    <meta property="og:image" content="IMG_PLACEHOLDER" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="TITLE_PLACEHOLDER" />
    <meta name="twitter:description" content="DESC_PLACEHOLDER" />
    <meta name="twitter:image" content="IMG_PLACEHOLDER" />
'@

$updated = 0
foreach ($item in $files) {
    $path = $item.f
    if (-not (Test-Path $path)) { Write-Host "MISSING: $path"; continue }
    $content = Get-Content $path -Raw -Encoding utf8
    if ($content -match 'og:type') { Write-Host "SKIP: $path"; continue }
    $og = $ogTemplate `
        -replace 'URL_PLACEHOLDER', $item.u `
        -replace 'TITLE_PLACEHOLDER', $item.t `
        -replace 'DESC_PLACEHOLDER', $item.d `
        -replace 'IMG_PLACEHOLDER', $item.i
    $pattern = '(<meta name="robots"[^/]*/>\s*)'
    $newContent = [regex]::Replace($content, $pattern, { param($m) $m.Value + $og }, 1)
    if ($newContent -eq $content) { Write-Host "WARN no match: $path"; continue }
    $newContent | Out-File $path -Encoding utf8 -NoNewline
    $updated++
    Write-Host "OK: $path"
}
Write-Host "Done: $updated files updated"
