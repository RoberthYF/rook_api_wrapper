# 🐶 Rook API Wrapper

This project is a secure wrapper over the [Dog CEO API](https://dog.ceo/dog-api/) built using **FastAPI**. It supports JWT-based authentication and stores breed request data in **MongoDB** for analytics and tracking.

---

## 📦 How to Install the Dependencies

1. Clone this repository and enter the project folder:

```bash
git clone https://github.com/RoberthYF/rook_api_wrapper.git
cd rook_api_wrapper
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
call .venv\Scripts\activate   # (On Windows)
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```
The ``requirements.txt`` includes all necessary libraries, including FastAPI, Uvicorn, Motor, and pytest.

## 🗄️How to Set Up MongoDB Locally
1. Download and install MongoDB Community Edition:
https://www.mongodb.com/try/download/community

2. Start the MongoDB server:
```bash
mongod
```

3. Create a ``.env`` file in the root folder of the project with this content:

```ini
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=dogapi
MONGODB_COLLECTION=requests
```
This will create a database named ``dogapi`` and use the collection ``requests``.

## 🚀 How to Run the FastAPI Server Locally
You can use the provided script:
```bash
run.bat
```
Or run manually with:
```bash
uvicorn app.main:app --reload
```
The server will start at:
http://127.0.0.1:8000

### Main Endpoints Overview
The API has three main endpoints:

- ``POST /token`` → Generate a JWT token using username/password (admin / secret).
- ``GET/dog/breed/{breed_name}`` → Retrieve an image and track the breed request.
- ``GET/dog/stats`` → Get top 10 most requested breeds.

There's also a root endpoint (``GET /``) that simply confirms the API is active.

## 🧪 How to Run the Pytest Tests
Make sure the server is not running, then run the tests:
```bash
pytest -s
```
This will execute the tests located in the ``tests/`` folder.

## 🧾 OpenAPI / Swagger Documentation
FastAPI automatically provides API documentation at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### To authenticate in Swagger UI

To use the protected endpoints (/dog/breed/{breed_name} and /dog/stats), you must first obtain and provide a valid JWT token.

Follow these steps:

1. Go to the /token endpoint on Swagger UI:
2. Click "Try it out" and enter the credentials:

```json
{
  "username": "admin",
  "password": "secret"
}
```
3. Click "Execute", and copy the ``access_token`` returned.
4. Scroll to the top of Swagger UI and click the "Authorize" 🔒 button.
5. Paste the token.
6. Now you can call:
- ``GET /dog/breed/{breed_name}`` (e.g., ``/dog/breed/beagle``)
- ``GET /dog/stats``

💡 Without a valid token, you'll receive a 401 Unauthorized error.

7. Token expiration:
By default, tokens expire after **30 minutes**.
This is defined in the code as:
```python
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

