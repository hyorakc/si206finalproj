import re
import requests
import requests.auth
import sqlite3
import datetime
import json
import reddit_info


r_account = reddit_info.client_ID
r_secret = reddit_info.client_secret
client_auth = requests.auth.HTTPBasicAuth(r_account,r_secret)
post_data = {"grant_type":"client_credentials"}
headers = {"User-Agent":"uofmsi206finalpj/hyorakc/0.1 by u/foolme_bear"}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
token = response.json()
# print(token)
headers["Authorization"] = " ".join([token['token_type'],token['access_token']])
# headers["limit"] = '20'
r = requests.get("https://oauth.reddit.com/r/awww/hot?limit=100", headers = headers)
# r = requests.get("https://oauth.reddit.com/api/v1/me", headers = headers)
af = r.json()['data']['after']
r2 = requests.get("https://oauth.reddit.com/r/awww/hot?limit=100&after=" + af, headers = headers)
x = open('sample.json','w')
x2 = open('sample2.json','w')
try:
    
    # print(r)
    r_json = r.json()
    # print(r_json)
    r2_json = r2.json()
    json.dump(r_json,x)
    json.dump(r2_json,x2)


    conn = sqlite3.connect('reddit_r_awww.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Reddit')
    cur.execute('CREATE TABLE Reddit (name TEXT, author TEXT, upvote INTEGER, thumburl TEXT, url TEXT, permalink TEXT, catvsdog TEXT)')

    for _ in r_json['data']['children']:
        name = _['data']['id']
        author = _['data']['author']
        upv = int(_['data']['ups'])
        thumburl = _['data']['thumbnail']
        url = _['data']['url']
        p = _['data']['permalink']



        query = '''
		INSERT INTO Reddit (name, author, upvote, thumburl, url, permalink) 
		VALUES (?, ?, ?, ?, ?, ?)
		'''
        attr = (name, author, upv, thumburl, url, p)
        cur.execute(query,attr)

    for _ in r2_json['data']['children']:
        name = _['data']['id']
        author = _['data']['author']
        upv = int(_['data']['ups'])
        thumburl = _['data']['thumbnail']
        url = _['data']['url']
        p = _['data']['permalink']



        query = '''
		INSERT INTO Reddit (name, author, upvote, thumburl, url, permalink) 
		VALUES (?, ?, ?, ?, ?, ?)
		'''
        attr = (name, author, upv, thumburl, url, p)
        cur.execute(query,attr)

    conn.commit()

    
except:
    # print("idk whats happening")
    x.write(r.text)

x.close()