"""
QUICK REFERENCE GUIDE
For using the enhanced workflow system
"""

# ============================================================================
# QUICK START - 3 Steps to Enhance Your Form Processing
# ============================================================================

# STEP 1: Import the modules
from step3_semantic_retrieval import SemanticRetriever
from knowledge_bases import get_knowledge_base
from field_mapper import FieldMapper
from validators import get_validation_engine

# STEP 2: Initialize for your domain
domain = "real_estate"  # or: medical, insurance, finance, legal
retriever = SemanticRetriever(domain=domain)
kb = get_knowledge_base(domain)
mapper = FieldMapper(domain=domain)
validator = get_validation_engine(domain)

# STEP 3: Process your form
documents = [...]  # Your extracted PDF content
field_value = retriever.retrieve("Property Address", documents)
print(f"Value: {field_value.matched_value}, Confidence: {field_value.confidence:.2f}")


# ============================================================================
# DOMAIN OPTIONS
# ============================================================================

AVAILABLE_DOMAINS = [
    "real_estate",    # Property transactions, deeds, closings
    "medical",        # Patient records, clinical data
    "insurance",      # Policies, coverage, premiums
    "finance",        # Accounting, transactions, reports
    "legal",          # Contracts, agreements, dates
]


# ============================================================================
# MODULE REFERENCE
# ============================================================================

# 1. SEMANTIC RETRIEVER - Extract values from documents
# ────────────────────────────────────────────────────
from step3_semantic_retrieval import SemanticRetriever, RetrievalMatch

retriever = SemanticRetriever(domain="real_estate")

# Methods:
retriever.retrieve(field_name, documents) -> RetrievalMatch
# Returns: RetrievalMatch with:
#   - matched_value: The extracted value
#   - confidence: 0.0-1.0 score
#   - retrieval_strategy: Which method found it
#   - reasoning: Why it was selected

# Strategies used (in order):
# 1. Semantic similarity
# 2. Entity recognition
# 3. Domain-specific rules
# 4. Enhanced keyword matching


# 2. KNOWLEDGE BASES - Domain terminology and validation
# ──────────────────────────────────────────────────────
from knowledge_bases import get_knowledge_base

kb = get_knowledge_base("medical")

# Methods:
kb.normalize_term("HTN") -> "Hypertension"
kb.get_related_terms("Hypertension") -> ["HTN", "High Blood Pressure"]
kb.validate_field_value("Age", "35") -> (True, "Valid")

# Attributes:
kb.glossary        # Main terms and definitions
kb.abbreviations   # Abbreviation mappings
kb.relationships   # Field relationships
kb.validation_rules # Domain rules


# 3. FIELD MAPPER - Intelligent matching between fields and documents
# ────────────────────────────────────────────────────────────────────
from field_mapper import FieldMapper

mapper = FieldMapper(domain="real_estate")

# Methods:
mapper.extract_features("Property Address") -> feature_vector
mapper.match_field_to_document("Property Address", document) -> score (0-100)
mapper.rank_documents_for_field("Property Address", documents, kb, top_k=3) -> [doc_score, ...]
mapper.disambiguate_field("Seller", candidates) -> best_candidate

# Scoring factors:
# - Token overlap (25%)
# - Category match (25%)
# - Domain keyword match (25%)
# - Metadata match (15%)
# - Knowledge base match (10%)


# 4. VALIDATORS - Validation and compliance checking
# ───────────────────────────────────────────────────
from validators import get_validation_engine, ValidationResult

validator = get_validation_engine("real_estate")

# Methods:
validator.validate_field("Purchase Price", "$250,000") -> ValidationResult
validator.validate_cross_fields(form_data) -> [ValidationResult, ...]
validator.check_compliance(form_data) -> {"rule_name": [results], ...}
validator.get_audit_trail() -> [all_validation_results]

# ValidationResult attributes:
result.field_name      # The field checked
result.is_valid        # Pass/fail
result.severity        # CRITICAL, WARNING, INFO, OPTIONAL
result.message         # Human-readable explanation
result.rule_name       # Name of the rule
result.timestamp       # When it was checked


# ============================================================================
# COMMON TASKS
# ============================================================================

# Task 1: Extract a single field
# ────────────────────────────────
field_name = "Grantor"
documents = [{"content": "Grantor: John Smith, Grantee: Jane Doe"}]

retriever = SemanticRetriever("real_estate")
match = retriever.retrieve(field_name, documents)

print(f"Found: {match.matched_value}")
print(f"Confidence: {match.confidence * 100:.1f}%")
print(f"Strategy: {match.retrieval_strategy}")


# Task 2: Validate extracted data
# ────────────────────────────────
validator = get_validation_engine("real_estate")

# Field-level validation
result = validator.validate_field("Purchase Price", "$250,000")
if result.is_valid:
    print("✓ Price is valid")
else:
    print(f"✗ Price error: {result.message}")

# Cross-field validation
form_data = {
    "Seller Name": "John Smith",
    "Buyer Name": "Jane Doe",
    "Purchase Price": "$250,000",
}
cross_results = validator.validate_cross_fields(form_data)


# Task 3: Check domain compliance
# ────────────────────────────────
compliance_results = validator.check_compliance(form_data)

for rule_name, results in compliance_results.items():
    print(f"{rule_name}:")
    for result in results:
        status = "✓" if result.is_valid else "✗"
        print(f"  {status} {result.message}")


# Task 4: Get domain terminology
# ──────────────────────────────
kb = get_knowledge_base("medical")

# What does "HTN" mean?
print(kb.normalize_term("HTN"))  # "Hypertension"

# What are synonyms for "Hypertension"?
print(kb.get_related_terms("Hypertension"))  # ["HTN", "HBP", ...]


# Task 5: Process complete form
# ──────────────────────────────
from integration_guide import EnhancedWorkflowIntegration

workflow = EnhancedWorkflowIntegration(domain="real_estate")

form_data = {
    "Seller Name": None,
    "Buyer Name": None,
    "Property Address": None,
    "Purchase Price": None,
}

documents = [...]  # Your PDF content

# Process entire form
result = workflow.process_form(form_data, documents)

# Result structure:
# {
#   "domain": "real_estate",
#   "timestamp": "2024-01-15T10:30:00",
#   "fields": {
#     "field_name": {
#       "steps": {
#         "retrieval": {...},
#         "mapping": {...},
#         "validation": {...}
#       }
#     }
#   },
#   "compliance": {
#     "cross_field": [...],
#     "domain_rules": {...}
#   }
# }


# ============================================================================
# ERROR HANDLING
# ============================================================================

# Handle missing values
match = retriever.retrieve("NonexistentField", documents)
if match.matched_value is None:
    print("Field not found in documents")
elif match.confidence < 0.5:
    print("Found but low confidence - may need review")


# Handle validation errors
result = validator.validate_field("Age", "invalid")
if not result.is_valid:
    print(f"Validation failed: {result.message}")
    print(f"Severity: {result.severity.name}")


# ============================================================================
# PERFORMANCE TIPS
# ============================================================================

# Tip 1: Reuse objects (don't create new ones for each field)
retriever = SemanticRetriever("real_estate")  # Create once
for field in fields:
    result = retriever.retrieve(field, documents)  # Reuse many times

# Tip 2: Filter documents before ranking (faster)
relevant_docs = [d for d in documents if "real estate" in d.get("content", "").lower()]
ranked = mapper.rank_documents_for_field(field, relevant_docs, kb)

# Tip 3: Batch validation (validate many fields at once)
form_data = {field1: value1, field2: value2, ...}
validator.validate_cross_fields(form_data)  # More efficient

# Tip 4: Use confidence scores to filter results
matches = [m for m in results if m.confidence > 0.7]  # High confidence only


# ============================================================================
# EXTENDING THE SYSTEM
# ============================================================================

# Add custom validator
from validators import FieldValidator

class MyValidator(FieldValidator):
    def validate(self, value):
        if value and len(value) > 10:
            return True, "Valid"
        return False, "Too short"

# Add custom retrieval strategy
from step3_semantic_retrieval import SemanticRetriever

class MyRetriever(SemanticRetriever):
    def _custom_strategy(self, field, documents):
        # Your custom logic here
        pass


# ============================================================================
# INTEGRATION WITH YOUR CODE
# ============================================================================

# Step 1: Extract fields (using existing step2_user_confirmation.py)
# Step 2: Use NEW semantic retriever instead of old step3_data_retrieval.py
# Step 3: Validate results (using new validators.py)
# Step 4: Fill form (using existing step4_verify_fill.py)

# Example pipeline:
from step2_user_confirmation import confirm_fields
from step3_semantic_retrieval import SemanticRetriever
from validators import get_validation_engine
from step4_verify_fill import fill_form

# Extract fields from PDF
fields = confirm_fields(pdf_path)

# Get values using new retriever
retriever = SemanticRetriever(domain="real_estate")
filled_data = {}
for field in fields:
    match = retriever.retrieve(field, source_documents)
    filled_data[field] = match.matched_value

# Validate
validator = get_validation_engine("real_estate")
for field, value in filled_data.items():
    result = validator.validate_field(field, value)
    if not result.is_valid:
        print(f"Warning: {field} - {result.message}")

# Fill form
filled_form = fill_form(pdf_path, filled_data)


# ============================================================================
# TROUBLESHOOTING
# ============================================================================

# Problem: Low confidence scores
# Solution: Check if documents contain the information
#           Use different domain if needed
#           Review field names for clarity

# Problem: Validation fails
# Solution: Check field format vs validation rule
#           Use kb.normalize_term() to check term mapping
#           Review domain rules in validators.py

# Problem: Module not found errors
# Solution: Ensure all files are in same directory
#           from knowledge_bases import ...
#           Check Python path

# Problem: Performance issues
# Solution: Filter documents before processing
#           Batch operations together
#           Use multiprocessing for large forms


# ============================================================================
# DOCUMENTATION LINKS
# ============================================================================

"""
See these files for more information:

1. ENHANCEMENT_COMPLETION_REPORT.md
   - Full technical documentation
   - Architecture details
   - Performance metrics

2. integration_guide.py
   - Complete working examples
   - Integration patterns
   - Best practices

3. step3_semantic_retrieval.py
   - Retrieval strategy details
   - Confidence scoring
   - Fallback logic

4. knowledge_bases.py
   - Domain terminology
   - Abbreviation mappings
   - Validation rules

5. field_mapper.py
   - Scoring system details
   - Feature engineering
   - ML integration points

6. validators.py
   - Validation rules per domain
   - Compliance checking
   - Audit trail
"""

print(__doc__)
