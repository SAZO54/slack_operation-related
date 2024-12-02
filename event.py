from flask import Blueprint, request, jsonify

slack_event_bp = Blueprint("slack_event_bp", __name__)

@slack_event_bp.route("/slack/events", methods=["POST"])
def handle_event():
    data = request.json

    # Slackからのchallengeリクエストに応答
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    # イベント処理ロジックを追加
    event = data.get("event", {})
    if event.get("type") == "message":
      user = event.get("user")
      text = event.get("text")
      print(f"Received a message from {user}: {text}")

    return jsonify({"status": "success"})
