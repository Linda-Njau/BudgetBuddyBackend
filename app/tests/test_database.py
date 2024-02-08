import sqlalchemy

# Replace '<your-database-url>' with your actual database URL
database_url = 'sqlite:///test_database.db'

engine = sqlalchemy.create_engine(database_url)
connection = engine.connect()
connection.close()
