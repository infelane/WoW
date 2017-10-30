""" Script to check the auction house """

# 3th party libraries
import urllib.request, json
import time
import pickle
import sqlite3


def main():
    # My WOW API key
    key = "g4s923e95jgmyq5w24cra8gpc746b7rt"
    
    if 0:
        server = 'dragonmaw'
    else:
        server = 'kazzak'

    url = "https://eu.api.battle.net/wow/auction/data/{}?locale=en_EU&apikey=".format(server) + key

    data = json_openener(url)

    data = data['files'][0]

    print(data)

    t_lastmod = data['lastModified']
    url_lastmod = data['url']

    print(t_lastmod)
    sec2other(t_lastmod)

    new_data = False
    if new_data:
        data2 = json_openener(url_lastmod)
        picke_saver(data2)

    data2 = pickle_loader()
    # print(data2)

    # save data as SQL database
    for foo in data2['auctions'][0]:
        print(foo)

    print(data2['auctions'][0])

    new_sql= False
    if new_sql:
        make_sql()
        save_sql(data2['auctions'])

    sql_command = """ SELECT *
    FROM auction
    WHERE owner = 'Naidaddy'"""
    sql_select(sql_command)


def sql_select(sql_command):
    connection = sqlite3.connect("ah.db")
    cursor = connection.cursor()

    cursor.execute(sql_command)
    result = cursor.fetchall()
    print(cursor.description)
    for r in result:
        print(r)

def picke_saver(dictionary):
    pickle.dump(dictionary, open("save.p", "wb"))


def pickle_loader():
    return pickle.load(open("save.p", "rb"))


def json_openener(url_link):
    start = time.time()
    with urllib.request.urlopen(url_link) as url:
        data = json.loads(url.read().decode())
    end = time.time()
    print("took {} secs".format(end - start))
    return data


# url = "http://maps.googleapis.com/maps/api/geocode/json?address=google"
# url = "http://auction-api-us.worldofwarcraft.com/auction-data/64562f637ba0d2475075c0d61648d512/auctions.json"
#
# status_URL = "http://us.battle.net/api/wow/auction/data/boulderfist"
#
# url = "https://us.api.battle.net/wow/auction/data/:realm-slug?locale=:preferred-locale&apikey=:your-key-here"
#
# key = "g4s923e95jgmyq5w24cra8gpc746b7rt"
# url = "https://us.api.battle.net/wow/auction/data/:dragonmaw?locale=:en_EU&apikey=:" + key
#
# url = "https://us.api.battle.net/wow/auction/data/dragonmaw?locale=en_EU&apikey=g4s923e95jgmyq5w24cra8gpc746b7rt"
#
#
# with urllib.request.urlopen(url) as url:
#     data = json.loads(url.read().decode())
#     print(data)
#
#
#
#
#     # a = data.read()
#     # print(data[0])
#



def save_sql(data):
    # init
    connection = sqlite3.connect("ah.db")
    cursor = connection.cursor()

    format_str = """INSERT INTO auction (owner, ownerrealm, itemid, buyout, auc, context, quantity, timeleft, seed, bid, rand)
    VALUES ("{owner}", "{ownerRealm}", "{item}", "{buyout}", "{auc}", "{context}" , "{quantity}" , "{timeLeft}" , "{seed}" , "{bid}" , "{rand}");"""

    for data_i in data:
        sql_command = format_str.format(**data_i)
        cursor.execute(sql_command)

    connection.commit()
    connection.close()

def make_sql():
    connection = sqlite3.connect("ah.db")
    cursor = connection.cursor()

    sql_command = """
    CREATE TABLE auction (
    auctionid INTEGER PRIMARY KEY,
    owner VARCHAR(20),
    ownerrealm VARCHAR(20),
    itemid INT,
    buyout REAL,
    auc INT,
    context INT,
    quantity INT,
    timeleft VARCHAR(10),
    seed INT,
    bid REAL,
    rand INT);"""

    cursor.execute(sql_command)
    connection.close()


def sec2other(sec):
    date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sec/1000))
    print(date_time)


# sql_command = """INSERT INTO employee (staff_number, fname, lname, gender, birth_date)
#     VALUES (NULL, "William", "Shakespeare", "m", "1961-10-25");"""
# cursor.execute(sql_command)
#
#
# sql_command = """INSERT INTO employee (staff_number, fname, lname, gender, birth_date)
#     VALUES (NULL, "Frank", "Schiller", "m", "1955-08-17");"""
# cursor.execute(sql_command)
#
# connection.commit()
# # connection.close()
#
#
# staff_data = [ ("William", "Shakespeare", "m", "1961-10-25"),
#                ("Frank", "Schiller", "m", "1955-08-17"),
#                ("Jane", "Wall", "f", "1989-03-14") ]
#
# for p in staff_data:
#     format_str = """INSERT INTO employee (staff_number, fname, lname, gender, birth_date)
#     VALUES (NULL, "{first}", "{last}", "{gender}", "{birthdate}");"""
#
#     sql_command = format_str.format(first=p[0], last=p[1], gender=p[2], birthdate = p[3])
#     cursor.execute(sql_command)
#
# cursor.execute("SELECT * FROM employee")
# result = cursor.fetchall()
# for r in result:
#     print(r)
#
# res = cursor.fetchone()
# print(res)
#
#     # sql_commqnd = """SELECT * FROM employee"""
# # sql_result = cursor.execute(sql_command)
# # print(sql_result)

if __name__ == '__main__':
    main()
