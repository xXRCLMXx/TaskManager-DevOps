# Resultados y conclusiones

## Resultados

| Fase | Herramienta | Resultado |
|---|---|---|
| Planificación | GitHub Projects + Issues | Tablero Board con 5 columnas, 6 historias de usuario, 15 issues con responsable, prioridad, estimación, fase y fecha |
| Desarrollo | Git + GitHub | Aplicación Flask con los 6 requerimientos (100 %), ramas `feature/*`, commits y Pull Requests revisados |
| Integración continua | GitHub Actions (`ci.yml`) | En cada push/PR a `main` se instalan dependencias y se ejecutan 21 pruebas |
| Pruebas | Pytest + matriz manual | 21 pruebas automatizadas aprobadas, 9 casos manuales aprobados, bugs registrados como issues y corregidos por PR |
| Entrega continua | Releases + `cd.yml` | Release `v1.0.0` y artefacto `TaskManager-v1` generado automáticamente |
| Despliegue | Render | Aplicación pública con `gunicorn app:app`, redeploy automático al actualizar `main` |
| Operación y monitoreo | `/health`, `monitoreo.yml`, Issues | Registro de disponibilidad y tiempos, incidencias documentadas, 5 mejoras y plan v2 |

## Conclusiones

1. DevOps no es solo programar: es un ciclo continuo (planear → programar → integrar → probar → entregar → desplegar → monitorear) donde cada fase alimenta a la siguiente.
2. GitHub permitió concentrar todo el ciclo en un solo lugar: el tablero y los issues para planear, Git y los Pull Requests para colaborar, Actions para automatizar y Releases para versionar.
3. La integración continua nos protegió: ningún cambio entraba a `main` sin que las pruebas pasaran, así los errores se detectaban en el PR y no en producción.
4. Trabajar con ramas evitó que nos estorbáramos entre integrantes y dejó un historial claro de quién hizo qué.
5. El monitoreo mostró problemas que no aparecían en local (datos que se pierden al redeplegar, primera carga lenta), lo que confirma que el trabajo continúa después de publicar.

## Preguntas de análisis

**1. ¿Qué ventajas ofrece utilizar GitHub Projects para organizar un proyecto de software?**
Muestra en un tablero visual qué está pendiente, en proceso, en revisión o terminado; cada tarjeta está ligada a un issue con responsable, prioridad, estimación y fecha. Así se evita la pérdida de información y la duplicidad, y todo el equipo ve el avance en tiempo real, junto al código.

**2. ¿Cuál es la diferencia entre Git y GitHub?**
Git es el sistema de control de versiones que se instala en la computadora y guarda el historial de cambios (commits, ramas, merges). GitHub es una plataforma en la nube que aloja repositorios Git y agrega herramientas de colaboración: Pull Requests, Issues, Projects, Actions y Releases.

**3. ¿Por qué es importante utilizar ramas durante el desarrollo?**
Cada integrante trabaja aislado en su funcionalidad sin romper `main`, que siempre se mantiene estable. Permite trabajar en paralelo, revisar los cambios antes de integrarlos y, si algo sale mal, descartar la rama sin afectar al resto.

**4. ¿Qué función cumple un Pull Request?**
Es la solicitud para integrar una rama a `main`. Permite que otro integrante revise el código, comente, pida cambios y apruebe; además dispara la integración continua, así que se ve si las pruebas pasan antes de hacer el merge.

**5. ¿Qué problemas permite detectar la integración continua?**
Pruebas que fallan, errores de sintaxis o importación, dependencias faltantes en `requirements.txt`, conflictos entre los cambios de distintos integrantes y código que "funciona en mi máquina" pero no en un entorno limpio.

**6. ¿Cuál es la diferencia entre integración continua y entrega continua?**
La integración continua (CI) une y prueba automáticamente el código cada vez que hay un cambio. La entrega continua (CD) va un paso después: toma el código ya probado y lo deja empaquetado y listo para publicarse (en nuestro caso, Release v1.0.0 + artefacto), pero publicar sigue siendo una decisión manual.

**7. ¿Qué diferencia existe entre entrega continua y despliegue continuo?**
En la entrega continua la versión queda lista y una persona decide cuándo publicarla. En el despliegue continuo la publicación es automática: cada cambio que pasa las pruebas y llega a `main` se despliega solo al servidor (Render redeploya en cuanto se actualiza `main`).

**8. ¿Por qué es importante automatizar las pruebas?**
Porque se ejecutan siempre, igual y en segundos, sin depender de que alguien se acuerde. Detectan regresiones (algo que ya funcionaba y se rompió) en cuanto se sube el cambio, y dan confianza para publicar seguido.

**9. ¿Qué sucede si se integra código que contiene errores?**
La rama principal deja de ser estable: el error puede llegar a producción, afectar a los usuarios, perder datos y bloquear al resto del equipo, que parte de un código roto. Corregirlo después cuesta más que detectarlo en el PR; por eso CI bloquea el merge si las pruebas fallan.

**10. ¿Por qué DevOps requiere monitorear una aplicación después de publicarla?**
Porque en producción aparecen problemas que no se ven en desarrollo: caídas, lentitud, errores con datos reales, límites del servidor. El monitoreo permite detectarlos rápido, registrarlos como incidencias y convertirlos en mejoras para la siguiente versión, cerrando el ciclo.

**11. ¿Qué beneficios obtiene una empresa al implementar DevOps?**
Entregas más rápidas y frecuentes, menos errores en producción, recuperación más rápida ante fallas, mejor comunicación entre desarrollo y operaciones, trazabilidad de cada cambio y clientes más satisfechos.

**12. ¿Cómo podrían mejorar el proceso de desarrollo en una segunda versión?**
Proteger la rama `main` para exigir PR aprobado y CI en verde; agregar análisis de estilo (flake8) y cobertura de pruebas al pipeline; pruebas de interfaz automatizadas; usar PostgreSQL; desplegar primero a un ambiente de staging; y alertas automáticas cuando falle el monitoreo.
