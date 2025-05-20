from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from app.schemas import StressTestRequest, StressTestResponse
from app.stress import run_stress_test, StressResult

app = FastAPI(
    title="API Stress Tester",
    description="Asynchronous API stress testing with real-time metrics.",
    version="1.0.0",
    docs_url=None,        # disable default docs
    redoc_url=None        # disable default redoc
)

# Serve a custom-themed Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="🔧 API Stress Tester Docs",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        swagger_ui_parameters={
            "docExpansion": "list",            # list endpoints by default
            "defaultModelsExpandDepth": -1,      # hide schema models section
            "persistAuthorization": True         # keep auth data on reload
        }
    )

@app.post("/stress-test", response_model=StressTestResponse)
async def stress_test(req: StressTestRequest):
    """
    Launch a stress test against the specified URL.
    """
    result: StressResult = await run_stress_test(
        url=req.url,
        duration=req.duration,
        concurrency=req.concurrency
    )
    if result.total == 0:
        raise HTTPException(status_code=400, detail="No requests were executed.")

    return StressTestResponse(
        total_requests=result.total,
        successful_requests=result.success,
        failed_requests=result.failed,
        average_latency_ms=result.avg_latency,
        throughput_rps=result.throughput
    )