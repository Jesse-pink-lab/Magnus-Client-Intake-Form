#!/usr/bin/env python3
"""
Magnus Client Intake Form Generator
- Save drafts in Word format (.docx) for editing
- Generate final reports in PDF format

INSTALLATION REQUIRED:
pip install reportlab python-docx
"""

import os
import sys
import traceback

# Check for required packages
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_RIGHT
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from datetime import datetime
except ImportError:
    print("ERROR: ReportLab is not installed. Please run: pip install reportlab")
    sys.exit(1)

try:
    from docx import Document
    from docx.shared import Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except ImportError:
    print("ERROR: python-docx is not installed. Please run: pip install python-docx")
    sys.exit(1)

from .validation import parse_usd, format_usd, parse_percent, format_percent, parse_iso_date


def fmt_usd(val):
    num = parse_usd(val)
    return format_usd(num) if num is not None else "[Not provided]"


def fmt_percent(val):
    num = parse_percent(val)
    return format_percent(num) if num is not None else "[Not provided]"


def fmt_date(val):
    d = parse_iso_date(val) if isinstance(val, str) else None
    return d.strftime("%Y-%m-%d") if d else "[Not provided]"


class NumberedCanvas(canvas.Canvas):
    """Canvas that knows how to draw headers, footers, and page numbers."""

    def __init__(self, *args, title: str = "", generated: str = "", **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.generated = generated
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count: int):
        width, height = self._pagesize
        self.setFont("Helvetica", 8)
        # Header
        self.drawString(72, height - 0.75 * inch, self.title)
        self.drawRightString(width - 72, height - 0.75 * inch, self.generated)
        # Footer
        self.drawString(72, 0.75 * inch, "Magnus Client Intake Form — Confidential")
        self.drawRightString(
            width - 72,
            0.75 * inch,
            f"Page {self._pageNumber} of {page_count}",
        )

def save_draft_word(form_data, output_path):
    """Save form data as a Word document draft"""
    try:
        # Create document
        doc = Document()
        
        # Add title
        doc.add_heading('Magnus Client Intake Form', 0)
        doc.add_paragraph()
        
        # Personal Information
        doc.add_heading('Personal Information', level=1)
        doc.add_paragraph(f"Full Name: {form_data.get('full_name', '[Not provided]')}")
        doc.add_paragraph(f"Date of Birth: {form_data.get('dob', '[Not provided]')}")
        doc.add_paragraph(f"Social Security Number: {form_data.get('ssn', '[Not provided]')}")
        doc.add_paragraph(f"Citizenship: {form_data.get('citizenship', '[Not provided]')}")
        doc.add_paragraph(f"Marital Status: {form_data.get('marital_status', '[Not provided]')}")
        doc.add_paragraph()
        
        # Contact Information
        doc.add_heading('Contact Information', level=1)
        doc.add_paragraph(f"Residential Address: {form_data.get('address', '[Not provided]')}")
        doc.add_paragraph(f"Email: {form_data.get('email', '[Not provided]')}")
        doc.add_paragraph(f"Home Phone: {form_data.get('phone_home', '[Not provided]')}")
        doc.add_paragraph(f"Mobile Phone: {form_data.get('phone_mobile', '[Not provided]')}")
        doc.add_paragraph(f"Work Phone: {form_data.get('phone_work', '[Not provided]')}")
        doc.add_paragraph()
        
        # Employment Information
        doc.add_heading('Employment Information', level=1)
        doc.add_paragraph(f"Employment Status: {form_data.get('employment_status', '[Not provided]')}")
        doc.add_paragraph(f"Employer Name: {form_data.get('employer_name', '[Not provided]')}")
        doc.add_paragraph(f"Employer Address: {form_data.get('employer_address', '[Not provided]')}")
        doc.add_paragraph(f"Occupation/Title: {form_data.get('job_title', '[Not provided]')}")
        doc.add_paragraph(f"Years Employed: {form_data.get('years_with_employer', '[Not provided]')}")
        doc.add_paragraph(f"Annual Income: {fmt_usd(form_data.get('annual_income'))}")
        
        # Retirement Information (if applicable)
        if form_data.get("employment_status") == "Retired":
            doc.add_paragraph()
            doc.add_heading('Retirement Information', level=1)
            doc.add_paragraph(f"Former Employer: {form_data.get('former_employer', '[Not provided]')}")
            doc.add_paragraph(f"Source of Income: {form_data.get('income_source', '[Not provided]')}")
        
        doc.add_paragraph()
        
        # Financial Information
        doc.add_heading('Financial Information', level=1)
        doc.add_paragraph(f"Education Status: {form_data.get('education_status', '[Not provided]')}")
        doc.add_paragraph(f"Estimated Tax Bracket: {fmt_percent(form_data.get('est_tax_bracket'))}")
        doc.add_paragraph(f"Investment Risk Tolerance: {form_data.get('risk_tolerance', '[Not provided]')}")
        doc.add_paragraph(f"Time Horizon: {form_data.get('time_horizon', '[Not provided]')}")
        doc.add_paragraph(f"Investment Objective: {form_data.get('investment_objective', '[Not provided]')}")
        doc.add_paragraph(f"Net Worth (excluding primary home): {fmt_usd(form_data.get('est_net_worth'))}")
        doc.add_paragraph(f"Liquid Net Worth: {fmt_usd(form_data.get('est_liquid_net_worth'))}")
        doc.add_paragraph(f"Assets Held Away – Total: {fmt_usd(form_data.get('assets_held_away_total'))}")
        doc.add_paragraph(f"Assets Held Away – Liquid: {fmt_usd(form_data.get('assets_held_away_liquid'))}")
        doc.add_paragraph(f"Assets Held Away at Other Brokerage Firms: {fmt_usd(form_data.get('assets_held_away_other_brokers'))}")
        doc.add_paragraph()
        
        # Spouse Information (if applicable)
        if not form_data.get("spouse_applicable", False):
            doc.add_heading('Spouse/Partner Information', level=1)
            doc.add_paragraph(f"Spouse Full Name: {form_data.get('spouse_full_name', '[Not provided]')}")
            doc.add_paragraph(f"Spouse Date of Birth: {form_data.get('spouse_dob', '[Not provided]')}")
            doc.add_paragraph(f"Spouse SSN: {form_data.get('spouse_ssn', '[Not provided]')}")
            doc.add_paragraph(f"Spouse Employment Status: {form_data.get('spouse_employment_status', '[Not provided]')}")
            doc.add_paragraph(f"Spouse Employer Name: {form_data.get('spouse_employer_name', '[Not provided]')}")
            doc.add_paragraph(f"Spouse Occupation/Title: {form_data.get('spouse_job_title', '[Not provided]')}")
            doc.add_paragraph(f"Spouse Phone: {form_data.get('spouse_phone', '[Not provided]')}")
            doc.add_paragraph()
        else:
            doc.add_heading('Spouse/Partner Information', level=1)
            doc.add_paragraph("[Not applicable]")
            doc.add_paragraph()
        
        # Dependents Information
        doc.add_heading('Dependents Information', level=1)
        dependents = form_data.get("dependents", [])
        if dependents:
            for i, dep in enumerate(dependents):
                doc.add_paragraph(f"Dependent {i+1}:")
                doc.add_paragraph(f"  Name: {dep.get('full_name', '[Not provided]')}")
                doc.add_paragraph(f"  Date of Birth: {fmt_date(dep.get('dob'))}")
                doc.add_paragraph(f"  Relationship: {dep.get('relationship', '[Not provided]')}")
        else:
            doc.add_paragraph("No dependents specified")
        doc.add_paragraph()

        # Beneficiaries Information
        doc.add_heading('Beneficiaries Information', level=1)
        beneficiaries = form_data.get("beneficiaries", [])
        if beneficiaries:
            for i, ben in enumerate(beneficiaries):
                doc.add_paragraph(f"Beneficiary {i+1}:")
                doc.add_paragraph(f"  Name: {ben.get('full_name', '[Not provided]')}")
                doc.add_paragraph(f"  Date of Birth: {fmt_date(ben.get('dob'))}")
                doc.add_paragraph(f"  Relationship: {ben.get('relationship', '[Not provided]')}")
                doc.add_paragraph(f"  SSN: {ben.get('beneficiary_ssn', '[Not provided]')}")
                doc.add_paragraph(f"  Percentage: {fmt_percent(ben.get('allocation'))}")
        else:
            doc.add_paragraph("No beneficiaries specified")
        doc.add_paragraph()
        
        # Investment Experience
        doc.add_heading('Investment Experience', level=1)
        asset_map = [
            ("Stocks", "stocks"),
            ("Bonds", "bonds"),
            ("Mutual Funds", "mutual_funds"),
            ("UITs", "uits"),
            ("Annuities (Fixed)", "annuities_fixed"),
            ("Annuities (Variable)", "annuities_variable"),
            ("Options", "options"),
            ("Commodities", "commodities"),
            ("Alternative Investments", "alternative_investments"),
            ("Limited Partnerships", "limited_partnerships"),
            ("Variable Contracts", "variable_contracts"),
        ]
        for label, key in asset_map:
            year = form_data.get(f"{key}_year_started")
            level = form_data.get(f"{key}_level")
            doc.add_paragraph(f"{label} – Year Started: {year if year else '[Not provided]'}, Level: {level if level else '[Not provided]'}")
            doc.add_paragraph()
        
        # Outside Broker Information
        if form_data.get("has_outside_broker", False):
            doc.add_heading('Outside Broker Information', level=1)
            doc.add_paragraph(f"Broker Firm Name: {form_data.get('outside_broker_name', '[Not provided]')}")
            doc.add_paragraph(f"Account Number: {form_data.get('outside_broker_account', '[Not provided]')}")
            doc.add_paragraph(f"Account Type: {form_data.get('outside_broker_account_type', '[Not provided]')}")
            doc.add_paragraph()
        
        # Trusted Contact Information
        doc.add_heading('Trusted Contact Information', level=1)
        doc.add_paragraph(f"Full Name: {form_data.get('tc_full_name', '[Not provided]')}")
        doc.add_paragraph(f"Relationship: {form_data.get('tc_relationship', '[Not provided]')}")
        doc.add_paragraph(f"Phone Number: {form_data.get('tc_phone', '[Not provided]')}")
        doc.add_paragraph(f"Email Address: {form_data.get('tc_email', '[Not provided]')}")
        doc.add_paragraph()
        
        # Regulatory Consent
        doc.add_heading('Regulatory Consent', level=1)
        electronic_consent = form_data.get("ed_consent", "No") or "No"
        doc.add_paragraph(f"Electronic Delivery Consent: {electronic_consent}")
        
        # Save document
        doc.save(output_path)
        return True
        
    except Exception as e:
        print(f"Error saving Word document: {str(e)}")
        traceback.print_exc()
        return False

def generate_pdf_report(form_data, output_path):
    """Generate a professional PDF report from form data."""
    try:
        if not isinstance(form_data, dict):
            raise ValueError("Form data must be a dictionary")

        generated_ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )

        styles = getSampleStyleSheet()
        section_heading_style = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            spaceBefore=12,
            spaceAfter=6,
            backColor=colors.whitesmoke,
        )
        label_style = ParagraphStyle(
            "FieldLabel",
            fontName="Helvetica-Bold",
            fontSize=10,
            alignment=TA_LEFT,
        )
        value_style = ParagraphStyle(
            "FieldValue",
            fontName="Helvetica",
            fontSize=10,
            alignment=TA_LEFT,
        )
        value_currency_style = ParagraphStyle(
            "CurrencyValue",
            parent=value_style,
            alignment=TA_RIGHT,
        )
        empty_value_style = ParagraphStyle(
            "EmptyValue",
            fontName="Helvetica-Oblique",
            fontSize=10,
            textColor=colors.grey,
            alignment=TA_LEFT,
        )
        empty_currency_style = ParagraphStyle(
            "EmptyCurrency",
            parent=empty_value_style,
            alignment=TA_RIGHT,
        )
        table_header_style = ParagraphStyle(
            "TableHeader",
            fontName="Helvetica-Bold",
            fontSize=10,
            alignment=TA_LEFT,
        )

        def safe(v):
            return "" if v is None else str(v).replace("\n", "<br/>")

        def field_row(label, value, is_currency=False):
            lbl = Paragraph(label, label_style)
            if value in (None, "", "[Not provided]"):
                val = Paragraph(
                    "Not Provided",
                    empty_currency_style if is_currency else empty_value_style,
                )
            else:
                val_text = fmt_usd(value) if is_currency else safe(value)
                val = Paragraph(
                    val_text,
                    value_currency_style if is_currency else value_style,
                )
            return [lbl, val]

        def add_section(title, fields):
            content.append(Paragraph(title, section_heading_style))
            rows = [field_row(*f) for f in fields]
            table = Table(rows, colWidths=[2.5 * inch, 3.5 * inch])
            table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
            content.append(table)
            content.append(Spacer(1, 12))

        def add_table_section(title, headers, rows, col_widths=None):
            content.append(Paragraph(title, section_heading_style))
            table_data = [[Paragraph(h, table_header_style) for h in headers]]
            if rows:
                for row in rows:
                    table_data.append([
                        Paragraph(
                            "Not Provided" if (c is None or c == "") else safe(c),
                            empty_value_style if (c is None or c == "") else value_style,
                        ) for c in row
                    ])
            else:
                table_data.append([Paragraph("Not Provided", empty_value_style) for _ in headers])
            table = Table(table_data, colWidths=col_widths, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
                ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
                ("VALIGN", (0,0), (-1,-1), "TOP"),
            ]))
            content.append(table)
            content.append(Spacer(1, 12))

        content = []
        content.append(Paragraph("Magnus Client Intake Form", styles["Title"]))
        content.append(Spacer(1, 12))

        investment_objective = form_data.get("investment_objective")

        add_section("Personal Information", [
            ("Full Name", form_data.get("full_name")),
            ("Date of Birth", form_data.get("dob")),
            ("Social Security Number", form_data.get("ssn")),
            ("Citizenship", form_data.get("citizenship_status")),
            ("Marital Status", form_data.get("marital_status")),
        ])

        add_section("Contact Information", [
            ("Residential Address", form_data.get("address")),
            ("Email", form_data.get("email")),
            ("Home Phone", form_data.get("phone_home")),
            ("Mobile Phone", form_data.get("phone_mobile")),
            ("Work Phone", form_data.get("phone_work")),
        ])

        add_section("Employment Information", [
            ("Employment Status", form_data.get("employment_status")),
            ("Employer Name", form_data.get("employer_name")),
            ("Employer Address", form_data.get("employer_address")),
            ("Occupation/Title", form_data.get("job_title")),
            ("Years Employed", form_data.get("years_with_employer")),
            ("Annual Income", form_data.get("annual_income"), True),
        ])

        add_section("Financial Information", [
            ("Education Status", form_data.get("education_status")),
            ("Estimated Tax Bracket", fmt_percent(form_data.get("est_tax_bracket"))),
            ("Investment Risk Tolerance", form_data.get("risk_tolerance")),
            ("Time Horizon", form_data.get("time_horizon")),
            ("Investment Objective", investment_objective),
            ("Estimated Net Worth", form_data.get("est_net_worth"), True),
            ("Liquid Net Worth", form_data.get("est_liquid_net_worth"), True),
            ("Assets Held Away – Total", form_data.get("assets_held_away_total"), True),
            ("Assets Held Away – Liquid", form_data.get("assets_held_away_liquid"), True),
            ("Assets Held Away – At Other Brokerage Firms", form_data.get("assets_held_away_other_brokers"), True),
        ])

        add_section("Spouse/Partner Information", [
            ("Full Name", form_data.get("spouse_full_name")),
            ("Date of Birth", form_data.get("spouse_dob")),
            ("SSN", form_data.get("spouse_ssn")),
            ("Employment Status", form_data.get("spouse_employment_status")),
            ("Employer Name", form_data.get("spouse_employer_name")),
            ("Occupation/Title", form_data.get("spouse_job_title")),
            ("Phone", form_data.get("spouse_phone")),
        ])

        dependents = form_data.get("dependents") or []
        dep_rows = [[d.get("full_name"), fmt_date(d.get("dob")), d.get("relationship")] for d in dependents]
        add_table_section("Dependents", ["Name", "DOB", "Relationship"], dep_rows)

        beneficiaries = form_data.get("beneficiaries") or []
        ben_rows = [
            [
                b.get("full_name"),
                fmt_date(b.get("dob")),
                b.get("beneficiary_ssn"),
                fmt_percent(b.get("allocation")),
            ]
            for b in beneficiaries
        ]
        add_table_section(
            "Beneficiaries",
            ["Name", "DOB", "SSN", "Allocation"],
            ben_rows,
            col_widths=[2.5 * inch, 1.5 * inch, 1.5 * inch, 1.0 * inch],
        )

        asset_map = [
            ("Stocks", "stocks"),
            ("Bonds", "bonds"),
            ("Mutual Funds", "mutual_funds"),
            ("UITs", "uits"),
            ("Annuities (Fixed)", "annuities_fixed"),
            ("Annuities (Variable)", "annuities_variable"),
            ("Options", "options"),
            ("Commodities", "commodities"),
            ("Alternative Investments", "alternative_investments"),
            ("Limited Partnerships", "limited_partnerships"),
            ("Variable Contracts", "variable_contracts"),
        ]
        inv_rows = [[label, form_data.get(f"{key}_year_started"), form_data.get(f"{key}_level")] for label, key in asset_map]
        add_table_section("Investment Experience", ["Investment", "Year Started", "Level"], inv_rows)

        add_section("Broker-Dealer Relationships", [
            ("Employed by This Broker-Dealer", form_data.get("employee_this_bd")),
            ("Related to Employee of This Broker-Dealer", form_data.get("related_this_bd")),
            ("Employed by Other Broker-Dealer", form_data.get("employee_other_bd")),
            ("Related to Employee of Other Broker-Dealer", form_data.get("related_other_bd")),
        ])

        add_section("Regulatory Affiliations", [
            ("Membership Type", form_data.get("membership_type")),
            ("CRD/Member ID", form_data.get("sro_crd")),
            ("Branch", form_data.get("sro_branch")),
            ("Company", form_data.get("company_name")),
            ("Ticker", form_data.get("ticker")),
            ("Exchange", form_data.get("exchange")),
            ("Role/Capacity", form_data.get("role")),
            ("Ownership %", fmt_percent(form_data.get("ownership_pct"))),
            ("As Of", form_data.get("as_of")),
        ])

        add_section("Foreign Financial Accounts", [
            ("Institution", form_data.get("institution_name")),
            ("Country", form_data.get("country")),
            ("Purpose", form_data.get("purpose")),
            ("Source of Funds", form_data.get("source_of_funds")),
            ("Open Date", form_data.get("open_date")),
            ("Private Banking Account", form_data.get("private_banking")),
            ("Foreign Bank Account", form_data.get("foreign_bank_acct")),
        ])

        add_section("Politically Exposed Person (PEP)", [
            ("Name", form_data.get("pep_name")),
            ("Country", form_data.get("pep_country")),
            ("Relationship", form_data.get("pep_relationship")),
            ("Title", form_data.get("pep_title")),
            ("Start Date", form_data.get("pep_start")),
            ("End Date", form_data.get("pep_end")),
            ("Screening Consent", form_data.get("pep_screening_consent")),
        ])

        add_section("Outside Broker Information", [
            ("Broker Firm Name", form_data.get("outside_firm_name")),
            ("Account Type", form_data.get("outside_broker_account_type")),
            ("Account Number", form_data.get("outside_broker_account_number")),
            ("Liquid Amount", form_data.get("outside_liquid_amount"), True),
        ])

        add_section("Trusted Contact Information", [
            ("Full Name", form_data.get("tc_full_name")),
            ("Relationship", form_data.get("tc_relationship")),
            ("Phone Number", form_data.get("tc_phone")),
            ("Email Address", form_data.get("tc_email")),
        ])

        add_section("Regulatory Consent", [
            ("Electronic Delivery Consent", form_data.get("ed_consent", "No")),
        ])

        doc.build(
            content,
            canvasmaker=lambda *args, **kw: NumberedCanvas(
                *args, title="Magnus Client Intake Form", generated=generated_ts, **kw
            ),
        )
        return True

    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        traceback.print_exc()
        return False
# Alias for backward compatibility with main_enhanced.py
generate_pdf_from_data = generate_pdf_report


def generate(form_data, output_path):
    """Compatibility wrapper expected by the UI."""
    return generate_pdf_report(form_data, output_path)
