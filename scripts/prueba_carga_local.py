"""Prueba de carga y concurrencia HTTP local (T-035 / RNF-04, RNF-05) contra Django TestClient/WSGI."""
from concurrent.futures import ThreadPoolExecutor
import ctypes.util
import os
from pathlib import Path
import statistics
import sys
import time

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
from django.db import connections  # noqa: E402
from django.test import Client  # noqa: E402


def ejecutar_lote(concurrencia: int, solicitudes: int) -> dict:
    tiempos = []
    errores_5xx = 0

    def tarea(_i: int) -> tuple[float, int]:
        cliente = Client(HTTP_HOST="localhost")
        inicio = time.perf_counter()
        resp = cliente.get("/api/salud/")
        duracion = time.perf_counter() - inicio
        connections.close_all()
        return duracion, resp.status_code

    with ThreadPoolExecutor(max_workers=concurrencia) as pool:
        codigos_200 = 0
        for duracion, codigo in pool.map(tarea, range(solicitudes)):
            tiempos.append(duracion)
            if codigo == 200:
                codigos_200 += 1
            if codigo >= 500:
                errores_5xx += 1

    tiempos.sort()
    p95 = tiempos[int(len(tiempos) * 0.95) - 1]
    tasa_5xx = 100.0 * errores_5xx / len(tiempos)
    return {
        "concurrencia": concurrencia,
        "solicitudes": solicitudes,
        "exitosas_200": codigos_200,
        "p50_ms": round(statistics.median(tiempos) * 1000, 2),
        "p95_ms": round(p95 * 1000, 2),
        "errores_5xx": errores_5xx,
        "tasa_5xx_pct": round(tasa_5xx, 3),
    }


def main() -> int:
    django.setup()
    print("=== Prueba de carga local (T-035 / RNF-04 y RNF-05) ===")
    lote_200 = ejecutar_lote(concurrencia=20, solicitudes=200)
    print(f"Lote 200 req (20 hilos): 200 OK={lote_200['exitosas_200']}/200, p50={lote_200['p50_ms']} ms, p95={lote_200['p95_ms']} ms, 5xx={lote_200['tasa_5xx_pct']} %")
    lote_500 = ejecutar_lote(concurrencia=40, solicitudes=500)
    print(f"Lote 500 req (40 hilos): 200 OK={lote_500['exitosas_200']}/500, p50={lote_500['p50_ms']} ms, p95={lote_500['p95_ms']} ms, 5xx={lote_500['tasa_5xx_pct']} %")
    ok = (
        lote_200["exitosas_200"] == 200
        and lote_500["exitosas_200"] == 500
        and lote_200["p95_ms"] <= 2000.0
        and lote_500["tasa_5xx_pct"] < 1.0
    )
    print("OK: Umbrales locales p95 <= 2000 ms y 5xx < 1 % cumplidos." if ok else "ERROR: Umbral excedido.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
