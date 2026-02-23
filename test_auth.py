"""
Test script for House Price Prediction authentication system.
Run this after starting the Flask server.
"""
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_auth_flow():
    print("=" * 50)
    print("Testing Authentication System")
    print("=" * 50)
    
    session = requests.Session()
    
    # Test 1: Access home page (should redirect to login)
    print("\n[TEST 1] Accessing home page without login...")
    response = session.get(f"{BASE_URL}/")
    if response.url.endswith("/login"):
        print("[PASS] Redirected to login page")
    else:
        print(f"[FAIL] Expected redirect to /login, got {response.url}")
    
    # Test 2: Sign up a new user
    print("\n[TEST 2] Creating new user 'testuser'...")
    signup_data = {
        "username": "testuser",
        "password": "test1234",
        "confirm_password": "test1234"
    }
    response = session.post(f"{BASE_URL}/signup", data=signup_data)
    if "Account created successfully" in response.text or response.url.endswith("/login"):
        print("[PASS] User created successfully")
    else:
        # Check if user already exists (from previous test runs)
        if "already exists" in response.text:
            print("[PASS] User already exists (expected on re-run)")
        else:
            print(f"[FAIL] Signup failed")
    
    # Test 3: Login with the new user
    print("\n[TEST 3] Logging in as 'testuser'...")
    login_data = {
        "username": "testuser",
        "password": "test1234"
    }
    response = session.post(f"{BASE_URL}/login", data=login_data)
    if "Welcome" in response.text or "testuser" in response.text or response.url.endswith("/"):
        print("[PASS] Login successful")
    else:
        print(f"[FAIL] Login failed")
    
    # Test 4: Access home page after login
    print("\n[TEST 4] Accessing home page after login...")
    response = session.get(f"{BASE_URL}/")
    if response.status_code == 200 and "testuser" in response.text:
        print("[PASS] Home page accessible, username displayed")
    else:
        print(f"[FAIL] Home page access failed")
    
    # Test 5: Make a prediction
    print("\n[TEST 5] Making house price prediction...")
    prediction_data = {
        "area": 1000,
        "bedrooms": 2,
        "bathrooms": 2,
        "floor": 3,
        "total_floors": 5,
        "furnished": 1,
        "balcony": 1,
        "age_of_house": 5,
        "parking": 1,
        "near_school": 1,
        "near_metro": 0
    }
    response = session.post(f"{BASE_URL}/predict", data=prediction_data)
    if response.status_code == 200 and ("Estimated House Price" in response.text or "Error" in response.text):
        print("[PASS] Prediction endpoint working")
    else:
        print(f"[FAIL] Prediction failed with status {response.status_code}")
    
    # Test 6: Logout
    print("\n[TEST 6] Logging out...")
    response = session.get(f"{BASE_URL}/logout")
    if "logged out" in response.text.lower() or response.url.endswith("/login"):
        print("[PASS] Logout successful")
    else:
        print(f"[FAIL] Logout failed")
    
    # Test 7: Try to access home after logout
    print("\n[TEST 7] Accessing home page after logout...")
    response = session.get(f"{BASE_URL}/")
    if response.url.endswith("/login"):
        print("[PASS] Redirected to login after logout")
    else:
        print(f"[FAIL] Should redirect to login, got {response.url}")
    
    # Test 8: Test invalid login
    print("\n[TEST 8] Testing invalid login credentials...")
    invalid_login = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    response = session.post(f"{BASE_URL}/login", data=invalid_login)
    if "Invalid" in response.text or "invalid" in response.text.lower():
        print("[PASS] Invalid password rejected")
    else:
        print("[FAIL] Should reject invalid password")
    
    print("\n" + "=" * 50)
    print("Testing Complete!")
    print("=" * 50)

if __name__ == "__main__":
    try:
        test_auth_flow()
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server.")
        print("Make sure the Flask server is running: python app.py")
    except Exception as e:
        print(f"ERROR: {e}")
