"""
ENHANCED STEP 3: Semantic Data Retrieval with ML-based Matching
Replaces keyword-only search with embeddings-based semantic matching

Features:
  - Semantic similarity using sentence transformers
  - Domain-aware field mapping
  - Confidence scoring
  - Fallback strategies
  - Context preservation
"""

import json
import re
import argparse
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
import numpy as np

# Optional: Would require: pip install sentence-transformers
# For now, we provide a simulated version that can be upgraded

@dataclass
class RetrievalMatch:
    """Represents a successful field-to-document match"""
    field_id: str
    field_name: str
    source_doc_id: str
    retrieved_value: Optional[str]
    confidence_score: float
    match_type: str  # 'semantic', 'keyword', 'entity', 'rule-based'
    match_reason: str
    domain_context: str


class SemanticRetriever:
    """
    Semantic-based document retriever using multiple strategies:
    1. Semantic similarity (embeddings)
    2. Entity recognition
    3. Domain-specific rules
    4. Keyword fallback
    """
    
    def __init__(self, domain: str = "generic"):
        self.domain = domain
        self.query_cache = {}
        self.match_history = []
        
    def retrieve(self, field: Dict, documents: List[Dict]) -> Optional[RetrievalMatch]:
        """
        Retrieve data for a field using multiple strategies with fallback
        """
        field_name = field.get("name", "")
        field_context = field.get("context", "")
        query = f"{field_name} {field_context}"
        
        # Strategy 1: Semantic Similarity
        semantic_match = self._semantic_match(query, documents)
        if semantic_match and semantic_match.confidence_score >= 0.75:
            return semantic_match
        
        # Strategy 2: Entity Recognition
        entity_match = self._entity_match(field_name, documents)
        if entity_match and entity_match.confidence_score >= 0.70:
            return entity_match
        
        # Strategy 3: Domain-Specific Rules
        domain_match = self._domain_rule_match(field_name, documents)
        if domain_match and domain_match.confidence_score >= 0.65:
            return domain_match
        
        # Strategy 4: Keyword Fallback (improved)
        keyword_match = self._enhanced_keyword_match(query, documents)
        if keyword_match and keyword_match.confidence_score >= 0.55:
            return keyword_match
        
        # No match found
        return None
    
    def _semantic_match(self, query: str, documents: List[Dict]) -> Optional[RetrievalMatch]:
        """
        Semantic similarity matching using document embeddings
        
        In production, this would use:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        query_embedding = model.encode(query)
        doc_embeddings = [model.encode(doc['content']) for doc in documents]
        similarities = cosine_similarity([query_embedding], doc_embeddings)[0]
        """
        best_match = None
        highest_score = 0
        
        for doc in documents:
            content = doc.get("content", "").lower()
            # Simulated semantic scoring (would use embeddings in production)
            # Score based on term presence and context
            score = self._calculate_similarity_score(query.lower(), content)
            
            if score > highest_score and score > 0:
                highest_score = score
                best_match = doc
        
        if best_match and highest_score > 0:
            extracted_value = self._extract_value_from_match(
                query, best_match.get("content", "")
            )
            return RetrievalMatch(
                field_id=query.split()[0],
                field_name=query,
                source_doc_id=best_match.get("id", ""),
                retrieved_value=extracted_value,
                confidence_score=min(highest_score, 1.0),
                match_type="semantic",
                match_reason=f"Content similarity: {highest_score:.2f}",
                domain_context=best_match.get("metadata", {}).get("type", "")
            )
        
        return None
    
    def _entity_match(self, field_name: str, documents: List[Dict]) -> Optional[RetrievalMatch]:
        """
        Entity-based matching for names, places, codes, etc.
        """
        # Extract potential entities from field name
        entities = self._extract_entities(field_name)
        
        if not entities:
            return None
        
        for doc in documents:
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            
            # Check if entities appear in document
            entity_matches = sum(1 for entity in entities if entity.lower() in content.lower())
            
            if entity_matches > 0:
                confidence = min(entity_matches / len(entities), 1.0)
                
                if confidence >= 0.5:
                    extracted_value = self._extract_value_from_match(
                        field_name, content
                    )
                    return RetrievalMatch(
                        field_id=field_name,
                        field_name=field_name,
                        source_doc_id=doc.get("id", ""),
                        retrieved_value=extracted_value,
                        confidence_score=confidence,
                        match_type="entity",
                        match_reason=f"Entity match: {entity_matches}/{len(entities)} entities found",
                        domain_context=metadata.get("type", "")
                    )
        
        return None
    
    def _domain_rule_match(self, field_name: str, documents: List[Dict]) -> Optional[RetrievalMatch]:
        """
        Domain-specific rule-based matching
        Uses domain knowledge to map fields to document types
        """
        # Domain rules mapping
        domain_rules = {
            "real_estate": {
                "property": ["deed", "property description", "address"],
                "seller": ["seller name", "grantor", "owner"],
                "deed reference": ["instrument number", "book", "page"]
            },
            "medical": {
                "patient name": ["patient", "name"],
                "age": ["age", "dob", "birth"],
                "diagnosis": ["diagnosis", "condition", "code"],
                "medications": ["medication", "drug", "prescription", "rx"]
            },
            "insurance": {
                "policy number": ["policy", "number", "id"],
                "beneficiary": ["beneficiary", "dependent", "name"],
                "coverage": ["coverage", "limit", "amount", "benefit"]
            }
        }
        
        # Get rules for current domain
        rules = domain_rules.get(self.domain, {})
        
        # Check if field matches any rule
        for rule_category, keywords in rules.items():
            if any(kw.lower() in field_name.lower() for kw in keywords):
                # Try to find matching document
                for doc in documents:
                    content = doc.get("content", "")
                    metadata = doc.get("metadata", {})
                    
                    # Check metadata for domain hints
                    if metadata.get("section") or metadata.get("type"):
                        if any(kw.lower() in content.lower() for kw in keywords):
                            extracted_value = self._extract_value_from_match(
                                field_name, content
                            )
                            return RetrievalMatch(
                                field_id=field_name,
                                field_name=field_name,
                                source_doc_id=doc.get("id", ""),
                                retrieved_value=extracted_value,
                                confidence_score=0.72,
                                match_type="rule-based",
                                match_reason=f"Domain rule matched: {rule_category}",
                                domain_context=metadata.get("type", "")
                            )
        
        return None
    
    def _enhanced_keyword_match(self, query: str, documents: List[Dict]) -> Optional[RetrievalMatch]:
        """
        Improved keyword matching with better scoring
        """
        query_keywords = set(re.findall(r"\w+", query.lower()))
        best_match = None
        highest_score = 0
        
        for doc in documents:
            content = doc.get("content", "").lower()
            metadata = doc.get("metadata", {})
            
            # Combine content and metadata for scoring
            searchable = f"{content} {' '.join(str(v) for v in metadata.values())}"
            doc_keywords = set(re.findall(r"\w+", searchable))
            
            # Calculate Jaccard similarity
            if query_keywords or doc_keywords:
                intersection = len(query_keywords & doc_keywords)
                union = len(query_keywords | doc_keywords)
                similarity = intersection / union if union > 0 else 0
                
                # Boost score if metadata section matches
                if metadata.get("section"):
                    if metadata["section"].lower() in query.lower():
                        similarity *= 1.2
                
                if similarity > highest_score:
                    highest_score = similarity
                    best_match = doc
        
        if best_match and highest_score > 0.2:
            extracted_value = self._extract_value_from_match(
                query, best_match.get("content", "")
            )
            return RetrievalMatch(
                field_id=query.split()[0],
                field_name=query,
                source_doc_id=best_match.get("id", ""),
                retrieved_value=extracted_value,
                confidence_score=highest_score,
                match_type="keyword",
                match_reason=f"Keyword overlap: {highest_score:.2f}",
                domain_context=best_match.get("metadata", {}).get("type", "")
            )
        
        return None
    
    def _calculate_similarity_score(self, query: str, content: str) -> float:
        """Calculate text similarity score"""
        query_terms = set(query.split())
        content_terms = set(content.split())
        
        if not query_terms or not content_terms:
            return 0.0
        
        intersection = len(query_terms & content_terms)
        union = len(query_terms | content_terms)
        
        return intersection / union if union > 0 else 0.0
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract named entities from text"""
        # Simple entity extraction - would use NER in production
        # For now, extract capitalized words and important terms
        entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        entities += [word for word in text.split() if len(word) > 3]
        return list(set(entities))
    
    def _extract_value_from_match(self, field_name: str, content: str) -> Optional[str]:
        """Extract relevant value from matched document"""
        # Simple extraction - find sentence containing field keywords
        sentences = re.split(r'[.!?]', content)
        field_keywords = field_name.lower().split()
        
        for sentence in sentences:
            if any(kw in sentence.lower() for kw in field_keywords):
                extracted = sentence.strip()
                if len(extracted) > 10 and len(extracted) < 500:
                    return extracted
        
        return None


def load_json(filepath: Path) -> dict:
    """Load JSON file safely"""
    if not filepath.is_file():
        print(f"[Error] File not found: {filepath}")
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"[Error] Failed to parse JSON {filepath}: {e}")
        return {}


def save_json(filepath: Path, data):
    """Write data to JSON file"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="Enhanced Step 3: Semantic Data Retrieval"
    )
    parser.add_argument(
        "-i", "--input",
        default="step2_output.json",
        help="Confirmed fields from Step 2"
    )
    parser.add_argument(
        "-s", "--source",
        default="source_data.json",
        help="Source documents"
    )
    parser.add_argument(
        "-o", "--output",
        default="step3_semantic_output.json",
        help="Output file for retrieval results"
    )
    parser.add_argument(
        "-d", "--domain",
        default="generic",
        help="Domain (real_estate, medical, insurance, finance, legal)"
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    source_path = Path(args.source)
    output_path = Path(args.output)
    domain = args.domain
    
    # Load data
    fields = load_json(input_path)
    source_data = load_json(source_path)
    
    if not isinstance(fields, list):
        print(f"[Error] Expected list of fields in {input_path}")
        sys.exit(1)
    
    if not isinstance(source_data, dict) or "documents" not in source_data:
        print(f"[Error] Expected dict with 'documents' key in {source_path}")
        sys.exit(1)
    
    documents = source_data["documents"]
    retriever = SemanticRetriever(domain=domain)
    retrieved = []
    
    print("=" * 80)
    print(f"ENHANCED STEP 3: Semantic Data Retrieval (Domain: {domain.upper()})")
    print("=" * 80)
    
    for field in fields:
        name = field.get("name", "")
        print(f"\nRetrieving: '{name}'")
        
        match = retriever.retrieve(field, documents)
        
        if match:
            print(f"  ✅ MATCH FOUND ({match.match_type})")
            print(f"     Document: {match.source_doc_id}")
            print(f"     Confidence: {match.confidence_score:.2%}")
            print(f"     Reason: {match.match_reason}")
            print(f"     Value: {match.retrieved_value[:60] if match.retrieved_value else 'N/A'}...")
            
            retrieved.append({
                "field_id": match.field_id,
                "field_name": match.field_name,
                "source_doc_id": match.source_doc_id,
                "retrieved_value": match.retrieved_value,
                "confidence_score": match.confidence_score,
                "match_type": match.match_type,
                "match_reason": match.match_reason,
                "domain_context": match.domain_context,
                "relationship": {
                    "source_type": match.domain_context,
                    "connected_node": match.source_doc_id
                }
            })
        else:
            print(f"  ❌ NO MATCH - No suitable data found in sources")
            retrieved.append({
                "field_id": name,
                "field_name": name,
                "retrieved_value": None,
                "note": "Data not found in source documents",
                "recommendation": f"Manual lookup or additional source needed for: {name}"
            })
    
    # Save results
    save_json(output_path, retrieved)
    
    # Print summary
    successful = sum(1 for r in retrieved if r.get("retrieved_value") is not None)
    total = len(retrieved)
    rate = (successful / total * 100) if total > 0 else 0
    
    print(f"\n{'=' * 80}")
    print(f"SUMMARY")
    print(f"{'=' * 80}")
    print(f"Total Fields: {total}")
    print(f"Successfully Retrieved: {successful}")
    print(f"Retrieval Rate: {rate:.2f}%")
    print(f"Output saved to: {output_path}")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    main()
