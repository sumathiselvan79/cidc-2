import json
import re
import argparse
import sys
from pathlib import Path


def load_json(filepath: Path):
    """Load a JSON file and return its content.
    Returns an empty dict if the file does not exist or is invalid.
    """
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
    """Write data to a JSON file with pretty indentation."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def extract_keywords(text: str) -> set:
    """Return a set of lower‑cased word tokens from the given text.
    Simple tokenisation – split on non‑word characters.
    """
    return set(re.findall(r"\w+", text.lower()))


def simulate_vector_search(query: str, documents: list) -> dict | None:
    """Very lightweight vector‑search stand‑in.
    * `query` – string built from field name + context.
    * `documents` – list of dicts each containing at least `content` and optional `metadata`.
    Returns the document dict with the highest keyword overlap score.
    """
    query_keywords = extract_keywords(query)
    best_match = None
    highest_score = 0
    for doc in documents:
        content = doc.get("content", "")
        # Combine content and any useful metadata fields for scoring
        meta_text = " ".join(str(v) for v in doc.get("metadata", {}).values())
        searchable = f"{content} {meta_text}".lower()
        score = sum(1 for kw in query_keywords if kw in searchable)
        # Small boost if the document's metadata contains a section that matches a word in the query
        if "section" in doc.get("metadata", {}):
            if doc["metadata"]["section"].lower() in query.lower():
                score += 2
        if score > highest_score:
            highest_score = score
            best_match = doc
    return best_match


def main():
    parser = argparse.ArgumentParser(description="Generic data‑retrieval step (Step 3)")
    parser.add_argument(
        "-i",
        "--input",
        default="step2_output.json",
        help="JSON file containing the confirmed fields (default: step2_output.json)",
    )
    parser.add_argument(
        "-s",
        "--source",
        default="source_data.json",
        help="JSON file containing source documents (default: source_data.json)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="step3_output.json",
        help="File to write the retrieval results (default: step3_output.json)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    source_path = Path(args.source)
    output_path = Path(args.output)

    # Load data
    fields = load_json(input_path)
    source_data = load_json(source_path)

    if not isinstance(fields, list):
        print(f"[Error] Expected a list of fields in {input_path}, got {type(fields)}")
        sys.exit(1)
    if not isinstance(source_data, dict) or "documents" not in source_data:
        print(f"[Error] Expected a dict with a 'documents' key in {source_path}")
        sys.exit(1)

    documents = source_data["documents"]
    retrieved = []

    print("--- Step 3: Data Retrieval (generic) ---")
    for field in fields:
        name = field.get("name")
        context = field.get("context", "")
        query = f"{name} {context}" if context else name
        print(f"Retrieving for field: '{name}' (query: '{query}')")
        match = simulate_vector_search(query, documents)
        if match:
            # Very naive extraction – try to pull a value based on the field name
            extracted = None
            # Look for a direct occurrence of the field name in the content
            if name.lower() in match.get("content", "").lower():
                # Grab the surrounding sentence (simple split on periods)
                sentences = re.split(r"[.!?]", match["content"])  # type: ignore
                for s in sentences:
                    if name.lower() in s.lower():
                        extracted = s.strip()
                        break
            retrieved.append(
                {
                    "field_id": field.get("id"),
                    "field_name": name,
                    "source_doc_id": match.get("id"),
                    "retrieved_value": extracted,
                    "confidence_score": 0.8 if extracted else 0.5,
                    "relationship": {
                        "source_type": match.get("metadata", {}).get("type"),
                        "connected_node": match.get("id"),
                    },
                }
            )
            print(f"  -> Matched doc {match.get('id')}, extracted: {extracted}")
        else:
            print(f"  -> No matching source found.")
            retrieved.append(
                {
                    "field_id": field.get("id"),
                    "field_name": name,
                    "retrieved_value": None,
                    "note": "Data not found in source",
                }
            )

    save_json(output_path, retrieved)
    print(f"\nStep 3 Complete. Results saved to {output_path}")

if __name__ == "__main__":
    main()
