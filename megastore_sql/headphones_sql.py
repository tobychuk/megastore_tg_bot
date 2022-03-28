class HeadphonesSQL():
    def __init__(self, cursor):
        self.cursor = cursor

    def create_headphones_table(self):
        query = """
        CREATE TABLE headphones(
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        price VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        available_status TEXT NOT NULL);
        """
        self.cursor.execute(query)
    def update_headphones_table(self, data):
        query = f"""
        INSERT INTO headphones(name, price, description, available_status)
        VALUES(
        '{data.get("name")}',
        '{data.get("price")}',
        '{data.get("description")}',
        '{data.get("available_info")}'
        )
        """
        self.cursor.execute(query)

    def delete_headphones_table(self):
        self.cursor.execute("DROP TABLE headphones")

    def found_headphones_with_name(self, name):
        self.cursor.execute(f"SELECT * FROM headphones WHERE name LIKE '%{name}%'")
        return self.cursor.fetchall()

    def found_headphones_with_id(self, id):
        self.cursor.execute(f"SELECT * FROM headphones WHERE id = {id}")
        return self.cursor.fetchone()