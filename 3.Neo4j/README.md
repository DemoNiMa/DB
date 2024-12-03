# Neo4j

https://moodle2.petrsu.ru/mod/page/view.php?id=108440


**Cypher** – это декларативный язык запросов, специально разработанный для работы с графовыми базами данных, такими как Neo4j. Cypher делает работу с графовыми структурами интуитивной и легкой для понимания благодаря своему синтаксису, который напоминает естественный язык.

Cypher позволяет создавать, читать, обновлять и удалять узлы и связи, обеспечивая полный контроль над графовыми данными.

 Cypher оптимизирован для выполнения сложных графовых запросов, обеспечивая высокую скорость и эффективность работы с большими объемами данных.
 
Cypher предоставляет встроенные функции для выполнения различных графовых алгоритмов, таких как поиск кратчайшего пути, кластеризация и др.
   
## Основные команды:
1. **MATCH** - используется для поиска узлов и связей:
 ```
MATCH (n) RETURN n
```
    
2. **CREATE** - используется для создания узлов и связей:
```
CREATE (n:Person {name: 'Alice'})
```
    
3.  **MERGE** - используется для объединения, при котором создается только новый узел или связь, если они еще не существуют:
```
MERGE (n:Person {name: 'Alice'})
 ```
    
4. **DELETE** - используется для удаления узлов и связей:
```
MATCH (n:Person {name: 'Alice'})
DELETE n
```
    
5. **DETACH DELETE** - используется для удаления узлов вместе со всеми связями:
```
MATCH (n:Person {name: 'Alice'})
DETACH DELETE n
```
    
6. **SET** - используется для установки или обновления свойств:
```
MATCH (n:Person {name: 'Alice'})
SET n.age = 30
```
    
7. **REMOVE** - используется для удаления свойств или меток:
```
MATCH (n:Person {name: 'Alice'})
REMOVE n.age
```

## Дополнительные функции:
8. **Создание связи**:
```
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
CREATE (a)-[:KNOWS]->(b)
 ```
    
9.  **Обновление связей**: 
```
MATCH (a:Person {name: 'Alice'})-[r:KNOWS]->(b:Person {name: 'Bob'})
SET r.since = 2020
```
    
10. **Удаление связей**:
```
MATCH (a:Person {name: 'Alice'})-[r:KNOWS]->(b:Person {name: 'Bob'})
DELETE r
```
    
11. **Поиск по меткам и свойствам**:
```
MATCH (n:Person {age: 30})
RETURN n
```
    
12. **Агрегация данных**:
```
MATCH (n:Person)
RETURN count(n)
```
## Задание (если не подключаетесь к готовому серверу, тут агрегация бд):
0. **Удалить все записи*)
```
MATCH (n) DETACH DELETE n
MATCH r=()-[]-() RETURN r
```

1. **Создание остановок:**
```
CREATE (:Station{name: 'ул. Хейкконена'}),
       (:Station{name: 'ТЦ “Столица”'}),
       (:Station{name: 'Детская Республиканская больница'}),
       (:Station{name: 'Сигма'}),
       (:Station{name: 'ул. Ватутина'}),
       (:Station{name: 'ЖД вокзал'}),
       (:Station{name: 'пл. Гагарина'}),
       (:Station{name: 'Детская художественная школа'}),
       (:Station{name: 'пр. Александра Невского'}),
       (:Station{name: 'ул. Маршала Мерецкова'}),
       (:Station{name: 'СК “Курган”'}),
       (:Station{name: 'ул. Ровио'}),
       (:Station{name: 'ул. Лыжная'}),
       (:Station{name: 'ул. Антонова'}),
       (:Station{name: 'ул. Сегежская'}),
       (:Station{name: 'Ключевское шоссе'}),
       (:Station{name: 'Колледж культуры и искусств'}),
       (:Station{name: 'Речное училище'}),
       (:Station{name: 'ул. Калинина'}),
       (:Station{name: 'ул. Правды'}),
       (:Station{name: 'ул. Пробная'}),
       (:Station{name: 'Металлосклад'}),
       (:Station{name: 'Завод “Славмо”'}),
       (:Station{name: 'пр. Кирова'}),
       (:Station{name: 'ул. Куйбышева'}),
       (:Station{name: 'ул. Ленинградская'}),
       (:Station{name: 'наб. Варкауса'}),
       (:Station{name: 'ул. Московская'}),
       (:Station{name: 'гост. Северная'}),
       (:Station{name: 'Гос. университет'})
```
2. **Создание организаций:**
```
CREATE (:Organization{name: 'Светофор', category:'Магазин'})
CREATE (:Organization{name: 'Школа №46', category:'Учебная организация'})
CREATE (:Organization{name: 'Семерочка', category:'Магазин'})
CREATE (:Organization{name: 'Лотос Плаза', category:'ТЦ'})
CREATE (:Organization{name: 'ИМО', category:'Учебная организация'})
CREATE (:Organization{name: 'Беккер', category:'Магазин'})
CREATE (:Organization{name: 'Суши шоп', category:'Магазин'})
CREATE (:Organization{name: 'Театралка', category:'Учебная организация'})
CREATE (:Organization{name: 'Весна', category:'ТЦ'})
CREATE (:Organization{name: 'Одежда', category:'Магазин'})
CREATE (:Organization{name: 'Школа №22', category:'Учебная организация'})
CREATE (:Organization{name: 'Бочонок', category:'Магазин'})
CREATE (:Organization{name: 'Магнит', category:'Магазин'})
CREATE (:Organization{name: 'ФГБОУ ВО Речное училище', category:'Учебная организация'})
CREATE (:Organization{name: 'Красное и белое', category:'Магазин'})
CREATE (:Organization{name: 'Восторг', category:'Магазин'})
CREATE (:Organization{name: 'Пирамида', category:'Магазин'})
CREATE (:Organization{name: 'ПетрГУ', category:'Учебная организация'})
CREATE (:Organization{name: 'Детский мир', category:'Магазин'})
CREATE (:Organization{name: 'Пятерочка', category:'Магазин'})
CREATE (:Organization{name: 'Школа №35', category:'Учебная организация'})
```

3. **Связь организаций с остановками:**
```
MATCH (a:Station{name: 'ул. Хейкконена'}),  (b:Organization{name: 'Светофор'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'ТЦ “Столица”'}),  (b:Organization{name: 'Школа №46'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'Детская Республиканская больница'}),  (b:Organization{name: 'Семерочка'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'Сигма'}),  (b:Organization{name: 'Лотос Плаза'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'ул. Ватутина'}),  (b:Organization{name: 'ИМО'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'ЖД вокзал'}),  (b:Organization{name: 'Беккер'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'пл. Гагарина'}),  (b:Organization{name: 'Суши шоп'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'Детская художественная школа'}),  (b:Organization{name:'Театралка'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'СК “Курган”'}),  (b:Organization{name: 'Весна'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'ул. Лыжная'}),  (b:Organization{name: 'Одежда'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'ул. Антонова'}),  (b:Organization{name: 'Школа №22'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'ул. Сегежская'}),  (b:Organization{name: 'Бочонок'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'Ключевское шоссе'}),  (b:Organization{name: 'Магнит'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'Речное училище'}),  (b:Organization{name: 'ФГБОУ ВО Речное училище'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'ул. Маршала Мерецкова'}),  (b:Organization{name: 'Красное и белое'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'ул. Правды'}),  (b:Organization{name: 'Восторг'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'пр. Кирова'}),  (b:Organization{name: 'Пирамида'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'Гос. университет'}),  (b:Organization{name: 'ПетрГУ'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'наб. Варкауса'}),  (b:Organization{name: 'Детский мир'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'ул. Куйбышева'}),  (b:Organization{name: 'Пятерочка'})
CREATE  (a)<-[:nearby]-(b);
MATCH (a:Station{name: 'ул. Московская'}),  (b:Organization{name: 'Школа №35'})
CREATE  (a)<-[:nearby]-(b);
```
4. **Создание маршрутов:**
-   **Маршрут №17**:
    ```
    MATCH (a:Station{name: 'ул. Хейкконена'}),
          (b:Station{name: 'ТЦ “Столица”'}),
          (c:Station{name: 'Детская Республиканская больница'}),
          (d:Station{name: 'Сигма'}),
          (e:Station{name: 'ул. Ватутина'}),
          (f:Station{name: 'ЖД вокзал'}),
          (g:Station{name: 'пл. Гагарина'}),
          (h:Station{name: 'Детская художественная школа'}),
          (i:Station{name: 'пр. Александра Невского'}),
          (j:Station{name: 'СК “Курган”'}),
          (k:Station{name: 'ул. Ровио'}),
          (l:Station{name: 'ул. Лыжная'})
    CREATE (a)-[:BUS17 {distance: 1}]->(b),
           (b)-[:BUS17 {distance: 10}]->(c),
           (c)-[:BUS17 {distance: 13}]->(d),
           (d)-[:BUS17 {distance: 2}]->(e),
           (e)-[:BUS17 {distance: 25}]->(f),
           (f)-[:BUS17 {distance: 1}]->(g),
           (g)-[:BUS17 {distance: 3}]->(h),
           (h)-[:BUS17 {distance: 1}]->(i),
           (i)-[:BUS17 {distance: 1}]->(j),
           (j)-[:BUS17 {distance: 3}]->(k),
           (k)-[:BUS17 {distance: 1}]->(l)
    ```
    
-   **Маршрут №22**:
    ```
    MATCH (a:Station{name: 'ул. Хейкконена'}),
          (b:Station{name: 'ТЦ “Столица”'}),
          (c:Station{name: 'Детская Республиканская больница'}),
          (d:Station{name: 'Сигма'}),
          (e:Station{name: 'ул. Ватутина'}),
          (f:Station{name: 'ЖД вокзал'}),
          (g:Station{name: 'пл. Гагарина'}),
          (h:Station{name: 'Гос. университет'}),
          (i:Station{name: 'гост. Северная'}),
          (j:Station{name: 'ул. Куйбышева'}),
          (k:Station{name: 'пр. Кирова'}),
          (l:Station{name: 'ул. Правды'}),
          (m:Station{name: 'ул. Пробная'}), 
          (n:Station{name: 'Металлосклад'}),
          (o:Station{name: 'Завод “Славмо”'})
    CREATE (a)-[:BUS22 {distance: 20}]->(b),
           (b)-[:BUS22 {distance: 1}]->(c),
           (c)-[:BUS22 {distance: 3}]->(d),
           (d)-[:BUS22 {distance: 2}]->(e),
           (e)-[:BUS22 {distance: 1}]->(f),
           (f)-[:BUS22 {distance: 1}]->(g),
           (g)-[:BUS22 {distance: 2}]->(h),
           (h)-[:BUS22 {distance: 1}]->(i),
           (i)-[:BUS22 {distance: 1}]->(j),
           (j)-[:BUS22 {distance: 1}]->(k),
           (k)-[:BUS22 {distance: 9}]->(l),
           (l)-[:BUS22 {distance: 4}]->(m),
           (m)-[:BUS22 {distance: 1}]->(n),
           (n)-[:BUS22 {distance: 2}]->(o)
    ```
    
-   **Маршрут №1**:
    ```
    MATCH (a:Station{name: 'ул. Антонова'}),
          (b:Station{name: 'ул. Сегежская'}),
          (c:Station{name: 'Ключевское шоссе'}),
          (d:Station{name: 'ул. Лыжная'}),
          (e:Station{name: 'ул. Ровио'}),
          (f:Station{name: 'СК “Курган”'})
    CREATE (a)-[:BUS1 {distance: 2}]->(b),
           (b)-[:BUS1 {distance: 1}]->(c),
           (c)-[:BUS1 {distance: 2}]->(d),
           (d)-[:BUS1 {distance: 1}]->(e),
           (e)-[:BUS1 {distance: 3}]->(f)
    
    ```
    
-   **Маршрут №8**:
    ```
    MATCH (a:Station{name: 'наб. Варкауса'}),
          (b:Station{name: 'ул. Ленинградская'}),
          (c:Station{name: 'ул. Куйбышева'}),
          (d:Station{name: 'гост. Северная'}),
          (e:Station{name: 'Гос. университет'}),
          (f:Station{name: 'пл. Гагарина'}),
          (g:Station{name: 'Детская художественная школа'}),
          (h:Station{name: 'пр. Александра Невского'}),
          (i:Station{name: 'ул. Маршала Мерецкова'}),
          (j:Station{name: 'ул. Калинина'}),
          (k:Station{name: 'ул. Правды'}),
          (l:Station{name: 'ул. Пробная'})
    CREATE (a)-[:BUS8 {distance: 1}]->(b),
           (b)-[:BUS8 {distance: 5}]->(c),
           (c)-[:BUS8 {distance: 3}]->(d),
           (d)-[:BUS8 {distance: 3}]->(e),
           (e)-[:BUS8 {distance: 2}]->(f),
           (f)-[:BUS8 {distance: 1}]->(g),
           (g)-[:BUS8 {distance: 2}]->(h),
           (h)-[:BUS8 {distance: 3}]->(i),
           (i)-[:BUS8 {distance: 1}]->(j),
           (j)-[:BUS8 {distance: 1}]->(k),
           (k)-[:BUS8 {distance: 4}]->(l)
    
    ```
    
-   **Маршрут №5**:
    ```
    MATCH (a:Station{name: 'Ключевское шоссе'}),
          (b:Station{name: 'Колледж культуры и искусств'}),
          (c:Station{name: 'Речное училище'}),
          (d:Station{name: 'ул. Калинина'}),
          (e:Station{name: 'ул. Правды'}),
          (f:Station{name: 'пр. Кирова'}),
          (g:Station{name: 'ул. Куйбышева'}),
          (h:Station{name: 'ул. Ленинградская'}),
          (i:Station{name: 'ул. Московская'})
    CREATE (a)-[:BUS5 {distance: 2}]->(b),
           (b)-[:BUS5 {distance: 3}]->(c),
           (c)-[:BUS5 {distance: 2}]->(d),
           (d)-[:BUS5 {distance: 11}]->(e),
           (e)-[:BUS5 {distance: 9}]->(f),
           (f)-[:BUS5 {distance: 1}]->(g),
           (g)-[:BUS5 {distance: 1}]->(h),
           (h)-[:BUS5 {distance: 5}]->(i)
    ```
