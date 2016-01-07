from flask import Flask, render_template, request
import MySQLdb
import MySQLdb.cursors
import simplejson as json
from instance import db_config
from wtforms import *
from pydash import _

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

    @app.route("/", methods=['GET', 'POST'])
    def main():
        class RandomizerForm(Form):
            base = BooleanField('Base')
            intrigue = BooleanField('Intrigue')
            prosperity = BooleanField('Prosperity')
            seaside = BooleanField('Seaside')

            randomize_button = SubmitField('Get cards!')

        form = RandomizerForm()

        return render_template('main.html', form=form)

    @app.route("/cards", methods=['POST'])
    def cards():
        #grab sets from request.form
        sets = []
        for set in _.keys(request.form):
            if set != 'randomize_button':
                sets.append("CardSet = " + "\'" + set + "\'")

        where_string = ' or '.join(sets)

        query = "SELECT * FROM cards WHERE %s" % where_string


        cursor.execute(query)

        content = cursor.fetchall()

        return json.dumps(content)

    @app.route("/api/v1/allcards")
    def all():
        cursor.execute("SELECT * FROM cards")
        content = cursor.fetchall()
        return json.dumps(content)


    if __name__ == '__main__':
        app.run(debug=True)

