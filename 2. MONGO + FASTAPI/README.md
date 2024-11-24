## **Как установить и запустить:**

 - [ ] **Сменить USER и GROUP!**

**1. Футбол**
Зависимости - ***requirements-1.txt***
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
├── requirements-1.txt           # Файл зависимостей
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
**2. Интернет-магазин**

Зависимости - ***requirements-2.txt***
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
├── requirements-2.txt           # Файл зависимостей
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

**3. Общие настройки**

 - ***Установить зависимости:***
 ```
 pip install -r requirements-1.txt
 или
 pip install -r requirements-2.txt
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

