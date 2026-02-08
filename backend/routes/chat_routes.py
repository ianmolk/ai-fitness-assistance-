from flask import Blueprint, request, jsonify
from utils.jwt_utils import token_required
from services.ai_services import generate_chat_reply


chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.route("/ask", methods=["POST"])
@token_required
def ask(current_user):
    data = request.get_json() or {}
    message = data.get("message", "")

    reply = generate_chat_reply(message)

    return jsonify({"reply": reply}), 200
    