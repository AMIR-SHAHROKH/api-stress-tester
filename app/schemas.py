from pydantic import BaseModel, AnyHttpUrl, Field

class StressTestRequest(BaseModel):
    url: AnyHttpUrl = Field(..., description="Target API endpoint URL")
    duration: int = Field(..., gt=0, description="Test duration in seconds")
    concurrency: int = Field(..., gt=0, description="Number of concurrent workers")

class StressTestResponse(BaseModel):
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_latency_ms: float
    throughput_rps: float