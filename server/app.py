from flask import Flask, request
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()  # ensures the table exists


class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return [p.to_dict() for p in plants], 200

    def post(self):
        data = request.get_json()
        plant = Plant(
            name=data["name"], image=data.get("image"), price=data.get("price")
        )
        db.session.add(plant)
        db.session.commit()
        return plant.to_dict(), 201


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return {"error": "Plant not found"}, 404
        return plant.to_dict(), 200


api.add_resource(Plants, "/plants")
api.add_resource(PlantByID, "/plants/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)