from app import create_app, db

# Create an app instance
app = create_app()

with app.app_context():
    if db is None:
        db.create_all()


if __name__ == ("__main__"):
    app.run(debug=True)
