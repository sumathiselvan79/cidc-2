import json
import os

def load_json(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    input_file = 'Sample-Fillable-PDF_fields.json'
    memory_file = 'field_memory.json'
    output_file = 'step2_output.json'

    # Load input data from Step 1
    raw_data = load_json(input_file)
    if not raw_data:
        print(f"No input found in {input_file}")
        return

    # Flatten fields from the new structure
    discovered_fields = []
    if 'pages' in raw_data:
        for page in raw_data['pages']:
            for field in page.get('fields', []):
                # Map user's JSON structure to our internal structure
                mapped_field = {
                    "id": field.get('key'), # Use key as ID for now
                    "name": field.get('key'),
                    "context": field.get('field_label') or f"Coordinates: {field.get('coordinates')}",
                    "properties": {
                        "type": field.get('type'),
                        "confidence": 1.0 # Assume 1.0 for now as it comes from a previous tool
                    }
                }
                discovered_fields.append(mapped_field)
    else:
        # Fallback for flat list if needed
        discovered_fields = raw_data

    # Load memory (learning)
    memory = load_json(memory_file)
    memory_map = {item['name']: item for item in memory}

    confirmed_fields = []
    
    print("--- Step 2: User Fields & Context Confirmation ---")

    for field in discovered_fields:
        name = field.get('name')
        context = field.get('context')
        props = field.get('properties', {})
        
        print(f"\nProcessing Field: {name}")
        print(f"  Context: {context}")
        print(f"  Detected Type: {props.get('type')}")
        
        # Check memory for past confirmation
        if name in memory_map:
            print(f"  [Memory] Found known pattern for '{name}'. Auto-confirming.")
            field['status'] = 'auto-confirmed'
            confirmed_fields.append(field)
        else:
            # Low confidence or new field -> Ask User
            print(f"  [New/Low Confidence] Please confirm this field.")
            # For automation purposes in this environment, we will default to 'y' if no input is possible,
            # but since we are running interactively, we ask.
            user_input = input(f"  Keep '{name}'? (y/n/rename): ").strip().lower()
            
            if user_input == 'y' or user_input == '':
                field['status'] = 'user-confirmed'
                confirmed_fields.append(field)
                memory.append({
                    'name': name,
                    'context_pattern': context,
                    'user_preference': 'keep'
                })
            elif user_input == 'n':
                print(f"  Skipping {name}")
            else:
                new_name = input(f"  Enter new name for '{name}': ").strip()
                field['original_name'] = name
                field['name'] = new_name
                field['status'] = 'user-renamed'
                confirmed_fields.append(field)
                memory.append({
                    'name': name,
                    'mapped_to': new_name,
                    'user_preference': 'rename'
                })

    # Save output for Step 3
    save_json(output_file, confirmed_fields)
    
    # Update memory
    save_json(memory_file, memory)
    
    print(f"\nStep 2 Complete. Confirmed fields saved to {output_file}")
    print(f"Learning updated in {memory_file}")

if __name__ == "__main__":
    main()
