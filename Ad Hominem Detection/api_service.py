from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="Ad Hominem Detection API", version="0.1.0")


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    is_ad_hominem: bool
    confidence: float
    prediction: str


def heuristic_detect(text: str) -> tuple[bool, float]:
    lowered = text.lower()
    abusive_keywords = [
        "cahil",
        "aptal",
        "salak",
        "gerizekalı",
        "mal",
        "ahmak",
        "eşek",
        "seni bilmez",
        "hiçbir şey bilmiyorsun",
    ]
    matched_count = sum(1 for keyword in abusive_keywords if keyword in lowered)
    is_ad_hominem = matched_count > 0
    confidence = min(0.35 + (0.2 * matched_count), 0.95) if is_ad_hominem else 0.05
    return is_ad_hominem, confidence


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest) -> PredictResponse:
    is_ad_hominem, confidence = heuristic_detect(payload.text)
    return PredictResponse(
        is_ad_hominem=is_ad_hominem,
        confidence=confidence,
        prediction="Ad Hominem" if is_ad_hominem else "Not Ad Hominem",
    )
