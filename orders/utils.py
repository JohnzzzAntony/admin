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
    Generates a professional PDF invoice for a CustomerOrder restructured like the requested image.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elements = []
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    brand_style = ParagraphStyle('Brand', parent=styles['Heading1'], textColor=colors.HexColor("#114084"), fontSize=24, spaceAfter=8)
    header_style = ParagraphStyle('Header', parent=styles['Normal'], fontSize=9, leading=12)
    section_title_style = ParagraphStyle('SectionTitle', parent=styles['Heading2'], fontSize=16, fontName='Helvetica-Bold', spaceBefore=20, spaceAfter=12)
    table_header_style = ParagraphStyle('TableHeader', parent=styles['Normal'], fontSize=9, fontName='Helvetica-Bold', leading=12)
    table_cell_style = ParagraphStyle('TableCell', parent=styles['Normal'], fontSize=9, leading=12)
    breakdown_style = ParagraphStyle('Breakdown', parent=styles['Normal'], fontSize=11, leading=18)
    total_label_style = ParagraphStyle('TotalLabel', parent=styles['Heading2'], fontSize=14, fontName='Helvetica-Bold', spaceBefore=20)
    total_amount_style = ParagraphStyle('TotalAmount', parent=styles['Normal'], fontSize=20, fontName='Helvetica-Bold', spaceBefore=10)

    # 1. Header (Brand & Invoice Info)
    from core.models import SiteSettings
    site_settings = SiteSettings.objects.first()
    brand_name = site_settings.company_name if site_settings and site_settings.company_name else "Demo International"
    
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
    elements.append(Spacer(1, 15))

    # 2. Billing & Shipping Info
    addr_data = [
        [Paragraph("<b>SHIPPING ADDRESS</b>", header_style), Paragraph("<b>BILLING ADDRESS</b>", header_style)]
    ]
    
    from django.utils.html import escape
    def format_address(obj, prefix=""):
        fname = getattr(obj, f"{prefix}first_name")
        lname = getattr(obj, f"{prefix}last_name")
        street = getattr(obj, f"{prefix}street")
        street2 = getattr(obj, f"{prefix}street2") or ""
        emir = getattr(obj, f"{prefix}emirates") or ""
        city = getattr(obj, f"{prefix}city")
        country = getattr(obj, f"{prefix}country")
        phone = getattr(obj, f"{prefix}phone")
        lines = [f"<b>{escape(fname)} {escape(lname)}</b>", escape(street)]
        if street2: lines.append(escape(street2))
        lines.append(f"{escape(emir or city)}, {escape(country)}")
        lines.append(f"Phone: {escape(phone)}")
        return "<br/>".join(lines)

    ship_to = format_address(order)
    bill_to = ship_to if order.billing_address_same_as_shipping else format_address(order, prefix="billing_")
    addr_data.append([Paragraph(ship_to, header_style), Paragraph(bill_to, header_style)])
    
    addr_table = Table(addr_data, colWidths=[3.25*inch, 3.25*inch])
    addr_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,0), 5)]))
    elements.append(addr_table)
    
    if order.trn:
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"<b>Customer TRN:</b> {order.trn}", header_style))

    # 3. Order Summary Table
    elements.append(Paragraph("Order Summary", section_title_style))
    
    item_data = [[
        Paragraph('Product', table_header_style), 
        Paragraph('Qty', table_header_style), 
        Paragraph('Regular Price', table_header_style), 
        Paragraph('Offer Price', table_header_style), 
        Paragraph('Final Price', table_header_style), 
        Paragraph('Total', table_header_style)
    ]]
    
    for item in order.items.all():
        p_name = Paragraph(escape(item.product_name), table_cell_style)
        item_data.append([
            p_name,
            str(item.quantity),
            f"AED {item.regular_price:,.2f}",
            f"AED {(item.offer_price or item.unit_price):,.2f}",
            f"AED {item.unit_price:,.2f}",
            f"AED {item.total_price:,.2f}"
        ])
    
    summary_table = Table(item_data, colWidths=[2*inch, 0.4*inch, 1.1*inch, 1.1*inch, 1*inch, 1*inch])
    summary_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,1), (-1,-2), 0.5, colors.lightgrey),
        ('LINEBELOW', (0,-1), (-1,-1), 1, colors.black),
    ]))
    elements.append(summary_table)

    # 4. Pricing Breakdown
    elements.append(Paragraph("Pricing Breakdown", section_title_style))
    
    subtotal = sum(i.total_price for i in order.items.all())
    adjusted_subtotal = subtotal - order.discount_amount
    
    breakdown_items = [
        f"<li><b>Subtotal:</b> AED {subtotal:,.2f}</li>"
    ]
    if order.discount_amount > 0:
        coupon_text = f" ({order.coupon_code})" if order.coupon_code else ""
        breakdown_items.append(f"<li><b>Coupon Discount{coupon_text}:</b> - AED {order.discount_amount:,.2f}</li>")
        breakdown_items.append(f"<li><b>Adjusted Subtotal:</b> AED {adjusted_subtotal:,.2f}</li>")
    
    breakdown_items.append(f"<li><b>Shipping Cost:</b> AED {order.shipping_amount:,.2f}</li>")
    breakdown_items.append(f"<li><b>VAT (5%):</b> AED {order.tax_amount:,.2f}</li>")
    
    breakdown_text = f"<ul bulletColor='#114084' spaceBefore=10>{''.join(breakdown_items)}</ul>"
    elements.append(Paragraph(breakdown_text, breakdown_style))

    # 5. Grand Total
    elements.append(Paragraph("Grand Total", total_label_style))
    elements.append(Paragraph(f"AED {order.total_amount:,.2f}", total_amount_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<hr/>", header_style))

    # 6. Payment Details
    elements.append(Paragraph("Payment Details", section_title_style))
    payment_details = [
        f"<li><b>Payment Method:</b> {order.get_payment_method_display()}</li>",
        f"<li><b>Order Status:</b> {order.get_status_display()}</li>"
    ]
    elements.append(Paragraph(f"<ul>{''.join(payment_details)}</ul>", breakdown_style))

    doc.build(elements)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_Demo_{order.pk:05d}.pdf"'
    return response
