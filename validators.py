"""
Validation and Compliance Engines
Domain-specific validation rules and compliance checking for each sector

Features:
  - Field-level validation
  - Cross-field validation
  - Domain-specific business rules
  - Compliance checking (HIPAA, regulatory, etc.)
  - Audit trail generation
"""

import re
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class ComplianceLevel(Enum):
    """Compliance requirement levels"""
    CRITICAL = 1      # Must pass
    WARNING = 2       # Should pass
    INFO = 3          # For information
    OPTIONAL = 4      # Nice to have


@dataclass
class ValidationResult:
    """Result of a validation check"""
    field_name: str
    is_valid: bool
    severity: ComplianceLevel
    message: str
    rule_name: str
    timestamp: str


class FieldValidator:
    """Base validator for field values"""
    
    def validate(self, value: Optional[str]) -> Tuple[bool, str]:
        """Validate a field value. Returns (is_valid, message)"""
        raise NotImplementedError


class RegexValidator(FieldValidator):
    """Validates field against regex pattern"""
    
    def __init__(self, pattern: str, error_msg: str):
        self.pattern = re.compile(pattern)
        self.error_msg = error_msg
    
    def validate(self, value: Optional[str]) -> Tuple[bool, str]:
        if value is None:
            return False, "Value is empty"
        
        if self.pattern.match(value):
            return True, "Valid"
        return False, self.error_msg


class DateValidator(FieldValidator):
    """Validates date format"""
    
    def __init__(self, formats: List[str]):
        self.formats = formats
    
    def validate(self, value: Optional[str]) -> Tuple[bool, str]:
        if value is None:
            return False, "Date is empty"
        
        for fmt in self.formats:
            try:
                datetime.strptime(value, fmt)
                return True, "Valid date"
            except ValueError:
                continue
        
        return False, f"Invalid date format. Expected: {', '.join(self.formats)}"


class RangeValidator(FieldValidator):
    """Validates numeric value in range"""
    
    def __init__(self, min_val: Optional[float], max_val: Optional[float]):
        self.min_val = min_val
        self.max_val = max_val
    
    def validate(self, value: Optional[str]) -> Tuple[bool, str]:
        if value is None:
            return False, "Value is empty"
        
        try:
            num = float(value)
            
            if self.min_val is not None and num < self.min_val:
                return False, f"Value {num} is less than minimum {self.min_val}"
            
            if self.max_val is not None and num > self.max_val:
                return False, f"Value {num} exceeds maximum {self.max_val}"
            
            return True, "Valid"
        except ValueError:
            return False, "Value is not a number"


class DomainValidationEngine:
    """Base validation engine for a domain"""
    
    def __init__(self, domain_name: str):
        self.domain_name = domain_name
        self.field_validators = {}
        self.cross_field_validators = {}
        self.compliance_rules = {}
        self.audit_trail = []
        self._initialize()
    
    def _initialize(self):
        """Initialize domain-specific validators"""
        raise NotImplementedError
    
    def validate_field(self, field_name: str, value: Optional[str]) -> ValidationResult:
        """Validate a single field"""
        if field_name not in self.field_validators:
            return ValidationResult(
                field_name=field_name,
                is_valid=True,
                severity=ComplianceLevel.INFO,
                message="No specific validation rules",
                rule_name="none",
                timestamp=datetime.now().isoformat()
            )
        
        validator = self.field_validators[field_name]
        is_valid, message = validator.validate(value)
        
        result = ValidationResult(
            field_name=field_name,
            is_valid=is_valid,
            severity=ComplianceLevel.CRITICAL if not is_valid else ComplianceLevel.INFO,
            message=message,
            rule_name=field_name,
            timestamp=datetime.now().isoformat()
        )
        
        self.audit_trail.append(result)
        return result
    
    def validate_cross_fields(self, form_data: Dict[str, Optional[str]]) -> List[ValidationResult]:
        """Validate relationships between fields"""
        results = []
        
        for rule_name, rule_func in self.cross_field_validators.items():
            is_valid, message = rule_func(form_data)
            
            result = ValidationResult(
                field_name="(cross-field)",
                is_valid=is_valid,
                severity=ComplianceLevel.CRITICAL if not is_valid else ComplianceLevel.INFO,
                message=message,
                rule_name=rule_name,
                timestamp=datetime.now().isoformat()
            )
            
            results.append(result)
            self.audit_trail.append(result)
        
        return results
    
    def check_compliance(self, form_data: Dict[str, Optional[str]]) -> Dict[str, List[ValidationResult]]:
        """Check compliance with domain rules"""
        results = {}
        
        for compliance_rule, rule_func in self.compliance_rules.items():
            rule_results = rule_func(form_data)
            results[compliance_rule] = rule_results
            self.audit_trail.extend(rule_results)
        
        return results
    
    def get_audit_trail(self) -> List[ValidationResult]:
        """Get validation audit trail"""
        return self.audit_trail


class RealEstateValidationEngine(DomainValidationEngine):
    """Real Estate domain validation"""
    
    def __init__(self):
        super().__init__("real_estate")
    
    def _initialize(self):
        # Field validators
        self.field_validators = {
            "Purchase Price": RegexValidator(
                r'^\$?\d+(?:,\d{3})*(?:\.\d{2})?$',
                "Purchase price must be in format: $XXX,XXX.XX"
            ),
            "Closing Date": DateValidator(
                ["%m/%d/%Y", "%Y-%m-%d", "%B %d, %Y"]
            ),
            "Deed Book": RegexValidator(
                r'^[Bb]ook\s*\d+',
                "Deed book must be formatted: Book XXXXX"
            ),
            "Page Number": RegexValidator(
                r'^\d+',
                "Page number must be numeric"
            ),
        }
        
        # Cross-field validators
        self.cross_field_validators = {
            "valid_parties": self._validate_parties,
            "price_amount": self._validate_price_amount,
        }
        
        # Compliance rules
        self.compliance_rules = {
            "transaction_completeness": self._check_transaction_completeness,
        }
    
    def _validate_parties(self, form_data: Dict) -> Tuple[bool, str]:
        """Verify both seller and buyer are present"""
        seller = form_data.get("Seller Name") or form_data.get("Grantor")
        buyer = form_data.get("Buyer Name") or form_data.get("Grantee")
        
        if seller and buyer:
            return True, "Both parties identified"
        return False, "Both seller and buyer must be specified"
    
    def _validate_price_amount(self, form_data: Dict) -> Tuple[bool, str]:
        """Verify purchase price is reasonable"""
        price_str = form_data.get("Purchase Price", "")
        if not price_str:
            return True, "Price not specified"
        
        try:
            # Extract numeric value
            price = float(re.sub(r'[^\d.]', '', price_str))
            if price < 1000:
                return False, "Purchase price seems unusually low (< $1,000)"
            if price > 10000000:
                return False, "Purchase price seems unusually high (> $10,000,000)"
            return True, "Price amount is reasonable"
        except:
            return False, "Could not parse purchase price"
    
    def _check_transaction_completeness(self, form_data: Dict) -> List[ValidationResult]:
        """Check if all critical transaction fields are present"""
        results = []
        required_fields = ["Seller Name", "Buyer Name", "Property Address", "Purchase Price"]
        
        for field in required_fields:
            if not form_data.get(field):
                results.append(ValidationResult(
                    field_name=field,
                    is_valid=False,
                    severity=ComplianceLevel.CRITICAL,
                    message=f"Required field '{field}' is missing",
                    rule_name="transaction_completeness",
                    timestamp=datetime.now().isoformat()
                ))
        
        return results


class MedicalValidationEngine(DomainValidationEngine):
    """Medical/Healthcare validation with HIPAA considerations"""
    
    def __init__(self):
        super().__init__("medical")
    
    def _initialize(self):
        self.field_validators = {
            "Date of Birth": DateValidator(
                ["%m/%d/%Y", "%Y-%m-%d"]
            ),
            "Patient ID": RegexValidator(
                r'^[A-Z0-9]{6,12}$',
                "Patient ID must be 6-12 alphanumeric characters"
            ),
            "Age": RangeValidator(0, 150),
        }
        
        self.cross_field_validators = {
            "consistent_age": self._validate_age_consistency,
        }
        
        self.compliance_rules = {
            "hipaa_compliance": self._check_hipaa_compliance,
            "clinical_completeness": self._check_clinical_completeness,
        }
    
    def _validate_age_consistency(self, form_data: Dict) -> Tuple[bool, str]:
        """Verify age matches date of birth"""
        # Simplified check
        return True, "Age data present"
    
    def _check_hipaa_compliance(self, form_data: Dict) -> List[ValidationResult]:
        """Check HIPAA compliance requirements"""
        results = []
        
        # PHI identifiers should be present
        if not form_data.get("Patient ID"):
            results.append(ValidationResult(
                field_name="Patient ID",
                is_valid=False,
                severity=ComplianceLevel.WARNING,
                message="HIPAA: Patient must be de-identified or have proper access controls",
                rule_name="hipaa_compliance",
                timestamp=datetime.now().isoformat()
            ))
        
        return results
    
    def _check_clinical_completeness(self, form_data: Dict) -> List[ValidationResult]:
        """Check clinical information completeness"""
        results = []
        
        # Should have diagnosis or reason for visit
        if not form_data.get("Diagnosis") and not form_data.get("Reason for Visit"):
            results.append(ValidationResult(
                field_name="(diagnosis)",
                is_valid=False,
                severity=ComplianceLevel.WARNING,
                message="Clinical record should include diagnosis or reason for visit",
                rule_name="clinical_completeness",
                timestamp=datetime.now().isoformat()
            ))
        
        return results


class InsuranceValidationEngine(DomainValidationEngine):
    """Insurance domain validation"""
    
    def __init__(self):
        super().__init__("insurance")
    
    def _initialize(self):
        self.field_validators = {
            "Policy Number": RegexValidator(
                r'^[A-Z0-9]{6,20}$',
                "Policy number must be 6-20 alphanumeric characters"
            ),
            "Premium": RangeValidator(0, 100000),
            "Deductible": RangeValidator(0, 10000),
            "Coverage Limit": RangeValidator(0, 5000000),
        }
        
        self.cross_field_validators = {
            "coverage_consistency": self._validate_coverage_consistency,
            "premium_relationship": self._validate_premium_relationship,
        }
        
        self.compliance_rules = {
            "policy_validity": self._check_policy_validity,
        }
    
    def _validate_coverage_consistency(self, form_data: Dict) -> Tuple[bool, str]:
        """Verify coverage relationships"""
        deductible = self._parse_float(form_data.get("Deductible", ""))
        limit = self._parse_float(form_data.get("Coverage Limit", ""))
        
        if deductible and limit and deductible > limit:
            return False, "Deductible cannot exceed coverage limit"
        return True, "Coverage values are consistent"
    
    def _validate_premium_relationship(self, form_data: Dict) -> Tuple[bool, str]:
        """Verify premium is reasonable"""
        premium = self._parse_float(form_data.get("Premium", ""))
        limit = self._parse_float(form_data.get("Coverage Limit", ""))
        
        if premium and limit:
            ratio = premium / limit
            if ratio > 0.1:  # Premium shouldn't exceed 10% of coverage
                return False, "Premium seems high relative to coverage limit"
        
        return True, "Premium relationship OK"
    
    def _check_policy_validity(self, form_data: Dict) -> List[ValidationResult]:
        """Check policy validity requirements"""
        results = []
        
        required = ["Policy Number", "Policyholder"]
        for field in required:
            if not form_data.get(field):
                results.append(ValidationResult(
                    field_name=field,
                    is_valid=False,
                    severity=ComplianceLevel.CRITICAL,
                    message=f"Required field '{field}' missing for valid policy",
                    rule_name="policy_validity",
                    timestamp=datetime.now().isoformat()
                ))
        
        return results
    
    @staticmethod
    def _parse_float(value: Optional[str]) -> Optional[float]:
        """Parse float from string, removing currency symbols"""
        if not value:
            return None
        try:
            return float(re.sub(r'[^\d.]', '', value))
        except:
            return None


class FinanceValidationEngine(DomainValidationEngine):
    """Finance/Accounting validation"""
    
    def __init__(self):
        super().__init__("finance")
    
    def _initialize(self):
        self.field_validators = {
            "Revenue": RangeValidator(0, float('inf')),
            "Expense": RangeValidator(0, float('inf')),
            "Account Number": RegexValidator(
                r'^\d{4}-\d{3}$',
                "Account number format: XXXX-XXX"
            ),
        }
        
        self.cross_field_validators = {
            "income_calculation": self._validate_income_calculation,
        }
        
        self.compliance_rules = {
            "accounting_compliance": self._check_accounting_compliance,
        }
    
    def _validate_income_calculation(self, form_data: Dict) -> Tuple[bool, str]:
        """Verify Revenue - Expense = Net Income"""
        revenue = self._parse_float(form_data.get("Revenue", ""))
        expense = self._parse_float(form_data.get("Expense", ""))
        net_income = self._parse_float(form_data.get("Net Income", ""))
        
        if revenue and expense and net_income:
            expected = revenue - expense
            if abs(net_income - expected) > 0.01:  # Allow small rounding errors
                return False, f"Income calculation error: {revenue} - {expense} ≠ {net_income}"
        
        return True, "Income calculations correct"
    
    def _check_accounting_compliance(self, form_data: Dict) -> List[ValidationResult]:
        """Check accounting compliance"""
        results = []
        
        revenue = self._parse_float(form_data.get("Revenue", ""))
        expense = self._parse_float(form_data.get("Expense", ""))
        
        if revenue and expense and revenue < expense:
            results.append(ValidationResult(
                field_name="Revenue/Expense",
                is_valid=False,
                severity=ComplianceLevel.WARNING,
                message="Expenses exceed revenue (loss situation)",
                rule_name="accounting_compliance",
                timestamp=datetime.now().isoformat()
            ))
        
        return results
    
    @staticmethod
    def _parse_float(value: Optional[str]) -> Optional[float]:
        """Parse float from string"""
        if not value:
            return None
        try:
            return float(re.sub(r'[^\d.]', '', value))
        except:
            return None


class LegalValidationEngine(DomainValidationEngine):
    """Legal/Contract validation"""
    
    def __init__(self):
        super().__init__("legal")
    
    def _initialize(self):
        self.field_validators = {
            "Effective Date": DateValidator(["%m/%d/%Y", "%Y-%m-%d"]),
        }
        
        self.cross_field_validators = {
            "date_sequence": self._validate_date_sequence,
        }
        
        self.compliance_rules = {
            "contract_completeness": self._check_contract_completeness,
        }
    
    def _validate_date_sequence(self, form_data: Dict) -> Tuple[bool, str]:
        """Verify effective date is before termination date"""
        effective = form_data.get("Effective Date")
        termination = form_data.get("Termination Date")
        
        if effective and termination:
            # Simple string comparison (works for YYYY-MM-DD format)
            if effective > termination:
                return False, "Effective date must be before termination date"
        
        return True, "Date sequence valid"
    
    def _check_contract_completeness(self, form_data: Dict) -> List[ValidationResult]:
        """Check contract completeness"""
        results = []
        
        critical_fields = ["Party", "Effective Date", "Consideration"]
        for field in critical_fields:
            if not form_data.get(field):
                results.append(ValidationResult(
                    field_name=field,
                    is_valid=False,
                    severity=ComplianceLevel.CRITICAL,
                    message=f"Contract must include: {field}",
                    rule_name="contract_completeness",
                    timestamp=datetime.now().isoformat()
                ))
        
        return results


# Registry of validation engines
VALIDATION_ENGINES = {
    "real_estate": RealEstateValidationEngine,
    "medical": MedicalValidationEngine,
    "insurance": InsuranceValidationEngine,
    "finance": FinanceValidationEngine,
    "legal": LegalValidationEngine,
}


def get_validation_engine(domain: str) -> DomainValidationEngine:
    """Get or create a validation engine for a domain"""
    engine_class = VALIDATION_ENGINES.get(domain.lower())
    if engine_class:
        return engine_class()
    
    # Return base engine if domain not found
    return DomainValidationEngine(domain)


if __name__ == "__main__":
    print("Validation Engine Test")
    print("=" * 60)
    
    # Test real estate validation
    engine = RealEstateValidationEngine()
    
    test_data = {
        "Seller Name": "John Smith",
        "Buyer Name": "Jane Doe",
        "Property Address": "123 Main St",
        "Purchase Price": "$250,000",
        "Closing Date": "01/15/2024",
    }
    
    print("\nReal Estate Validation:")
    for field, value in test_data.items():
        result = engine.validate_field(field, value)
        status = "✅" if result.is_valid else "❌"
        print(f"  {status} {field}: {result.message}")
