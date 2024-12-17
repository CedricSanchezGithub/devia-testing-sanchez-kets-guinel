import unittest
from flask import Flask, json
from models.database import db
from models.order import Order
from models.bot import Bot
from routes.order_routes import order_bp

class OrderRoutesTestCase(unittest.TestCase):
    def setUp(self):
        # Configuration de l'application Flask pour les tests
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # Initialisation de la base de données
        db.init_app(self.app)
        self.app.register_blueprint(order_bp, url_prefix="/orders")

        with self.app.app_context():
            db.create_all()
            # Ajouter des données de test
            bot1 = Bot(name="Bot A", price=99.99)
            bot2 = Bot(name="Bot B", price=149.99)
            db.session.add_all([bot1, bot2])
            db.session.commit()

            order1 = Order(bot_id=bot1.id, status="en attente")
            order2 = Order(bot_id=bot2.id, status="expédiée")
            db.session.add_all([order1, order2])
            db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        # Nettoyage de la base de données après chaque test
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_order_details(self):
        response = self.client.get("/orders/1")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["bot_name"], "Bot A")
        self.assertEqual(data["status"], "en attente")

    def test_get_order_not_found(self):
        response = self.client.get("/orders/999")
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data["error"], "Order not found")

    def test_update_order_status(self):
        updated_data = {"status": "livrée"}
        response = self.client.put("/orders/1", json=updated_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data["status"], "livrée")

    def test_update_order_not_found(self):
        updated_data = {"status": "annulée"}
        response = self.client.put("/orders/999", json=updated_data)
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data["error"], "Order not found")

    def test_update_order_status_missing_field(self):
        response = self.client.put("/orders/1", json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data["error"], "Status is required")


if __name__ == "__main__":
    unittest.main()
