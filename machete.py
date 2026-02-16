import os
import sys
from collections import defaultdict

IGNORAR_CARPETAS = {
    "__pycache__",
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "dist",
    "build",
    ".idea",
    ".vscode"
}

IGNORAR_ARCHIVOS = {
    ".DS_Store"
}

EXTENSIONES_BINARIAS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp",
    ".exe", ".dll", ".so",
    ".zip", ".tar", ".gz",
    ".db", ".sqlite"
}


def es_binario(ruta):
    return os.path.splitext(ruta)[1].lower() in EXTENSIONES_BINARIAS


def generar_snapshot(repo_path, output_file="snapshot.txt"):
    conteo_extensiones = defaultdict(int)
    conteo_carpetas = defaultdict(int)

    archivos_validos = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORAR_CARPETAS]

        for archivo in files:
            if archivo in IGNORAR_ARCHIVOS:
                continue

            ruta_completa = os.path.join(root, archivo)

            if es_binario(ruta_completa):
                continue

            extension = os.path.splitext(archivo)[1].lower() or "[sin_extension]"
            conteo_extensiones[extension] += 1

            carpeta_relativa = os.path.relpath(root, repo_path)
            conteo_carpetas[carpeta_relativa] += 1

            archivos_validos.append(ruta_completa)

    with open(output_file, "w", encoding="utf-8") as salida:

        # =========================
        # MÉTRICAS
        # =========================
        salida.write("=" * 80 + "\n")
        salida.write("MÉTRICAS DEL REPOSITORIO\n")
        salida.write("=" * 80 + "\n\n")

        salida.write("Archivos por extensión:\n")
        for ext, cantidad in sorted(conteo_extensiones.items()):
            salida.write(f"  {ext}: {cantidad}\n")

        salida.write("\nCarpetas y cantidad de archivos:\n")
        for carpeta, cantidad in sorted(conteo_carpetas.items()):
            salida.write(f"  {carpeta}/: {cantidad}\n")

        salida.write("\n\n")

        # =========================
        # SNAPSHOT DE ARCHIVOS
        # =========================

        for ruta_completa in archivos_validos:
            ruta_relativa = os.path.relpath(ruta_completa, repo_path)

            try:
                with open(ruta_completa, "r", encoding="utf-8") as f:
                    contenido = f.read()
            except Exception:
                continue

            separador_inicio = f"\n{'='*80}\n"
            separador_inicio += f"INICIO ARCHIVO: {ruta_relativa}\n"
            separador_inicio += f"{'='*80}\n\n"

            separador_fin = f"\n{'='*80}\n"
            separador_fin += f"FIN ARCHIVO: {ruta_relativa}\n"
            separador_fin += f"{'='*80}\n\n"

            salida.write(separador_inicio)
            salida.write(contenido)
            salida.write(separador_fin)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python snapshot.py <ruta_del_repositorio>")
        sys.exit(1)

    repo_path = sys.argv[1]

    if not os.path.exists(repo_path):
        print("La ruta no existe.")
        sys.exit(1)

    generar_snapshot(repo_path)
    print("✔ Snapshot con métricas generado correctamente.")
