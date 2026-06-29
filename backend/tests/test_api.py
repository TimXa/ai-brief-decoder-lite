SAMPLE_BRIEF = """
We need a landing page for a B2B SaaS analytics product.
The page should explain the product, include pricing teaser,
capture emails, and be ready in 2 weeks.
Budget is limited. We also need copy suggestions and basic SEO.
"""


def test_decode_happy_path_with_fake_provider(client):
    response = client.post("/v1/briefs/decode", json={"text": SAMPLE_BRIEF})

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["result"]["summary"]
    assert body["result"]["risks"][0]["severity"] == "medium"

    run_response = client.get(f"/v1/briefs/runs/{body['run_id']}")
    assert run_response.status_code == 200
    assert run_response.json()["structured_result"]["summary"] == body["result"]["summary"]


def test_decode_handles_malformed_json(client):
    response = client.post("/v1/briefs/decode", json={"text": SAMPLE_BRIEF, "mode": "malformed_json"})

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "failed"
    assert body["error"]["code"] == "invalid_json"


def test_decode_handles_provider_failure(client):
    response = client.post("/v1/briefs/decode", json={"text": SAMPLE_BRIEF, "mode": "provider_failure"})

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "failed"
    assert body["error"]["code"] == "provider_error"
