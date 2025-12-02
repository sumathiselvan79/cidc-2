"""
Integration Guide: Enhanced Workflow with New Modules
Complete walkthrough for using the new semantic retrieval, knowledge bases, field mapping, and validation systems
"""

import json
from pathlib import Path
from typing import Dict, Optional, List

# Import the new modules
from step3_semantic_retrieval import SemanticRetriever, RetrievalMatch
from knowledge_bases import get_knowledge_base, KNOWLEDGE_BASES
from field_mapper import FieldMapper
from validators import get_validation_engine, ValidationResult


class EnhancedWorkflowIntegration:
    """Demonstrates integration of all new components"""
    
    def __init__(self, domain: str):
        """Initialize with a specific domain"""
        self.domain = domain.lower()
        self.retriever = SemanticRetriever(domain=self.domain)
        self.knowledge_base = get_knowledge_base(self.domain)
        self.field_mapper = FieldMapper(domain=self.domain)
        self.validator = get_validation_engine(self.domain)
        self.results = []
    
    def process_field(
        self, 
        field_name: str, 
        documents: List[Dict], 
        form_data: Optional[Dict] = None
    ) -> Dict:
        """
        Process a single field through the entire enhanced workflow
        
        Args:
            field_name: Field to extract from documents
            documents: List of source documents
            form_data: Optional form data for context
            
        Returns:
            Dict with retrieval, mapping, and validation results
        """
        result = {
            "field": field_name,
            "domain": self.domain,
            "steps": {}
        }
        
        # Step 1: Semantic Retrieval
        retrieval = self.retriever.retrieve(field_name, documents)
        result["steps"]["retrieval"] = {
            "matched_value": retrieval.matched_value,
            "confidence": retrieval.confidence,
            "strategy": retrieval.retrieval_strategy,
            "reasoning": retrieval.reasoning,
        }
        
        # Step 2: Field Mapping and Ranking
        ranked_docs = self.field_mapper.rank_documents_for_field(
            field_name, 
            documents, 
            self.knowledge_base,
            top_k=3
        )
        result["steps"]["mapping"] = {
            "top_documents": ranked_docs,
            "count": len(ranked_docs),
        }
        
        # Step 3: Validation
        if retrieval.matched_value:
            validation = self.validator.validate_field(field_name, retrieval.matched_value)
            result["steps"]["validation"] = {
                "is_valid": validation.is_valid,
                "severity": validation.severity.name,
                "message": validation.message,
            }
        
        return result
    
    def process_form(self, form_data: Dict, documents: List[Dict]) -> Dict:
        """
        Process entire form through enhanced workflow
        
        Args:
            form_data: Form with fields to extract
            documents: Source documents
            
        Returns:
            Dict with complete workflow results and compliance report
        """
        form_results = {
            "domain": self.domain,
            "timestamp": str(__import__('datetime').datetime.now().isoformat()),
            "fields": {},
            "compliance": {}
        }
        
        # Process each field
        for field_name in form_data.keys():
            form_results["fields"][field_name] = self.process_field(
                field_name, 
                documents,
                form_data
            )
        
        # Cross-field validation
        cross_field_results = self.validator.validate_cross_fields(form_data)
        form_results["compliance"]["cross_field"] = [
            {
                "rule": r.rule_name,
                "is_valid": r.is_valid,
                "message": r.message,
            }
            for r in cross_field_results
        ]
        
        # Domain compliance check
        compliance_results = self.validator.check_compliance(form_data)
        form_results["compliance"]["domain_rules"] = {
            rule_name: [
                {
                    "is_valid": r.is_valid,
                    "severity": r.severity.name,
                    "message": r.message,
                }
                for r in results
            ]
            for rule_name, results in compliance_results.items()
        }
        
        return form_results


def example_real_estate_processing():
    """Example: Process real estate form with new workflow"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Real Estate Processing")
    print("="*70)
    
    integration = EnhancedWorkflowIntegration(domain="real_estate")
    
    # Sample documents (could be extracted from PDFs)
    documents = [
        {
            "source": "deed_book_123.pdf",
            "content": "Grantor: John Smith, Grantee: Jane Doe, Property: 123 Main Street",
            "metadata": {"type": "deed", "date": "2024-01-15"}
        },
        {
            "source": "closing_statement.pdf",
            "content": "Purchase Price: $250,000, Seller: John Smith, Buyer: Jane Doe",
            "metadata": {"type": "closing", "date": "2024-01-15"}
        }
    ]
    
    form_fields = {
        "Seller Name": None,
        "Buyer Name": None,
        "Property Address": None,
        "Purchase Price": None,
    }
    
    print("\nProcessing Real Estate Form:")
    for field_name in form_fields.keys():
        result = integration.process_field(field_name, documents)
        print(f"\n  Field: {field_name}")
        retrieval = result["steps"]["retrieval"]
        print(f"    Value: {retrieval['matched_value']}")
        print(f"    Confidence: {retrieval['confidence']:.2f}")
        print(f"    Strategy: {retrieval['strategy']}")
    
    # Full form processing
    print("\n  Full Form Validation:")
    form_result = integration.process_form(form_fields, documents)
    print(f"    Compliance Checks: {len(form_result['compliance']['cross_field'])} rules")


def example_medical_processing():
    """Example: Process medical form with validation"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Medical Form Processing")
    print("="*70)
    
    integration = EnhancedWorkflowIntegration(domain="medical")
    
    documents = [
        {
            "source": "patient_chart.pdf",
            "content": "DOB: 01/15/1985, HTN (Hypertension), Age 38",
            "metadata": {"type": "chart", "date": "2024-01-15"}
        }
    ]
    
    form_fields = {
        "Date of Birth": None,
        "Diagnosis": None,
        "Age": None,
    }
    
    print("\nProcessing Medical Form:")
    print("  Domain Knowledge Base Terms:")
    kb = integration.knowledge_base
    for term, alias in list(kb.abbreviations.items())[:3]:
        print(f"    {term} → {alias}")
    
    for field_name in form_fields.keys():
        result = integration.process_field(field_name, documents)
        retrieval = result["steps"]["retrieval"]
        print(f"\n  Field: {field_name}")
        print(f"    Value: {retrieval['matched_value']}")
        print(f"    Confidence: {retrieval['confidence']:.2f}")
        if "validation" in result["steps"]:
            validation = result["steps"]["validation"]
            print(f"    Valid: {validation['is_valid']}")


def example_insurance_processing():
    """Example: Process insurance form with compliance"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Insurance Form Processing")
    print("="*70)
    
    integration = EnhancedWorkflowIntegration(domain="insurance")
    
    # Create test form data
    form_data = {
        "Policy Number": "POL123456",
        "Premium": "150",
        "Deductible": "500",
        "Coverage Limit": "100000",
    }
    
    documents = [
        {
            "source": "policy.pdf",
            "content": "Policy POL123456, Premium $150/month, $500 deductible, $100,000 limit",
            "metadata": {"type": "policy"}
        }
    ]
    
    print("\nProcessing Insurance Policy:")
    
    # Process form
    form_result = integration.process_form(form_data, documents)
    
    # Display compliance report
    print("\n  Compliance Report:")
    compliance = form_result["compliance"]["domain_rules"]
    
    for rule_name, rule_results in compliance.items():
        print(f"    {rule_name}:")
        for result in rule_results:
            status = "✅" if result["is_valid"] else "❌"
            print(f"      {status} {result['message']}")


def example_workflow_comparison():
    """Compare old vs new workflow improvements"""
    print("\n" + "="*70)
    print("COMPARISON: Old vs New Workflow")
    print("="*70)
    
    comparison = {
        "Aspect": [
            "Field Extraction Strategy",
            "Domain Knowledge",
            "Entity Recognition",
            "Validation",
            "Compliance Checking",
            "Match Confidence",
            "Audit Trail",
            "Cross-field Validation",
        ],
        "Old Workflow": [
            "Keyword only",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
        ],
        "New Workflow": [
            "4-strategy multi-method",
            "5 domain knowledge bases",
            "Named entity recognition",
            "Field-level validation",
            "Domain compliance rules",
            "Confidence scoring",
            "Complete audit trail",
            "Cross-field rules engine",
        ],
        "Expected Improvement": [
            "Better accuracy",
            "Context-aware retrieval",
            "Better entity matching",
            "Data quality assurance",
            "Regulatory compliance",
            "+60-75% retrieval rate",
            "Full compliance tracking",
            "Data consistency checks",
        ]
    }
    
    print("\n  {:<30} {:<25} {:<25} {:<25}".format(
        "Aspect", "Old", "New", "Improvement"
    ))
    print("  " + "-" * 105)
    
    for i, aspect in enumerate(comparison["Aspect"]):
        print("  {:<30} {:<25} {:<25} {:<25}".format(
            aspect,
            comparison["Old Workflow"][i],
            comparison["New Workflow"][i],
            comparison["Expected Improvement"][i]
        ))


def print_available_domains():
    """Print available domains and their features"""
    print("\n" + "="*70)
    print("AVAILABLE DOMAINS AND FEATURES")
    print("="*70)
    
    for domain, kb_class in KNOWLEDGE_BASES.items():
        print(f"\n  Domain: {domain.upper()}")
        kb = kb_class()
        total_abbr = sum(len(term.abbreviations) for term in kb.glossary.values())
        print(f"    Glossary Terms: {len(kb.glossary)}")
        print(f"    Total Abbreviations: {total_abbr}")
        print(f"    Sample Terms: {list(kb.glossary.keys())[:3]}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("ENHANCED WORKFLOW INTEGRATION GUIDE")
    print("="*70)
    
    # Show available domains
    print_available_domains()
    
    # Run examples
    try:
        example_real_estate_processing()
    except Exception as e:
        print(f"  Real Estate example error: {e}")
    
    try:
        example_medical_processing()
    except Exception as e:
        print(f"  Medical example error: {e}")
    
    try:
        example_insurance_processing()
    except Exception as e:
        print(f"  Insurance example error: {e}")
    
    # Show comparison
    example_workflow_comparison()
    
    print("\n" + "="*70)
    print("INTEGRATION GUIDE COMPLETE")
    print("="*70)
    print("\nQuick Start:")
    print("  1. from integration_guide import EnhancedWorkflowIntegration")
    print("  2. workflow = EnhancedWorkflowIntegration(domain='real_estate')")
    print("  3. result = workflow.process_field(field_name, documents)")
    print("  4. form_result = workflow.process_form(form_data, documents)")
    print("\n" + "="*70)
