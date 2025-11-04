import psycopg2
from psycopg2 import sql


DB_CONFIG = {
    "host": "localhost",
    "database": "js_db",
    "user": "postgres",
    "password": "password",
    "port": "5432"
}

def connect_db():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    return conn

def create_table(conn):
    """Creates a simple 'user' table"""

    with conn.cursor() as connection:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
            );
        """
        connection.execute(create_table_query)


def insert_user(conn, name, email):
    """Inserts a new user record into the 'users' table."""
    cursor = conn.cursor()
    with conn.cursor() as conncection:
        insert_query = sql.SQL(
            "INSERT INTO users (name, email) VALUES ({}, {})"
        ).format(
            sql.Literal(name),
            sql.Literal(email)
        )
        conncection.execute(insert_query)

def select_all_users(conn):
    """Retrieves and prints all records from the 'users' table."""
    cursor = conn.cursor()
    try:
        print("\n--- Current Users in Database ---")
        cursor.execute("SELECT id, name, email FROM users ORDER BY id;")
        records = cursor.fetchall()
        
        if not records:
            print("No users found.")
            return

        for record in records:
            print(f"ID: {record[0]}, Name: {record[1]}, Email: {record[2]}")
        print("---------------------------------")

    except Exception as e:
        print(f"Error selecting data: {e}")
    finally:
        cursor.close()

# --- 4. Main Execution ---
if __name__ == "__main__":
    
    # 1. Connect to the database
    connection = connect_db()
    
    if connection:
        try:
            # 2. Setup the table
            create_table(connection)
            
            # 3. Insert some data
            insert_user(connection, "Alice Smith", "alice.s@example.com")
            insert_user(connection, "Bob Johnson", "bob.j@example.com")
            insert_user(connection, "Alice Smith", "alice.s@example.com") # Should skip this due to UNIQUE constraint
            
            # 4. Read the data
            select_all_users(connection)
            
        finally:
            # 5. Close the connection
            if connection:
                connection.close()
                print("\nDatabase connection closed.")
    else:
        print("\nApplication aborted due to connection failure.")
