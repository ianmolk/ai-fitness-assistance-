from flask import Blueprint, request, jsonify
from services.ai_services import generate_chat_reply

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

@chat_bp.route("/ask", methods=["POST"])
def ask():
    data = request.get_json() or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Message is required"}), 400

    reply = generate_chat_reply(message)
    return jsonify({"reply": reply}), 200
