# 12 · Guía viva de la plataforma — Kitchi Studio

Documento de estudio para la sustentación · Versión 0.1 (esqueleto) · 28 de octubre de 2026

> **Estado:** documento vivo, casi vacío a propósito. Se completará **por incrementos** a medida que la aplicación se implemente. No describe funcionalidades que aún no existen.
>
> **Para quién es:** todos los integrantes del equipo, incluida la diseñadora. Es la lectura previa a la presentación y la base para responder preguntas individuales sobre cualquier parte del proyecto.

## Para qué sirve

- Explicar qué problema resuelve Kitchi Studio y para quién.
- Recorrer el flujo completo de la plataforma sin leer el código.
- Entender cómo se conectan la interfaz, la API, la base de datos y el motor gráfico.
- Preparar una demo de 10 minutos y las preguntas individuales del profesor.
- Dejar por escrito las decisiones y limitaciones que un integrante nuevo necesitaría conocer.

## Regla de actualización

1. Cada incremento que cambie el funcionamiento, una pantalla, la arquitectura, la instalación o la demo debe actualizar este documento en el mismo cambio.
2. Se escribe en lenguaje claro: **qué hace**, **cómo se usa** y **por qué se diseñó así**.
3. No se copia código completo; se explican los módulos y se enlazan los archivos.
4. No se marca como terminado nada que solo exista en el diseño o esté simulado.
5. Al final de cada incremento se añade una fila al registro de la última sección.

## 1. Resumen en una frase

_Pendiente de completar cuando exista el primer flujo funcional._

## 2. Problema, usuario y propuesta de valor

_Pendiente (P10/P18)._

## 3. Flujo completo del usuario

_Pendiente (P10–P19). Debe cubrir: crear gato → personalizar → generar seis stickers → descargar → registrarse → publicar → copiar._

## 4. Pantallas y navegación

_Pendiente por pantalla: Inicio, Editor, Importación de fotografía, Revisión de IA, Generador, Paquete, Registro/Login, Hub, Publicación y Mis gatos._

## 5. Arquitectura en cinco minutos

_Pendiente (P02/P03). Explicar Flet, Django REST Framework, MySQL, almacenamiento local y motor Pillow._

## 6. Modelo de datos

_Pendiente (P11). Entidades principales y por qué la configuración del gato se guarda como JSON validado._

## 7. Motor de stickers

_Pendiente (P04/P13/P14). Capas, orden de composición, transparencia, validación de los seis PNG y determinismo._

## 8. Integración de IA

_Pendiente (P05/P16). Alternativa elegida, inferencia real, privacidad y contingencia._

## 9. Concurrencia, multiprocesamiento y paralelismo

_Pendiente (P20–P22). Qué se mide, con qué operaciones reales y qué significan los resultados._

## 10. Guion de la demo de 10 minutos

_Pendiente (P28/P37). Debe coincidir con [`11_DEMO_SCRIPT.md`](11_DEMO_SCRIPT.md)._

## 11. Preguntas frecuentes de la sustentación

_Pendiente. Añadir preguntas reales de los ensayos y respuestas breves._

## 12. Limitaciones conocidas y trabajo futuro

_Pendiente. Distinguir claramente lo implementado, lo simulado y lo fuera de alcance._

## 13. Glosario

_Pendiente. Términos como configuración, capa, pose, paquete, publicación, trabajo de generación, inferencia y benchmark._

## Registro de incrementos

| Fecha | Incremento | Qué se documentó | Autor |
| --- | --- | --- | --- |
| 2026-10-28 | Estructura inicial | Se creó el esqueleto y las reglas de actualización; aún no hay funcionalidades implementadas | Equipo |
