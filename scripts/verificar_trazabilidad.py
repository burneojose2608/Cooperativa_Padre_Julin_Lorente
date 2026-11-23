"""Comprueba la trazabilidad de los specs contra las fuentes versionadas."""

import csv
from collections import Counter
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SPECS = ROOT / "specs"
DOC = ROOT / "documentacion"
ENTREGA = DOC / "entregable"


def filas(archivo):
    with archivo.open(encoding="utf-8-sig", newline="") as entrada:
        return list(csv.DictReader(entrada))


def identificadores(texto, prefijo):
    patrones = {"RF": r"RF-\d{2}(?:-\d+)?", "HU": r"HU-\d{3}",
                 "UR": r"UR-\d{2}", "CU": r"CU-G\d{2}", "RNF": r"RNF-\d{2}"}
    return set(re.findall(patrones[prefijo], texto))


def main():
    matriz = filas(SPECS / "trazabilidad.csv")
    backlog = {f["Work item ID"]: f for f in filas(DOC / "product_con_subtareas.csv")
               if f["Work Type"] in {"Story", "Sub-task"}}
    funcionales = {f["id_requisito"]: f for f in filas(ENTREGA / "requisitos_funcionales.csv")}
    usuarios = {f["id_requisito"]: f for f in filas(ENTREGA / "requisitos_usuario.csv")}
    calidad = {f["id_requisito"] for f in filas(ENTREGA / "requisitos_no_funcionales.csv")}
    ea = {(f["HU"], f["RF"]): f for f in filas(ENTREGA / "trazabilidad/TRAZABILIDAD-VERIFICADA.csv")}
    inventario = filas(SPECS / "estado-implementacion.csv")
    modulos = {p.name for p in SPECS.iterdir() if p.is_dir() and p.name != "000-plataforma"}
    errores = []

    def comprobar(condicion, mensaje):
        if not condicion:
            errores.append(mensaje)

    claves = Counter((f["hu"], f["rf"]) for f in matriz)
    comprobar(all(n == 1 for n in claves.values()), "Hay relaciones HU–RF duplicadas.")
    comprobar(set(claves) == set(ea), "Las relaciones HU–RF difieren del catálogo EA.")
    comprobar({f["item"] for f in matriz} == set(backlog), "La cobertura del backlog difiere.")
    comprobar({f["spec"] for f in inventario} == modulos and len(inventario) == len(modulos),
              "El inventario no cubre cada módulo exactamente una vez.")
    comprobar({f["spec"] for f in matriz} == modulos, "La matriz no cubre los módulos del inventario.")

    for modulo in sorted(modulos):
        carpeta = SPECS / modulo
        spec = (carpeta / "spec.md").read_text(encoding="utf-8-sig")
        plan = (carpeta / "plan.md").read_text(encoding="utf-8-sig")
        tareas = (carpeta / "tasks.md").read_text(encoding="utf-8-sig")
        for clave in identificadores(spec + plan + tareas, "RNF"):
            comprobar(clave in calidad, f"{modulo} menciona un RNF desconocido: {clave}.")

        requisitos = set(re.findall(r"^### (RF-\d{2}-\d+)\b", spec, re.MULTILINE))
        historias = set(re.findall(r"^### (HU-\d{3}):", spec, re.MULTILINE))
        registros = [f for f in matriz if f["spec"] == modulo]
        comprobar({f["rf"] for f in registros} == requisitos, f"{modulo}: los RF del spec difieren.")
        comprobar({f["hu"] for f in registros} == historias, f"{modulo}: las HU del spec difieren.")

        for fila in registros:
            hu, rf, ur, cu = (fila[k] for k in ("hu", "rf", "ur", "cu"))
            fuente = backlog.get(fila["item"], {})
            requisito = funcionales.get(rf, {})
            modelo = ea.get((hu, rf), {})
            marco = f"{hu}/{rf}"
            comprobar(fuente.get("Summary", "").startswith(f"{hu}:")
                      and fuente.get("Work Type") == fila["tipo"]
                      and fuente.get("Sprint planificado") == fila["sprint"],
                      f"{marco}: identificación, tipo o sprint difieren del backlog.")
            comprobar(hu in identificadores(requisito.get("hu_asociadas", ""), "HU")
                      and identificadores(ur, "UR") == identificadores(requisito.get("ur_asociados", ""), "UR")
                      and identificadores(cu, "CU") == identificadores(requisito.get("cu_asociados", ""), "CU"),
                      f"{marco}: correspondencia de requisitos distinta de la fuente.")
            comprobar(all(rf in identificadores(usuarios.get(k, {}).get("rf_asociados", ""), "RF")
                          for k in identificadores(ur, "UR")), f"{marco}: falta el enlace inverso UR–RF.")
            comprobar(modelo.get("WorkItem") == fila["item"]
                      and identificadores(ur, "UR") == identificadores(modelo.get("UR", ""), "UR")
                      and cu in {modelo.get("CU_grupo_original"), modelo.get("CU_diagrama_actual")}
                      and bool(modelo.get("CU_GUID")), f"{marco}: falta una correspondencia EA con GUID.")
            seccion = re.search(rf"^### {rf}\b.*?(?=^### |^## |\Z)", spec, re.MULTILINE | re.DOTALL)
            comprobar(bool(seccion) and all(set(identificadores(seccion[0], p)) == identificadores(v, p)
                                           for p, v in (("HU", hu), ("UR", ur), ("CU", cu))),
                      f"{marco}: el texto del requisito difiere de la matriz.")
            comprobar(bool(re.search(rf"^- \[[ xX]\] {hu}-[A-Z]+ \({rf}(?:[,)])", tareas, re.MULTILINE)),
                      f"{marco}: no hay tarea con la relación explícita.")

    for fila in inventario:
        for campo in ("backend", "frontend", "evidencia"):
            ruta = fila[campo]
            if campo != "evidencia" or ruta.startswith("specs/"):
                comprobar((ROOT / ruta).is_file(), f"{fila['spec']}: ruta de {campo} inexistente ({ruta}).")

    for fila in filas(ENTREGA / "trazabilidad/RNF-RF.csv"):
        comprobar(fila["rnf"] in calidad and fila["rf"] in funcionales,
                  f"Vínculo de calidad inválido: {fila['rnf']}/{fila['rf']}.")

    if errores:
        raise SystemExit("\n".join(errores))
    print(f"{len(modulos)} módulos, {len(claves)} relaciones HU–RF–UR–CU y {len(calidad)} RNF verificados.")


if __name__ == "__main__":
    main()
