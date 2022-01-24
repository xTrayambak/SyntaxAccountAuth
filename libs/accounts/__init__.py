import uuid
import random

def randChar():
    string = ""
    for x in range(random.randint(5, 9)):
        r = random.randint(0, 1)
        if r == 0:
            string += str(r)
        else:
            string += str(
                random.randint(0, 9)+x
            )

    return string

def genUUID(username):
    uid = uuid.uuid4()

    return str(uid) + randChar()

def userExists(username: str, id:int, db):
    data = db.query("GET")

    for user in data:
        if user != "version":
            if data[user]['name'] == username and data[user]['id'] == id:
                return True

    return False

def on_new_account_make(username: str, password: str, id: int, server):
    if userExists(username, id, server.database):
        return "username-exists"

    uid = genUUID(username)
    server.database.query(
        f"create user{uid}"
    )

    server.database.query(f'new user{uid} name "{username}"@string')
    server.database.query(f'new user{uid} password "{password}"@string')

    server.database.query(f'new user{uid} uid "{uid}"@string')
    server.database.query(f'new user{uid} id "{id}"@string')
    server.database.query(f'new user{uid} ownerships []@array')

    server.database.logp(f"A new Syntax Account was made under the username {username}#{id} with UID '{uid}'")

    return uid