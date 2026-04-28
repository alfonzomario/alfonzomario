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
    canvas.drawString(2 * cm, 1.2 * cm, "Apollo.io vs Clay  |  Analisis comparativo para decision de stack")
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
            P("Precio entrada (anual)", "td_label"),
            P("$49 / usuario / mes (Basic)", "td"),
            P("$167 / mes (Launch) - sin limite de usuarios", "td"),
        ],
        [
            P("Precio recomendado", "td_label"),
            P("<b>$79 / usuario / mes</b> (Professional)", "td"),
            P("<b>$167 - $446 / mes</b> (Launch o Growth)", "td"),
        ],
        [
            P("Modelo de cobro", "td_label"),
            P("Por usuario + creditos. Vence mensual.", "td"),
            P("Por mes + 2 tipos de credito (Data + Actions). Roll-over hasta 2x.", "td"),
        ],
        [
            P("Busqueda de contactos", "td_label"),
            P("<font color='#16A34A'><b>SI</b></font> - base propia 275M+ contactos / 60M+ empresas, incluida en plan.", "td"),
            P("<font color='#D97706'><b>SI, pero consume creditos</b></font> - 150+ providers via Data Credits. Por eso conviene traer lista propia.", "td"),
        ],
        [
            P("Deep research con IA", "td_label"),
            P("AI Research (Perplexity Sonar). Bueno, no tan profundo. <b>7.500 lookups/mes en Pro</b>.", "td"),
            P("<b>Claygent</b>: agente que navega webs, LinkedIn, news, careers. Lo mas profundo del mercado.", "td"),
        ],
        [
            P("Personalizacion de emails", "td_label"),
            P("AI Composer (300K creditos/mes en Pro). Muy decente.", "td"),
            P("Excelente, totalmente custom via prompts y workflows.", "td"),
        ],
        [
            P("Envio de emails / sequencer", "td_label"),
            P("<font color='#16A34A'><b>SI</b></font> - sequencer multi-paso + dialer US + A/B testing.", "td"),
            P("<font color='#16A34A'><b>SI</b></font> - sequencer nativo (powered by Smartlead) lanzado en 2025. <b>Limites:</b> hasta 4 pasos por campania, solo email, sin inbox rotation avanzada.", "td"),
        ],
        [
            P("Casillas de email (mailboxes) por usuario", "td_label"),
            P("Basic: ~1-2 / <b>Pro: 5 mailboxes/usuario</b> / Org: 15 mailboxes/usuario. Recomendado 50 emails/dia/mailbox.", "td"),
            P("<b>Ilimitadas por workspace</b> (no por usuario). Recomendado ~24 emails/dia/mailbox. El cupo real lo limitan los Actions del plan.", "td"),
        ],
        [
            P("Volumen practico de envio", "td_label"),
            P("<b>Pro: ~250 emails/dia/usuario</b> (5 mailboxes x 50). Mensual: ~5.000-7.500 emails. Org: ~750/dia/usuario.", "td"),
            P("Launch: hasta ~15.000 emails/mes (1 Action por email). Growth: hasta ~40.000/mes. Sin tope por usuario.", "td"),
        ],
        [
            P("Match rate de email", "td_label"),
            P("~65-80% (single-source).", "td"),
            P("~78%+ por waterfall multi-provider.", "td"),
        ],
        [
            P("Curva de aprendizaje", "td_label"),
            P("<font color='#16A34A'>Baja</font> - plug & play.", "td"),
            P("<font color='#D97706'>Alta</font> - requiere mentalidad RevOps.", "td"),
        ],
        [
            P("Costo por lead enriquecido", "td_label"),
            P("$0,05-$0,15 (email) / hasta $0,80 (con telefono).", "td"),
            P("$0,30-$1,00 (workflow con research profundo).", "td"),
        ],
        [
            P("Riesgo de overage", "td_label"),
            P("Medio. $0,20/credito extra (min $50).", "td"),
            P("Alto. Top-ups +30-50% sobre tarifa de plan.", "td"),
        ],
        [
            P("Campanias masivas", "td_label"),
            P("<font color='#16A34A'><b>SI</b></font> - capacidad para miles/mes.", "td"),
            P("<font color='#DC2626'>Caro</font> - se quema en 200-800 contactos.", "td"),
        ],
        [
            P("Top 50-200 cuentas con research", "td_label"),
            P("Suficiente para la mayoria de casos.", "td"),
            P("<font color='#16A34A'><b>El mejor</b></font>. Sin competencia.", "td"),
        ],
        [
            P("G2 rating", "td_label"),
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
        "<b>Pros:</b><br/>"
        "+ Base de datos de 275M+ contactos incluida en el plan: descubris prospects sin gastar creditos extra.<br/>"
        "+ Sequencer multi-paso + dialer US integrados, con A/B testing avanzado.<br/>"
        "+ AI Research te alcanza para 7.500 cuentas/mes en Professional.<br/>"
        "+ Costo predecible y barato a escala (~$79/usuario/mes).<br/>"
        "+ Curva de aprendizaje baja: tu equipo arranca en horas, no semanas.<br/>"
        "+ Permite campanias masivas SIN quemar el presupuesto en research.<br/>"
        "+ Intent data y filtros avanzados (technographics, funding, hiring) nativos."
    )
    apollo_cons = (
        "<b>Contras:</b><br/>"
        "- AI Research es bueno pero no tan profundo como Claygent (no encadena scraping multi-fuente).<br/>"
        "- Match rate de email ~65-80%: bounce rate mas alto que Clay.<br/>"
        "- Cobranza por usuario: si suma el equipo, escala lineal.<br/>"
        "- Telefono cuesta 8x mas creditos que email.<br/>"
        "- Workflows custom limitados comparado con la flexibilidad spreadsheet de Clay."
    )
    clay_pros = (
        "<b>Pros:</b><br/>"
        "+ Claygent: research mas profundo del mercado (web + LinkedIn + news + careers).<br/>"
        "+ Match rate ~78%+ por waterfall multi-provider sobre 150+ fuentes.<br/>"
        "+ Workflows custom tipo spreadsheet: lo que imagines, lo armas.<br/>"
        "+ Sin tope de usuarios: el equipo entero usa una sola cuenta.<br/>"
        "+ Sequencer nativo (powered by Smartlead) ya integrado: 0,1 credito por email enviado, 0,5 por AI snippet.<br/>"
        "+ Calidad de output premium para top accounts.<br/>"
        "+ Roll-over de Data Credits hasta 2x del cupo mensual."
    )
    clay_cons = (
        "<b>Contras:</b><br/>"
        "- <b>Sequencer es basico:</b> max 4 pasos por campania, solo email, sin inbox rotation avanzada ni IP management. Para volumen serio igual hace falta Instantly/Smartlead.<br/>"
        "- Buscar contactos en Clay tambien consume Data Credits (por eso traes lista propia hoy).<br/>"
        "- Doble sistema de creditos (Data + Actions) = factura impredecible.<br/>"
        "- Campanias masivas con research profundo: 2.500 Data Credits se queman en 500-800 contactos.<br/>"
        "- Curva de aprendizaje alta: requiere RevOps o varias semanas para sacarle jugo.<br/>"
        "- Failed lookups igual cobran credito.<br/>"
        "- Top-ups con 30-50% de premium sobre la tarifa de plan."
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
        [P("Si tu prioridad es...", "th"), P("Eleccion", "th"), P("Por que", "th")],
        [
            P("Mandar campanias masivas (1.000+ leads/mes) con personalizacion media", "td"),
            P("<b><font color='#1E40AF'>APOLLO</font></b>", "td"),
            P("Apollo Pro te da base de datos + 7.500 AI researches/mes + sequencer multi-paso. El sequencer de Clay es basico (max 4 pasos, sin inbox rotation) y a ese volumen los creditos se evaporan.", "td"),
        ],
        [
            P("Top 50-200 cuentas con research super profundo (campanias ABM premium)", "td"),
            P("<b><font color='#7C3AED'>CLAY</font></b>", "td"),
            P("Claygent es el unico agente que hace deep research real. Si tu agencia vende personalizacion como diferencial, vale el costo.", "td"),
        ],
        [
            P("Costo predecible mes a mes", "td"),
            P("<b><font color='#1E40AF'>APOLLO</font></b>", "td"),
            P("Plan + creditos con tope claro. Clay tiene doble sistema de creditos y top-ups +30-50%.", "td"),
        ],
        [
            P("Equipo pequeno sin perfil tecnico/RevOps", "td"),
            P("<b><font color='#1E40AF'>APOLLO</font></b>", "td"),
            P("Plug and play. Clay requiere semanas de setup y mentalidad de RevOps para sacarle jugo.", "td"),
        ],
        [
            P("Match rate maximo de emails (bounce rate bajo)", "td"),
            P("<b><font color='#7C3AED'>CLAY</font></b>", "td"),
            P("Waterfall sobre 150+ providers da ~78%+ vs ~65-80% de Apollo single-source.", "td"),
        ],
        [
            P("Workflows muy custom y dependientes de senales (intent, hiring, funding)", "td"),
            P("<b><font color='#7C3AED'>CLAY</font></b>", "td"),
            P("Apollo tiene intent topics pero Clay arma cualquier workflow imaginable y lo automatiza.", "td"),
        ],
        [
            P("Tener TODO en una sola herramienta (DB + research + envio)", "td"),
            P("<b><font color='#1E40AF'>APOLLO</font></b>", "td"),
            P("Apollo trae base de datos propia + sequencer multi-paso + dialer. Clay tambien envia, pero su sequencer es basico (max 4 pasos) y la base de datos se paga por cada lookup.", "td"),
        ],
        [
            P("Optimizar el costo por lead a escala", "td"),
            P("<b><font color='#1E40AF'>APOLLO</font></b>", "td"),
            P("$0,05-$0,15 por lead enriquecido vs $0,30-$1,00 en Clay con workflow profundo.", "td"),
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
        [P("Plan", "th"), P("Mailboxes incluidas", "th"), P("Emails / dia recomendados", "th"), P("Volumen mensual aprox", "th")],
        [P("Apollo <b>Basic</b> ($49/usuario/mes)", "td"), P("1-2 por usuario", "td"), P("50/dia/mailbox", "td"), P("~1.000-2.500 emails/usuario/mes", "td")],
        [P("Apollo <b>Professional</b> ($79/usuario/mes)", "td"), P("<b>5 mailboxes/usuario</b>", "td"), P("50/dia/mailbox = 250/dia/usuario", "td"), P("<b>~5.000-7.500 emails/usuario/mes</b>", "td")],
        [P("Apollo <b>Organization</b> ($119/usuario/mes)", "td"), P("15 mailboxes/usuario", "td"), P("50/dia/mailbox = 750/dia/usuario", "td"), P("~15.000-22.500 emails/usuario/mes", "td")],
        [P("Clay <b>Launch</b> ($167/mes)", "td"), P("Ilimitadas por workspace*", "td"), P("~24/dia/mailbox sugerido", "td"), P("Tope ~<b>15.000 emails/mes</b> (limite Actions)", "td")],
        [P("Clay <b>Growth</b> ($446/mes)", "td"), P("Ilimitadas por workspace*", "td"), P("~24/dia/mailbox sugerido", "td"), P("Tope ~<b>40.000 emails/mes</b> (limite Actions)", "td")],
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
        [P("Escenario (mensual)", "th"), P("APOLLO.io", "th"), P("CLAY.com", "th")],
        [
            P("Suscripcion base (1 plan recomendado)", "td_label"),
            P("Pro: $79 / usuario", "td"),
            P("Launch: $167  |  Growth: $446", "td"),
        ],
        [
            P("Costo si suma 1 SDR mas (2 usuarios)", "td_label"),
            P("$158", "td"),
            P("Igual ($167 / $446) - sin tope de usuarios", "td"),
        ],
        [
            P("Costo si suma 3 SDRs mas (4 usuarios)", "td_label"),
            P("$316", "td"),
            P("Igual ($167 / $446) - sin tope de usuarios", "td"),
        ],
        [
            P("Lo que enriqueces / mes (estimado)", "td_label"),
            P("Hasta 7.500 con AI Research", "td"),
            P("~500 (Launch) / ~2.000 (Growth) con workflows profundos", "td"),
        ],
        [
            P("Sequencer de envio incluido?", "td_label"),
            P("<font color='#16A34A'><b>SI</b></font> - multi-paso + A/B testing + dialer US", "td"),
            P("<font color='#16A34A'><b>SI</b></font>, basico (max 4 pasos, solo email). Cada email = 0,1 Action. Para volumen alto conviene sumar sender externo.", "td"),
        ],
        [
            P("Costo realista total para 1 SDR", "td_label"),
            P("<b>~$79-$130 / mes</b>", "td"),
            P("<b>~$167-$520 / mes</b> (sin sender extra)", "td"),
        ],
        [
            P("Costo realista total para 3 SDRs", "td_label"),
            P("<b>~$237-$390 / mes</b>", "td"),
            P("<b>~$167-$520 / mes</b> (mismo precio, sin tope users)", "td"),
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
                "Que herramienta de prospecting elegir para nuestra agencia<br/>"
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
        "<b>Veredicto en una linea:</b><br/>"
        "Para nuestra agencia (presupuesto acotado + necesidad de combinar campanias masivas Y top 200 con personalizacion), "
        "<b>APOLLO Professional ($79/usuario/mes)</b> es la eleccion correcta. "
        "Clay es superior en profundidad de research, pero su modelo de creditos hace que cada lookup, email enviado "
        "y AI snippet pague tarifa. Apollo trae base de datos incluida, sequencer multi-paso y AI Research suficiente "
        "para personalizar a escala, a 1/3 del costo total."
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
        "Hoy usamos Clay para campanias tipo top 200: pasamos una lista de 200 prospects buscados a mano, Clay corre "
        "deep research por cuenta y arma un email personalizado. Tambien enviamos las campanias desde el Sequencer nativo "
        "de Clay. La calidad del output es buena, pero el modelo de creditos hace que cada campania nos consuma "
        "mucho presupuesto, dejandonos sin margen para correr campanias masivas en paralelo. Antes usabamos Apollo, "
        "y la duda es si volver a Apollo (o quedarnos en Clay) sin perder personalizacion ni calidad.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>Conclusion del analisis:</b> ambas plataformas hoy hacen lo mismo a alto nivel (busqueda de contactos, "
        "research IA y envio de emails), pero con filosofias muy distintas. Apollo es una <i>plataforma all-in-one con "
        "base de datos propia incluida</i>, sequencer multi-paso y dialer; el research IA es solido pero menos profundo. "
        "Clay es un <i>motor de enriquecimiento y research premium</i> con un sequencer nativo basico (lanzado en 2025), "
        "donde cada paso (incluido buscar contactos o enviar emails) consume creditos. La eleccion depende de si "
        "valoramos mas la profundidad por cuenta, o la cobertura masiva con costo predecible.",
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
    story.append(Paragraph("3. Casillas de email y volumen de envio", styles["h1"]))
    story.append(Paragraph(
        "Pregunta clave para deliverability y para saber cuantas campanias podemos correr en paralelo: "
        "<b>cuantas casillas (mailboxes) podemos conectar y cuantos emails podemos enviar por dia</b>. "
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
        "<b>Apollo cobra por usuario y te da casillas por usuario.</b> Si tenemos 1 SDR en Pro: 5 casillas con capacidad real de ~250 emails/dia. Si sumamos otro SDR ($79 mas): otras 5 casillas y duplicamos volumen.",
        "<b>Clay cobra por workspace, casillas ilimitadas.</b> Conectas las que quieras, todas comparten el mismo cupo de Actions del plan. En Launch (15.000 Actions/mes) podes enviar ~15.000 emails antes de quedarte sin nada para enrichments.",
        "Apollo recomienda 50 emails/dia/mailbox (mas conservador que el limite de Gmail/Workspace de 500-2.000). Clay recomienda ~24/dia/mailbox para mejor deliverability.",
        "<b>* En Clay las casillas son por workspace</b>: no se duplican si suman SDRs. Eso es bueno (no pagas por usuario) pero malo si necesitas mucho volumen (te limitan los Actions).",
        "Para campanias serias (1.000+ emails/dia) en cualquiera de las dos conviene comprar dominios alternativos y hacer warmup. Esto es independiente de la herramienta.",
    ]
    for b in bullets_mailbox:
        story.append(Paragraph(b, styles["bullet"], bulletText="•"))

    story.append(Spacer(1, 8))
    callout = (
        "<b>Conclusion practica para nuestra agencia:</b><br/>"
        "Con Apollo Professional, 1 usuario = 5 casillas = ~5.000-7.500 emails/mes con buena deliverability. "
        "Con Clay Launch, sin tope de casillas pero con tope de 15.000 emails/mes que tambien comparten con "
        "los enrichments y AI snippets. <b>Clay obliga a elegir entre research o envio</b>; Apollo tiene cupos separados."
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
    story.append(Paragraph("4. Pros y contras de cada herramienta", styles["h1"]))
    story.append(Spacer(1, 4))
    story.append(build_pros_cons_table(styles, page_width))

    # ------------- 5. COSTOS -------------
    story.append(Paragraph("5. Costo real proyectado", styles["h1"]))
    story.append(Paragraph(
        "El precio de lista no es el costo real. Hay que sumar overages, extra users (Apollo), "
        "y herramienta de envio externa (Clay).",
        styles["body"]
    ))
    story.append(Spacer(1, 4))
    story.append(build_cost_table(styles, page_width))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Lectura clave:</b> Apollo es mas barato con 1-2 usuarios; Clay no escala con usuarios pero "
        "obliga a pagar tool de envio aparte. Si tenemos 3 SDRs activos, los costos se igualan, pero "
        "Apollo nos da la base de datos + sequencer incluidos (Clay no).",
        styles["body"]
    ))

    story.append(PageBreak())

    # ------------- 6. MATRIZ DE DECISION -------------
    story.append(Paragraph("6. Matriz de decision: cuando elegir cual", styles["h1"]))
    story.append(Paragraph(
        "Esta tabla resume bajo que prioridad cada herramienta gana. Buscamos el match con nuestras prioridades "
        "como agencia.",
        styles["body"]
    ))
    story.append(Spacer(1, 4))
    story.append(build_decision_matrix(styles, page_width))

    # ------------- 7. RECOMENDACION FINAL -------------
    story.append(Paragraph("7. Recomendacion final para la agencia", styles["h1"]))

    rec_text = (
        "<b>Recomendamos APOLLO Professional</b> ($79/usuario/mes anual) por estas razones:"
    )
    story.append(Paragraph(rec_text, styles["body"]))

    bullets = [
        "<b>Base de datos propia incluida</b> (275M+ contactos): descubrimos prospects sin gastar creditos por cada lookup, como pasa hoy en Clay.",
        "<b>AI Research nativo</b>: 7.500 cuentas/mes con research IA contra paginas web (Perplexity Sonar). Suficientemente profundo para personalizar emails 1:1 en campanias top 200 y tambien correr campanias masivas en paralelo.",
        "<b>Sequencer multi-paso + dialer US integrados</b>: el sequencer de Clay es basico (max 4 pasos por campania, solo email, sin inbox rotation avanzada). Apollo lo supera para volumen serio.",
        "<b>5 casillas de email por usuario</b> en Pro: ~250 emails/dia/usuario con buena deliverability. Cupo separado del de research (en Clay todo sale del mismo bolsillo de Actions).",
        "<b>Costo predecible</b>: el sistema de un solo credito es mas simple que el doble credito de Clay (Data + Actions) y evita los top-ups con 30-50% de premium.",
        "<b>Curva de aprendizaje baja</b>: el equipo arranca en horas, no semanas. Clay requiere mentalidad RevOps que hoy no tenemos dedicada.",
        "<b>Habilita las dos campanias que necesitamos</b>: top 200 con personalizacion + campanias masivas con personalizacion media. Clay solo cubre bien la primera por costo.",
    ]
    for b in bullets:
        story.append(Paragraph(b, styles["bullet"], bulletText="•"))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Cuando volveriamos a evaluar Clay", styles["h2"]))
    story.append(Paragraph(
        "Clay tiene sentido cuando: (a) la agencia tenga un perfil RevOps dedicado, (b) cerremos cuentas mas grandes "
        "donde la calidad del research justifique el costo extra, o (c) Apollo deje de cubrir el match rate o la profundidad "
        "que necesitemos. Hasta entonces, conviene Apollo.",
        styles["body"]
    ))

    # Final callout
    final_text = (
        "<b>Plan de accion sugerido:</b><br/>"
        "1) Probar Apollo Free (50 creditos) para validar calidad del data en nuestro nicho.<br/>"
        "2) Migrar a Apollo Professional anual ($79/usuario/mes) - 20% de descuento vs mensual.<br/>"
        "3) Disenar plantillas de prompt para AI Research (calificacion ICP + frase personalizada).<br/>"
        "4) Pausar Clay al cierre del ciclo actual; rescatar workflows que sirvan como referencia.<br/>"
        "5) Reevaluar a los 90 dias con metricas: open rate, reply rate, costo por reunion."
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

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<i>Fuentes: pricing oficial de apollo.io/pricing y clay.com/pricing (abril 2026); G2 reviews; "
        "analisis publicos de Docket.io, Landbase, Salesmotion, Genesy.ai y Pipeline.help.</i>",
        styles["small"]
    ))

    doc.build(story)
    print(f"PDF generado: {output_path}")


if __name__ == "__main__":
    build_pdf()
