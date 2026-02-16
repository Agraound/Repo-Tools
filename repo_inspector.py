import os
import sys
from collections import defaultdict

IGNORAR_CARPETAS = {
    "__pycache__", ".git", "node_modules",
    "venv", ".venv", "dist", "build",
    ".idea", ".vscode"
}

IGNORAR_ARCHIVOS = {".DS_Store", ".env"}

EXTENSIONES_BINARIAS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp",
    ".exe", ".dll", ".so",
    ".zip", ".tar", ".gz",
    ".db", ".sqlite"
}


def es_binario(ruta):
    return os.path.splitext(ruta)[1].lower() in EXTENSIONES_BINARIAS


# =========================
# ÁRBOL
# =========================

def generar_arbol(directorio, prefijo=""):
    lineas = []

    try:
        elementos = sorted(
            [e for e in os.listdir(directorio)
             if e not in IGNORAR_CARPETAS and e not in IGNORAR_ARCHIVOS]
        )
    except PermissionError:
        return []

    total = len(elementos)

    for i, nombre in enumerate(elementos):
        ruta = os.path.join(directorio, nombre)
        es_ultimo = i == total - 1
        conector = "└── " if es_ultimo else "├── "

        if os.path.isdir(ruta):
            lineas.append(prefijo + conector + nombre + "/")
            extension_prefijo = "    " if es_ultimo else "│   "
            lineas.extend(generar_arbol(ruta, prefijo + extension_prefijo))
        else:
            lineas.append(prefijo + conector + nombre)

    return lineas


# =========================
# INSPECTOR COMPLETO
# =========================

def generar_reporte(repo_path, output_file="repo_report.txt"):

    conteo_ext = defaultdict(int)
    conteo_carpetas = defaultdict(int)
    archivos_validos = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORAR_CARPETAS]

        for archivo in files:
            if archivo in IGNORAR_ARCHIVOS:
                continue

            ruta = os.path.join(root, archivo)

            if es_binario(ruta):
                continue

            ext = os.path.splitext(archivo)[1].lower() or "[sin_extension]"
            conteo_ext[ext] += 1

            carpeta_rel = os.path.relpath(root, repo_path)
            conteo_carpetas[carpeta_rel] += 1

            archivos_validos.append(ruta)

    with open(output_file, "w", encoding="utf-8") as salida:

        # =========================
        # ÁRBOL
        # =========================
        salida.write("="*80 + "\nÁRBOL DEL REPOSITORIO\n" + "="*80 + "\n\n")
        salida.write(repo_path + "/\n")
        for linea in generar_arbol(repo_path):
            salida.write(linea + "\n")

        # =========================
        # MÉTRICAS
        # =========================
        salida.write("\n" + "="*80 + "\nMÉTRICAS\n" + "="*80 + "\n\n")

        salida.write("Archivos por extensión:\n")
        for ext, cant in sorted(conteo_ext.items()):
            salida.write(f"  {ext}: {cant}\n")

        salida.write("\nCarpetas y cantidad de archivos:\n")
        for carpeta, cant in sorted(conteo_carpetas.items()):
            salida.write(f"  {carpeta}/: {cant}\n")

        # =========================
        # SNAPSHOT
        # =========================
        salida.write("\n" + "="*80 + "\nSNAPSHOT DE ARCHIVOS\n" + "="*80 + "\n")

        for ruta in archivos_validos:
            rel = os.path.relpath(ruta, repo_path)

            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read()
            except Exception:
                continue

            salida.write(f"\n{'='*80}\nINICIO ARCHIVO: {rel}\n{'='*80}\n\n")
            salida.write(contenido)
            salida.write(f"\n{'='*80}\nFIN ARCHIVO: {rel}\n{'='*80}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python repo_inspector.py <ruta_del_repositorio>")
        sys.exit(1)

    repo = sys.argv[1]

    if not os.path.exists(repo):
        print("La ruta no existe.")
        sys.exit(1)

    generar_reporte(repo)
    print("✔ Reporte completo generado.")
