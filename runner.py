import flask

from libs.server import Server
from libs.decorators import thread
from libs.accounts import on_new_account_make

server = Server()

@thread
def start_flask_server():
    server.run()

@server.app.route("/confirmaction")
def confirmaction():
    username = flask.request.args["username"]
    id = flask.request.args["id"]
    password = flask.request.args["password"]

    users_data = server.database.query("GET")

    for user in users_data:
        if user != "version": 
            if users_data[user]["name"] == username and users_data[user]["password"] == password and users_data[user]["id"] == id:
                return flask.jsonify(
                    {
                        "authenticated": True,
                        "owns": [users_data[user]["ownerships"]],
                        "uid": users_data[user]["uid"]
                    }
                )

            else:
                return flask.jsonify(
                    {
                        "authenticated": False,
                        "owns": [],
                        "uid": "not-found"
                    }
                )

    return flask.jsonify(
        {
            "result": "error",
            "owns": [],
            "uid": "not-found"
        }
    )
    

@server.app.route("/signup")
def signup():
    username = flask.request.args["username"]
    password = flask.request.args["password"]
    id = flask.request.args["id"]

    token = on_new_account_make(username, password, id, server)
    if token == "username-exists": return flask.jsonify({"result":token, "token": "not-generated"})
    return flask.jsonify({"result": "success", "token": token})

def run():
    start_flask_server()

    server.database.load()
    server.autosave()

if __name__ == "__main__":
    run()