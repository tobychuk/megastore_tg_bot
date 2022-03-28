class CartSQL():
    def __init__(self, cursor):
        self.cursor = cursor

    def create_cart_table(self):
        query = """
CREATE TABLE user_cart(
id INTEGER PRIMARY KEY AUTO_INCREMENT,
owner_username VARCHAR(50) NOT NULL,
owner_first_name VARCHAR(50) NOT NULL,
product_name VARCHAR(100) NOT NULL,
product_price VARCHAR(50) NOT NULL
)"""
        self.cursor.execute(query)


    def add_users_products(self, data):
        query = f"""
INSERT INTO user_cart(owner_username, owner_first_name, product_name, product_price)
VALUES(
'{data.get("username")}','{data.get("first_name")}','{data.get("product_name")}','{data.get("product_price")}')
"""
        self.cursor.execute(query)

    def get_users_products(self, username):
        query = f"""
SELECT * FROM user_cart WHERE owner_username = '{username}'"""
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def del_users_products(self, number):
        query = f"""
DELETE FROM user_cart WHERE id = {number}"""
        self.cursor.execute(query)