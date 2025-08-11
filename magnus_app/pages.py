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
                    },
                    {
                        'name': 'dob',
                        'type': 'date',
                        'label': 'Date of Birth',
                        'required': True,
                    },
                    {
                        'name': 'ssn',
                        'type': 'text',
                        'label': 'Social Security Number',
                        'required': False,
                    },
                    {
                        'name': 'citizenship_status',
                        'type': 'select',
                        'label': 'Citizenship Status',
                        'required': False,
                        'options': ['U.S. Citizen', 'Resident Alien', 'Non-Resident Alien'],
                    },
                    {
                        'name': 'marital_status',
                        'type': 'select',
                        'label': 'Marital Status',
                        'required': False,
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
                    },
                    {
                        'name': 'phone_home',
                        'type': 'text',
                        'label': 'Home Phone',
                        'required': False,
                    },
                    {
                        'name': 'phone_mobile',
                        'type': 'text',
                        'label': 'Mobile Phone',
                        'required': False,
                    },
                    {
                        'name': 'phone_work',
                        'type': 'text',
                        'label': 'Work Phone',
                        'required': False,
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
                        'required': False,
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
                        'name': 'education',
                        'type': 'select',
                        'label': 'Education Status',
                        'required': False,
                        'options': ['High School', 'Some College', "Bachelor's", "Master's", 'Doctorate', 'Other'],
                    },
                    {
                        'name': 'tax_bracket',
                        'type': 'text',
                        'label': 'Estimated Tax Bracket',
                        'required': False,
                    },
                    {
                        'name': 'risk_tolerance',
                        'type': 'select',
                        'label': 'Investment Risk Tolerance',
                        'required': False,
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
                        'name': 'obj_trading_profits_rank',
                        'type': 'number',
                        'label': 'Trading Profits',
                        'required': False,
                    },
                    {
                        'name': 'obj_speculation_rank',
                        'type': 'number',
                        'label': 'Speculation',
                        'required': False,
                    },
                    {
                        'name': 'obj_capital_app_rank',
                        'type': 'number',
                        'label': 'Capital Appreciation',
                        'required': False,
                    },
                    {
                        'name': 'obj_income_rank',
                        'type': 'number',
                        'label': 'Income',
                        'required': False,
                    },
                    {
                        'name': 'obj_preservation_rank',
                        'type': 'number',
                        'label': 'Preservation of Capital',
                        'required': False,
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
                    },
                    {
                        'name': 'est_liquid_net_worth',
                        'type': 'text',
                        'label': 'Estimated Liquid Net Worth (cash + marketable securities)',
                        'required': False,
                    },
                    {
                        'name': 'assets_held_away',
                        'type': 'text',
                        'label': 'Assets Held Away (e.g., Brokerage Accounts, 401k, etc.)',
                        'required': False,
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
                            },
                            {
                                'name': 'spouse_dob',
                                'type': 'date',
                                'label': 'Date of Birth',
                                'required': False,
                                'validate': 'iso_date',
                            },
                            {
                                'name': 'spouse_ssn',
                                'type': 'text',
                                'label': 'Social Security Number',
                                'required': False,
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
                        'type': 'group',
                        'name': 'dependent_block',
                        'show_if': {'dependent_block': ''},
                        'fields': [
                            {
                                'name': 'dep_full_name',
                                'type': 'text',
                                'label': 'Dependent Full Name',
                                'required': False,
                            },
                            {
                                'name': 'dep_dob',
                                'type': 'date',
                                'label': 'Dependent Date of Birth',
                                'required': False,
                            },
                            {
                                'name': 'dep_relationship',
                                'type': 'text',
                                'label': 'Relationship',
                                'required': False,
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
                        'type': 'group',
                        'name': 'beneficiary_block',
                        'show_if': {'beneficiary_block': ''},
                        'fields': [
                            {
                                'name': 'ben_full_name',
                                'type': 'text',
                                'label': 'Beneficiary Full Name',
                                'required': False,
                            },
                            {
                                'name': 'ben_dob',
                                'type': 'date',
                                'label': 'Beneficiary Date of Birth',
                                'required': False,
                            },
                            {
                                'name': 'ben_relationship',
                                'type': 'text',
                                'label': 'Relationship',
                                'required': False,
                            },
                            {
                                'name': 'ben_allocation_pct',
                                'type': 'number',
                                'label': 'Allocation Percentage (%)',
                                'required': False,
                                'validate': 'pct_0_100_two_dec',
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
                    {
                        'name': 'stocks_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                    },
                    {
                        'name': 'stocks_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Good', 'Extensive'],
                    },
                    {
                        'name': 'bonds_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                    },
                    {
                        'name': 'bonds_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Good', 'Extensive'],
                    },
                    {
                        'name': 'mutual_funds_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                    },
                    {
                        'name': 'mutual_funds_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Good', 'Extensive'],
                    },
                    {
                        'name': 'uits_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                    },
                    {
                        'name': 'uits_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Good', 'Extensive'],
                    },
                    {
                        'name': 'annuities_fixed_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                    },
                    {
                        'name': 'annuities_fixed_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Good', 'Extensive'],
                    },
                    {
                        'name': 'annuities_variable_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                    },
                    {
                        'name': 'annuities_variable_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Good', 'Extensive'],
                    },
                    {
                        'name': 'options_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                    },
                    {
                        'name': 'options_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Good', 'Extensive'],
                    },
                    {
                        'name': 'commodities_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                    },
                    {
                        'name': 'commodities_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Good', 'Extensive'],
                    },
                    {
                        'name': 'alternative_investments_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                    },
                    {
                        'name': 'alternative_investments_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Good', 'Extensive'],
                    },
                    {
                        'name': 'limited_partnerships_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                    },
                    {
                        'name': 'limited_partnerships_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Good', 'Extensive'],
                    },
                    {
                        'name': 'variable_contracts_year_started',
                        'type': 'text',
                        'label': 'Year Started',
                        'required': False,
                    },
                    {
                        'name': 'variable_contracts_level',
                        'type': 'select',
                        'label': 'Level',
                        'required': False,
                        'options': ['None', 'Limited', 'Good', 'Extensive'],
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
                    },
                    {
                        'name': 'tcp_relationship',
                        'type': 'text',
                        'label': 'Relationship to You',
                        'required': False,
                    },
                    {
                        'name': 'tcp_phone',
                        'type': 'text',
                        'label': 'Phone Number',
                        'required': False,
                    },
                    {
                        'name': 'tcp_email',
                        'type': 'text',
                        'label': 'Email Address',
                        'required': False,
                    },
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
