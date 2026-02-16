# Arbol-Machete

Herramienta simple para inspección estructural de directorios y repositorios.

Permite generar:

* Árbol de archivos y carpetas
* Métricas del repositorio

  * Cantidad de archivos por extensión
  * Cantidad de archivos por carpeta
* Snapshot completo del contenido de los archivos con separadores de inicio y fin

Ignora automáticamente carpetas y archivos comunes como:

* **pycache**
* .git
* node_modules
* venv / .venv
* dist, build
* Archivos binarios conocidos

---

## Requisitos

* Python 3.9 o superior
* Sin dependencias externas

---

## Uso

### Generar árbol de archivos

```bash
python arbol.py /ruta/a/tu/directorio
```

Muestra en consola el árbol estructural del directorio indicado.

---

### Generar reporte completo

```bash
python repo_inspector.py /ruta/a/tu/repositorio
```

Genera un archivo `repo_report.txt` que incluye:

1. Árbol del repositorio
2. Métricas estructurales
3. Snapshot completo de los archivos

---

## Estructura del Reporte

```
================================================================================
ÁRBOL DEL REPOSITORIO
================================================================================

...

================================================================================
MÉTRICAS
================================================================================

...

================================================================================
SNAPSHOT DE ARCHIVOS
================================================================================

...
```

---

Arbol-Machete está diseñado como herramienta utilitaria para análisis rápido, documentación técnica y bootstrap de contexto en proyectos de software.
