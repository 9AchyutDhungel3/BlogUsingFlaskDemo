# when we are importing from packages( here the 'blog' folder
# ) the thing we are importing must be present in the __init__ file
from blog import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
