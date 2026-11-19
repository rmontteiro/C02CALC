# CO2calc — Manual de instalación y uso
**Idioma: Español (Argentina)** · rev. 2026-11-18 · también en [Português](MANUAL_pt-BR.md) y [English](MANUAL_en-US.md)

---

## 1. Qué es CO2calc

CO2calc es una calculadora y monitor personal de huella de carbono, 100 % Python + SQLite:

* **Motor de cálculo propio**: estimación rápida en 4 pasos (vivienda, manejo, vuelos y dieta) más registro detallado por actividad, sobre la *Taxonomía Mundial de Huella de Carbono Individual* (586 nodos, sectores A–J);
* **Multiusuario**: cada persona guarda su historial mensual/anual, país y reparto del hogar;
* **Paneles personalizables** (usuarios, tipología, período) y comparativas entre usuarios;
* **Reportes PDF** y exportación CSV;
* **Tres idiomas**: Português, English y Español.

Fuentes de los factores: Defra/DESNZ (WTT incluido), redes eléctricas IEA/Ember y promedios nacionales OECD — ver `docs/METODOLOGIA.md` y `docs/TAXONOMIA.md`.

---

## 2. Requisitos

| Ítem | Versión |
|---|---|
| Python | 3.10 a 3.12 (en 3.13+, creá el venv con `python3.12 -m venv`) |
| Espacio en disco | ~350 MB (entorno virtual incluido) |
| Sistema | Ubuntu 20.04+/Debian, Windows 10+, macOS 12+ |
| Red | solo para instalar las dependencias |

---

## 3. Instalación

### 3.1 Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip

git clone https://github.com/rmontteiro/C02CALC.git
cd C02CALC

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python app.py
```

Si la ventana no abre por falta de bibliotecas de medios del cliente gráfico:

```bash
sudo apt install -y libmpv1 libmpv-dev
```

Diagnóstico de biblioteca faltante: `ldd ~/.flet/bin/flet-0.28.3/flet/flet | grep -i "not found"`.

### 3.2 Windows

1. Instalá Python 3.10–3.12 (tildá *Add Python to PATH*);
2. Descargá el repositorio (**Code → Download ZIP**) y descomprimilo;
3. Doble clic en `Iniciar_CO2calc.bat` — crea el entorno y abre la app.

### 3.3 macOS

```bash
git clone https://github.com/rmontteiro/C02CALC.git && cd C02CALC
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
./iniciar_CO2calc.sh
```

### 3.4 Ejecutable autocontenido (sin Python en la máquina destino)

```bash
pip install pyinstaller
./empacotar_CO2calc.sh        # Linux/macOS  →  dist/CO2calc
Empacotar_CO2calc.bat         # Windows      →  dist\CO2calc.exe
```

El binario incluye la taxonomía, los factores, los assets y la planilla maestra de la taxonomía.
En Linux, el empaquetado necesita `binutils` y `libpython3.x` (`sudo apt install binutils libpython3.11`).

### 3.5 Modo navegador (sin ventana nativa)

```bash
CO2CALC_WEB=1 python app.py        # abre en http://localhost:8560
CO2CALC_WEB=1 CO2CALC_PORT=9000 python app.py   # otro puerto
```

---

## 4. Primera apertura: elección del idioma

Al abrir, la app muestra **solo** la pantalla de idioma, con las banderas dibujadas por la propia app:

| Bandera | Texto de la tarjeta | Idioma aplicado |
|---|---|---|
| 🇧🇷 | Português | pt-BR |
| 🇺🇸 | English | en-US |
| 🇦🇷 | Español | es-AR |

* La pantalla aparece **en cada apertura**; tu elección anterior viene marcada con ✓ y borde verde;
* Un clic en la bandera entra a la app en ese idioma;
* Cambiar después, sin reiniciar: pestaña **Usuarios → 🌐 Interfaz → Aplicar idioma**;
* Automatización: `CO2CALC_LANG=pt|en|es` saltea la pantalla.

Menús, pantallas, gráficos, reportes PDF y exportaciones CSV siguen el idioma elegido.

---

## 5. Recorrido por las pantallas

### 5.1 Inicio
* **Medidor 0–100**: puntuación del usuario en el período (más alto es mejor);
* Bandas: Excelente ≥80 · Muy bueno ≥60 · Razonable ≥40 · Alto ≥20 · Crítico <20;
* Tarjetas por tipología (transporte, vivienda, alimentación, bienes, servicios, residuos);
* Racha de meses consecutivos con registros (🔥);
* Encabezado: país del perfil + personas en el hogar y, debajo, el idioma de la interfaz;
* Selectores de usuario, año y mes (o vista anual).

### 5.2 Registrar (detalle)
1. Elegí **Sector (nivel 1)** → **Actividad (nivel 4)** de la taxonomía → **Factor de emisión**;
2. Ingresá la **cantidad** en la unidad de la actividad y el **reparto** (dividir entre N personas);
3. La **previsión** muestra `cantidad × factor ÷ personas` en kgCO₂e antes de guardar;
4. Periodicidad **mensual** o **anual**, con año/mes y observación opcional;
5. Registros recientes abajo, con borrado por ícono 🗑.

### 5.3 Calculadora (estimación rápida)
* 4 bloques: vivienda (tipo/calefacción), manejo (volumen/combustible), vuelos (cortos/largos), dieta;
* Resultado **por persona**, comparado con el promedio nacional del país;
* **Guardar baseline** conserva el escenario para comparar años en Supervisión;
* **Generar registros anuales** convierte la estimación en registros del historial.

### 5.4 Supervisar (paneles)
* Filtros por **tipología** y por **usuario** (chips clicables encienden/apagan series);
* Widgets: tendencia mensual, composición (rosca), barras por tipología, comparativa entre usuarios, tabla consolidada kgCO₂e/mes y baselines;
* **Reportes PDF**: reporte del primer usuario seleccionado o comparativa (≥2 usuarios).

### 5.5 Usuarios y ajustes
* Alta/edición/borrado de usuarios (nombre, país, personas en el hogar, observación);
* **🌐 Interfaz**: cambio de idioma inmediato;
* **⚙️ Editar factores de emisión**: selector con nombres completos en portugués/inglés/español más la tarjeta **📖 Sobre este factor** (qué es, dónde lo usa la app, unidad por extenso, fuente y código interno); guardar recalcula todo;
* **🗄️ Base de datos local**: ruta del SQLite, referencia de la taxonomía y su SHA-256;
* **Exportar registros (CSV)**.

---

## 6. Datos, archivos y exportaciones

| Archivo | Contenido |
|---|---|
| `data/co2calc.db` | base SQLite (usuarios, registros, factores, baselines, ajustes) |
| `data/charts/*.png` | gráficos generados |
| `data/relatorios/*.pdf` | reportes PDF |
| `data/export_*_*.csv` | exportaciones CSV |

* Base en otro lugar: `CO2CALC_DB=/ruta/mi.db python app.py`;
* Los encabezados del CSV y los textos de los PDF siguen el idioma activo; fechas en formato regional;
* El score compara la huella anualizada *per cápita* con el promedio nacional del país (editable en la base).

---

## 7. Verificación y pruebas

```bash
python tests/test_smoke.py            # 8 pruebas: base, motor, pantallas, PDF
python tests/test_i18n.py             # 6 pruebas: catálogo, idiomas, PDF/CSV localizados
python tools/reextrair_seeds.py --check   # seeds fieles a la planilla maestra de la taxonomía
```

---

## 8. Solución de problemas

| Síntoma | Causa / arreglo |
|---|---|
| `externally-managed-environment` en pip | usá el venv (§3.1) |
| `libmpv.so.1: cannot open shared object` | `sudo apt install libmpv1 libmpv-dev` (§3.1) |
| La ventana no abre pero el proceso corre | usá el modo navegador (§3.5) |
| Python 3.13 sin wheels | `python3.12 -m venv .venv` |
| Puerto 8560 ocupado en modo web | `CO2CALC_PORT=9000` |
| Quiero rever la pantalla de idioma | vuelve en cada apertura; o Usuarios → Interfaz |

---

## 9. Referencias del repositorio

* `docs/METODOLOGIA.md` — fórmulas, factores y reglas (reparto, clases de vuelo, WTT);
* `docs/TAXONOMIA.md` + `docs/taxonomia/` — planilla maestra de la taxonomía y su SHA-256;
* `docs/ESQUEMA_BANCO.md` — esquema SQLite (el mismo que usará la futura app Android);
* `docs/GUIA_DE_MARCA.md` — paleta, logos y bandas de puntuación;
* `docs/ROADMAP_ANDROID.md` — camino hacia `flet build apk`.
