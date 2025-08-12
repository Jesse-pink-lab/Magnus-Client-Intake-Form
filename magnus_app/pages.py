from typing import Any, Dict, List

ISO_COUNTRIES = [
    'United States',
    'Canada',
    'Mexico',
    'United Kingdom',
    'Germany',
    'France',
    'Australia',
    'Japan',
    'China',
    'India',
    'Brazil',
    'Italy',
    'Spain',
]

PAGES: List[Dict[str, Any]] = [
    {
        'key': 'personal_info',
        'title': 'Personal Information',
        'sections': [
            {
                'title': 'Personal Information',
                'fields': [
                    {
                        'name': 'full_name',
                        'type': 'text',
                        'label': 'Full Legal Name',
                        'required': True,
                        'validate': 'person_name',
                    },
                    {
                        'name': 'dob',
                        'type': 'date',
                        'label': 'Date of Birth',
                        'required': True,
                        'validate': 'date_adult',
                    },
                    {
                        'name': 'ssn',
                        'type': 'text',
                        'label': 'Social Security Number',
                        'required': False,
                        'validate': 'ssn_masked',
                        'input_mask': 'ssn',
                    },
                    {
                        'name': 'citizenship_status',
                        'type': 'select',
                        'label': 'Citizenship Status',
                        'required': True,
                        'options': ['U.S. Citizen', 'Resident Alien', 'Non-Resident Alien'],
                    },
                    {
                        'name': 'marital_status',
                        'type': 'select',
                        'label': 'Marital Status',
                        'required': True,
                        'options': ['Single', 'Married', 'Separated', 'Divorced', 'Widowed'],
                    },
                ],
            }
        ],
    },
    {
        'key': 'contact_info',
        'title': 'Contact Information',
        'sections': [
            {
                'title': 'Contact Information',
                'fields': [
                    {
                        'name': 'address',
                        'type': 'textarea',
                        'label': 'Residential Address',
                        'required': False,
                    },
                    {
                        'name': 'email',
                        'type': 'text',
                        'label': 'Email Address',
                        'required': False,
                        'validate': 'email_basic',
                    },
                    {
                        'name': 'phone_home',
                        'type': 'text',
                        'label': 'Home Phone',
                        'required': False,
                        'validate': 'phone_us',
                        'input_mask': 'phone',
                    },
                    {
                        'name': 'phone_mobile',
                        'type': 'text',
                        'label': 'Mobile Phone',
                        'required': False,
                        'validate': 'phone_us',
                        'input_mask': 'phone',
                    },
                    {
                        'name': 'phone_work',
                        'type': 'text',
                        'label': 'Work Phone',
                        'required': False,
                        'validate': 'phone_us',
                        'input_mask': 'phone',
                    },
                ],
            }
        ],
    },
    {
        'key': 'employment_info',
        'title': 'Employment Information',
        'sections': [
            {
                'title': 'Employment Information',
                'fields': [
                    {
                        'name': 'employment_status',
                        'type': 'select',
                        'label': 'Employment Status',
                        'required': True,
                        'options': ['Employed', 'Self-Employed', 'Unemployed', 'Retired', 'Student', 'Homemaker'],
                    },
                    {
                        'name': 'employer_name',
                        'type': 'text',
                        'label': 'Employer Name',
                        'required': False,
                    },
                    {
                        'name': 'job_title',
                        'type': 'text',
                        'label': 'Occupation/Job Title',
                        'required': False,
                        'validate': 'optional_person_name',
                    },
                    {
                        'name': 'years_with_employer',
                        'type': 'number',
                        'label': 'Years with Current Employer',
                        'required': False,
                    },
                    {
                        'name': 'annual_income',
                        'type': 'text',
                        'label': 'Annual Income',
                        'required': False,
                        'validate': 'usd_currency_0_1b',
                    },
                ],
            }
        ],
    },
    {
        'key': 'financial_info',
        'title': 'Financial Information',
        'sections': [
            {
                'title': 'Financial Details',
                'fields': [
                    {
                        'name': 'education_status',
                        'type': 'select',
                        'label': 'Education Status',
                        'required': False,
                        'options': ['High School', 'Some College', "Bachelor's", "Master's", 'Doctorate', 'Other'],
                    },
                    {
                        'name': 'est_tax_bracket',
                        'type': 'text',
                        'label': 'Estimated Tax Bracket',
                        'required': False,
                        'validate': 'percent_0_100',
                    },
                    {
                        'name': 'risk_tolerance',
                        'type': 'select',
                        'label': 'Investment Risk Tolerance',
                        'required': True,
                        'options': ['Low', 'Moderate', 'High'],
                    },
                ],
            },
            {
                'title': 'Investment Purpose',
                'fields': [
                    {
                        'name': 'inv_purpose_income',
                        'type': 'checkbox',
                        'label': 'Income',
                        'required': False,
                    },
                    {
                        'name': 'inv_purpose_growth_income',
                        'type': 'checkbox',
                        'label': 'Growth and Income',
                        'required': False,
                    },
                    {
                        'name': 'inv_purpose_cap_app',
                        'type': 'checkbox',
                        'label': 'Capital Appreciation',
                        'required': False,
                    },
                    {
                        'name': 'inv_purpose_speculation',
                        'type': 'checkbox',
                        'label': 'Speculation',
                        'required': False,
                    },
                ],
            },
            {
                'title': 'Investment Objectives (Rank 1–5; 1 is highest priority)',
                'fields': [
                    {
                        'name': 'rank_trading_profits',
                        'type': 'number',
                        'label': 'Trading Profits',
                        'required': False,
                        'validate': 'rank_1_5',
                    },
                    {
                        'name': 'rank_speculation',
                        'type': 'number',
                        'label': 'Speculation',
                        'required': False,
                        'validate': 'rank_1_5',
                    },
                    {
                        'name': 'rank_capital_appreciation',
                        'type': 'number',
                        'label': 'Capital Appreciation',
                        'required': False,
                        'validate': 'rank_1_5',
                    },
                    {
                        'name': 'rank_income',
                        'type': 'number',
                        'label': 'Income',
                        'required': False,
                        'validate': 'rank_1_5',
                    },
                    {
                        'name': 'rank_preservation',
                        'type': 'number',
                        'label': 'Preservation of Capital',
                        'required': False,
                        'validate': 'rank_1_5',
                    },
                ],
            },
            {
                'title': 'Totals',
                'fields': [
                    {
                        'name': 'est_net_worth',
                        'type': 'text',
                        'label': 'Estimated Net Worth (excluding primary residence)',
                        'required': False,
                        'validate': 'usd_currency_0_1b',
                        'placeholder': '$0.00',
                    },
                    {
                        'name': 'est_liquid_net_worth',
                        'type': 'text',
                        'label': 'Estimated Liquid Net Worth (cash + marketable securities)',
                        'required': False,
                        'validate': 'usd_currency_0_1b',
                        'placeholder': '$0.00',
                    },
                    {
                        'name': 'assets_held_away',
                        'type': 'text',
                        'label': 'Assets Held Away (e.g., Brokerage Accounts, 401k, etc.)',
                        'required': False,
                        'validate': 'usd_currency_0_1b',
                        'placeholder': '$0.00',
                    },
                ],
            },
        ],
    },
    {
        'key': 'spouse_info',
        'title': 'Spouse/Partner Information',
        'sections': [
            {
                'title': 'Spouse/Partner Information',
                'fields': [
                    {
                        'name': 'no_spouse',
                        'type': 'checkbox',
                        'label': 'N/A (I do not have a spouse/partner)',
                        'required': False,
                    },
                    {
                        'type': 'group',
                        'show_if': {'no_spouse': False},
                        'fields': [
                            {
                                'name': 'spouse_full_name',
                                'type': 'text',
                                'label': 'Full Legal Name',
                                'required': False,
                                'validate': 'person_name',
                            },
                            {
                                'name': 'spouse_dob',
                                'type': 'date',
                                'label': 'Date of Birth',
                                'required': False,
                                'validate': 'date_adult',
                            },
                            {
                                'name': 'spouse_ssn',
                                'type': 'text',
                                'label': 'Social Security Number',
                                'required': False,
                                'validate': 'ssn_masked',
                                'input_mask': 'ssn',
                            },
                            {
                                'name': 'spouse_employment_status',
                                'type': 'select',
                                'label': 'Employment Status',
                                'required': False,
                                'options': ['Employed', 'Self-Employed', 'Unemployed', 'Retired', 'Student', 'Homemaker'],
                            },
                            {
                                'name': 'spouse_employer_name',
                                'type': 'text',
                                'label': 'Employer Name',
                                'required': False,
                            },
                            {
                                'name': 'spouse_job_title',
                                'type': 'text',
                                'label': 'Occupation/Job Title',
                                'required': False,
                                'validate': 'optional_person_name',
                            },
                        ],
                    },
                ],
            }
        ],
    },
    {
        'key': 'dependents',
        'title': 'Dependents Information',
        'sections': [
            {
                'title': 'Dependents',
                'fields': [
                    {
                        'name': 'dependents',
                        'type': 'repeating_group',
                        'item_label': 'Dependent',
                        'fields': [
                            {
                                'name': 'full_name',
                                'type': 'text',
                                'label': 'Full Name',
                                'required': False,
                                'validate': 'person_name',
                            },
                            {
                                'name': 'dob',
                                'type': 'date',
                                'label': 'Date of Birth',
                                'required': False,
                                'validate': 'date_optional',
                            },
                            {
                                'name': 'relationship',
                                'type': 'text',
                                'label': 'Relationship',
                                'required': False,
                                'validate': 'optional_person_name',
                            },
                        ],
                    }
                ],
            }
        ],
    },
    {
        'key': 'beneficiaries',
        'title': 'Beneficiaries Information',
        'sections': [
            {
                'title': 'Beneficiaries',
                'fields': [
                    {
                        'name': 'beneficiaries',
                        'type': 'repeating_group',
                        'item_label': 'Beneficiary',
                        'fields': [
                            {
                                'name': 'full_name',
                                'type': 'text',
                                'label': 'Full Name',
                                'required': False,
                                'validate': 'person_name',
                            },
                            {
                                'name': 'dob',
                                'type': 'date',
                                'label': 'Date of Birth',
                                'required': False,
                                'validate': 'date_optional',
                            },
                            {
                                'name': 'relationship',
                                'type': 'text',
                                'label': 'Relationship',
                                'required': False,
                                'validate': 'optional_person_name',
                            },
                            {
                                'name': 'allocation',
                                'type': 'number',
                                'label': 'Allocation Percentage (%)',
                                'required': False,
                                'validate': 'percent_0_100',
                            },
                        ],
                    }
                ],
            }
        ],
    },
    {
        'key': 'assets_experience',
        'title': 'Assets & Investment Experience',
        'sections': [
            {
                'title': 'Asset Overview',
                'fields': [
                    {
                        'name': 'include_breakdown',
                        'type': 'checkbox',
                        'label': 'Include Asset Breakdown',
                        'required': False,
                    },
                    {
                        'name': 'outside_broker_assets',
                        'type': 'checkbox',
                        'label': 'Do you have assets with an outside broker firm?',
                        'required': False,
                    },
                ],
            },
            {
                'title': 'Investment Experience by Asset Type',
                'fields': [
                    {'name': 'label_stocks', 'type': 'label', 'label': 'Stocks'},
                    {
                        'name': 'stocks_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                        'validate': 'year_1900_current',
                    },
                    {
                        'name': 'stocks_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Moderate', 'Extensive'],
                    },
                    {'name': 'label_bonds', 'type': 'label', 'label': 'Bonds'},
                    {
                        'name': 'bonds_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                        'validate': 'year_1900_current',
                    },
                    {
                        'name': 'bonds_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Moderate', 'Extensive'],
                    },
                    {'name': 'label_mutual_funds', 'type': 'label', 'label': 'Mutual Funds'},
                    {
                        'name': 'mutual_funds_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                        'validate': 'year_1900_current',
                    },
                    {
                        'name': 'mutual_funds_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Moderate', 'Extensive'],
                    },
                    {'name': 'label_uits', 'type': 'label', 'label': 'UITs'},
                    {
                        'name': 'uits_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                        'validate': 'year_1900_current',
                    },
                    {
                        'name': 'uits_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Moderate', 'Extensive'],
                    },
                    {'name': 'label_annuities_fixed', 'type': 'label', 'label': 'Annuities (Fixed)'},
                    {
                        'name': 'annuities_fixed_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                        'validate': 'year_1900_current',
                    },
                    {
                        'name': 'annuities_fixed_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Moderate', 'Extensive'],
                    },
                    {'name': 'label_annuities_variable', 'type': 'label', 'label': 'Annuities (Variable)'},
                    {
                        'name': 'annuities_variable_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                        'validate': 'year_1900_current',
                    },
                    {
                        'name': 'annuities_variable_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Moderate', 'Extensive'],
                    },
                    {'name': 'label_options', 'type': 'label', 'label': 'Options'},
                    {
                        'name': 'options_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                        'validate': 'year_1900_current',
                    },
                    {
                        'name': 'options_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Moderate', 'Extensive'],
                    },
                    {'name': 'label_commodities', 'type': 'label', 'label': 'Commodities'},
                    {
                        'name': 'commodities_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                        'validate': 'year_1900_current',
                    },
                    {
                        'name': 'commodities_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Moderate', 'Extensive'],
                    },
                    {'name': 'label_alternative_investments', 'type': 'label', 'label': 'Alternative Investments'},
                    {
                        'name': 'alternative_investments_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                        'validate': 'year_1900_current',
                    },
                    {
                        'name': 'alternative_investments_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Moderate', 'Extensive'],
                    },
                    {'name': 'label_limited_partnerships', 'type': 'label', 'label': 'Limited Partnerships'},
                    {
                        'name': 'limited_partnerships_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                        'validate': 'year_1900_current',
                    },
                    {
                        'name': 'limited_partnerships_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Moderate', 'Extensive'],
                    },
                    {'name': 'label_variable_contracts', 'type': 'label', 'label': 'Variable Contracts'},
                    {
                        'name': 'variable_contracts_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                        'validate': 'year_1900_current',
                    },
                    {
                        'name': 'variable_contracts_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Moderate', 'Extensive'],
                    },
                ],
            },
        ],
    },
    {
        'key': 'trusted_contact',
        'title': 'Trusted Contact Person',
        'sections': [
            {
                'title': 'Trusted Contact Person',
                'fields': [
                    {
                        'name': 'tcp_full_name',
                        'type': 'text',
                        'label': 'Full Legal Name',
                        'required': False,
                        'validate': 'optional_person_name',
                    },
                    {
                        'name': 'tcp_relationship',
                        'type': 'text',
                        'label': 'Relationship to You',
                        'required': False,
                        'validate': 'optional_person_name',
                    },
                    {
                        'name': 'tcp_phone',
                        'type': 'text',
                        'label': 'Phone Number',
                        'required': False,
                        'validate': 'phone_us',
                        'input_mask': 'phone',
                    },
                    {
                        'name': 'tcp_email',
                        'type': 'text',
                        'label': 'Email Address',
                        'required': False,
                        'validate': 'email_basic',
                    },
                ],
            }
        ],
    },
    {
        'key': 'reg_consent',
        'title': 'Regulatory Consent',
        'sections': [
            {
                'title': 'Electronic Delivery',
                'fields': [
                    {
                        'name': 'ed_consent',
                        'type': 'radio',
                        'label': 'Do you consent to electronic delivery of documents?',
                        'required': True,
                        'options': ['Yes', 'No'],
                    }
                ],
            }
        ],
    },
    {
        'key': 'broker_dealer_relationships',
        'title': 'Broker-Dealer Relationships',
        'sections': [
            {
                'title': 'Associations',
                'fields': [
                    {
                        'name': 'employee_this_bd',
                        'type': 'radio',
                        'label': 'Employee of this Broker-Dealer?',
                        'required': True,
                        'options': ['Yes', 'No'],
                    },
                    {
                        'type': 'group',
                        'show_if': {'employee_this_bd': 'Yes'},
                        'fields': [
                            {
                                'name': 'employee_name',
                                'type': 'text',
                                'label': 'Employee Name',
                                'required': True,
                            },
                            {
                                'name': 'department',
                                'type': 'text',
                                'label': 'Department',
                                'required': False,
                            },
                            {
                                'name': 'branch',
                                'type': 'text',
                                'label': 'Branch',
                                'required': False,
                            },
                            {
                                'name': 'start_date',
                                'type': 'date',
                                'label': 'Start Date',
                                'required': True,
                                'validate': 'iso_date',
                            },
                        ],
                    },
                    {
                        'name': 'related_this_bd',
                        'type': 'radio',
                        'label': 'Related to an Employee of this Broker-Dealer?',
                        'required': True,
                        'options': ['Yes', 'No'],
                    },
                    {
                        'type': 'group',
                        'show_if': {'related_this_bd': 'Yes'},
                        'fields': [
                            {
                                'name': 'related_employee_name',
                                'type': 'text',
                                'label': 'Employee Name',
                                'required': True,
                            },
                            {
                                'name': 'relationship',
                                'type': 'select',
                                'label': 'Relationship',
                                'required': True,
                                'options': ['Spouse', 'Parent', 'Child', 'Sibling', 'Other'],
                            },
                            {
                                'name': 'branch_related',
                                'type': 'text',
                                'label': 'Branch',
                                'required': False,
                            },
                        ],
                    },
                    {
                        'name': 'employee_other_bd',
                        'type': 'radio',
                        'label': 'Employee of another Broker-Dealer?',
                        'required': True,
                        'options': ['Yes', 'No'],
                    },
                    {
                        'type': 'group',
                        'show_if': {'employee_other_bd': 'Yes'},
                        'fields': [
                            {
                                'name': 'firm_name_other',
                                'type': 'text',
                                'label': 'Firm Name',
                                'required': True,
                            },
                            {
                                'name': 'crd_other',
                                'type': 'text',
                                'label': 'CRD #',
                                'required': True,
                                'validate': 'crd',
                            },
                            {
                                'name': 'role_other',
                                'type': 'text',
                                'label': 'Role',
                                'required': False,
                            },
                            {
                                'name': 'start_date_other',
                                'type': 'date',
                                'label': 'Start Date',
                                'required': False,
                                'validate': 'iso_date',
                            },
                        ],
                    },
                    {
                        'name': 'related_other_bd',
                        'type': 'radio',
                        'label': 'Related to an employee of another Broker-Dealer?',
                        'required': True,
                        'options': ['Yes', 'No'],
                    },
                    {
                        'type': 'group',
                        'show_if': {'related_other_bd': 'Yes'},
                        'fields': [
                            {
                                'name': 'firm_name_rel',
                                'type': 'text',
                                'label': 'Firm Name',
                                'required': True,
                            },
                            {
                                'name': 'employee_name_rel',
                                'type': 'text',
                                'label': 'Employee Name',
                                'required': True,
                            },
                            {
                                'name': 'relationship_rel',
                                'type': 'select',
                                'label': 'Relationship',
                                'required': True,
                                'options': ['Spouse', 'Parent', 'Child', 'Sibling', 'Other'],
                            },
                        ],
                    },
                ],
            }
        ],
    },
    {
        'key': 'reg_affiliations',
        'title': 'Regulatory Affiliations',
        'sections': [
            {
                'title': 'SRO Membership & Control Persons',
                'fields': [
                    {
                        'name': 'sro_member',
                        'type': 'radio',
                        'label': 'Member of Stk Exch./FINRA?',
                        'required': True,
                        'options': ['Yes', 'No'],
                    },
                    {
                        'type': 'group',
                        'show_if': {'sro_member': 'Yes'},
                        'fields': [
                            {
                                'name': 'membership_type',
                                'type': 'select',
                                'label': 'Membership Type',
                                'required': True,
                                'options': ['FINRA', 'NYSE', 'NASDAQ', 'Other'],
                            },
                            {
                                'name': 'sro_crd',
                                'type': 'text',
                                'label': 'CRD #',
                                'required': False,
                                'validate': 'crd',
                            },
                            {
                                'name': 'sro_branch',
                                'type': 'text',
                                'label': 'Branch',
                                'required': False,
                            },
                        ],
                    },
                    {
                        'name': 'control_person',
                        'type': 'radio',
                        'label': 'Are you a senior officer, director, or 10% or more shareholder of a public company?',
                        'required': True,
                        'options': ['Yes', 'No'],
                    },
                    {
                        'type': 'group',
                        'show_if': {'control_person': 'Yes'},
                        'fields': [
                            {
                                'name': 'company_name',
                                'type': 'text',
                                'label': 'Company Name',
                                'required': True,
                            },
                            {
                                'name': 'ticker',
                                'type': 'text',
                                'label': 'Ticker',
                                'required': False,
                                'validate': 'ticker',
                            },
                            {
                                'name': 'exchange',
                                'type': 'select',
                                'label': 'Exchange',
                                'required': False,
                                'options': ['NYSE', 'NASDAQ', 'AMEX', 'Other'],
                            },
                            {
                                'name': 'role',
                                'type': 'text',
                                'label': 'Role',
                                'required': False,
                            },
                            {
                                'name': 'ownership_pct',
                                'type': 'number',
                                'label': 'Ownership %',
                                'required': False,
                                'validate': 'pct_0_100_two_dec',
                            },
                            {
                                'name': 'as_of',
                                'type': 'date',
                                'label': 'As Of',
                                'required': False,
                                'validate': 'iso_date',
                            },
                        ],
                    },
                ],
            }
        ],
    },
    {
        'key': 'foreign_accounts',
        'title': 'Foreign Financial Accounts',
        'sections': [
            {
                'title': 'FFI / Private Banking',
                'fields': [
                    {
                        'name': 'has_ffi',
                        'type': 'radio',
                        'label': 'Foreign Financial Institution Account?',
                        'required': True,
                        'options': ['Yes', 'No'],
                    },
                    {
                        'type': 'group',
                        'show_if': {'has_ffi': 'Yes'},
                        'fields': [
                            {
                                'name': 'institution_name',
                                'type': 'text',
                                'label': 'Institution Name',
                                'required': True,
                            },
                            {
                                'name': 'country',
                                'type': 'select',
                                'label': 'Country',
                                'required': True,
                                'options': 'ISO_COUNTRIES',
                            },
                            {
                                'name': 'purpose',
                                'type': 'select',
                                'label': 'Purpose',
                                'required': True,
                                'options': ['Savings', 'Brokerage', 'Payments', 'Other'],
                            },
                            {
                                'name': 'source_of_funds',
                                'type': 'textarea',
                                'label': 'Source of Funds',
                                'required': False,
                            },
                            {
                                'name': 'open_date',
                                'type': 'date',
                                'label': 'Open Date',
                                'required': False,
                                'validate': 'iso_date',
                            },
                            {
                                'name': 'private_banking',
                                'type': 'radio',
                                'label': 'Is this a private banking account?',
                                'required': False,
                                'options': ['Yes', 'No'],
                            },
                            {
                                'name': 'foreign_bank_acct',
                                'type': 'radio',
                                'label': 'Is this an account for a Foreign Bank?',
                                'required': False,
                                'options': ['Yes', 'No'],
                            },
                        ],
                    },
                ],
            }
        ],
    },
    {
        'key': 'pep',
        'title': 'Politically Exposed Person (PEP)',
        'sections': [
            {
                'title': 'PEP Screening',
                'fields': [
                    {
                        'name': 'is_pep',
                        'type': 'radio',
                        'label': 'Politically Exposed Person?',
                        'required': True,
                        'options': ['Yes', 'No'],
                    },
                    {
                        'type': 'group',
                        'show_if': {'is_pep': 'Yes'},
                        'fields': [
                            {
                                'name': 'pep_name',
                                'type': 'text',
                                'label': 'PEP Name',
                                'required': True,
                            },
                            {
                                'name': 'pep_country',
                                'type': 'select',
                                'label': 'Country',
                                'required': True,
                                'options': 'ISO_COUNTRIES',
                            },
                            {
                                'name': 'pep_relationship',
                                'type': 'select',
                                'label': 'Relationship',
                                'required': True,
                                'options': ['Self', 'Family', 'Associate'],
                            },
                            {
                                'name': 'pep_title',
                                'type': 'text',
                                'label': 'Title',
                                'required': False,
                            },
                            {
                                'name': 'pep_start',
                                'type': 'date',
                                'label': 'Start Date',
                                'required': False,
                                'validate': 'iso_date',
                            },
                            {
                                'name': 'pep_end',
                                'type': 'date',
                                'label': 'End Date',
                                'required': False,
                                'validate': 'iso_date>=pep_start',
                            },
                            {
                                'name': 'pep_screening_consent',
                                'type': 'checkbox',
                                'label': 'I consent to screening',
                                'required': True,
                            },
                        ],
                    },
                ],
            }
        ],
    },
]
