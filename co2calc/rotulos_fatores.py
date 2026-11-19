# -*- coding: utf-8 -*-
"""Rótulos e explicações, em português completo, dos fatores de emissão.

Transforma os códigos internos (ex.: FAST_HOME_KWH_LARGE, GRID_BR) em nomes
intuitivos e fornece um parágrafo explicativo para cada fator, usado no painel
"Editar fatores de emissão" da tela Usuários e no formulário de lançamento.

Versões English (en-US) y Español (es-AR) vivem em ROTULOS_ALT; frases
estruturais (grupos, unidades, uso) são resolvidas via co2calc.i18n.
"""
import json, os

from . import i18n as I

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
    "MEAL_BOVINO": "Alimentação — refeição com carne bovina, por refeição",
    "MEAL_AVE": "Alimentação — refeição com frango ou ave, por refeição",
    "MEAL_PEIXE": "Alimentação — refeição com peixe, por refeição",
    "MEAL_OVO_LACTEO": "Alimentação — refeição com ovos e laticínios, por refeição",
    "MEAL_VEGETARIANO": "Alimentação — refeição vegetariana, por refeição",
    "MEAL_VEGANO": "Alimentação — refeição vegana, por refeição",
    "MEAL_RESTAURANTE": "Alimentação — refeição fora de casa (média), por refeição",
    "MEAL_MULT_LOCAL": "Alimentação — multiplicador por preferência de produtos locais (valor 0,92)",
    "GOODS_ROUPA": "Bens — peça de vestuário, por unidade comprada",
    "GOODS_CALCADO": "Bens — par de calçados, por unidade comprada",
    "GOODS_MOBILIARIO": "Bens — móvel ou equipamento doméstico, por unidade comprada",
    "GOODS_SMARTPHONE": "Bens — smartphone (fabricação e ciclo de vida), por unidade",
    "GOODS_NOTEBOOK": "Bens — notebook (ciclo de vida), por unidade",
    "GOODS_ELETRO": "Bens — eletrodoméstico, por unidade",
    "SERV_KWH_DIG": "Serviços — uso digital (streaming, nuvem): lance os quilowatt-hora (o app usa a rede do país)",
    "SERV_R_015": "Serviços — gastos gerais em serviços e bens, por real gasto (R$)",
    "G_PET_CAO_ANO": "Outros — cão de porte médio (ração e cuidados), por ano",
    "G_PET_GATO_ANO": "Outros — gato (ração e cuidados), por ano",
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

_EN = {
    "TR_CAR_KM_GAS": "Transport — gasoline car, per kilometer driven",
    "TR_CAR_KM_DIESEL": "Transport — diesel car, per kilometer driven",
    "TR_CAR_KM_HIBRIDO": "Transport — hybrid car (non plug-in), per kilometer driven",
    "TR_CAR_KM_ELETRICO": "Transport — electric car, per kilometer driven (country grid average)",
    "TR_CAR_KM_GNV": "Transport — natural gas (CNG) car, per kilometer driven",
    "TR_CAR_KM_LPG": "Transport — LPG car, per kilometer driven",
    "TR_LIT_GASOLINA": "Transport — gasoline, per liter refueled",
    "TR_LIT_DIESEL": "Transport — diesel, per liter refueled",
    "TR_LIT_ETANOL": "Transport — hydrous ethanol, per liter refueled",
    "TR_M2_KWH": "Transport — electric traction: automatically uses the country power-grid factor",
    "TR_RIDE_KM_APP": "Transport — ride-hailing car, per passenger-kilometer",
    "TR_RIDE_KM_TAXI": "Transport — taxi, per passenger-kilometer",
    "TR_PASS_KM_ONIBUS_URB": "Transport — city bus, per passenger-kilometer",
    "TR_PASS_KM_ONIBUS_INT": "Transport — intercity coach, per passenger-kilometer",
    "TR_PASS_KM_METRO": "Transport — subway and light rail, per passenger-kilometer",
    "TR_PASS_KM_TREM_URB": "Transport — commuter train, per passenger-kilometer",
    "TR_PASS_KM_TREM_LH": "Transport — long-distance electric train, per passenger-kilometer",
    "TR_PASS_KM_BALSA": "Transport — ferry (without car), per passenger-kilometer",
    "TR_ACTIVE_KM": "Transport — bike, walking or kick scooter: zero traction emissions, per kilometer",
    "TR_MICRO_KM": "Transport — electric micromobility (kick scooter and e-bike), per kilometer",
    "TR_AIR_KM_CURTO_ECON": "Flights — short-haul (up to 1,500 km), economy class, per passenger-kilometer",
    "TR_AIR_KM_LONGO_ECON": "Flights — long-haul, economy class, per passenger-kilometer",
    "TR_AIR_KM_DOMESTICO": "Flights — domestic flight, per passenger-kilometer",
    "TR_AIR_MULT_ECON": "Flights — economy class multiplier (value 1.0)",
    "TR_AIR_MULT_EXEC": "Flights — business class multiplier (value 1.65)",
    "TR_AIR_MULT_PRIMEIRA": "Flights — first class multiplier (value 2.2)",
    "TR_MOTO_KM_PEQ": "Transport — small motorcycle or moped, per kilometer",
    "TR_MOTO_KM_MED": "Transport — mid-size motorcycle, per kilometer",
    "TR_MOTO_KM_GRAN": "Transport — large motorcycle, per kilometer",
    "HEAT_KWH_GAS_NAT": "Home — piped natural gas (heating and cooking), per kilowatt-hour used",
    "HEAT_KWH_GAS_LITRAO": "Home — bottled gas (LPG), per equivalent cubic meter",
    "HEAT_KWH_OLEO": "Home — heating oil, per kilowatt-hour used",
    "HEAT_KWH_LENHA": "Home — firewood and biomass, per kilowatt-hour used",
    "HEAT_KWH_PELLET": "Home — biomass pellets, per kilowatt-hour used",
    "HEAT_KWH_BOMBA": "Home — heat pump: log the electric kilowatt-hours (the app converts using grid and COP)",
    "HEAT_COP_PADRAO": "Home — typical heat-pump efficiency (COP: heat delivered per electric kilowatt-hour)",
    "WATER_M3": "Home — tap water (supply and sewage treatment), per cubic meter",
    "WASTE_KG_MISTO": "Home — mixed waste sent to landfill, per kilogram",
    "WASTE_KG_COMPOSTA": "Home — composted organic waste, per kilogram",
    "WASTE_KG_RECICLA": "Home — recycling collection, per kilogram",
    "MEAL_BOVINO": "Food — beef meal, per meal",
    "MEAL_AVE": "Food — chicken meal, per meal",
    "MEAL_PEIXE": "Food — fish meal, per meal",
    "MEAL_OVO_LACTEO": "Food — eggs and dairy meal, per meal",
    "MEAL_VEGETARIANO": "Food — vegetarian meal, per meal",
    "MEAL_VEGANO": "Food — vegan meal, per meal",
    "MEAL_RESTAURANTE": "Food — eating out (average), per meal",
    "MEAL_MULT_LOCAL": "Food — local-produce preference multiplier (value 0.92)",
    "GOODS_ROUPA": "Goods — clothing item, per purchased unit",
    "GOODS_CALCADO": "Goods — pair of shoes, per purchased unit",
    "GOODS_MOBILIARIO": "Goods — furniture or home appliance, per purchased unit",
    "GOODS_SMARTPHONE": "Goods — smartphone (manufacturing and life cycle), per unit",
    "GOODS_NOTEBOOK": "Goods — laptop (life cycle), per unit",
    "GOODS_ELETRO": "Goods — major home appliance, per unit",
    "SERV_KWH_DIG": "Services — digital use (streaming, cloud): log the kilowatt-hours (the app uses the country grid)",
    "SERV_R_015": "Services — general spending on services and goods, per real spent (R$)",
    "G_PET_CAO_ANO": "Others — medium-size dog (food and care), per year",
    "G_PET_GATO_ANO": "Others — cat (food and care), per year",
    "FAST_HOME_KWH_FLAT": "Quick estimate — yearly apartment electricity (about 3,000 kWh per year)",
    "FAST_HOME_KWH_SMALL": "Quick estimate — yearly small-house electricity, 1-2 bedrooms (about 4,500 kWh per year)",
    "FAST_HOME_KWH_MED": "Quick estimate — yearly medium-house electricity, 3 bedrooms (about 6,500 kWh per year)",
    "FAST_HOME_KWH_LARGE": "Quick estimate — yearly large-house electricity, 4+ bedrooms (about 9,500 kWh per year)",
    "FAST_HEAT_GAS_SHARE": "Quick estimate — share of home energy used for gas heating (70 percent)",
    "FAST_DRIVE_BUCKETS_KM": "Quick estimate — yearly driving mileage bands (reference values; bands live in the engine)",
    "FAST_FLIGHT_SHORT_RT": "Quick estimate — short-haul round-trip flight (about 500 kg CO₂e per trip)",
    "FAST_FLIGHT_LONG_RT": "Quick estimate — long-haul round-trip flight (about 2,500 kg CO₂e per trip)",
    "FAST_GOODS_SHARE": "Quick estimate — goods and services as a share of the national average (35 percent)",
    "FAST_HOME_SHARE_ADJ": "Quick estimate — household sharing rule: each extra person adds 0.75 to the divisor",
}

_ES = {
    "TR_CAR_KM_GAS": "Transporte — auto a nafta (gasolina), por kilómetro recorrido",
    "TR_CAR_KM_DIESEL": "Transporte — auto a diesel, por kilómetro recorrido",
    "TR_CAR_KM_HIBRIDO": "Transporte — auto híbrido (no enchufable), por kilómetro recorrido",
    "TR_CAR_KM_ELETRICO": "Transporte — auto eléctrico, por kilómetro recorrido (red media del país)",
    "TR_CAR_KM_GNV": "Transporte — auto a gas natural comprimido (GNC), por kilómetro recorrido",
    "TR_CAR_KM_LPG": "Transporte — auto a gas envasado (GLP), por kilómetro recorrido",
    "TR_LIT_GASOLINA": "Transporte — nafta (gasolina), por litro cargado",
    "TR_LIT_DIESEL": "Transporte — diesel, por litro cargado",
    "TR_LIT_ETANOL": "Transporte — etanol hidratado, por litro cargado",
    "TR_M2_KWH": "Transporte — tracción eléctrica: usa automáticamente el factor de la red eléctrica del país",
    "TR_RIDE_KM_APP": "Transporte — auto de aplicación, por pasajero-kilómetro",
    "TR_RIDE_KM_TAXI": "Transporte — taxi, por pasajero-kilómetro",
    "TR_PASS_KM_ONIBUS_URB": "Transporte — colectivo urbano, por pasajero-kilómetro",
    "TR_PASS_KM_ONIBUS_INT": "Transporte — micro / ómnibus de larga distancia, por pasajero-kilómetro",
    "TR_PASS_KM_METRO": "Transporte — subte y tren ligero, por pasajero-kilómetro",
    "TR_PASS_KM_TREM_URB": "Transporte — tren suburbano, por pasajero-kilómetro",
    "TR_PASS_KM_TREM_LH": "Transporte — tren eléctrico de larga distancia, por pasajero-kilómetro",
    "TR_PASS_KM_BALSA": "Transporte — ferry (sin auto), por pasajero-kilómetro",
    "TR_ACTIVE_KM": "Transporte — bicicleta, caminata o monopatín: cero emisiones de tracción, por kilómetro",
    "TR_MICRO_KM": "Transporte — micromovilidad eléctrica (monopatín y bici eléctrica), por kilómetro",
    "TR_AIR_KM_CURTO_ECON": "Avión — vuelo corto (hasta 1.500 km), clase económica, por pasajero-kilómetro",
    "TR_AIR_KM_LONGO_ECON": "Avión — vuelo largo, clase económica, por pasajero-kilómetro",
    "TR_AIR_KM_DOMESTICO": "Avión — vuelo doméstico, por pasajero-kilómetro",
    "TR_AIR_MULT_ECON": "Avión — multiplicador de clase económica (valor 1,0)",
    "TR_AIR_MULT_EXEC": "Avión — multiplicador de clase ejecutiva (valor 1,65)",
    "TR_AIR_MULT_PRIMEIRA": "Avión — multiplicador de primera clase (valor 2,2)",
    "TR_MOTO_KM_PEQ": "Transporte — moto chica o ciclomotor, por kilómetro",
    "TR_MOTO_KM_MED": "Transporte — moto mediana, por kilómetro",
    "TR_MOTO_KM_GRAN": "Transporte — moto grande, por kilómetro",
    "HEAT_KWH_GAS_NAT": "Vivienda — gas natural de caño (calefacción y cocina), por kilovatio-hora usado",
    "HEAT_KWH_GAS_LITRAO": "Vivienda — gas envasado (cilindro), por metro cúbico equivalente",
    "HEAT_KWH_OLEO": "Vivienda — gasoil de calefacción, por kilovatio-hora usado",
    "HEAT_KWH_LENHA": "Vivienda — leña y biomasa, por kilovatio-hora usado",
    "HEAT_KWH_PELLET": "Vivienda — pellets de biomasa, por kilovatio-hora usado",
    "HEAT_KWH_BOMBA": "Vivienda — bomba de calor: registrá los kilovatios-hora eléctricos (la app convierte con la red y el COP)",
    "HEAT_COP_PADRAO": "Vivienda — eficiencia típica de la bomba de calor (COP: calor entregado por kilovatio-hora eléctrico)",
    "WATER_M3": "Vivienda — agua de red (provisión y tratamiento de líquidos cloacales), por metro cúbico",
    "WASTE_KG_MISTO": "Vivienda — residuo mixto enviado a relleno sanitario, por kilogramo",
    "WASTE_KG_COMPOSTA": "Vivienda — residuo orgánico compostado, por kilogramo",
    "WASTE_KG_RECICLA": "Vivienda — recolección separada y reciclaje, por kilogramo",
    "MEAL_BOVINO": "Alimentación — comida con carne vacuna, por comida",
    "MEAL_AVE": "Alimentación — comida con pollo, por comida",
    "MEAL_PEIXE": "Alimentación — comida con pescado, por comida",
    "MEAL_OVO_LACTEO": "Alimentación — comida con huevos y lácteos, por comida",
    "MEAL_VEGETARIANO": "Alimentación — comida vegetariana, por comida",
    "MEAL_VEGANO": "Alimentación — comida vegana, por comida",
    "MEAL_RESTAURANTE": "Alimentación — comida afuera (promedio), por comida",
    "MEAL_MULT_LOCAL": "Alimentación — multiplicador por preferencia de productos locales (valor 0,92)",
    "GOODS_ROUPA": "Bienes — prenda de vestir, por unidad comprada",
    "GOODS_CALCADO": "Bienes — par de zapatos, por unidad comprada",
    "GOODS_MOBILIARIO": "Bienes — mueble o artefacto del hogar, por unidad comprada",
    "GOODS_SMARTPHONE": "Bienes — smartphone (fabricación y ciclo de vida), por unidad",
    "GOODS_NOTEBOOK": "Bienes — notebook (ciclo de vida), por unidad",
    "GOODS_ELETRO": "Bienes — electrodoméstico, por unidad",
    "SERV_KWH_DIG": "Servicios — uso digital (streaming, nube): registrá los kilovatios-hora (la app usa la red del país)",
    "SERV_R_015": "Servicios — gastos generales en servicios y bienes, por moneda local gastada",
    "G_PET_CAO_ANO": "Otros — perro mediano (alimento y cuidados), por año",
    "G_PET_GATO_ANO": "Otros — gato (alimento y cuidados), por año",
    "FAST_HOME_KWH_FLAT": "Estimación rápida — electricidad anual de departamento (unos 3.000 kWh por año)",
    "FAST_HOME_KWH_SMALL": "Estimación rápida — electricidad anual de casa chica, 1-2 dormitorios (unos 4.500 kWh por año)",
    "FAST_HOME_KWH_MED": "Estimación rápida — electricidad anual de casa mediana, 3 dormitorios (unos 6.500 kWh por año)",
    "FAST_HOME_KWH_LARGE": "Estimación rápida — electricidad anual de casa grande, 4+ dormitorios (unos 9.500 kWh por año)",
    "FAST_HEAT_GAS_SHARE": "Estimación rápida — fracción de la energía de la vivienda para calefacción a gas (70 por ciento)",
    "FAST_DRIVE_BUCKETS_KM": "Estimación rápida — franjas anuales de kilómetro manejado (valores de referencia; las franjas están en el motor)",
    "FAST_FLIGHT_SHORT_RT": "Estimación rápida — vuelo corto de ida y vuelta (unos 500 kg de CO₂e por viaje)",
    "FAST_FLIGHT_LONG_RT": "Estimación rápida — vuelo largo de ida y vuelta (unos 2.500 kg de CO₂e por viaje)",
    "FAST_GOODS_SHARE": "Estimación rápida — bienes y servicios como fracción del promedio nacional (35 por ciento)",
    "FAST_HOME_SHARE_ADJ": "Estimación rápida — reparto del hogar: cada persona adicional suma 0,75 al divisor",
}

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

GRID_SIGN = ("É a emissão média, em quilogramas de CO₂ equivalente, para entregar um quilowatt-hora de "
             "eletricidade na rede de {pais} — inclui a geração nas usinas e as perdas de transmissão e distribuição.")
MEDIA_SIGN = ("É a pegada de carbono anual média de cada residente de {pais}, em toneladas de CO₂ equivalente, "
              "calculada a partir de estatísticas nacionais de energia e consumo.")
FONTE_NOTE = ("Valor calibrado pelo CO2calc e totalmente editável — substitua por um dado oficial quando houver.")


def _get(row, chave, padrao=""):
    if not row:
        return padrao
    try:
        v = row[chave]
    except Exception:
        return padrao
    return padrao if v is None else v


def rotulo(codigo, row=None):
    """Nome completo e localizado do fator identificado por `codigo`."""
    lang = I.get_lang()
    if codigo.startswith("GRID_"):
        iso = codigo[5:]
        return I.FM("Rede elétrica — {pais}: emissões por quilowatt-hora de eletricidade consumida",
                   pais=PAISES.get(iso, iso))
    if codigo.startswith("MEDIA_"):
        iso = codigo[6:]
        return I.FM("Média nacional por habitante — {pais}: pegada anual de cada residente (referência de comparação)",
                   pais=PAISES.get(iso, iso))
    if lang == "en":
        return _EN.get(codigo) or ROTULOS.get(codigo) or _get(row, "descricao") or codigo
    if lang == "es":
        return _ES.get(codigo) or ROTULOS.get(codigo) or _get(row, "descricao") or codigo
    return ROTULOS.get(codigo) or _get(row, "descricao") or codigo


def grupo_nome(grupo):
    return I.T(GRUPO_NOME.get(grupo, grupo or ""))


def unidade_texto(unidade):
    return I.T(UNID_TXT.get(unidade or "", unidade or "—"))


def explicacao(codigo, row=None):
    """Parágrafo localizável: o que é, onde o app usa, unidade e fonte."""
    row = row or {}
    grupo = _get(row, "grupo")
    fonte = _get(row, "fonte")
    unidade = _get(row, "unidade")
    pais = PAISES.get(codigo[5:], codigo[5:]) if codigo.startswith("GRID_") else \
        PAISES.get(codigo[6:], codigo[6:]) if codigo.startswith("MEDIA_") else ""
    if codigo.startswith("GRID_"):
        sign, grupo = I.FM(GRID_SIGN, pais=pais), grupo or "GRID"
    elif codigo.startswith("MEDIA_"):
        sign, grupo = I.FM(MEDIA_SIGN, pais=pais), grupo or "MEDIA"
    else:
        sign = SIGN_ESPECIAL.get(codigo)
        if not sign:
            d = _get(row, "descricao") or ROTULOS.get(codigo, codigo)
            sign = I.FM("O que representa: {d}.", d=d[0].lower() + d[1:])
        grupo = grupo or "FAST"
    partes = [sign, I.T(USO.get(grupo, ""))]
    if unidade:
        partes.append(I.FM("Unidade do valor: {u}.", u=unidade_texto(unidade)))
    if fonte:
        partes.append(I.FM("Fonte registrada: {f}.", f=fonte))
        if fonte.startswith("ESTIMATIVA") or "Calibração" in fonte:
            partes.append(I.T(FONTE_NOTE))
    return " ".join(p for p in partes if p)


def ordenar(rows):
    """Ordena linhas de fatores por grupo amigável e, depois, por código."""
    def chave(r):
        g = _get(r, "grupo", "")
        return (ORDEM_GRUPOS.index(g) if g in ORDEM_GRUPOS else 99, _get(r, "codigo", ""))
    return sorted(rows, key=chave)
