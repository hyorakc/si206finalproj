import sqlite3
import plotly.plotly as py
import plotly.graph_objs as go
import json

options = ['Cat','Dog','Both']

conn = sqlite3.connect('reddit_r_awww.sqlite')
cur = conn.cursor()
cur.execute('SELECT * FROM Imagerec where catvsdog = "Dog"')
dogs = len(cur.fetchall())
cur.execute('SELECT * FROM Imagerec where catvsdog = "Cat"')
cats = len(cur.fetchall())
cur.execute('SELECT * FROM Imagerec where catvsdog = "Cat and Dog"')
boths = len(cur.fetchall())
cur.execute('SELECT * FROM Imagerec where catvsdog = "None"')
nones = len(cur.fetchall())


catups = 0
dogups = 0
bothups = 0
noneups = 0

cur.execute('SELECT * FROM Imagerec')
looker = cur.fetchall()
for _ in looker:
    cur.execute('SELECT upvote FROM Reddit WHERE name = ?', (_[0],))
    num = int(cur.fetchall()[0][0])
    if _[1] == 'Cat':
        catups += num
    elif _[1] == 'Dog':
        dogups += num
    elif _[1] == 'Cat and Dog':
        bothups += num
    else:
        noneups += num



counts = [cats,dogs,boths]

trace = go.Bar(x = options, y = counts)
data = [trace]
print(py.plot(data, filename='cat_vs_dogs_post_counting'))

options = ['Cat upvotes','Dog upvotes','Both']
counts = [catups,dogups,bothups]
trace = go.Bar(x = options, y = counts)
data = [trace]
print(py.plot(data, filename='cat_vs_dogs_upvotes_counting'))


r = open('catvsdog_results.json','w')

totals = dogs + cats + boths + nones

d = {"dogs":{'num of posts':dogs,'percentage of posts':dogs / totals, 'upvotes':dogups}, "cats":{'num of posts':cats,'percentage of posts':cats / totals, 'upvotes': catups}, "both":{"num of posts":boths,'percentage of posts':boths / totals, 'upvotes':bothups}, "neither":{'num of posts':nones,'percentage of posts':nones / totals, 'upvotes':noneups}}

json.dump(d,r)
r.close()