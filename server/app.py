from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Plant

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# INDEX
@app.route("/plants", methods=["GET"])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants]), 200


# SHOW
@app.route("/plants/<int:id>", methods=["GET"])
def get_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({"error": "Plant not found"}), 404
    return jsonify(plant.to_dict()), 200


# CREATE
@app.route("/plants", methods=["POST"])
def create_plant():
    data = request.get_json()

    plant = Plant(
        name=data.get("name"),
        image=data.get("image"),
        price=data.get("price")
    )

    db.session.add(plant)
    db.session.commit()

    return jsonify(plant.to_dict()), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)
with app.app_context():
    db.create_all()
