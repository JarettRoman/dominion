from lxml import etree
import urllib
from instance import db_config
import MySQLdb
import re

web = urllib.urlopen("http://dominion.diehrstraits.com/?set=All&f=list")
s = re.sub('<(br|hr)>', ', ', web.read())

print s

html = etree.HTML(s)


tr_nodes = html.xpath('//tr')

header = []

for i in tr_nodes[0].xpath("th"):
    header.append(i.text)

content = []
x = 0
for tr in tr_nodes[1:]:
    content.append([])
    for td in tr.xpath('td|td//a|td/br'):
        if td.text:
            content[x].append(td.text)
    print content[x][1:]
    x = x+1

db = MySQLdb.connect(host=db_config.config['host'], user=db_config.config['user'], passwd=db_config.config['password'], db=db_config.config['database'])

cursor = db.cursor()

# print cursor.execute("SELECT 1")
# cursor.execute("""INSERT INTO cards (CardName, CardSet, CardType, Cost, Rules)
#                 VALUES(%s,%s,%s,%s,%s)""", ['a','a','a','a','a'])
# print cursor.fetchall()



for card in content:
    if len(card) > 0:
        print cursor.execute("""INSERT INTO cards (CardName, CardSet, CardType, Cost, Rules)
                       VALUES(%s,%s,%s,%s,%s);""", card[1:])



db.commit()


# cursor.execute("""INSERT INTO cards""")