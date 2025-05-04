from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import ObjectId
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)


def iso(x):
    if isinstance(x, datetime):
        return x.isoformat()
    return str(x)


def ensure_indexes():
    col = mongo.db.meetings
    col.create_index([("start_time", 1)], name="idx_start_time")
    col.create_index([("end_time", 1)], name="idx_end_time")
    col.create_index([("room", "hashed")], name="idx_room_hashed")
    col.create_index([("club", 1), ("start_time", 1)], name="idx_club_start")
ensure_indexes()


@app.route("/meetings", methods=["POST"])
def create_meeting():
    data = request.get_json()
    data["start_time"] = datetime.fromisoformat(data["start_time"])
    data["end_time"] = datetime.fromisoformat(data["end_time"])
    result = mongo.db.meetings.insert_one(data)
    return jsonify({"status": "success", "id": str(result.inserted_id)})


@app.route("/meetings", methods=["GET"])
def get_meetings():
    docs = list(mongo.db.meetings.find())
    for d in docs:
        d["_id"] = str(d["_id"])
        d["start_time"] = iso(d["start_time"])
        d["end_time"] = iso(d["end_time"])
    return jsonify({"status": "success", "meetings": docs})


@app.route("/meetings/<id>", methods=["PUT"])
def update_meeting(id):
    data = request.get_json()
    if "start_time" in data:
        data["start_time"] = datetime.fromisoformat(data["start_time"])
    if "end_time" in data:
        data["end_time"] = datetime.fromisoformat(data["end_time"])
    res = mongo.db.meetings.update_one({"_id": ObjectId(id)}, {"$set": data})
    if not res.matched_count:
        return jsonify({"status": "error", "message": "Meeting not found"}), 404
    return jsonify({"status": "success"})


@app.route("/meetings/<id>", methods=["DELETE"])
def delete_meeting(id):
    res = mongo.db.meetings.delete_one({"_id": ObjectId(id)})
    if not res.deleted_count:
        return jsonify({"status": "error", "message": "Meeting not found"}), 404
    return jsonify({"status": "success"})


@app.route("/meetings/filter", methods=["GET"])
def filter_meetings():
    f = {}
    if request.args.get("room"):
        f["room"] = request.args["room"]
    if request.args.get("club"):
        f["club"] = request.args["club"]

    if request.args.get("start"):
        d = datetime.fromisoformat(request.args["start"])
        f["start_time"] = {"$gte": d, "$lt": d + timedelta(days=1)}
    if request.args.get("end"):
        d = datetime.fromisoformat(request.args["end"])
        f["end_time"] = {"$gte": d, "$lt": d + timedelta(days=1)}

    docs = list(mongo.db.meetings.find(f))

    durations = [
        (d["end_time"] - d["start_time"]).total_seconds() / 60 for d in docs
    ]
    if durations:
        stats = {
            "count": len(docs),
            "avg_duration_min": round(sum(durations) / len(durations), 1),
            "min_duration_min": round(min(durations), 1),
            "max_duration_min": round(max(durations), 1),
            "first_start": iso(min(d["start_time"] for d in docs)),
            "last_end": iso(max(d["end_time"] for d in docs)),
        }
    else:
        stats = {
            "count": 0,
            "avg_duration_min": 0,
            "min_duration_min": 0,
            "max_duration_min": 0,
            "first_start": None,
            "last_end": None,
        }

    for d in docs:
        d["_id"] = str(d["_id"])
        d["start_time"] = iso(d["start_time"])
        d["end_time"] = iso(d["end_time"])

    return jsonify({"status": "success", "meetings": docs, "stats": stats})


if __name__ == "__main__":
    app.run(debug=True)