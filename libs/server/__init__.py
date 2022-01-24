import flask
import json
import time

from flask import Flask

from libs.syntaxdb.db import Database
from libs.decorators import thread

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.database = Database("syntaxaccounts")

    def query(self, command: str):
        self.database.query(command)

    def run(self, host: str = "localhost", port: int = 8000):
        self.app.run(host, port, debug = False)

    @thread
    def autosave(self, delay: int = 30):
        while True:
            self.query("DUMP")
            time.sleep(delay * 60)