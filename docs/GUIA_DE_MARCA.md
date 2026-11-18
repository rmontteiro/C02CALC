# CO2calc — Guia de marca

Proposta de marca única (conceito → símbolo → paleta → tipografia → aplicações →
arquivo vetorial + rasteres).

## 1. Posicionamento
**CO2calc** = "a régua pessoal do carbono". Ferramenta de medição confiável (método auditável, banco local, fontes citadas) e ao mesmo tempo leve e diária — linguagem visual amigável de app de bem-estar/estilo de vida.

## 2. Símbolo — "anel de medição + molécula"
- **Conceito:** um gauge incompleto (arcos de tamanhos diferentes) = medição contínua e progresso; o gap superior-direito vira uma **conta de dados** (ponto de brilho) e sugere a órbita/quebra de uma molécula. Ao centro, **CO₂** com o "2" subscrito — literal e instantâneo.
- **Geometria:** grid de 512 pt, anel raio 150, traço 34, cantos dos arcos arredondados (round cap); 3 arcos + trilho escuro de 360°.
- **Gradiente:** verde-esmeralda escuro → primária (fundo), símbolo em menta/branco/âmbar (dados/meta/alerta — o âmbar traz o "sinal de alerta" climático sem virar vermelho).

Arquivos: `assets/logo_co2calc.svg` (mestre), `wordmark_co2calc.svg`, `icon_512/192.png`, `favicon.png`, `ic_launcher.png`, `co2calc.ico`, `brand_board.png`.

## 3. Paleta
| Token | Hex | Uso |
|---|---|---|
| primary | `#0FA968` | ações, seleção, header do app |
| primary-dark | `#067A4B` | texto sobre claro, toasts |
| data-1 (acento) | `#37D67A` | série transporte? não: série principal |
| data-2 | `#2E86DE` | segunda série |
| warn | `#F2B233` | âmbar — dieta/alerta leve |
| alert | `#E0563A` | crítico |
| bg-menta | `#EDF7F0` | fundo geral |
| ink | `#0B3D2E` | tipografia principal |

**Bandas do score (gauge 0–100):** ≥80 Excelente · ≥60 Muito bom · ≥40 Razoável · ≥20 Alto · <20 Crítico — definidas em `branding.BANDAS` e usadas em UI, gráficos e PDF.

## 4. Tipografia
Sem geometrista única: **Segoe UI** (Windows, padrão do app) / **Roboto** (Android, futuro). Números tabulares nos cards; pesos 300 e 700 no wordmark ("calc" leve em cor primária).

## 5. Regras de uso
- Área de respiro ≥ ½ do "CO" do símbolo; nunca esticar o anel.
- Ícone do launcher = SVG mestre exportado 512 (adaptive icon: o anel vive dentro do safe zone de 66 dp do Android — previsto no roadmap).
- Em PDFs e dashboards, o gauge usa sempre as cores das bandas (semântica de dados > cor decorativa).
- Não posicionar o símbolo sobre foto sem véu; usar o lockup claro em card branco.

## 6. Direção de UI
Fundo menta · cards brancos 18 px de raio, sombra difusa · chips pill com emoji de tipologia · nav inferior de 5 destinos com rótulo visível · stepper +/− numérico · gauge circular no topo do painel.
