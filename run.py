from app import create_app, create_database, create_


app = create_app()

if __name__ == "__main__":
    create_database(app)
    
    app.run(debug=True)
