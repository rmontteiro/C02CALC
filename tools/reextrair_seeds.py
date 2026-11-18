# -*- coding: utf-8 -*-
"""Relê a planilha-mestre versionada (docs/taxonomia/*.xlsx) e:
  --check  → confirma se os seeds JSON no repositório ainda são idênticos a ela
  --write  → regenera taxonomia.json e metodos.json a partir da planilha (uso ao
             incorporar uma nova revisão; rode os testes antes de commitar)
Dependência: openpyxl (pip install openpyxl)."""
import argparse, hashlib, json, os, sys

import openpyxl

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX = os.path.join(RAIZ, "docs", "taxonomia", "Taxonomia_Mundial_Pegada_Carbono_Individual.xlsx")
SEED = os.path.join(RAIZ, "co2calc", "seed")


MAPA = [("codigo", "Código"), ("pai", "Código pai"), ("nivel", "Nível"), ("tipo", "Tipo de registro"),
        ("nome", "Nome do nó"), ("setor", "Nível 1 · setor"), ("subsetor", "Nível 2 · subsetor"),
        ("familia", "Nível 3 · família"), ("metodo", "Método"), ("unidade", "Unidade de atividade"),
        ("coicop", "COICOP 2018 · divisão"), ("perimetro", "Perímetro"), ("regras", "Regras"),
        ("geo", "Geografia do fator"), ("caminho", "Caminho hierárquico")]


def extrair():
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    rows = list(wb["Taxonomia"].iter_rows(values_only=True))
    hdr = [str(h) for h in rows[3]]
    saida = []
    for r in rows[4:]:
        if not r or r[0] in (None, ""):
            continue
        d = dict(zip(hdr, r))
        item = {}
        for k, src in MAPA:
            val = d[src]
            if val in (None, ""):
                item[k] = None
            elif k == "nivel":
                item[k] = int(val)
            else:
                item[k] = str(val).strip()
        saida.append(item)
    met = list(wb["Métodos"].iter_rows(values_only=True))
    mh = [str(h) for h in met[3]]
    metodos = []
    for r in met[4:]:
        if not r or r[0] in (None, ""):
            continue
        metodos.append({k: (str(v).strip() if v is not None else None) for k, v in zip(mh, r)})
    return saida, metodos


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--write", action="store_true")
    a = ap.parse_args()

    with open(XLSX, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    nodes, metodos = extrair()
    tj = json.dumps(nodes, ensure_ascii=False, indent=1)
    mj = json.dumps(metodos, ensure_ascii=False, indent=1)

    if a.write:
        with open(os.path.join(SEED, "taxonomia.json"), "w", encoding="utf-8") as f:
            f.write(tj)
        with open(os.path.join(SEED, "metodos.json"), "w", encoding="utf-8") as f:
            f.write(mj)
        print(f"[OK] seeds reextraídos de {os.path.basename(XLSX)} (SHA-256 {sha[:16]}…)")
        return

    ok = True
    for name, content in [("taxonomia.json", tj), ("metodos.json", mj)]:
        p = os.path.join(SEED, name)
        atual = open(p, encoding="utf-8").read()
        same = atual == content
        print(f"{name}: {'IDÊNTICO ✓' if same else 'DIVERGE — rode --write e revise os diffs'}")
        ok = ok and same
    print(f"planilha: SHA-256 {sha}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
