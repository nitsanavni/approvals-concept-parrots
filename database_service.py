class DatabaseConnection:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connected = False
    
    def connect(self):
        print(f"Connecting to {self.host}:{self.port} as {self.username}")
        self.connected = True
        return True
    
    def query(self, sql):
        if not self.connected:
            raise RuntimeError("Not connected to database")
        
        if sql == "SELECT * FROM users":
            return [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ]
        elif sql == "SELECT COUNT(*) FROM users":
            return [{"count": 2}]
        elif "DROP" in sql.upper():
            raise ValueError("DROP operations not allowed")
        else:
            return []


class UserService:
    def get_all_users(self):
        db = DatabaseConnection("localhost", 5432, "admin", "secret123")
        db.connect()
        return db.query("SELECT * FROM users")
    
    def get_user_count(self):
        db = DatabaseConnection("localhost", 5432, "admin", "secret123")
        db.connect()
        result = db.query("SELECT COUNT(*) FROM users")
        return result[0]["count"] if result else 0
    
    def dangerous_operation(self):
        db = DatabaseConnection("localhost", 5432, "admin", "secret123")
        db.connect()
        return db.query("DROP TABLE users")