from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import requests
from django.conf import settings


@dataclass
class DetectionResult:
    is_ad_hominem: bool
    confidence: float
    source: str


class AdHominemDetector:
    def __init__(self) -> None:
        self.endpoint: Optional[str] = settings.AD_HOMINEM_MODEL_ENDPOINT
        self.timeout: int = settings.AD_HOMINEM_MODEL_TIMEOUT

    def detect(self, text: str) -> DetectionResult:
        if self.endpoint:
            remote_result = self._detect_with_remote_model(text=text)
            if remote_result is not None:
                return remote_result
        return self._detect_with_heuristic(text=text)

    def _detect_with_remote_model(self, text: str) -> Optional[DetectionResult]:
        try:
            response = requests.post(
                self.endpoint,
                json={"text": text},
                timeout=self.timeout,
            )
            response.raise_for_status()
            payload: Dict[str, object] = response.json()
        except Exception:
            return None

        if "is_ad_hominem" in payload:
            is_ad_hominem = bool(payload["is_ad_hominem"])
        else:
            prediction = str(payload.get("prediction", "")).lower()
            is_ad_hominem = "ad hominem" in prediction and "not" not in prediction

        confidence = self._parse_confidence(payload)
        return DetectionResult(
            is_ad_hominem=is_ad_hominem,
            confidence=confidence,
            source="remote-model",
        )

    def _parse_confidence(self, payload: Dict[str, object]) -> float:
        raw_confidence = payload.get("confidence", payload.get("score", 0.0))
        try:
            confidence = float(raw_confidence)
        except (TypeError, ValueError):
            return 0.0

        if confidence < 0.0:
            return 0.0
        if confidence > 1.0:
            return 1.0
        return confidence

    def _detect_with_heuristic(self, text: str) -> DetectionResult:
        lowered = str(text or "").lower()
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
        return DetectionResult(
            is_ad_hominem=is_ad_hominem,
            confidence=confidence,
            source="heuristic-fallback",
        )
