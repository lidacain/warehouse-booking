from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Accounting Service Mock")

KNOWN_VINS = {
    "LVVDB21B4RD012401",
    "LVVDB21B4RD012402",
    "XWEPC81BDR0004421",
    "XWEPC81BDR0004422",
    "JN1TENT32Z0123456",
    "Z94C241BBRR108873",
    "Z94C241BBRR108880",
    "Z94C241BBRR108881",
    "Z94C241BBRR108882",
    "Z94C241BBRR108883",
    "Z94C241BBRR108884",
}


class LookupRequest(BaseModel):
    vins: list[str]


class LookupResponse(BaseModel):
    found: list[str]


@app.post("/api/v1/vehicles/lookup", response_model=LookupResponse)
async def lookup_vehicles(payload: LookupRequest) -> LookupResponse:
    found = [vin for vin in payload.vins if vin in KNOWN_VINS]
    return LookupResponse(found=found)
