import pytest
import json
from app import app, db
from models import Plant

# -----------------------------
# Test Setup
# -----------------------------
@pytest.fixture(scope="module")
def test_client():
    # Set up Flask test client
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"  # in-memory DB for tests
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()  # <-- create all tables before tests
        yield testing_client
        with app.app_context():
            db.drop_all()  # <-- clean up after tests

# -----------------------------
# Tests
# -----------------------------

def test_plants_get_route_returns_list_of_plant_objects(test_client):
    """returns JSON representing Plant objects at "/plants"."""
    with app.app_context():
        # Add a plant to test GET route
        p = Plant(name="Douglas Fir", image="https://example.com/douglas.jpg", price=100.00)
        db.session.add(p)
        db.session.commit()

    response = test_client.get('/plants')
    data = json.loads(response.data.decode())

    assert type(data) == list
    assert len(data) >= 1
    assert data[0]["name"] == "Douglas Fir"
    assert data[0]["image"] == "https://example.com/douglas.jpg"

def test_plants_post_route_creates_plant_record_in_db(test_client):
    """allows users to create Plant records through the "/plants" POST route."""
    response = test_client.post(
        '/plants',
        json = {
            "name": "Live Oak",
            "image": "https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx",
            "price": 250.00
        }
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 201

    with app.app_context():
        lo = Plant.query.filter_by(name="Live Oak").first()
        assert lo is not None
        assert lo.name == "Live Oak"
        assert lo.image == "https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx"
        assert lo.price == 250.00
