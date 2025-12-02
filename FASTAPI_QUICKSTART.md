# 🚀 FastAPI Quick Start Guide

Complete step-by-step guide to running the PDF Form Processing FastAPI application.

---

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Basic command line knowledge

---

## ⚡ 5-Minute Quick Start

### Step 1: Install Dependencies

```bash
cd d:\2-12-cidc
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi-0.104.0 uvicorn-0.24.0 pydantic-2.0.0 ...
```

### Step 2: Start the Server

```bash
python fastapi_app.py
```

**Expected output:**
```
======================================================================
🚀 PDF Form Processing Pipeline - FastAPI Server Starting
======================================================================
Timestamp: 2024-01-15T10:30:45.123456
Endpoints available:
  - POST /upload         : Upload JSON file for processing
  - POST /process        : Process JSON data directly
  - GET  /status/{request_id}  : Get processing status
  - GET  /results/{request_id} : Get final results
  - GET  /health         : Health check
  - GET  /docs           : API documentation
======================================================================
```

✅ Server is running! It will stay running in this terminal.

### Step 3: Open API Documentation

In a new terminal or browser, open:
```
http://localhost:8000/docs
```

You should see the **Swagger UI** with all available endpoints.

### Step 4: Test with Sample Data

Open another terminal and run:

```bash
python test_fastapi.py
```

This will run all tests and show detailed output.

---

## 🧪 Detailed Testing Steps

### Option 1: Using Python Script (Recommended)

```bash
# In a new terminal
python test_fastapi.py
```

**Output:**
```
======================================================================
  FastAPI PDF Form Processing Pipeline - Test Suite
======================================================================
Base URL: http://localhost:8000
Timeout: 30s
======================================================================

🔍 Checking server connection...
✅ Server is running and responding

======================================================================
  TEST 1: Health Check
======================================================================
✅ Health check passed
   Status: healthy
   Timestamp: 2024-01-15T10:30:45.123456
   Version: 1.0.0

======================================================================
  TEST 2: Direct Processing (REAL_ESTATE)
======================================================================
📨 Sending request with 5 fields...

✅ Processing completed successfully
   Request ID: test_real_estate_1705330245
   Total Duration: 245.67ms
   Steps Completed: 5
   Success: True

📋 Step-by-Step Results:

✅ 1. Input Validation
   Status: completed
   Duration: 111.11ms
   Validated Fields: 5

✅ 2. Field Mapping & Normalization
   Status: completed
   Duration: 134.56ms
   Mapped Fields: 5

✅ 3. Semantic Data Retrieval
   Status: completed
   Duration: 155.78ms
   Retrieved Values: 5

✅ 4. Validation & Compliance Check
   Status: completed
   Duration: 188.90ms
   Valid Fields: 5/5

✅ 5. Output Generation
   Status: completed
   Duration: 89.12ms
   Output Fields: 5

🎯 Final Output:
   Status: SUCCESS
   Validation Status: COMPLIANT
   Processed Fields: 5

[... more tests ...]

📊 Results: 5/5 tests passed
✅ All tests passed!
```

---

### Option 2: Using cURL (Command Line)

#### Test Health Check
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456",
  "version": "1.0.0"
}
```

#### Process Real Estate Data
```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d "{
    \"request_id\": \"demo_001\",
    \"input_data\": {
      \"property_address\": \"123 Main St, Springfield, IL\",
      \"seller_name\": \"John Smith\",
      \"buyer_name\": \"Jane Doe\",
      \"purchase_price\": \"$250,000\",
      \"closing_date\": \"2024-02-15\"
    },
    \"domain\": \"real_estate\",
    \"verbose\": true,
    \"include_validation\": true
  }"
```

**Response (simplified):**
```json
{
  "request_id": "demo_001",
  "timestamp": "2024-01-15T10:30:46.234567",
  "total_duration_ms": 245.67,
  "success": true,
  "steps": [
    {
      "step_number": 1,
      "step_name": "Input Validation",
      "status": "completed",
      "duration_ms": 111.11
    },
    ...
  ]
}
```

#### Upload JSON File
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@sample_real_estate.json" \
  -F "domain=real_estate"
```

**Response:**
```json
{
  "request_id": "req_20240115_103045_123456",
  "filename": "sample_real_estate.json",
  "file_size": 1024,
  "message": "File uploaded successfully. Processing started..."
}
```

#### Check Upload Status
```bash
curl http://localhost:8000/status/req_20240115_103045_123456
```

---

### Option 3: Using Python Requests

Create a file `test_simple.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Test 1: Health check
print("1️⃣  Testing health check...")
response = requests.get(f"{BASE_URL}/health")
print(f"   Status: {response.json()['status']}")

# Test 2: Process real estate data
print("\n2️⃣  Processing real estate data...")
data = {
    "request_id": "demo_001",
    "input_data": {
        "property_address": "123 Main St",
        "seller_name": "John Smith",
        "purchase_price": "$250,000"
    },
    "domain": "real_estate",
    "verbose": False,
    "include_validation": True
}

response = requests.post(f"{BASE_URL}/process", json=data)
result = response.json()

print(f"   Success: {result['success']}")
print(f"   Duration: {result['total_duration_ms']:.2f}ms")
print(f"   Steps: {len(result['steps'])}")

# Show each step
for step in result['steps']:
    print(f"   ✓ Step {step['step_number']}: {step['step_name']} ({step['status']})")

# Test 3: Process medical data
print("\n3️⃣  Processing medical data...")
medical_data = {
    "request_id": "demo_002",
    "input_data": {
        "patient_name": "Robert Johnson",
        "date_of_birth": "1970-06-15",
        "diagnosis": "Hypertension",
        "medication": "Lisinopril 10mg"
    },
    "domain": "medical",
    "verbose": False,
    "include_validation": True
}

response = requests.post(f"{BASE_URL}/process", json=medical_data)
result = response.json()

print(f"   Success: {result['success']}")
print(f"   Duration: {result['total_duration_ms']:.2f}ms")

print("\n✅ All tests completed!")
```

Run it:
```bash
python test_simple.py
```

---

## 📁 Working with JSON Files

### Sample Files Included

The project includes 3 sample JSON files:

1. **sample_real_estate.json** - Property transaction data
2. **sample_medical.json** - Patient medical information
3. **sample_insurance.json** - Insurance policy data

### Using Sample Files

#### Upload via cURL
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@sample_real_estate.json" \
  -F "domain=real_estate"
```

#### Upload via Python
```python
import requests

with open('sample_real_estate.json', 'rb') as f:
    files = {'file': f}
    params = {'domain': 'real_estate'}
    response = requests.post(
        'http://localhost:8000/upload',
        files=files,
        params=params
    )
    
request_id = response.json()['request_id']
print(f"Request ID: {request_id}")

# Check status
import time
time.sleep(2)

status = requests.get(f'http://localhost:8000/status/{request_id}')
print(f"Status: {status.json()['status']}")
```

### Creating Your Own JSON

Create a file `my_data.json`:

```json
{
  "property_address": "456 Oak Lane, Chicago, IL 60601",
  "seller_name": "Jane Smith",
  "buyer_name": "Michael Johnson",
  "purchase_price": "$500,000",
  "closing_date": "2024-03-01"
}
```

Then upload:
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@my_data.json" \
  -F "domain=real_estate"
```

---

## 🎯 Understanding the Output

### Step Breakdown

When processing completes, you get 5 steps:

**Step 1: Input Validation** ✅
```
Status: completed
Duration: 111.11ms
Output: 
  - Validated: true
  - Field count: 5
  - Errors: none
```

**Step 2: Field Mapping & Normalization** ✅
```
Status: completed
Duration: 134.56ms
Output:
  - Mapped count: 5
  - Unmapped count: 0
  - Domain: real_estate
```

**Step 3: Semantic Data Retrieval** ✅
```
Status: completed
Duration: 155.78ms
Output:
  - Retrieval count: 5
  - Confidence scores: 0.95+
  - KB used: true
```

**Step 4: Validation & Compliance** ✅
```
Status: completed
Duration: 188.90ms
Output:
  - Valid count: 5
  - Invalid count: 0
  - Compliance status: COMPLIANT
```

**Step 5: Output Generation** ✅
```
Status: completed
Duration: 89.12ms
Output:
  - Field count: 5
  - Timestamp: 2024-01-15T10:30:46.234567
```

---

## 🐛 Troubleshooting

### Problem: "Connection refused"
**Solution:** Make sure the server is running in another terminal:
```bash
python fastapi_app.py
```

### Problem: "ModuleNotFoundError: No module named 'fastapi'"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Problem: "Address already in use"
**Solution:** The port 8000 is already in use. Either:
1. Stop the other process using port 8000
2. Or edit fastapi_app.py and change port 8000 to another (e.g., 8001)

### Problem: Tests fail with timeout
**Solution:** Increase the timeout in test_fastapi.py:
```python
TIMEOUT = 60  # Increase from 30
```

### Problem: File upload shows "Invalid JSON format"
**Solution:** Make sure your JSON file is valid:
```bash
python -m json.tool your_file.json
```

---

## 📊 Performance Metrics

Typical execution times:

| Domain | Total Time | Per Field |
|--------|-----------|-----------|
| Real Estate (5 fields) | 245ms | 49ms |
| Medical (10 fields) | 380ms | 38ms |
| Insurance (15 fields) | 520ms | 34ms |

**Note:** First request may be slightly slower due to module loading.

---

## 🔗 API Reference Quick Links

- **Full API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

---

## 📚 Example Workflows

### Workflow 1: Single Request Processing

```python
import requests

# 1. Send data
response = requests.post('http://localhost:8000/process', json={
    'request_id': 'workflow_001',
    'input_data': {'seller_name': 'John', 'property': '123 Main'},
    'domain': 'real_estate'
})

# 2. Get result
result = response.json()

# 3. Check if successful
if result['success']:
    print(f"✅ Processed in {result['total_duration_ms']:.2f}ms")
    for step in result['steps']:
        print(f"  {step['step_name']}: {step['status']}")
```

### Workflow 2: Batch Processing

```python
import requests

domains = ['real_estate', 'medical', 'insurance']
for domain in domains:
    response = requests.post('http://localhost:8000/process', json={
        'request_id': f'batch_{domain}',
        'input_data': {...},
        'domain': domain
    })
    result = response.json()
    print(f"{domain}: {result['success']}")
```

### Workflow 3: File Upload with Polling

```python
import requests
import time

# Upload
with open('data.json', 'rb') as f:
    response = requests.post('http://localhost:8000/upload',
        files={'file': f},
        params={'domain': 'real_estate'}
    )

request_id = response.json()['request_id']

# Poll status
for i in range(10):
    status = requests.get(f'http://localhost:8000/status/{request_id}')
    if status.json()['status'] == 'completed':
        break
    time.sleep(1)

# Get results
results = requests.get(f'http://localhost:8000/results/{request_id}')
print(results.json())
```

---

## 🎓 Next Steps

1. ✅ Run the test suite (`python test_fastapi.py`)
2. ✅ Explore the interactive API docs (`http://localhost:8000/docs`)
3. ✅ Process your own JSON files
4. ✅ Integrate into your application
5. ✅ Customize domains and validation rules

---

## 📞 Help & Support

- Check `/docs` for interactive documentation
- Review `README_FASTAPI.md` for detailed API reference
- Check `test_fastapi.py` for usage examples
- Look at sample JSON files for data structure examples

---

**Happy processing! 🎉**
