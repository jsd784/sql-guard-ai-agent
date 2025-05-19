# SQL Guard AI Agent

## Overview

The **SQL Guard AI Agent** analyzes incoming SQL queries for potential security risks such as:

- SQL injection
- Sensitive data access
- Administrative privilege misuse.

It uses an LLM (Azure OpenAI) to classify the risk level of the query as one of:

- `high`
- `medium`
- `low`

This agent returns the analysis, classification reason, and optionally the query result, in a structured JSON format — making it suitable for automated testing or embedding into broader security workflows.

This is powered by **LangServe** and served via a FastAPI-compatible REST API.

---

## Requirements

- Python 3.10+
- A virtual environment is recommended.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/jsd784/sql-guard-ai-agent
   cd sql-guard-ai-agent
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Setup

1. Set the following environment variables:

   ```env
   AZURE_OPENAI_API_KEY=your-azure-api-key
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
   AZURE_OPENAI_API_VERSION=2025-01-01-preview
   ```

---

## Running the LangServe API

1. Start the server with:

   ```bash
   python server.py
   ```

   By default, this launches the app at [http://localhost:8000](http://localhost:8000)

2. Access the API docs:

   Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the OpenAPI interface.

---

## Sample API Request

```bash
curl -X POST http://localhost:8000/sql-guard/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "sql_query": "SELECT * FROM customers LIMIT 1;",
      "ip_address": "191.0.0.5"
    }
  }'
```

---

## Output

A successful response will return:

```json
{
  "output": {
    "status": "not banned",
    "risk": "low",
    "reason": "The query retrieves a single record from the customers table without any filtering or user input, minimizing the risk of SQL injection or sensitive data leaks.",
    "query_result": [
      {
        "CustomerId": 1,
        "FirstName": "Luís",
        "LastName": "Gonçalves",
        "Company": "Embraer - Empresa Brasileira de Aeronáutica S.A.",
        "Address": "Av. Brigadeiro Faria Lima, 2170",
        "City": "São José dos Campos",
        "State": "SP",
        "Country": "Mars",
        "PostalCode": "12227-000",
        "Phone": "+55 (12) 3923-5555",
        "Fax": "+55 (12) 3923-5566",
        "Email": "luisg@embraer.com.br",
        "SupportRepId": 3
      }
    ],
    "error": ""
  },
  "metadata": {
    "run_id": "f77f5e12-1ac5-45b9-b6f8-52d8f8b2f093",
    "feedback_tokens": []
  }
}
```

---

## License

This project is licensed under the Apache-2.0 License.
