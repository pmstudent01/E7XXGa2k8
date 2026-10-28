"""
Vehicle Service SDK (Python)
============================
A lightweight client library for the Vehicle Service API, derived from the
Postman "Vehicle Service Collection".

This is a hand-authored SDK provided because the automated Postman SDK
generation service was unavailable at build time. It mirrors the same surface
an auto-generated client would expose: one method per collection endpoint,
API-Key auth, and typed return values.

Usage:
    from vehicle_service_client import VehicleServiceClient

    client = VehicleServiceClient(base_url="http://localhost:4500", api_key="my-key")
    vehicles = client.list_vehicles()
    created = client.create_vehicle({
        "nickName": "The Lisa Marie",
        "vin": "4M2DV11W4RDJ53329",
        "make": "Mercury",
        "model": "Villager",
        "year": "1994",
        "miles": 159864,
    })
"""

from typing import Any, Dict, List, Optional

import requests


class VehicleServiceError(Exception):
    """Raised when the API returns a non-success status code."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"[{status_code}] {message}")


class VehicleServiceClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()

    def _headers(self) -> Dict[str, str]:
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers

    def _handle(self, resp: requests.Response) -> Any:
        if resp.status_code == 204:
            return None
        try:
            payload = resp.json()
        except ValueError:
            payload = {"message": resp.text}
        if not resp.ok:
            raise VehicleServiceError(resp.status_code, payload.get("message", "Unknown error"))
        return payload

    # -- Endpoints -----------------------------------------------------------

    def create_vehicle(self, vehicle: Dict[str, Any]) -> Dict[str, Any]:
        """POST /vehicles -> 201 Created"""
        resp = self.session.post(
            f"{self.base_url}/vehicles", json=vehicle, headers=self._headers(), timeout=self.timeout
        )
        return self._handle(resp)

    def list_vehicles(self) -> List[Dict[str, Any]]:
        """GET /vehicles -> 200 OK"""
        resp = self.session.get(
            f"{self.base_url}/vehicles", headers=self._headers(), timeout=self.timeout
        )
        return self._handle(resp)

    def get_vehicle(self, vehicle_id: int) -> Dict[str, Any]:
        """GET /vehicles/{id} -> 200 OK (404 if missing)"""
        resp = self.session.get(
            f"{self.base_url}/vehicles/{vehicle_id}", headers=self._headers(), timeout=self.timeout
        )
        return self._handle(resp)

    def update_vehicle(self, vehicle_id: int, changes: Dict[str, Any]) -> Dict[str, Any]:
        """PATCH /vehicles/{id} -> 200 OK (404 if missing)"""
        resp = self.session.patch(
            f"{self.base_url}/vehicles/{vehicle_id}",
            json=changes,
            headers=self._headers(),
            timeout=self.timeout,
        )
        return self._handle(resp)

    def delete_vehicle(self, vehicle_id: int) -> None:
        """DELETE /vehicles/{id} -> 204 No Content (404 if missing)"""
        resp = self.session.delete(
            f"{self.base_url}/vehicles/{vehicle_id}", headers=self._headers(), timeout=self.timeout
        )
        return self._handle(resp)
