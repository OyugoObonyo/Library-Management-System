from app import create_app, db

# Create an app instance
app = create_app()

if __name__ == ("__main__"):
    app.run(debug=True)
