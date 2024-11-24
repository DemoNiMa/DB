## **MONGODB + FASTAPI**

https://moodle2.petrsu.ru/mod/page/view.php?id=108439
 - [ ] **Обязательно сменить USER и GROUP!**

## **1. Футбол**

```
db = client["Group"]  
collections = {  
    "Игры": db["User-games"],  
    "Футбольные команды": db["User-teams"],  
}
```

**Структура:**
```
1/
│
├── main.py                    # Основной файл приложения FastAPI
│
├── templates/                 # HTML-шаблоны для отображения страниц
│   ├── aggregate.html
│   ├── aggregate_results.html
│   ├── index.html
│   ├── search.html
│   └── search_results.html
│
└── static/                    # Статические файлы (CSS)
    └── style.css

```

## **2. Интернет-магазин**

```
db = client["Group"]  
online_store = db["User-online-store"]
```
**Структура:**
```
2/
│
├── main.py                    # Основной файл приложения FastAPI
├── generate_products.py       # Скрипт для генерации тестовых данных
│
├── templates/                 # HTML-шаблоны для отображения страниц
│   ├── base.html
│   ├── index.html
│   ├── products.html
│   ├── category.html
│   ├── characteristics.html
│   ├── buyer.html
│   ├── color.html
│   ├── total_sales.html
│   ├── category_count.html
│   ├── product_buyers.html
│   └── product_buyers_delivery.html
│
└── static/                    # Статические файлы (CSS)
    └── styles.css

```

## **3. Общие настройки**

 - ***Установка зависимостей:***
 ```
 pip install -r requirements.txt
 ```

 -  ***Запуск через UVICORN:*** 
```
uvicorn main:app --host 127.0.0.1 --port 4000 --reload 
```
 *или* 
 ```
   uvicorn main:app --reload
```
   
   `main` - имя исполняемого файла 
   `--host` и `--port` не обязательные параметры запуска.

