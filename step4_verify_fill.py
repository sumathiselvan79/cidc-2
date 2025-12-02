import json

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    retrieved_data_file = 'step3_output.json'
    filled_output_file = 'step4_filled_form.json'
    report_file = 'validation_report.txt'

    retrieved_items = load_json(retrieved_data_file)
    
    filled_form = {}
    total_fields = len(retrieved_items)
    filled_count = 0
    
    print("--- Step 4: Verify & Fill ---")
    
    validation_log = []
    
    for item in retrieved_items:
        field_name = item['field_name']
        value = item.get('retrieved_value')
        
        # Verify
        if value is not None:
            print(f"  [OK] Field '{field_name}' -> '{value}'")
            filled_form[field_name] = value
            filled_count += 1
            validation_log.append(f"SUCCESS: {field_name} filled with '{value}'")
        else:
            print(f"  [MISSING] Field '{field_name}' could not be filled.")
            filled_form[field_name] = "" # Leave empty or mark as pending
            validation_log.append(f"FAILURE: {field_name} is missing data.")

    # Fill Rate Calculation
    fill_rate = (filled_count / total_fields) * 100
    
    # Validate
    print(f"\n--- Validation Report ---")
    print(f"Total Fields: {total_fields}")
    print(f"Filled Fields: {filled_count}")
    print(f"Fill Rate: {fill_rate:.2f}%")
    
    validation_log.append(f"\nSUMMARY: Fill Rate {fill_rate:.2f}% ({filled_count}/{total_fields})")
    
    # Save outputs
    save_json(filled_output_file, filled_form)
    
    with open(report_file, 'w') as f:
        f.write("\n".join(validation_log))
        
    print(f"\nStep 4 Complete.")
    print(f"Filled form saved to {filled_output_file}")
    print(f"Validation report saved to {report_file}")

if __name__ == "__main__":
    main()
