# app/routes.py
from fastapi.responses import JSONResponse
from app.db import collection
from datetime import datetime
from pymongo.errors import PyMongoError

from fastapi import APIRouter, HTTPException, Body
from app.auth import create_access_token

from app.auth import verify_token
from fastapi import Depends

import httpx

router = APIRouter()

DOG_API_URL = "https://dog.ceo/api/breed/{breed}/images/random"


@router.get("/dog/breed/{breed_name}")
async def get_dog_image(breed_name: str, _token_data=Depends(verify_token)):
    url = DOG_API_URL.format(breed=breed_name.lower())

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
    except httpx.RequestError as e:
        # Error de red o fallo de conexión
        await collection.insert_one({
            "breed": breed_name.lower(),
            "image_url": None,
            "timestamp": datetime.utcnow(),
            "response_code": 500
        })
        raise HTTPException(
            status_code=500, detail=f"Request failed: {str(e)}") from e

    try:
        data = response.json()
    except Exception as exc:
        await collection.insert_one({
            "breed": breed_name.lower(),
            "image_url": None,
            "timestamp": datetime.utcnow(),
            "response_code": response.status_code
        })
        raise HTTPException(status_code=502, detail="Dog API error") from exc

    # Guardar SIEMPRE
    await collection.insert_one({
        "breed": breed_name.lower(),
        "image_url": data.get("message") if response.status_code == 200 and data.get("status") == "success" else None,
        "timestamp": datetime.utcnow(),
        "response_code": response.status_code
    })

    # Y lanzar excepciones si aplica
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=data.get("message", "Dog API error"))

    if data.get("status") != "success":
        raise HTTPException(status_code=404, detail="Breed not found")

    return {
        "breed": breed_name,
        "image_url": data["message"]
    }


@router.get("/dog/stats")
async def get_stats(_token_data=Depends(verify_token)):
    try:
        pipeline = [
            {"$match": {"image_url": {"$ne": None}}},  # Solo entradas exitosas
            {"$group": {"_id": "$breed", "requests": {"$sum": 1}}},
            {"$sort": {"requests": -1}},
            {"$limit": 10}
        ]
        results = await collection.aggregate(pipeline).to_list(length=10)

        stats = [{"breed": doc["_id"], "requests": doc["requests"]}
                 for doc in results]
        return {"stats": stats}

    except PyMongoError as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"MongoDB error: {str(e)}"}
        )


@router.post("/token")
def login(username: str = Body(...), password: str = Body(...)):
    # Esto es un "login simulado" para pruebas
    if username == "admin" and password == "secret":
        access_token = create_access_token(data={"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
