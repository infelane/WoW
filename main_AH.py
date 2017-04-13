""" Script to check the auction house """

import urllib.request, json

def main():
    # My WOW API key
    key = "g4s923e95jgmyq5w24cra8gpc746b7rt"

    url = "https://us.api.battle.net/wow/auction/data/dragonmaw?locale=en_EU&apikey=" + key

    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())['files'][0]

    print(data)

    t_lastmod = data['lastModified']
    url_lastmod = data['url']
    print(t_lastmod)

    with urllib.request.urlopen(url) as url:

    sec2other(t_lastmod)

def json_openener():
    

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
# a = 1/0
#
def sec2other(sec):
    import time
    date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sec/1000))
    print(date_time)

# import sqlite3
# connection = sqlite3.connect("ah.db")
#
# cursor = connection.cursor()
#
# sql_command = """
# CREATE TABLE employee (
# staff_number INTEGER PRIMARY KEY,
# fname VARCHAR(20),
# lname VARCHAR(30),
# gender CHAR(1),
# joining DATE,
# birth_date DATE);"""
#
# # cursor.execute(sql_command)
#
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
