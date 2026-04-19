import sqlite3 as sql

ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}

def get_ticket_price(destination_city:str):
    print(f"tool called for {destination_city}")
    price = ticket_prices.get(destination_city.lower(),'Price is not known')
    return f"The ticket price for {destination_city} is {price}"

def set_ticket_price(destination_city:str = '',price=0,action='set'):
    conn = sql.connect(r'C:\Users\PGCP-AI\projects\MyLLMLearning\Utils\Tables.db')
    conn.row_factory = sql.Row
    cursor = conn.cursor()
    create_table = """
    CREATE TABLE IF NOT EXISTS cityPrices(
    city TEXT PRIMARY KEY,
    price INTEGER
    )
    """
    destination_city = destination_city.lower()
    city_data = (destination_city,price)

    cursor.execute(create_table)

    add_city_price = """
    INSERT OR REPLACE INTO cityPrices VALUES(?,?)
    """
    get_by_name = """
    SELECT *
    FROM cityPrices
    WHERE city=?
    """
    get_by_price = """
    SELECT *
    FROM cityPrices
    WHERE price=?
    """
    filter_by_price_min = """
    SELECT *
    FROM cityPrices
    WHERE price>=?   
    """
    filter_by_price_max = """
    SELECT *
    FROM cityPrices
    WHERE price<=?   
    """
    match action:
        case 'set':
            cursor.execute(add_city_price,city_data)
            result = f'adding {destination_city} price as {price}'

        case 'get_by_name':
            cursor.execute(get_by_name,(destination_city,))
            print(f'called get_by_name on {destination_city}')
            row = cursor.fetchone()
            result = dict(row)

        case 'get_by_price':
            cursor.execute(get_by_price,(price,))
            print(f'called get_by_price with price {price}')
            rows = cursor.fetchall()
            result = [dict(r) for r in rows]

        case 'filter_by_price_min':
            cursor.execute(filter_by_price_min,(price,))
            print(f'called filter_by_price_min with price {price}')
            rows = cursor.fetchall()
            result = [dict(r) for r in rows]

        case 'filter_by_price_max':
            cursor.execute(filter_by_price_max,(price,))
            print(f'called filter_by_price_max with price {price}')
            rows = cursor.fetchall()
            result = [dict(r) for r in rows]
            
        case _:
            result = 'Invalid Query'

    conn.commit()
    conn.close()
    return f'The result of your query is {result}'