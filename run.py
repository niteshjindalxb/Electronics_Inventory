from Inventory import app
from Inventory import views

if __name__ == "__main__":
    views.load_data()
    app.run(debug=True)
