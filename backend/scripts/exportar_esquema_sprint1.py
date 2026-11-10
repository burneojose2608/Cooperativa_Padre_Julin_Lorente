"""Exporta solo metadatos de las tablas de usuarios; no consulta filas de personas."""
import os
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from django.db import connection, transaction

TABLAS = ("usuario", "socio", "padron_prueba", "rol", "usuario_rol", "permiso", "rol_permiso",
          "consentimiento", "sesion", "auditoria", "token_recuperacion")
SALIDA = BASE.parent / "documentacion" / "sprint-1-equipo" / "datos"


def exportar():
    with transaction.atomic(), connection.cursor() as cursor:
        cursor.execute("SET TRANSACTION READ ONLY")
        cursor.execute("""SELECT table_name, column_name, udt_name, is_nullable, ordinal_position
                          FROM information_schema.columns
                          WHERE table_schema='public' AND table_name=ANY(%s)
                          ORDER BY table_name, ordinal_position""", [list(TABLAS)])
        columnas = cursor.fetchall()
        cursor.execute("""SELECT origen.relname, c.contype, c.conkey, destino.relname, c.confkey,
                                 c.conname, pg_get_constraintdef(c.oid)
                          FROM pg_constraint c JOIN pg_class origen ON origen.oid=c.conrelid
                          JOIN pg_namespace n ON n.oid=origen.relnamespace
                          LEFT JOIN pg_class destino ON destino.oid=c.confrelid
                          WHERE n.nspname='public' AND origen.relname=ANY(%s)
                          ORDER BY origen.relname, c.conname""", [list(TABLAS)])
        restricciones = cursor.fetchall()
        cursor.execute("""SELECT tablename, indexname, indexdef FROM pg_indexes
                          WHERE schemaname='public' AND tablename=ANY(%s)
                          ORDER BY tablename, indexname""", [list(TABLAS)])
        indices = cursor.fetchall()
    por_posicion = {(tabla, posicion): nombre for tabla, nombre, _, _, posicion in columnas}
    presentes = {fila[0] for fila in columnas}
    if presentes != set(TABLAS):
        raise SystemExit("Faltan tablas de Sprint 1; preparar SQL 01-06 antes de exportar.")
    claves = {}
    for tabla, tipo, campos, _, _, _, _ in restricciones:
        if tipo in ("p", "f"):
            for posicion in campos:
                claves.setdefault((tabla, posicion), set()).add("PK" if tipo == "p" else "FK")
    md = ["# Diccionario de datos de Sprint 1", "",
          "Generado desde metadatos PostgreSQL en una transacción de solo lectura. No incluye registros de personas, claves o tokens.",
          "El alcance es usuarios, autenticación, roles, padrón y auditoría. Los modelos físicos de módulos posteriores no se declaran cerrados por este catálogo.", ""]
    er = ["erDiagram"]
    for tabla in TABLAS:
        md += [f"## {tabla}", "", "| Columna | Tipo PostgreSQL | Admite NULL | Clave |", "| --- | --- | --- | --- |"]
        er.append(f"    {tabla} {{")
        for actual, nombre, tipo, nullable, posicion in columnas:
            if actual != tabla:
                continue
            clave = ", ".join(sorted(claves.get((tabla, posicion), set())))
            md.append(f"| {nombre} | {tipo} | {nullable} | {clave or '-'} |")
            er.append(f"        {tipo} {nombre}" + (f" {clave}" if clave else ""))
        er.append("    }")
        md += ["", "Restricciones:", ""]
        for actual, _, _, _, _, nombre, definicion in restricciones:
            if actual == tabla:
                md.append(f"- `{nombre}`: `{definicion.replace('|', '&#124;')}`.")
        md += ["", "Índices:", ""]
        for actual, nombre, definicion in indices:
            if actual == tabla:
                md.append(f"- `{nombre}`: `{definicion}`.")
        md.append("")
    for tabla, tipo, campos, padre, _, _, _ in restricciones:
        if tipo != "f" or padre not in TABLAS:
            continue
        unicas = [set(r[2]) for r in restricciones if r[0] == tabla and r[1] in ("p", "u")]
        extremo = "o|" if set(campos) in unicas else "o{"
        nullable = any(fila[0] == tabla and fila[4] in campos and fila[3] == "YES" for fila in columnas)
        inicio = "o|" if nullable else "||"
        etiqueta = "_".join(por_posicion[(tabla, posicion)] for posicion in campos)
        er.append(f'    {padre} {inicio}--{extremo} {tabla} : "{etiqueta}"')
    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / "diccionario-datos.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (SALIDA / "modelo-er.mmd").write_text("\n".join(er) + "\n", encoding="utf-8")
    print(f"Exportados metadatos de {len(TABLAS)} tablas y {len(columnas)} columnas, sin datos personales.")


if __name__ == "__main__":
    exportar()
