from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# The community-verified CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Access-Control-Allow-Origin"],
)

# Embedded telemetry bundle
DATA = [
    {"region": "apac", "service": "catalog", "latency_ms": 200.63, "uptime_pct": 97.657, "timestamp": 20250301},
    {"region": "apac", "service": "payments", "latency_ms": 102.46, "uptime_pct": 98.72, "timestamp": 20250302},
    {"region": "apac", "service": "checkout", "latency_ms": 192.95, "uptime_pct": 97.189, "timestamp": 20250303},
    {"region": "apac", "service": "catalog", "latency_ms": 145.22, "uptime_pct": 98.341, "timestamp": 20250304},
    {"region": "apac", "service": "support", "latency_ms": 139.09, "uptime_pct": 98.065, "timestamp": 20250305},
    {"region": "apac", "service": "support", "latency_ms": 233.49, "uptime_pct": 97.819, "timestamp": 20250306},
    {"region": "apac", "service": "analytics", "latency_ms": 195.94, "uptime_pct": 99.222, "timestamp": 20250307},
    {"region": "apac", "service": "recommendations", "latency_ms": 167.02, "uptime_pct": 97.847, "timestamp": 20250308},
    {"region": "apac", "service": "payments", "latency_ms": 141.23, "uptime_pct": 99.065, "timestamp": 20250309},
    {"region": "apac", "service": "checkout", "latency_ms": 186.96, "uptime_pct": 97.278, "timestamp": 20250310},
    {"region": "apac", "service": "payments", "latency_ms": 154.13, "uptime_pct": 98.57, "timestamp": 20250311},
    {"region": "apac", "service": "recommendations", "latency_ms": 133.93, "uptime_pct": 97.529, "timestamp": 20250312},
    {"region": "emea", "service": "checkout", "latency_ms": 158.2, "uptime_pct": 98.006, "timestamp": 20250301},
    {"region": "emea", "service": "catalog", "latency_ms": 195.9, "uptime_pct": 97.26, "timestamp": 20250302},
    {"region": "emea", "service": "recommendations", "latency_ms": 142.66, "uptime_pct": 98.236, "timestamp": 20250303},
    {"region": "emea", "service": "recommendations", "latency_ms": 127.2, "uptime_pct": 97.322, "timestamp": 20250304},
    {"region": "emea", "service": "catalog", "latency_ms": 147.93, "uptime_pct": 98.97, "timestamp": 20250305},
    {"region": "emea", "service": "recommendations", "latency_ms": 188.37, "uptime_pct": 97.749, "timestamp": 20250306},
    {"region": "emea", "service": "catalog", "latency_ms": 133.14, "uptime_pct": 98.216, "timestamp": 20250307},
    {"region": "emea", "service": "catalog", "latency_ms": 143.96, "uptime_pct": 98.783, "timestamp": 20250308},
    {"region": "emea", "service": "recommendations", "latency_ms": 138.16, "uptime_pct": 97.412, "timestamp": 20250309},
    {"region": "emea", "service": "catalog", "latency_ms": 138.17, "uptime_pct": 99.383, "timestamp": 20250310},
    {"region": "emea", "service": "payments", "latency_ms": 173.21, "uptime_pct": 98.404, "timestamp": 20250311},
    {"region": "emea", "service": "support", "latency_ms": 151.06, "uptime_pct": 97.3, "timestamp": 20250312},
    {"region": "amer", "service": "payments", "latency_ms": 179.23, "uptime_pct": 98.795, "timestamp": 20250301},
    {"region": "amer", "service": "support", "latency_ms": 203.72, "uptime_pct": 98.928, "timestamp": 20250302},
    {"region": "amer", "service": "payments", "latency_ms": 106.63, "uptime_pct": 98.452, "timestamp": 20250303},
    {"region": "amer", "service": "catalog", "latency_ms": 139.31, "uptime_pct": 97.615, "timestamp": 20250304},
    {"region": "amer", "service": "checkout", "latency_ms": 213.89, "uptime_pct": 99.421, "timestamp": 20250305},
    {"region": "amer", "service": "support", "latency_ms": 127.1, "uptime_pct": 97.914, "timestamp": 20250306},
    {"region": "amer", "service": "payments", "latency_ms": 161.35, "uptime_pct": 98.81, "timestamp": 20250307},
    {"region": "amer", "service": "payments", "latency_ms": 219.17, "uptime_pct": 99.4, "timestamp": 20250308},
    {"region": "amer", "service": "support", "latency_ms": 186.15, "uptime_pct": 97.924, "timestamp": 20250309},
    {"region": "amer", "service": "catalog", "latency_ms": 146.46, "uptime_pct": 97.829, "timestamp": 20250310},
    {"region": "amer", "service": "support", "latency_ms": 139.55, "uptime_pct": 98.306, "timestamp": 20250311},
    {"region": "amer", "service": "recommendations", "latency_ms": 138.94, "uptime_pct": 98.19, "timestamp": 20250312}
]

class RequestPayload(BaseModel):
    regions: List[str]
    threshold_ms: float

def calculate_p95(data: List[float]) -> float:
    if not data: return 0.0
    sorted_data = sorted(data)
    idx = (len(sorted_data) - 1) * 0.95
    lower = int(idx)
    upper = lower + 1
    weight = idx - lower
    
    if upper >= len(sorted_data):
        return float(sorted_data[lower])
    return float(sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight)

@app.post("/api/metrics")
def get_metrics(payload: RequestPayload):
    results = {}
    
    for region in payload.regions:
        region_data = [d for d in DATA if d["region"] == region]
        if not region_data:
            continue
            
        latencies = [d["latency_ms"] for d in region_data]
        uptimes = [d["uptime_pct"] for d in region_data]
        
        avg_latency = sum(latencies) / len(latencies)
        p95_latency = calculate_p95(latencies)
        avg_uptime = sum(uptimes) / len(uptimes)
        breaches = sum(1 for l in latencies if l > payload.threshold_ms)
        
        results[region] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches
        }
        
    # THE FIX: Wrap the results inside a "regions" key
    return {"regions": results}
