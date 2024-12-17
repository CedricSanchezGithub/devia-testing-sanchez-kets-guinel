from flask import Blueprint, jsonify, request
from models.database import db
from models.bot import Bot

bot_bp = Blueprint("bots", __name__)

@bot_bp.route("/bots", methods=["GET"])
def get_bots():
    bots = Bot.query.all()
    if not bots:
        return jsonify([]), 200
    return jsonify([bot.to_dict() for bot in bots]), 200

@bot_bp.route("/bots/<int:id>", methods=["PUT"])
def update_bot(id):
    bot = Bot.query.get(id)
    if not bot:
        return jsonify({"error": "Bot not found"}), 404

    data = request.get_json()
    name = data.get("name")
    price = data.get("price")

    if name:
        bot.name = name
    if price is not None:
        bot.price = price

    db.session.commit()

    return jsonify(bot.to_dict()), 200
