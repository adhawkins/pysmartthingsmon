from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields, inputs
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_apscheduler import APScheduler

from datetime import datetime, timedelta

from Database import *

API_BASE = "/smartthingsmon/api/v1"


app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pysmartthingsmon.db"
db = SQLAlchemy(model_class=Database.Base)
migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)
auth = HTTPBasicAuth()

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@scheduler.task('interval', id='cleanup', hours=1)
def cleanup():
    now = datetime.now()
    threshold = (now - timedelta(days=10)).astimezone()

    with app.app_context():
        query = db.delete(Database.Readings).where(
            Database.Readings.timestamp < threshold)
        result = db.session.execute(query)
        print(f"Readings cleanup: {result.rowcount} readings deleted")

        db.session.commit()


@auth.verify_password
def verifyPassword(username, password):
    return username == "andy" and password == "testing"


location_fields = api.model(
    "Location",
    {
        "id": fields.String,
        "name": fields.String,
        "latitude": fields.Float,
        "longitude": fields.Float,
        "region_radius": fields.Integer,
        "temperature_scale": fields.String,
        "locale": fields.String,
        "country_code": fields.String,
        "timezone_id": fields.String,
        "uri": fields.Url("location_info", absolute=True, scheme="https"),
    },
)

locationInfoArgs = api.parser()
locationInfoArgs.add_argument(
    "id",
    type=str,
    required=True,
    help="No id provided",
    location="json",
)
locationInfoArgs.add_argument(
    "name",
    type=str,
    required=True,
    help="No name provided",
    location="json",
)
locationInfoArgs.add_argument(
    "latitude",
    type=float,
    required=False,
    help="No latitude provided",
    location="json",
)
locationInfoArgs.add_argument(
    "longitude",
    type=float,
    required=False,
    help="No latitude provided",
    location="json",
)
locationInfoArgs.add_argument(
    "region_radius",
    type=int,
    required=False,
    help="No latitude provided",
    location="json",
)
locationInfoArgs.add_argument(
    "temperature_scale",
    type=str,
    required=False,
    help="No temperature scale provided",
    location="json",
)
locationInfoArgs.add_argument(
    "locale",
    type=str,
    required=False,
    help="No locale provided",
    location="json",
)
locationInfoArgs.add_argument(
    "country_code",
    type=str,
    required=False,
    help="No country code provided",
    location="json",
)
locationInfoArgs.add_argument(
    "timezone_id",
    type=str,
    required=False,
    help="No timezone id provided",
    location="json",
)


@api.route(f"{API_BASE}/locations", endpoint="locations_list")
class LocationsListAPI(Resource):
    @auth.login_required
    @api.marshal_list_with(location_fields, envelope="locations")
    def get(self):
        query = db.select(Database.Locations)

        locations = db.session.execute(query).scalars()
        return list(locations)

    @auth.login_required
    @api.expect(locationInfoArgs)
    def post(self):
        try:
            args = locationInfoArgs.parse_args()

            location = Database.Locations(
                id=args["id"],
                name=args["name"],
            )

            if "latitude" in args:
                location.latitude = args["latitude"]

            if "longitude" in args:
                location.longitude = args["longitude"]

            if "region_radius" in args:
                location.region_radius = args["region_radius"]

            if "temperature_scale" in args:
                location.temperature_scale = args["temperature_scale"]

            if "locale" in args:
                location.locale = args["locale"]

            if "country_code" in args:
                location.country_code = args["country_code"]

            if "timezone_id" in args:
                location.timezone_id = args["timezone_id"]

            db.session.add(location)
            db.session.commit()
            return redirect(url_for("location_info", id=location.id))
        except IntegrityError as e:
            return {"error": str(e.orig)}, 409


@api.route(f"{API_BASE}/locations/<string:id>", endpoint="location_info")
class LocationAPI(Resource):
    @auth.login_required
    @api.marshal_with(location_fields, envelope="location")
    def get(self, id):
        location = db.get_or_404(Database.Locations, id)
        return location

    @auth.login_required
    def delete(self, id):
        location = db.get_or_404(Database.Locations, id)
        db.session.delete(location)
        db.session.commit()

        return redirect(url_for("locations_list"))

    @auth.login_required
    @api.expect(locationInfoArgs)
    def patch(self, id):
        try:
            args = locationInfoArgs.parse_args()

            location = db.get_or_404(Database.Locations, id)
            location.name = args["name"]

            if "latitude" in args:
                location.latitude = args["latitude"]

            if "longitude" in args:
                location.longitude = args["longitude"]

            if "region_radius" in args:
                location.region_radius = args["region_radius"]

            if "temperature_scale" in args:
                location.temperature_scale = args["temperature_scale"]

            if "locale" in args:
                location.locale = args["locale"]

            if "country_code" in args:
                location.country_code = args["country_code"]

            if "timezone_id" in args:
                location.timezone_id = args["timezone_id"]

            db.session.add(location)
            db.session.commit()

            return redirect(url_for("location_info", id=location.id))
        except IntegrityError as e:
            return {"error": str(e.orig)}, 409


room_fields = api.model(
    "Room",
    {
        "id": fields.String,
        "location_id": fields.String,
        "locationdetails.name": fields.String,
        "name": fields.String,
        "background_image": fields.String,
        "uri": fields.Url("room_info", absolute=True, scheme="https"),
    },
)

roomInfoArgs = api.parser()
roomInfoArgs.add_argument(
    "id",
    type=str,
    required=True,
    help="No id provided",
    location="json",
)
roomInfoArgs.add_argument(
    "location_id",
    type=str,
    required=True,
    help="No location_id provided",
    location="json",
)
roomInfoArgs.add_argument(
    "name",
    type=str,
    required=True,
    help="No name provided",
    location="json",
)
roomInfoArgs.add_argument(
    "background_image",
    type=str,
    required=False,
    help="No background_image provided",
    location="json",
)


@api.route(f"{API_BASE}/rooms", endpoint="rooms_list")
class RoomsListAPI(Resource):
    @auth.login_required
    @api.marshal_list_with(room_fields, envelope="rooms")
    def get(self):
        query = db.select(Database.Rooms)

        rooms = db.session.execute(query).scalars()
        return list(rooms)

    @auth.login_required
    @api.expect(roomInfoArgs)
    def post(self):
        try:
            args = roomInfoArgs.parse_args()

            room = Database.Rooms(
                id=args["id"],
                location_id=args["location_id"],
                name=args["name"],
            )

            if "background_image" in args:
                room.background_image = args["background_image"]

            db.session.add(room)
            db.session.commit()
            return redirect(url_for("room_info", id=room.id))
        except IntegrityError as e:
            return {"error": str(e.orig)}, 409


@api.route(f"{API_BASE}/rooms/<string:id>", endpoint="room_info")
class RoomAPI(Resource):
    @auth.login_required
    @api.marshal_with(room_fields, envelope="room")
    def get(self, id):
        room = db.get_or_404(Database.Rooms, id)
        return room

    @auth.login_required
    def delete(self, id):
        room = db.get_or_404(Database.Rooms, id)
        db.session.delete(room)
        db.session.commit()

        return redirect(url_for("rooms_list"))

    @auth.login_required
    @api.expect(roomInfoArgs)
    def patch(self, id):
        try:
            args = roomInfoArgs.parse_args()

            room = db.get_or_404(Database.Rooms, id)
            room.location_id = args["location_id"]
            room.name = args["name"]

            if "background_image" in args:
                room.background_image = args["background_image"]

            db.session.add(room)
            db.session.commit()

            return redirect(url_for("room_info", id=room.id))
        except IntegrityError as e:
            return {"error": str(e.orig)}, 409


reading_fields = api.model(
    "Reading",
    {
        "id": fields.Integer,
        "room_id": fields.String,
        "roomdetails.name": fields.String,
        "timestamp": fields.DateTime,
        "set_point": fields.Float,
        "ambient": fields.Float,
        "humidity": fields.Float,
        "state": fields.String,
    },
)

readingInfoArgs = api.parser()
readingInfoArgs.add_argument(
    "room_id",
    type=str,
    required=True,
    help="No room_id provided",
    location="json",
)
readingInfoArgs.add_argument(
    "set_point",
    type=float,
    required=False,
    help="No set_point provided",
    location="json",
)
readingInfoArgs.add_argument(
    "ambient",
    type=float,
    required=True,
    help="No ambient provided",
    location="json",
)
readingInfoArgs.add_argument(
    "humidity",
    type=float,
    required=False,
    help="No humidity provided",
    location="json",
)
readingInfoArgs.add_argument(
    "target",
    type=float,
    required=False,
    help="No target provided",
    location="json",
)
readingInfoArgs.add_argument(
    "state",
    type=str,
    required=False,
    help="No state provided",
    location="json",
)


def toDate(dateString):
    return datetime.strptime(dateString, "%Y-%m-%d").astimezone()


@api.route(f"{API_BASE}/readings", endpoint="readings_list")
class ReadingsListAPI(Resource):
    @auth.login_required
    @api.marshal_list_with(reading_fields, envelope="readings")
    def get(self):
        date = request.args.get("date", default=None, type=toDate)

        query = db.select(Database.Readings)
        if date:
            startDate = date - timedelta(minutes=1)
            endDate = date + timedelta(days=1, minutes=1)

            query = query.where(Database.Readings.timestamp >= startDate)
            query = query.where(Database.Readings.timestamp < endDate)

        readings = db.session.execute(query).scalars()

        return list(readings)

    @auth.login_required
    @api.expect(readingInfoArgs)
    def post(self):
        try:
            args = readingInfoArgs.parse_args()

            reading = Database.Readings(
                room_id=args["room_id"], ambient=args["ambient"]
            )

            if "set_point" in args:
                reading.set_point = args["set_point"]

            if "humidity" in args:
                reading.humidity = args["humidity"]

            if "state" in args:
                reading.state = args["state"]

            db.session.add(reading)
            db.session.commit()
            return redirect(url_for("reading_info", id=reading.id))
        except IntegrityError as e:
            return {"error": str(e.orig)}, 409


@api.route(f"{API_BASE}/readings/<int:id>", endpoint="reading_info")
class ReadingAPI(Resource):
    @auth.login_required
    @api.marshal_with(reading_fields, envelope="reading")
    def get(self, id):
        room = db.get_or_404(Database.Readings, id)
        return room
