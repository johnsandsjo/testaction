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

# --- 3. Database Operations ---
def create_table(conn):
    """Creates a simple 'users' table if it doesn't already exist."""
    cursor = conn.cursor()
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        );
        """
        cursor.execute(create_table_query)
        print("-> Table 'users' created or already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()

def insert_user(conn, name, email):
    """Inserts a new user record into the 'users' table."""
    cursor = conn.cursor()
    try:
        insert_query = sql.SQL(
            "INSERT INTO users (name, email) VALUES ({}, {})"
        ).format(
            sql.Literal(name),
            sql.Literal(email)
        )
        cursor.execute(insert_query)
        print(f"-> Inserted user: {name} ({email})")
    except psycopg2.IntegrityError:
        # Catch duplicate key errors (if email already exists)
        print(f"-> Skipping insert: User with email {email} already exists.")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()

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
