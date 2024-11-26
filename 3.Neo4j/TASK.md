Лучше тестировать с запросами из кода, тут есть неточности и не всегда проходят валидацию sypher.


-   **Получить последовательность остановок для заданного маршрута**:
    ```
    MATCH (a)-[r:BUS5]-(b)
    RETURN DISTINCT a.name
    
    ```
    
-   **Получить названия организаций, расположенных рядом с заданной остановкой**:
    ```
    MATCH (a:Station{name: 'ул. Хейкконена'})-[]-(b:Organization)
    RETURN b.name
    
    ```
    
-   **Найти все названия остановок, на которых возможны пересадки на другой маршрут**:
    ```
    MATCH (b:Station)-[r1]->(),(b:Station)-[r2]->()
    WHERE type(r1) <> type(r2)
    RETURN DISTINCT b.name
    
    ```
    
-   **Найти все названия остановок, на которых останавливается только один маршрут**:
    ```
    MATCH ()-[r1]->(b:Station)
    WHERE (count{()-->(b)} = 1)
    RETURN DISTINCT b.name
    
    ```
    
-   **Найти названия учебных организаций и названия остановок, около которых они расположены**:
    ```
    MATCH (a:organization{category:"Учебная организация"})-[r:nearby]-(b)
    RETURN a.name, b.name
    
    ```
    
-   **Получить все маршруты от одной заданной остановки до другой заданной остановки (один маршрут)**:
    ```
    MATCH(a:Station{name:'Гос. университет'})-[r1]->(),(b:Station{name:'пр. Александра Невского'})-[r2]-() 
    WHERE type(r1) = type(r2) 
    RETURN DISTINCT type(r1)
    
    ```
    
-   **Получить все маршруты от одной заданной остановки до другой заданной остановки (разные маршруты)**:
    ```
    MATCH p = (a:Station{name:'наб. Варкауса'})-[*]->(b:Station{name:'ул. Московская'}) 
    WITH relationships(p) AS p
    CALL{
        WITH p
        UNWIND p AS n
        RETURN collect(DISTINCT type(n)) AS cn 
    }
    RETURN DISTINCT cn AS nameRoute
    
    ```
    
-   **Получить минимальный по количеству остановок маршрут от одной заданной остановки до другой заданной остановки (один маршрут)**:
    ```
    MATCH (a:Station{name:"пр. Александра Невского"})-[r1]-(), (b:Station{name:"ул. Правды"})-[r2]-(), p=shortestPath((a)-[*]->(b))
    WHERE type(r1) = type(r2) 
    RETURN p
    
    ```
    
-   **Получить минимальный по количеству остановок маршрут от одной заданной остановки до другой заданной остановки (разные маршруты)**:
    ```
    MATCH p = shortestPath((a:Station{name:"пр. Александра Невского"})-[*]->(b:Station{name:"гост. Северная"}))
    RETURN p
    
    ```
    
-   **Получить все маршруты, которые проходят через 3 заданные остановки**:
    ```
    MATCH (:Station{name: 'ул. Хейкконена'})-[r1]->(), 
          (:Station{name: 'Сигма'})-[r2]->(), 
          (:Station{name: 'пл. Гагарина'})-[r3]->() 
    WHERE type(r1) = type(r2) = type(r3) 
    RETURN DISTINCT type(r1)
    
    ```
    
-   **Получить маршрут, который проходит рядом с максимальным количеством магазинов**:
    ```
	MATCH (a:Station)-[r]-(b:Station)
	WITH DISTINCT a, type(r) AS routeType
	OPTIONAL MATCH (a)<-[:nearby]-(org:Organization{category:'Магазин'})
	RETURN routeType, count(org) AS shopCount
	ORDER BY shopCount DESC
	LIMIT 1

    ```
    
-   **Получить минимальный по расстоянию маршрут от одной заданной остановки до другой заданной остановки**:
    ```
    MATCH p=((a:Station{name:'пл. Гагарина'})-[*]->(b:Station{name:'ул. Калинина'}))
    WITH relationships(p) AS rell, nodes(p) AS nodes, p as stations
    CALL{
        WITH rell 
        UNWIND rell AS q
        RETURN sum(q.distance) AS s
    }
    RETURN DISTINCT stations, s
    ORDER BY s
    LIMIT 1
    
    ```
    
-   **Найти названия организаций, расположенных рядом с третьей по счету остановкой от заданной остановки**:
    ```
    MATCH p = (a:Station{name:'ул. Хейкконена'})-[*3]->(b)
    WITH nodes(p)[3].name AS n
    CALL{
        WITH n 
        MATCH (:Station{name:n})-[:nearby]-(r) 
        RETURN r
    }
    RETURN DISTINCT r.name
    
    ```
    
-   **Найти все маршруты, длина которых превышает 10 км**:
    ```
    MATCH p = (a:Station)-[r]-(b:Station)
    WITH relationships(p) AS rell, type(r) AS ty
    CALL{
        WITH rell
        UNWIND rell AS r
        RETURN r.distance AS s
    } 
    WITH sum(s)/2 AS summ, ty
    WHERE summ > 10
    RETURN summ, ty
    ORDER BY summ DESC
    ```
