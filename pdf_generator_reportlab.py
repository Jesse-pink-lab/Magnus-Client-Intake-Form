#!/usr/bin/env python3
"""
PDF Generator for Magnus Client Intake Form
Uses ReportLab to create a professional PDF form
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

def generate_pdf_from_data(form_data, output_path):
    """Generate a PDF from the form data"""
    try:
        # Create the PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = styles["Heading1"]
        heading_style = styles["Heading2"]
        normal_style = styles["Normal"]
        
        # Create custom styles
        label_style = ParagraphStyle(
            'Label',
            parent=styles["Normal"],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=12
        )
        
        value_style = ParagraphStyle(
            'Value',
            parent=styles["Normal"],
            fontName='Helvetica',
            fontSize=10,
            leading=12,
            leftIndent=20
        )
        
        # Build the document content
        content = []
        
        # Title
        content.append(Paragraph("Magnus Client Intake Form", title_style))
        content.append(Spacer(1, 0.25*inch))
        
        # Personal Information
        content.append(Paragraph("Personal Information", heading_style))
        content.append(Spacer(1, 0.1*inch))
        
        personal_info = [
            ("Full Name", form_data.get("full_name", "")),
            ("Date of Birth", form_data.get("dob", "")),
            ("Social Security Number", form_data.get("ssn", "")),
            ("Citizenship", form_data.get("citizenship", "")),
            ("Marital Status", form_data.get("marital_status", ""))
        ]
        
        for label, value in personal_info:
            content.append(Paragraph(f"<b>{label}:</b> {value}", normal_style))
            content.append(Spacer(1, 0.05*inch))
        
        content.append(Spacer(1, 0.1*inch))
        
        # Contact Information
        content.append(Paragraph("Contact Information", heading_style))
        content.append(Spacer(1, 0.1*inch))
        
        # Format address with line breaks
        res_address = form_data.get("residential_address", "").replace("\n", "<br/>")
        content.append(Paragraph("<b>Residential Address:</b>", normal_style))
        content.append(Paragraph(res_address, value_style))
        content.append(Spacer(1, 0.05*inch))
        
        if form_data.get("mailing_address_different", False):
            mail_address = form_data.get("mailing_address", "").replace("\n", "<br/>")
            content.append(Paragraph("<b>Mailing Address:</b>", normal_style))
            content.append(Paragraph(mail_address, value_style))
            content.append(Spacer(1, 0.05*inch))
        
        contact_info = [
            ("Home Phone", form_data.get("home_phone", "")),
            ("Work Phone", form_data.get("work_phone", "")),
            ("Mobile Phone", form_data.get("mobile_phone", "")),
            ("Email", form_data.get("email", ""))
        ]
        
        for label, value in contact_info:
            content.append(Paragraph(f"<b>{label}:</b> {value}", normal_style))
            content.append(Spacer(1, 0.05*inch))
        
        content.append(Spacer(1, 0.1*inch))
        
        # Employment Information
        content.append(Paragraph("Employment Information", heading_style))
        content.append(Spacer(1, 0.1*inch))
        
        employment_info = [
            ("Employment Status", form_data.get("employment_status", "")),
            ("Employer Name", form_data.get("employer_name", "")),
            ("Occupation/Title", form_data.get("occupation", "")),
            ("Years Employed", str(form_data.get("years_employed", "")))
        ]
        
        for label, value in employment_info:
            content.append(Paragraph(f"<b>{label}:</b> {value}", normal_style))
            content.append(Spacer(1, 0.05*inch))
        
        # Format employer address with line breaks
        emp_address = form_data.get("employer_address", "").replace("\n", "<br/>")
        content.append(Paragraph("<b>Employer Address:</b>", normal_style))
        content.append(Paragraph(emp_address, value_style))
        
        content.append(Spacer(1, 0.1*inch))
        
        # Spouse Information (if applicable)
        if form_data.get("spouse_applicable", False):
            content.append(Paragraph("Spouse/Partner Information", heading_style))
            content.append(Spacer(1, 0.1*inch))
            
            spouse_info = [
                ("Spouse Full Name", form_data.get("spouse_full_name", "")),
                ("Spouse Date of Birth", form_data.get("spouse_dob", "")),
                ("Spouse SSN", form_data.get("spouse_ssn", "")),
                ("Spouse Employment Status", form_data.get("spouse_employment_status", "")),
                ("Spouse Employer Name", form_data.get("spouse_employer_name", "")),
                ("Spouse Occupation/Title", form_data.get("spouse_occupation", ""))
            ]
            
            for label, value in spouse_info:
                content.append(Paragraph(f"<b>{label}:</b> {value}", normal_style))
                content.append(Spacer(1, 0.05*inch))
            
            content.append(Spacer(1, 0.1*inch))
        
        # Dependents Information
        if isinstance(form_data.get("dependents"), list) and form_data["dependents"]:
            content.append(Paragraph("Dependents Information", heading_style))
            content.append(Spacer(1, 0.1*inch))
            
            # Create a table for dependents
            dependents_data = [["Name", "Date of Birth", "Relationship"]]
            for dep in form_data["dependents"]:
                dependents_data.append([
                    dep.get("name", ""),
                    dep.get("dob", ""),
                    dep.get("relationship", "")
                ])
            
            t = Table(dependents_data, colWidths=[2*inch, 1.5*inch, 2*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            content.append(t)
            content.append(Spacer(1, 0.2*inch))
        
        # Beneficiaries Information
        if isinstance(form_data.get("beneficiaries"), list) and form_data["beneficiaries"]:
            content.append(Paragraph("Beneficiaries Information", heading_style))
            content.append(Spacer(1, 0.1*inch))
            
            # Create a table for beneficiaries
            beneficiaries_data = [["Name", "Date of Birth", "Relationship", "Percentage"]]
            for ben in form_data["beneficiaries"]:
                beneficiaries_data.append([
                    ben.get("name", ""),
                    ben.get("dob", ""),
                    ben.get("relationship", ""),
                    f"{ben.get('percentage', '')}".replace('%', '') + "%"

                ])
            
            t = Table(beneficiaries_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            content.append(t)
            content.append(Spacer(1, 0.2*inch))
        
        # Assets & Investment Experience
        content.append(Paragraph("Assets & Investment Experience", heading_style))
        content.append(Spacer(1, 0.1*inch))
        
        assets_info = [
            ("Net Worth (excluding primary home)", form_data.get("net_worth", "")),
            ("Liquid Net Worth (cash + securities)", form_data.get("liquid_net_worth", "")),
            ("Assets Held Away (Brokerage, etc.)", form_data.get("assets_held_away", ""))
        ]
        
        for label, value in assets_info:
            content.append(Paragraph(f"<b>{label}:</b> {value}", normal_style))
            content.append(Spacer(1, 0.05*inch))
        
        # Asset Breakdown (if included)
        if form_data.get("include_breakdown", False) and "asset_breakdown" in form_data:
            content.append(Paragraph("<b>Asset Breakdown:</b>", normal_style))
            content.append(Spacer(1, 0.05*inch))
            
            breakdown_data = [["Asset Type", "Percentage"]]
            for asset, percentage in form_data["asset_breakdown"].items():
                breakdown_data.append([asset, f"{percentage}%"])
            
            t = Table(breakdown_data, colWidths=[3*inch, 1.5*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            content.append(t)
            content.append(Spacer(1, 0.1*inch))
        
        # Asset Type Experience
        if isinstance(form_data.get("asset_experience"), dict):
            content.append(Paragraph("<b>Asset Type Experience:</b>", normal_style))
            content.append(Spacer(1, 0.05*inch))
            
            experience_data = [["Asset Type", "Year Started", "Experience Level"]]
            for asset, exp in form_data["asset_experience"].items():
                experience_data.append([
                    asset,
                    exp.get("year_started", ""),
                    exp.get("level", "")
                ])
            
            t = Table(experience_data, colWidths=[2*inch, 1.5*inch, 2*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            content.append(t)
            content.append(Spacer(1, 0.1*inch))
        
        # Outside Broker Firm (if applicable)
        if form_data.get("has_outside_broker", False):
            content.append(Paragraph("<b>Outside Broker Firm Information:</b>", normal_style))
            content.append(Spacer(1, 0.05*inch))
            
            outside_broker_info = [
                ("Firm Name", form_data.get("outside_firm_name", "")),
                ("Liquid Amount", form_data.get("outside_liquid_amount", ""))
            ]
            
            for label, value in outside_broker_info:
                content.append(Paragraph(f"<b>{label}:</b> {value}", normal_style))
                content.append(Spacer(1, 0.05*inch))
        
        # Financial Information Section (Moved from end of file)
        content.append(Spacer(1, 0.2*inch))
        content.append(Paragraph("Financial Information", heading_style))
        content.append(Spacer(1, 0.1*inch))
        
        financial_info = [
            ("Annual Income", form_data.get("annual_income", "")),
            ("Education Status", form_data.get("education_status", "")),
            ("Tax Bracket", form_data.get("tax_bracket", "")),
            ("Risk Tolerance", form_data.get("risk_tolerance", "")),
            ("Investment Objectives", form_data.get("investment_objectives", "")),
            ("Net Worth", form_data.get("net_worth", "")),
            ("Liquid Net Worth", form_data.get("liquid_net_worth", ""))
        ]
        
        for label, value in financial_info:
            if value:  # Only include if value exists
                content.append(Paragraph(f"<b>{label}:</b> {value}", normal_style))
                content.append(Spacer(1, 0.05*inch))

        # Retirement Information (if applicable)
        if form_data.get("employment_status") == "Retired":
            content.append(Paragraph("Retirement Information", heading_style))
            content.append(Spacer(1, 0.1*inch))
            retirement_info = [
                ("Former Employer", form_data.get("former_employer", "")),
                ("Source of Income", form_data.get("income_source", ""))
            ]
            for label, value in retirement_info:
                content.append(Paragraph(f"<b>{label}:</b> {value}", normal_style))
                content.append(Spacer(1, 0.05*inch))

        # Trusted Contact Person
        if form_data.get("trusted_full_name"):
            content.append(Paragraph("Trusted Contact Person", heading_style))
            content.append(Spacer(1, 0.1*inch))
            trusted_contact_info = [
                ("Full Name", form_data.get("trusted_full_name", "")),
                ("Relationship", form_data.get("trusted_relationship", "")),
                ("Phone", form_data.get("trusted_phone", "")),
                ("Email", form_data.get("trusted_email", ""))
            ]
            for label, value in trusted_contact_info:
                content.append(Paragraph(f"<b>{label}:</b> {value}", normal_style))
                content.append(Spacer(1, 0.05*inch))

        # Regulatory Consent
        content.append(Paragraph("Regulatory Consent", heading_style))
        content.append(Spacer(1, 0.1*inch))
        electronic_consent = "Yes" if form_data.get("electronic_regulatory_yes") else "No"
        content.append(Paragraph(f"<b>Electronic Delivery Consent:</b> {electronic_consent}", normal_style))
        content.append(Spacer(1, 0.05*inch))

        # Build the PDF
        doc.build(content)
        return True
    except Exception as e:
        print(f"Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

# Test function
if __name__ == "__main__":
    # Sample data for testing
    test_data = {
        "full_name": "John Doe",
        "dob": "01/15/1980",
        "ssn": "123-45-6789",
        "citizenship": "US",
        "marital_status": "Married",
        "residential_address": "123 Main St\nAnytown, CA 12345",
        "mailing_address_different": True,
        "mailing_address": "PO Box 456\nAnytown, CA 12345",
        "home_phone": "(555) 123-4567",
        "work_phone": "(555) 987-6543",
        "mobile_phone": "(555) 555-5555",
        "email": "john.doe@example.com",
        "employment_status": "Employed",
        "employer_name": "ACME Corporation",
        "occupation": "Software Engineer",
        "employer_address": "456 Business Ave\nAnytown, CA 12345",
        "years_employed": 5,
        "spouse_applicable": True,
        "spouse_full_name": "Jane Doe",
        "spouse_dob": "03/20/1982",
        "spouse_ssn": "987-65-4321",
        "spouse_employment_status": "Employed",
        "spouse_employer_name": "XYZ Company",
        "spouse_occupation": "Marketing Manager",
        "dependents": [
            {"name": "Jimmy Doe", "dob": "05/10/2010", "relationship": "Son"},
            {"name": "Sally Doe", "dob": "07/15/2012", "relationship": "Daughter"}
        ],
        "beneficiaries": [
            {"name": "Jane Doe", "dob": "03/20/1982", "relationship": "Spouse", "percentage": 50},
            {"name": "Jimmy Doe", "dob": "05/10/2010", "relationship": "Son", "percentage": 25},
            {"name": "Sally Doe", "dob": "07/15/2012", "relationship": "Daughter", "percentage": 25}
        ],
        "net_worth": "800000",
        "liquid_net_worth": "300000",
        "assets_held_away": "200000",
        "include_breakdown": True,
        "asset_breakdown": {
            "Stocks": 30,
            "Bonds": 20,
            "Mutual Funds": 15,
            "ETFs": 15,
            "Options": 5,
            "Futures": 5,
            "Short-Term": 5,
            "Other": 5
        },
        "asset_experience": {
            "Stocks": {"year_started": "2010", "level": "Good"},
            "Bonds": {"year_started": "2012", "level": "Limited"},
            "Mutual Funds": {"year_started": "2008", "level": "Extensive"},
            "ETFs": {"year_started": "2015", "level": "Good"},
            "Options": {"year_started": "2018", "level": "Limited"},
            "Futures": {"year_started": "2020", "level": "None"}
        },
        "has_outside_broker": True,
        "outside_firm_name": "Fidelity Investments",
        "outside_liquid_amount": "150000",
        "annual_income": "100000",
        "education_status": "Bachelor\'s Degree",
        "tax_bracket": "25%",
        "risk_tolerance": "Moderate",
        "investment_objectives": "Retirement",
        "electronic_regulatory_yes": True,
        "former_employer": "Old Company",
        "income_source": "Pension"
    }
    
    # Generate test PDF
    output_path = "sample_form.pdf"
    if generate_pdf_from_data(test_data, output_path):
        print(f"Test PDF generated successfully at {output_path}")
    else:
        print("Failed to generate test PDF")


