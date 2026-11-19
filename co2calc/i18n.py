# -*- coding: utf-8 -*-
"""Internacionalização do CO2calc — português (pt-BR, idioma-fonte), inglês (en-US)
e espanhol (es-AR).

Padrão gettext simplificado: as strings em português usadas na interface são a
chave; `T()` devolve a tradução do idioma ativo (ou a própria chave, se não
houver). `FM()` aceita marcadores {nome} para frases montadas.
Idioma ativo é lembrado na tabela `ajustes` (chave 'idioma') e pode ser
sobrescrito pela variável de ambiente CO2CALC_LANG.
"""
import threading

CODES = ["pt", "en", "es"]
LANGS = [
    {"code": "pt", "rotulo": "Português", "pais": "Brasil", "flag": "assets/flags/br.png"},
    {"code": "en", "rotulo": "English", "pais": "United States", "flag": "assets/flags/us.png"},
    {"code": "es", "rotulo": "Español", "pais": "Argentina", "flag": "assets/flags/ar.png"},
]

_lock = threading.RLock()
_st = {"lang": "pt"}


def set_lang(code):
    _lock.acquire() if False else None
    _st["lang"] = code if code in CODES else "pt"


def get_lang():
    return _st["lang"]


def T(s):
    lang = _st["lang"]
    if lang == "pt":
        return s
    row = _CAT.get(s)
    if not row:
        return s
    return row[0] if lang == "en" else row[1]


def FM(txt, **kw):
    return T(txt).format(**kw)


MESES_AB = {
    "pt": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "es": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
}


def meses_ab():
    return MESES_AB[_st["lang"]]


def nome_idioma(code=None):
    code = code or _st["lang"]
    return next(l["rotulo"] for l in LANGS if l["code"] == code)


# PT-chave -> (English, Español-AR)  — voseo e vocabulário rioplatenses no ES
_CAT = {
    # ---- navegação / comum
    "Início": ("Home", "Inicio"),
    "Lançar": ("Log data", "Registrar"),
    "Calculadora": ("Calculator", "Calculadora"),
    "Monitorar": ("Monitor", "Supervisar"),
    "Usuários": ("Users", "Usuarios"),
    "CO2calc — pegada de carbono pessoal": ("CO2calc — personal carbon footprint", "CO2calc — huella de carbono personal"),
    "mês": ("month", "mes"),
    "ano": ("year", "año"),
    "Ano": ("Year", "Año"),
    "Mês": ("Month", "Mes"),
    "Usuário": ("User", "Usuario"),
    "minha pegada, meu monitor": ("my footprint, my monitor", "mi huella, mi monitor"),
    "sem dados": ("no data", "sin datos"),
    "Excluir": ("Delete", "Eliminar"),
    "Observação": ("Note", "Observación"),
    "Nome": ("Name", "Nombre"),
    "País": ("Country", "País"),
    # ---- tela Início
    "Nenhum usuário cadastrado": ("No users registered yet", "Aún no hay usuarios registrados"),
    "Vá até a aba Usuários para criar seu primeiro perfil.": ("Go to the Users tab to create your first profile.", "Ve a la pestaña Usuarios para crear tu primer perfil."),
    "Ir para Usuários": ("Go to Users", "Ir a Usuarios"),
    "Cadastrar usuário": ("Register a user", "Registrar usuario"),
    "🇧🇷 {pais} · {p}p": ("🇧🇷 {pais} · {p} people", "🇧🇷 {pais} · {p} personas"),
    "vs média {pais} {v} t": ("vs {pais} average {v} t", "vs promedio {pais} {v} t"),
    "tCO₂e/ano": ("tCO₂e/year", "tCO₂e/año"),
    "{v} kgCO₂e em {periodo}": ("{v} kgCO₂e in {periodo}", "{v} kgCO₂e en {periodo}"),
    "🔥 {n} meses seguidos": ("🔥 {n} months in a row", "🔥 {n} meses seguidos"),
    "Transportes": ("Transportation", "Transporte"),
    "Moradia & Energia": ("Home & Energy", "Vivienda y Energía"),
    "Alimentação": ("Food", "Alimentación"),
    "Bens & Consumo": ("Goods & Consumption", "Bienes y Consumo"),
    "Serviços & Lazer": ("Services & Leisure", "Servicios y Ocio"),
    "Resíduos": ("Waste", "Residuos"),
    "Animais & Autoconsumo": ("Animals & Self-consumption", "Animales y Autoconsumo"),
    "Serviços coletivos": ("Collective services", "Servicios colectivos"),
    "Fora do perímetro": ("Out of scope", "Fuera del perímetro"),
    "Dashboard completo": ("Full dashboard", "Panel completo"),
    "Monitorar & comparar usuários": ("Monitor & compare users", "Supervisar y comparar usuarios"),
    "Dashboard": ("Dashboard", "Panel"),
    "Últimos lançamentos": ("Latest entries", "Últimos registros"),
    "nenhum lançamento ainda": ("no entries yet", "aún no hay registros"),
    "+ Novo lançamento": ("+ New entry", "+ Nuevo registro"),
    "Calculadora rápida": ("Quick calculator", "Calculadora rápida"),
    # ---- Lançar
    "Cadastre um usuário primeiro.": ("Register a user first.", "Primero registrá un usuario."),
    "Setor (nível 1)": ("Sector (level 1)", "Sector (nivel 1)"),
    "Atividade (nível 4)": ("Activity (level 4)", "Actividad (nivel 4)"),
    "Fator de emissão": ("Emission factor", "Factor de emisión"),
    "Quantidade da atividade": ("Activity amount", "Cantidad de la actividad"),
    "Quantidade ({un})": ("Amount ({un})", "Cantidad ({un})"),
    "Rateio: dividir entre N": ("Sharing: divide among N", "Reparto: dividir entre N"),
    "Periodicidade": ("Frequency", "Periodicidad"),
    "Mensal": ("Monthly", "Mensual"),
    "Anual": ("Annual", "Anual"),
    "Emissão: —": ("Emission: —", "Emisión: —"),
    "Prévia: —": ("Preview: —", "Previa: —"),
    "Prévia: dados incompletos": ("Preview: incomplete data", "Previa: datos incompletos"),
    "Prévia: {v} kgCO₂e": ("Preview: {v} kgCO₂e", "Previa: {v} kgCO₂e"),
    "Prévia: fator não encontrado no banco": ("Preview: factor not found in database", "Previa: factor no encontrado en la base"),
    "Prévia: atividade sem fator numérico": ("Preview: activity without numeric factor", "Previa: actividad sin factor numérico"),
    "⚠️ Atividade sem vínculo definido": ("⚠️ Activity without defined link", "⚠️ Actividad sin vínculo definido"),
    "⚠️ Método: {m} | Status: {s}": ("⚠️ Method: {m} | Status: {s}", "⚠️ Método: {m} | Estado: {s}"),
    "📋 Fator pendente de cadastro - use valor manual": ("📋 Pending factor - use manual value", "📋 Factor pendiente de registro - use valor manual"),
    "Pendente": ("Pending", "Pendiente"),
    "Escolha um fator de emissão válido.": ("Choose a valid emission factor.", "Elegí un factor de emisión válido."),
    "Lançamento registrado como pendência (sem fator numérico)": ("Entry logged as pending (no numeric factor)", "Registro guardado como pendiente (sin factor numérico)"),
    "Informe uma quantidade válida.": ("Enter a valid amount.", "Ingresá una cantidad válida."),
    "Escolha um fator de emissão.": ("Choose an emission factor.", "Elegí un factor de emisión."),
    "Lançado: {v} kgCO₂e": ("Logged: {v} kgCO₂e", "Registrado: {v} kgCO₂e"),
    "Lançamento removido.": ("Entry deleted.", "Registro eliminado."),
    "Lançamentos recentes": ("Recent entries", "Registros recientes"),
    "nenhum lançamento deste usuário ainda": ("no entries for this user yet", "aún no hay registros de este usuario"),
    "Novo lançamento de dados": ("New data entry", "Nuevo registro de datos"),
    ("Escolha setor → atividade (Taxonomia Mundial, 586 nós) → fator. "
     "Mensal ou anual, com rateio por pessoas."): (
        "Choose sector → activity (World Taxonomy, 586 nodes) → factor. Monthly or annual, with household sharing.",
        "Elegí sector → actividad (Taxonomía Mundial, 586 nodos) → factor. Mensual o anual, con reparto por personas."),
    "Salvar lançamento": ("Save entry", "Guardar registro"),
    "anual": ("annual", "anual"),
    "mensal": ("monthly", "mensual"),
    # ---- Calculadora
    "🏢 Apartamento": ("🏢 Apartment", "🏢 Departamento"),
    "🏠 Casa pequena (1–2 quartos)": ("🏠 Small house (1–2 bedrooms)", "🏠 Casa chica (1–2 dormitorios)"),
    "🏡 Casa média (3 quartos)": ("🏡 Medium house (3 bedrooms)", "🏡 Casa mediana (3 dormitorios)"),
    "🏘️ Casa grande (4+ quartos)": ("🏘️ Large house (4+ bedrooms)", "🏘️ Casa grande (4+ dormitorios)"),
    "🔥 Gás encanado": ("🔥 Piped gas", "🔥 Gas de caño"),
    "⚡ Elétrico": ("⚡ Electric", "⚡ Eléctrico"),
    "♨️ Bomba de calor": ("♨️ Heat pump", "♨️ Bomba de calor"),
    "🛢️ Óleo/botijão": ("🛢️ Oil/cylinder", "🛢️ Oil/cilindro"),
    "🚶 Quase não dirijo": ("🚶 I barely drive", "🚶 Casi no manejo"),
    "🚗 Pouco (< ~4.000 km/ano)": ("🚗 Little (< ~4,000 km/yr)", "🚗 Poco (< ~4.000 km/año)"),
    "🚙 Média (≈ 8.000 km)": ("🚙 Medium (≈ 8,000 km)", "🚙 Medio (≈ 8.000 km)"),
    "🏎️ Muito (≈ 16.000 km)": ("🏎️ High (≈ 16,000 km)", "🏎️ Mucho (≈ 16.000 km)"),
    "⛽ Gasolina": ("⛽ Gasoline", "⛽ Nafta"),
    "🛢️ Diesel": ("🛢️ Diesel", "🛢️ Diesel"),
    "🔋 Híbrido": ("🔋 Hybrid", "🔋 Híbrido"),
    "🔌 Elétrico": ("🔌 Electric", "🔌 Eléctrico"),
    "🥩 Carne quase todo dia": ("🥩 Meat almost every day", "🥩 Carne casi todos los días"),
    "🍗 Carne algumas vezes/semana": ("🍗 Meat a few times/week", "🍗 Carne algunas veces por semana"),
    "🥚 Maior parte vegetariana": ("🥚 Mostly vegetarian", "🥚 Mayormente vegetariana"),
    "🌱 Vegana/plant-based": ("🌱 Vegan/plant-based", "🌱 Vegana/plant-based"),
    "1 · Sua moradia": ("1 · Your home", "1 · Tu vivienda"),
    "Tamanho e aquecimento definem a energia do imóvel.": ("Size and heating set the home's energy use.", "El tamaño y la calefacción definen la energía del hogar."),
    "2 · Como você dirige": ("2 · How you drive", "2 · Cómo manejás"),
    "Volume anual aproximado e tipo de veículo.": ("Approximate annual mileage and vehicle type.", "Kilometraje anual aproximado y tipo de vehículo."),
    "3 · Voos no último ano": ("3 · Flights in the last year", "3 · Vuelos del último año"),
    "Ida e volta contam como 1 viagem (curto ≤5h, longo >5h).": ("Round trips count as one trip (short ≤5h, long >5h).", "Ida y vuelta cuentan como 1 viaje (corto ≤5h, largo >5h)."),
    "4 · Sua dieta": ("4 · Your diet", "4 · Tu dieta"),
    "Uma ideia geral já basta.": ("A general idea is enough.", "Una idea general alcanza."),
    "Pessoas no domicílio": ("Household size (people)", "Personas en el hogar"),
    "Voos curtos de ida-e-volta": ("Short round-trip flights", "Vuelos cortos de ida y vuelta"),
    "Voos longos de ida-e-volta": ("Long round-trip flights", "Vuelos largos de ida y vuelta"),
    "País (define redes e médias)": ("Country (sets grids and averages)", "País (define redes y promedios)"),
    "Calcular para": ("Calculate for", "Calcular para"),
    "média {pais}: {v} t": ("{pais} average: {v} t", "promedio {pais}: {v} t"),
    "tCO₂e/pessoa": ("tCO₂e/person", "tCO₂e/persona"),
    "🏠 Moradia": ("🏠 Home", "🏠 Vivienda"),
    "🚗 Carro": ("🚗 Car", "🚗 Auto"),
    "✈️ Voos": ("✈️ Flights", "✈️ Vuelos"),
    "🍽️ Alimentação": ("🍽️ Food", "🍽️ Alimentación"),
    "🛍️ Bens & serviços": ("🛍️ Goods & services", "🛍️ Bienes y servicios"),
    "abaixo": ("below", "por debajo"),
    "acima": ("above", "por encima"),
    "{dir} da média {pais} em {pct}% · domicílio de {n}p ≈ {v} tCO₂e/ano": (
        "{dir} the {pais} average by {pct}% · {n}-person household ≈ {v} tCO₂e/year",
        "{dir} del promedio de {pais} en {pct}% · hogar de {n} ≈ {v} tCO₂e/año"),
    "Sua estimativa: {v} tCO₂e por pessoa/ano": ("Your estimate: {v} tCO₂e per person/year", "Tu estimación: {v} tCO₂e por persona/año"),
    "Salvar baseline": ("Save baseline", "Guardar baseline"),
    "Baseline salva — compare anos no Monitoramento.": ("Baseline saved — compare years in Monitor.", "Baseline guardada — compará años en Supervisión."),
    "Gerar lançamentos anuais no histórico": ("Generate annual entries in history", "Generar registros anuales en el historial"),
    "Ver no dashboard": ("View in dashboard", "Ver en el panel"),
    "Estimativa em 4 blocos — moradia, direção, voos e dieta; bens & serviços calibrados pela média nacional (OECD/Defra) e fator de rede elétrica do país (IEA/Ember).": (
        "4-block estimate — home, driving, flights and diet; goods & services calibrated by the national average (OECD/Defra) and the country's grid factor (IEA/Ember).",
        "Estimación en 4 bloques — vivienda, manejo, vuelos y dieta; bienes y servicios calibrados por el promedio nacional (OECD/Defra) y el factor de red eléctrica del país (IEA/Ember)."),
    "{n} registros anuais criados (origem: calculadora).": ("{n} annual records created (source: calculator).", "{n} registros anuales creados (origen: calculadora)."),
    # ---- Monitorar
    "Cadastre usuários primeiro.": ("Register users first.", "Primero registrá usuarios."),
    "Monitoramento": ("Monitor", "Supervisión"),
    "dashboards customizáveis · clique nos filtros para ligar/desligar séries": (
        "customizable dashboards · click the filters to toggle series",
        "paneles personalizables · hacé clic en los filtros para encender/apagar series"),
    "Tipologias:": ("Typologies:", "Tipologías:"),
    "Usuários:": ("Users:", "Usuarios:"),
    "Tendência": ("Trend", "Tendencia"),
    "Composição": ("Breakdown", "Composición"),
    "Tipologia": ("By typology", "Tipología"),
    "Comparativo": ("Comparison", "Comparativa"),
    "Tabela": ("Table", "Tabla"),
    "Baselines": ("Baselines", "Baselines"),
    "📈 Tendência mensal": ("📈 Monthly trend", "📈 Tendencia mensual"),
    "linha tracejada = mesmo período no ano anterior": ("dashed line = same period last year", "línea punteada = mismo período del año anterior"),
    "Tendência mensal — {nome} · {ano}": ("Monthly trend — {nome} · {ano}", "Tendencia mensual — {nome} · {ano}"),
    "🍩 Composição por tipologia": ("🍩 Breakdown by typology", "🍩 Composición por tipología"),
    "📊 kgCO₂e por tipologia": ("📊 kgCO₂e by typology", "📊 kgCO₂e por tipología"),
    "⚖️ Comparativo entre usuários": ("⚖️ Compare users", "⚖️ Comparativa entre usuarios"),
    "Exportar comparativo PDF": ("Export comparison PDF", "Exportar PDF comparativo"),
    "selecione ≥ 2 usuários para exportar o comparativo": (
        "select ≥ 2 users to export the comparison", "seleccioná ≥ 2 usuarios para exportar la comparativa"),
    "| Usuário |": ("| User |", "| Usuario |"),
    "| Total |": ("| Total |", "| Total |"),
    "🗓️ Tabela consolidada (kgCO₂e/mês)": ("🗓️ Consolidated table (kgCO₂e/month)", "🗓️ Tabla consolidada (kgCO₂e/mes)"),
    "📄 Relatórios PDF": ("📄 PDF reports", "📄 Reportes PDF"),
    "Relatório do 1º usuário · {ano}": ("First user's report · {ano}", "Reporte del 1er usuario · {ano}"),
    "Comparativo · {ano}": ("Comparison · {ano}", "Comparativa · {ano}"),
    "PDF gerado: {p}": ("PDF generated: {p}", "PDF generado: {p}"),
    "🧭 Baselines da calculadora rápida (comparar anos)": (
        "🧭 Quick-calculator baselines (compare years)", "🧭 Baselines de la calculadora rápida (comparar años)"),
    "{nome} — baseline {data}": ("{nome} — baseline {data}", "{nome} — baseline {data}"),
    "total do domicílio: {v} kgCO₂e · {respostas}": ("household total: {v} kgCO₂e · {respostas}", "total del hogar: {v} kgCO₂e · {respostas}"),
    "nenhuma baseline salva": ("no baseline saved", "ninguna baseline guardada"),
    # ---- Usuários & Config
    "➕ Novo usuário": ("➕ New user", "➕ Nuevo usuario"),
    "O app aceita múltiplos usuários/perfis; cada um guarda seu histórico mensal e anual.": (
        "The app supports multiple users/profiles; each keeps its own monthly and annual history.",
        "La app admite múltiples usuarios/perfiles; cada uno guarda su historial mensual y anual."),
    "Cadastrar": ("Register", "Registrar"),
    "Usuário “{nome}” criado.": ("User “{nome}” created.", "Usuario “{nome}” creado."),
    "Informe um nome.": ("Enter a name.", "Ingresá un nombre."),
    "Já existe um usuário com esse nome.": ("A user with that name already exists.", "Ya existe un usuario con ese nombre."),
    "Erro: {e}": ("Error: {e}", "Error: {e}"),
    "“{nome}” removido com seus dados.": ("“{nome}” and all their data were removed.", "“{nome}” y sus datos fueron eliminados."),
    "Selecionar": ("Select", "Seleccionar"),
    "Cancelar": ("Cancel", "Cancelar"),
    "Excluir usuário?": ("Delete user?", "¿Eliminar usuario?"),
    "Esta ação remove “{nome}” e todos os seus lançamentos. Não pode ser desfeita.": (
        "This permanently removes “{nome}” and all their entries. This cannot be undone.",
        "Esta acción elimina a “{nome}” y todos sus registros. No se puede deshacer."),
    "Excluir usuário e dados": ("Delete user and data", "Eliminar usuario y datos"),
    "⚙️ Editar fatores de emissão": ("⚙️ Edit emission factors", "⚙️ Editar factores de emisión"),
    ("todos os fatores do cálculo, incluindo a rede elétrica e a média nacional do seu país — "
     "ao gravar, tudo é recalculado no app"): (
        "all factors used in the calculation, including your country's grid and national average — saving recalculates everything",
        "todos los factores del cálculo, incluida la red eléctrica y el promedio nacional de tu país — al guardar se recalcula todo"),
    "Fator de emissão (nome completo)": ("Emission factor (full name)", "Factor de emisión (nombre completo)"),
    "Novo valor": ("New value", "Nuevo valor"),
    "Gravar fator": ("Save factor", "Guardar factor"),
    "Fator atualizado: {r} → {v} ✓": ("Factor updated: {r} → {v} ✓", "Factor actualizado: {r} → {v} ✓"),
    "valor inválido": ("invalid value", "valor inválido"),
    "📖 Sobre este fator": ("📖 About this factor", "📖 Sobre este factor"),
    "o que significa, onde o app usa e de onde vem o valor selecionado": (
        "what it means, where the app uses it and where the selected value comes from",
        "qué significa, dónde lo usa la app y de dónde viene el valor elegido"),
    "Unidade do valor": ("Value unit", "Unidad del valor"),
    "Fonte registrada": ("Registered source", "Fuente registrada"),
    "Código interno": ("Internal code", "Código interno"),
    "🗄️ Banco de dados local": ("🗄️ Local database", "🗄️ Base de datos local"),
    "Arquivo SQLite": ("SQLite file", "Archivo SQLite"),
    "Taxonomia (referência-mestre)": ("Taxonomy (master reference)", "Taxonomía (referencia maestra)"),
    "Versão da planilha (SHA-256)": ("Spreadsheet version (SHA-256)", "Versión de la planilla (SHA-256)"),
    "Portabilidade": ("Portability", "Portabilidad"),
    "mesmo esquema SQLite será usado no app Android (roadmap em docs/)": (
        "the same SQLite schema will power the Android app (roadmap in docs/)",
        "el mismo esquema SQLite se usará en la app Android (roadmap en docs/)"),
    "Exportar lançamentos (CSV)": ("Export entries (CSV)", "Exportar registros (CSV)"),
    "CSV exportado: {p}": ("CSV exported: {p}", "CSV exportado: {p}"),
    "🌐 Interface": ("🌐 Interface", "🌐 Interfaz"),
    "Idioma do app — menus, telas, gráficos e relatórios": (
        "App language — menus, screens, charts and reports", "Idioma de la app — menús, pantallas, gráficos y reportes"),
    "🌍 Idioma — {l}": ("🌍 Language — {l}", "🌍 Idioma — {l}"),
    "Idioma alterado para {l}": ("Language switched to {l}", "Idioma cambiado a {l}"),
    # ---- gráficos (charts.py)
    "Tendência mensal (kgCO₂e)": ("Monthly trend (kgCO₂e)", "Tendencia mensual (kgCO₂e)"),
    "período anterior": ("previous period", "período anterior"),
    "média {v}": ("average {v}", "promedio {v}"),
    "Emissões por tipologia (kgCO₂e)": ("Emissions by typology (kgCO₂e)", "Emisiones por tipología (kgCO₂e)"),
    "Comparativo entre usuários (kgCO₂e no período)": (
        "User comparison (kgCO₂e in period)", "Comparativa entre usuarios (kgCO₂e en el período)"),
    "/ 100 · ": ("/ 100 · ", "/ 100 · "),
    # ---- relatórios PDF
    "Relatório de emissões — {nome}": ("Emissions report — {nome}", "Reporte de emisiones — {nome}"),
    "Período: {p} · Pessoas: {n} · Gerado em {ts}": ("Period: {p} · People: {n} · Generated at {ts}", "Período: {p} · Personas: {n} · Generado el {ts}"),
    "Resumo": ("Summary", "Resumen"),
    "Total no período (kgCO₂e)": ("Total in period (kgCO₂e)", "Total del período (kgCO₂e)"),
    "Projeção anual (kgCO₂e/ano)": ("Annual projection (kgCO₂e/yr)", "Proyección anual (kgCO₂e/año)"),
    "Per capita (tCO₂e/ano)": ("Per capita (tCO₂e/yr)", "Per cápita (tCO₂e/año)"),
    "Média nacional (tCO₂e/per capita)": ("National average (tCO₂e per capita)", "Promedio nacional (tCO₂e per cápita)"),
    "Pontuação CO2calc (0–100)": ("CO2calc score (0–100)", "Puntuación CO2calc (0–100)"),
    "Composição por tipologia": ("Breakdown by typology", "Composición por tipología"),
    "kgCO₂e por tipologia": ("kgCO₂e by typology", "kgCO₂e por tipología"),
    "Lançamentos do período": ("Entries in the period", "Registros del período"),
    "Atividade": ("Activity", "Actividad"),
    "Grupo": ("Group", "Grupo"),
    "Unid.": ("Unit", "Unid."),
    "kgCO₂e": ("kgCO₂e", "kgCO₂e"),
    "Rec.": ("Cat.", "Rec."),
    ("Metodologia: fatores Defra/DESNZ (WTT incluso), redes elétricas IEA/Ember e médias nacionais "
     "OECD 2022, aplicados sobre a Taxonomia Mundial de Pegada de Carbono Individual (setores A–J) "
     "conforme a planilha de taxonomia anexa. Valores são estimativas auditáveis por lançamento; "
     "fórmulas: E = atividade × fator ÷ rateio de pessoas."): (
        "Methodology: Defra/DESNZ factors (incl. WTT), IEA/Ember electricity grids and OECD 2022 national averages, "
        "applied over the World Taxonomy of Personal Carbon Footprint (sectors A–J) as per the attached taxonomy sheet. "
        "Values are auditable per-entry estimates; formula: E = activity × factor ÷ people sharing.",
        "Metodología: factores Defra/DESNZ (incl. WTT), redes eléctricas IEA/Ember y promedios nacionales OECD 2022, "
        "aplicados sobre la Taxonomía Mundial de Huella de Carbono Individual (sectores A–J) según la planilla adjunta. "
        "Los valores son estimaciones auditables por registro; fórmula: E = actividad × factor ÷ reparto de personas."),
    "Comparativo de usuários — {ano}": ("User comparison — {ano}", "Comparativa entre usuarios — {ano}"),
    "Emissões mensais consolidadas por tipologia · {nomes}": (
        "Consolidated monthly emissions by typology · {nomes}", "Emisiones mensales consolidadas por tipología · {nomes}"),
    "Pessoas": ("People", "Personas"),
    "Total ano (kgCO₂e)": ("Year total (kgCO₂e)", "Total del año (kgCO₂e)"),
    "tCO₂e/per capita": ("tCO₂e per capita", "tCO₂e per cápita"),
    "Classificação": ("Rating", "Clasificación"),
    ("Score = anualização per capita vs média nacional do país (OECD/Defra aprox., editável no banco)."): (
        "Score = per-capita annualization vs the country's national average (OECD/Defra approx., editable in the database).",
        "Score = anualización per cápita vs promedio nacional del país (OECD/Defra aprox., editable en la base)."),
    # ---- faixas de pontuação
    "Excelente": ("Excellent", "Excelente"),
    "Muito bom": ("Very good", "Muy bueno"),
    "Razoável": ("Fair", "Razonable"),
    "Alto": ("High", "Alto"),
    "Crítico": ("Critical", "Crítico"),
    # ---- exportações CSV
    "usuario": ("user", "usuario"), "codigo": ("code", "código"), "grupo": ("group", "grupo"),
    "atividade": ("activity", "actividad"), "valor": ("value", "valor"), "unidade": ("unit", "unidad"),
    "fator": ("factor", "factor"), "pessoas": ("people", "personas"), "tipo": ("type", "tipo"),
    "origem": ("source", "origen"),
    # ---- registros gerados pela calculadora (engine)
    "Estimativa quick: moradia": ("Quick estimate: home", "Estimación rápida: vivienda"),
    "Estimativa quick: carro": ("Quick estimate: car", "Estimación rápida: auto"),
    "Estimativa quick: voos": ("Quick estimate: flights", "Estimación rápida: vuelos"),
    "Estimativa quick: alimentação": ("Quick estimate: food", "Estimación rápida: alimentación"),
    "gerado da calculadora rápida": ("generated by the quick calculator", "generado por la calculadora rápida"),
    # ---- rótulos de fatores (rotulos_fatores)
    "Estimativa rápida (4 etapas)": ("Quick estimate (4 steps)", "Estimación rápida (4 pasos)"),
    "Moradia (aquecimento, água e resíduos)": ("Home (heating, water and waste)", "Vivienda (calefacción, agua y residuos)"),
    "Transporte e deslocamentos": ("Transport and commuting", "Transporte y desplazamientos"),
    "Bens e compras": ("Goods and purchases", "Bienes y compras"),
    "Serviços e uso digital": ("Services and digital use", "Servicios y uso digital"),
    "Animais de estimação e outros": ("Pets and others", "Mascotas y otros"),
    "Rede elétrica do país": ("Country power grid", "Red eléctrica del país"),
    "Média nacional por habitante": ("National average per inhabitant", "Promedio nacional por habitante"),
    "Rede elétrica — {pais}: emissões por quilowatt-hora de eletricidade consumida": (
        "Power grid — {pais}: emissions per kilowatt-hour of electricity consumed",
        "Red eléctrica — {pais}: emisiones por kilovatio-hora de electricidad consumida"),
    "Média nacional por habitante — {pais}: pegada anual de cada residente (referência de comparação)": (
        "National average per inhabitant — {pais}: each resident's yearly footprint (comparison reference)",
        "Promedio nacional por habitante — {pais}: huella anual de cada residente (referencia de comparación)"),
    ("É a emissão média, em quilogramas de CO₂ equivalente, para entregar um quilowatt-hora de "
     "eletricidade na rede de {pais} — inclui a geração nas usinas e as perdas de transmissão e distribuição."): (
        "Average emissions, in kilograms of CO₂ equivalent, needed to deliver one kilowatt-hour of electricity "
        "on {pais}'s grid — includes power generation plus transmission and distribution losses."),
    ("É a pegada de carbono anual média de cada residente de {pais}, em toneladas de CO₂ equivalente, "
     "calculada a partir de estatísticas nacionais de energia e consumo."): (
        "Average yearly carbon footprint of each resident of {pais}, in tonnes of CO₂ equivalent, "
        "computed from national energy and consumption statistics."),
    # placeholders ES para os dois blocos acima (estrutura alternativa: dict próprio no RF)
    "É a emissão média, em quilogramas de CO₂ equivalente, para entregar um quilowatt-hora de eletricidade na rede de {pais} — inclui a geração nas usinas e as perdas de transmissão e distribuição.": (
        "Average emissions, in kilograms of CO₂ equivalent, needed to deliver one kilowatt-hour of electricity on {pais}'s grid — includes generation and transmission/distribution losses.",
        "Es la emisión media, en kilogramos de CO₂ equivalente, necesaria para entregar un kilovatio-hora de electricidad en la red de {pais} — incluye la generación y las pérdidas de transmisión y distribución."),
    "É a pegada de carbono anual média de cada residente de {pais}, em toneladas de CO₂ equivalente, calculada a partir de estatísticas nacionais de energia e consumo.": (
        "Average yearly carbon footprint of each resident of {pais}, in tonnes of CO₂ equivalent, computed from national energy and consumption statistics.",
        "Es la huella de carbono anual media de cada residente de {pais}, en toneladas de CO₂ equivalente, calculada a partir de estadísticas nacionales de energía y consumo."),
    # ---- onde cada fator é usado (explicação)
    "É usado na estimativa rápida em 4 etapas (moradia, direção, voos e dieta), quando não há lançamento detalhado.": (
        "Used by the 4-step quick estimate (home, driving, flights and diet) when there are no detailed entries.",
        "Se usa en la estimación rápida de 4 pasos (vivienda, manejo, vuelos y dieta) cuando no hay registros detallados."),
    "É aplicado na apuração detalhada de transporte: a quantidade lançada é multiplicada por este fator para obter a emissão do lançamento.": (
        "Applied in detailed transport entries: the logged amount is multiplied by this factor to get the entry's emissions.",
        "Se aplica en los registros detallados de transporte: la cantidad ingresada se multiplica por este factor para obtener las emisiones."),
    "É aplicado na apuração detalhada de moradia (aquecimento, água e resíduos): a quantidade lançada é multiplicada por este fator.": (
        "Applied in detailed home entries (heating, water and waste): the logged amount is multiplied by this factor.",
        "Se aplica en los registros detallados de vivienda (calefacción, agua y residuos): la cantidad se multiplica por este factor."),
    "É aplicado na apuração detalhada de alimentação: multiplica o número de refeições lançadas.": (
        "Applied in detailed food entries: multiplies the number of logged meals.",
        "Se aplica en los registros detallados de alimentación: multiplica la cantidad de comidas."),
    "É aplicado na apuração detalhada de bens: multiplica o número de unidades compradas.": (
        "Applied in detailed goods entries: multiplies the number of purchased units.",
        "Se aplica en los registros detallados de bienes: multiplica la cantidad de unidades compradas."),
    "É aplicado na apuração detalhada de serviços e de uso digital.": (
        "Applied in detailed service and digital-use entries.", "Se aplica en los registros detallados de servicios y uso digital."),
    "É aplicado na apuração detalhada de animais de estimação e outros itens.": (
        "Applied in detailed pet and other-items entries.", "Se aplica en los registros detallados de mascotas y otros ítems."),
    "É usado sempre que um lançamento consome eletricidade da rede (moradia, bomba de calor, carro elétrico, uso digital) e também na estimativa rápida.": (
        "Used whenever an entry consumes grid electricity (home, heat pump, electric car, digital use) and by the quick estimate.",
        "Se usa cada vez que un registro consume electricidad de red (vivienda, bomba de calor, auto eléctrico, uso digital) y en la estimación rápida."),
    "Serve de referência comparativa: a pontuação de 0 a 100 e os painéis comparam a sua pegada anualizada com esta média.": (
        "Serves as a comparison reference: the 0–100 score and the dashboards compare your annualized footprint to this average.",
        "Sirve de referencia comparativa: la puntuación de 0 a 100 y los paneles comparan tu huella anualizada con este promedio."),
    # ---- unidades dos fatores
    "quilômetros rodados": ("kilometers driven", "kilómetros recorridos"),
    "litros de combustível": ("liters of fuel", "litros de combustible"),
    "quilowatt-hora (kWh)": ("kilowatt-hour (kWh)", "kilovatio-hora (kWh)"),
    "quilowatt-hora por ano": ("kilowatt-hours per year", "kilovatios-hora por año"),
    "quilômetros por ano": ("kilometers per year", "kilómetros por año"),
    "metros cúbicos (m³)": ("cubic meters (m³)", "metros cúbicos (m³)"),
    "coeficiente adimensional (fração ou multiplicador)": ("dimensionless coefficient (fraction or multiplier)", "coeficiente adimensional (fracción o multiplicador)"),
    "refeições": ("meals", "comidas"),
    "unidades compradas": ("purchased units", "unidades compradas"),
    "reais gastos (R$)": ("reais spent (R$)", "reales gastados (ARS)"),
    "anos (por animal)": ("years (per animal)", "años (por animal)"),
    "viagens de ida e volta": ("round trips", "viajes de ida y vuelta"),
    "toneladas de CO₂ equivalente por pessoa ao ano": ("tonnes of CO₂ equivalent per person per year", "toneladas de CO₂ equivalente por persona por año"),
    # ---- frases especiais de fatores
    "Este fator não tem valor próprio: o motor de cálculo substitui automaticamente pelo fator da rede elétrica do país selecionado.": (
        "This factor has no value of its own: the engine automatically substitutes the selected country's grid factor.",
        "Este factor no tiene valor propio: el motor sustituye automáticamente por el factor de la red eléctrica del país elegido."),
    "A bomba de calor consome eletricidade: o motor converte o calor entregue em quilowatt-hora elétricos usando o COP e aplica o fator da rede do país.": (
        "The heat pump runs on electricity: the engine converts delivered heat into electric kWh using the COP and applies the country's grid factor.",
        "La bomba de calor consume electricidad: el motor convierte el calor entregado en kilovatios-hora eléctricos usando el COP y aplica el factor de la red del país."),
    "Este fator não tem valor próprio: o consumo digital é convertido em quilowatt-hora e calculado com o fator da rede elétrica do país.": (
        "This factor has no value of its own: digital use is converted to kWh and computed with the country's grid factor.",
        "Este factor no tiene valor propio: el consumo digital se convierte a kilovatios-hora y se calcula con el factor de la red eléctrica del país."),
    "Valor de referência (zero): as faixas anuais de direção (0, 4.000, 8.000 e 16.000 quilômetros) e os fatores de cada faixa são definidos no motor de cálculo.": (
        "Reference value (zero): yearly driving bands (0, 4,000, 8,000 and 16,000 km) and each band's factor live in the engine.",
        "Valor de referencia (cero): las franjas anuales de manejo (0, 4.000, 8.000 y 16.000 km) y sus factores están definidos en el motor."),
    "COP (coeficiente de performance): quantos quilowatt-hora de calor a bomba entrega para cada quilowatt-hora de eletricidade consumido.": (
        "COP (coefficient of performance): how many kWh of heat the pump delivers per kWh of electricity consumed.",
        "COP (coeficiente de rendimiento): cuántos kilovatios-hora de calor entrega la bomba por cada kilovatio-hora de electricidad consumida."),
    "Multiplicador aplicado à emissão do voo conforme a classe viajada; a classe econômica é a referência (1,0).": (
        "Multiplier applied to flight emissions by travel class; economy is the reference (1.0).",
        "Multiplicador aplicado a la emisión del vuelo según la clase viajada; económica es la referencia (1,0)."),
    "Multiplicador aplicado à emissão do voo conforme a classe viajada: a executiva ocupa mais espaço e peso por passageiro.": (
        "Multiplier applied to flight emissions by travel class: business seats take more space and weight per passenger.",
        "Multiplicador aplicado a la emisión del vuelo según la clase: ejecuta ocupa más espacio y peso por pasajero."),
    "Multiplicador aplicado à emissão do voo conforme a classe viajada: a primeira classe é a que mais emissões aloca por passageiro.": (
        "Multiplier applied to flight emissions by travel class: first class allocates the most emissions per passenger.",
        "Multiplicador aplicado a la emisión del vuelo según la clase: primera es la que más emisiones asigna por pasajero."),
    "Reduz em 8 por cento a emissão das refeições quando há preferência por produtos locais e de proximidade.": (
        "Cuts meal emissions by 8 percent when local and nearby products are preferred.",
        "Reduce un 8 por ciento la emisión de las comidas cuando se priorizan productos locales y de cercanía."),
    ("Regra de rateio do domicílio: o divisor total é 1 + 0,75 × (número de pessoas − 1), para que moradias compartilhadas dividam as emissões de forma justa."): (
        "Household sharing rule: the total divisor is 1 + 0.75 × (people − 1), so shared homes split emissions fairly.",
        "Regla de reparto del hogar: el divisor total es 1 + 0,75 × (personas − 1), para que los hogares compartidos dividan las emisiones de forma justa."),
    "Fonte registrada: {f}.": ("Registered source: {f}.", "Fuente registrada: {f}."),
    "Unidade do valor: {u}.": ("Value unit: {u}.", "Unidad del valor: {u}."),
    "O que representa: {d}.": ("What it represents: {d}.", "Qué representa: {d}."),
    "Valor calibrado pelo CO2calc e totalmente editável — substitua por um dado oficial quando houver.": (
        "Value calibrated by CO2calc and fully editable — replace with official data when available.",
        "Valor calibrado por CO2calc y totalmente editable — reemplazalo por un dato oficial cuando exista."),
    "taxonomia_sha256": ("taxonomia_sha256", "taxonomia_sha256"),
}

_CAT.update({
    "{flag} {pais} · {p} pessoas no domicílio": ("{flag} {pais} · {p} people in household", "{flag} {pais} · {p} personas en el hogar"),
    "🌐 Idioma: {l}": ("🌐 Language: {l}", "🌐 Idioma: {l}"),
    "Calcular minha pegada ⚡": ("Calculate my footprint ⚡", "Calculá mi huella ⚡"),
    "Aplicar idioma": ("Apply language", "Aplicar idioma"),
    "{pais} · {p} pessoas · {c} registros · {sz} kg": ("{pais} · {p} people · {c} entries · {sz} kg", "{pais} · {p} personas · {c} registros · {sz} kg"),
    "unidade": ("unit", "unidad"),
    "Estimativa quick: bens e serviços": ("Quick estimate: goods & services", "Estimación rápida: bienes y servicios"),
})

# linha incompleta (ES faltante) corrigida: chave trunca do bloco "Rede elétrica"
_CAT.pop("É a emissão média, em quilogramas de CO₂ equivalente, para entregar um quilowatt-hora de eletricidade na rede de {pais} — inclui a geração nas usinas e as perdas de transmissão e distribuição.", None)
_CAT["É a emissão média, em quilogramas de CO₂ equivalente, para entregar um quilowatt-hora de eletricidade na rede de {pais} — inclui a geração nas usinas e as perdas de transmissão e distribuição."] = (
    "Average emissions, in kilograms of CO₂ equivalent, needed to deliver one kilowatt-hour of electricity on {pais}'s grid — includes generation and transmission/distribution losses.",
    "Es la emisión media, en kilogramos de CO₂ equivalente, necesaria para entregar un kilovatio-hora de electricidad en la red de {pais} — incluye la generación y las pérdidas de transmisión y distribución.")
_CAT["É a pegada de carbono anual média de cada residente de {pais}, em toneladas de CO₂ equivalente, calculada a partir de estatísticas nacionais de energia e consumo."] = (
    "Average yearly carbon footprint of each resident of {pais}, in tonnes of CO₂ equivalent, computed from national energy and consumption statistics.",
    "Es la huella de carbono anual media de cada residente de {pais}, en toneladas de CO₂ equivalente, calculada a partir de estadísticas nacionales de energía y consumo.")
