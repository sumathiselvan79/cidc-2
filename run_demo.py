#!/usr/bin/env python3
"""
Simple Demo Script - Execute FastAPI with Sample Data
Shows step-by-step how to use the application
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 30

# Sample data by domain
SAMPLES = {
    "real_estate": {
        "property_address": "123 Oak Avenue, Springfield, Illinois 62701",
        "property_type": "Single Family Residence",
        "seller_name": "John Michael Smith",
        "buyer_name": "Sarah Jane Doe",
        "purchase_price": "$325,000.00",
        "closing_date": "2024-02-15"
    },
    "medical": {
        "patient_name": "Robert Michael Johnson",
        "date_of_birth": "1970-06-15",
        "visit_date": "2024-01-10",
        "diagnosis": "Essential Hypertension (HTN)",
        "medication": "Lisinopril 10mg daily",
        "blood_pressure": "138/88 mmHg"
    },
    "insurance": {
        "policy_holder_name": "Alice Marie Williams",
        "policy_number": "POL-2024-001",
        "policy_type": "Comprehensive Auto Insurance",
        "coverage_type": "Full Coverage",
        "premium_amount": "$1,200.00",
        "effective_date": "2024-01-01"
    }
}


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_step(number, name, status, duration=None, details=None):
    """Print step information"""
    symbol = "✅" if status == "completed" else "❌"
    print(f"\n{symbol} Step {number}: {name}")
    print(f"   Status: {status}")
    if duration:
        print(f"   Duration: {duration:.2f}ms")
    if details:
        for key, value in details.items():
            if isinstance(value, (dict, list)):
                print(f"   {key}: {json.dumps(value)[:60]}...")
            else:
                print(f"   {key}: {value}")


def demo_health_check():
    """Demo 1: Health Check"""
    print_section("DEMO 1: HEALTH CHECK")
    
    try:
        print("📍 Endpoint: GET /health")
        print("📝 Description: Check if server is running\n")
        
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        data = response.json()
        
        print("✅ Response:")
        print(json.dumps(data, indent=2))
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def demo_direct_processing(domain="real_estate"):
    """Demo 2: Direct JSON Processing"""
    print_section(f"DEMO 2: DIRECT JSON PROCESSING ({domain.upper()})")
    
    try:
        print(f"📍 Endpoint: POST /process")
        print(f"📝 Domain: {domain.upper()}")
        print(f"📊 Input Fields: {len(SAMPLES[domain])}\n")
        
        # Prepare request
        request_body = {
            "request_id": f"demo_{domain}_{int(datetime.now().timestamp())}",
            "input_data": SAMPLES[domain],
            "domain": domain,
            "verbose": True,
            "include_validation": True
        }
        
        print("📤 Request Body:")
        print(json.dumps(request_body, indent=2))
        
        print("\n⏳ Processing...")
        response = requests.post(
            f"{BASE_URL}/process",
            json=request_body,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        
        result = response.json()
        
        # Display results
        print("\n✅ Processing Complete!")
        print(f"   Request ID: {result['request_id']}")
        print(f"   Total Duration: {result['total_duration_ms']:.2f}ms")
        print(f"   Success: {result['success']}")
        print(f"   Message: {result['message']}")
        
        # Show each step
        print("\n📋 Pipeline Steps:")
        for step in result['steps']:
            details = {}
            if step['output']:
                if 'field_count' in step['output']:
                    details['Fields'] = step['output']['field_count']
                if 'mapped_count' in step['output']:
                    details['Mapped'] = step['output']['mapped_count']
                if 'retrieval_count' in step['output']:
                    details['Retrieved'] = step['output']['retrieval_count']
                if 'valid_count' in step['output']:
                    valid = step['output'].get('valid_count', 0)
                    total = step['output'].get('validation_count', 0)
                    details['Valid'] = f"{valid}/{total}"
            
            print_step(
                step['step_number'],
                step['step_name'],
                step['status'],
                step.get('duration_ms'),
                details
            )
        
        # Show final output
        if result['final_output']:
            print("\n🎯 Final Output Summary:")
            output = result['final_output']
            print(f"   Status: {output.get('status')}")
            print(f"   Validation: {output.get('validation_status')}")
            print(f"   Processed Fields: {len(output.get('processed_fields', {}))}")
            
            # Show sample field
            fields = output.get('processed_fields', {})
            if fields:
                first_field = list(fields.items())[0]
                print(f"\n   Sample Field ('{first_field[0]}'):")
                print(f"      Value: {first_field[1].get('value')}")
                print(f"      Valid: {first_field[1].get('valid')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def demo_all_domains():
    """Demo 3: Process All Domains"""
    print_section("DEMO 3: PROCESS ALL DOMAINS")
    
    domains = list(SAMPLES.keys())
    print(f"📊 Processing {len(domains)} domains...\n")
    
    results = {}
    for domain in domains:
        try:
            print(f"🔄 Processing {domain.upper()}...", end=" ")
            
            request_body = {
                "request_id": f"demo_{domain}_{int(datetime.now().timestamp())}",
                "input_data": SAMPLES[domain],
                "domain": domain,
                "verbose": False,
                "include_validation": True
            }
            
            response = requests.post(
                f"{BASE_URL}/process",
                json=request_body,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            
            result = response.json()
            results[domain] = {
                "success": result['success'],
                "duration": result['total_duration_ms'],
                "steps": len(result['steps']),
                "fields": len(result['final_output'].get('processed_fields', {})) if result['final_output'] else 0
            }
            
            print(f"✅ ({result['total_duration_ms']:.0f}ms)")
            
        except Exception as e:
            results[domain] = {"success": False, "error": str(e)}
            print(f"❌ ({str(e)})")
    
    # Summary
    print("\n📊 Domain Processing Summary:")
    print("-" * 70)
    for domain, result in results.items():
        if result.get('success'):
            print(f"  {domain.upper():15} | Duration: {result['duration']:8.2f}ms | Steps: {result['steps']} | Fields: {result['fields']}")
        else:
            print(f"  {domain.upper():15} | ❌ Error: {result.get('error', 'Unknown error')}")
    
    success_count = sum(1 for r in results.values() if r.get('success'))
    print(f"\n✅ Success: {success_count}/{len(domains)} domains")
    
    return success_count == len(domains)


def demo_custom_input():
    """Demo 4: Custom User Input"""
    print_section("DEMO 4: CUSTOM USER INPUT")
    
    print("📝 This demo shows how to use your own data\n")
    
    print("Example JSON you can use:")
    print(json.dumps({
        "field_name_1": "value_1",
        "field_name_2": "value_2",
        "field_name_3": "value_3"
    }, indent=2))
    
    print("\nThe process is:")
    print("  1. Prepare your JSON data")
    print("  2. Send it to the /process endpoint")
    print("  3. Specify the domain (real_estate, medical, insurance, etc.)")
    print("  4. Receive detailed step-by-step results")
    
    print("\nFor Real Estate data, use fields like:")
    print("  - property_address")
    print("  - seller_name")
    print("  - buyer_name")
    print("  - purchase_price")
    print("  - closing_date")
    
    print("\nFor Medical data, use fields like:")
    print("  - patient_name")
    print("  - date_of_birth")
    print("  - diagnosis")
    print("  - medication")
    print("  - visit_date")
    
    return True


def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("  FastAPI PDF Form Processing - EXECUTION DEMO")
    print("=" * 70)
    
    print("\n🔍 Checking server connection...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print("✅ Server is running!\n")
    except Exception as e:
        print(f"❌ Cannot connect to server: {str(e)}")
        print("\n💡 Make sure to start the server first:")
        print("   python fastapi_app.py")
        print("\nThen run this demo script in another terminal")
        return
    
    # Run demos
    demos = [
        ("Health Check", demo_health_check),
        ("Real Estate Processing", lambda: demo_direct_processing("real_estate")),
        ("Medical Processing", lambda: demo_direct_processing("medical")),
        ("Insurance Processing", lambda: demo_direct_processing("insurance")),
        ("All Domains", demo_all_domains),
        ("Custom Input Guide", demo_custom_input),
    ]
    
    results = {}
    for demo_name, demo_func in demos:
        try:
            result = demo_func()
            results[demo_name] = result
        except Exception as e:
            print(f"\n❌ Demo crashed: {str(e)}")
            results[demo_name] = False
    
    # Summary
    print_section("EXECUTION SUMMARY")
    
    for demo_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {demo_name}")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\n📊 Results: {passed}/{total} demos passed")
    
    if passed == total:
        print("\n✨ All demos executed successfully!")
        print("\n🎯 Next steps:")
        print("  1. Visit http://localhost:8000/docs for interactive API")
        print("  2. Try uploading your own JSON files")
        print("  3. Use different domains")
        print("  4. Integrate into your application")
    else:
        print(f"\n⚠️  {total - passed} demo(s) had issues")


if __name__ == "__main__":
    main()
