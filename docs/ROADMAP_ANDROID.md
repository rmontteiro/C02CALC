# Roadmap CO2calc → Android

O app desktop é **Flet** (Python + Flutter). A mesma base de código gera o APK:

## Caminho imediato (mesmo código)
```bash
pip install flet flet-cli
flet doctor                    # Flutter SDK + JDK 17 + Android SDK
flet create . --template        # (ou) adicionar android/ via: flet build? — veja abaixo
flet build apk -t --project-id com.co2calc.app
```
No Flet 0.28.x: `flet build apk` inicializa o projeto Flutter wrapper e empacota `app.py` com Python embarcado (Oppy/Runtime). O alvo é um app 100 % local — mantemos essa filosofia:

| Desktop hoje | Android amanhã |
|---|---|
| janela Flet | `flet build apk` / `bundle` |
| `data/co2calc.db` ao lado do exe | SQLite interno do app (mesmo esquema, `ESQUEMA_BANCO.md`) — Room não precisa migrar tabelas, só o driver |
| `flet pack` exe | não usar — APK nativo |
| relatórios em `data/relatorios/` | salvar via `share sheet` (`page.save_file` → arquivo PDF do mesmo `reports.py`) |
| matplotlib PNG | manter p/ MVP; substituir por `ft.LineChart/BarChart/PieChart` nativos (mais leve no ARM) ou `fl_chart` via bridge |

## Requisitos já previstos no design
1. **Offline-first, sem conta**: nenhuma tabela de auth; multiusuário local.
2. **Esquema portável**: PKs naturais, timestamps ISO — drift/Room importam o `.db` atual sem conversão.
3. **Modularização**: `engine.py` é puro SQLite (sem I/O de UI) → vira pacote `core/` no monorepo Android/iOS.
4. **Marca**: ícone 512 + SVG já em `assets/`; para adaptive icon gerar `mipmap-*` de `ic_launcher.png`
   (fundo `#064E3B→#0FA968` é o mesmo do launcher desktop).

## Backlog sugerido pós-MVP Android
- Notificação diária de lançamento (streak de meses com registro);
- Scaneamento de QR de conta de luz / OCR de fatura → `registros` com `origem='ocr'`;
- `distância great-circle` por pares de aeroporto (tabela `aeroportos(iso3, lat, lon)` + haversine) para cálculo de voo por rota;
- exportação `CSV/PDF` compartilhável + backup `.db` no Drive;
- sync opcional (mesmo esquema com carimbo `atualizado_em` + deleted-flag) quando houver backend.

## Teste rápido do build
O `tests/test_smoke.py` roda fora do Flutter (só Python puro nas partes críticas: banco, engine, PDF).
Na CI Android, adicionar: `flet build apk --debug` + `adb install` + `python tests/...`.
