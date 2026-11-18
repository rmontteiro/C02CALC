# Metodologia de cálculo CO2calc

O CO2calc calcula pegada de carbono pessoal em **kgCO₂e** com a relação
padrão de inventários de gases de efeito estufa:

> **E = atividade × fator × fração de atribuição (rateio)**

## 1. Limites do inventário
* Escopo temporal: **12 meses** por ano de referência; lançamentos podem ser **mensais** (o mês representa aquele consumo) ou **anuais** (somam-se ao total do ano).
* Unidades: energia (kWh/m³), massa de combustível (L/kg), distância (km), refeições, itens de consumo e resíduos (kg).
* Resultados em **CO₂-equivalente** (gases agregados por GWP-100).

## 2. Conjuntos de fatores (fontes públicas de dados)
| Família | Fonte | Observação |
|---|---|---|
| Combustíveis e veículos (kg/km, kg/L) | **Defra/DESNZ** GHG Conversion Factors 2023 (OGL) | inclui well-to-tank (WTT) |
| Voo por passageiro-km + multiplicadores de classe | Defra/EPA (aprox.) | radiative forcing aproximado incluso |
| Rede elétrica por país (kgCO₂e/kWh) | **IEA/Ember** + dados nacionais (aprox., 2024) | geração + perdas T&D + montante |
| Média nacional per capita (tCO₂e) | **OECD** GHG Footprint Indicators 2022 (CC BY 4.0) / **Defra** 2023 (OGL) | consumo-based, arredondada |
| Alimentos por refeição, bens, resíduos, água | estimativas publicadas (POF/WRI, DEFRA waste) | marcadas `ESTIMATIVA` na coluna `fonte` |

**Atribuição:** os dados OECD são usados sob **CC BY 4.0** e Defra sob **OGL v3** — as
atribuições acima devem acompanhar redistribuições dos fatores. Valores aproximados
são editáveis no app (aba Usuários → Editar fatores) e persistidos no banco com
`fonte` e rastreabilidade por linha.

## 3. Estimativa rápida (4 etapas)
Blocos e coeficientes atuais (tabela `fatores`, grupo `FAST`, todos editáveis):

1. **Moradia** — porte do imóvel define energia anual estimada (3.000 / 4.500 / 6.500 / 9.500 kWh-eq);
   o tipo de aquecimento divide a demanda entre gás/óleo/eletricidade/bomba de calor (COP≈3);
   a parte elétrica usa o fator GRID do país. Rateio do domicílio: `÷ (1 + 0,75·(n−1))`.
2. **Direção** — buckets de 0 / 4.000 / 8.000 / 16.000 km × fator por combustível (WTT incluso).
3. **Voos** — 500 kgCO₂e por ida-e-volta curta, 2.500 kg por longa (calibração CO2calc).
4. **Dieta** — 2,9 / 2,15 / 1,6 / 1,25 tCO₂e/pessoa/ano (onívora frequente → vegana).

**Bens & serviços** completam o total como fração (35 %) da média nacional —
escalamento por país, coerente com pegada consumption-based.

O resultado compara-se à média nacional (`MEDIA_<iso>`) e gera score 0–100:

```
ratio  = anualizado per capita (t) ÷ média nacional (t)
score  = 100 · (1,35 − ratio) ÷ 1,10   , limitado a [0, 100]
```

Bandas: ≥80 Excelente · ≥60 Muito bom · ≥40 Razoável · ≥20 Alto · <20 Crítico.

## 4. Inventário detalhado (menu Lançar)
Cada lançamento grava um **snapshot auditável** (`valor`, `unidade`, `fator` aplicado,
`pessoas`, `co2e_kg`, origem e período) vinculado a um nó da Taxonomia Mundial de
Pegada de Carbono Individual (586 nós; setores A–J; 33 métodos; regras R01–R14),
com a regra R03 (rateio) materializada no campo `pessoas`.

## 5. Validação e limitações
* Validação cruzada com `tests/test_smoke.py` (taxonomia, rateio, mensal×anual, score, PDFs).
* **Não** substitui inventário normativo (GHG Protocol / ISO 14064-2) nem relatórios de escopo organizacional.
* Fatores de rede/médias são aproximações para uso educativo; para decisões formais,
  importe os conjuntos completos das fontes primárias (links em `fatores.json.fonte`).
