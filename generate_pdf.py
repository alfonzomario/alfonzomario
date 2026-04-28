"""Genera el PDF comparativo Apollo vs Clay para presentar al jefe.

Uso: python3 generate_pdf.py
Salida: Apollo_vs_Clay_Analisis.pdf
"""

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    PageBreak,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)


PRIMARY = colors.HexColor("#0F172A")
ACCENT = colors.HexColor("#2563EB")
APOLLO_COLOR = colors.HexColor("#1E40AF")
CLAY_COLOR = colors.HexColor("#7C3AED")
LIGHT_BG = colors.HexColor("#F1F5F9")
MID_BG = colors.HexColor("#E2E8F0")
GREEN = colors.HexColor("#16A34A")
RED = colors.HexColor("#DC2626")
AMBER = colors.HexColor("#D97706")
TEXT = colors.HexColor("#0F172A")
MUTED = colors.HexColor("#475569")


def build_styles():
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "title", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=26, leading=30, textColor=PRIMARY, alignment=TA_LEFT, spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "subtitle", parent=base["Normal"], fontName="Helvetica",
            fontSize=12, leading=16, textColor=MUTED, alignment=TA_LEFT, spaceAfter=16,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"], fontName="Helvetica-Bold",
            fontSize=16, leading=20, textColor=PRIMARY, spaceBefore=14, spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=13, leading=17, textColor=ACCENT, spaceBefore=10, spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "body", parent=base["BodyText"], fontName="Helvetica",
            fontSize=10.5, leading=15, textColor=TEXT, alignment=TA_JUSTIFY, spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "bullet", parent=base["BodyText"], fontName="Helvetica",
            fontSize=10.5, leading=14, textColor=TEXT, leftIndent=14, bulletIndent=2, spaceAfter=3,
        ),
        "small": ParagraphStyle(
            "small", parent=base["Normal"], fontName="Helvetica",
            fontSize=9, leading=12, textColor=MUTED,
        ),
        "tag_apollo": ParagraphStyle(
            "tag_apollo", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=11, textColor=colors.white, alignment=TA_CENTER,
        ),
        "tag_clay": ParagraphStyle(
            "tag_clay", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=11, textColor=colors.white, alignment=TA_CENTER,
        ),
        "callout": ParagraphStyle(
            "callout", parent=base["Normal"], fontName="Helvetica",
            fontSize=10.5, leading=14, textColor=TEXT, alignment=TA_LEFT,
        ),
        "callout_bold": ParagraphStyle(
            "callout_bold", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=11, leading=14, textColor=PRIMARY,
        ),
        "verdict": ParagraphStyle(
            "verdict", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=14, leading=18, textColor=colors.white, alignment=TA_LEFT,
        ),
        "verdict_body": ParagraphStyle(
            "verdict_body", parent=base["Normal"], fontName="Helvetica",
            fontSize=10.5, leading=14, textColor=colors.white, alignment=TA_LEFT,
        ),
        "th": ParagraphStyle(
            "th", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=10, leading=12, textColor=colors.white, alignment=TA_CENTER,
        ),
        "td": ParagraphStyle(
            "td", parent=base["Normal"], fontName="Helvetica",
            fontSize=9.5, leading=12, textColor=TEXT, alignment=TA_LEFT,
        ),
        "td_label": ParagraphStyle(
            "td_label", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=9.5, leading=12, textColor=PRIMARY, alignment=TA_LEFT,
        ),
    }
    return styles


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(2 * cm, 1.2 * cm, "Apollo.io vs Clay  |  Analisis comparativo para decidir que herramienta usar")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Pagina {doc.page}")
    canvas.setStrokeColor(MID_BG)
    canvas.setLineWidth(0.5)
    canvas.line(2 * cm, 1.5 * cm, A4[0] - 2 * cm, 1.5 * cm)
    canvas.restoreState()


def colored_box(text, bg, style, width):
    """Single-cell table acting as a colored callout box."""
    tbl = Table([[Paragraph(text, style)]], colWidths=[width])
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("ROUNDEDCORNERS", [6, 6, 6, 6]),
            ]
        )
    )
    return tbl


def build_comparison_table(styles, page_width):
    P = lambda t, s="td": Paragraph(t, styles[s])
    rows = [
        [P("Criterio", "th"), P("APOLLO.io", "th"), P("CLAY.com", "th")],
        [
            P("Precio mas barato (anual)", "td_label"),
            P("$49 / usuario / mes (plan Basic)", "td"),
            P("$167 / mes (plan Launch) - sin limite de personas que lo usan", "td"),
        ],
        [
            P("Precio recomendado para nosotros", "td_label"),
            P("<b>$79 / usuario / mes</b> (plan Professional)", "td"),
            P("<b>$167 - $446 / mes</b> (Launch o Growth)", "td"),
        ],
        [
            P("Como te cobran", "td_label"),
            P("Pagas por persona del equipo + creditos para acciones. Los creditos se renuevan cada mes (lo que no usas se pierde).", "td"),
            P("Pagas por mes + 2 tipos de credito: <b>Data Credits</b> (para buscar datos) y <b>Actions</b> (para todo lo demas: enviar emails, ejecutar flujos). Lo que no uses se acumula hasta el doble.", "td"),
        ],
        [
            P("Buscar contactos nuevos", "td_label"),
            P("<font color='#16A34A'><b>SI, gratis</b></font> - tiene su propia base de datos con 275 millones de contactos y 60 millones de empresas, incluida en el plan.", "td"),
            P("<font color='#D97706'><b>SI, pero gastando creditos</b></font> - busca en 150+ proveedores externos pero cada busqueda consume creditos. Por eso hoy le pasas la lista hecha.", "td"),
        ],
        [
            P("Investigacion profunda con IA por cuenta", "td_label"),
            P("Tiene IA que investiga webs (usa Perplexity). <b>7.500 cuentas investigadas por mes</b> en plan Pro. Buena pero no tan profunda como Clay.", "td"),
            P("<b>Claygent</b>: agente que navega la web, LinkedIn, noticias, paginas de empleo. Lo mas profundo del mercado.", "td"),
        ],
        [
            P("Escribir emails personalizados con IA", "td_label"),
            P("IA propia que escribe emails (300.000 mensajes/mes en Pro). Funciona bien.", "td"),
            P("Excelente, totalmente personalizable por flujos de trabajo y prompts.", "td"),
        ],
        [
            P("Enviar campanias de email", "td_label"),
            P("<font color='#16A34A'><b>SI</b></font> - sistema completo de envio con varios pasos, llamador telefonico US, y permite probar 2 versiones distintas para ver cual funciona mejor.", "td"),
            P("<font color='#16A34A'><b>SI</b></font> - sistema basico de envio incorporado en 2025 (usa Smartlead por debajo). <b>Limites:</b> hasta 4 emails por campania, solo email, sin rotacion avanzada de casillas.", "td"),
        ],
        [
            P("Casillas de email por persona", "td_label"),
            P("Basic: 1-2 / <b>Pro: 5 casillas por persona</b> / Org: 15 casillas. Sugiere 50 emails/dia/casilla para no caer en spam.", "td"),
            P("<b>Casillas ilimitadas</b>, pero compartidas por todo el equipo. Sugiere ~24 emails/dia/casilla. El total de envios lo limita el cupo de Actions del plan.", "td"),
        ],
        [
            P("Cuantos emails podes mandar por mes", "td_label"),
            P("<b>Pro: ~250 emails/dia por persona</b> (5 casillas x 50). Mensual: ~5.000-7.500 emails. Org: ~750/dia por persona.", "td"),
            P("Launch: hasta ~15.000 emails/mes (cada email gasta 1 Action). Growth: hasta ~40.000/mes. Sin importar cuanta gente lo use.", "td"),
        ],
        [
            P("LinkedIn", "td_label"),
            P("<font color='#D97706'><b>Parcial</b></font>. Enriquece datos de perfiles + extension de Chrome para sacar emails desde LinkedIn. <b>Tareas manuales</b> en las campanias (te avisa que vayas a LinkedIn y lo hagas a mano). <b>NO automatiza solicitudes ni mensajes</b> (LinkedIn lo bloqueo en marzo 2025).", "td"),
            P("<font color='#D97706'><b>Solo saca datos</b></font>. Trae datos de perfiles, posts, cambios de trabajo (gastando creditos). <b>NO automatiza acciones en LinkedIn</b>. Tiene conexion nativa con HeyReach/Expandi para automatizar (son suscripciones aparte de ~$79-$99/mes).", "td"),
        ],
        [
            P("Calidad de los emails que entrega", "td_label"),
            P("~65-80% son validos (los demas rebotan o no existen). Una sola fuente.", "td"),
            P("~78%+ son validos. Mejor calidad porque consulta varias fuentes en cascada.", "td"),
        ],
        [
            P("Que tan facil es de usar", "td_label"),
            P("<font color='#16A34A'>Facil</font> - lo configuras y arrancas en pocas horas.", "td"),
            P("<font color='#D97706'>Dificil</font> - hay que invertir tiempo en aprenderlo. Mejor si hay alguien tecnico en el equipo.", "td"),
        ],
        [
            P("Costo por contacto investigado", "td_label"),
            P("$0,05-$0,15 (solo email) / hasta $0,80 (con telefono).", "td"),
            P("$0,30-$1,00 (con investigacion profunda).", "td"),
        ],
        [
            P("Que pasa si te quedas sin creditos", "td_label"),
            P("Riesgo medio. Compras extra a $0,20/credito (minimo $50).", "td"),
            P("Riesgo alto. Compras extra cuestan 30-50% mas caro que la tarifa del plan.", "td"),
        ],
        [
            P("Campanias masivas (cientos o miles de contactos)", "td_label"),
            P("<font color='#16A34A'><b>SI</b></font> - aguanta miles de contactos por mes sin problema.", "td"),
            P("<font color='#DC2626'>Carisimo</font> - los creditos se queman entre 200 y 800 contactos.", "td"),
        ],
        [
            P("Top 50-200 cuentas con investigacion profunda", "td_label"),
            P("Alcanza para la mayoria de los casos.", "td"),
            P("<font color='#16A34A'><b>Es el mejor</b></font>. No tiene competencia ahi.", "td"),
        ],
        [
            P("Calificacion en G2 (sitio de reviews)", "td_label"),
            P("4.7 / 5 (~9.400 reviews).", "td"),
            P("4.9 / 5.", "td"),
        ],
    ]

    col_widths = [page_width * 0.26, page_width * 0.37, page_width * 0.37]
    table = Table(rows, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), PRIMARY),
                ("BACKGROUND", (1, 0), (1, 0), APOLLO_COLOR),
                ("BACKGROUND", (2, 0), (2, 0), CLAY_COLOR),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LINEBELOW", (0, 0), (-1, -1), 0.4, MID_BG),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
                ("BOX", (0, 0), (-1, -1), 0.6, MID_BG),
            ]
        )
    )
    return table


def build_pros_cons_table(styles, page_width):
    P = lambda t, s="td": Paragraph(t, styles[s])

    apollo_pros = (
        "<b>A favor:</b><br/>"
        "+ Base de datos propia con 275 millones de contactos incluida en el plan: encontras clientes potenciales sin gastar creditos extra.<br/>"
        "+ Sistema de envio de campanias completo, con varios pasos, llamador telefonico y posibilidad de probar 2 versiones del email para ver cual funciona mejor.<br/>"
        "+ La IA puede investigar 7.500 cuentas por mes en el plan Pro.<br/>"
        "+ Costo predecible y barato (~$79 por persona, por mes).<br/>"
        "+ Facil de usar: el equipo arranca en horas, no semanas.<br/>"
        "+ Permite campanias masivas sin quemar el presupuesto en investigacion.<br/>"
        "+ Filtros avanzados ya incluidos: tecnologias que usa la empresa, rondas de financiacion, vacantes que tienen abiertas, senales de compra."
    )
    apollo_cons = (
        "<b>En contra:</b><br/>"
        "- La investigacion con IA es buena pero no tan profunda como la de Clay (no encadena varias fuentes).<br/>"
        "- 65-80% de los emails son validos: tasa de rebote mas alta que Clay.<br/>"
        "- Te cobran por persona del equipo: si sumas gente al equipo, el costo crece proporcionalmente.<br/>"
        "- Conseguir un numero de telefono cuesta 8 veces mas creditos que un email.<br/>"
        "- Menos flexible que Clay para armar flujos de trabajo personalizados.<br/>"
        "- LinkedIn: ya no automatiza acciones (LinkedIn lo bloqueo en 2025). Las tareas son manuales."
    )
    clay_pros = (
        "<b>A favor:</b><br/>"
        "+ Claygent: la investigacion mas profunda del mercado (web + LinkedIn + noticias + paginas de empleo).<br/>"
        "+ ~78%+ de emails validos consultando 150+ fuentes en cascada.<br/>"
        "+ Hojas de calculo flexibles: lo que imagines, lo armas.<br/>"
        "+ Sin limite de personas que lo usen: todo el equipo con una sola cuenta.<br/>"
        "+ Sistema de envio incorporado: 0,1 credito por email enviado, 0,5 por mensaje generado por IA.<br/>"
        "+ Calidad de salida premium para cuentas estrategicas.<br/>"
        "+ Los creditos no usados se acumulan hasta el doble del cupo mensual."
    )
    clay_cons = (
        "<b>En contra:</b><br/>"
        "- <b>El sistema de envio es basico:</b> maximo 4 pasos por campania, solo email, sin rotacion avanzada de casillas. Para volumen alto igual hay que sumar Instantly o Smartlead.<br/>"
        "- Buscar contactos tambien consume creditos (por eso hoy le pasas la lista hecha).<br/>"
        "- Tiene 2 tipos de credito (Data + Actions): la factura es impredecible.<br/>"
        "- En campanias masivas con investigacion profunda, 2.500 creditos se queman en 500-800 contactos.<br/>"
        "- Dificil de aprender: requiere alguien tecnico o varias semanas de practica.<br/>"
        "- Si una busqueda no encuentra resultados, igual te cobra el credito.<br/>"
        "- Comprar creditos extra cuesta 30-50% mas que la tarifa de tu plan.<br/>"
        "- LinkedIn: solo extrae datos. Para automatizar mensajes necesitas HeyReach o Expandi aparte ($79-99/mes adicionales)."
    )

    rows = [
        [
            Paragraph("APOLLO.io", styles["tag_apollo"]),
            Paragraph("CLAY.com", styles["tag_clay"]),
        ],
        [P(apollo_pros, "td"), P(clay_pros, "td")],
        [P(apollo_cons, "td"), P(clay_cons, "td")],
    ]
    col_widths = [page_width * 0.5, page_width * 0.5]
    table = Table(rows, colWidths=col_widths)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), APOLLO_COLOR),
                ("BACKGROUND", (1, 0), (1, 0), CLAY_COLOR),
                ("BACKGROUND", (0, 1), (0, 1), colors.HexColor("#EFF6FF")),
                ("BACKGROUND", (1, 1), (1, 1), colors.HexColor("#F5F3FF")),
                ("BACKGROUND", (0, 2), (0, 2), colors.HexColor("#FEF2F2")),
                ("BACKGROUND", (1, 2), (1, 2), colors.HexColor("#FEF2F2")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("TOPPADDING", (0, 1), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 12),
                ("BOX", (0, 0), (-1, -1), 0.5, MID_BG),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, MID_BG),
            ]
        )
    )
    return table


def build_decision_matrix(styles, page_width):
    P = lambda t, s="td": Paragraph(t, styles[s])

    rows = [
        [P("Lo mas importante para nosotros es...", "th"), P("Cual gana", "th"), P("Por que", "th")],
        [
            P("Mandar campanias grandes (1.000+ contactos/mes) con personalizacion media", "td"),
            P("<b><font color='#1E40AF'>APOLLO</font></b>", "td"),
            P("Apollo te da base de datos + 7.500 cuentas investigadas con IA por mes + sistema de envio multi-paso. El de Clay es basico (max 4 pasos) y a ese volumen los creditos se evaporan.", "td"),
        ],
        [
            P("Top 50-200 cuentas con investigacion super profunda", "td"),
            P("<b><font color='#7C3AED'>CLAY</font></b>", "td"),
            P("Claygent es el unico agente que hace investigacion profunda de verdad. Si la agencia vende personalizacion como diferencial, vale el costo.", "td"),
        ],
        [
            P("Que el costo mensual sea predecible", "td"),
            P("<b><font color='#1E40AF'>APOLLO</font></b>", "td"),
            P("Plan + creditos con tope claro. Clay tiene 2 tipos de credito y los extras cuestan 30-50% mas caros.", "td"),
        ],
        [
            P("Equipo chico sin perfil tecnico", "td"),
            P("<b><font color='#1E40AF'>APOLLO</font></b>", "td"),
            P("Apollo se aprende en horas. Clay requiere semanas de practica para sacarle jugo.", "td"),
        ],
        [
            P("Que la mayor cantidad de emails sean validos (poco rebote)", "td"),
            P("<b><font color='#7C3AED'>CLAY</font></b>", "td"),
            P("Consultar 150+ fuentes en cascada da ~78%+ de validez vs ~65-80% de Apollo (una sola fuente).", "td"),
        ],
        [
            P("Hacer flujos super personalizados con disparadores (vacantes nuevas, financiacion, etc)", "td"),
            P("<b><font color='#7C3AED'>CLAY</font></b>", "td"),
            P("Apollo tiene algunas senales de compra, pero Clay arma cualquier flujo imaginable y lo automatiza.", "td"),
        ],
        [
            P("Tener TODO en una sola herramienta (base de datos + investigacion + envio)", "td"),
            P("<b><font color='#1E40AF'>APOLLO</font></b>", "td"),
            P("Apollo trae base de datos + envio multi-paso + llamador. Clay tambien envia, pero su sistema es basico (max 4 pasos) y la base de datos se paga por cada busqueda.", "td"),
        ],
        [
            P("Que el costo por contacto sea lo mas bajo posible", "td"),
            P("<b><font color='#1E40AF'>APOLLO</font></b>", "td"),
            P("$0,05-$0,15 por contacto investigado en Apollo vs $0,30-$1,00 en Clay con investigacion profunda.", "td"),
        ],
    ]
    col_widths = [page_width * 0.36, page_width * 0.16, page_width * 0.48]
    table = Table(rows, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
                ("BOX", (0, 0), (-1, -1), 0.6, MID_BG),
                ("LINEBELOW", (0, 0), (-1, -1), 0.4, MID_BG),
            ]
        )
    )
    return table


def build_mailbox_table(styles, page_width):
    P = lambda t, s="td": Paragraph(t, styles[s])
    rows = [
        [P("Plan", "th"), P("Casillas que podes conectar", "th"), P("Emails por dia recomendados", "th"), P("Cuantos emails por mes (aprox)", "th")],
        [P("Apollo <b>Basic</b> ($49/persona/mes)", "td"), P("1-2 por persona", "td"), P("50 por casilla", "td"), P("~1.000-2.500 emails por persona", "td")],
        [P("Apollo <b>Professional</b> ($79/persona/mes)", "td"), P("<b>5 casillas por persona</b>", "td"), P("50 por casilla = 250 por persona", "td"), P("<b>~5.000-7.500 emails por persona</b>", "td")],
        [P("Apollo <b>Organization</b> ($119/persona/mes)", "td"), P("15 casillas por persona", "td"), P("50 por casilla = 750 por persona", "td"), P("~15.000-22.500 emails por persona", "td")],
        [P("Clay <b>Launch</b> ($167/mes)", "td"), P("Ilimitadas, compartidas por todo el equipo*", "td"), P("~24 por casilla sugerido", "td"), P("Tope ~<b>15.000 emails/mes</b> en total", "td")],
        [P("Clay <b>Growth</b> ($446/mes)", "td"), P("Ilimitadas, compartidas por todo el equipo*", "td"), P("~24 por casilla sugerido", "td"), P("Tope ~<b>40.000 emails/mes</b> en total", "td")],
    ]
    col_widths = [page_width * 0.30, page_width * 0.20, page_width * 0.24, page_width * 0.26]
    table = Table(rows, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("ROWBACKGROUNDS", (0, 1), (-1, 3), [colors.HexColor("#EFF6FF"), colors.HexColor("#DBEAFE")]),
                ("ROWBACKGROUNDS", (0, 4), (-1, 5), [colors.HexColor("#F5F3FF"), colors.HexColor("#EDE9FE")]),
                ("BOX", (0, 0), (-1, -1), 0.6, MID_BG),
                ("LINEBELOW", (0, 0), (-1, -1), 0.4, MID_BG),
            ]
        )
    )
    return table


def build_cost_table(styles, page_width):
    P = lambda t, s="td": Paragraph(t, styles[s])
    rows = [
        [P("Escenario (precio mensual)", "th"), P("APOLLO.io", "th"), P("CLAY.com", "th")],
        [
            P("Plan recomendado, 1 persona usandolo", "td_label"),
            P("Pro: $79", "td"),
            P("Launch: $167  |  Growth: $446", "td"),
        ],
        [
            P("Si suma 1 persona mas al equipo (2 en total)", "td_label"),
            P("$158", "td"),
            P("Igual ($167 o $446) - no cobra extra por gente", "td"),
        ],
        [
            P("Si suma 3 personas mas al equipo (4 en total)", "td_label"),
            P("$316", "td"),
            P("Igual ($167 o $446) - no cobra extra por gente", "td"),
        ],
        [
            P("Cuantos contactos podes investigar al mes", "td_label"),
            P("Hasta 7.500 con la IA", "td"),
            P("~500 (Launch) o ~2.000 (Growth) con investigacion profunda", "td"),
        ],
        [
            P("Permite enviar campanias de email?", "td_label"),
            P("<font color='#16A34A'><b>SI</b></font> - varios pasos + probar 2 versiones del email + llamador US", "td"),
            P("<font color='#16A34A'><b>SI</b></font>, basico (max 4 pasos, solo email). Cada email gasta 0,1 credito. Para volumen alto conviene sumar otra herramienta de envio.", "td"),
        ],
        [
            P("Costo total realista para 1 persona", "td_label"),
            P("<b>~$79-$130 / mes</b>", "td"),
            P("<b>~$167-$520 / mes</b>", "td"),
        ],
        [
            P("Costo total realista para 3 personas", "td_label"),
            P("<b>~$237-$390 / mes</b>", "td"),
            P("<b>~$167-$520 / mes</b> (no cobra extra por gente)", "td"),
        ],
    ]
    col_widths = [page_width * 0.34, page_width * 0.30, page_width * 0.36]
    table = Table(rows, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), PRIMARY),
                ("BACKGROUND", (1, 0), (1, 0), APOLLO_COLOR),
                ("BACKGROUND", (2, 0), (2, 0), CLAY_COLOR),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
                ("BOX", (0, 0), (-1, -1), 0.6, MID_BG),
            ]
        )
    )
    return table


def build_pdf(output_path: str = "Apollo_vs_Clay_Analisis.pdf"):
    styles = build_styles()
    doc = BaseDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Apollo vs Clay - Analisis comparativo",
        author="Equipo de marketing",
    )
    page_width = doc.width
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    template = PageTemplate(id="main", frames=frame, onPage=header_footer)
    doc.addPageTemplates([template])

    story = []

    # ------------- COVER -------------
    cover_block = Table(
        [
            [Paragraph("APOLLO.io <b>vs</b> CLAY.com", styles["title"])],
            [Paragraph(
                "Que herramienta de busqueda y contacto de clientes elegir para nuestra agencia<br/>"
                "Analisis, comparativa y recomendacion final",
                styles["subtitle"]
            )],
        ],
        colWidths=[page_width],
    )
    cover_block.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    story.append(cover_block)

    # Highlight veredict box on cover
    verdict_text = (
        "<b>Conclusion en una linea:</b><br/>"
        "Para nuestra agencia (presupuesto acotado + necesidad de combinar campanias grandes con campanias top 200 personalizadas), "
        "<b>APOLLO Professional ($79 por persona, por mes)</b> es la eleccion correcta. "
        "Clay es superior en profundidad de investigacion por cuenta, pero su modelo de creditos hace que cada busqueda, "
        "cada email enviado y cada mensaje generado por IA pague tarifa. Apollo trae base de datos propia incluida, "
        "sistema de envio completo, e investigacion con IA suficiente para personalizar a escala, a un tercio del costo total."
    )
    verdict_box = Table(
        [[Paragraph(verdict_text, styles["verdict_body"])]],
        colWidths=[page_width],
    )
    verdict_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), APOLLO_COLOR),
                ("LEFTPADDING", (0, 0), (-1, -1), 16),
                ("RIGHTPADDING", (0, 0), (-1, -1), 16),
                ("TOPPADDING", (0, 0), (-1, -1), 14),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
            ]
        )
    )
    story.append(verdict_box)
    story.append(Spacer(1, 14))

    # ------------- 1. CONTEXTO -------------
    story.append(Paragraph("1. Contexto y problema actual", styles["h1"]))
    story.append(Paragraph(
        "Hoy usamos Clay para campanias tipo top 200: pasamos una lista de 200 contactos buscados a mano, Clay investiga "
        "cada cuenta a fondo y arma un email personalizado. Tambien enviamos las campanias desde el sistema de envio de "
        "Clay. La calidad del resultado es buena, pero el modelo de creditos hace que cada campania nos consuma mucho "
        "presupuesto, dejandonos sin margen para correr campanias mas grandes en paralelo. Antes usabamos Apollo, y la "
        "duda es si volver a Apollo (o quedarnos en Clay) sin perder personalizacion ni calidad.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>Conclusion del analisis:</b> ambas hoy hacen lo mismo a grandes rasgos (buscan contactos, investigan con IA "
        "y envian emails), pero con filosofias muy distintas. Apollo es una <i>plataforma todo-en-uno con base de datos "
        "propia</i>, sistema de envio completo y llamador telefonico; la investigacion con IA es solida pero menos "
        "profunda. Clay es un <i>motor de investigacion y enriquecimiento de datos premium</i> con un sistema de envio "
        "basico (lanzado en 2025), donde cada paso (buscar contactos, enviar emails, generar mensajes con IA) consume "
        "creditos. La eleccion depende de si valoramos mas la profundidad por cuenta, o la capacidad de hacer campanias "
        "grandes con costo predecible.",
        styles["body"]
    ))

    # ------------- 2. TABLA COMPARATIVA -------------
    story.append(Paragraph("2. Tabla comparativa Apollo vs Clay", styles["h1"]))
    story.append(Paragraph(
        "Comparativa criterio por criterio. Datos basados en pricing publico vigente a abril 2026.",
        styles["body"]
    ))
    story.append(Spacer(1, 4))
    story.append(build_comparison_table(styles, page_width))

    story.append(PageBreak())

    # ------------- 3. CASILLAS DE EMAIL Y VOLUMEN DE ENVIO -------------
    story.append(Paragraph("3. Casillas de email y cuantos podemos enviar", styles["h1"]))
    story.append(Paragraph(
        "Pregunta clave para no caer en spam y para saber cuantas campanias podemos correr en paralelo: "
        "<b>cuantas casillas de email podemos conectar y cuantos emails podemos enviar por dia</b>. "
        "Las dos plataformas tienen modelos distintos.",
        styles["body"]
    ))
    story.append(Spacer(1, 4))
    story.append(build_mailbox_table(styles, page_width))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Como se lee esta tabla:</b>", styles["body"]
    ))
    bullets_mailbox = [
        "<b>Apollo cobra por persona y te da casillas por persona.</b> Si 1 persona usa el plan Pro: 5 casillas con capacidad real de ~250 emails/dia. Si sumamos otra persona ($79 mas): otras 5 casillas y duplicamos volumen.",
        "<b>Clay cobra por mes, casillas ilimitadas pero compartidas.</b> Conectas las que quieras, todas comparten el mismo cupo del plan. En Launch (15.000 Actions/mes) podes enviar ~15.000 emails antes de quedarte sin nada para investigar.",
        "Apollo recomienda 50 emails/dia por casilla (es conservador, los limites de Gmail/Workspace son 500-2.000). Clay recomienda ~24/dia por casilla para que los emails lleguen mejor a la bandeja de entrada.",
        "<b>* En Clay las casillas son del workspace</b>: no se multiplican si suma gente. Eso es bueno (no pagas por persona) pero malo si necesitas mucho volumen (te frena el cupo total).",
        "Para campanias serias (1.000+ emails/dia) en cualquiera de las dos conviene comprar dominios alternativos y \"calentar\" las casillas (mandar emails de prueba un par de semanas antes). Esto es independiente de la herramienta.",
    ]
    for b in bullets_mailbox:
        story.append(Paragraph(b, styles["bullet"], bulletText="•"))

    story.append(Spacer(1, 8))
    callout = (
        "<b>Conclusion practica para nuestra agencia:</b><br/>"
        "Con Apollo Professional, 1 persona = 5 casillas = ~5.000-7.500 emails/mes con buena entregabilidad. "
        "Con Clay Launch no hay tope de casillas, pero si un tope de 15.000 emails/mes que ademas se comparte con "
        "todo lo demas (investigacion, mensajes IA). <b>Clay obliga a elegir: o investigas, o envias</b>; "
        "Apollo tiene cupos separados para cada cosa."
    )
    callout_box = Table([[Paragraph(callout, styles["verdict_body"])]], colWidths=[page_width])
    callout_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), APOLLO_COLOR),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    story.append(callout_box)

    story.append(PageBreak())

    # ------------- 4. PROS Y CONTRAS -------------
    story.append(Paragraph("4. A favor y en contra de cada herramienta", styles["h1"]))
    story.append(Spacer(1, 4))
    story.append(build_pros_cons_table(styles, page_width))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Aclaracion sobre LinkedIn (importante)", styles["h2"]))
    story.append(Paragraph(
        "En 2026 ninguna de las dos herramientas automatiza acciones reales en LinkedIn (mensajes directos, "
        "solicitudes de conexion, InMails). LinkedIn bloqueo a Apollo, Seamless.ai y otras en marzo de 2025, "
        "quitandoles el acceso para extraer datos. Lo que ofrecen hoy es:",
        styles["body"]
    ))
    bullets_li = [
        "<b>Apollo:</b> extension de Chrome para sacar emails desde perfiles de LinkedIn + recordatorios manuales en las campanias (te avisa que vayas a LinkedIn y hagas la accion vos mismo).",
        "<b>Clay:</b> extrae datos de los perfiles (puesto, posts, cambios de trabajo) consumiendo creditos + tiene conexion lista con HeyReach (~$79/mes) que SI automatiza acciones en LinkedIn.",
        "<b>Para automatizar LinkedIn de verdad</b> (que es lo unico que escala) las dos requieren contratar otra herramienta: HeyReach, Expandi o La Growth Machine, que cuestan entre $79 y $120/mes por persona.",
        "<b>Conclusion:</b> en LinkedIn las dos estan empatadas (= ninguna lo hace por su cuenta). Esto NO deberia ser un factor decisivo entre Apollo y Clay.",
    ]
    for b in bullets_li:
        story.append(Paragraph(b, styles["bullet"], bulletText="•"))

    # ------------- 5. COSTOS -------------
    story.append(Paragraph("5. Costo real proyectado", styles["h1"]))
    story.append(Paragraph(
        "El precio que figura en la web no es el costo real. Hay que sumar lo que se paga si te pasas "
        "del cupo (extras), y sumar gente al equipo (en Apollo eso multiplica el costo).",
        styles["body"]
    ))
    story.append(Spacer(1, 4))
    story.append(build_cost_table(styles, page_width))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Lectura clave:</b> Apollo es mas barato si somos 1 o 2 personas usandolo. Clay no aumenta de "
        "precio si suma gente, pero su sistema de envio es basico (4 pasos maximo); para campanias "
        "serias terminas sumando otra herramienta de envio aparte. Si somos 3 personas activas, los "
        "costos se igualan, pero Apollo nos da la base de datos y el sistema de envio multi-paso "
        "incluidos (Clay no).",
        styles["body"]
    ))

    story.append(PageBreak())

    # ------------- 6. MATRIZ DE DECISION -------------
    story.append(Paragraph("6. Que herramienta elegir segun la prioridad", styles["h1"]))
    story.append(Paragraph(
        "Esta tabla resume bajo que prioridad cada herramienta gana. Buscamos cual coincide con nuestras "
        "prioridades como agencia.",
        styles["body"]
    ))
    story.append(Spacer(1, 4))
    story.append(build_decision_matrix(styles, page_width))

    # ------------- 7. RECOMENDACION FINAL -------------
    story.append(Paragraph("7. Recomendacion final para la agencia", styles["h1"]))

    rec_text = (
        "<b>Recomendamos APOLLO plan Professional</b> ($79 por persona, por mes, pago anual) por estas razones:"
    )
    story.append(Paragraph(rec_text, styles["body"]))

    bullets = [
        "<b>Base de datos propia incluida</b> (275 millones de contactos): encontramos clientes nuevos sin gastar creditos por cada busqueda, como pasa hoy en Clay.",
        "<b>Investigacion con IA incluida</b>: hasta 7.500 cuentas investigadas por mes con IA que navega webs (usa Perplexity). Suficientemente profundo para personalizar emails uno por uno en campanias top 200 y tambien correr campanias mas grandes en paralelo.",
        "<b>Sistema de envio completo + llamador telefonico</b>: el de Clay es basico (maximo 4 pasos por campania, solo email, sin rotacion avanzada de casillas). Apollo lo supera para volumen serio.",
        "<b>5 casillas de email por persona</b> en Pro: ~250 emails/dia por persona con buena entregabilidad. Y el cupo de envios esta separado del de investigacion (en Clay todo sale del mismo bolsillo).",
        "<b>Costo predecible</b>: sistema de un solo credito mas simple que el de doble credito de Clay (Data + Actions), y evita comprar extras con 30-50% de recargo.",
        "<b>Facil de aprender</b>: el equipo arranca en horas, no semanas. Clay requiere alguien tecnico dedicado que hoy no tenemos.",
        "<b>Habilita las dos campanias que necesitamos</b>: top 200 con personalizacion fuerte + campanias mas grandes con personalizacion media. Clay solo cubre bien la primera por costo.",
    ]
    for b in bullets:
        story.append(Paragraph(b, styles["bullet"], bulletText="•"))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Cuando volveriamos a evaluar Clay", styles["h2"]))
    story.append(Paragraph(
        "Clay tiene sentido cuando: (a) la agencia tenga alguien tecnico dedicado a armar flujos de trabajo, "
        "(b) empecemos a cerrar cuentas mas grandes donde la calidad de la investigacion justifique pagar el costo "
        "extra, o (c) Apollo deje de cubrir la cantidad o calidad de contactos que necesitemos. Hasta entonces, "
        "conviene Apollo.",
        styles["body"]
    ))

    # Final callout
    final_text = (
        "<b>Plan de accion sugerido:</b><br/>"
        "1) Probar Apollo gratis (50 creditos) para validar la calidad de los datos en nuestro nicho.<br/>"
        "2) Pasar a Apollo Professional con plan anual ($79 por persona, por mes) - 20% de descuento contra el plan mensual.<br/>"
        "3) Disenar plantillas para que la IA investigue las cuentas y arme una oracion personalizada para cada email.<br/>"
        "4) Pausar Clay al cierre del ciclo actual; guardar los flujos que armamos como referencia para el futuro.<br/>"
        "5) Reevaluar a los 90 dias con metricas: tasa de apertura, tasa de respuesta, costo por reunion agendada."
    )
    final_box = Table([[Paragraph(final_text, styles["verdict_body"])]], colWidths=[page_width])
    final_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PRIMARY),
                ("LEFTPADDING", (0, 0), (-1, -1), 16),
                ("RIGHTPADDING", (0, 0), (-1, -1), 16),
                ("TOPPADDING", (0, 0), (-1, -1), 14),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
            ]
        )
    )
    story.append(Spacer(1, 8))
    story.append(final_box)

    # ------------- 8. GLOSARIO -------------
    story.append(Spacer(1, 14))
    story.append(Paragraph("8. Glosario rapido (terminos que aparecen en el PDF)", styles["h1"]))
    glossary_rows = [
        [Paragraph("<b>Termino</b>", styles["td_label"]), Paragraph("<b>Que significa</b>", styles["td_label"])],
        [Paragraph("Apollo / Clay", styles["td"]),
         Paragraph("Las dos plataformas que estamos comparando. Sirven para encontrar contactos, investigarlos y mandarles emails.", styles["td"])],
        [Paragraph("Credito", styles["td"]),
         Paragraph("Una unidad que se gasta cada vez que la herramienta hace algo (buscar un email, generar texto con IA, enviar un email). Cada plan trae una cantidad mensual.", styles["td"])],
        [Paragraph("Data Credits / Actions (Clay)", styles["td"]),
         Paragraph("Clay tiene 2 tipos de credito. Data Credits = para comprar datos (emails, telefonos). Actions = para todo lo demas (correr flujos, enviar emails, generar mensajes con IA).", styles["td"])],
        [Paragraph("Claygent", styles["td"]),
         Paragraph("Es el agente de IA de Clay que navega la web por su cuenta para investigar empresas y personas.", styles["td"])],
        [Paragraph("Casilla de email / mailbox", styles["td"]),
         Paragraph("Una direccion de email desde la que se mandan campanias (ej: ventas@miagencia.com). Conviene tener varias para no quemar una sola y caer en spam.", styles["td"])],
        [Paragraph("Calentar / warmup", styles["td"]),
         Paragraph("Proceso de mandar emails de prueba durante un par de semanas para que Gmail/Outlook confien en una casilla nueva y no la marquen como spam.", styles["td"])],
        [Paragraph("Tasa de rebote", styles["td"]),
         Paragraph("Porcentaje de emails que no llegan al destinatario porque la direccion no existe o esta mal. Mientras mas baja, mejor.", styles["td"])],
        [Paragraph("Tasa de apertura / respuesta", styles["td"]),
         Paragraph("Tasa de apertura: % de gente que abrio tu email. Tasa de respuesta: % que efectivamente te contesto.", styles["td"])],
        [Paragraph("HeyReach / Expandi", styles["td"]),
         Paragraph("Herramientas externas para automatizar acciones en LinkedIn (mandar mensajes, conectar). Cuestan $79-99/mes adicionales.", styles["td"])],
        [Paragraph("Instantly / Smartlead", styles["td"]),
         Paragraph("Herramientas externas especializadas en envio masivo de emails con buena entregabilidad. Cuestan $30-100/mes.", styles["td"])],
    ]
    glossary_table = Table(glossary_rows, colWidths=[page_width * 0.30, page_width * 0.70])
    glossary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), MID_BG),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
                ("BOX", (0, 0), (-1, -1), 0.5, MID_BG),
                ("LINEBELOW", (0, 0), (-1, -1), 0.4, MID_BG),
            ]
        )
    )
    story.append(glossary_table)

    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "<i>Fuentes: pricing oficial de apollo.io/pricing y clay.com/pricing (abril 2026); reviews de G2; "
        "analisis publicos de Docket.io, Landbase, Salesmotion, Genesy.ai y Pipeline.help.</i>",
        styles["small"]
    ))

    doc.build(story)
    print(f"PDF generado: {output_path}")


if __name__ == "__main__":
    build_pdf()
