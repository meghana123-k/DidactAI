from flask import Blueprint, request, jsonify
from services.certificate_generator import CertificateGenerator

certificate_bp = Blueprint("certificate", __name__)
generator = CertificateGenerator()

@certificate_bp.route("/generate", methods=["POST"])
def generate_certificate():
    data = request.json

    cert = generator.generate_certificate(
        student_name=data["student_name"],
        topic=data["topic"],
        analytics=data["analytics"]
    )

    return jsonify(cert.__dict__)
