#!/usr/bin/env python3
"""
Enhanced Validation Module for Magnus Client Intake Form
Provides comprehensive validation with real-time feedback
"""

import re
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime, date

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class FormValidator:
    """Comprehensive form validation class"""
    
    def __init__(self):
        self.errors = {}
        self.warnings = {}
    
    def clear_errors(self):
        """Clear all validation errors and warnings"""
        self.errors.clear()
        self.warnings.clear()
    
    def add_error(self, field: str, message: str):
        """Add a validation error for a specific field"""
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(message)
    
    def add_warning(self, field: str, message: str):
        """Add a validation warning for a specific field"""
        if field not in self.warnings:
            self.warnings[field] = []
        self.warnings[field].append(message)
    
    def has_errors(self) -> bool:
        """Check if there are any validation errors"""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Check if there are any validation warnings"""
        return len(self.warnings) > 0
    
    def get_error_summary(self) -> str:
        """Get a formatted summary of all errors"""
        if not self.has_errors():
            return ""
        
        summary = "Please correct the following errors:\n\n"
        for field, messages in self.errors.items():
            summary += f"• {field}: {', '.join(messages)}\n"
        return summary
    
    def get_warning_summary(self) -> str:
        """Get a formatted summary of all warnings"""
        if not self.has_warnings():
            return ""
        
        summary = "Please review the following warnings:\n\n"
        for field, messages in self.warnings.items():
            summary += f"• {field}: {', '.join(messages)}\n"
        return summary
    
    # Field-specific validation methods
    
    def validate_required_field(self, field_name: str, value: str) -> bool:
        """Validate that a required field is not empty"""
        if not value or value.strip() == "":
            self.add_error(field_name, "This field is required")
            return False
        return True
    
    def validate_email(self, field_name: str, email: str) -> bool:
        """Validate email format"""
        if not email:
            return True  # Allow empty emails unless required
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            self.add_error(field_name, "Please enter a valid email address")
            return False
        return True
    
    def validate_ssn(self, field_name: str, ssn: str) -> bool:
        """Validate Social Security Number format"""
        if not ssn:
            return True  # Allow empty unless required
        
        # Remove any formatting
        clean_ssn = re.sub(r'[^\d]', '', ssn)
        
        if len(clean_ssn) != 9:
            self.add_error(field_name, "SSN must be 9 digits")
            return False
        
        # Check for invalid patterns
        invalid_patterns = [
            '000000000', '111111111', '222222222', '333333333',
            '444444444', '555555555', '666666666', '777777777',
            '888888888', '999999999', '123456789'
        ]
        
        if clean_ssn in invalid_patterns:
            self.add_error(field_name, "Please enter a valid SSN")
            return False
        
        return True
    
    def validate_phone(self, field_name: str, phone: str) -> bool:
        """Validate phone number format"""
        if not phone:
            return True  # Allow empty unless required
        
        # Remove formatting
        clean_phone = re.sub(r'[^\d]', '', phone)
        
        if len(clean_phone) != 10:
            self.add_error(field_name, "Phone number must be 10 digits")
            return False
        
        return True
    
    def validate_date(self, field_name: str, date_str: str, min_age: int = None, max_age: int = None) -> bool:
        """Validate date and optionally check age constraints"""
        if not date_str:
            return True  # Allow empty unless required
        
        try:
            # Parse date (assuming MM/dd/yyyy format)
            date_obj = datetime.strptime(date_str, "%m/%d/%Y").date()
            
            # Check if date is in the future
            if date_obj > date.today():
                self.add_error(field_name, "Date cannot be in the future")
                return False
            
            # Check age constraints if provided
            if min_age or max_age:
                today = date.today()
                age = today.year - date_obj.year - ((today.month, today.day) < (date_obj.month, date_obj.day))
                
                if min_age and age < min_age:
                    self.add_error(field_name, f"Age must be at least {min_age} years")
                    return False
                
                if max_age and age > max_age:
                    self.add_error(field_name, f"Age cannot exceed {max_age} years")
                    return False
            
            return True
            
        except ValueError:
            self.add_error(field_name, "Please enter a valid date (MM/DD/YYYY)")
            return False
    
    def validate_percentage_total(self, field_name: str, percentages: List[float], expected_total: float = 100.0) -> bool:
        """Validate that percentages add up to expected total"""
        total = sum(percentages)
        
        if abs(total - expected_total) > 0.01:  # Allow small floating point differences
            self.add_error(field_name, f"Percentages must total {expected_total}% (currently {total}%)")
            return False
        
        return True
    
    def validate_numeric_range(self, field_name: str, value: float, min_val: float = None, max_val: float = None) -> bool:
        """Validate numeric value is within specified range"""
        if min_val is not None and value < min_val:
            self.add_error(field_name, f"Value must be at least {min_val}")
            return False
        
        if max_val is not None and value > max_val:
            self.add_error(field_name, f"Value cannot exceed {max_val}")
            return False
        
        return True
    
    def validate_personal_info(self, data: Dict) -> bool:
        """Validate personal information section"""
        valid = True
        
        # Required fields
        if not self.validate_required_field("Full Name", data.get("full_name", "")):
            valid = False
        
        if not self.validate_required_field("Date of Birth", data.get("dob", "")):
            valid = False
        else:
            # Validate age (must be at least 18, not more than 120)
            if not self.validate_date("Date of Birth", data.get("dob", ""), min_age=18, max_age=120):
                valid = False
        
        if not self.validate_required_field("Citizenship", data.get("citizenship", "")):
            valid = False
        
        # SSN validation
        if not self.validate_ssn("Social Security Number", data.get("ssn", "")):
            valid = False
        
        return valid
    
    def validate_contact_info(self, data: Dict) -> bool:
        """Validate contact information section"""
        valid = True
        
        # Required fields
        if not self.validate_required_field("Residential Address", data.get("residential_address", "")):
            valid = False
        
        # Email validation
        if not self.validate_email("Email Address", data.get("email", "")):
            valid = False
        
        # Phone validation (at least one phone number required)
        home_phone = data.get("home_phone", "")
        work_phone = data.get("work_phone", "")
        mobile_phone = data.get("mobile_phone", "")
        
        if not home_phone and not work_phone and not mobile_phone:
            self.add_error("Phone Numbers", "At least one phone number is required")
            valid = False
        else:
            # Validate individual phone numbers
            if home_phone and not self.validate_phone("Home Phone", home_phone):
                valid = False
            if work_phone and not self.validate_phone("Work Phone", work_phone):
                valid = False
            if mobile_phone and not self.validate_phone("Mobile Phone", mobile_phone):
                valid = False
        
        return valid
    
    def validate_employment_info(self, data: Dict) -> bool:
        """Validate employment information section"""
        valid = True
        
        employment_status = data.get("employment_status", "")
        
        # If employed, require employer information
        if employment_status in ["Employed", "Self-Employed"]:
            if not self.validate_required_field("Employer Name", data.get("employer_name", "")):
                valid = False
            if not self.validate_required_field("Occupation/Title", data.get("occupation", "")):
                valid = False
        
        # Validate years employed
        years_employed = data.get("years_employed", 0)
        if not self.validate_numeric_range("Years Employed", years_employed, min_val=0, max_val=70):
            valid = False
        
        return valid
    
    def validate_beneficiaries(self, beneficiaries: List[Dict]) -> bool:
        """Validate beneficiaries information"""
        valid = True
        
        if not beneficiaries:
            self.add_warning("Beneficiaries", "No beneficiaries specified")
            return True
        
        # Validate individual beneficiaries
        total_percentage = 0
        for i, beneficiary in enumerate(beneficiaries):
            field_prefix = f"Beneficiary {i+1}"
            
            if not self.validate_required_field(f"{field_prefix} Name", beneficiary.get("name", "")):
                valid = False
            
            if not self.validate_required_field(f"{field_prefix} Relationship", beneficiary.get("relationship", "")):
                valid = False
            
            percentage = beneficiary.get("percentage", 0)
            if not self.validate_numeric_range(f"{field_prefix} Percentage", percentage, min_val=0, max_val=100):
                valid = False
            
            total_percentage += percentage
        
        # Validate total percentage
        if not self.validate_percentage_total("Beneficiaries Total", [total_percentage]):
            valid = False
        
        return valid
    
    def validate_assets(self, data: Dict) -> bool:
        """Validate assets and investment information"""
        valid = True
        
        # Validate numeric fields
        net_worth = data.get("net_worth", "")
        if net_worth and not net_worth.replace(",", "").replace(".", "").isdigit():
            self.add_error("Net Worth", "Please enter a valid numeric value")
            valid = False
        
        liquid_net_worth = data.get("liquid_net_worth", "")
        if liquid_net_worth and not liquid_net_worth.replace(",", "").replace(".", "").isdigit():
            self.add_error("Liquid Net Worth", "Please enter a valid numeric value")
            valid = False
        
        # Validate asset breakdown if included
        if data.get("include_breakdown", False):
            breakdown = data.get("asset_breakdown", {})
            if breakdown:
                percentages = [v for v in breakdown.values() if isinstance(v, (int, float))]
                if not self.validate_percentage_total("Asset Breakdown", percentages):
                    valid = False
        
        return valid

    def validate_annual_income(self, field_name: str, income: str) -> bool:
        """Validate annual income format and range"""
        if not income:
            return True  # Allow empty unless required
        
        # Remove formatting (commas, dollar signs)
        clean_income = re.sub(r'[^\d.]', '', income)
        
        try:
            income_value = float(clean_income)
            if income_value < 0:
                self.add_error(field_name, "Annual income cannot be negative")
                return False
            if income_value > 100000000:  # 100 million cap for reasonableness
                self.add_error(field_name, "Annual income seems unreasonably high")
                return False
            return True
        except ValueError:
            self.add_error(field_name, "Please enter a valid annual income amount")
            return False
    
    def validate_tax_bracket(self, field_name: str, bracket: str) -> bool:
        """Validate US tax bracket selection"""
        if not bracket:
            return True  # Allow empty unless required
        
        valid_brackets = [
            "0-15%", "15%-32%", "32%+", 
            "Not sure", "Prefer not to answer"
        ]
        
        if bracket not in valid_brackets:
            self.add_error(field_name, "Please select a valid tax bracket")
            return False
        
        return True
    
    def validate_education_status(self, field_name: str, education: str) -> bool:
        """Validate education status selection"""
        if not education:
            return True  # Allow empty unless required
        
        valid_education = [
            "High School", "Some College", "Associate Degree", 
            "Bachelor's Degree", "Master's Degree", "Doctoral Degree",
            "Professional Degree", "Other", "Prefer not to answer"
        ]
        
        if education not in valid_education:
            self.add_error(field_name, "Please select a valid education level")
            return False
        
        return True
    
    def validate_risk_tolerance(self, field_name: str, risk_tolerance: str) -> bool:
        """Validate risk tolerance selection"""
        if not risk_tolerance:
            return True  # Allow empty unless required
        
        valid_risk_levels = [
            "Conservative", "Moderate", "Moderate Aggressive", "Aggressive"
        ]
        
        if risk_tolerance not in valid_risk_levels:
            self.add_error(field_name, "Please select a valid risk tolerance level")
            return False
        
        return True
    
    def validate_investment_objectives(self, field_name: str, objectives: str) -> bool:
        """Validate investment objectives selection"""
        if not objectives:
            return True  # Allow empty unless required
        
        valid_objectives = [
            "Income", "Growth and Income", "Capital Appreciation", "Speculation"
        ]
        
        if objectives not in valid_objectives:
            self.add_error(field_name, "Please select a valid investment objective")
            return False
        
        return True
    
    def validate_trusted_contact_info(self, data: Dict) -> bool:
        """Validate trusted contact information if opted in"""
        valid = True
        
        if not data.get("trusted_contact_opt_in", False):
            return True  # Skip validation if not opted in
        
        # Required fields for trusted contact
        if not self.validate_required_field("Trusted Contact Name", data.get("trusted_contact_name", "")):
            valid = False
        
        if not self.validate_required_field("Trusted Contact Relationship", data.get("trusted_contact_relationship", "")):
            valid = False
        
        # Phone number validation
        if not self.validate_phone("Trusted Contact Phone", data.get("trusted_contact_phone", "")):
            valid = False
        
        # Email validation (optional but if provided must be valid)
        trusted_email = data.get("trusted_contact_email", "")
        if trusted_email and not self.validate_email("Trusted Contact Email", trusted_email):
            valid = False
        
        return valid
    
    def validate_retirement_info(self, data: Dict) -> bool:
        """Validate retirement-specific information"""
        valid = True
        
        employment_status = data.get("employment_status", "")
        if employment_status != "Retired":
            return True  # Skip validation if not retired
        
        # Required fields for retired individuals
        if not self.validate_required_field("Former Employer", data.get("former_employer", "")):
            valid = False
        
        if not self.validate_required_field("Source of Income", data.get("retirement_income_source", "")):
            valid = False
        
        return valid
    
    def validate_expanded_asset_experience(self, data: Dict) -> bool:
        """Validate expanded asset experience information"""
        valid = True
        
        # List of all asset types
        asset_types = [
            "Stocks/Bonds", "Mutual Funds", "UITs", "Annuities Fixed", 
            "Annuities Variable", "Options", "Commodities", 
            "Alternative Investments", "Limited Partnerships", "Variable Contracts"
        ]
        
        asset_experience = data.get("expanded_asset_experience", {})
        
        for asset in asset_types:
            asset_key = asset.lower().replace("/", "_").replace(" ", "_")
            experience_data = asset_experience.get(asset, {})
            
            # Validate year started if provided
            year_started = experience_data.get("year_started", "")
            if year_started:
                try:
                    year = int(year_started)
                    current_year = datetime.now().year
                    if year < 1950 or year > current_year:
                        self.add_error(f"{asset} Experience Year", 
                                     f"Year must be between 1950 and {current_year}")
                        valid = False
                except ValueError:
                    self.add_error(f"{asset} Experience Year", "Please enter a valid year")
                    valid = False
        
        return valid
    
    def validate_financial_info_extended(self, data: Dict) -> bool:
        """Validate extended financial information"""
        valid = True
        
        # Validate annual income
        if not self.validate_annual_income("Annual Income", data.get("annual_income", "")):
            valid = False
        
        # Validate tax bracket
        if not self.validate_tax_bracket("Tax Bracket", data.get("tax_bracket", "")):
            valid = False
        
        # Validate education status
        if not self.validate_education_status("Education Status", data.get("education_status", "")):
            valid = False
        
        # Validate risk tolerance
        if not self.validate_risk_tolerance("Risk Tolerance", data.get("risk_tolerance", "")):
            valid = False
        
        # Validate investment objectives
        if not self.validate_investment_objectives("Investment Objectives", data.get("investment_objectives", "")):
            valid = False
        
        # Validate trusted contact info
        if not self.validate_trusted_contact_info(data):
            valid = False
        
        # Validate retirement info
        if not self.validate_retirement_info(data):
            valid = False
        
        # Validate expanded asset experience
        if not self.validate_expanded_asset_experience(data):
            valid = False
        
        return valid

# Global validator instance
form_validator = FormValidator()

