# -*- coding: utf-8 -*-
"""Rótulos e explicações, em português completo, dos fatores de emissão.

Transforma os códigos internos (ex.: FAST_HOME_KWH_LARGE, GRID_BR) em nomes
intuitivos e fornece um parágrafo explicativo para cada fator, usado no painel
"Editar fatores de emissão" da tela Usuários e no formulário de lançamento.
"""
import json, os

_PAISES_PATH = os.path.join(os.path.dirname(__file__), "seed", "paises.json")
try:
    with open(_PAISES_PATH, encoding="utf-8") as _f:
        PAISES = {p["iso"]: p["nome"] for p in json.load(_f)["paises"]}
except Exception:  # pragma: no cover
    PAISES = {}

ORDEM_GRUPOS = ["FAST", "MORAD", "TRANSP", "ALIM", "BENS", "SERV", "OUTROS", "GRID", "MEDIA"]

GRUPO_NOME = {
    "FAST": "Estimativa rápida (4 etapas)",
    "MORAD": "Moradia (aquecimento, água e resíduos)",
    "TRANSP": "Transporte e deslocamentos",
    "ALIM": "Alimentação",
    "BENS": "Bens e compras",
    "SERV": "Serviços e uso digital",
    "OUTROS": "Animais de estimação e outros",
    "GRID": "Rede elétrica do país",
    "MEDIA": "Média nacional por habitante",
}

# ---------------------------------------------------------------- rótulos ----
ROTULOS = {
    # Transporte
    "TR_CAR_KM_GAS": "Transporte — carro a gasolina, por quilômetro rodado",
    "TR_CAR_KM_DIESEL": "Transporte — carro a diesel, por quilômetro rodado",
    "TR_CAR_KM_HIBRIDO": "Transporte — carro híbrido (não plug-in), por quilômetro rodado",
    "TR_CAR_KM_ELETRICO": "Transporte — carro elétrico, por quilômetro rodado (rede média do país)",
    "TR_CAR_KM_GNV": "Transporte — carro a gás natural veicular (GNV), por quilômetro rodado",
    "TR_CAR_KM_LPG": "Transporte — carro a gás liquefeito de petróleo (GLP), por quilômetro rodado",
    "TR_LIT_GASOLINA": "Transporte — gasolina, por litro abastecido",
    "TR_LIT_DIESEL": "Transporte — diesel, por litro abastecido",
    "TR_LIT_ETANOL": "Transporte — etanol hidratado, por litro abastecido",
    "TR_M2_KWH": "Transporte — tração elétrica: usa automaticamente o fator da rede elétrica do país",
    "TR_RIDE_KM_APP": "Transporte — carro de aplicativo, por passageiro-quilômetro",
    "TR_RIDE_KM_TAXI": "Transporte — táxi, por passageiro-quilômetro",
    "TR_PASS_KM_ONIBUS_URB": "Transporte — ônibus urbano, por passageiro-quilômetro",
    "TR_PASS_KM_ONIBUS_INT": "Transporte — ônibus rodoviário / interestadual, por passageiro-quilômetro",
    "TR_PASS_KM_METRO": "Transporte — metrô e VLT, por passageiro-quilômetro",
    "TR_PASS_KM_TREM_URB": "Transporte — trem suburbano, por passageiro-quilômetro",
    "TR_PASS_KM_TREM_LH": "Transporte — trem de longa distância (elétrico), por passageiro-quilômetro",
    "TR_PASS_KM_BALSA": "Transporte — balsa ou ferry (sem carro), por passageiro-quilômetro",
    "TR_ACTIVE_KM": "Transporte — bicicleta, caminhada ou patinete: emissão zero de tração, por quilômetro",
    "TR_MICRO_KM": "Transporte — micromobilidade elétrica (patinete e bicicleta elétrica), por quilômetro",
    "TR_AIR_KM_CURTO_ECON": "Avião — voo curto (até 1.500 quilômetros), classe econômica, por passageiro-quilômetro",
    "TR_AIR_KM_LONGO_ECON": "Avião — voo longo, classe econômica, por passageiro-quilômetro",
    "TR_AIR_KM_DOMESTICO": "Avião — voo doméstico, por passageiro-quilômetro",
    "TR_AIR_MULT_ECON": "Avião — multiplicador da classe econômica (valor 1,0)",
    "TR_AIR_MULT_EXEC": "Avião — multiplicador da classe executiva (valor 1,65)",
    "TR_AIR_MULT_PRIMEIRA": "Avião — multiplicador da primeira classe (valor 2,2)",
    "TR_MOTO_KM_PEQ": "Transporte — motocicleta pequena ou ciclomotor, por quilômetro",
    "TR_MOTO_KM_MED": "Transporte — motocicleta média, por quilômetro",
    "TR_MOTO_KM_GRAN": "Transporte — motocicleta grande, por quilômetro",
    # Moradia
    "HEAT_KWH_GAS_NAT": "Moradia — gás natural de rua (aquecimento e cozinha), por quilowatt-hora usado",
    "HEAT_KWH_GAS_LITRAO": "Moradia — gás de botijão (GLP), por metro cúbico equivalente",
    "HEAT_KWH_OLEO": "Moradia — óleo combustível para aquecimento, por quilowatt-hora usado",
    "HEAT_KWH_LENHA": "Moradia — lenha e biomassa, por quilowatt-hora usado",
    "HEAT_KWH_PELLET": "Moradia — pellets de biomassa, por quilowatt-hora usado",
    "HEAT_KWH_BOMBA": "Moradia — bomba de calor: lance os quilowatt-hora elétricos (o app converte usando a rede e o COP)",
    "HEAT_COP_PADRAO": "Moradia — eficiência típica da bomba de calor (COP: calor entregue por quilowatt-hora elétrico)",
    "WATER_M3": "Moradia — água de rede (abastecimento e tratamento de esgoto), por metro cúbico",
    "WASTE_KG_MISTO": "Moradia — resíduo misto enviado a aterro, por quilograma",
    "WASTE_KG_COMPOSTA": "Moradia — resíduo orgânico compostado, por quilograma",
    "WASTE_KG_RECICLA": "Moradia — coleta seletiva e reciclagem, por quilograma",
    # Alimentação
    "MEAL_BOVINO": "Alimentação — refeição com carne bovina, por refeição",
    "MEAL_AVE": "Alimentação — refeição com frango ou ave, por refeição",
    "MEAL_PEIXE": "Alimentação — refeição com peixe, por refeição",
    "MEAL_OVO_LACTEO": "Alimentação — refeição com ovos e laticínios, por refeição",
    "MEAL_VEGETARIANO": "Alimentação — refeição vegetariana, por refeição",
    "MEAL_VEGANO": "Alimentação — refeição vegana, por refeição",
    "MEAL_RESTAURANTE": "Alimentação — refeição fora de casa (média), por refeição",
    "MEAL_MULT_LOCAL": "Alimentação — multiplicador por preferência de produtos locais (valor 0,92)",
    # Bens
    "GOODS_ROUPA": "Bens — peça de vestuário, por unidade comprada",
    "GOODS_CALCADO": "Bens — par de calçados, por unidade comprada",
    "GOODS_MOBILIARIO": "Bens — móvel ou equipamento doméstico, por unidade comprada",
    "GOODS_SMARTPHONE": "Bens — smartphone (fabricação e ciclo de vida), por unidade",
    "GOODS_NOTEBOOK": "Bens — notebook (ciclo de vida), por unidade",
    "GOODS_ELETRO": "Bens — eletrodoméstico, por unidade",
    # Serviços
    "SERV_KWH_DIG": "Serviços — uso digital (streaming, nuvem): lance os quilowatt-hora (o app usa a rede do país)",
    "SERV_R_015": "Serviços — gastos gerais em serviços e bens, por real gasto (R$)",
    # Outros
    "G_PET_CAO_ANO": "Outros — cão de porte médio (ração e cuidados), por ano",
    "G_PET_GATO_ANO": "Outros — gato (ração e cuidados), por ano",
    # Estimativa rápida
    "FAST_HOME_KWH_FLAT": "Estimativa rápida — eletricidade anual de apartamento (cerca de 3.000 quilowatt-hora por ano)",
    "FAST_HOME_KWH_SMALL": "Estimativa rápida — eletricidade anual de casa pequena, 1 a 2 quartos (cerca de 4.500 quilowatt-hora por ano)",
    "FAST_HOME_KWH_MED": "Estimativa rápida — eletricidade anual de casa média, 3 quartos (cerca de 6.500 quilowatt-hora por ano)",
    "FAST_HOME_KWH_LARGE": "Estimativa rápida — eletricidade anual de casa grande, 4 quartos ou mais (cerca de 9.500 quilowatt-hora por ano)",
    "FAST_HEAT_GAS_SHARE": "Estimativa rápida — fração da energia da moradia destinada a aquecimento a gás (70 por cento)",
    "FAST_DRIVE_BUCKETS_KM": "Estimativa rápida — faixas anuais de quilometragem dirigida (valores de referência; as faixas ficam no motor de cálculo)",
    "FAST_FLIGHT_SHORT_RT": "Estimativa rápida — voo curto de ida e volta (cerca de 500 quilogramas de CO₂ equivalente por viagem)",
    "FAST_FLIGHT_LONG_RT": "Estimativa rápida — voo longo de ida e volta (cerca de 2.500 quilogramas de CO₂ equivalente por viagem)",
    "FAST_GOODS_SHARE": "Estimativa rápida — bens e serviços como fração da média nacional (35 por cento)",
    "FAST_HOME_SHARE_ADJ": "Estimativa rápida — rateio do domicílio: cada pessoa adicional soma 0,75 ao divisor",
}

# ------------------------------------------------------------ explicações ----
UNID_TXT = {
    "km": "quilômetros rodados", "L": "litros de combustível", "kWh": "quilowatt-hora (kWh)",
    "kWh/ano": "quilowatt-hora por ano", "km/ano": "quilômetros por ano", "m3": "metros cúbicos (m³)",
    "coef": "coeficiente adimensional (fração ou multiplicador)", "refeicao": "refeições",
    "unidade": "unidades compradas", "R$": "reais gastos (R$)", "ano": "anos (por animal)",
    "viagem": "viagens de ida e volta", "tCO2e/pessoa/ano": "toneladas de CO₂ equivalente por pessoa ao ano",
}

USO = {
    "FAST": "É usado na estimativa rápida em 4 etapas (moradia, direção, voos e dieta), quando não há lançamento detalhado.",
    "TRANSP": "É aplicado na apuração detalhada de transporte: a quantidade lançada é multiplicada por este fator para obter a emissão do lançamento.",
    "MORAD": "É aplicado na apuração detalhada de moradia (aquecimento, água e resíduos): a quantidade lançada é multiplicada por este fator.",
    "ALIM": "É aplicado na apuração detalhada de alimentação: multiplica o número de refeições lançadas.",
    "BENS": "É aplicado na apuração detalhada de bens: multiplica o número de unidades compradas.",
    "SERV": "É aplicado na apuração detalhada de serviços e de uso digital.",
    "OUTROS": "É aplicado na apuração detalhada de animais de estimação e outros itens.",
    "GRID": "É usado sempre que um lançamento consome eletricidade da rede (moradia, bomba de calor, carro elétrico, uso digital) e também na estimativa rápida.",
    "MEDIA": "Serve de referência comparativa: a pontuação de 0 a 100 e os painéis comparam a sua pegada anualizada com esta média.",
}

SIGN_ESPECIAL = {
    "TR_M2_KWH": "Este fator não tem valor próprio: o motor de cálculo substitui automaticamente pelo fator da rede elétrica do país selecionado.",
    "HEAT_KWH_BOMBA": "A bomba de calor consome eletricidade: o motor converte o calor entregue em quilowatt-hora elétricos usando o COP e aplica o fator da rede do país.",
    "SERV_KWH_DIG": "Este fator não tem valor próprio: o consumo digital é convertido em quilowatt-hora e calculado com o fator da rede elétrica do país.",
    "FAST_DRIVE_BUCKETS_KM": "Valor de referência (zero): as faixas anuais de direção (0, 4.000, 8.000 e 16.000 quilômetros) e os fatores de cada faixa são definidos no motor de cálculo.",
    "HEAT_COP_PADRAO": "COP (coeficiente de performance): quantos quilowatt-hora de calor a bomba entrega para cada quilowatt-hora de eletricidade consumido.",
    "TR_AIR_MULT_ECON": "Multiplicador aplicado à emissão do voo conforme a classe viajada; a classe econômica é a referência (1,0).",
    "TR_AIR_MULT_EXEC": "Multiplicador aplicado à emissão do voo conforme a classe viajada: a executiva ocupa mais espaço e peso por passageiro.",
    "TR_AIR_MULT_PRIMEIRA": "Multiplicador aplicado à emissão do voo conforme a classe viajada: a primeira classe é a que mais emissões aloca por passageiro.",
    "FAST_HOME_SHARE_ADJ": "Regra de rateio do domicílio: o divisor total é 1 + 0,75 × (número de pessoas − 1), para que moradias compartilhadas dividam as emissões de forma justa.",
    "MEAL_MULT_LOCAL": "Reduz em 8 por cento a emissão das refeições quando há preferência por produtos locais e de proximidade.",
}


def _get(row, chave, padrao=""):
    if not row:
        return padrao
    try:
        v = row[chave]
    except Exception:
        return padrao
    return padrao if v is None else v


def rotulo(codigo, row=None):
    """Nome completo, em português, do fator identificado por `codigo`."""
    if codigo.startswith("GRID_"):
        iso = codigo[5:]
        return f"Rede elétrica — {PAISES.get(iso, iso)}: emissões por quilowatt-hora de eletricidade consumida"
    if codigo.startswith("MEDIA_"):
        iso = codigo[6:]
        return f"Média nacional por habitante — {PAISES.get(iso, iso)}: pegada anual de cada residente (referência de comparação)"
    return ROTULOS.get(codigo) or _get(row, "descricao") or codigo


def unidade_texto(unidade):
    return UNID_TXT.get(unidade or "", unidade or "—")


def explicacao(codigo, row=None):
    """Parágrafo explicativo: o que é, onde o app usa, unidade e fonte."""
    grupo = _get(row, "grupo")
    fonte = _get(row, "fonte")
    unidade = _get(row, "unidade")
    if codigo.startswith("GRID_"):
        iso = codigo[5:]
        sign = (f"É a emissão média, em quilogramas de CO₂ equivalente, para entregar um quilowatt-hora de "
                f"eletricidade na rede de {PAISES.get(iso, iso)} — inclui a geração nas usinas e as perdas de "
                f"transmissão e distribuição.")
        grupo = grupo or "GRID"
    elif codigo.startswith("MEDIA_"):
        iso = codigo[6:]
        sign = (f"É a pegada de carbono anual média de cada residente de {PAISES.get(iso, iso)}, em toneladas de "
                f"CO₂ equivalente, calculada a partir de estatísticas nacionais de energia e consumo.")
        grupo = grupo or "MEDIA"
    else:
        sign = SIGN_ESPECIAL.get(codigo)
        if not sign:
            d = _get(row, "descricao") or ROTULOS.get(codigo, codigo)
            sign = f"O que representa: {d[0].lower() + d[1:] if d else codigo}."
        grupo = grupo or "FAST"
    partes = [sign, USO.get(grupo, "")]
    if unidade:
        partes.append(f"Unidade do valor: {unidade_texto(unidade)}.")
    if fonte:
        partes.append(f"Fonte registrada: {fonte}.")
        if fonte.startswith("ESTIMATIVA") or "Calibração" in fonte:
            partes.append("Valor calibrado pelo CO2calc e totalmente editável — substitua por um dado oficial quando houver.")
    return " ".join(p for p in partes if p)


def ordenar(rows):
    """Ordena linhas de fatores por grupo amigável e, depois, por código."""
    def chave(r):
        g = _get(r, "grupo", "")
        return (ORDEM_GRUPOS.index(g) if g in ORDEM_GRUPOS else 99, _get(r, "codigo", ""))
    return sorted(rows, key=chave)
