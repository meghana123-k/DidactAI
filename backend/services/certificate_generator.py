from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4
from typing import Dict


@dataclass
class Certificate:
    certificate_id: str
    student_name: str
    topic: str
    final_score: float
    integrity_score: float
    issued_on: str
    status: str
    remarks: str


class CertificateGenerator:
    """
    Generates digital certificates based on assessment performance.
    """

    MIN_FINAL_SCORE = 0.7
    MIN_INTEGRITY_SCORE = 0.8

    def is_eligible(
        self,
        analytics: Dict
    ) -> (bool, str):
        """
        Check eligibility for certificate issuance.
        """
        if analytics["final_score"] < self.MIN_FINAL_SCORE:
            return False, "Final score below threshold"

        if analytics["integrity_score"] < self.MIN_INTEGRITY_SCORE:
            return False, "Integrity score below threshold"

        breakdown = analytics.get("breakdown", {})
        for level in ["beginner", "intermediate", "advanced"]:
            if breakdown.get(level, {}).get("count", 0) == 0:
                return False, f"No questions attempted at {level} level"

        return True, "Eligible"

    def generate_certificate(
        self,
        student_name: str,
        topic: str,
        analytics: Dict
    ) -> Certificate:
        eligible, reason = self.is_eligible(analytics)

        status = "Issued" if eligible else "Rejected"

        return Certificate(
            certificate_id=str(uuid4()),
            student_name=student_name,
            topic=topic,
            final_score=analytics["final_score"],
            integrity_score=analytics["integrity_score"],
            issued_on=datetime.utcnow().strftime("%Y-%m-%d"),
            status=status,
            remarks=reason
        )
