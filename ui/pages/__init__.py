from .welcome import create_page as welcome_page
from .personal_info import create_page as personal_info_page
from .contact_info import create_page as contact_info_page
from .employment_info import create_page as employment_info_page
from .financial_info import create_page as financial_info_page
from .spouse_info import create_page as spouse_info_page
from .dependents import create_page as dependents_page
from .beneficiaries import create_page as beneficiaries_page
from .assets_investment import create_page as assets_investment_page
from .trusted_contact import create_page as trusted_contact_page
from .regulatory import create_page as regulatory_page
from .review_submit import create_page as review_submit_page

PAGE_CREATORS = [
    welcome_page,
    personal_info_page,
    contact_info_page,
    employment_info_page,
    financial_info_page,
    spouse_info_page,
    dependents_page,
    beneficiaries_page,
    assets_investment_page,
    trusted_contact_page,
    regulatory_page,
    review_submit_page,
]
