from flask import Blueprint, jsonify, request
from models.database import db
from models.order import Order

order_bp = Blueprint("orders", __name__)

# Route GET pour consulter les détails d'une commande
@order_bp.route("/orders/<int:id>", methods=["GET"])
def get_order_details(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    return jsonify(order.to_dict()), 200

# Route PUT pour mettre à jour le statut de la commande
@order_bp.route("/orders/<int:id>", methods=["PUT"])
def update_order_status(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    data = request.get_json()
    new_status = data.get("status")

    if not new_status:
        return jsonify({"error": "Status is required"}), 400

    # Mettre à jour le statut
    order.status = new_status
    db.session.commit()

    return jsonify(order.to_dict()), 200
