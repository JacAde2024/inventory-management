"""
Tests for restocking API endpoints.
"""


class TestRestockingEndpoints:
    """Test suite for restocking-related endpoints."""

    def test_get_recommendations_requires_budget(self, client):
        """Missing budget query param returns 422."""
        response = client.get("/api/restocking/recommendations")
        assert response.status_code == 422

    def test_get_recommendations_rejects_non_positive_budget(self, client):
        """budget=0 or negative returns 422."""
        response = client.get("/api/restocking/recommendations?budget=0")
        assert response.status_code == 422
        response = client.get("/api/restocking/recommendations?budget=-100")
        assert response.status_code == 422

    def test_get_recommendations_structure(self, client):
        """Successful response has the expected shape."""
        response = client.get("/api/restocking/recommendations?budget=5000")
        assert response.status_code == 200
        data = response.json()
        assert "recommendations" in data
        assert "total_estimated_cost" in data
        assert "remaining_budget" in data
        assert isinstance(data["recommendations"], list)
        for item in data["recommendations"]:
            assert "sku" in item
            assert "recommended_quantity" in item
            assert "estimated_cost" in item
            assert "lead_time_days" in item
            assert item["recommended_quantity"] > 0

    def test_recommendations_respect_budget(self, client):
        """Sum of selected items' estimated_cost never exceeds the given budget."""
        response = client.get("/api/restocking/recommendations?budget=5000")
        data = response.json()
        total = sum(item["estimated_cost"] for item in data["recommendations"])
        assert total <= 5000
        assert abs(total - data["total_estimated_cost"]) < 0.01

    def test_recommendations_known_budget_selection(self, client):
        """budget=5000 selects exactly FLT-405, WDG-001, GSK-203, CTL-330 (worked example)."""
        response = client.get("/api/restocking/recommendations?budget=5000")
        data = response.json()
        skus = [item["sku"] for item in data["recommendations"]]
        assert skus == ["FLT-405", "WDG-001", "GSK-203", "CTL-330"]
        assert abs(data["total_estimated_cost"] - 4862.25) < 0.01
        assert abs(data["remaining_budget"] - 137.75) < 0.01

    def test_recommendations_tiny_budget_returns_empty(self, client):
        """A tiny budget that fits nothing returns an empty recommendations list."""
        response = client.get("/api/restocking/recommendations?budget=1")
        data = response.json()
        assert data["recommendations"] == []
        assert data["total_estimated_cost"] == 0

    def test_recommendations_exclude_well_stocked_items(self, client):
        """MTR-304 (decreasing trend, already overstocked) and PSU-501 never appear."""
        response = client.get("/api/restocking/recommendations?budget=100000")
        data = response.json()
        skus = [item["sku"] for item in data["recommendations"]]
        assert "MTR-304" not in skus
        assert "PSU-501" not in skus

    def test_create_restock_order_appends_to_orders(self, client):
        """Submitting a restock order increases /api/orders count and the new order is retrievable."""
        before = client.get("/api/orders").json()
        payload = {"budget": 2000, "items": [{"sku": "GSK-203", "quantity": 180}]}
        response = client.post("/api/orders/restock", json=payload)
        assert response.status_code == 201

        order = response.json()
        assert order["source"] == "restocking"
        assert order["status"] == "Processing"
        assert order["items"][0]["sku"] == "GSK-203"
        assert order["items"][0]["quantity"] == 180
        assert abs(order["total_value"] - (180 * 3.25)) < 0.01

        after = client.get("/api/orders").json()
        assert len(after) == len(before) + 1
        assert any(o["id"] == order["id"] for o in after)

    def test_create_restock_order_computes_lead_time_delivery(self, client):
        """expected_delivery equals order_date + the item's lead_time_days (GSK-203 => 18 days)."""
        from datetime import datetime
        payload = {"budget": 1000, "items": [{"sku": "GSK-203", "quantity": 10}]}
        response = client.post("/api/orders/restock", json=payload)
        order = response.json()
        order_date = datetime.fromisoformat(order["order_date"])
        expected_delivery = datetime.fromisoformat(order["expected_delivery"])
        assert (expected_delivery - order_date).days == 18

    def test_create_restock_order_uses_max_lead_time_across_items(self, client):
        """Multi-item order uses the longest lead time among included items."""
        from datetime import datetime
        payload = {
            "budget": 5000,
            "items": [
                {"sku": "CTL-330", "quantity": 5},
                {"sku": "GSK-203", "quantity": 5},
            ],
        }
        response = client.post("/api/orders/restock", json=payload)
        order = response.json()
        delta = (
            datetime.fromisoformat(order["expected_delivery"])
            - datetime.fromisoformat(order["order_date"])
        ).days
        assert delta == 18

    def test_create_restock_order_rejects_unknown_sku(self, client):
        """Unknown SKU returns 404."""
        payload = {"budget": 100, "items": [{"sku": "NOPE-999", "quantity": 1}]}
        response = client.post("/api/orders/restock", json=payload)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_create_restock_order_rejects_empty_items(self, client):
        """Empty items list returns 400."""
        response = client.post("/api/orders/restock", json={"budget": 100, "items": []})
        assert response.status_code == 400

    def test_create_restock_order_rejects_zero_quantity(self, client):
        """Zero/negative quantity returns 400."""
        payload = {"budget": 100, "items": [{"sku": "GSK-203", "quantity": 0}]}
        response = client.post("/api/orders/restock", json=payload)
        assert response.status_code == 400
