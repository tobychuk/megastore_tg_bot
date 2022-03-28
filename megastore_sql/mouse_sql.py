class MouseSQL():
    def __init__(self, cursor):
        self.cursor = cursor

    def create_mouse_table(self):
        query = """
        CREATE TABLE mouses(
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        price VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        available_status TEXT NOT NULL);
        """
        self.cursor.execute(query)

    def update_mouse_table(self, data):
        query = f"""
        INSERT INTO mouses(name, price, description, available_status)
        VALUES(
        '{data.get("name")}',
        '{data.get("price")}',
        '{data.get("description")}',
        '{data.get("available_info")}'
        )
        """
        self.cursor.execute(query)

    def delete_mouse_table(self):
        self.cursor.execute("DROP TABLE mouses")

    def found_mouse_with_name(self, name):
        self.cursor.execute(f"SELECT * FROM mouses WHERE name LIKE '%{name}%'")
        return self.cursor.fetchall()

    def found_mouse_with_id(self, id):
        self.cursor.execute(f"SELECT * FROM mouses WHERE id = {id}")
        return self.cursor.fetchone()

