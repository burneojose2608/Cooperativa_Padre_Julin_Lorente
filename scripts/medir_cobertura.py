"""Verificación automatizada de cobertura de lógica de negocio (T-039 / RNF-19) usando stdlib trace."""
import ctypes.util
import os
from pathlib import Path
import sys
import trace

ROOT = Path(__file__).resolve().parents[1]
if (ROOT / ".venv/Lib/site-packages").exists():
    sys.path.append(str(ROOT / ".venv/Lib/site-packages"))
sys.path.insert(0, str(ROOT / "backend"))
if os.name == "nt" and Path(r"C:\Program Files\PostgreSQL\18\bin\libpq.dll").exists():
    os.environ.setdefault("PSYCOPG_IMPL", "python")
    original_find = ctypes.util.find_library
    ctypes.util.find_library = lambda name: (
        r"C:\Program Files\PostgreSQL\18\bin\libpq.dll" if name in ("pq", "libpq.dll") else original_find(name)
    )
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402
from django.core.management import call_command  # noqa: E402

OBJETIVOS = [
    ROOT / "backend/apps/plataforma/negocio.py",
    ROOT / "backend/apps/plataforma/api_negocio.py",
    ROOT / "backend/apps/plataforma/api_comunidad.py",
    ROOT / "backend/apps/plataforma/api_reportes.py",
    ROOT / "backend/apps/plataforma/api_supervision.py",
    ROOT / "backend/apps/plataforma/contenidos.py",
    ROOT / "backend/apps/plataforma/notificaciones.py",
]


def contar_lineas_ejecutables(ruta: Path) -> set[int]:
    """Cuenta líneas ejecutables excluyendo comentarios, líneas en blanco y docstrings simples."""
    lineas = set()
    en_docstring = False
    for num, texto in enumerate(ruta.read_text(encoding="utf-8").splitlines(), start=1):
        limpia = texto.strip()
        if not limpia or limpia.startswith("#"):
            continue
        if limpia.startswith(('"""', "'''")):
            comilla = limpia[:3]
            if limpia.count(comilla) >= 2 and len(limpia) > 3:
                continue
            en_docstring = not en_docstring
            continue
        if en_docstring:
            continue
        if limpia.startswith(("def ", "class ", "@", "from ", "import ", "else:", "try:", "except", "finally:")):
            continue
        lineas.add(num)
    return lineas


def main() -> int:
    django.setup()
    trazador = trace.Trace(count=True, trace=False)
    trazador.runfunc(call_command, "test", "apps.plataforma", verbosity=1, interactive=False)
    resultados = trazador.results()

    ejecutadas_por_archivo: dict[Path, set[int]] = {}
    for (archivo, linea), cuenta in resultados.counts.items():
        if cuenta > 0:
            ejecutadas_por_archivo.setdefault(Path(archivo).resolve(), set()).add(linea)

    total_ejecutables = 0
    total_cubiertas = 0
    print("\n=== Cobertura de lógica de negocio (T-039 / RNF-19) ===")
    for ruta in OBJETIVOS:
        resuelta = ruta.resolve()
        ejecutables = contar_lineas_ejecutables(resuelta)
        cubiertas = ejecutables & ejecutadas_por_archivo.get(resuelta, set())
        porcentaje = (100.0 * len(cubiertas) / len(ejecutables)) if ejecutables else 100.0
        total_ejecutables += len(ejecutables)
        total_cubiertas += len(cubiertas)
        print(f"  {ruta.relative_to(ROOT)}: {len(cubiertas)}/{len(ejecutables)} ({porcentaje:.1f} %)")

    global_pct = (100.0 * total_cubiertas / total_ejecutables) if total_ejecutables else 0.0
    print(f"TOTAL COBERTURA LÓGICA DE NEGOCIO: {total_cubiertas}/{total_ejecutables} ({global_pct:.1f} %)")
    if global_pct < 70.0:
        print("ERROR: La cobertura está por debajo del mínimo exigido de 70 % (RNF-19).")
        return 1
    print("OK: Cobertura >= 70 % verificada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
