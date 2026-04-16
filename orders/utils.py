from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from django.conf import settings
from django.utils import timezone
import io

def create_invoice_pdf(order):
    """
    Generates a professional PDF invoice for a CustomerOrder.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elements = []
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    brand_style = ParagraphStyle('Brand', parent=styles['Heading1'], textColor=colors.HexColor("#114084"), fontSize=24, spaceAfter=10)
    header_style = ParagraphStyle('Header', parent=styles['Normal'], fontSize=10, leading=14)
    table_header_style = ParagraphStyle('TableHeader', parent=styles['Normal'], fontSize=10, textColor=colors.whitesmoke, fontName='Helvetica-Bold')

    # 1. Header (Brand & Invoice Info)
    from core.models import SiteSettings
    site_settings = SiteSettings.objects.first()
    
    brand_name = site_settings.company_name if site_settings and site_settings.company_name else "Demo International"
    
    # Company Contact Info for Header
    company_addr = ""
    if site_settings:
        addr_parts = []
        if site_settings.dubai_address:
            addr_parts.append(site_settings.dubai_address.replace('\n', '<br/>'))
        if site_settings.phone:
            addr_parts.append(f"Phone: {site_settings.phone}")
        if site_settings.email:
            addr_parts.append(f"Email: {site_settings.email}")
        company_addr = "<br/>".join(addr_parts)

    header_data = [
        [
            Paragraph(f"{brand_name}<br/><font size='8' color='#666666'>{company_addr}</font>", brand_style),
            Paragraph(f"<b>INVOICE</b><br/>Order #Demo-{order.pk:05d}<br/>Date: {order.created_at.strftime('%Y-%m-%d')}", header_style)
        ]
    ]
    header_table = Table(header_data, colWidths=[4*inch, 2.5*inch])
    header_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('ALIGN', (1,0), (1,0), 'RIGHT')]))
    elements.append(header_table)
    elements.append(Spacer(1, 20))

    # 2. Billing & Shipping Info
    addr_data = [
        [Paragraph("<b>SHIPPING ADDRESS</b>", header_style), Paragraph("<b>BILLING ADDRESS</b>", header_style)]
    ]
    
    from django.utils.html import escape
    
    def format_address(obj, prefix=""):
        fname = getattr(obj, f"{prefix}first_name")
        lname = getattr(obj, f"{prefix}last_name")
        street = getattr(obj, f"{prefix}street")
        street2 = getattr(obj, f"{prefix}street2")
        emirates = getattr(obj, f"{prefix}emirates")
        city = getattr(obj, f"{prefix}city")
        country = getattr(obj, f"{prefix}country")
        phone = getattr(obj, f"{prefix}phone")
        
        lines = [f"<b>{escape(fname)} {escape(lname)}</b>", escape(street)]
        if street2: lines.append(escape(street2))
        lines.append(f"{escape(emirates or city)}, {escape(country)}")
        lines.append(f"Phone: {escape(phone)}")
        return "<br/>".join(lines)

    ship_to = format_address(order)
    
    if order.billing_address_same_as_shipping:
        bill_to = ship_to
    else:
        bill_to = format_address(order, prefix="billing_")
    
    addr_data.append([Paragraph(ship_to, header_style), Paragraph(bill_to, header_style)])
    
    addr_table = Table(addr_data, colWidths=[3.25*inch, 3.25*inch])
    addr_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,0), 5)]))
    elements.append(addr_table)
    elements.append(Spacer(1, 10))

    # 3. TRN (if exists)
    if order.trn:
        elements.append(Paragraph(f"<b>Customer TRN:</b> {order.trn}", header_style))
        elements.append(Spacer(1, 15))

    # 4. Items Table
    item_data = [['Product', 'Qty', 'Unit Price', 'Total']]
    from django.utils.html import escape
    for item in order.items.all():
        # Escape product name for XML compatibility in Paragraphs
        p_name = Paragraph(escape(item.product_name), header_style)
        item_data.append([
            p_name,
            str(item.quantity),
            f"{item.unit_price:.2f} {settings.CURRENCY}",
            f"{item.total_price:.2f} {settings.CURRENCY}"
        ])
    
    items_table = Table(item_data, colWidths=[3.5*inch, 0.7*inch, 1.15*inch, 1.15*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#114084")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('VALIGN', (0,1), (-1,-1), 'MIDDLE'), # Vertical center for multi-line support
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 10),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 10))

    # 5. Totals
    subtotal = sum(i.total_price for i in order.items.all())
    totals_data = [
        ['', 'Subtotal:', f"{subtotal:.2f} {settings.CURRENCY}"],
        ['', 'Shipping:', f"{(order.shipping_amount or 0):.2f} {settings.CURRENCY}"],
        ['', 'VAT (Tax):', f"{(order.tax_amount or 0):.2f} {settings.CURRENCY}"],
        ['', 'Grand Total:', f"{(order.total_amount or 0):.2f} {settings.CURRENCY}"]
    ]
    totals_table = Table(totals_data, colWidths=[4*inch, 1.25*inch, 1.25*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('ALIGN', (2,0), (2,-1), 'RIGHT'),
        ('FONTNAME', (1,3), (2,3), 'Helvetica-Bold'),
        ('LINEABOVE', (1,3), (2,3), 1, colors.black),
    ]))
    elements.append(totals_table)
    
    # Bottom note
    elements.append(Spacer(1, 40))
    elements.append(Paragraph(f"Payment Method: {order.get_payment_method_display()}", header_style))
    elements.append(Paragraph(f"Order Status: {order.get_status_display()}", header_style))

    doc.build(elements)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_Demo_{order.pk:05d}.pdf"'
    return response
