from flask import Flask, render_template, request
import MySQLdb
import MySQLdb.cursors
import simplejson as json
from instance import db_config

app = Flask(__name__)

try:
    cnx = MySQLdb.connect(
        host = db_config.config['host'],
        user = db_config.config['user'],
        passwd = db_config.config['password'],
        db = db_config.config['database'],
        cursorclass = MySQLdb.cursors.DictCursor
    )

    cursor = cnx.cursor()

except MySQLdb.Error as err:
    print err

else:

    @app.route("/")
    def main():
        cursor.execute("SELECT * FROM cards")
        content = cursor.fetchall()
        cursor.close()
        return json.dumps(content)


    if __name__ == '__main__':
        app.run(debug=True)

