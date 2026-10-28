# Vehicle Service API — Python Implementation

A Flask implementation of the Vehicle Service API, built to satisfy the contract
defined in the Postman **Vehicle Service Collection**.

## Layout

```
app/
├── app.py                         # Flask API server (implements all 5 endpoints)
├── sdk/
│   └── vehicle_service_client.py  # Python SDK client for the API
├── requirements.txt
└── README.md
```

> Note: a hand-authored SDK (`sdk/vehicle_service_client.py`) is included because
> the automated Postman SDK generation service was unavailable at build time.
> It exposes one method per endpoint and matches the collection's API-Key auth.

## Endpoints

| Operation    | Method   | Path            | Success | Errors        |
|--------------|----------|-----------------|---------|---------------|
| Create       | `POST`   | `/vehicles`     | `201`   | `400`, `409`  |
| List all     | `GET`    | `/vehicles`     | `200`   | —             |
| Retrieve one | `GET`    | `/vehicles/:id` | `200`   | `404`         |
| Update       | `PATCH`  | `/vehicles/:id` | `200`   | `400`, `404`  |
| Delete       | `DELETE` | `/vehicles/:id` | `204`   | `404`         |

Any unexpected failure returns `500`.

## Authentication

Endpoints are protected via **API Key** auth using the `X-API-Key` header
(as configured in the collection). The expected key is read from the `API_KEY`
environment variable — **never** hard-coded in the repo. If `API_KEY` is unset,
the server runs in open dev mode so you can test locally without a key.

## Running

```bash
cd app
pip install -r requirements.txt

# Optional: enable API-Key auth
export API_KEY="your-secret-key"      # Windows (PowerShell): $env:API_KEY="your-secret-key"

python app.py
```

The server listens on port `4500` by default (override with the `PORT` env var),
matching the local mock URL so you can point Postman's `{{baseUrl}}` at it.

## Using the SDK

```python
from sdk.vehicle_service_client import VehicleServiceClient

client = VehicleServiceClient(base_url="http://localhost:4500", api_key="your-secret-key")

print(client.list_vehicles())
created = client.create_vehicle({
    "nickName": "The Lisa Marie",
    "vin": "4M2DV11W4RDJ53329",
    "make": "Mercury",
    "model": "Villager",
    "year": "1994",
    "miles": 159864,
})
```
