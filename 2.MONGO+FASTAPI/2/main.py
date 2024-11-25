from fastapi import FastAPI, HTTPException, Request, Form, Query
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from generate_products import generate_products

client = MongoClient("mongodb://195.133.13.249:3301")
db = client["22303"]
online_store = db["Demoev-online-store"]

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def initialize_database():
    if online_store.count_documents({}) == 0:
        products = generate_products(20)
        online_store.insert_many(products)

initialize_database()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/products", response_class=HTMLResponse)
async def get_products(request: Request):
    products = list(online_store.find())
    return templates.TemplateResponse("products.html", {"request": request, "products": products})

@app.get("/products/category", response_class=HTMLResponse)
async def get_category_form(request: Request):
    categories = ["Электроника", "Одежда", "Косметика", "Игрушки"]
    return templates.TemplateResponse("category.html", {"request": request, "categories": categories, "products": []})

@app.post("/products/category", response_class=HTMLResponse)
async def get_products_by_category(request: Request, category_name: str = Form(...)):
    products = online_store.find({"category": category_name})
    product_names = [product["name"] for product in products]
    categories = ["Электроника", "Одежда", "Косметика", "Игрушки"]
    return templates.TemplateResponse("category.html", {"request": request, "category_name": category_name, "products": product_names, "categories": categories})

@app.get("/products/category/characteristics", response_class=HTMLResponse)
async def get_characteristics_form(request: Request):
    categories = ["Электроника", "Одежда", "Косметика", "Игрушки"]
    return templates.TemplateResponse("characteristics.html", {"request": request, "categories": categories, "characteristics": []})

@app.post("/products/category/characteristics", response_class=HTMLResponse)
async def get_characteristics_by_category(request: Request, category_name: str = Form(...)):
    products = online_store.find({"category": category_name})
    characteristics = [product["characteristics"] for product in products]
    categories = ["Электроника", "Одежда", "Косметика", "Игрушки"]
    return templates.TemplateResponse("characteristics.html", {"request": request, "category_name": category_name, "characteristics": characteristics, "categories": categories})

@app.get("/products/buyer", response_class=HTMLResponse)
async def get_buyer_form(request: Request):
    buyers = online_store.distinct("buyers.name")
    return templates.TemplateResponse("buyer.html", {"request": request, "buyers": buyers, "products": []})

@app.post("/products/buyer", response_class=HTMLResponse)
async def get_products_by_buyer(request: Request, buyer_name: str = Form(...)):
    products = online_store.find({"buyers.name": buyer_name})
    buyer_products = [{"name": product["name"], "price": product["price"]} for product in products]
    buyers = online_store.distinct("buyers.name")
    return templates.TemplateResponse("buyer.html", {"request": request, "buyer_name": buyer_name, "products": buyer_products, "buyers": buyers})

@app.get("/products/color", response_class=HTMLResponse)
async def get_color_form(request: Request):
    colors = ["красный", "синий", "зеленый", "черный", "белый"]
    return templates.TemplateResponse("color.html", {"request": request, "colors": colors, "products": []})

@app.post("/products/color", response_class=HTMLResponse)
async def get_products_by_color(request: Request, color: str = Form(...)):
    products = online_store.find({"characteristics.color": color})
    colored_products = [{"name": product["name"], "manufacturer": product["manufacturer"], "price": product["price"]} for product in products]
    colors = ["красный", "синий", "зеленый", "черный", "белый"]
    return templates.TemplateResponse("color.html", {"request": request, "color": color, "products": colored_products, "colors": colors})

@app.get("/sales/total", response_class=HTMLResponse)
async def get_total_sales(request: Request):
    products = online_store.find()
    total_sales = sum([product["price"] for product in products])
    return templates.TemplateResponse("total_sales.html", {"request": request, "total_sales": total_sales})

@app.get("/products/category/count", response_class=HTMLResponse)
async def get_category_count(request: Request):
    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}}
    ]
    category_counts = list(online_store.aggregate(pipeline))
    return templates.TemplateResponse("category_count.html", {"request": request, "category_counts": category_counts})

@app.get("/products/buyers", response_class=HTMLResponse)
async def get_product_buyers_form(request: Request):
    products = online_store.distinct("name")
    return templates.TemplateResponse("product_buyers.html", {"request": request, "products": products, "buyers": None})

@app.post("/products/buyers", response_class=HTMLResponse)
async def get_buyers_by_product(request: Request, product_name: str = Form(...)):
    product = online_store.find_one({"name": product_name})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    buyers = [buyer["name"] for buyer in product["buyers"]]
    products = online_store.distinct("name")
    return templates.TemplateResponse("product_buyers.html", {"request": request, "product_name": product_name, "buyers": buyers, "products": products})

@app.get("/products/buyers/delivery", response_class=HTMLResponse)
async def get_delivery_service_form(request: Request):
    delivery_services = ["DHL", "Boxberry", "Почта России"]
    products = online_store.distinct("name")
    return templates.TemplateResponse("product_buyers_delivery.html", {"request": request, "delivery_services": delivery_services, "buyers": None, "product_name": "", "delivery_service": "", "products": products})

@app.post("/products/buyers/delivery", response_class=HTMLResponse)
async def get_buyers_by_delivery_service(request: Request, product_name: str = Form(...), delivery_service: str = Form(...)):
    product = online_store.find_one({"name": product_name})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    buyers = [buyer["name"] for buyer in product["buyers"] if buyer["delivery_service"] == delivery_service]
    delivery_services = ["DHL", "Boxberry", "Почта России"]
    products = online_store.distinct("name")
    return templates.TemplateResponse("product_buyers_delivery.html", {"request": request, "product_name": product_name, "delivery_service": delivery_service, "buyers": buyers, "delivery_services": delivery_services, "products": products})
