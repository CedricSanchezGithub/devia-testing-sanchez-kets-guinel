import unittest
from flask import Flask, json
from models.database import db
from models.bot import Bot
from routes.bot_routes import bot_bp

class BotRoutesTestCase(unittest.TestCase):
    def setUp(self):
        # Configuration de l'application Flask pour le test
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # Initialisation de la base de données
        db.init_app(self.app)
        self.app.register_blueprint(bot_bp)

        with self.app.app_context():
            db.create_all()
            # Ajouter des bots de test dans la base de données
            bot1 = Bot(name="Bot A", price=99.99)
            bot2 = Bot(name="Bot B", price=149.99)
            db.session.add_all([bot1, bot2])
            db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        # Nettoyage de la base de données après chaque test
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_bots(self):
        response = self.client.get("/bots")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json, "Response is not JSON")
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["name"], "Bot A")
        self.assertEqual(data[1]["name"], "Bot B")

    def test_get_bots_empty(self):
        with self.app.app_context():
            Bot.query.delete()
            db.session.commit()

        response = self.client.get("/bots")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json, "Response is not JSON")
        data = response.get_json()
        self.assertEqual(data, [])

    def test_update_bot(self):
        updated_data = {"name": "Updated Bot", "price": 199.99}
        response = self.client.put("/bots/1", json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json, "Response is not JSON")
        data = response.get_json()
        self.assertEqual(data["name"], "Updated Bot")
        self.assertEqual(data["price"], 199.99)

    def test_update_bot_not_found(self):
        updated_data = {"name": "Nonexistent Bot", "price": 299.99}
        response = self.client.put("/bots/999", json=updated_data)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(response.is_json, "Response is not JSON")
        data = response.get_json()
        self.assertEqual(data["error"], "Bot not found")


if __name__ == "__main__":
    unittest.main()
