# 3th party libraries
import urllib.request, json
import time
import pickle
import sqlite3
import datetime
import os
import pandas
import numpy as np
import matplotlib.pyplot as plt

from AH.wow_api import json_openener


def get_settings():
    # My WOW API key
    key = "g4s923e95jgmyq5w24cra8gpc746b7rt"
    
    if 0:
        server = 'dragonmaw'
    else:
        server = 'kazzak'
    
    return key, server


def main():

    data = get_data()
    lst_auc = data['auctions']
    
    #
    """
    all keys: 'timeLeft', 'quantity', 'bonusLists', 'owner', 'bid', 'rand', 'item', 'buyout', 'context', 'ownerRealm', 'seed', 'auc'
    buyout: in coppers (so /1000 for gold)
    """
    
    df_auc = pandas.DataFrame(data=lst_auc)
    
    lst_interested = []
    
    # find Potion of Prolonged Power
    id_item = 142117
    
    def filter(x):
        b1 = x['item'] == id_item
        b2 = x['buyout'] != 0   # no bids only
        
        return b1 and b2
    
    df_interested = df_auc[df_auc.apply(filter, axis=1)]

    # price per item
    df_interested['mean_buyout'] = df_interested.buyout / df_interested.quantity
    df_sorted = df_interested.sort_values('mean_buyout')
    
    # lst_n = []
    # lst_c = []
    # for index, row in df_sorted.iterrows():
    #     # for x in df_sorted.rows:
    #     lst_n.append(row.quantity)
    #     lst_c.append(row.mean_buyout)
    #
    # lst_n_cum = np.cumsum(lst_n)
    # plt.plot(lst_n_cum, lst_c)

    
    plt.figure(1)
    df_sorted['n_cum'] = df_sorted['quantity'].cumsum()
    df_sorted.plot(x='n_cum', y='mean_buyout')
    plt.yscale('log')
    
    # Interesting keys:
    
    
    # for auc_i in lst_auc:
    #     if auc_i['item'] == id_item:
    #         # add to interested
    #         lst_interested.append(auc_i)a
            
    # df_interested = pandas.DataFrame(data=lst_interested)
    
            
    ...

def get_data(new=False):
    path_file = '/ipi/private/lameeus/code/personal/WoW/data/save.p'
    
    if new:
        key, server = get_settings()
    
        url = "https://eu.api.battle.net/wow/auction/data/{}?locale=en_EU&apikey=".format(server) + key
    
        files = json_openener(url)['files'][0]

        # time
        timestamp_lastmod = files['lastModified']
        t_lastmod = datetime.datetime.fromtimestamp(timestamp_lastmod / 1000.)
        print('date of file: ', t_lastmod)
    
        url_lastmod = files['url']
        files = json_openener(url_lastmod)
        
        pickle.dump(files, open(path_file, "wb"))
        return files
    else:
        return pickle.load(open(path_file, "rb"))
    
    #
    # new_data = False
    # if new_data:
    #     data2 = json_openener(url_lastmod)
    #     picke_saver(data2)
    #
    # data2 = pickle_loader()
    #
    # def picke_saver(dictionary):
    #     pickle.dump(dictionary, open("save.p", "wb"))
    #
    # def pickle_loader():
    #     return pickle.load(open("save.p", "rb"))
    


    
if __name__ == '__main__':
    main()
