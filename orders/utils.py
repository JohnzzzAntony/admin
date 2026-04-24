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
    Generates a professional, premium PDF invoice for a CustomerOrder.
    """
    buffer = io.BytesIO()
    # Adjust margins for a more spacious, premium feel
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        rightMargin=30, 
        leftMargin=30, 
        topMargin=30, 
        bottomMargin=30
    )
    elements = []
    
    styles = getSampleStyleSheet()
    
    # --- Custom Design Tokens ---
    PRIMARY_BLUE = colors.HexColor("#114084")
    TEXT_DARK = colors.HexColor("#1e293b")
    TEXT_MUTED = colors.HexColor("#64748b")
    BORDER_LIGHT = colors.HexColor("#e2e8f0")
    BG_LIGHT = colors.HexColor("#f8fafc")

    # --- Custom Styles ---
    brand_style = ParagraphStyle(
        'Brand', 
        parent=styles['Heading1'], 
        textColor=PRIMARY_BLUE, 
        fontSize=26, 
        fontName='Helvetica-Bold',
        spaceAfter=2
    )
    invoice_title_style = ParagraphStyle(
        'InvoiceTitle', 
        parent=styles['Normal'], 
        fontSize=28, 
        textColor=PRIMARY_BLUE, 
        fontName='Helvetica-Bold', 
        alignment=2 # Right aligned
    )
    meta_label_style = ParagraphStyle(
        'MetaLabel', 
        parent=styles['Normal'], 
        fontSize=9, 
        textColor=TEXT_MUTED, 
        fontName='Helvetica-Bold',
        alignment=2
    )
    meta_value_style = ParagraphStyle(
        'MetaValue', 
        parent=styles['Normal'], 
        fontSize=10, 
        textColor=TEXT_DARK, 
        alignment=2,
        spaceAfter=2
    )
    header_contact_style = ParagraphStyle(
        'HeaderContact', 
        parent=styles['Normal'], 
        fontSize=9, 
        textColor=TEXT_MUTED, 
        leading=12
    )
    section_label_style = ParagraphStyle(
        'SectionLabel', 
        parent=styles['Normal'], 
        fontSize=10, 
        fontName='Helvetica-Bold', 
        textColor=PRIMARY_BLUE, 
        spaceAfter=6,
        textTransform='uppercase'
    )
    address_style = ParagraphStyle(
        'Address', 
        parent=styles['Normal'], 
        fontSize=9, 
        textColor=TEXT_DARK, 
        leading=13
    )
    table_header_style = ParagraphStyle(
        'TableHeader', 
        parent=styles['Normal'], 
        fontSize=9, 
        fontName='Helvetica-Bold', 
        textColor=colors.white,
        alignment=1 # Center
    )
    table_cell_style = ParagraphStyle(
        'TableCell', 
        parent=styles['Normal'], 
        fontSize=9, 
        textColor=TEXT_DARK, 
        leading=12
    )
    table_cell_right_style = ParagraphStyle(
        'TableCellRight', 
        parent=table_cell_style, 
        alignment=2
    )
    breakdown_label_style = ParagraphStyle(
        'BreakdownLabel', 
        parent=styles['Normal'], 
        fontSize=10, 
        textColor=TEXT_MUTED, 
        alignment=2,
        leading=16
    )
    breakdown_value_style = ParagraphStyle(
        'BreakdownValue', 
        parent=styles['Normal'], 
        fontSize=10, 
        textColor=TEXT_DARK, 
        fontName='Helvetica-Bold',
        alignment=2,
        leading=16
    )
    total_label_style = ParagraphStyle(
        'TotalLabel', 
        parent=styles['Normal'], 
        fontSize=14, 
        fontName='Helvetica-Bold', 
        textColor=PRIMARY_BLUE,
        alignment=2
    )
    total_amount_style = ParagraphStyle(
        'TotalAmount', 
        parent=styles['Normal'], 
        fontSize=16, 
        fontName='Helvetica-Bold', 
        textColor=PRIMARY_BLUE,
        alignment=2
    )

    # 1. Header (Logo/Brand & Meta Info)
    from core.models import SiteSettings
    site_settings = SiteSettings.objects.first()
    brand_name = site_settings.company_name if site_settings and site_settings.company_name else "JKR International"
    
    # Attempt to add Logo
    logo_img = None
    if site_settings and site_settings.logo:
        try:
            import os
            logo_path = os.path.join(settings.MEDIA_ROOT, site_settings.logo.name)
            if os.path.exists(logo_path):
                logo_img = Image(logo_path, width=1.8*inch, height=0.6*inch)
                logo_img.hAlign = 'LEFT'
        except Exception:
            logo_img = None

    header_left = [logo_img] if logo_img else [Paragraph(brand_name, brand_style)]
    
    # Company Contact Block
    if site_settings:
        addr_parts = []
        if site_settings.dubai_address:
            addr_parts.append(site_settings.dubai_address.replace('\n', '<br/>'))
        if site_settings.phone:
            addr_parts.append(f"Phone: {site_settings.phone}")
        if site_settings.email:
            addr_parts.append(f"Email: {site_settings.email}")
        header_left.append(Spacer(1, 8))
        header_left.append(Paragraph("<br/>".join(addr_parts), header_contact_style))

    header_right = [
        Paragraph("TAX INVOICE", invoice_title_style),
        Spacer(1, 10),
        Paragraph("Invoice Number", meta_label_style),
        Paragraph(f"INV-{order.pk:05d}", meta_value_style),
        Paragraph("Order Date", meta_label_style),
        Paragraph(order.created_at.strftime('%d %b %Y'), meta_value_style),
        Paragraph("Payment Status", meta_label_style),
        Paragraph(order.get_payment_status_display().upper(), meta_value_style),
    ]

    header_data = [[header_left, header_right]]
    header_table = Table(header_data, colWidths=[4*inch, 3.25*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 30))

    # 2. Billing & Shipping Info
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

    addr_data = [
        [Paragraph("Bill To", section_label_style), Paragraph("Ship To", section_label_style)],
        [Paragraph(bill_to, address_style), Paragraph(ship_to, address_style)]
    ]
    
    addr_table = Table(addr_data, colWidths=[3.62*inch, 3.62*inch])
    addr_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,0), 4),
        ('TOPPADDING', (0,1), (-1,1), 4),
    ]))
    elements.append(addr_table)
    
    # Customer TRN if exists
    if order.trn:
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"<b>Customer TRN:</b> {order.trn}", address_style))

    elements.append(Spacer(1, 30))

    # 3. Order Items Table
    item_data = [[
        Paragraph('#', table_header_style),
        Paragraph('Description', table_header_style),
        Paragraph('Qty', table_header_style),
        Paragraph('Unit Price', table_header_style),
        Paragraph('Amount', table_header_style)
    ]]
    
    for i, item in enumerate(order.items.all(), 1):
        item_data.append([
            Paragraph(str(i), table_cell_style),
            Paragraph(f"<b>{escape(item.product_name)}</b>", table_cell_style),
            Paragraph(str(item.quantity), table_cell_style),
            Paragraph(f"{item.unit_price:,.2f}", table_cell_right_style),
            Paragraph(f"{item.total_price:,.2f}", table_cell_right_style)
        ])
    
    # Table colWidths: Total ~ 7.25 inch
    items_table = Table(item_data, colWidths=[0.4*inch, 4.05*inch, 0.6*inch, 1.1*inch, 1.1*inch])
    
    # Style the table
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LINEBELOW', (0,0), (-1,0), 1.5, PRIMARY_BLUE),
        ('LINEBELOW', (0,1), (-1,-2), 0.5, BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [BG_LIGHT, colors.white]), # Subtle striping
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 20))

    # 4. Totals Breakdown (Right-aligned)
    subtotal = sum(i.total_price for i in order.items.all())
    
    breakdown_data = [
        [Paragraph("Subtotal", breakdown_label_style), Paragraph(f"AED {subtotal:,.2f}", breakdown_value_style)],
    ]
    
    if order.discount_amount > 0:
        coupon_text = f" ({order.coupon_code})" if order.coupon_code else ""
        breakdown_data.append([
            Paragraph(f"Discount{coupon_text}", breakdown_label_style), 
            Paragraph(f"- AED {order.discount_amount:,.2f}", breakdown_value_style)
        ])
        
    breakdown_data.append([
        Paragraph("Shipping Charge", breakdown_label_style), 
        Paragraph(f"AED {order.shipping_amount:,.2f}", breakdown_value_style)
    ])
    
    breakdown_data.append([
        Paragraph("VAT (5%)", breakdown_label_style), 
        Paragraph(f"AED {order.tax_amount:,.2f}", breakdown_value_style)
    ])
    
    breakdown_data.append([
        Paragraph("Total Amount", total_label_style), 
        Paragraph(f"AED {order.total_amount:,.2f}", total_amount_style)
    ])

    breakdown_table = Table(breakdown_data, colWidths=[5.15*inch, 2.1*inch])
    breakdown_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,-1), (-1,-1), 12), # Extra padding for Grand Total row
    ]))
    elements.append(breakdown_table)
    
    # 5. Payment & Footer Info
    elements.append(Spacer(1, 40))
    elements.append(Paragraph("Payment Information", section_label_style))
    payment_info = f"<b>Method:</b> {order.get_payment_method_display()}<br/><b>Transaction Ref:</b> {order.stripe_payment_id or 'N/A'}"
    elements.append(Paragraph(payment_info, address_style))
    
    elements.append(Spacer(1, 30))
    # Horizontal line
    elements.append(Table([['']], colWidths=[7.25*inch], style=[('LINEABOVE', (0,0), (-1,-1), 1, PRIMARY_BLUE)]))
    elements.append(Spacer(1, 10))
    
    footer_text = "Thank you for choosing JKR International. We appreciate your business!<br/>" \
                  "<font size='8' color='#64748b'>Terms & Conditions: Goods once sold are not returnable. This is a computer generated invoice.</font>"
    elements.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=styles['Normal'], alignment=1, fontSize=10, leading=14)))

    doc.build(elements)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{order.pk:05d}.pdf"'
    return response

