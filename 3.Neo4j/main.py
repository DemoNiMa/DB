from neo4j import GraphDatabase
import re

uri = "bolt://195.133.13.249:7687"
username = "neo4j"
password = "admin"
driver = GraphDatabase.driver(uri, auth=(username, password))


def run_query(driver, query):
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]


def get_all_routes(driver):
    query = "MATCH (n)-[r]->() RETURN DISTINCT type(r) as route"
    return [record['route'] for record in run_query(driver, query)]


def get_all_stops(driver):
    query = "MATCH (s:Station) RETURN s.name as stop"
    return [record['stop'] for record in run_query(driver, query)]


queries = {
    1: {"description": "Получить последовательность остановок для заданного маршрута",
        "subqueries": {
            "route": "Введите маршрут: ",
            "query": lambda route: f"MATCH (a)-[r:{route}]-(b) RETURN DISTINCT a.name"
        }
        },
    2: {"description": "Получить названия организаций, расположенных рядом с заданной остановкой",
        "subqueries": {
            "stop": "Введите название остановки: ",
            "query": lambda stop: f"MATCH (a:Station{{name: '{stop}'}})-[]-(b:Organization) RETURN b.name"
        }
        },
    3: {"description": "Найти все названия остановок, на которых возможны пересадки на другой маршрут",
        "query": "MATCH (b:Station)-[r1]->(),(b:Station)-[r2]->() WHERE type(r1) <> type(r2) RETURN DISTINCT b.name"
        },
    4: {"description": "Найти все названия остановок, на которых останавливается только один маршрут",
        "query": "MATCH (b:Station) WHERE size((b)<--()) = 1 RETURN DISTINCT b.name; "
        },
    5: {"description": "Найти названия учебных организаций и названия остановок, около которых они расположены",
        "query": "MATCH (a:Organization{category:'Учебная организация'})-[r:nearby]-(b) RETURN a.name, b.name"
        },
    6: {"description": "Получить все маршруты от одной заданной остановки до другой заданной остановки (один маршрут)",
        "subqueries": {
            "start": "Введите название начальной остановки: ",
            "end": "Введите название конечной остановки: ",
            "query": lambda start,
                            end: f"MATCH (a:Station {{name:'{start}'}})-[r1]->() WITH DISTINCT type(r1) AS type1 MATCH (b:Station {{name:'{end}'}})-[r2]-() WHERE type(r2) = type1 RETURN DISTINCT type1; "
        }
        },
    7: {
        "description": "Получить все маршруты от одной заданной остановки до другой заданной остановки (разные маршруты)",
        "subqueries": {
            "start": "Введите название начальной остановки: ",
            "end": "Введите название конечной остановки: ",
            "query": lambda start,
                            end: f"MATCH p = (a:Station{{name:'{start}'}})-[*]->(b:Station{{name:'{end}'}}) WITH relationships(p) AS p CALL{{ WITH p UNWIND p AS n RETURN collect(DISTINCT type(n)) AS cn }} RETURN DISTINCT cn AS nameRoute"
        }
    },
    8: {
        "description": "Получить минимальный по количеству остановок маршрут от одной заданной остановки до другой (один маршрут)",
        "subqueries": {
            "start": "Введите название начальной остановки: ",
            "end": "Введите название конечной остановки: ",
            "query": lambda start,
                            end: f"MATCH (a:Station{{name:'{start}'}}), (b:Station{{name:'{end}'}})MATCH p = shortestPath((a)-[*..5]->(b))RETURN p;"
        }
    },
    9: {
        "description": "Получить минимальный по количеству остановок маршрут от одной заданной остановки до другой (разные маршруты)",
        "subqueries": {
            "start": "Введите название начальной остановки: ",
            "end": "Введите название конечной остановки: ",
            "query": lambda start,
                            end: f"MATCH p = shortestPath((a:Station{{name:'{start}'}})-[*]->(b:Station{{name:'{end}'}})) RETURN p"
        }
    },
    10: {"description": "Получить все маршруты, которые проходят через 3 заданные остановки",
         "subqueries": {
             "stop1": "Введите название первой остановки: ",
             "stop2": "Введите название второй остановки: ",
             "stop3": "Введите название третьей остановки: ",
             "query": lambda stop1, stop2, stop3:
             f"MATCH (s1:Station {{name: '{stop1}'}})-[r1]->(), (s2:Station {{name: '{stop2}'}})-[r2]->(), (s3:Station {{name: '{stop3}'}})-[r3]->() WITH type(r1) AS type1, type(r2) AS type2, type(r3) AS type3 WHERE type1 = type2 AND type2 = type3 RETURN DISTINCT type1; "

         }
         },
    11: {"description": "Получить маршрут, который проходит рядом с максимальным количеством магазинов",
         "query": "MATCH p = (a:Station)-[r]-(b:Station) WITH DISTINCT a.name AS vse, type(r) AS ty CALL {     WITH vse     UNWIND vse AS vv     MATCH (a:Station {name: vv})<-[:nearby]-(b:Organization {category: 'Магазин'})     RETURN b AS name_organization } WITH COUNT(name_organization) AS q, ty RETURN q AS count_shop, ty AS name_bus ORDER BY q DESC LIMIT 1; "
         },
    12: {"description": "Получить минимальный по расстоянию маршрут от одной заданной остановки до другой",
         "subqueries": {
             "start": "Введите название начальной остановки: ",
             "end": "Введите название конечной остановки: ",
             "query": lambda start,
                             end: f"MATCH p=((a:Station{{name:'{start}'}})-[*]->(b:Station{{name:'{end}'}})) WITH relationships(p) AS rell, nodes(p) AS nodes, p as stations CALL{{ WITH rell UNWIND rell AS q RETURN sum(q.distance) AS s }} RETURN DISTINCT stations, s ORDER BY s LIMIT 1"
         }
         },
    13: {
        "description": "Найти названия организаций, расположенных рядом с третьей по счету остановкой от заданной остановки",
        "subqueries": {
            "start": "Введите название начальной остановки: ",
            "query": lambda
                start: f"MATCH p = (a:Station{{name:'{start}'}})-[*3]->(b) WITH nodes(p)[3].name AS n CALL{{ WITH n MATCH (:Station{{name:n}})-[:nearby]-(r) RETURN r }} RETURN DISTINCT r.name"
        }
    },
    14: {"description": "Найти все маршруты, длина которых превышает 10 км",
         "query": "MATCH p = (a:Station)-[r]-(b:Station) WITH relationships(p) AS rell, type(r) AS ty UNWIND rell AS r WITH r.distance AS s, ty WITH sum(s)/2 AS summ, ty WHERE summ > 10 RETURN summ, ty ORDER BY summ DESC"
         }
}


def main():
    print("Выберите запрос для выполнения:")
    for key, value in queries.items():
        print(f"{key}. {value['description']}")
    print("0. Выход")

    while True:
        choice = input("\nВведите номер запроса (или 0 для выхода): ")
        if choice == '0':
            break
        elif choice.isdigit() and int(choice) in queries:
            query_info = queries[int(choice)]
            if "subqueries" in query_info:
                subquery_results = []
                if int(choice) == 1:
                    routes = get_all_routes(driver)
                    print(f"Доступные маршруты: {', '.join(routes)}")
                elif int(choice) in [2, 6, 7, 8, 9, 10, 12, 13]:
                    stops = get_all_stops(driver)
                    print(f"Доступные остановки: {', '.join(stops)}")
                for subkey, subquery_prompt in query_info["subqueries"].items():
                    if subkey != "query":
                        user_input = input(subquery_prompt)
                        subquery_results.append(user_input)
                query = query_info["subqueries"]["query"](*subquery_results)
                print(query)
            else:
                query = query_info["query"]
            print(f"\n{query_info['description']}:\n")
            results = run_query(driver, query)
            for record in results:
                print(record)
                """
                match = re.search(r"'(.*?)'", str(record))
                if match:
                    print("  [+]", match.group(1))
                """
        else:
            print("Неверный ввод. Пожалуйста, введите номер запроса или 0 для выхода.")

main()
driver.close()


"""
Данные для тестов:
2 - ул. Хейкконена
6 - Гос. университет, пр. Александра Невского
7 - наб. Варкауса, ул. Московская
8 - пр. Александра Невского, ул. Правды
9 - пр. Александра Невского, гост. Северная
10 - ул. Хейкконена, Сигма, пл. Гагарина
12 - пл. Гагарина, ул. Калинина
13 - ул. Хейкконена
"""
