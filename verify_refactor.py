import requests
import uuid

BASE_URL = "http://localhost:5000"

def test_flow():
    email = f"test_{uuid.uuid4().hex[:6]}@example.com"
    password = "password123"
    
    print(f"Testing registration for {email}...")
    reg_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": email,
        "password": password,
        "type": "student",
        "gender": "male",
        "birth_date": "2000-01-01",
        "gpa": 3.8
    }
    res = requests.post(f"{BASE_URL}/auth/register", json=reg_data)
    print(f"Registration Status: {res.status_code}")
    print(f"Registration Response: {res.json()}")
    
    if res.status_code != 201:
        return

    print("\nTesting login...")
    login_data = {"email": email, "password": password}
    res = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login Status: {res.status_code}")
    login_res = res.json()
    print(f"Login Response: {login_res}")
    
    token = login_res.get("access_token")
    if not token:
        print("No token received")
        return

    print("\nTesting access to /students/...")
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/students/", headers=headers)
    print(f"Students Access Status: {res.status_code}")
    print(f"Students List: {res.json()}")

if __name__ == "__main__":
    try:
        test_flow()
    except Exception as e:
        print(f"Error during verification: {e}")
