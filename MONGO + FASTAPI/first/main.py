from fastapi import FastAPI, HTTPException, Request
from fastapi import Query
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
from bson.objectid import ObjectId
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
from pydantic import BaseModel

# Подключение к MongoDB
client = MongoClient("mongodb://192.168.112.103:27017/")
db = client["22303"]
collections = {
    "Игры": db["Demoev-games"],
    "Футбольные команды": db["Demoev-teams"],
}

# Инициализация FastAPI
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/search", response_class=HTMLResponse)
async def search_page(request: Request):
    """Страница для поиска документов."""
    collections_list = list(collections.keys())
    return templates.TemplateResponse("search.html", {"request": request, "collections": collections_list})

@app.get("/aggregate", response_class=HTMLResponse)
async def aggregate_page(request: Request):
    """Страница для агрегации документов."""
    collections_list = list(collections.keys())
    return templates.TemplateResponse("aggregate.html", {"request": request, "collections": collections_list})

@app.get("/search_results", response_class=HTMLResponse)
async def search_documents(request: Request, collection_name: str = Query(...), key: str = Query(...), comparison: str = Query(...), value: float = Query(...)):
    """Поиск документов с использованием ключа, знака сравнения и значения."""
    if collection_name not in collections:
        raise HTTPException(status_code=404, detail="Коллекция не найдена")

    collection = collections[collection_name]
    query = {}

    if comparison == "=":
        query[key] = value
    elif comparison == ">":
        query[key] = {"$gt": value}
    elif comparison == ">=":
        query[key] = {"$gte": value}
    elif comparison == "<":
        query[key] = {"$lt": value}
    elif comparison == "<=":
        query[key] = {"$lte": value}
    else:
        raise HTTPException(status_code=400, detail="Некорректный знак сравнения")

    documents = list(collection.find(query))
    for doc in documents:
        doc["_id"] = str(doc["_id"])  # Преобразуем ObjectId в строку для передачи в JSON
    return templates.TemplateResponse("search_results.html", {"request": request, "documents": documents})

@app.get("/aggregate_results", response_class=HTMLResponse)
async def aggregate_documents(request: Request, collection_name: str = Query(...), query: str = Query(...)):
    """Агрегация документов с использованием команды для поиска."""
    if collection_name not in collections:
        raise HTTPException(status_code=404, detail="Коллекция не найдена")

    collection = collections[collection_name]
    try:
        aggregation_query = json.loads(query)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Некорректный формат запроса")

    documents = list(collection.aggregate(aggregation_query))
    for doc in documents:
        doc["_id"] = str(doc["_id"])  # Преобразуем ObjectId в строку для передачи в JSON
    return templates.TemplateResponse("aggregate_results.html", {"request": request, "documents": documents})



class KeyValueInput(BaseModel):
    key: str
    value: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Главная страница с выбором коллекции."""
    return templates.TemplateResponse("index.html", {"request": request, "collections": list(collections.keys())})

@app.get("/documents/{collection_name}")
async def get_documents(collection_name: str):
    """Получить все документы из коллекции."""
    if collection_name not in collections:
        raise HTTPException(status_code=404, detail="Коллекция не найдена")

    collection = collections[collection_name]
    documents = list(collection.find())
    for doc in documents:
        doc["_id"] = str(doc["_id"])  # Преобразуем ObjectId в строку для передачи в JSON
    return {"documents": documents}

@app.post("/documents/{collection_name}")
async def create_document(collection_name: str):
    """Создать новый документ с готовыми ключами и пустыми значениями."""
    if collection_name not in collections:
        raise HTTPException(status_code=404, detail="Коллекция не найдена")

    collection = collections[collection_name]

    if collection_name == "Футбольные команды":
        new_document = {
            "name": "",
            "city": "",
            "coach_full_name": "",
            "starting_lineup": [{"full_name": "", "position": ""}],
            "substitute_players": [{"full_name": "", "position": ""}]
        }
    elif collection_name == "Игры":
        new_document = {
            "event_date": "",
            "score": "",
            "rule_violations": [{"card_type": "", "minute": "", "reason": ""}],
            "goals": [{"position": "", "minute": "", "author": "", "assist": ""}],
            "penalties": [{"position": "", "minute": "", "author": "", "assist": ""}],
            "shots_on_goal": [{"position": "", "minute": "", "author": ""}]
        }
    else:
        new_document = {}
    print(collection_name)
    print(new_document)
    result = collection.insert_one(new_document)
    return {"message": "Документ создан", "id": str(result.inserted_id)}


@app.put("/documents/{collection_name}/{document_id}")
async def update_document(collection_name: str, document_id: str, input_data: KeyValueInput):
    """Обновить документ (добавить или обновить ключ-значение)."""
    if collection_name not in collections:
        raise HTTPException(status_code=404, detail="Коллекция не найдена")

    collection = collections[collection_name]
    try:
        value = json.loads(input_data.value)  # Попытка преобразовать значение в JSON-объект
    except json.JSONDecodeError:
        value = input_data.value  # Если не получилось, оставляем значение строкой

    # Используем точечную нотацию для вложенных ключей
    update_op = {"$set": {input_data.key: value}}

    result = collection.update_one({"_id": ObjectId(document_id)}, update_op)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Документ не найден")
    return {"message": "Документ обновлён"}


@app.delete("/documents/{collection_name}/{document_id}")
async def delete_document(collection_name: str, document_id: str):
    """Удалить документ по ID."""
    if collection_name not in collections:
        raise HTTPException(status_code=404, detail="Коллекция не найдена")

    collection = collections[collection_name]
    result = collection.delete_one({"_id": ObjectId(document_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Документ не найден")
    return {"message": "Документ удалён"}




""" 4 пункт - тест
Подсчет количества нарушений
[
    { "$unwind": "$rule_violations" },
    { "$group": { "_id": "$rule_violations.card_type", "count": { "$sum": 1 } } }
]

Подсчет количества голов
[
    { "$unwind": "$goals" },
    { "$group": { "_id": "$_id", "total_goals": { "$sum": 1 } } }
]

"""