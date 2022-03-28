class KeyboardSQL():
    def __init__(self, cursor):
        self.cursor = cursor

    def create_keyboard_table(self):
        query = """
        CREATE TABLE keyboards(
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        price VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        available_status TEXT NOT NULL);
        """
        self.cursor.execute(query)

    def update_keyboard_table(self, data):
        query = f"""
        INSERT INTO keyboards(name, price, description, available_status)
        VALUES(
        '{data.get("name")}',
        '{data.get("price")}',
        '{data.get("description")}',
        '{data.get("available_info")}'
        )
        """
        self.cursor.execute(query)

    def delete_keyboard_table(self):
        self.cursor.execute("DROP TABLE keyboards")

    def found_keyboard_with_name(self, name):
        self.cursor.execute(f"SELECT * FROM keyboards WHERE name LIKE '%{name}%'")
        return self.cursor.fetchall()
    def found_keyboard_with_id(self, id):
        self.cursor.execute(f"SELECT * FROM keyboards WHERE id = {id}")
        return self.cursor.fetchone()