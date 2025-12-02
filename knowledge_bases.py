"""
Domain-Specific Knowledge Bases
Glossaries, ontologies, and terminology mappings for each sector

Includes:
  - Field name mappings across variations
  - Domain-specific terminology
  - Common abbreviations and expansions
  - Validation rules
  - Relationship mappings
"""

from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from enum import Enum


@dataclass
class TermMapping:
    """Represents a term mapping in a domain"""
    canonical_form: str
    aliases: List[str]
    category: str
    abbreviations: List[str]
    description: str
    examples: List[str]


class DomainKnowledgeBase:
    """Base class for domain knowledge bases"""
    
    def __init__(self, domain_name: str):
        self.domain_name = domain_name
        self.glossary = {}
        self.relationships = {}
        self.validation_rules = {}
        self.field_mappings = {}
    
    def normalize_term(self, term: str) -> Optional[str]:
        """Normalize a term to its canonical form"""
        term_lower = term.lower().strip()
        
        for canonical, mapping in self.glossary.items():
            if term_lower == canonical.lower():
                return canonical
            if term_lower in [alias.lower() for alias in mapping.aliases]:
                return canonical
            if term_lower in [abbr.lower() for abbr in mapping.abbreviations]:
                return canonical
        
        return None
    
    def get_related_terms(self, term: str) -> Set[str]:
        """Get all terms related to the given term"""
        canonical = self.normalize_term(term)
        if not canonical:
            return set()
        
        related = set()
        if canonical in self.glossary:
            related.add(canonical)
            related.update(self.glossary[canonical].aliases)
            related.update(self.glossary[canonical].abbreviations)
        
        if canonical in self.relationships:
            related.update(self.relationships[canonical])
        
        return related
    
    def validate_field_value(self, field_name: str, value: str) -> bool:
        """Validate a field value against domain rules"""
        if field_name not in self.validation_rules:
            return True  # No specific rule
        
        rule = self.validation_rules[field_name]
        return rule(value)


class RealEstateKB(DomainKnowledgeBase):
    """Real Estate domain knowledge base"""
    
    def __init__(self):
        super().__init__("real_estate")
        self._initialize()
    
    def _initialize(self):
        # Glossary for real estate terms
        self.glossary = {
            "Property Address": TermMapping(
                canonical_form="Property Address",
                aliases=["address", "property location", "real estate location", "premises"],
                category="property",
                abbreviations=["addr"],
                description="The physical location of the property",
                examples=["123 Main St, Nashville, TN 37201"]
            ),
            "Deed Book": TermMapping(
                canonical_form="Deed Book",
                aliases=["book number", "deed reference", "recording book"],
                category="recording",
                abbreviations=["book"],
                description="Reference to deed recording book",
                examples=["Book 5432"]
            ),
            "Page Number": TermMapping(
                canonical_form="Page Number",
                aliases=["page", "recording page"],
                category="recording",
                abbreviations=["pg", "p"],
                description="Page number in deed recording",
                examples=["Page 234"]
            ),
            "Legal Description": TermMapping(
                canonical_form="Legal Description",
                aliases=["legal description", "property description", "land description"],
                category="property",
                abbreviations=["legal desc"],
                description="Official legal description of the property",
                examples=["Lot 5, Block 2, Green Hills Subdivision"]
            ),
            "Grantor": TermMapping(
                canonical_form="Grantor",
                aliases=["seller", "conveyor", "donor"],
                category="party",
                abbreviations=["gr"],
                description="The party transferring the property",
                examples=["John Smith"]
            ),
            "Grantee": TermMapping(
                canonical_form="Grantee",
                aliases=["buyer", "purchaser", "recipient"],
                category="party",
                abbreviations=["ee"],
                description="The party receiving the property",
                examples=["Jane Doe"]
            ),
            "Purchase Price": TermMapping(
                canonical_form="Purchase Price",
                aliases=["sale price", "consideration", "price"],
                category="financial",
                abbreviations=["price"],
                description="Amount paid for the property",
                examples=["$250,000"]
            ),
            "Closing Date": TermMapping(
                canonical_form="Closing Date",
                aliases=["settlement date", "closing", "date of closing"],
                category="transaction",
                abbreviations=["close date"],
                description="Date the transaction closes",
                examples=["January 15, 2024"]
            ),
            "Title Company": TermMapping(
                canonical_form="Title Company",
                aliases=["title agent", "closing agent", "title insurer"],
                category="service",
                abbreviations=["title co"],
                description="Entity providing title services",
                examples=["First National Title Company"]
            ),
        }
        
        # Relationships between real estate concepts
        self.relationships = {
            "Deed Book": ["Page Number", "Legal Description", "Recording Date"],
            "Grantor": ["Grantee", "Property Address"],
            "Grantee": ["Grantor", "Purchase Price"],
            "Purchase Price": ["Financing", "Closing Date"],
            "Property Address": ["Legal Description", "Deed Book"]
        }
        
        # Validation rules
        self.validation_rules = {
            "Purchase Price": lambda v: v.startswith("$") or any(c.isdigit() for c in v),
            "Closing Date": lambda v: any(m in v for m in [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December",
                "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"
            ]),
            "Deed Book": lambda v: "book" in v.lower() or any(c.isdigit() for c in v),
        }
        
        # Field mappings for common variations
        self.field_mappings = {
            "seller name": "Grantor",
            "buyer name": "Grantee",
            "property location": "Property Address",
            "recording reference": "Deed Book",
            "transaction amount": "Purchase Price"
        }


class MedicalKB(DomainKnowledgeBase):
    """Medical/Healthcare domain knowledge base"""
    
    def __init__(self):
        super().__init__("medical")
        self._initialize()
    
    def _initialize(self):
        self.glossary = {
            "Patient Name": TermMapping(
                canonical_form="Patient Name",
                aliases=["patient", "name", "patient identifier"],
                category="demographic",
                abbreviations=["pt name"],
                description="Name of the patient",
                examples=["John Smith"]
            ),
            "Date of Birth": TermMapping(
                canonical_form="Date of Birth",
                aliases=["birth date", "DOB", "birthday"],
                category="demographic",
                abbreviations=["DOB", "dob"],
                description="Patient's date of birth",
                examples=["01/15/1980"]
            ),
            "Diagnosis": TermMapping(
                canonical_form="Diagnosis",
                aliases=["diagnosis code", "condition", "ICD code"],
                category="clinical",
                abbreviations=["dx"],
                description="Medical diagnosis code or description",
                examples=["I10 - Essential hypertension"]
            ),
            "Medication": TermMapping(
                canonical_form="Medication",
                aliases=["drug", "prescription", "medicine"],
                category="treatment",
                abbreviations=["med", "rx"],
                description="Prescribed medication",
                examples=["Lisinopril 10mg"]
            ),
            "Allergy": TermMapping(
                canonical_form="Allergy",
                aliases=["allergies", "adverse reaction", "intolerance"],
                category="safety",
                abbreviations=["allergy"],
                description="Known allergies",
                examples=["Penicillin, Peanuts"]
            ),
            "Provider": TermMapping(
                canonical_form="Provider",
                aliases=["physician", "doctor", "nurse"],
                category="personnel",
                abbreviations=["MD", "RN"],
                description="Healthcare provider name",
                examples=["Dr. Jane Smith, MD"]
            ),
            "Insurance ID": TermMapping(
                canonical_form="Insurance ID",
                aliases=["policy number", "member ID", "group number"],
                category="insurance",
                abbreviations=["ID"],
                description="Insurance policy or member ID",
                examples=["ABC123456"]
            ),
        }
        
        # Medical abbreviation mappings
        self.abbreviations_map = {
            "HTN": "Hypertension",
            "DM": "Diabetes Mellitus",
            "CHF": "Congestive Heart Failure",
            "CAD": "Coronary Artery Disease",
            "COPD": "Chronic Obstructive Pulmonary Disease",
            "MI": "Myocardial Infarction",
            "CVA": "Cerebrovascular Accident",
            "PE": "Pulmonary Embolism",
            "DVT": "Deep Vein Thrombosis",
            "UTI": "Urinary Tract Infection"
        }
        
        # Relationships
        self.relationships = {
            "Patient Name": ["Date of Birth", "Diagnosis", "Allergy"],
            "Diagnosis": ["Medication", "Provider"],
            "Medication": ["Allergy", "Dosage"],
            "Provider": ["Insurance ID"]
        }
        
        # Validation rules for medical data
        self.validation_rules = {
            "Date of Birth": lambda v: any(sep in v for sep in ["/", "-"]),
            "Diagnosis": lambda v: len(v) > 2,
            "Medication": lambda v: len(v) > 2,
        }


class InsuranceKB(DomainKnowledgeBase):
    """Insurance domain knowledge base"""
    
    def __init__(self):
        super().__init__("insurance")
        self._initialize()
    
    def _initialize(self):
        self.glossary = {
            "Policy Number": TermMapping(
                canonical_form="Policy Number",
                aliases=["policy", "policy ID", "contract number"],
                category="policy",
                abbreviations=["pol", "policy #"],
                description="Unique insurance policy identifier",
                examples=["POL-2024-001234"]
            ),
            "Policyholder": TermMapping(
                canonical_form="Policyholder",
                aliases=["insured", "primary insured", "named insured"],
                category="party",
                abbreviations=["ph"],
                description="Person or entity holding the policy",
                examples=["John Smith"]
            ),
            "Beneficiary": TermMapping(
                canonical_form="Beneficiary",
                aliases=["beneficiaries", "dependent", "named beneficiary"],
                category="party",
                abbreviations=["ben"],
                description="Designated recipient of policy benefits",
                examples=["Jane Smith"]
            ),
            "Coverage Limit": TermMapping(
                canonical_form="Coverage Limit",
                aliases=["limit", "coverage amount", "benefit maximum"],
                category="financial",
                abbreviations=["limit"],
                description="Maximum amount insurer will pay",
                examples=["$500,000"]
            ),
            "Premium": TermMapping(
                canonical_form="Premium",
                aliases=["payment", "monthly payment", "annual premium"],
                category="financial",
                abbreviations=["prem"],
                description="Amount paid for insurance",
                examples=["$1,250/month"]
            ),
            "Deductible": TermMapping(
                canonical_form="Deductible",
                aliases=["out of pocket", "deductable"],
                category="financial",
                abbreviations=["ded"],
                description="Amount insured pays before coverage starts",
                examples=["$1,000"]
            ),
            "Effective Date": TermMapping(
                canonical_form="Effective Date",
                aliases=["start date", "policy start"],
                category="temporal",
                abbreviations=["eff date"],
                description="Date policy becomes active",
                examples=["January 1, 2024"]
            ),
        }
        
        self.relationships = {
            "Policy Number": ["Policyholder", "Beneficiary", "Effective Date"],
            "Policyholder": ["Beneficiary", "Coverage Limit"],
            "Coverage Limit": ["Premium", "Deductible"]
        }
        
        self.validation_rules = {
            "Policy Number": lambda v: len(v) > 3,
            "Coverage Limit": lambda v: any(c.isdigit() for c in v),
            "Premium": lambda v: any(c.isdigit() for c in v),
        }


class FinanceKB(DomainKnowledgeBase):
    """Finance/Accounting domain knowledge base"""
    
    def __init__(self):
        super().__init__("finance")
        self._initialize()
    
    def _initialize(self):
        self.glossary = {
            "Revenue": TermMapping(
                canonical_form="Revenue",
                aliases=["sales", "income", "proceeds"],
                category="financial",
                abbreviations=["rev"],
                description="Total income from business operations",
                examples=["$1,000,000"]
            ),
            "Expense": TermMapping(
                canonical_form="Expense",
                aliases=["cost", "expenditure", "outflow"],
                category="financial",
                abbreviations=["exp"],
                description="Costs of doing business",
                examples=["$500,000"]
            ),
            "Net Income": TermMapping(
                canonical_form="Net Income",
                aliases=["profit", "earnings", "bottom line"],
                category="financial",
                abbreviations=["NI"],
                description="Revenue minus expenses",
                examples=["$500,000"]
            ),
            "Account Number": TermMapping(
                canonical_form="Account Number",
                aliases=["GL account", "account code"],
                category="accounting",
                abbreviations=["acct"],
                description="General ledger account identifier",
                examples=["4000-001"]
            ),
            "Tax Amount": TermMapping(
                canonical_form="Tax Amount",
                aliases=["taxes", "tax liability"],
                category="tax",
                abbreviations=["tax"],
                description="Tax liability",
                examples=["$100,000"]
            ),
        }
        
        self.relationships = {
            "Revenue": ["Expense", "Net Income"],
            "Expense": ["Net Income", "Account Number"],
            "Net Income": ["Tax Amount"]
        }


class LegalKB(DomainKnowledgeBase):
    """Legal/Contract domain knowledge base"""
    
    def __init__(self):
        super().__init__("legal")
        self._initialize()
    
    def _initialize(self):
        self.glossary = {
            "Party": TermMapping(
                canonical_form="Party",
                aliases=["parties", "contracting party", "entity"],
                category="legal",
                abbreviations=["party"],
                description="Entity entering into contract",
                examples=["John Smith"]
            ),
            "Consideration": TermMapping(
                canonical_form="Consideration",
                aliases=["payment", "benefit", "exchange"],
                category="legal",
                abbreviations=["consid"],
                description="Something of value exchanged",
                examples=["$10,000"]
            ),
            "Effective Date": TermMapping(
                canonical_form="Effective Date",
                aliases=["start date", "commencement date"],
                category="temporal",
                abbreviations=["eff date"],
                description="Date contract becomes effective",
                examples=["January 1, 2024"]
            ),
            "Termination Clause": TermMapping(
                canonical_form="Termination Clause",
                aliases=["termination", "end date", "expiration"],
                category="legal",
                abbreviations=["term"],
                description="Conditions for ending the contract",
                examples=["Either party may terminate with 30 days notice"]
            ),
            "Liability": TermMapping(
                canonical_form="Liability",
                aliases=["indemnification", "responsibility", "obligation"],
                category="legal",
                abbreviations=["liab"],
                description="Legal obligation or responsibility",
                examples=["Each party is liable for their own negligence"]
            ),
        }
        
        self.relationships = {
            "Party": ["Consideration", "Effective Date", "Liability"],
            "Consideration": ["Termination Clause"],
        }


# Registry of all knowledge bases
KNOWLEDGE_BASES = {
    "real_estate": RealEstateKB,
    "medical": MedicalKB,
    "insurance": InsuranceKB,
    "finance": FinanceKB,
    "legal": LegalKB,
}


def get_knowledge_base(domain: str) -> Optional[DomainKnowledgeBase]:
    """Get or create a knowledge base for a domain"""
    kb_class = KNOWLEDGE_BASES.get(domain.lower())
    if kb_class:
        return kb_class()
    return None


def list_available_domains() -> List[str]:
    """List all available domains"""
    return list(KNOWLEDGE_BASES.keys())


# Example usage
if __name__ == "__main__":
    print("Available Knowledge Bases:")
    for domain in list_available_domains():
        print(f"  • {domain}")
        kb = get_knowledge_base(domain)
        print(f"    - {len(kb.glossary)} terms")
        print(f"    - {len(kb.relationships)} relationships")
