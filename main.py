from app import create_app

# Create an app instance
app = create_app()

if __name__ == ("__main__"):
    app.run(debug=True)
