from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import numpy as np

app = FastAPI()

# Enhanced CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=86400,
)

DATA = [{"region":"apac","service":"analytics","latency_ms":197.32,"uptime_pct":98.278,"timestamp":20250301},{"region":"apac","service":"recommendations","latency_ms":206.54,"uptime_pct":98.04,"timestamp":20250302},{"region":"apac","service":"support","latency_ms":186.32,"uptime_pct":97.397,"timestamp":20250303},{"region":"apac","service":"checkout","latency_ms":189.95,"uptime_pct":97.227,"timestamp":20250304},{"region":"apac","service":"payments","latency_ms":182.06,"uptime_pct":98.346,"timestamp":20250305},{"region":"apac","service":"payments","latency_ms":213.32,"uptime_pct":99.126,"timestamp":20250306},{"region":"apac","service":"analytics","latency_ms":112.05,"uptime_pct":97.307,"timestamp":20250307},{"region":"apac","service":"catalog","latency_ms":186.49,"uptime_pct":99.281,"timestamp":20250308},{"region":"apac","service":"support","latency_ms":205.84,"uptime_pct":97.436,"timestamp":20250309},{"region":"apac","service":"checkout","latency_ms":165.17,"uptime_pct":98.891,"timestamp":20250310},{"region":"apac","service":"checkout","latency_ms":126.26,"uptime_pct":98.9,"timestamp":20250311},{"region":"apac","service":"support","latency_ms":165.12,"uptime_pct":99.301,"timestamp":20250312},{"region":"emea","service":"payments","latency_ms":126.41,"uptime_pct":99.169,"timestamp":20250301},{"region":"emea","service":"checkout","latency_ms":192.06,"uptime_pct":98.3,"timestamp":20250302},{"region":"emea","service":"support","latency_ms":193.82,"uptime_pct":97.235,"timestamp":20250303},{"region":"emea","service":"support","latency_ms":205.62,"uptime_pct":98.515,"timestamp":20250304},{"region":"emea","service":"catalog","latency_ms":184.76,"uptime_pct":98.652,"timestamp":20250305},{"region":"emea","service":"support","latency_ms":129.74,"uptime_pct":99.365,"timestamp":20250306},{"region":"emea","service":"catalog","latency_ms":141.99,"uptime_pct":97.861,"timestamp":20250307},{"region":"emea","service":"checkout","latency_ms":140.2,"uptime_pct":98.959,"timestamp":20250308},{"region":"emea","service":"recommendations","latency_ms":136.9,"uptime_pct":97.209,"timestamp":20250309},{"region":"emea","service":"checkout","latency_ms":151.26,"uptime_pct":98.907,"timestamp":20250310},{"region":"emea","service":"checkout","latency_ms":159.53,"uptime_pct":98.489,"timestamp":20250311},{"region":"emea","service":"analytics","latency_ms":136.05,"uptime_pct":97.543,"timestamp":20250312},{"region":"amer","service":"payments","latency_ms":163.47,"uptime_pct":99.375,"timestamp":20250301},{"region":"amer","service":"support","latency_ms":167.37,"uptime_pct":97.512,"timestamp":20250302},{"region":"amer","service":"payments","latency_ms":186.85,"uptime_pct":97.31,"timestamp":20250303},{"region":"amer","service":"analytics","latency_ms":184.97,"uptime_pct":97.333,"timestamp":20250304},{"region":"amer","service":"payments","latency_ms":219.35,"uptime_pct":99.423,"timestamp":20250305},{"region":"amer","service":"catalog","latency_ms":175.77,"uptime_pct":97.652,"timestamp":20250306},{"region":"amer","service":"payments","latency_ms":205.36,"uptime_pct":98.193,"timestamp":20250307},{"region":"amer","service":"recommendations","latency_ms":212.6,"uptime_pct":99.294,"timestamp":20250308},{"region":"amer","service":"catalog","latency_ms":198.46,"uptime_pct":97.919,"timestamp":20250309},{"region":"amer","service":"checkout","latency_ms":110.19,"uptime_pct":99.105,"timestamp":20250310},{"region":"amer","service":"support","latency_ms":231.76,"uptime_pct":97.216,"timestamp":20250311},{"region":"amer","service":"support","latency_ms":182.55,"uptime_pct":98.595,"timestamp":20250312}]

class LatencyRequest(BaseModel):
    regions: List[str]
    threshold_ms: float

@app.get("/")
def read_root(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return {"message": "Latency API is running"}

@app.post("/analyze")
def analyze_latency(request: LatencyRequest, response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    
    regions_data = []
    for region in request.regions:
        region_data = [r for r in DATA if r["region"] == region]
        if not region_data:
            region_result = {
                "region": region,
                "avg_latency": 0, 
                "p95_latency": 0, 
                "avg_uptime": 0, 
                "breaches": 0
            }
        else:
            latencies = [r["latency_ms"] for r in region_data]
            uptimes = [r["uptime_pct"] for r in region_data]
            avg_latency = round(float(np.mean(latencies)), 2)
            p95_latency = round(float(np.percentile(latencies, 95)), 2)
            avg_uptime = round(float(np.mean(uptimes)), 2)
            breaches = sum(1 for lat in latencies if lat > request.threshold_ms)
            region_result = {
                "region": region,
                "avg_latency": avg_latency, 
                "p95_latency": p95_latency, 
                "avg_uptime": avg_uptime, 
                "breaches": breaches
            }
        regions_data.append(region_result)
    
    return {
        "regions": regions_data,
        "threshold_ms": request.threshold_ms,
        "total_regions": len(request.regions)
    }

@app.options("/{path:path}")
def options_handler(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept, Origin, User-Agent, DNT, Cache-Control, X-Mx-ReqToken, Keep-Alive, X-Requested-With, If-Modified-Since"
    response.headers["Access-Control-Max-Age"] = "86400"
    response.status_code = 200
    return {"status": "OK"}

# Additional global OPTIONS handler for root
@app.options("/")
def root_options_handler(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept, Origin, User-Agent, DNT, Cache-Control, X-Mx-ReqToken, Keep-Alive, X-Requested-With, If-Modified-Since"
    response.headers["Access-Control-Max-Age"] = "86400"
    response.status_code = 200
    return {"status": "OK"}