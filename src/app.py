from routes import app

app.static_folder = 'static'

if __name__ == "__main__":
    app.run(port=8000, debug=True)
