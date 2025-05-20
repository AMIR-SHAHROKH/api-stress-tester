# API Stress Tester

A high-performance, asynchronous API stress testing tool built with Python and FastAPI. This project lets you:

* Launch stress tests against any API endpoint.
* Configure test parameters (URL, duration, concurrency) via API or CLI.
* View real-time results through a web interface with Swagger UI documentation.
* Run locally with a virtual environment or containerize with Docker.

---

## Features

* **FastAPI**: Provides a RESTful interface with automatic OpenAPI/Swagger UI documentation.
* **Async HTTP Requests**: Uses `aiohttp` to maximize concurrency and throughput.
* **Configurable**: Customize target URL, test duration, concurrency level, and request rate.
* **Results Summary**: Returns total requests, success/failure counts, average latency, and throughput.
* **Dockerized**: Prebuilt `Dockerfile` for easy deployment.

---

## Project Structure

```
api-stress-tester/
├── app/
│   ├── main.py         # FastAPI application
│   ├── stress.py       # Core stress testing logic
│   └── schemas.py      # Pydantic models for request/response
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

* Python 3.11+
* Git
* (Optional) Docker

### Local Setup (venv)

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/api-stress-tester.git
   cd api-stress-tester
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run the API server**

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the Swagger UI**
   Open your browser and navigate to:

   ```
   http://localhost:8000/docs
   ```

You can also use the Redoc UI at `http://localhost:8000/redoc`.

### Running Without Docker

Yes! When using a virtual environment, you can run the application directly with Uvicorn as shown above. There is no need for Docker unless you want containerized deployment.

---

## Usage

### API Endpoint

`POST /stress-test`

**Request Body** (application/json):

```json
{
  "url": "https://jsonplaceholder.typicode.com/posts",
  "duration": 60,
  "concurrency": 100
}
```

* `url` (string): Target API endpoint.
* `duration` (integer): Test duration in seconds.
* `concurrency` (integer): Number of concurrent requests.

**Response** (application/json):

```json
{
  "total_requests": 12000,
  "successful_requests": 11950,
  "failed_requests": 50,
  "average_latency_ms": 45.23,
  "throughput_rps": 200.00
}
```

### CLI Script

You can also run the stress test directly without the API server:

```bash
python app/main.py \
  --url https://jsonplaceholder.typicode.com/posts \
  --duration 60 \
  --concurrency 100
```

Use `--help` for more options.

---

## Docker Usage

1. **Build the image**

   ```bash
   docker build -t api-stress-tester:latest .
   ```

2. **Run the container**

   ```bash
   docker run --rm -p 8000:8000 api-stress-tester:latest
   ```

3. **Open Swagger UI**
   Navigate to `http://localhost:8000/docs`.

---

## Swagger / OpenAPI Specification

This project uses FastAPI to automatically generate an OpenAPI schema. You can find the raw JSON/YAML at:

* JSON: `http://localhost:8000/openapi.json`
* YAML: `http://localhost:8000/openapi.yaml`

Feel free to import the schema into Postman or any other API tool.

---

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m "Add my feature"`
4. Push to branch: `git push origin feature/my-feature`
5. Open a Pull Request.

Please follow the existing code style and include tests for new functionality.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
