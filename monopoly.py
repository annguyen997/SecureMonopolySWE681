from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    page="""<title>Welcome to Monopoly | ISA-681-DL1 | Hoa Luu</title>
    <h1>Welcome to Monopoly | ISA-681-DL1 | Hoa Luu</h1>
  <form action="/new_game">
  <input type="submit" value="New Game">
</form>  """
    return page


@app.route("/new_game")
def new_game():
    page="""<title>Welcome to Monopoly | ISA-681-DL1 | Hoa Luu</title>
    <h1>Generating New Game...</h1> """
    return page


if __name__ == "__main__":
    app.run(host='127.0.0.1',port='8443',debug=True,ssl_context='adhoc')