# -*- coding: utf-8 -*-
"""Motor de cálculo CO2calc — estimativa rápida em 4 etapas e
apuração por atividade (E = atividade × fator × fração de atribuição).

Estrutura P = atividade × fator × fração de atribuição, conforme a taxonomia
anexa (planilha 'Guia'). Fatores vêm da tabela `fatores` (editável).
"""
from . import database as db

CASA_KWH = {"flat": "FAST_HOME_KWH_FLAT", "small": "FAST_HOME_KWH_SMALL",
            "medium": "FAST_HOME_KWH_MED", "large": "FAST_HOME_KWH_LARGE"}
AQUEC = {"gas": 0.70, "eletric": 0.45, "bomba": 0.45, "oleo": 0.75}   # fração p/ aquecimento
AQUEC_FATOR = {"gas": ("HEAT_KWH_GAS_NAT", 0.201), "oleo": ("HEAT_KWH_OLEO", 0.266),
               "eletric": None, "bomba": None}
DRIVE_KM = {"nenhum": 0, "pouco": 4000, "medio": 8000, "muito": 16000}   # mi→km arredondado
DRIVE_FATOR = {"gasolina": ("TR_CAR_KM_GAS", 0.181), "diesel": ("TR_CAR_KM_DIESEL", 0.171),
               "hibrido": ("TR_CAR_KM_HIBRIDO", 0.125), "eletrico": ("TR_CAR_KM_ELETRICO", 0.055)}
DIETA_T = {"carne_dias": 2.9, "carne_poucas": 2.15, "veggie": 1.6, "vegana": 1.25}  # tCO2e/pessoa/ano


def fator(con, codigo, default=None):
    v = db.get_fator(con, codigo)
    return v if v is not None else default


def fast_calc(con, casa="flat", aquec="gas", pessoas=1, drive="medio", fuel="gasolina",
               voos_curto=1, voos_longo=0, dieta="carne_poucas", pais="BR"):
    """Estimativa rápida em 4 etapas (moradia, direção, voos, dieta).

    Retorna dict com breakdown kgCO2e/pessoa/ano e comparativo com a média
    nacional (OECD/Defra) do país escolhido — como no site original.
    """
    pessoas = max(1, int(pessoas))
    grid = db.grid_pais(con, pais)

    # 1 · Moradia: tamanho define kWh totais; tipo de aquecimento divide gás × eletricidade.
    kwh_total = fator(con, CASA_KWH[casa], 4500)
    share_gas = AQUEC.get(aquec, 0.5)
    if aquec == "gas":
        f_gas = fator(con, "HEAT_KWH_GAS_NAT", 0.201)
        gas_kwh = kwh_total * share_gas
        el_kwh = kwh_total - gas_kwh
        morad = gas_kwh * f_gas + el_kwh * grid
    elif aquec == "oleo":
        f_oil = fator(con, "HEAT_KWH_OLEO", 0.266)
        morad = kwh_total * share_gas * f_oil + kwh_total * (1 - share_gas) * grid
    elif aquec == "bomba":
        cop = fator(con, "HEAT_COP_PADRAO", 3.0)
        morad = kwh_total / cop * grid + kwh_total * (1 - share_gas) * grid
    else:  # eletric
        morad = kwh_total * grid
    # rateio da moradia: cada pessoa extra soma ~3/4 (regra de domicílio)
    adj = fator(con, "FAST_HOME_SHARE_ADJ", 0.75)
    divisor = 1 + adj * (pessoas - 1)
    morad_pp = morad / divisor

    # 2 · Dirigir
    km = DRIVE_KM[drive]
    fk = fator(con, DRIVE_FATOR[fuel][0], DRIVE_FATOR[fuel][1])  # EV usa fator médio de rede
    car = km * fk
    car_pp = car / pessoas

    # 3 · Voos (ida e volta, kgCO2e por viagem — calibração CO2calc)
    v_curto = fator(con, "FAST_FLIGHT_SHORT_RT", 500) * voos_curto
    v_longo = fator(con, "FAST_FLIGHT_LONG_RT", 2500) * voos_longo
    flights_pp = (v_curto + v_longo) / pessoas

    # 4 · Dieta (tCO2e/pessoa/ano → kg)
    alim_pp = DIETA_T[dieta] * 1000

    # 5 · Bens & serviços: fração da média nacional
    media = db.media_pais(con, pais) * 1000
    bens_pp = media * fator(con, "FAST_GOODS_SHARE", 0.35)

    total_pp = morad_pp + car_pp + flights_pp + alim_pp + bens_pp
    return {
        "breakdown_pp": {"moradia": round(morad_pp, 1), "carro": round(car_pp, 1),
                          "voos": round(flights_pp, 1), "alimentacao": round(alim_pp, 1),
                          "bens_servicos": round(bens_pp, 1)},
        "total_pp": round(total_pp, 1),
        "total_hogar": round(total_pp * pessoas, 1),
        "media_nacional": round(media, 1),
        "pais": pais, "pessoas": pessoas,
        "vs_media": round((total_pp / media - 1) * 100, 1),
    }


FAST_RESPOSTAS = fast_calc.__name__

def records_from_baseline(con, uid, res, brk):
    """Cria registros anuais (origem 'quick') a partir de uma estimativa salva."""
    import datetime
    ano = datetime.date.today().year
    mapa = {"moradia": ("B1", "MORAD", "Estimativa quick: moradia"),
            "carro": ("A1", "TRANSP", "Estimativa quick: carro"),
            "voos": ("A3", "TRANSP", "Estimativa quick: voos"),
            "alimentacao": ("C1", "ALIM", "Estimativa quick: alimentação"),
            "bens_servicos": ("D", "BENS", "Estimativa quick: bens e serviços")}
    n = 0
    for k, kg in brk.items():
        cod, grp, nome = mapa[k]
        con.execute("INSERT INTO registros(usuario_id,codigo,grupo,atividade,metodo,valor,unidade,fator,pessoas,co2e_kg,tipo_periodo,ano,mes,obs,origem,criado_em)"
                    " VALUES (?,?,?,?,?,1,'baseline','1.0',1,?, 'A', ?, NULL, ?, 'quick', datetime('now'))",
                    (uid, cod, grp, nome, kg, ano, "gerado da calculadora rápida"))
        n += 1
    con.commit()
    return n
