from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_root_endpoint():
    """Test the health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "Simple Message API is running" in data["message"]


def test_post_message():
    """Test posting a new message"""
    message_data = {"message": "Hello, World!"}
    response = client.post("/messages", json=message_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello, World!"
    assert "id" in data


def test_get_message():
    """Test getting a message by ID"""
    # First, post a message
    message_data = {"message": "Test message"}
    post_response = client.post("/messages", json=message_data)
    message_id = post_response.json()["id"]

    # Then, get the message
    response = client.get(f"/messages/{message_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Test message"
    assert data["id"] == message_id


def test_get_nonexistent_message():
    """Test getting a message that doesn't exist"""
    response = client.get("/messages/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Message not found"


def test_delete_message():
    """Test deleting a message"""
    # First, post a message
    message_data = {"message": "Message to delete"}
    post_response = client.post("/messages", json=message_data)
    message_id = post_response.json()["id"]

    # Delete the message
    response = client.delete(f"/messages/{message_id}")
    assert response.status_code == 200
    assert f"Message {message_id} deleted successfully" in response.json()["message"]

    # Verify it's deleted
    get_response = client.get(f"/messages/{message_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_message():
    """Test deleting a message that doesn't exist"""
    response = client.delete("/messages/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Message not found"


def test_list_messages():
    """Test listing all messages"""
    # Clear any existing messages by testing with fresh client
    response = client.get("/messages")
    assert response.status_code == 200
    assert "messages" in response.json()


def test_message_workflow():
    """Test the complete workflow: post, get, list, delete"""
    # Post a message
    message_data = {"message": "Workflow test message"}
    post_response = client.post("/messages", json=message_data)
    assert post_response.status_code == 200
    message_id = post_response.json()["id"]

    # Get the message
    get_response = client.get(f"/messages/{message_id}")
    assert get_response.status_code == 200
    assert get_response.json()["message"] == "Workflow test message"

    # List messages (should include our message)
    list_response = client.get("/messages")
    assert list_response.status_code == 200
    messages = list_response.json()["messages"]
    assert any(msg["id"] == message_id for msg in messages)

    # Delete the message
    delete_response = client.delete(f"/messages/{message_id}")
    assert delete_response.status_code == 200

    # Verify it's gone
    get_response_after_delete = client.get(f"/messages/{message_id}")
    assert get_response_after_delete.status_code == 404


def test_invalid_message_post():
    """Test posting an invalid message"""
    response = client.post("/messages", json={})
    assert response.status_code == 422  # Validation error
