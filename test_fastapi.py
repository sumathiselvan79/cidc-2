"""
Test script for FastAPI application
Tests the pipeline with sample JSON data
"""

import json
import requests
import time
import sys
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 30

# Sample test data
SAMPLE_DATA = {
    "real_estate": {
        "property_address": "123 Main Street, Springfield, IL 62701",
        "seller_name": "John Smith",
        "buyer_name": "Jane Doe",
        "purchase_price": "$250,000",
        "closing_date": "2024-02-15"
    },
    "medical": {
        "patient_name": "Robert Johnson",
        "date_of_birth": "1985-06-15",
        "diagnosis": "HTN (Hypertension)",
        "medication": "Lisinopril 10mg",
        "visit_date": "2024-01-10"
    },
    "insurance": {
        "policy_holder": "Alice Williams",
        "policy_number": "POL-2024-001",
        "coverage_type": "Comprehensive",
        "premium_amount": "$1,200",
        "effective_date": "2024-01-01"
    }
}


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def test_health_check():
    """Test health check endpoint"""
    print_header("TEST 1: Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Health check passed")
        print(f"   Status: {data['status']}")
        print(f"   Timestamp: {data['timestamp']}")
        print(f"   Version: {data['version']}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return False


def test_direct_processing(domain="real_estate"):
    """Test direct data processing"""
    print_header(f"TEST 2: Direct Processing ({domain.upper()})")
    
    try:
        payload = {
            "request_id": f"test_{domain}_{int(time.time())}",
            "input_data": SAMPLE_DATA[domain],
            "domain": domain,
            "verbose": True,
            "include_validation": True
        }
        
        print(f"📨 Sending request with {len(payload['input_data'])} fields...")
        
        response = requests.post(
            f"{BASE_URL}/process",
            json=payload,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        
        result = response.json()
        
        print(f"\n✅ Processing completed successfully")
        print(f"   Request ID: {result['request_id']}")
        print(f"   Total Duration: {result['total_duration_ms']:.2f}ms")
        print(f"   Steps Completed: {len(result['steps'])}")
        print(f"   Success: {result['success']}")
        
        print("\n📋 Step-by-Step Results:")
        for step in result['steps']:
            status_symbol = "✅" if step['status'] == 'completed' else "❌"
            print(f"\n{status_symbol} {step['step_number']}. {step['step_name']}")
            print(f"   Status: {step['status']}")
            if step['duration_ms']:
                print(f"   Duration: {step['duration_ms']:.2f}ms")
            if step['error_message']:
                print(f"   Error: {step['error_message']}")
            
            if step['output']:
                output = step['output']
                if step['step_number'] == 1:
                    print(f"   Validated Fields: {output.get('field_count', 0)}")
                elif step['step_number'] == 2:
                    print(f"   Mapped Fields: {output.get('mapped_count', 0)}")
                elif step['step_number'] == 3:
                    print(f"   Retrieved Values: {output.get('retrieval_count', 0)}")
                elif step['step_number'] == 4:
                    print(f"   Valid Fields: {output.get('valid_count', 0)}/{output.get('validation_count', 0)}")
                elif step['step_number'] == 5:
                    print(f"   Output Fields: {output.get('field_count', 0)}")
        
        if result['final_output']:
            print("\n🎯 Final Output:")
            print(f"   Status: {result['final_output'].get('status')}")
            print(f"   Validation Status: {result['final_output'].get('validation_status')}")
            print(f"   Processed Fields: {len(result['final_output'].get('processed_fields', {}))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Processing failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_file_upload(domain="real_estate"):
    """Test file upload and background processing"""
    print_header(f"TEST 3: File Upload ({domain.upper()})")
    
    try:
        # Create temporary JSON file
        temp_file = f"temp_test_{domain}.json"
        with open(temp_file, 'w') as f:
            json.dump(SAMPLE_DATA[domain], f)
        
        print(f"📁 Created test file: {temp_file}")
        
        # Upload file
        with open(temp_file, 'rb') as f:
            files = {'file': (temp_file, f, 'application/json')}
            params = {'domain': domain}
            
            response = requests.post(
                f"{BASE_URL}/upload",
                files=files,
                params=params,
                timeout=TIMEOUT
            )
        
        response.raise_for_status()
        result = response.json()
        
        print(f"✅ File uploaded successfully")
        print(f"   Request ID: {result['request_id']}")
        print(f"   Filename: {result['filename']}")
        print(f"   File Size: {result['file_size']} bytes")
        print(f"   Message: {result['message']}")
        
        # Wait for background processing
        print(f"\n⏳ Waiting for background processing...")
        request_id = result['request_id']
        
        for attempt in range(10):
            time.sleep(2)
            
            # Check status
            status_response = requests.get(
                f"{BASE_URL}/status/{request_id}",
                timeout=TIMEOUT
            )
            status_data = status_response.json()
            
            print(f"   Attempt {attempt + 1}: {status_data['status']}")
            
            if status_data['status'] == 'completed':
                print(f"\n✅ Background processing completed")
                
                # Get results
                results_response = requests.get(
                    f"{BASE_URL}/results/{request_id}",
                    timeout=TIMEOUT
                )
                results = results_response.json()
                
                print(f"   Steps Completed: {len(results['steps'])}")
                if results['final_output']:
                    print(f"   Final Output Fields: {len(results['final_output'].get('processed_fields', {}))}")
                
                break
        
        # Clean up
        Path(temp_file).unlink(missing_ok=True)
        
        return True
        
    except Exception as e:
        print(f"❌ File upload failed: {str(e)}")
        Path(temp_file).unlink(missing_ok=True)
        return False


def test_all_domains():
    """Test processing for all domains"""
    print_header("TEST 4: All Domains Processing")
    
    domains = list(SAMPLE_DATA.keys())
    results = {}
    
    for domain in domains:
        print(f"\n🔄 Processing {domain.upper()}...")
        try:
            payload = {
                "request_id": f"all_domains_{domain}_{int(time.time())}",
                "input_data": SAMPLE_DATA[domain],
                "domain": domain,
                "verbose": False,
                "include_validation": True
            }
            
            response = requests.post(
                f"{BASE_URL}/process",
                json=payload,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            
            result = response.json()
            results[domain] = {
                "success": result['success'],
                "duration": result['total_duration_ms'],
                "steps": len(result['steps'])
            }
            
            print(f"   ✅ Success: {result['success']}")
            print(f"   Duration: {result['total_duration_ms']:.2f}ms")
            
        except Exception as e:
            results[domain] = {"success": False, "error": str(e)}
            print(f"   ❌ Failed: {str(e)}")
    
    # Summary
    print("\n📊 Domain Processing Summary:")
    print("-" * 70)
    for domain, result in results.items():
        status = "✅" if result.get('success') else "❌"
        print(f"{status} {domain.upper():15} | Duration: {result.get('duration', 0):8.2f}ms | Steps: {result.get('steps', 0)}")


def main():
    """Main test function"""
    print("\n" + "=" * 70)
    print("  FastAPI PDF Form Processing Pipeline - Test Suite")
    print("=" * 70)
    print(f"Base URL: {BASE_URL}")
    print(f"Timeout: {TIMEOUT}s")
    print("=" * 70)
    
    # Check if server is running
    print("\n🔍 Checking server connection...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print("✅ Server is running and responding")
    except Exception as e:
        print(f"❌ Cannot connect to server: {str(e)}")
        print(f"\n💡 Make sure to start the server first:")
        print(f"   python fastapi_app.py")
        return
    
    # Run tests
    tests = [
        ("Health Check", test_health_check),
        ("Real Estate Processing", lambda: test_direct_processing("real_estate")),
        ("Medical Processing", lambda: test_direct_processing("medical")),
        ("Insurance Processing", lambda: test_direct_processing("insurance")),
        ("All Domains Test", test_all_domains),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {str(e)}")
            results[test_name] = False
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed!")
    else:
        print(f"⚠️  {total - passed} test(s) failed")


if __name__ == "__main__":
    main()
