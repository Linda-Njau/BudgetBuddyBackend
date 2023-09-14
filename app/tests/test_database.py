import sqlalchemy

# Replace '<your-database-url>' with your actual database URL
database_url = 'sqlite:///test_database.db'


try:
    engine = sqlalchemy.create_engine(database_url)
    connection = engine.connect()
    print("Connected to the database successfully")
    
    # Check if the 'User' table exists (replace with your actual table name)
    if engine.dialect.has_table(connection, 'User'):
        print("The 'User' table exists.")
    else:
        print("The 'User' table does not exist.")

    connection.close()
except Exception as e:
    print(f"Database connection error: {e}")
