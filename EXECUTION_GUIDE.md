# 🚀 HOW TO EXECUTE - Complete Execution Guide

## Quick Start (2 Minutes)

### Step 1: Start the Server
```bash
cd d:\2-12-cidc
python fastapi_app.py
```

You should see:
```
======================================================================
🚀 PDF Form Processing Pipeline - FastAPI Server Starting
======================================================================
Server will start at: http://localhost:8000
API Docs at: http://localhost:8000/docs
======================================================================
```

### Step 2: Open in Browser
Visit: **http://localhost:8000/docs**

You'll see an interactive API interface (Swagger UI) where you can test endpoints directly.

---

## Input Format

### ✅ Valid JSON Input Structure

The application accepts JSON objects with key-value pairs:

```json
{
  "field_name_1": "value_1",
  "field_name_2": "value_2",
  "field_name_3": "value_3"
}
```

### Examples by Domain

#### 🏠 Real Estate Example
```json
{
  "property_address": "123 Oak Avenue, Springfield, Illinois 62701",
  "seller_name": "John Michael Smith",
  "buyer_name": "Sarah Jane Doe",
  "purchase_price": "$325,000.00",
  "closing_date": "2024-02-15"
}
```

#### 🏥 Medical Example
```json
{
  "patient_name": "Robert Michael Johnson",
  "date_of_birth": "1970-06-15",
  "diagnosis": "Essential Hypertension (HTN)",
  "medication": "Lisinopril 10mg daily",
  "visit_date": "2024-01-10"
}
```

#### 🚗 Insurance Example
```json
{
  "policy_holder_name": "Alice Marie Williams",
  "policy_number": "POL-2024-001",
  "coverage_type": "Full Coverage",
  "premium_amount": "$1,200.00",
  "effective_date": "2024-01-01"
}
```

---

## Execution Methods

### Method 1️⃣: Interactive Swagger UI (Easiest)

**Steps:**
1. Start server: `python fastapi_app.py`
2. Open: http://localhost:8000/docs
3. Click on **POST /process**
4. Click **Try it out**
5. Paste your JSON in the request body
6. Click **Execute**

**Example to paste:**
```json
{
  "request_id": "demo_001",
  "input_data": {
    "property_address": "123 Main St, Springfield, IL",
    "seller_name": "John Smith",
    "buyer_name": "Jane Doe",
    "purchase_price": "$250,000",
    "closing_date": "2024-02-15"
  },
  "domain": "real_estate",
  "verbose": true,
  "include_validation": true
}
```

**You'll see:**
- Step 1: Input Validation ✅
- Step 2: Field Mapping ✅
- Step 3: Semantic Retrieval ✅
- Step 4: Validation & Compliance ✅
- Step 5: Output Generation ✅
- Final result with all processed fields

---

### Method 2️⃣: Python Script

**Create file: `run_demo.py`**
```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Your data
data = {
    "request_id": "demo_001",
    "input_data": {
        "property_address": "123 Main St, Springfield, IL",
        "seller_name": "John Smith",
        "buyer_name": "Jane Doe",
        "purchase_price": "$250,000",
        "closing_date": "2024-02-15"
    },
    "domain": "real_estate",
    "verbose": True,
    "include_validation": True
}

# Send request
print("Sending request...")
response = requests.post(f"{BASE_URL}/process", json=data)

# Display results
result = response.json()
print(f"\n✅ Success: {result['success']}")
print(f"📊 Duration: {result['total_duration_ms']:.2f}ms")

# Show each step
print("\n📋 Steps:")
for step in result['steps']:
    status = "✅" if step['status'] == 'completed' else "❌"
    print(f"{status} Step {step['step_number']}: {step['step_name']}")
    print(f"   Duration: {step['duration_ms']:.2f}ms")

# Show final output
if result['final_output']:
    print("\n🎯 Final Output:")
    print(json.dumps(result['final_output'], indent=2))
```

**Run it:**
```bash
python run_demo.py
```

---

### Method 3️⃣: cURL Command Line

**Single line - Real Estate:**
```bash
curl -X POST http://localhost:8000/process ^
  -H "Content-Type: application/json" ^
  -d "{\"request_id\":\"demo_001\",\"input_data\":{\"property_address\":\"123 Main St\",\"seller_name\":\"John Smith\",\"purchase_price\":\"$250,000\"},\"domain\":\"real_estate\",\"verbose\":true,\"include_validation\":true}"
```

**Or with a file - Save as `request.json`:**
```json
{
  "request_id": "demo_001",
  "input_data": {
    "property_address": "123 Main St, Springfield, IL",
    "seller_name": "John Smith",
    "purchase_price": "$250,000"
  },
  "domain": "real_estate",
  "verbose": true,
  "include_validation": true
}
```

Then run:
```bash
curl -X POST http://localhost:8000/process ^
  -H "Content-Type: application/json" ^
  -d @request.json
```

---

### Method 4️⃣: Upload JSON File

**Create file: `my_data.json`**
```json
{
  "property_address": "456 Oak Lane, Chicago, IL 60601",
  "seller_name": "Jane Smith",
  "buyer_name": "Michael Johnson",
  "purchase_price": "$500,000",
  "closing_date": "2024-03-01"
}
```

**Upload:**
```bash
curl -X POST http://localhost:8000/upload ^
  -F "file=@my_data.json" ^
  -F "domain=real_estate"
```

**Response:**
```json
{
  "request_id": "req_20240115_103045_123456",
  "filename": "my_data.json",
  "file_size": 256,
  "message": "File uploaded successfully. Processing started..."
}
```

**Check status:**
```bash
curl http://localhost:8000/status/req_20240115_103045_123456
```

**Get results:**
```bash
curl http://localhost:8000/results/req_20240115_103045_123456
```

---

### Method 5️⃣: Automated Test Suite

**Run all tests:**
```bash
python test_fastapi.py
```

**Output:**
```
======================================================================
  FastAPI PDF Form Processing Pipeline - Test Suite
======================================================================

🔍 Checking server connection...
✅ Server is running and responding

======================================================================
  TEST 1: Health Check
======================================================================
✅ Health check passed

======================================================================
  TEST 2: Direct Processing (REAL_ESTATE)
======================================================================
✅ Processing completed successfully
   Request ID: test_real_estate_1705330245
   Total Duration: 245.67ms

📋 Step-by-Step Results:
✅ 1. Input Validation (completed, 111.11ms)
✅ 2. Field Mapping & Normalization (completed, 134.56ms)
✅ 3. Semantic Data Retrieval (completed, 155.78ms)
✅ 4. Validation & Compliance Check (completed, 188.90ms)
✅ 5. Output Generation (completed, 89.12ms)

📊 Results: 5/5 tests passed
✅ All tests passed!
```

---

## Complete Step-by-Step Example

### Using Swagger UI (Recommended for First Time)

**1. Start Server**
```bash
python fastapi_app.py
```

**2. Open Swagger UI**
Go to: http://localhost:8000/docs

**3. Find and Click: POST /process**

**4. Click "Try it out" Button**

**5. Replace Request Body with:**
```json
{
  "request_id": "my_first_request",
  "input_data": {
    "property_address": "100 Main Street, New York, NY 10001",
    "seller_name": "Alice Brown",
    "buyer_name": "Bob Green",
    "purchase_price": "$750,000",
    "closing_date": "2024-04-15"
  },
  "domain": "real_estate",
  "verbose": true,
  "include_validation": true
}
```

**6. Click "Execute"**

**7. See Complete Output:**
```
Response body:
{
  "request_id": "my_first_request",
  "timestamp": "2024-01-15T10:30:46.234567",
  "total_duration_ms": 245.67,
  "success": true,
  "steps": [
    {
      "step_number": 1,
      "step_name": "Input Validation",
      "status": "completed",
      "duration_ms": 111.11,
      "output": {
        "validated": true,
        "field_count": 5,
        "fields": ["property_address", "seller_name", "buyer_name", "purchase_price", "closing_date"]
      }
    },
    ... (4 more steps)
  ],
  "final_output": {
    "processed_fields": {
      "property_address": {
        "value": "100 Main Street, New York, NY 10001",
        "valid": true
      },
      ... (more fields)
    }
  }
}
```

---

## Request Body Parameters

### Required Fields

```json
{
  "request_id": "unique_identifier",
  "input_data": { /* YOUR DATA */ },
  "domain": "real_estate"
}
```

### Optional Fields

```json
{
  "request_id": "unique_identifier",
  "input_data": { /* YOUR DATA */ },
  "domain": "real_estate",
  "verbose": true,              // Show detailed output
  "include_validation": true    // Include validation step
}
```

### Domain Options

- `"real_estate"` - Property transactions
- `"medical"` - Healthcare information
- `"insurance"` - Insurance policies
- `"finance"` - Financial documents
- `"legal"` - Legal documents

---

## Input Data Guidelines

### ✅ DO:
- Use descriptive field names: `"property_address"` not `"addr"`
- Use complete values: `"2024-02-15"` not `"2/15"`
- Include context: `"John Smith"` not just `"John"`
- Use standard formats: `"$250,000"` or `"250000"` for money

### ❌ DON'T:
- Leave fields empty or null
- Use special characters in field names
- Mix data types inconsistently
- Use abbreviations without explanation

---

## Sample JSON Files Provided

Three sample files are included in the project:

### 1. Real Estate
```bash
cat sample_real_estate.json
```
Uses: 11 fields for property transactions

### 2. Medical
```bash
cat sample_medical.json
```
Uses: 15 fields for patient information

### 3. Insurance
```bash
cat sample_insurance.json
```
Uses: 17 fields for policy information

---

## Expected Output Format

Every request returns:

```json
{
  "request_id": "string",
  "timestamp": "ISO 8601 datetime",
  "total_duration_ms": number,
  "success": boolean,
  "message": "string",
  "steps": [
    {
      "step_number": 1-5,
      "step_name": "string",
      "status": "completed|error",
      "duration_ms": number,
      "output": { /* step-specific output */ }
    }
  ],
  "final_output": {
    "processing_timestamp": "ISO 8601 datetime",
    "status": "SUCCESS|FAILED",
    "validation_status": "COMPLIANT|NON_COMPLIANT",
    "processed_fields": {
      "field_name": {
        "value": "any",
        "valid": boolean,
        "severity": "INFO|WARNING|CRITICAL"
      }
    }
  }
}
```

---

## Troubleshooting

### Problem: "Connection refused"
**Solution:** Make sure server is running
```bash
python fastapi_app.py
```

### Problem: "ModuleNotFoundError"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Problem: "Port 8000 already in use"
**Solution:** Kill the process or use a different port

Edit `fastapi_app.py` line 601:
```python
port=8001  # Change from 8000
```

### Problem: "Invalid JSON"
**Solution:** Validate your JSON format
```bash
python -m json.tool your_file.json
```

---

## Performance Expectations

Typical execution times:
- Health check: ~50ms
- Real Estate (5 fields): ~250ms
- Medical (10 fields): ~380ms
- Insurance (15 fields): ~520ms

---

## Next Steps

1. ✅ Start the server
2. ✅ Visit http://localhost:8000/docs
3. ✅ Try the POST /process endpoint
4. ✅ Use your own JSON data
5. ✅ Integrate into your application

---

**Ready to execute? Start with:**
```bash
python fastapi_app.py
```

Then visit: **http://localhost:8000/docs**
