from app.schemas.auth import RegisterRequest
import pydantic
import json
try:
    req = RegisterRequest(fullName="a", email="a", password="a", instituteName="a")
    print(req)
except Exception as e:
    print(e)

try:
    req = RegisterRequest.model_validate({"fullName": "a", "email": "a", "password": "a", "instituteName": "a"})
    print(req)
except Exception as e:
    print("from json error:", e)
