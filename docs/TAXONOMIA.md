# Taxonomia de emissões utilizada pelo CO2calc

> **Referência-mestre:** *Minha Pegada — Taxonomia Mundial de Pegada de Carbono Individual —
> Inventário individual de gases de efeito estufa*. A planilha original está versionada neste
> repositório em [`docs/taxonomia/`](taxonomia/) e é a fonte única dos seeds do aplicativo.

## Identificação da versão

| Campo | Valor |
|---|---|
| Arquivo | `docs/taxonomia/Taxonomia_Mundial_Pegada_Carbono_Individual.xlsx` |
| SHA-256 | `bf70ee0eee96a73d170a422eea499a831109f8323eb82599fe49723f9b58f032` |
| Tamanho | 106.817 bytes |
| Revisão obtida | 2026-11-18 |
| Unidades de referência | Inventário bruto de consumo atribuível a uma pessoa, por período |

O hash é gravado no banco do app (tabela `ajustes`, chave `taxonomia_sha256`) e exibido na aba
**Usuários → Banco de dados local** — qualquer usuário pode verificar se seu `co2calc.db`
corresponde exatamente a esta planilha.

## Estrutura da planilha (10 abas)

| Aba | Registros | O que contém |
|---|---:|---|
| Guia | 11 | fluxo de decisão: escolher atividade → contexto → método/fator → cálculo (`atividade × fator × fração`) → lacunas e limites |
| **Taxonomia** | **586** | árvore de 4 níveis: **106 agregadores + 470 atividades + 8 indicadores + 2 pendências** |
| Métodos | 33 | métodos de cálculo por tipo de atividade (TR_CAR, TR_AIR, GRID, MEAL, GOODS, SERV, WASTE…) |
| Dimensões | 38 | atributos de contexto em 12 temas (Localização, Mobilidade, Energia, Fluidos, Alimentação, Duráveis, Saneamento, Resíduos, Serviços, Digital, Inventário, Período) |
| Geografias | 250 | países/territórios ISO 3166-1 (alfa-2/3/numérico) + orientação de localização do fator |
| Regras | 16 | R01–R16: atribuição e dupla contagem (rateio, ciclos de vida, eletricidade geográfica × contratual, serviços combinados etc.) |
| Exemplos | 12 | casos de enquadramento com códigos + método + regra |
| COICOP | 15 | vínculo ONU COICOP 2018 ↔ setores da taxonomia |
| Fatores | — | *modelo* de cadastro de fatores (19 campos: valor, unidade, GWP, fases, fonte, vigência…) |
| Fontes | 21 | referências normativas (abaixo) |

### Setores de nível 1 (perímetro principal A–G; paralelos H–J)

| Código | Setor | | Código | Setor |
|---|---|---|---|---|
| **A** | Transportes | | **F** | Resíduos e fim de vida |
| **B** | Moradia, energia e utilidades | | **G** | Animais domésticos e autoconsumo |
| **C** | Alimentação, bebidas e tabaco | | **H** | Serviços coletivos e consumo financiado por terceiros |
| **D** | Bens, vestuário e equipamentos | | **I** | Patrimônio financeiro / fora do perímetro pessoal |
| **E** | Serviços, saúde, educação, lazer e turismo | | **J** | Registros complementares e pendências |

## Como o CO2calc incorpora a taxonomia

| Da planilha | Para o repositório/app |
|---|---|
| Aba Taxonomia (586 nós) | `co2calc/seed/taxonomia.json` → tabela SQLite `taxonomia` (formulário Lançar: setor → atividade → método → fator) |
| Aba Métodos (33) | `co2calc/seed/metodos.json` → tabela `metodos` |
| Aba Regras R01–R16 | coluna `taxonomia.regras`; **R03 (rateio)** materializada no campo `pessoas` do lançamento; **R02 (recarga)** orientando a escolha GRID × TR_CAR |
| Aba COICOP | coluna `taxonomia.coicop` |
| Aba Geografias (250) | `co2calc/seed/paises.json` (63 países com fator de rede e média nacional, selecionados a partir do cadastro ISO da planilha) |
| Aba Fatores (modelo) | esquema da tabela `fatores` do app + `fatores.json` preenchido (cada linha cita sua fonte) |
| Abas Guia/Dimensões/Exemplos | princípios de UI e os campos de `obs`/contexto do lançamento |

**Verificação programática:** `tools/reextrair_seeds.py` relê a planilha versionada e compara
byte-a-byte os seeds `taxonomia.json` e `metodos.json`:

```bash
python tools/reextrair_seeds.py --check   # diz se os seeds ainda refletem a planilha
```

## Referências normativas citadas pela própria taxonomia (aba Fontes)

COICOP 2018 (ONU) · ISO 3166-1 · M49 (ONU) · IPCC Diretrizes 2006 e Refinamento 2019 · IPCC AR6 WGI cap. 7, tabela 7.15 (GWP-100) · GHG Protocol Scope 2 Guidance e Technical Guidance (Scope 3) · ISO 14067 · DESNZ *Government GHG Conversion Factors* (Reino Unido) · US EPA GHG Emission Factors Hub · Ember *Yearly Electricity Data* · MCTI/SIRENE fatores do SIN (Brasil) · ICAO ICEC · ADEME AGRIBALYSE · FAOSTAT Emissions Intensities · US EPA USEEIO (supply-chain) · EXIOBASE · GLEC Framework (Smart Freight Centre) · Google Cloud Carbon Footprint · PCAF Global GHG Standard Parte A.

Os fatores numéricos usados no aplicativo seguem esse mesmo mapa de fontes; a coluna `fonte` da
tabela `fatores` registra a procedência de cada linha (e o que é calibração própria aparece como
`ESTIMATIVA`/`Calibração CO2calc`, editável na interface).

## Citação sugerida

> MONTEIRO, R. **Minha Pegada — Taxonomia Mundial de Pegada de Carbono Individual**
> (planilha, rev. 2026-11-18, SHA-256 `bf70ee0e…b58f032`). Incorporada como dados de
> referência do aplicativo CO2calc, v1.0.0. Disponível em
> `docs/taxonomia/` deste repositório.

## Limites declarados pela planilha (Guia)
A–G compõem o perímetro principal do inventário pessoal; H registra serviços coletivos;
I fica fora do perímetro (patrimônio financeiro); J são pendências. O app reproduz essa
separação nos grupos `COLETIVO` e `FORA` do dashboard.
