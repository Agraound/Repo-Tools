import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

IGNORAR = {
    "__pycache__",
    ".git",
    "node_modules",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
    "dist",
    "build",
    ".DS_Store"
}


def generar_arbol(directorio, prefijo=""):
    lineas = []

    try:
        elementos = sorted(
            [e for e in os.listdir(directorio) if e not in IGNORAR]
        )
    except PermissionError:
        lineas.append(f"{prefijo}└── [Acceso denegado]")
        return lineas

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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python arbol.py <ruta_del_directorio>")
        sys.exit(1)

    ruta_base = sys.argv[1]

    if not os.path.exists(ruta_base):
        print("La ruta no existe.")
        sys.exit(1)

    resultado = [ruta_base + "/"]
    resultado.extend(generar_arbol(ruta_base))

    arbol_texto = "\n".join(resultado)

    print(arbol_texto)
