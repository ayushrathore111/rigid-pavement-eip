from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak,HRFlowable
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
from reportlab.lib.units import inch
import math
def create_report(data: dict) -> BytesIO:
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=20, leftMargin=20,
                            topMargin=20, bottomMargin=0)
    
    
    styles = getSampleStyleSheet()
    styleN= styles['Normal']
    styleN.alignment =1
    styles.add(ParagraphStyle(name="SubTitle", fontSize=12, leading=15, alignment=1, textColor=colors.black))
    styles.add(ParagraphStyle(name="Body", fontSize=10, leading=14))
    styles.add(ParagraphStyle(name="Label", fontSize=10, leading=14, textColor=colors.black, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="Value", fontSize=10, leading=14, textColor=colors.black))
    styles.add(ParagraphStyle(name="Calc", fontSize=9, leading=11, textColor=colors.grey))
    styles.add(ParagraphStyle(name="Heading", fontSize=16, leading=20, alignment=1,
                            textColor=colors.darkblue, spaceAfter=15))
    # project inputs
    project = data.get('project', 'N/A')
    tit = data.get('tit', 'N/A')
    doc = data.get('doc', 'N/A')
    des = data.get('des', 'N/A')
    app = data.get('app', 'N/A')
    chk = data.get('chk', 'N/A')
    rev = data.get('rev', 'N/A')
    
    #Design inputs
    vehicels= float(data.get('veh'))
    wheel_load = float(data.get('load'))
    cbr = float(data.get('cbr'))
    k = float(data.get('k'))
    e = float(data.get('e'))
    mu = float(data.get('mu'))
    cs = int(data.get('cs'))
    rup = float(data.get('rup'))
    axle = int(data.get('axle'))
    spacing = int(data.get('spacing'))
    tyreP = float(data.get('tyreP'))
    temp = int(data.get('temp'))
    deltaT = float(data.get('delta'))
    alpha = float(data.get('alpha'))
    life = int(data.get('life'))
    thickness = float(data.get('thickness'))
    wbm = float(data.get('wbm'))
    gsb = float(data.get('gsb'))
    thick= 1000*thickness
    wheel = wheel_load/4
    wheel_load_kg = 9.96*(wheel_load/4)
    p = math.ceil(wheel_load_kg / 10) * 10
    
    
    a2= math.sqrt((0.8521*p*1000)/(axle*tyreP*math.pi)+(spacing/(math.pi))*math.sqrt(p*1000/(0.5227*tyreP*axle)))
    a1= math.pow(p*1000/(tyreP*math.pi),0.5)
    
    a= a2 if axle==2 else a1
    
    
    l = math.pow(1000*e*math.pow(thick,3)/(12*k*(1-math.pow(mu,2))),(1/4))
    
    sig= (4*math.log10(l/a)+0.666*(a/l)-0.034)*803*p/(math.pow(thick,2))
    
    
    status_text = "SAFE" if sig < rup else "UNSAFE"
    
    total_thickness= (wbm+gsb+thickness*1000)
    
    story = []

    # --- Logo and Header ---
    logo = "static/lnt logo.jpeg"
    r1= 'static/radius_img.jpg'
    r2= 'static/radius2.png'
    radius_img = r1 if axle==2 else r2
    relative_stiffness= 'static/relative_stiffness.png'
    stress_img= 'static/stress.png'
    try:
        logo = Image(logo, width=2*inch, height=1.0*inch)  # Adjust as needed
        logo.hAlign = 'LEFT'  # Align logo to left within cell
        
    except:
        logo = Paragraph("<b>L&T Construction</b>", styles["Body"])
    story.append(logo)
    
    title_data = [
        [Paragraph('PROJECT', styleN), Paragraph(project, styleN),
        Paragraph('DOCUMENT NO', styleN),'', Paragraph('DATE', styleN)],
        ['', '', Paragraph(doc, styleN),'', Paragraph('20-04-2004', styleN)],
        ['', '', Paragraph('DESIGNED', styleN), Paragraph('CHECKED', styleN), Paragraph('APPROVED', styleN)],
        ['', '', '', '', ''],
        [Paragraph('TITLE', styleN),
        Paragraph(tit, styleN),
        Paragraph(des, styleN), Paragraph(chk, styleN), Paragraph(app, styleN)]
    ]

    col_widths = [80, 200, 85, 80, 100]  # Adjust proportionally to fit within border
    title_table = Table(title_data, colWidths=col_widths,hAlign='CENTER')

    # ---- Styling ----
    title_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.7, colors.black),

        # Merge PROJECT label vertically (rows 0–3)
        ('SPAN', (0, 0), (0, 3)),

        # Merge PROJECT value vertically (rows 0–3)
        ('SPAN', (1, 0), (1, 3)),

        # Merge DOCUMENT NO label (col 3) with col 2 (only in first row)
        ('SPAN', (2, 0), (3, 0)),
        ('SPAN',(2,1),(3,1)),

        # Merge DESIGNED, CHECKED, APPROVED (cols 2–4) vertically (rows 2–3)
        ('SPAN', (2, 2), (2, 3)),
        ('SPAN', (3, 2), (3, 3)),
        ('SPAN', (4, 2), (4, 3)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),

        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))

    story.append(title_table)
    story.append(Spacer(1, 8))
    
    # --- Title ---
    story.append(Paragraph("<b>DESIGN OF CONCRETE PAVEMENTS</b>", styles["Title"]))
    story.append(Paragraph("(AS PER IRC: SP 62-2014)", styles["SubTitle"]))
    # story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    # story.append(Spacer(1, 10))
    
    
    content = [
        [Paragraph('DESIGN TRAFFIC:', styles['Label'])],
        [Paragraph('No of commercial vehicle per day', styles['Label']), Paragraph('=', styleN),
        Paragraph(f'{vehicels} CVPD', styleN),'', Paragraph('', styleN)],
        [Paragraph('Wheel load for Trailer(6 axle with dual wheel each side)', styles['Label']), Paragraph('=', styleN),
        Paragraph(f'{wheel} Tonne', styleN),'', Paragraph(f'(as per site input: {wheel_load} tonne/axle )', styleN)],
        [Paragraph('Design wheel load ', styles['Label']), Paragraph('=', styleN),
        Paragraph(f'{p} kg', styleN),'', Paragraph('(adopted for safety )', styleN)],
        [Paragraph('California Bearing Ratio(CBR)', styles['Label']), Paragraph('=', styleN),
        Paragraph(str(cbr), styleN),'', Paragraph('(as per soil report )', styleN)],
        [Paragraph('Modulus of Subgrade Reaction(k)', styles['Label']), Paragraph('=', styleN),
        Paragraph(str(k), styleN),'', Paragraph('(as per Table 3.1, IRC:SP 62-2014 )', styleN)],
        [Paragraph('Elastic Modulus of Concrete(E)', styles['Label']), Paragraph('=', styleN),
        Paragraph(str(e), styleN),'', Paragraph('(as per Table 3.8, IRC:SP 62-2014 )', styleN)],
        [Paragraph('Poisson Ratio of the Concrete(μ)', styles['Label']), Paragraph('=', styleN),
        Paragraph(str(mu), styleN),'', Paragraph('(as per Table 3.8, IRC:SP 62-2014)', styleN)],
        [Paragraph('Compressive Strength of Concrete at 28 days(fc)', styles['Label']), Paragraph('=', styleN),
        Paragraph(str(cs), styleN)],
        [Paragraph('Modulus of rupture of Concrete,fcr', styles['Label']), Paragraph('=', styleN),
        Paragraph(str(rup), styleN)],
        [Paragraph('Type of axle(1-single/2-dual)', styles['Label']), Paragraph('=', styleN),
        Paragraph(str(axle), styleN)],
        [Paragraph('Spacing of wheels(Sd)', styles['Label']), Paragraph('=', styleN),
        Paragraph(f'{spacing} mm', styleN),'', Paragraph('9as per Table 3.1, IRC:SP 62-2014 )', styleN)],
        [Paragraph('Tyre pressure(p)', styles['Label']), Paragraph('=', styleN),
        Paragraph(f'{tyreP} Mpa', styleN),'', Paragraph('(as per Table 3.2, IRC:SP 62-2014 )', styleN)],
        [Paragraph('Temperature zone (1 to 6)', styles['Label']), Paragraph('=', styleN),
        Paragraph(str(temp), styleN)],
        [Paragraph('Temperature differential ((ΔT)', styles['Label']), Paragraph('=', styleN),
        Paragraph(f'{deltaT}°C', styleN),'', Paragraph('(as per Table 4.1, IRC:SP 62-2014)', styleN)],
        [Paragraph('Co-efficient of Thermal Expansion', styles['Label']), Paragraph('=', styleN),
        Paragraph(f"{alpha:.5f}", styleN),'', Paragraph('(as per Table 3.9, IRC:SP 62-2014 )', styleN)],
        [Paragraph('Design life of pavement',styles['Label']), Paragraph('=', styleN),
        Paragraph(f'{life} years', styleN),'', Paragraph('(as per Table 3.3, IRC:SP 62-2014 )', styleN)],
        [story.append(Spacer(1,10))],
        [Paragraph('Trail Thickness of pavement ',styles['Label']), Paragraph('=', styleN),
        Paragraph(f'{thickness} m', styleN)],
        [Paragraph('Thickness of WBM layer ',styles['Label']), Paragraph('=', styleN),
        Paragraph(f'{wbm} mm', styleN)],
        [Paragraph('Thickness of GSB layer ',styles['Label']), Paragraph('=', styleN),
        Paragraph(f'{gsb} mm', styleN)],
        [story.append(Spacer(1,10))],
        [Paragraph('Calculation:', styles['Label'])],
        [Paragraph('Design traffic is <50 CVPD:', styles['Label'])],
        [Paragraph('for thickness estimation of pavement, Only wheel load stresses for a load of 50kN on dual wheel need to be considered.', styles['Label'])],
        [Paragraph('Radius of Contact(a) ',styles['Label']), Image(radius_img, width=300, height=50)],
        [Paragraph(' ',styles['Label']), Paragraph('=', styleN),
        Paragraph(f'{a:.2f} mm', styleN),'', Paragraph('(as per data given )', styleN)],
        [Paragraph('Radius of relative stiffness(l) ',styles['Label']), Image(relative_stiffness, width=160, height=50)],
        [Paragraph(' ',styles['Label']), Paragraph('=', styleN),
        Paragraph(f'{l:.4f} m', styleN),'', Paragraph('(as per data given )', styleN)],
        [Paragraph('Wheel stress developed at edge(σ) ',styles['Label']), Image(stress_img, width=250, height=50)],
        [Paragraph('',styles['Label']), Paragraph('=', styleN),
        Paragraph(f'{sig:.4f}Mpa', styleN),'', Paragraph('(as per data given )', styleN)],
        [Paragraph(f'Hence,  Design is ',styles['Label']),'',Paragraph(status_text, styles['Label'])],
        [Paragraph('So,',styles['Label'])],
        [Paragraph('Thickness of Concrete(RCC) Slab ',styles['Label']), Paragraph('=', styleN),
        Paragraph(f'{thick}mm', styleN)],
        [Paragraph(f'(with Min. Reinforcement of 8mm dia, 300mm spacing, M{cs} grade)', styleN)],
        [Paragraph('Thickness of WBM layer ',styles['Label']), Paragraph('=', styleN),
        Paragraph(f'{wbm}mm', styleN)],
        [Paragraph('Thickness of GSB layer ',styles['Label']), Paragraph('=', styleN),
        Paragraph(f'{gsb}mm', styleN)],
        [story.append(Spacer(1,10))],
        [Paragraph('Total Thickness of RCC pavement ',styles['Label']), Paragraph('=', styleN),
        Paragraph(f'{total_thickness}mm', styles['Label'])],
    ]

    # Create table with 4 columns
    table = Table(content, colWidths=[200, 30, 70, 110])

    # Table styling (no visible borders)
    table.setStyle(TableStyle([
        ('SPAN', (0, 24), (-1, 24)),
        ('SPAN', (1, 25), (3, 25)),
        ('SPAN', (1, 27), (3, 27)),
        ('SPAN', (1, 29), (3, 29)),
        ('SPAN', (0, 34), (3, 34)),
        
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),

        # Hide all borders
        ('BOX', (0, 0), (-1, -1), 0, colors.white),
        ('INNERGRID', (0, 0), (-1, -1), 0, colors.white),
    ]))
    
    story.append(table)
    
    
    

    def draw_page_border_and_number(canvas, doc):
            """Draws a neat border and page number"""
            width, height = A4

        # Outer border (adjust margins)
            margin = 25
            canvas.setLineWidth(1)
            canvas.rect(margin, margin, width - 2*margin, height - 2*margin)

        # Page number at bottom center
            page_num = f"Page {doc.page}"
            canvas.setFont("Helvetica", 9)
            canvas.drawCentredString(width / 2.0, 15, page_num)

    pdf.build(story, onFirstPage=draw_page_border_and_number,
            onLaterPages=draw_page_border_and_number)
    
    # pdf.build(story)
    buffer.seek(0)
    return buffer