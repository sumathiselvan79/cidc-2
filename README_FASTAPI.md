# FastAPI PDF Form Processing Pipeline

Complete FastAPI REST API for processing PDF form fields with semantic intelligence and multi-step validation.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
python fastapi_app.py
```

The server will start at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## 📊 Processing Pipeline

The FastAPI application processes JSON data through 5 sequential steps:

```
┌─────────────────────────────────────────────────────────────┐
│                   INPUT JSON FILE                           │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
    ┌─────────────────────┐
    │ STEP 1: VALIDATION  │ ✅ Validate JSON structure
    └────────┬────────────┘    Check required fields
             │                 Normalize format
             ▼
    ┌─────────────────────┐
    │ STEP 2: MAPPING     │ ✅ Map fields to schema
    └────────┬────────────┘    Apply normalization
             │                 Extract metadata
             ▼
    ┌─────────────────────┐
    │ STEP 3: RETRIEVAL   │ ✅ Semantic matching
    └────────┬────────────┘    Domain knowledge base
             │                 Confidence scoring
             ▼
    ┌─────────────────────┐
    │ STEP 4: VALIDATION  │ ✅ Field-level validation
    └────────┬────────────┘    Cross-field checking
             │                 Compliance rules
             ▼
    ┌─────────────────────┐
    │ STEP 5: OUTPUT      │ ✅ Generate final output
    └────────┬────────────┘    Compliance report
             │                 Summary statistics
             ▼
        ┌──────────────┐
        │ JSON RESULT  │
        └──────────────┘
```

## 🔌 API Endpoints

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456",
  "version": "1.0.0"
}
```

---

### Process Data Directly

```http
POST /process
```

**Request Body:**
```json
{
  "request_id": "req_unique_identifier",
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

**Response:**
```json
{
  "request_id": "req_unique_identifier",
  "timestamp": "2024-01-15T10:30:46.234567",
  "total_duration_ms": 245.67,
  "success": true,
  "message": "Processing completed successfully",
  "steps": [
    {
      "step_number": 1,
      "step_name": "Input Validation",
      "status": "completed",
      "start_time": "2024-01-15T10:30:45.234567",
      "end_time": "2024-01-15T10:30:45.345678",
      "duration_ms": 111.11,
      "output": {
        "validated": true,
        "field_count": 3,
        "fields": ["property_address", "seller_name", "purchase_price"],
        "errors": []
      }
    },
    ...more steps...
  ],
  "final_output": {
    "processing_timestamp": "2024-01-15T10:30:46.234567",
    "status": "SUCCESS",
    "validation_status": "COMPLIANT",
    "processed_fields": {
      "property_address": {
        "value": "123 Main St, Springfield, IL",
        "valid": true,
        "severity": "INFO"
      },
      ...more fields...
    }
  }
}
```

---

### Upload JSON File

```http
POST /upload
```

**Form Data:**
- `file`: JSON file (multipart/form-data)
- `domain`: Domain type (query parameter)

**Response:**
```json
{
  "request_id": "req_20240115_103045_123456",
  "filename": "form_data.json",
  "file_size": 1024,
  "message": "File uploaded successfully. Processing started..."
}
```

---

### Get Processing Status

```http
GET /status/{request_id}
```

**Response:**
```json
{
  "request_id": "req_20240115_103045_123456",
  "status": "completed",
  "upload_time": "2024-01-15T10:30:45.123456",
  "domain": "real_estate",
  "steps_completed": 5,
  "message": "Processing in progress or completed"
}
```

---

### Get Processing Results

```http
GET /results/{request_id}
```

**Response:**
```json
{
  "request_id": "req_20240115_103045_123456",
  "filename": "form_data.json",
  "status": "completed",
  "steps": [...],
  "final_output": {...},
  "timestamp": "2024-01-15T10:30:50.234567"
}
```

---

## 📝 Domain Types

The system supports multiple domains:

| Domain | Description | Key Fields |
|--------|-------------|-----------|
| `real_estate` | Property transactions | Address, Seller, Buyer, Price, Closing Date |
| `medical` | Healthcare information | Patient Name, DOB, Diagnosis, Medication |
| `insurance` | Insurance policies | Policy Holder, Policy #, Coverage, Premium |
| `finance` | Financial documents | Account, Amount, Interest Rate, Term |
| `legal` | Legal documents | Party Names, Jurisdiction, Case #, Dates |

---

## 💻 Usage Examples

### Python (using requests)

```python
import requests

# Direct processing
response = requests.post(
    "http://localhost:8000/process",
    json={
        "request_id": "test_001",
        "input_data": {
            "property_address": "123 Main St",
            "seller_name": "John Smith",
            "purchase_price": "$250,000"
        },
        "domain": "real_estate",
        "verbose": True,
        "include_validation": True
    }
)

result = response.json()
print(f"Request ID: {result['request_id']}")
print(f"Success: {result['success']}")
print(f"Duration: {result['total_duration_ms']:.2f}ms")

for step in result['steps']:
    print(f"Step {step['step_number']}: {step['step_name']} - {step['status']}")
```

### cURL

```bash
# Health check
curl http://localhost:8000/health

# Process data
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "test_001",
    "input_data": {
      "property_address": "123 Main St",
      "seller_name": "John Smith"
    },
    "domain": "real_estate",
    "verbose": true,
    "include_validation": true
  }'

# Upload file
curl -X POST http://localhost:8000/upload \
  -F "file=@data.json" \
  -F "domain=real_estate"

# Check status
curl http://localhost:8000/status/req_20240115_103045_123456

# Get results
curl http://localhost:8000/results/req_20240115_103045_123456
```

### JavaScript/Node.js

```javascript
const response = await fetch('http://localhost:8000/process', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    request_id: 'test_001',
    input_data: {
      property_address: '123 Main St',
      seller_name: 'John Smith'
    },
    domain: 'real_estate',
    verbose: true,
    include_validation: true
  })
});

const result = await response.json();
console.log(`Status: ${result.success ? 'SUCCESS' : 'FAILED'}`);
console.log(`Duration: ${result.total_duration_ms.toFixed(2)}ms`);

result.steps.forEach(step => {
  console.log(`${step.step_number}. ${step.step_name}: ${step.status}`);
});
```

---

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_fastapi.py
```

The test suite includes:
- ✅ Health check
- ✅ Direct processing (all domains)
- ✅ File upload and background processing
- ✅ Multi-domain processing

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
   ...

📊 Results: 5/5 tests passed
✅ All tests passed!
```

---

## 📊 Step Descriptions

### Step 1: Input Validation
- Validates JSON structure
- Checks required fields
- Normalizes data format
- **Output**: Validation status and field count

### Step 2: Field Mapping & Normalization
- Maps input fields to standard schema
- Applies domain-specific normalization
- Extracts field metadata
- **Output**: Mapped field list with types

### Step 3: Semantic Data Retrieval
- Applies semantic matching for values
- Uses domain knowledge bases
- Generates confidence scores
- **Output**: Retrieved values with confidence

### Step 4: Validation & Compliance
- Validates data against rules
- Checks domain-specific requirements
- Generates compliance status
- **Output**: Validation results with severity

### Step 5: Output Generation
- Prepares final output data
- Generates processing summary
- Creates compliance report
- **Output**: Final processed JSON

---

## 🔒 Error Handling

The API returns appropriate HTTP status codes:

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 400 | Invalid JSON format or request |
| 404 | Request ID not found |
| 500 | Server error during processing |

**Error Response:**
```json
{
  "detail": "Invalid JSON format: Expecting value: line 1 column 1"
}
```

---

## 📈 Performance

Typical processing times per step:

| Step | Duration |
|------|----------|
| Step 1: Validation | 50-150ms |
| Step 2: Mapping | 100-200ms |
| Step 3: Retrieval | 150-300ms |
| Step 4: Validation | 100-250ms |
| Step 5: Output | 50-100ms |
| **Total** | **~500-1000ms** |

---

## 🔧 Configuration

Edit `fastapi_app.py` to modify:

- **Host**: Line 600 (default: `0.0.0.0`)
- **Port**: Line 601 (default: `8000`)
- **Log Level**: Line 602 (options: `critical`, `error`, `warning`, `info`, `debug`)
- **Workers**: Add `workers=4` parameter for multi-process

---

## 📚 Project Structure

```
d:\2-12-cidc\
├── fastapi_app.py              # Main FastAPI application
├── test_fastapi.py             # Comprehensive test suite
├── requirements.txt            # Python dependencies
├── step3_semantic_retrieval.py  # Semantic retrieval engine
├── knowledge_bases.py          # Domain knowledge bases
├── field_mapper.py             # ML-based field mapping
├── validators.py               # Data validation engine
└── README_FASTAPI.md          # This file
```

---

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "fastapi_app.py"]
```

Build and run:
```bash
docker build -t pdf-processing-api .
docker run -p 8000:8000 pdf-processing-api
```

### Production Settings

For production deployment:

1. Use `gunicorn` with `uvicorn` workers:
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker fastapi_app:app --bind 0.0.0.0:8000
```

2. Use HTTPS/SSL
3. Add authentication (OAuth2, API Keys)
4. Implement rate limiting
5. Add logging and monitoring

---

## 📞 Support

For issues or questions:

1. Check API documentation at `/docs`
2. Review test examples in `test_fastapi.py`
3. Check server logs for detailed error messages
4. Verify all dependencies are installed: `pip install -r requirements.txt`

---

## 📄 License

Part of the PDF Form Processing Enhancement Project

---

## 🎯 Next Steps

- ✅ Deploy to production environment
- ✅ Add authentication and API keys
- ✅ Implement rate limiting
- ✅ Add monitoring and logging
- ✅ Extend with more domains
- ✅ Integrate ML models for better retrieval
