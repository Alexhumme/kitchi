# Plan maestro de desarrollo — Kitchi Studio

Documento de planificación técnica · MVP académico · Versión 1.0 · 26 de octubre de 2026

Proyecto: aplicación web móvil para crear gatos chibi personalizados y generar paquetes de stickers, con personalización manual, inteligencia artificial y galería comunitaria.

Duración: 5 semanas · Equipo: 3 desarrolladores + 1 diseñadora gráfica junior · Modalidad: desarrollo local · Presupuesto: cero · Entrega: demostración visual y técnica.

La propuesta está concebida para servir como documento rector del proyecto, guía de implementación para el equipo y contexto de trabajo para los agentes de programación que participen en el repositorio.

La regla central es esta: construir un producto pequeño pero funcional, cuya arquitectura permita demostrar claramente los conceptos académicos, en lugar de intentar reproducir una aplicación comercial completa.

## 1. Resumen ejecutivo

[Download Kawaii Cat Waving and Smiling Kawaii Online - Creative Fabrica](https://images.openai.com/static-rsc-4/B5K6h8mnI784pTNEzUCq8eVXL8uq2w0rvS9v2aqi37glptLBsWU4ir3QXuwjZCZI0appdKkS1BfnUG88MqRucEIRwxG1FbWA-w4ZZsblRKutQ7tJklYgs-YbgiPWgbLiqMJtJZ96s5tqOefP7nbAHqNt_UkL99UokvRnRNzt17Q?purpose=inline)

# Kitchi Studio

Nombre de trabajo, sujeto a validación de marca.

Una experiencia de creación de personajes felinos que convierte combinaciones de ilustraciones y fotografías de referencia en stickers personalizados, descargables y compartibles.

PLAZO

## 5 semanas

PAQUETE MVP

## 6 stickers

CLIENTE

### Web móvil

ARTE

### 2D por capas

### 1.1 Objetivo general

Desarrollar un prototipo web móvil funcional que permita a usuarios crear personajes felinos de estilo chibi mediante personalización gráfica manual o transformación asistida por inteligencia artificial, generar paquetes de seis stickers con expresiones y poses predefinidas, descargarlos y compartirlos, y explorar o reutilizar personajes publicados por otros usuarios.

### 1.2 Objetivos específicos

1. Implementar un editor de personajes mediante composición de ilustraciones 2D por capas.
2. Desarrollar un flujo de transformación de fotografías de personas y gatos reales en representaciones felinas estilizadas, sujeto a la viabilidad del modelo de IA elegido.
3. Generar seis imágenes PNG con fondo transparente a partir de una configuración persistente del personaje.
4. Implementar acceso como invitado, registro, inicio de sesión y límites de creación del plan gratuito.
5. Crear un hub donde los usuarios registrados publiquen, exploren y copien creaciones.
6. Demostrar concurrencia, multiprocesamiento y paralelismo mediante operaciones reales, medibles y documentadas.
7. Mantener documentación técnica y de producto suficiente para que cualquier integrante o agente de programación pueda continuar el trabajo sin reconstruir el contexto.

### 1.3 Qué significa terminar el MVP

El MVP estará terminado cuando un usuario pueda completar un flujo integral:

Crear gato → personalizarlo → generar seis stickers → descargar el paquete → registrarse → publicar una creación → encontrarla desde otro usuario → copiarla y personalizarla.

La generación por IA debe contar con un flujo verificable independiente. Si el servicio externo no está disponible, el editor manual y la composición de stickers deben continuar funcionando.

## 2. Alcance: qué se construye y qué no

La restricción más importante del proyecto no es solamente el tiempo de programación. Es la combinación de diseño gráfico, editor interactivo, procesamiento de imágenes, integración de IA y backend.

Por ello, el alcance se divide en tres niveles.

P0 — Obligatorio para la entrega

- Editor de gatos 2D por capas.
- Tres opciones por cada campo de personalización.
- Seis stickers por paquete.
- Exportación PNG transparente.
- Invitado y cuenta registrada.
- Límite de tres gatos para usuarios gratuitos.
- Publicar, explorar y copiar personajes.
- IA integrada o, como mínimo, una integración real demostrable con un flujo de contingencia documentado.
- Evidencias de concurrencia, multiprocesamiento y paralelismo.

P1 — Solo después de completar P0

- Favoritos.
- Perfil público más elaborado.
- Búsqueda y filtros avanzados del hub.
- Guardado de paquetes completos en la cuenta.
- Indicador visual de tareas de generación en cola.
- Simulación de catálogo premium.

Fuera del MVP

- Pagos o suscripciones reales.
- Aplicación nativa publicada en tiendas.
- Integración directa con WhatsApp como paquete instalable.
- Modelos 3D y animaciones 3D.
- Entrenamiento de un modelo propio.
- Entrenamiento personalizado por usuario.
- Infraestructura de producción distribuida.
- Mensajería privada, comentarios y red social completa.

### 2.1 Funcionalidades concretas del editor

Cada campo tendrá tres alternativas seleccionables. Para evitar que el diseño gráfico crezca descontroladamente, las alternativas serán recursos gráficos predefinidos, no piezas que deban dibujarse en tiempo real.

| Campo                       | Tres alternativas conceptuales                        |
| --------------------------- | ----------------------------------------------------- |
| Patrón y colores del pelaje | Atigrado naranja, bicolor, manchas oscuras            |
| Ojos y color                | Redondos verdes, grandes azules, almendrados ámbar    |
| Cabello y color             | Flequillo corto, mechones laterales, cabello ondulado |
| Parte superior              | Camiseta, sudadera, camisa                            |
| Parte inferior              | Pantalón corto, falda, pantalón largo                 |
| Accesorios                  | Gafas, lazo, gorro                                    |

Las combinaciones deben seguir reglas de compatibilidad. Por ejemplo, una prenda puede ocultar una parte del cuerpo y el accesorio debe renderizarse delante o detrás de la cabeza según corresponda.

Importante: tres opciones por campo significan un catálogo inicial de 18 opciones conceptuales, no 729 ilustraciones independientes. El motor combina recursos compatibles. El número de combinaciones teóricas es \\(3^6=729\\), pero no es necesario producir 729 imágenes finales de antemano.

### 2.2 Las seis poses

Se propone empezar con seis poses estáticas reutilizables:

1. Saludo.
2. Alegría.
3. Enfado.
4. Tristeza.
5. Sorpresa.
6. Sueño o descanso.

La diseñadora deberá producir las piezas y las poses siguiendo una guía de proporciones, anclajes y orden de capas. La consistencia no puede depender únicamente de instrucciones de texto a una IA.

## 3. Decisión arquitectónica recomendada

Se recomienda conservar Python, Flet, Django y MySQL, con una distinción importante: Flet será la interfaz del prototipo web y Django REST Framework será la API del sistema.

No se recomienda crear dos backends, repartir la lógica entre Flet y Django, ni introducir microservicios o infraestructura compleja.

### 3.1 Arquitectura lógica

Capa 1 — Interfaz Flet

Editor · Selector de poses · Hub · Login · Descargas

Capa 2 — Django REST Framework

API REST · Validación · Autorización · Reglas de negocio · Tareas

MySQL

Usuarios y metadatos

Almacenamiento de archivos

PNG, referencias y recursos gráficos

Capa 3 — Motor de generación

Pillow · asyncio · procesos trabajadores · adaptador de IA

### 3.2 Responsabilidad de cada tecnología

| Tecnología                           | Responsabilidad                                       |
| ------------------------------------ | ----------------------------------------------------- |
| Python                               | Lenguaje principal y lógica del motor gráfico         |
| Flet                                 | Interfaz web móvil y controles del editor             |
| Django                               | Backend, modelos, autenticación y reglas de negocio   |
| Django REST Framework                | API consumida por la interfaz                         |
| MySQL                                | Persistencia relacional                               |
| Pillow                               | Composición, transformación y exportación de imágenes |
| `asyncio`                            | Coordinación asíncrona de operaciones de E/S          |
| `concurrent.futures`                 | Ejecución en hilos o procesos, según el tipo de tarea |
| Servicio de IA o modelo preentrenado | Transformación de fotografías                         |
| Git y repositorio compartido         | Integración, revisión y trazabilidad del desarrollo   |

La propuesta se apoya en librerías conocidas y evita una cola de mensajes o un servidor de tareas independiente durante la primera versión.

### 3.3 Condiciones técnicas que deben verificarse en la primera semana

Antes de desarrollar todas las pantallas, se debe validar:

- Que la versión elegida de Flet permita servir el prototipo web móvil como se espera.
- Que el cliente Flet pueda comunicarse correctamente con la API de Django.
- Que la autenticación elegida funcione con el cliente y con las peticiones de descarga.
- Que Pillow pueda componer los recursos gráficos en el formato requerido.
- Que el método de IA elegido permita ejecutar una prueba real sin pago.
- Que la herramienta de desarrollo y las versiones de Python sean compatibles.

El equipo deberá fijar versiones exactas en los archivos de dependencias una vez comprobadas. No conviene utilizar versiones flotantes ni actualizar dependencias a mitad del proyecto sin una razón concreta.

## 4. Diseño funcional y navegación

La aplicación debe sentirse como un juego de vestir personajes, no como un formulario administrativo. La interfaz puede inspirarse en la accesibilidad de los juegos de personalización y en la expresividad de los stickers, sin copiar sus recursos gráficos ni sus interfaces exactas.

### 4.1 Mapa de navegación

\#chatgpt-mermaid-\_r_1c6\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;font-size:16px;fill:rgb(13, 13, 13);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_1c6\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_1c6\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_1c6\_ .error-icon{fill:rgb(243, 243, 243);}#chatgpt-mermaid-\_r_1c6\_ .error-text{fill:rgb(13, 13, 13);stroke:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1c6\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_1c6\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_1c6\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_1c6\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_1c6\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_1c6\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_1c6\_ .marker{fill:rgb(143, 143, 143);stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_1c6\_ .marker.cross{stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_1c6\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;font-size:16px;}#chatgpt-mermaid-\_r_1c6\_ p{margin:0;}#chatgpt-mermaid-\_r_1c6\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;color:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1c6\_ .cluster-label text{fill:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1c6\_ .cluster-label span{color:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1c6\_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-\_r_1c6\_ .label text,#chatgpt-mermaid-\_r_1c6\_ span{fill:rgb(13, 13, 13);color:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1c6\_ .node rect,#chatgpt-mermaid-\_r_1c6\_ .node circle,#chatgpt-mermaid-\_r_1c6\_ .node ellipse,#chatgpt-mermaid-\_r_1c6\_ .node polygon,#chatgpt-mermaid-\_r_1c6\_ .node path{fill:rgb(222, 234, 251);stroke:rgb(83, 154, 248);stroke-width:1px;}#chatgpt-mermaid-\_r_1c6\_ .rough-node .label text,#chatgpt-mermaid-\_r_1c6\_ .node .label text,#chatgpt-mermaid-\_r_1c6\_ .image-shape .label,#chatgpt-mermaid-\_r_1c6\_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-\_r_1c6\_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-\_r_1c6\_ .rough-node .label,#chatgpt-mermaid-\_r_1c6\_ .node .label,#chatgpt-mermaid-\_r_1c6\_ .image-shape .label,#chatgpt-mermaid-\_r_1c6\_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-\_r_1c6\_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-\_r_1c6\_ .root .anchor path{fill:rgb(143, 143, 143)!important;stroke-width:0;stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_1c6\_ .arrowheadPath{fill:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_1c6\_ .edgePath .path{stroke:rgb(143, 143, 143);stroke-width:1px;}#chatgpt-mermaid-\_r_1c6\_ .flowchart-link{stroke:rgb(143, 143, 143);fill:none;}#chatgpt-mermaid-\_r_1c6\_ .edgeLabel{background-color:rgb(252, 252, 252);text-align:center;}#chatgpt-mermaid-\_r_1c6\_ .edgeLabel p{background-color:rgb(252, 252, 252);}#chatgpt-mermaid-\_r_1c6\_ .edgeLabel rect{opacity:0.5;background-color:rgb(252, 252, 252);fill:rgb(252, 252, 252);}#chatgpt-mermaid-\_r_1c6\_ .labelBkg{background-color:rgba(252, 252, 252, 0.5);}#chatgpt-mermaid-\_r_1c6\_ .cluster rect{fill:rgb(243, 243, 243);stroke:rgba(0, 0, 0, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_1c6\_ .cluster text{fill:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1c6\_ .cluster span{color:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1c6\_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;font-size:12px;background:rgb(243, 243, 243);border:1px solid rgba(0, 0, 0, 0.1);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-\_r_1c6\_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1c6\_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-\_r_1c6\_ .icon-shape,#chatgpt-mermaid-\_r_1c6\_ .image-shape{background-color:rgb(252, 252, 252);text-align:center;}#chatgpt-mermaid-\_r_1c6\_ .icon-shape p,#chatgpt-mermaid-\_r_1c6\_ .image-shape p{background-color:rgb(252, 252, 252);padding:2px;}#chatgpt-mermaid-\_r_1c6\_ .icon-shape .label rect,#chatgpt-mermaid-\_r_1c6\_ .image-shape .label rect{opacity:0.5;background-color:rgb(252, 252, 252);fill:rgb(252, 252, 252);}#chatgpt-mermaid-\_r_1c6\_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-\_r_1c6\_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-\_r_1c6\_ .node .neo-node{stroke:rgb(83, 154, 248);}#chatgpt-mermaid-\_r_1c6\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_1c6\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_1c6\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_1c6\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1c6\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_1c6\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_1c6\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_1c6\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1c6\_ [data-look="neo"].node .neo-line path{stroke:rgb(83, 154, 248);filter:none;}#chatgpt-mermaid-\_r_1c6\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_1c6\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1c6\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_1c6\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_1c6\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1c6\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_1c6\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1c6\_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(0, 79, 153);}#chatgpt-mermaid-\_r_1c6\_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(0, 79, 153);}#chatgpt-mermaid-\_r_1c6\_ .node tspan[font-weight="normal"],#chatgpt-mermaid-\_r_1c6\_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-\_r_1c6\_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(245, 250, 255);stroke:rgb(206, 219, 229);stroke-width:1px;}#chatgpt-mermaid-\_r_1c6\_ .node rect,#chatgpt-mermaid-\_r_1c6\_ .node circle,#chatgpt-mermaid-\_r_1c6\_ .node ellipse,#chatgpt-mermaid-\_r_1c6\_ .node polygon,#chatgpt-mermaid-\_r_1c6\_ .node path{fill:rgb(229, 243, 255);stroke:rgba(0, 0, 0, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_1c6\_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-\_r_1c6\_ .node.mermaid-decision .label-container{fill:rgb(245, 250, 255);stroke:rgb(206, 219, 229);stroke-dasharray:2px,2px;}#chatgpt-mermaid-\_r_1c6\_ .edgePaths .flowchart-link{stroke:rgb(143, 143, 143);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-\_r_1c6\_ .marker{fill:rgb(143, 143, 143);stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_1c6\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;}InicioExplorar hubCrear gatoMis gatosIniciar sesión / RegistrarseElegir métodoPersonalización manualCrear desde fotografía con IARevisar resultadoPrevisualizar personajeGenerar 6 stickersVista previa del paqueteDescargar PNGGuardar paqueteVer personaje publicadoCopiar personajeCuenta registradaPublicar creaciónMis publicaciones

### 4.2 Pantallas mínimas

| Pantalla                    | Elementos esenciales                                      | Criterio de finalización                             |
| --------------------------- | --------------------------------------------------------- | ---------------------------------------------------- |
| Inicio                      | Acceso al editor y al hub                                 | Permite iniciar los flujos principales               |
| Editor                      | Vista del gato, seis selectores y controles de navegación | Las seis categorías actualizan la apariencia         |
| Importación de fotografía   | Selección de archivo, vista previa y envío a IA           | Valida formato, tamaño y errores                     |
| Revisión de IA              | Imagen generada y opciones para continuar o reintentar    | El resultado puede pasar al flujo de creación        |
| Generador                   | Seis poses, indicador de progreso y estado                | Produce seis imágenes válidas                        |
| Paquete                     | Vista previa, descarga y opción de guardar                | Se descargan los archivos esperados                  |
| Registro e inicio de sesión | Formularios y validación                                  | Se crea una sesión autenticada                       |
| Hub                         | Galería de creaciones públicas                            | Permite abrir una creación y copiar su configuración |
| Publicación                 | Nombre, descripción y visibilidad                         | Una creación se publica y queda disponible en el hub |
| Mis gatos                   | Lista de personajes propios                               | Permite abrir, editar y eliminar creaciones propias  |

### 4.3 Reglas de acceso

Invitado

- Puede crear hasta tres gatos en el dispositivo o sesión local.
- Puede personalizar y generar paquetes.
- Puede descargar los PNG.
- Puede copiar personajes públicos.
- No puede publicar en el hub.
- Sus datos locales pueden perderse al borrar los datos del navegador. Esta limitación debe explicarse.

Usuario registrado

- Puede crear y guardar hasta tres gatos en el plan gratuito.
- Puede publicar y explorar creaciones públicas.
- Puede copiar una creación a su propio editor sin modificar el original.
- Puede gestionar sus publicaciones y sus gatos.
- No puede editar ni eliminar las creaciones de otro usuario.

Premium simulado

El MVP no debe tener cobros reales. El catálogo premium puede representarse con opciones bloqueadas, un indicador visual y una simulación controlada para la demostración.

La restricción de tres gatos deberá comprobarse en el backend para los usuarios registrados. La interfaz por sí sola no constituye un mecanismo de control. En el modo invitado, se puede utilizar almacenamiento local, pero no debe presentarse como una protección contra la manipulación.

## 5. Motor gráfico 2D por capas

Esta es la parte central del producto. La aplicación no debería almacenar una ilustración diferente para cada combinación. Debe almacenar una configuración del personaje y reconstruir su apariencia usando recursos gráficos.

### 5.1 Estructura conceptual del personaje

Un personaje se define mediante un documento de configuración semejante al siguiente:

```
{
  "schema_version": 1,
  "fur": {
    "pattern": "tabby",
    "base_color": "#F2A15A",
    "secondary_color": "#FFF0D8"
  },
  "eyes": {
    "style": "round",
    "color": "#4DAD72"
  },
  "hair": {
    "style": "short_fringe",
    "color": "#684632"
  },
  "top": "hoodie",
  "bottom": "shorts",
  "accessory": "bow"
}
```

Este ejemplo es ilustrativo: las claves definitivas deben coincidir con los recursos que produzca la diseñadora.

El backend validará los identificadores de los recursos contra el catálogo disponible. No debe aceptar nombres de archivos arbitrarios enviados por el cliente.

### 5.2 Organización de los recursos gráficos

Se recomienda una estructura como esta:

```
assets/
├── characters/
│   ├── base/
│   ├── fur/
│   ├── eyes/
│   ├── hair/
│   ├── tops/
│   ├── bottoms/
│   └── accessories/
├── poses/
│   ├── greeting/
│   ├── happy/
│   ├── angry/
│   ├── sad/
│   ├── surprised/
│   └── sleepy/
├── ui/
└── catalog.json
```

La estructura exacta de las carpetas puede cambiar según el formato de las ilustraciones. Lo importante es que cada recurso tenga un identificador estable y metadatos que indiquen:

- Categoría y variante.
- Orden de composición.
- Anclaje y posición.
- Compatibilidad con otras piezas.
- Paleta o tintado permitido.
- Licencia y autoría del recurso.

### 5.3 Orden de composición

El orden debe ser explícito. Un orden inicial posible:

1. Cuerpo y cola.
2. Pelaje y marcas.
3. Parte inferior.
4. Parte superior.
5. Cabello posterior.
6. Cabeza y rasgos faciales.
7. Cabello frontal.
8. Accesorios.
9. Elementos gráficos del sticker.

El orden definitivo dependerá de las ilustraciones. Si todas las prendas están diseñadas como capas completas, habrá que evitar duplicar partes del cuerpo o crear huecos entre piezas.

### 5.4 Contrato entre diseño y desarrollo

La diseñadora no debería entregar imágenes aisladas sin especificaciones. El equipo necesita acordar desde la primera semana:

- Un lienzo y una resolución base comunes.
- El centro de referencia y las coordenadas de cada capa.
- Un sistema coherente de nombres de archivos.
- Una convención de transparencia.
- Reglas de superposición.
- Una lista de recursos obligatorios para el primer paquete.
- Una hoja de control de recursos aprobados y pendientes.

La primera entrega gráfica debe incluir un personaje completo que pueda componerse técnicamente. Es preferible tener un gato completo con pocas opciones que seis categorías incompletas.

### 5.5 Generación de stickers

El motor recibirá una configuración válida del personaje y un identificador de pose. Para cada pose:

1. Carga las capas necesarias.
2. Comprueba que los recursos existan.
3. Compone las imágenes en el orden definido.
4. Aplica colores cuando corresponda.
5. Ajusta el resultado al lienzo final.
6. Conserva el canal alfa.
7. Guarda el PNG.
8. Verifica dimensiones, transparencia y existencia del archivo.

La función principal debería ser determinista: la misma configuración y la misma versión de los recursos deben producir el mismo resultado, salvo que se introduzca aleatoriedad deliberadamente.

### 5.6 Especificación de exportación

Para el prototipo se recomienda:

- Formato: PNG RGBA.
- Fondo: transparente.
- Dimensión inicial de trabajo: 512 × 512 píxeles.
- Perfil de color: sRGB cuando sea posible.
- Nombre de archivo: identificador del paquete, pose y versión.
- Validación: seis archivos válidos por paquete completado.

Los 512 × 512 píxeles son una decisión de trabajo para la demostración, no una afirmación de que ese tamaño sea suficiente para cualquier integración futura. Los requisitos específicos de WhatsApp deberán revisarse si más adelante se implementa la importación directa de paquetes.

## 6. Arquitectura de inteligencia artificial

La IA debe integrarse como un subsistema independiente. No debe convertirse en un requisito para abrir el editor, personalizar un gato o generar stickers desde recursos 2D.

Hay una diferencia importante entre crear un personaje original y transformar una fotografía de una persona o mascota en una representación felina. El segundo caso es más difícil porque exige preservar rasgos reconocibles, controlar el estilo y obtener resultados utilizables como piezas gráficas.

### 6.1 Alternativas que se deben evaluar

[PNG Cute cartoon orange kitten | Premium PNG  - rawpixel](https://images.openai.com/static-rsc-4/Lzwj8A7QToCaaLZkbueiYQakv_NObJkTIBuYR8fOEBN60oHXyuZZzUrOvYKvzDNAr6htagsPbK75ejAZzXM1ypoSTcP88TJ9wpaltFCDI81CHle2hVviTDmDpGmO4mM9fftUFVYi87QvFBXtmFDm5lVULkMOe5-GHcAXuUn5CIQ?purpose=inline)

Alternativa A — Modelo generativo mediante servicio externo

Se envía una imagen de referencia y una instrucción para obtener un gato chibi. El resultado se muestra al usuario y puede servir como referencia para personalizar el personaje.

Ventajas: menos infraestructura local. Riesgos: límites gratuitos variables, claves API, disponibilidad, privacidad y consistencia entre resultados.

[Template Detail - WowAI.pet](https://images.openai.com/static-rsc-4/jC9JCDW-mj2Ia5YrxGng9sGNn3BlLIKkj1jol5RECreVLCQzBneoU3gcZRVY1PHfOuVszgNkoKUmcLug9EENiT7LLLKUnRVKdZGowbhOJh9lVvAp460VRfVpimYEVMauYoUkdjuulZ-DvJd-TOiAgCu5ngKRQ7ZulpBWpNWwBs4?purpose=inline)

Alternativa B — Modelo preentrenado local

El grupo ejecuta un modelo generativo ya entrenado y lo invoca desde Python.

Ventajas: mayor control del entorno y sin cobro por petición a un proveedor. Riesgos: requisitos de GPU, memoria, instalación, tiempo de inferencia y calidad variable.

[Cat OC Maker: Create Original Cat Characters](https://images.openai.com/static-rsc-4/_yxPSnurchC56oz95mcOEzQ3PYEoObqulMLEkrq2uuJNuVSIyya3oW0mBkTqvMWBdPg1KJNh64PkAilxg-hfzUj43Hk_ouvGxFWPJIGujYZhA7wI04BBP4I_t5Ckn4R3LfYHMT1VlPqKVqug57QIYQKyWurcXtncxvYRbLNkqwE?purpose=inline)

Alternativa C — IA asistida por catálogo

La IA propone atributos o variantes de un gato y el motor 2D compone la imagen con recursos de la marca.

Ventajas: resultados visualmente consistentes y menor dependencia de generación gráfica completa. Riesgos: el parecido con la fotografía será limitado.

Recomendación para el MVP: diseñar una arquitectura que admita las tres alternativas, pero implementar inicialmente una sola. Si el equipo no dispone de GPU ni de una API gratuita confirmada, la alternativa C es la más segura para terminar a tiempo, aunque no satisface por sí sola una transformación fotorrealista o de gran parecido. Para cumplir el requisito de IA con rigor, deberá existir una inferencia real de un modelo, no solo una selección aleatoria de opciones.

### 6.2 Flujo propuesto

\#chatgpt-mermaid-\_r_1di\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;font-size:16px;fill:rgb(13, 13, 13);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_1di\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_1di\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_1di\_ .error-icon{fill:rgb(243, 243, 243);}#chatgpt-mermaid-\_r_1di\_ .error-text{fill:rgb(13, 13, 13);stroke:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1di\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_1di\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_1di\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_1di\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_1di\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_1di\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_1di\_ .marker{fill:rgb(143, 143, 143);stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_1di\_ .marker.cross{stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_1di\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;font-size:16px;}#chatgpt-mermaid-\_r_1di\_ p{margin:0;}#chatgpt-mermaid-\_r_1di\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;color:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1di\_ .cluster-label text{fill:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1di\_ .cluster-label span{color:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1di\_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-\_r_1di\_ .label text,#chatgpt-mermaid-\_r_1di\_ span{fill:rgb(13, 13, 13);color:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1di\_ .node rect,#chatgpt-mermaid-\_r_1di\_ .node circle,#chatgpt-mermaid-\_r_1di\_ .node ellipse,#chatgpt-mermaid-\_r_1di\_ .node polygon,#chatgpt-mermaid-\_r_1di\_ .node path{fill:rgb(222, 234, 251);stroke:rgb(83, 154, 248);stroke-width:1px;}#chatgpt-mermaid-\_r_1di\_ .rough-node .label text,#chatgpt-mermaid-\_r_1di\_ .node .label text,#chatgpt-mermaid-\_r_1di\_ .image-shape .label,#chatgpt-mermaid-\_r_1di\_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-\_r_1di\_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-\_r_1di\_ .rough-node .label,#chatgpt-mermaid-\_r_1di\_ .node .label,#chatgpt-mermaid-\_r_1di\_ .image-shape .label,#chatgpt-mermaid-\_r_1di\_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-\_r_1di\_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-\_r_1di\_ .root .anchor path{fill:rgb(143, 143, 143)!important;stroke-width:0;stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_1di\_ .arrowheadPath{fill:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_1di\_ .edgePath .path{stroke:rgb(143, 143, 143);stroke-width:1px;}#chatgpt-mermaid-\_r_1di\_ .flowchart-link{stroke:rgb(143, 143, 143);fill:none;}#chatgpt-mermaid-\_r_1di\_ .edgeLabel{background-color:rgb(252, 252, 252);text-align:center;}#chatgpt-mermaid-\_r_1di\_ .edgeLabel p{background-color:rgb(252, 252, 252);}#chatgpt-mermaid-\_r_1di\_ .edgeLabel rect{opacity:0.5;background-color:rgb(252, 252, 252);fill:rgb(252, 252, 252);}#chatgpt-mermaid-\_r_1di\_ .labelBkg{background-color:rgba(252, 252, 252, 0.5);}#chatgpt-mermaid-\_r_1di\_ .cluster rect{fill:rgb(243, 243, 243);stroke:rgba(0, 0, 0, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_1di\_ .cluster text{fill:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1di\_ .cluster span{color:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1di\_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;font-size:12px;background:rgb(243, 243, 243);border:1px solid rgba(0, 0, 0, 0.1);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-\_r_1di\_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1di\_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-\_r_1di\_ .icon-shape,#chatgpt-mermaid-\_r_1di\_ .image-shape{background-color:rgb(252, 252, 252);text-align:center;}#chatgpt-mermaid-\_r_1di\_ .icon-shape p,#chatgpt-mermaid-\_r_1di\_ .image-shape p{background-color:rgb(252, 252, 252);padding:2px;}#chatgpt-mermaid-\_r_1di\_ .icon-shape .label rect,#chatgpt-mermaid-\_r_1di\_ .image-shape .label rect{opacity:0.5;background-color:rgb(252, 252, 252);fill:rgb(252, 252, 252);}#chatgpt-mermaid-\_r_1di\_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-\_r_1di\_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-\_r_1di\_ .node .neo-node{stroke:rgb(83, 154, 248);}#chatgpt-mermaid-\_r_1di\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_1di\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_1di\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_1di\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1di\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_1di\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_1di\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_1di\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1di\_ [data-look="neo"].node .neo-line path{stroke:rgb(83, 154, 248);filter:none;}#chatgpt-mermaid-\_r_1di\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_1di\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1di\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_1di\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_1di\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1di\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_1di\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1di\_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(0, 79, 153);}#chatgpt-mermaid-\_r_1di\_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(0, 79, 153);}#chatgpt-mermaid-\_r_1di\_ .node tspan[font-weight="normal"],#chatgpt-mermaid-\_r_1di\_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-\_r_1di\_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(245, 250, 255);stroke:rgb(206, 219, 229);stroke-width:1px;}#chatgpt-mermaid-\_r_1di\_ .node rect,#chatgpt-mermaid-\_r_1di\_ .node circle,#chatgpt-mermaid-\_r_1di\_ .node ellipse,#chatgpt-mermaid-\_r_1di\_ .node polygon,#chatgpt-mermaid-\_r_1di\_ .node path{fill:rgb(229, 243, 255);stroke:rgba(0, 0, 0, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_1di\_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-\_r_1di\_ .node.mermaid-decision .label-container{fill:rgb(245, 250, 255);stroke:rgb(206, 219, 229);stroke-dasharray:2px,2px;}#chatgpt-mermaid-\_r_1di\_ .edgePaths .flowchart-link{stroke:rgb(143, 143, 143);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-\_r_1di\_ .marker{fill:rgb(143, 143, 143);stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_1di\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;}Usuario selecciona fotoValidar formato y tamañoArchivo válido?Mostrar errorCrear trabajo de IAEjecutar modeloResultado válido?Registrar fallo y permitirreintentoGuardar resultado temporalMostrar previsualizaciónUsuario acepta resultadoCrear configuración editableContinuar en el editor 2DNoSíNoSí

El modelo puede generar una imagen de referencia que el usuario acepte y luego utilice como guía para seleccionar rasgos manualmente. No se debe prometer que una imagen generada se convertirá automáticamente en capas editables: esa transformación exige un proceso adicional de segmentación y reconstrucción que queda fuera del MVP.

### 6.3 Requisitos de seguridad y privacidad

- Aceptar únicamente formatos de imagen permitidos.
- Limitar el tamaño de los archivos subidos.
- No almacenar fotografías originales más tiempo del necesario.
- Evitar guardar imágenes en directorios públicos.
- No registrar imágenes, tokens o datos sensibles en los logs.
- Eliminar archivos temporales tras el procesamiento o la expiración definida.
- Documentar si el servicio externo recibe fotografías.
- Obtener consentimiento para el procesamiento de imágenes.
- Si se admiten fotografías de menores, no recopilar ni publicar esas imágenes sin una política específica y medidas de protección adecuadas.

La clave de cualquier proveedor de IA debe permanecer en el backend o en variables de entorno locales, nunca en el código de la interfaz ni en el repositorio.

### 6.4 Criterio para elegir el modelo

Durante los primeros tres días, realizar una prueba comparativa breve y documentar:

1. ¿Se puede ejecutar sin coste?
2. ¿Acepta imágenes como entrada?
3. ¿Produce un gato ilustrado reconocible?
4. ¿Se puede utilizar legalmente bajo sus condiciones?
5. ¿Cuál es el tiempo de inferencia?
6. ¿Qué ocurre cuando falla?
7. ¿Puede ejecutarse en los equipos disponibles?

La decisión se registrará en `docs/decisions/`. Si la prueba de IA consume más tiempo del presupuestado, se congela el alcance de esta función y se continúa con el editor manual.

## 7. Concurrencia, multiprocesamiento y paralelismo

Esta sección debe diseñarse en función de los criterios de evaluación del profesor. Como la rúbrica aún no está disponible, la estrategia será demostrar cada concepto por separado y mantener evidencias reproducibles.

No se deben confundir tres conceptos:

- Concurrencia: organizar varias tareas para que progresen durante intervalos solapados.
- Paralelismo: ejecutar operaciones realmente al mismo tiempo, por ejemplo, en distintos núcleos de CPU.
- Multiprocesamiento: utilizar varios procesos independientes, lo que puede permitir paralelismo y aislamiento de fallos.

`asyncio` facilita concurrencia cooperativa, especialmente para operaciones de E/S. No hace que el procesamiento intensivo de imágenes se ejecute en paralelo automáticamente.

### 7.1 Caso de uso A — Concurrencia con `asyncio`

Al generar un paquete, la aplicación puede necesitar consultar varios recursos o solicitar varias operaciones de red.

Se puede demostrar concurrencia ejecutando varias solicitudes de E/S asíncronas independientes, con límites y manejo de errores.

Ejemplo ilustrativo:

```
import asyncioasync def consultar_recurso(nombre):    await asyncio.sleep(1)    return f"Recurso procesado: {nombre}"async def main():    resultados = await asyncio.gather(        consultar_recurso("pose_1"),        consultar_recurso("pose_2"),        consultar_recurso("pose_3"),    )    print(resultados)asyncio.run(main())
```

Este ejemplo demuestra tareas concurrentes simulando espera de E/S; no es todavía una integración real con el producto. En la implementación, la espera debe sustituirse por operaciones reales, por ejemplo, peticiones HTTP asíncronas al servicio de IA.

La evidencia incluirá el tiempo total de ejecución, el comportamiento cuando una petición falla y una prueba de que la interfaz no queda bloqueada esperando el resultado.

### 7.2 Caso de uso B — Multiprocesamiento

La composición o transformación de imágenes puede ser una tarea intensiva en CPU. El equipo puede ejecutar trabajos independientes en un grupo de procesos.

Ejemplo de estructura:

```
from concurrent.futures import ProcessPoolExecutordef procesar_pose(datos):    # La función real compondrá y exportará una pose.    return datos["pose_id"]def generar_paquete(trabajos):    with ProcessPoolExecutor(max_workers=3) as pool:        return list(pool.map(procesar_pose, trabajos))
```

Este código es ilustrativo; debe adaptarse al motor gráfico real. Las funciones ejecutadas en procesos deben ser importables, recibir argumentos serializables y no depender de objetos de interfaz, conexiones de base de datos abiertas o estado compartido no controlado.

En Windows y macOS es especialmente importante utilizar el punto de entrada adecuado para crear procesos y evitar que la importación del módulo vuelva a iniciar el programa.

### 7.3 Caso de uso C — Paralelismo medible

Para demostrar paralelismo de manera convincente, se procesará un conjunto fijo de imágenes en dos modalidades:

1. Ejecución secuencial.
2. Ejecución con un grupo de procesos.

Se utilizará el mismo conjunto de recursos y la misma configuración. Se registrarán tiempo de inicio, tiempo de finalización, cantidad de imágenes, errores y número de trabajadores.

La aceleración se calcula como:

\\[ S = \frac{T\_{\text{secuencial}}}{T\_{\text{paralelo}}} \\]

Si la ejecución secuencial tarda 4 segundos y la paralela 2,5 segundos, la aceleración observada sería \\(1{,}6\\). No se debe asumir que la ejecución paralela siempre será más rápida: para trabajos pequeños, el coste de crear procesos y serializar datos puede superar el beneficio.

### 7.4 Diseño integrado

Solicitud de generación

Validar configuración y crear registro de trabajo

Coordinador de tareas

Estado, concurrencia limitada y seguimiento

E/S asíncrona

Solicitudes a IA, operaciones de red

Procesos trabajadores

Composición y exportación de imágenes

Resultado

Seis PNG · estado completado o fallido · métricas de ejecución

### 7.5 Qué evitar

- Crear un proceso por cada tarea sin límite.
- Lanzar procesos desde una petición web y bloquear la respuesta hasta terminar.
- Usar `asyncio` para envolver una función intensiva de CPU sin delegar el trabajo.
- Abrir una conexión MySQL antes de crear procesos y reutilizarla en todos.
- Utilizar una sola prueba artificial como única evidencia de los requisitos académicos.
- Medir solamente el tiempo total sin registrar qué se está comparando.

### 7.6 Estrategia de implementación en cinco semanas

Primero se implementará el motor secuencial correcto. Después se añadirán las pruebas de concurrencia y paralelismo como módulos claramente separados. Solo cuando estén verificadas se integrarán con la interfaz.

Si el profesor exige tecnologías concretas, como `threading`, `multiprocessing`, `asyncio`, `ProcessPoolExecutor` o `ThreadPoolExecutor`, esa decisión deberá ajustarse a la rúbrica. No conviene añadir todos estos mecanismos sin necesidad antes de conocer los requisitos.

## 8. Modelo de datos de MySQL

La base de datos debe representar usuarios, configuraciones de personajes, paquetes de stickers, publicaciones y trabajos de generación. No es necesario crear tablas para cada una de las 729 combinaciones posibles.

### 8.1 Entidades principales

| Entidad           | Propósito                    | Campos principales                                                                              |
| ----------------- | ---------------------------- | ----------------------------------------------------------------------------------------------- |
| `users`           | Usuarios registrados         | `id`, `username`, `email`, `password`, `created_at`, `updated_at`                               |
| `cats`            | Personajes guardados         | `id`, `user_id`, `name`, `configuration`, `created_at`, `updated_at`                            |
| `sticker_packs`   | Paquetes de stickers         | `id`, `cat_id`, `status`, `created_at`, `completed_at`                                          |
| `stickers`        | Imágenes individuales        | `id`, `pack_id`, `pose_id`, `file_path`, `status`                                               |
| `poses`           | Catálogo de poses            | `id`, `code`, `name`, `asset_path`, `is_active`                                                 |
| `catalog_options` | Opciones del editor          | `id`, `category`, `code`, `asset_path`, `is_premium`, `is_active`                               |
| `publications`    | Creaciones compartidas       | `id`, `cat_id`, `user_id`, `title`, `description`, `visibility`, `created_at`                   |
| `generation_jobs` | Trabajos de IA o composición | `id`, `user_id`, `job_type`, `status`, `created_at`, `started_at`, `completed_at`, `error_code` |

Los nombres son una propuesta inicial y deberán normalizarse al fijar el esquema definitivo.

### 8.2 Relaciones

\#chatgpt-mermaid-\_r_1f0\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;font-size:16px;fill:rgb(13, 13, 13);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_1f0\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_1f0\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_1f0\_ .error-icon{fill:rgb(243, 243, 243);}#chatgpt-mermaid-\_r_1f0\_ .error-text{fill:rgb(13, 13, 13);stroke:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1f0\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_1f0\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_1f0\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_1f0\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_1f0\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_1f0\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_1f0\_ .marker{fill:rgb(143, 143, 143);stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_1f0\_ .marker.cross{stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_1f0\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;font-size:16px;}#chatgpt-mermaid-\_r_1f0\_ p{margin:0;}#chatgpt-mermaid-\_r_1f0\_ .entityBox{fill:rgb(222, 234, 251);stroke:rgb(83, 154, 248);}#chatgpt-mermaid-\_r_1f0\_ .relationshipLabelBox{fill:rgb(243, 243, 243);opacity:0.7;background-color:rgb(243, 243, 243);}#chatgpt-mermaid-\_r_1f0\_ .relationshipLabelBox rect{opacity:0.5;}#chatgpt-mermaid-\_r_1f0\_ .labelBkg{background-color:rgba(243, 243, 243, 0.5);}#chatgpt-mermaid-\_r_1f0\_ .edgeLabel{background-color:rgb(252, 252, 252);}#chatgpt-mermaid-\_r_1f0\_ .edgeLabel .label rect{fill:rgb(252, 252, 252);}#chatgpt-mermaid-\_r_1f0\_ .edgeLabel .label text{fill:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1f0\_ .edgeLabel .label{fill:rgb(83, 154, 248);font-size:14px;}#chatgpt-mermaid-\_r_1f0\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;color:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1f0\_ .edge-pattern-dashed{stroke-dasharray:8,8;}#chatgpt-mermaid-\_r_1f0\_ .node rect,#chatgpt-mermaid-\_r_1f0\_ .node circle,#chatgpt-mermaid-\_r_1f0\_ .node ellipse,#chatgpt-mermaid-\_r_1f0\_ .node polygon{fill:rgb(222, 234, 251);stroke:rgb(83, 154, 248);stroke-width:1px;}#chatgpt-mermaid-\_r_1f0\_ .relationshipLine{stroke:rgb(143, 143, 143);stroke-width:1px;fill:none;}#chatgpt-mermaid-\_r_1f0\_ .marker{fill:none!important;stroke:rgb(143, 143, 143)!important;stroke-width:1;}#chatgpt-mermaid-\_r_1f0\_ [data-look=neo].labelBkg{background-color:rgba(243, 243, 243, 0.5);}#chatgpt-mermaid-\_r_1f0\_ .node .neo-node{stroke:rgb(83, 154, 248);}#chatgpt-mermaid-\_r_1f0\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_1f0\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_1f0\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_1f0\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1f0\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_1f0\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_1f0\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_1f0\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1f0\_ [data-look="neo"].node .neo-line path{stroke:rgb(83, 154, 248);filter:none;}#chatgpt-mermaid-\_r_1f0\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_1f0\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1f0\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_1f0\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_1f0\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1f0\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_1f0\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1f0\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;}USERSCATSPUBLICATIONSSTICKER_PACKSSTICKERSPOSESGENERATION_JOBScreatespublishesgeneratescontainsdefinesappears_inrequests

### 8.3 Decisiones de modelado

Configuración del gato. Para el MVP, se puede almacenar como JSON validado en una columna de MySQL. Esto facilita guardar combinaciones de atributos sin crear numerosas tablas. Los recursos válidos seguirán definidos por el catálogo.

Archivos. Los PNG y las fotografías no deben almacenarse como cadenas Base64 en las tablas. La base de datos guardará rutas relativas o identificadores de almacenamiento; los archivos vivirán en el sistema de archivos local durante la demostración.

Contraseñas. Deben gestionarse mediante el sistema de autenticación de Django, que incluye hashing y mecanismos de validación. Nunca se almacenarán en texto plano.

Invitados. No necesitan una fila en `users` si sus gatos se almacenan en el navegador y no existe sincronización entre dispositivos. Si más adelante se requiere persistencia en el servidor, se puede diseñar una identidad anónima temporal.

Copias. Copiar una creación pública debe crear un nuevo gato propiedad del usuario actual. No debe modificar la creación original ni su configuración.

Publicaciones. La publicación y el personaje son entidades distintas. El usuario puede dejar de publicar un gato sin que eso obligue a borrar el gato de su colección.

Estados. Los trabajos deben tener estados definidos, por ejemplo `pending`, `running`, `completed` y `failed`. Las transiciones deben validarse en el backend.

### 8.4 Restricciones e índices

Como mínimo:

- Unicidad de `username` y `email`.
- Claves foráneas con políticas explícitas de eliminación.
- Índices para `cats.user_id`, `publications.user_id`, `publications.visibility` y `stickers.pack_id`.
- Validación del límite de gatos mediante una operación transaccional o mecanismo equivalente que evite dos creaciones simultáneas que excedan el límite.
- Acceso a publicaciones públicas sin permitir modificar datos de otros usuarios.
- No confiar en los identificadores enviados por el cliente para autorizar modificaciones.

### 8.5 Migraciones y estructura de Django

El esquema se administrará mediante modelos y migraciones de Django. No se recomienda crear manualmente las tablas y después intentar sincronizarlas con los modelos.

La configuración de MySQL deberá utilizar variables de entorno. Se añadirá un archivo de ejemplo con nombres de variables, pero sin credenciales reales.

## 9. Diseño de la API REST

La API debe ofrecer contratos estables entre Flet y Django. Los endpoints propuestos son conceptuales; sus nombres definitivos se registrarán en la documentación técnica.

| Método   | Endpoint                       | Propósito                           |
| -------- | ------------------------------ | ----------------------------------- |
| `POST`   | `/api/auth/register/`          | Registrar un usuario                |
| `POST`   | `/api/auth/login/`             | Iniciar sesión                      |
| `POST`   | `/api/auth/logout/`            | Cerrar sesión                       |
| `GET`    | `/api/catalog/`                | Obtener opciones disponibles        |
| `GET`    | `/api/poses/`                  | Obtener las poses                   |
| `GET`    | `/api/cats/`                   | Listar gatos propios                |
| `POST`   | `/api/cats/`                   | Crear un gato                       |
| `GET`    | `/api/cats/{id}/`              | Consultar un gato                   |
| `PATCH`  | `/api/cats/{id}/`              | Actualizar su configuración         |
| `DELETE` | `/api/cats/{id}/`              | Eliminar un gato propio             |
| `POST`   | `/api/sticker-packs/`          | Solicitar generación de un paquete  |
| `GET`    | `/api/sticker-packs/{id}/`     | Consultar estado y resultado        |
| `POST`   | `/api/ai-jobs/`                | Solicitar una transformación por IA |
| `GET`    | `/api/ai-jobs/{id}/`           | Consultar el resultado de IA        |
| `GET`    | `/api/publications/`           | Explorar el hub                     |
| `POST`   | `/api/publications/`           | Publicar una creación               |
| `POST`   | `/api/publications/{id}/copy/` | Copiar una creación pública         |

### 9.1 Comportamiento de la generación

La petición de generar un paquete debería responder con un identificador de trabajo y no esperar necesariamente a que terminen los seis stickers.

Por ejemplo, una respuesta inicial podría incluir:

```
{
  "job_id": "identificador",
  "status": "pending"
}
```

La interfaz consultará el estado mediante el endpoint correspondiente. Cuando el trabajo finalice, el backend devolverá las rutas o URL autorizadas para descargar los resultados.

Para el prototipo local, una solución sencilla de consulta periódica es suficiente. No es necesario introducir WebSockets para comunicar el progreso.

### 9.2 Gestión de errores

Los errores deben tener respuestas coherentes:

- `400`: datos inválidos.
- `401`: usuario no autenticado.
- `403`: usuario sin permisos.
- `404`: recurso inexistente.
- `409`: conflicto de estado o límite alcanzado, cuando corresponda.
- `413`: archivo demasiado grande.
- `429`: límite de solicitudes excedido.
- `500`: error interno no esperado.

La interfaz mostrará mensajes comprensibles y el backend registrará detalles técnicos sin exponer secretos al usuario.

## 10. Estructura del repositorio y documentación para agentes

La documentación no será un apéndice. Será el mecanismo para mantener coherencia entre tres desarrolladores y los agentes de programación que realicen cambios en paralelo.

Se recomienda organizar el repositorio de la siguiente manera:

```
kitchi-studio/
├── README.md
├── AGENTS.md
├── .gitignore
├── .env.example
├── docker-compose.yml              # Opcional, solo si se acuerda usarlo
├── docs/
│   ├── 00_PROJECT_OVERVIEW.md
│   ├── 01_MASTER_PLAN.md
│   ├── 02_REQUIREMENTS.md
│   ├── 03_ARCHITECTURE.md
│   ├── 04_DATA_MODEL.md
│   ├── 05_API_CONTRACTS.md
│   ├── 06_DESIGN_SYSTEM.md
│   ├── 07_AI_INTEGRATION.md
│   ├── 08_CONCURRENCY_AND_PARALLELISM.md
│   ├── 09_TEST_PLAN.md
│   ├── 10_DEVELOPMENT_CHECKLIST.md
│   ├── 11_DEMO_SCRIPT.md
│   ├── decisions/
│   │   ├── ADR-001-frontend-backend.md
│   │   ├── ADR-002-character-rendering.md
│   │   └── ADR-003-ai-strategy.md
│   └── reports/
├── frontend/
│   ├── pyproject.toml
│   ├── src/
│   └── tests/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/
│   ├── apps/
│   │   ├── accounts/
│   │   ├── catalog/
│   │   ├── cats/
│   │   ├── stickers/
│   │   ├── community/
│   │   └── ai_jobs/
│   └── tests/
├── shared/
│   └── contracts/
├── assets/
│   ├── characters/
│   ├── poses/
│   ├── ui/
│   └── catalog.json
├── storage/
│   └── .gitkeep
└── scripts/
    ├── setup_dev.py
    ├── seed_demo_data.py
    └── benchmark_generation.py
```

Esta estructura es orientativa. No es obligatorio separar cada entidad en una aplicación Django diferente si el código resultante es demasiado pequeño. Los directorios `frontend/src/` y `backend/apps/` deberán adaptarse al empaquetado real que se escoja.

### 10.1 El comando maestro para agentes

El archivo `AGENTS.md` será el punto de entrada obligatorio para cualquier agente de programación que trabaje en el repositorio.

Debe indicar:

1. Leer `docs/00_PROJECT_OVERVIEW.md`.
2. Leer `docs/01_MASTER_PLAN.md`.
3. Leer la arquitectura y los contratos relevantes antes de editar.
4. Consultar `docs/decisions/` antes de proponer una alternativa que cambie el diseño.
5. Identificar las tareas asignadas y los criterios de aceptación.
6. No modificar contratos compartidos sin coordinación.
7. No introducir dependencias sin justificar su necesidad.
8. No alterar migraciones existentes de forma destructiva.
9. Ejecutar las pruebas pertinentes.
10. Documentar archivos modificados, decisiones y limitaciones.
11. No marcar tareas como terminadas si no hay evidencia de que funcionan.

El agente debe tratar la documentación del repositorio como contexto de trabajo, no como una autorización para ignorar instrucciones de seguridad o exponer credenciales.

### 10.2 Plantilla del comando maestro

Este sería el contenido inicial recomendado para `AGENTS.md`:

# AGENTS.md — Kitchi Studio

## Contexto obligatorio

Antes de modificar el código, lee en este orden:

1. `docs/00_PROJECT_OVERVIEW.md`
2. `docs/01_MASTER_PLAN.md`
3. `docs/02_REQUIREMENTS.md`
4. `docs/03_ARCHITECTURE.md`
5. El contrato, modelo o plan de pruebas pertinente a tu tarea.
6. Las decisiones registradas en `docs/decisions/`.

## Objetivo del proyecto

Construir un MVP web móvil para crear gatos chibi mediante ilustraciones 2D por capas, generar seis stickers PNG transparentes, admitir una integración de IA y ofrecer autenticación y un hub comunitario básico.

## Reglas de desarrollo

- Respeta la arquitectura y los contratos existentes.
- No implementes funcionalidades fuera del alcance acordado sin aprobación.
- No dupliques lógica de negocio entre frontend y backend.
- La validación y autorización deben residir en el backend cuando corresponda.
- No almacenes contraseñas, tokens ni credenciales en texto plano.
- No incluyas archivos `.env`, fotografías privadas ni resultados temporales en Git.
- No cambies contratos compartidos sin informar a los responsables.
- No añadas dependencias sin explicar el motivo.
- No afirmes que una función está implementada si solo tiene una interfaz simulada.
- Mantén los cambios pequeños y enfocados en la tarea asignada.

## Procedimiento obligatorio

1. Resume el objetivo de la tarea y sus criterios de aceptación.
2. Identifica las dependencias y archivos que se modificarán.
3. Revisa si hay cambios pendientes que puedan entrar en conflicto.
4. Implementa la solución.
5. Ejecuta las pruebas relevantes.
6. Documenta las limitaciones y decisiones nuevas.
7. Informa qué archivos modificaste, qué pruebas ejecutaste y qué queda pendiente.

## Gestión de decisiones

Las decisiones que alteren la arquitectura, el esquema de datos, los contratos de API, las dependencias principales o el alcance deben registrarse en `docs/decisions/` antes de implementar cambios incompatibles.

## Criterio de finalización

Una tarea solo se considera terminada cuando satisface sus criterios de aceptación, las pruebas pertinentes pasan y la documentación afectada queda actualizada.

### 10.3 Gestión del plan con checkboxes

El archivo `docs/10_DEVELOPMENT_CHECKLIST.md` debe ser el tablero de seguimiento del proyecto. Cada tarea tendrá identificador, responsable, dependencia, estado y criterio de aceptación.

Ejemplo:

# Checklist de desarrollo — Kitchi Studio

## Semana 1 — Fundamentos

- P01 — Confirmar la rúbrica académica.
- P02 — Validar Flet, Django REST Framework y MySQL.
- P03 — Definir contratos iniciales de la API.
- P04 — Probar composición de un gato con capas.
- P05 — Evaluar una opción real de IA.
- P06 — Aprobar guía de ilustraciones y poses.
- P07 — Crear repositorio y reglas de integración.

## Semana 2 — Editor y persistencia

- P08 — Implementar catálogo de recursos.
- P09 — Implementar configuración de personajes.
- P10 — Implementar editor manual.
- P11 — Crear modelos y migraciones.
- P12 — Implementar registro e inicio de sesión.

## Semana 3 — Generación e IA

- P13 — Componer las seis poses.
- P14 — Exportar PNG con transparencia.
- P15 — Implementar seguimiento de trabajos.
- P16 — Integrar y probar el flujo de IA.
- P17 — Añadir gestión de errores y reintentos.

## Semana 4 — Hub y programación avanzada

- P18 — Implementar publicación y galería.
- P19 — Implementar copia de creaciones.
- P20 — Demostrar concurrencia.
- P21 — Demostrar multiprocesamiento.
- P22 — Ejecutar benchmark de paralelismo.
- P23 — Completar pruebas de permisos y límites.

## Semana 5 — Integración y entrega

- P24 — Ejecutar pruebas de aceptación.
- P25 — Corregir errores críticos.
- P26 — Preparar datos de demostración.
- P27 — Documentar resultados de rendimiento.
- P28 — Ensayar demostración visual y técnica.
- P29 — Verificar instalación desde un clon limpio.
- P30 — Congelar versión de entrega.

Las tareas deben tener un responsable, una fecha objetivo y un criterio de aceptación en el tablero de seguimiento. No se deben marcar como terminadas únicamente porque el código se haya escrito.

### 10.4 Decisiones arquitectónicas

Cada decisión importante debe tener un registro ADR (Architecture Decision Record). Como mínimo, incluirá:

- Contexto y problema.
- Alternativas evaluadas.
- Decisión adoptada.
- Justificación.
- Consecuencias y riesgos.
- Fecha y responsables.

Si se cambia de enfoque gráfico, de mecanismo de autenticación o de proveedor de IA, el equipo debe registrar la decisión y actualizar los documentos afectados.

### 10.5 Trabajo con agentes en paralelo

Para tres integrantes, se recomienda dividir las tareas por componentes y asignar un responsable de integración. No conviene permitir que varios agentes modifiquen simultáneamente los mismos modelos, contratos o archivos de configuración.

Reglas operativas:

- Una rama Git por funcionalidad.
- Commits pequeños y descriptivos.
- Pull request o revisión cruzada antes de integrar.
- Contratos de API acordados antes de desarrollar frontend y backend en paralelo.
- Pruebas automáticas antes de fusionar cambios.
- Un único responsable de aprobar migraciones y cambios arquitectónicos.
- Ningún agente puede sobrescribir silenciosamente cambios de otro integrante.

La documentación y los contratos compartidos son más importantes que la cantidad de agentes utilizados.

## 11. Distribución del trabajo del equipo

Con tres integrantes de desarrollo y una diseñadora, la división debe reducir las dependencias entre personas y mantener una responsabilidad clara sobre la integración.

Integrante A — Frontend e integración UX

Responsable de Flet, navegación, editor visual, estados de generación, hub y comunicación con la API.

Entregable principal: experiencia completa desde la creación del gato hasta la descarga.

Integrante B — Backend y datos

Responsable de Django REST Framework, MySQL, autenticación, modelos, permisos, API y persistencia.

Entregable principal: API documentada y funcional, con pruebas de permisos y límites.

Integrante C — Motor gráfico, IA y programación avanzada

Responsable de composición con Pillow, exportación, adaptador de IA, procesamiento de tareas y pruebas de rendimiento.

Entregable principal: generador verificable de seis PNG y evidencias académicas reproducibles.

Diseñadora gráfica — Sistema visual y recursos

Responsable de la guía visual, personajes base, catálogo de opciones, poses, accesorios, iconografía y validación de consistencia.

Entregable principal: biblioteca gráfica organizada, documentada y lista para composición.

### 11.1 La integración es responsabilidad de todos

Aunque cada integrante tenga un área principal, la revisión del código, las pruebas y la documentación son responsabilidades compartidas.

La persona responsable de integración deberá comprobar que las funcionalidades no solo funcionan de manera aislada, sino también en el flujo completo. Debe evitarse que el integrante A construya un frontend contra una API imaginaria mientras el integrante B cambia sus contratos cada día.

Por eso, los contratos iniciales se acordarán en la primera semana y se modificarán únicamente mediante coordinación y registro de decisiones.

## 12. Cronograma maestro de cinco semanas

El cronograma está diseñado para que el equipo disponga de un resultado funcional desde la primera semana y no descubra los principales riesgos técnicos al final.

Semana 1 — Validación y cimientos

Fundacional

Objetivo: eliminar las incertidumbres que podrían bloquear el MVP.

- Confirmar la rúbrica con el profesor.
- Crear repositorio, estructura documental y reglas de agentes.
- Validar Flet web móvil, Django y conexión a MySQL.
- Componer un gato con varias capas reales.
- Comparar opciones de IA con una prueba mínima.
- Aprobar contratos iniciales de API y catálogo gráfico.
- Preparar un ejemplo de benchmark de procesamiento.\
  Hito: un gato visible desde recursos 2D y una decisión fundamentada sobre IA y arquitectura.

Semana 2 — Editor y persistencia

Funcional

- Implementar navegación principal.
- Implementar selectores de las seis categorías.
- Crear modelos y migraciones.
- Implementar registro e inicio de sesión.
- Guardar y recuperar configuraciones de gatos.
- Aplicar el límite de tres gatos.\
  Hito: un usuario puede personalizar un gato, guardarlo y recuperarlo.

Semana 3 — Stickers e IA

Generación

- Implementar las seis poses.
- Componer imágenes mediante Pillow.
- Exportar PNG transparentes.
- Implementar el registro y seguimiento de trabajos.
- Integrar la IA elegida.
- Implementar errores, límites y reintentos.\
  Hito: un usuario puede generar y descargar un paquete completo.

Semana 4 — Hub y requisitos académicos

Integración

- Implementar publicación y exploración del hub.
- Implementar copia de creaciones públicas.
- Demostrar concurrencia con operaciones reales.
- Implementar multiprocesamiento para trabajos gráficos.
- Ejecutar benchmarks secuenciales y paralelos.
- Verificar permisos, límites y privacidad.\
  Hito: el flujo comunitario funciona y existen evidencias técnicas de los tres conceptos.

Semana 5 — Pruebas y entrega

Estabilización

- Ejecutar pruebas unitarias, integración y aceptación.
- Corregir errores críticos.
- Verificar que el proyecto se instala desde un clon limpio.
- Preparar datos de demostración.
- Documentar resultados de rendimiento.
- Ensayar la exposición académica.
- Congelar versiones y etiquetar la entrega.\
  Hito: prototipo demostrable, reproducible y documentado.

### 12.1 Dependencias críticas

La secuencia de trabajo debe respetar cuatro dependencias:

1. El editor no puede finalizarse sin una convención de recursos gráficos.
2. El backend no puede integrarse con el frontend sin contratos de API.
3. El generador de stickers debe funcionar antes de incorporar paralelismo.
4. La demostración académica debe prepararse antes de la última semana.

La prueba de IA se realizará en la primera semana. No se dejará para después de terminar el editor.

### 12.2 Regla para recuperar retrasos

Si al final de la segunda semana el editor y la persistencia todavía no funcionan, se congelarán las funcionalidades P1. Si al final de la tercera semana la IA no está integrada, se documentará el motivo y se aplicará el plan de contingencia, sin comprometer la generación manual de stickers.

La última semana no debe utilizarse para incorporar funcionalidades nuevas. Debe reservarse para integración, correcciones y demostración.

## 13. Plan de pruebas y control de calidad

Las pruebas deben validar tanto el funcionamiento del producto como los requisitos de programación avanzada.

### 13.1 Pruebas unitarias

Se probarán de forma aislada:

- Validación de configuraciones de gatos.
- Reglas del catálogo.
- Límite de tres gatos.
- Composición de capas.
- Exportación PNG.
- Transiciones de estados de trabajos.
- Permisos de publicaciones.
- Cálculo de rutas y nombres de archivos.
- Validación de archivos de entrada para IA.

### 13.2 Pruebas de integración

| Prueba                               | Resultado esperado                                                         |
| ------------------------------------ | -------------------------------------------------------------------------- |
| Flet consulta el catálogo            | Obtiene las opciones activas de la API                                     |
| Usuario registra un gato             | El registro persiste en MySQL                                              |
| Se solicita un paquete               | Se crea un trabajo y se devuelve un identificador                          |
| Termina el trabajo                   | El estado cambia a `completed` y existen seis PNG                          |
| Falla una pose                       | El fallo se registra y no se declara éxito completo sin validar el paquete |
| Usuario publica un gato              | La publicación aparece en el hub                                           |
| Otro usuario copia el gato           | Se crea una copia independiente                                            |
| Invitado intenta publicar            | La API rechaza la operación                                                |
| Usuario intenta editar un gato ajeno | La API rechaza la operación                                                |
| Usuario supera el límite gratuito    | La API impide la creación adicional                                        |

### 13.3 Pruebas de aceptación

El criterio de aceptación no será que las pantallas se vean bien en una captura. Se debe poder ejecutar el recorrido completo con datos reales de prueba.

### Escenario de aceptación principal

El evaluador debe poder repetir este recorrido sin editar la base de datos manualmente.

1. Entrar como invitado y crear un gato.
2. Modificar las seis categorías y comprobar los cambios visuales.
3. Generar el paquete de seis stickers.
4. Descargar y abrir los PNG para comprobar que tienen fondo transparente.
5. Crear una cuenta e iniciar sesión.
6. Publicar el personaje y encontrarlo desde otra sesión.
7. Copiar el personaje y verificar que editar la copia no altera el original.
8. Ejecutar la demostración de IA y mostrar el manejo de errores.
9. Ejecutar las pruebas de concurrencia y mostrar los resultados del benchmark.

### 13.4 Pruebas de seguridad

- Contraseñas gestionadas por Django.
- Protección de endpoints privados.
- Verificación de propiedad en operaciones de modificación y eliminación.
- Validación de archivos subidos.
- Restricción de tipos de archivo.
- Configuración segura de CORS.
- Secretos fuera del repositorio.
- Eliminación de fotografías temporales.
- Control de errores para no exponer trazas internas.
- Prevención de acceso a archivos mediante rutas manipuladas.

### 13.5 Pruebas de rendimiento

Para la demostración se recomienda medir:

- Tiempo de composición de un sticker.
- Tiempo de generación de seis stickers.
- Tiempo secuencial frente a multiproceso.
- Número de procesos trabajadores.
- Número de tareas completadas y fallidas.
- Tiempo de respuesta de la API.
- Latencia de IA, por separado de la composición gráfica.

Se registrarán el equipo utilizado, la versión de Python, el tamaño de las imágenes, el número de repeticiones y la metodología. Las mediciones deben ser reproducibles y no se deben presentar como garantías de rendimiento en producción.

## 14. Gestión de riesgos

| Riesgo                                 | Probabilidad | Impacto | Mitigación                                                           |
| -------------------------------------- | ------------ | ------- | -------------------------------------------------------------------- |
| IA gratuita no disponible o limitada   | Alta         | Alto    | Validación en semana 1 y adaptador de proveedor                      |
| Inconsistencia de ilustraciones        | Media        | Alto    | Guía gráfica, anclajes y catálogo controlado                         |
| Retrasos en las capas                  | Media        | Alto    | Personaje completo temprano y entregas parciales                     |
| Flet no cubre una interacción prevista | Media        | Alto    | Prototipo técnico antes de construir todas las pantallas             |
| Conflictos entre agentes               | Alta         | Medio   | Contratos, ramas, revisiones y responsable de integración            |
| Errores de concurrencia                | Media        | Alto    | Pruebas aisladas antes de integrar con la API                        |
| Falta de tiempo para el hub            | Media        | Alto    | Implementación básica de publicaciones, sin funciones sociales extra |
| Archivos temporales acumulados         | Media        | Medio   | Directorios controlados y política de limpieza                       |
| Cambios tardíos de arquitectura        | Media        | Alto    | ADR y congelación de decisiones al inicio                            |
| Requisitos académicos desconocidos     | Alta         | Alto    | Consultar al profesor durante el primer día                          |

### 14.1 Plan de contingencia de IA

La arquitectura debe permitir desactivar la integración de IA sin desactivar el resto de la aplicación.

El modo de contingencia tendrá estas propiedades:

- El editor manual seguirá funcionando.
- El motor de composición seguirá generando los seis stickers.
- Los errores de IA se mostrarán como estados comprensibles.
- La aplicación no fingirá que una inferencia se ejecutó si no ocurrió.
- La demostración distinguirá claramente entre funcionalidades reales y simuladas.

Si la rúbrica exige que la IA sea una característica central y no acepta una integración limitada, la prueba de concepto de la primera semana será una puerta de decisión: si no hay una alternativa viable sin coste, se deberá renegociar el alcance o el requisito con el profesor.

## 15. Criterios de aceptación generales

El MVP se considerará entregable cuando satisfaga todos los criterios obligatorios siguientes.

| ID    | Criterio                                                 | Evidencia                               |
| ----- | -------------------------------------------------------- | --------------------------------------- |
| AC-01 | El editor permite modificar las seis categorías          | Prueba funcional y captura              |
| AC-02 | Las opciones se componen sin perder la coherencia visual | Paquete de personajes de prueba         |
| AC-03 | Se genera un paquete con seis stickers PNG               | Archivos de salida verificables         |
| AC-04 | Los PNG conservan transparencia                          | Prueba de canal alfa                    |
| AC-05 | Un usuario gratuito no supera tres gatos guardados       | Prueba de límite                        |
| AC-06 | Registro e inicio de sesión funcionan                    | Pruebas de autenticación                |
| AC-07 | Las publicaciones pueden explorarse y copiarse           | Prueba entre dos cuentas                |
| AC-08 | La IA ejecuta una inferencia real en el flujo acordado   | Entrada, salida y registro del trabajo  |
| AC-09 | Se demuestra concurrencia con operaciones reales         | Logs y pruebas de tareas                |
| AC-10 | Se demuestra multiprocesamiento                          | Identificación de procesos y resultados |
| AC-11 | Se mide el procesamiento secuencial y paralelo           | Informe reproducible                    |
| AC-12 | El repositorio contiene documentación actualizada        | Revisión de archivos                    |
| AC-13 | El proyecto arranca desde un clon limpio                 | Registro de instalación y ejecución     |
| AC-14 | No se exponen secretos ni imágenes privadas por defecto  | Revisión de configuración y permisos    |

Los criterios AC-09, AC-10 y AC-11 deben adaptarse si la rúbrica establece otros requisitos. No debe asumirse que esta tabla sustituye las instrucciones del profesor.

## 16. Protocolo de instalación y ejecución

La entrega debe ser reproducible. Otro integrante o evaluador debe poder clonar el repositorio y ejecutar el proyecto siguiendo instrucciones documentadas, sin depender de configuraciones personales no registradas.

La documentación incluirá:

- Versiones de Python y dependencias.
- Requisitos previos de MySQL.
- Creación y configuración de la base de datos.
- Variables de entorno requeridas.
- Comandos de migración y carga de datos de demostración.
- Comandos para iniciar backend y frontend.
- Comandos para ejecutar las pruebas.
- Comando para ejecutar el benchmark.
- Solución de errores comunes.

Se recomienda mantener los comandos en el `README.md` y separar la configuración del backend y del frontend cuando sea necesario. Los archivos de dependencias deben estar fijados a versiones verificadas.

`docker-compose.yml` queda como opcional: no se introducirá Docker si el equipo no lo domina o si su configuración consume tiempo que se necesita para las funcionalidades.

## 17. Preparación de la demostración académica

La exposición debe demostrar tanto el producto como las decisiones técnicas. Se recomienda preparar una presentación de entre 8 y 12 minutos, si el tiempo asignado por el profesor lo permite.

Bloque 1 — Producto y diseño

Mostrar el editor, modificar los seis atributos y explicar cómo las capas mantienen la consistencia de marca.

Bloque 2 — Generación

Crear un paquete, mostrar los seis PNG transparentes y explicar cómo el motor compone los recursos.

Bloque 3 — Inteligencia artificial

Mostrar la entrada, la ejecución del modelo, el resultado y el manejo de errores.

Bloque 4 — Comunidad

Publicar un personaje, abrir otra sesión y copiarlo sin alterar el original.

Bloque 5 — Programación avanzada

Ejecutar la prueba concurrente, comparar procesamiento secuencial y paralelo, y explicar los procesos observados.

La exposición debe incluir resultados obtenidos durante las pruebas, no cifras inventadas ni demostraciones preparadas únicamente para aparentar concurrencia.

## 18. Decisiones pendientes y protocolo de aprobación

El plan define la dirección del proyecto, pero algunas decisiones deben cerrarse antes de desarrollar las funcionalidades que dependen de ellas.

| Prioridad | Decisión pendiente                                                   | Responsable sugerido | Fecha límite |
| --------- | -------------------------------------------------------------------- | -------------------- | ------------ |
| Crítica   | Rúbrica exacta de concurrencia, multiprocesamiento, paralelismo e IA | Todo el equipo       | Día 1        |
| Crítica   | Prueba real de IA sin coste                                          | Integrante C         | Día 3        |
| Crítica   | Compatibilidad del prototipo web con Flet                            | Integrante A         | Día 2        |
| Crítica   | Primer gato completo y contrato de capas                             | Diseñadora + C       | Día 3        |
| Alta      | Contratos iniciales de API                                           | A + B                | Día 3        |
| Alta      | Esquema inicial de datos y autenticación                             | Integrante B         | Día 4        |
| Alta      | Formato definitivo de recursos y poses                               | Diseñadora + C       | Día 4        |
| Alta      | Mecanismo de autenticación entre Flet y Django                       | A + B                | Día 4        |
| Media     | Persistencia de invitados y recuperación de sesiones                 | A + B                | Semana 2     |
| Media     | Comportamiento visual del plan premium simulado                      | A + diseñadora       | Semana 2     |

Estas fechas son objetivos internos, no garantías. Si una prueba crítica falla, se debe registrar el problema y tomar una decisión explícita en vez de continuar suponiendo que se resolverá más adelante.

### Preguntas que deben hacerle al profesor

Es especialmente importante obtener respuesta a estas cuestiones:

1. ¿Se exige implementar `threading`, `multiprocessing`, `asyncio` o alguna biblioteca concreta?
2. ¿Deben demostrarse los tres conceptos por separado o basta con una solución integrada?
3. ¿La IA debe utilizar un modelo de aprendizaje automático real? ¿Se permite un modelo preentrenado o un servicio externo?
4. ¿Se exige entrenamiento del modelo o es suficiente la inferencia?
5. ¿Debe existir una medición de rendimiento que compare ejecución secuencial y paralela?
6. ¿Se requiere una cantidad mínima de procesos, hilos o tareas concurrentes?
7. ¿Se calificará el uso de la base de datos, las pruebas automatizadas y la documentación?
8. ¿Qué peso tiene la aplicación funcional frente a la exposición y las evidencias técnicas?

La respuesta a estas preguntas puede cambiar el orden de trabajo y la selección del modelo de IA, pero no debería alterar la visión central del producto.

## 19. Primeras 72 horas: plan de ejecución inmediato

Para evitar que el documento se quede en una planificación teórica, recomiendo que el equipo comience con este orden:

Día 1 — Organización

- Crear el repositorio.
- Añadir `AGENTS.md` y la documentación inicial.
- Consultar al profesor.
- Asignar responsables y establecer el mecanismo de revisión de cambios.

Día 2 — Pruebas técnicas

- Crear una aplicación mínima con Flet.
- Crear una API mínima con Django REST Framework.
- Conectar Django a MySQL.
- Componer un gato con dos o tres capas.
- Registrar tiempos de composición.

Día 3 — Validación de riesgos

- Probar el servicio o modelo de IA.
- Evaluar el resultado gráfico.
- Verificar compatibilidad del entorno.
- Aprobar la primera guía de recursos.
- Registrar las decisiones técnicas definitivas.

Al finalizar estas 72 horas, el equipo debe tener un repositorio que arranque, un primer recurso gráfico componible, una API conectada a la base de datos y una decisión sustentada sobre la viabilidad de IA.

## 20. Definición final del éxito

El proyecto no se medirá por la cantidad de pantallas, archivos o tecnologías que se consigan incorporar, sino por la coherencia del sistema completo.

Un buen MVP de Kitchi Studio debe cumplir cinco condiciones:

1. Producto: el usuario puede crear un gato y obtener un paquete de stickers real.
2. Diseño: las combinaciones son personalizables, pero siguen perteneciendo a un lenguaje visual reconocible.
3. Arquitectura: interfaz, API, base de datos, almacenamiento y motor de generación tienen responsabilidades claras.
4. Rigor académico: la IA, la concurrencia, el multiprocesamiento y el paralelismo se pueden explicar y demostrar con evidencias.
5. Reproducibilidad: un integrante nuevo o un evaluador puede comprender el repositorio, instalar el proyecto y repetir las pruebas.

Mi recomendación principal es mantener el enfoque 2D por capas, comenzar por el motor gráfico y los contratos de API, validar la IA antes de comprometerse con un modelo concreto y reservar la última semana para estabilización y demostración.

El siguiente paso prioritario es confirmar la rúbrica con el profesor y ejecutar las pruebas técnicas de la primera semana. Con esas dos cosas resueltas, podrán convertir este plan en tareas de implementación sin dejar decisiones críticas para el final.