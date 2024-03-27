from Database import Database

queries = [

    """CREATE TABLE users(
            user_id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(20) NOT NULL,
            password VARCHAR(20) NOT NULL,
            email VARCHAR(20),
            phone_num VARCHAR(15),
            user_type BOOLEAN

    )""",

    """ CREATE TABLE categories(
            category_id INT PRIMARY KEY AUTO_INCREMENT,
            category_name VARCHAR(50)
    ) """,

    """ CREATE TABLE products(
            product_id INT PRIMARY KEY AUTO_INCREMENT,
            category_id INT,
            product_name VARCHAR(30),
            product_desc VARCHAR(100),
            unit_price DECIMAL(10,2),
            availibility INT UNSIGNED  
    ) """,

    """ CREATE TABLE orders(
            order_id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT, 
            order_date DATE,
            fulfilled BOOLEAN,
            cancled BOOLEAN,
            paid_ammount DECIMAL(10,2)
    ) """,

    """ CREATE TABLE orders_details(
            order_details_id INT PRIMARY KEY AUTO_INCREMENT,
            order_id INT,
            product_id INT,
            price DECIMAL(10,2),
            quantity INT UNSIGNED,
            discount INT,
            total DECIMAL(10,2)
        
    ) """,

    """ALTER TABLE users AUTO_INCREMENT=10001""",

    """ALTER TABLE categories AUTO_INCREMENT=2001""",

    """ALTER TABLE products AUTO_INCREMENT=3001""",

    """ALTER TABLE orders AUTO_INCREMENT=4001""",

    """ALTER TABLE orders_details AUTO_INCREMENT=5001""",

    """ ALTER TABLE products ADD FOREIGN KEY (category_id) REFERENCES categories(category_id)
    """,

    """ ALTER TABLE orders ADD FOREIGN KEY (user_id) REFERENCES users(user_id)
    """,

    """ ALTER TABLE orders_details ADD FOREIGN KEY (order_id) REFERENCES orders(order_id),
        ADD FOREIGN KEY (product_id) REFERENCES products(product_id)
    """
]

def create_database(dbname, conn):
    try:
        cursor = conn.cursor()
        sql = f"CREATE DATABASE {dbname}"
        print(f"EXCECUTING: {sql}")
        cursor.execute(sql)
        print(f"DATABASE {dbname} Create successfully")
    except Exception as e:
        print(f"EXCEPTION OCCOURED: {e}")
    finally:          
        cursor.close()
        conn.close()
        return dbname


def main():
    db = Database()
    con = db.connect()

    dbname = "grocery_store"
    dbname = create_database(dbname, con)

    db.create_tables(queries)

    db.insert("users", 
        username="admin", 
        password="test", 
        email="admin@shop.com", phone_num=123456, user_type=1 
    ) 

    db.insert("users", 
        username="dhruv", 
        password="hello", 
        email="dhruv@shop.com", phone_num=123456, user_type=0 
    ) 
    db.insert("users", 
        username="agrim", 
        password="hello", 
        email="agrim@shop.com", phone_num=123456, user_type=0
    ) 

    db.insert("categories", category_name="Personal Hygine")
    db.insert("categories", category_name="stationary")

    

if(__name__ == "__main__"):
    main()