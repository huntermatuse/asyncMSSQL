from fastapi.testclient import TestClient
from fe import app 

client = TestClient(app)

def test_read_data():
    response = client.get("/data/")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)  
    if data["data"]:  
        assert isinstance(data["data"][0], dict)
