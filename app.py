from flask import Flask, render_template, request
from wtforms import *
from pydash import _
import utils
import not_statement
import re
import db

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main():

    #WTForms validators
    def set_checker(form, field):
        if len(request.values) > 2:
            return True
        raise ValidationError('Please select at least one set.')

    def blacklist_checker(form, field):
        if re.match(".*[,;]$", request.values['blacklist']):
            raise ValidationError('Please don\'t have trailing punctuation in the blacklist box.')

    class RandomizerForm(Form):
        base = BooleanField('Base')
        intrigue = BooleanField('Intrigue')
        seaside = BooleanField('Seaside')
        alchemy = BooleanField('Alchemy')
        prosperity = BooleanField('Prosperity')
        cornucopia = BooleanField('Cornucopia')
        hinterlands = BooleanField('Hinterlands')
        darkages = BooleanField('Dark Ages')
        guilds = BooleanField('Guilds')
        adventures = BooleanField('Adventures')
        blacklist = TextAreaField('Blacklisted cards', [blacklist_checker])

        randomize_button = SubmitField('Get cards!', [set_checker])

    form = RandomizerForm(request.values)

    if ('randomize_button' in request.values) and form.validate():

        conn = db.DB()

        sets = []
        for set in _.keys(request.values):
            if set == 'darkages':
                sets.append("\'Dark Ages\'")
            elif set != 'randomize_button' and set != 'blacklist':
                sets.append("\'" + set + "\'")

        where_string = ', '.join(sets)

        query = """CREATE OR REPLACE VIEW picked_cards as
                SELECT * FROM cards
                WHERE CardSet IN ({}) AND ({}) ORDER BY RAND() LIMIT 10""".format(where_string,
                                                                                  not_statement.blacklist(request.values['blacklist']))

        conn.execute(query)

        query = "SELECT * FROM picked_cards ORDER BY CardSet, Cost"

        content = conn.execute(query).fetchall()

        img_links = utils.cardImgLinker(content)

        return render_template('main.html', form=form, links=img_links)

    return render_template('main.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
