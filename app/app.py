"""
Vehicle Service API
====================
A Python (Flask) implementation of the Vehicle Service API, built to satisfy the
contract defined in the Postman "Vehicle Service Collection".

Endpoints:
    POST   /vehicles        -> 201 Created   (409 on duplicate VIN, 400 on missing attr)
    GET    /vehicles        -> 200 OK        (list all vehicles)
    GET    /vehicles/<id>   -> 200 OK        (404 if not found)
    PATCH  /vehicles/<id>   -> 200 OK        (404 if not found, 400 on bad body)
    DELETE /vehicles/<id>   -> 204 No Content(404 if not found)

Auth:
    API Key authentication via the `X-API-Key` header (matches the collection auth config).
    The expected key is read from the API_KEY environment variable so it is never
    stored in plaintext in the repo. If API_KEY is unset, auth is disabled (dev mode).
"""

import os
from functools import wraps

from flask import Flask, jsonify, request

app = Flask(__name__)

# ---------------------------------------------------------------------------
# In-memory data store (seeded with the examples from the collection)
# ---------------------------------------------------------------------------
REQUIRED_ATTRS = ["nickName", "vin", "make", "model", "year", "miles"]

vehicles = {
    1: {
        "id": 1,
        "nickName": "The Lisa Marie",
        "vin": "4M2DV11W4RDJ53329",
        "make": "Mercury",
        "model": "Villager",
        "year": "1994",
        "miles": 159864,
    },
    2: {
        "id": 2,
        "nickName": "Dolly",
        "vin": "JN8AZ2KR1AT169594",
        "make": "Nissan",
        "model": "Cube",
        "year": "2010",
        "miles": 59000,
    },
}
_next_id = 3


def _allocate_id():
    global _next_id
    new_id = _next_id
    _next_id += 1
    return new_id


# ---------------------------------------------------------------------------
# Authentication (X-API-Key)
# ---------------------------------------------------------------------------
def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        expected = os.environ.get("API_KEY")
        # If no API_KEY is configured, run in open "dev" mode.
        if expected:
            provided = request.headers.get("X-API-Key")
            if not provided or provided != expected:
                return jsonify({"message": "Unauthorized: invalid or missing X-API-Key"}), 401
        return func(*args, **kwargs)

    return wrapper


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/vehicles", methods=["POST"])
@require_api_key
def create_vehicle():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"message": "Request body must be valid JSON"}), 400

    # 400 - missing required attribute
    for attr in REQUIRED_ATTRS:
        if attr not in body or body[attr] in (None, ""):
            return jsonify({"message": f"Request body missing required attribute: {attr}"}), 400

    # 409 - duplicate VIN
    for existing in vehicles.values():
        if existing["vin"] == body["vin"]:
            return (
                jsonify(
                    {
                        "message": f"Vehicle with VIN {body['vin']} already exists. "
                        f"Existing vehicle ID: {existing['id']}"
                    }
                ),
                409,
            )

    new_id = _allocate_id()
    vehicle = {
        "id": new_id,
        "nickName": body["nickName"],
        "vin": body["vin"],
        "make": body["make"],
        "model": body["model"],
        "year": body["year"],
        "miles": body["miles"],
    }
    vehicles[new_id] = vehicle
    return jsonify(vehicle), 201


@app.route("/vehicles", methods=["GET"])
@require_api_key
def get_all_vehicles():
    return jsonify(list(vehicles.values())), 200


@app.route("/vehicles/<int:vehicle_id>", methods=["GET"])
@require_api_key
def get_vehicle(vehicle_id):
    vehicle = vehicles.get(vehicle_id)
    if vehicle is None:
        return jsonify({"message": f"Vehicle with id: {vehicle_id} not found."}), 404
    return jsonify(vehicle), 200


@app.route("/vehicles/<int:vehicle_id>", methods=["PATCH"])
@require_api_key
def update_vehicle(vehicle_id):
    vehicle = vehicles.get(vehicle_id)
    if vehicle is None:
        return jsonify({"message": f"Vehicle with id: {vehicle_id} not found."}), 404

    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"message": "Request body must be valid JSON"}), 400

    # Only allow known attributes to be patched.
    for key, value in body.items():
        if key in REQUIRED_ATTRS:
            vehicle[key] = value
        elif key != "id":
            return jsonify({"message": f"Unknown attribute in request body: {key}"}), 400

    vehicles[vehicle_id] = vehicle
    return jsonify(vehicle), 200


@app.route("/vehicles/<int:vehicle_id>", methods=["DELETE"])
@require_api_key
def delete_vehicle(vehicle_id):
    if vehicle_id not in vehicles:
        return jsonify({"message": f"Vehicle with id: {vehicle_id} not found."}), 404
    del vehicles[vehicle_id]
    return "", 204


# ---------------------------------------------------------------------------
# Error handlers -> 500 for anything unexpected
# ---------------------------------------------------------------------------
@app.errorhandler(Exception)
def handle_unexpected(err):
    return jsonify({"message": "An unexpected error occurred."}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4500))
    app.run(host="0.0.0.0", port=port, debug=True)
