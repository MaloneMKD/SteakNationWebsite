from steaknation import app
from waitress import serve

if __name__ == "__main__":
    # app.run(debug=True)
    serve(app, port=5000)
