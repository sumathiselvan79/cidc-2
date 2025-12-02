"""
ML-Based Field Mapping Module
Intelligent field-to-document matching using domain context

Features:
  - Feature extraction from field names and documents
  - Machine learning-based similarity scoring
  - Domain context awareness
  - Field disambiguation
  - Confidence-based ranking
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import math


@dataclass
class FieldFeatures:
    """Features extracted from a field for ML matching"""
    field_name: str
    tokens: List[str]
    length: int
    has_numbers: bool
    has_special_chars: bool
    category: str  # demographic, financial, clinical, legal, etc.
    domain_keywords: List[str]


class FieldMapper:
    """
    ML-based field to document mapper
    Learns patterns from domain knowledge to match fields to source data
    """
    
    def __init__(self, domain: str = "generic"):
        self.domain = domain
        self.field_history = {}
        self.match_patterns = self._initialize_patterns()
        self.field_vectorizer = FieldVectorizer()
    
    def _initialize_patterns(self) -> Dict[str, List[str]]:
        """Initialize domain-specific field patterns"""
        patterns = {
            "real_estate": {
                "property": ["address", "location", "property", "premises", "land", "real estate"],
                "party": ["seller", "buyer", "grantor", "grantee", "owner", "name"],
                "financial": ["price", "consideration", "amount", "cost", "payment"],
                "recording": ["deed", "book", "page", "reference", "instrument", "number"],
                "temporal": ["date", "closing", "settlement", "commencement"],
            },
            "medical": {
                "demographic": ["name", "patient", "age", "birth", "dob", "id"],
                "clinical": ["diagnosis", "condition", "disease", "code", "icd"],
                "treatment": ["medication", "drug", "prescription", "rx", "therapy"],
                "safety": ["allergy", "adverse", "reaction", "intolerance", "contraindication"],
                "vital": ["blood pressure", "heart rate", "temperature", "weight", "height"],
            },
            "insurance": {
                "policy": ["policy", "number", "id", "contract"],
                "party": ["policyholder", "beneficiary", "insured", "recipient"],
                "coverage": ["limit", "coverage", "benefit", "amount"],
                "financial": ["premium", "deductible", "payment", "rate"],
            },
            "finance": {
                "financial": ["revenue", "expense", "income", "cost", "profit"],
                "accounting": ["account", "ledger", "journal", "entry", "code"],
                "tax": ["tax", "liability", "deduction", "rate", "filing"],
            },
            "legal": {
                "party": ["party", "parties", "entity", "person", "organization"],
                "obligation": ["obligation", "liability", "responsibility", "duty"],
                "termination": ["termination", "end date", "expiration", "renewal"],
            }
        }
        return patterns.get(domain, {})
    
    def extract_features(self, field_name: str, context: str = "") -> FieldFeatures:
        """Extract features from a field for ML matching"""
        full_text = f"{field_name} {context}".lower()
        tokens = re.findall(r'\w+', full_text)
        
        # Categorize field
        category = self._categorize_field(field_name)
        
        # Extract domain keywords
        domain_keywords = self._extract_domain_keywords(field_name)
        
        return FieldFeatures(
            field_name=field_name,
            tokens=tokens,
            length=len(tokens),
            has_numbers=any(c.isdigit() for c in field_name),
            has_special_chars=bool(re.search(r'[^\w\s]', field_name)),
            category=category,
            domain_keywords=domain_keywords
        )
    
    def _categorize_field(self, field_name: str) -> str:
        """Categorize field based on name"""
        field_lower = field_name.lower()
        
        for category, keywords in self.match_patterns.items():
            for keyword in keywords:
                if keyword in field_lower:
                    return category
        
        return "general"
    
    def _extract_domain_keywords(self, field_name: str) -> List[str]:
        """Extract domain-specific keywords from field name"""
        keywords = []
        field_lower = field_name.lower()
        
        for category, words in self.match_patterns.items():
            for word in words:
                if word in field_lower:
                    keywords.append(word)
        
        return keywords
    
    def match_field_to_document(self, 
                               field: Dict, 
                               document: Dict,
                               knowledge_base=None) -> float:
        """
        Calculate similarity score between a field and document
        Returns a score between 0 and 1
        """
        field_name = field.get("name", "")
        field_features = self.extract_features(field_name, field.get("context", ""))
        
        doc_content = document.get("content", "").lower()
        doc_metadata = document.get("metadata", {})
        
        scores = []
        
        # Score 1: Token overlap
        token_score = self._calculate_token_overlap(field_features.tokens, doc_content)
        scores.append(("token_overlap", token_score, 0.25))
        
        # Score 2: Category match
        category_score = self._calculate_category_match(field_features.category, doc_content)
        scores.append(("category_match", category_score, 0.25))
        
        # Score 3: Domain keyword match
        keyword_score = self._calculate_keyword_match(field_features.domain_keywords, doc_content)
        scores.append(("keyword_match", keyword_score, 0.25))
        
        # Score 4: Metadata match
        metadata_score = self._calculate_metadata_match(field_features, doc_metadata)
        scores.append(("metadata_match", metadata_score, 0.15))
        
        # Score 5: Knowledge base match (if available)
        if knowledge_base:
            kb_score = self._calculate_kb_match(field_name, doc_content, knowledge_base)
            scores.append(("kb_match", kb_score, 0.10))
        
        # Calculate weighted average
        total_weight = 0
        weighted_score = 0
        
        for score_name, score, weight in scores:
            weighted_score += score * weight
            total_weight += weight
        
        final_score = weighted_score / total_weight if total_weight > 0 else 0
        
        return min(final_score, 1.0)  # Clamp to [0, 1]
    
    def _calculate_token_overlap(self, field_tokens: List[str], doc_content: str) -> float:
        """Calculate token overlap score"""
        if not field_tokens:
            return 0.0
        
        doc_tokens = set(re.findall(r'\w+', doc_content))
        field_token_set = set(field_tokens)
        
        intersection = len(field_token_set & doc_tokens)
        union = len(field_token_set | doc_tokens)
        
        if union == 0:
            return 0.0
        
        # Jaccard similarity
        return intersection / union
    
    def _calculate_category_match(self, category: str, doc_content: str) -> float:
        """Calculate category-based match score"""
        if category not in self.match_patterns:
            return 0.0
        
        keywords = self.match_patterns[category]
        matches = sum(1 for kw in keywords if kw in doc_content)
        
        if not keywords:
            return 0.0
        
        return min(matches / len(keywords), 1.0)
    
    def _calculate_keyword_match(self, domain_keywords: List[str], doc_content: str) -> float:
        """Calculate domain keyword match score"""
        if not domain_keywords:
            return 0.0
        
        matches = sum(1 for kw in domain_keywords if kw in doc_content)
        return min(matches / len(domain_keywords), 1.0)
    
    def _calculate_metadata_match(self, field_features: FieldFeatures, 
                                 doc_metadata: Dict) -> float:
        """Calculate metadata match score"""
        score = 0.0
        
        # Check document type/section
        if "type" in doc_metadata:
            if field_features.category in str(doc_metadata["type"]).lower():
                score += 0.5
        
        if "section" in doc_metadata:
            section_lower = str(doc_metadata["section"]).lower()
            for token in field_features.tokens:
                if token in section_lower:
                    score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_kb_match(self, field_name: str, doc_content: str, 
                           knowledge_base) -> float:
        """Calculate knowledge base match score"""
        if not knowledge_base:
            return 0.0
        
        # Normalize field name using KB
        normalized = knowledge_base.normalize_term(field_name)
        if normalized:
            # Check if normalized term appears in document
            if normalized.lower() in doc_content:
                return 0.8
            
            # Check for related terms
            related = knowledge_base.get_related_terms(field_name)
            matches = sum(1 for term in related if term.lower() in doc_content)
            if matches > 0:
                return 0.5
        
        return 0.0
    
    def rank_documents_for_field(self, 
                                field: Dict, 
                                documents: List[Dict],
                                knowledge_base=None,
                                top_k: int = 3) -> List[Tuple[Dict, float]]:
        """
        Rank documents for a field and return top-k matches
        """
        scores = []
        
        for doc in documents:
            score = self.match_field_to_document(field, doc, knowledge_base)
            if score > 0:
                scores.append((doc, score))
        
        # Sort by score (descending)
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return scores[:top_k]
    
    def disambiguate_field(self, 
                          field_name: str, 
                          candidates: List[str]) -> Optional[str]:
        """
        Disambiguate between multiple candidate field names
        Returns the most likely canonical field name
        """
        if not candidates:
            return None
        
        if len(candidates) == 1:
            return candidates[0]
        
        # Calculate similarity between field_name and each candidate
        field_tokens = set(re.findall(r'\w+', field_name.lower()))
        
        best_match = None
        best_score = 0
        
        for candidate in candidates:
            candidate_tokens = set(re.findall(r'\w+', candidate.lower()))
            
            if field_tokens or candidate_tokens:
                intersection = len(field_tokens & candidate_tokens)
                union = len(field_tokens | candidate_tokens)
                similarity = intersection / union if union > 0 else 0
                
                if similarity > best_score:
                    best_score = similarity
                    best_match = candidate
        
        return best_match if best_score > 0 else None


class FieldVectorizer:
    """
    Converts field information to numerical vectors for ML models
    """
    
    def vectorize_field(self, field: Dict) -> List[float]:
        """Convert field to a feature vector"""
        features = []
        
        field_name = field.get("name", "")
        context = field.get("context", "")
        
        # Length features
        features.append(len(field_name) / 100.0)  # Normalize by typical max length
        features.append(len(context) / 500.0)
        
        # Token count
        tokens = re.findall(r'\w+', f"{field_name} {context}")
        features.append(len(tokens) / 20.0)
        
        # Character type features
        has_digits = 1.0 if any(c.isdigit() for c in field_name) else 0.0
        has_special = 1.0 if re.search(r'[^\w\s]', field_name) else 0.0
        has_caps = 1.0 if any(c.isupper() for c in field_name) else 0.0
        
        features.extend([has_digits, has_special, has_caps])
        
        # Word complexity (unique words / total words)
        if tokens:
            unique_ratio = len(set(tokens)) / len(tokens)
            features.append(unique_ratio)
        else:
            features.append(0.0)
        
        return features
    
    def vectorize_document(self, document: Dict) -> List[float]:
        """Convert document to a feature vector"""
        features = []
        
        content = document.get("content", "")
        metadata = document.get("metadata", {})
        
        # Content length features
        features.append(len(content) / 5000.0)  # Normalize
        
        # Token features
        tokens = re.findall(r'\w+', content)
        features.append(len(tokens) / 500.0)
        
        # Metadata features
        has_type = 1.0 if "type" in metadata else 0.0
        has_section = 1.0 if "section" in metadata else 0.0
        
        features.extend([has_type, has_section])
        
        # Document quality indicators
        if tokens:
            unique_ratio = len(set(tokens)) / len(tokens)
            features.append(unique_ratio)
        else:
            features.append(0.0)
        
        return features


# Example usage and testing
if __name__ == "__main__":
    print("Field Mapper Test")
    print("=" * 60)
    
    # Initialize mapper
    mapper = FieldMapper(domain="real_estate")
    
    # Test field
    test_field = {
        "name": "Seller Name",
        "context": "The undersigned seller"
    }
    
    # Test documents
    test_docs = [
        {
            "id": "doc1",
            "content": "John Smith, the grantor and seller, agrees to transfer property",
            "metadata": {"type": "real_estate_agreement", "section": "parties"}
        },
        {
            "id": "doc2",
            "content": "This is a medical record for patient John Smith",
            "metadata": {"type": "medical_record"}
        },
    ]
    
    # Extract features
    features = mapper.extract_features(test_field["name"], test_field["context"])
    print(f"\nField Features:")
    print(f"  Category: {features.category}")
    print(f"  Domain Keywords: {features.domain_keywords}")
    
    # Rank documents
    print(f"\nDocument Ranking for '{test_field['name']}':")
    ranked = mapper.rank_documents_for_field(test_field, test_docs, top_k=2)
    for doc, score in ranked:
        print(f"  • {doc['id']}: {score:.2%}")
