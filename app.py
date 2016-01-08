from flask import Flask, render_template, request
import MySQLdb
import MySQLdb.cursors
import simplejson as json
from instance import db_config
from wtforms import *
from pydash import _
import utils

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
            darkages = BooleanField('Dark Ages')

            randomize_button = SubmitField('Get cards!')

        form = RandomizerForm()

        return render_template('main.html', form=form)

    @app.route("/cards", methods=['POST'])
    def cards():
        #grab sets from request.form
        sets = []
        for set in _.keys(request.form):
            if set == 'darkages':
                sets.append("\'Dark Ages\'")
            elif set != 'randomize_button':
                sets.append("\'" + set + "\'")

        where_string = ', '.join(sets)

        query = "SELECT * FROM cards WHERE CardSet IN (%s) ORDER BY RAND() LIMIT 10" % where_string

        cursor.execute(query)

        content = cursor.fetchall()

        img_links = utils.cardImgLinker(content)

        return render_template('cards.html', links=img_links)

    @app.route("/api/v1/allcards")
    def all():
        cursor.execute("SELECT * FROM cards")
        content = cursor.fetchall()
        return json.dumps(content)


    if __name__ == '__main__':
        app.run(debug=True)

