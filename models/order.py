from models.database import db

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    bot_id = db.Column(db.Integer, db.ForeignKey("bots.id"), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="en attente")

    # Relation avec le modèle Bot
    bot = db.relationship("Bot", backref="orders")

    def to_dict(self):
        return {
            "id": self.id,
            "bot_id": self.bot_id,
            "bot_name": self.bot.name if self.bot else None,
            "status": self.status,
        }
