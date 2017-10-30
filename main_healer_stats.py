""" trying to calculate what stats I want/need """

import requests
import numpy as np


def request_test(new = True):
    file_name = 'data/data_user'
    if new:
        key = "g4s923e95jgmyq5w24cra8gpc746b7rt"
        char_name = 'neurochain'
        realm_name = 'kazzak'
        fields = 'stats'
    
        url = 'https://eu.api.battle.net/wow/character/{}/{}?fields={}&locale=en_EU&apikey='.format(realm_name, char_name, fields) + key
        
        data = requests.json_openener(url)
        requests.save_obj(data, file_name)

    else:
        data = requests.load_obj(file_name)
        
    return data['stats']

def coeff_gen(a):
    # percentage to multiplier
    return 1. + a/100.

def coeff_crit(a):
    if type(a) is dict:
        return coeff_gen(a['crit'])
    else:
        return coeff_gen(a)

def coeff_haste(a):
    if type(a) is dict:
        return coeff_gen(a['haste'])
    else:
        return coeff_gen(a)

def coeff_vers(a):
    if type(a) is dict:
        return coeff_gen(a['versatilityHealingDoneBonus'])
    else:
        return coeff_gen(a)

def coeff_mastery(a):
    if type(a) is dict:
        return coeff_gen(a['mastery'])
    else:
        return coeff_gen(a)
    
def conv_haste_rating_to_perc(haste_rating):
    # rating to percentage
    return haste_rating/400

def conv_rating_to_perc(a):
    # int, crit, haste, mastery (3 times as strong for resto shaman), versatility
    conv = np.array([1, 400, 375, 400*3, 475])
    # 5% crit basis, 24 base mastery (or 8*3)
    bias = np.array([0, 5, 0, 24, 0])
    return a/conv + bias

def calc_riptide(intellect, haste, crit, mastery, versatility):
    # riptide: 2.5*spell_power + 2.5*spell_power (over 15s)
    # 5 % bonus intellect from wearing all mail
    
    spell_coeff_direct = 2.5
    spell_coeff_hot = 2.5
    
    power_heal_direct = (intellect*1.05)*spell_coeff_direct*coeff_mastery(mastery)*coeff_crit(crit)*coeff_vers(versatility)
    power_hot = (intellect*1.05)*spell_coeff_hot*coeff_mastery(mastery)*coeff_crit(crit)*coeff_vers(versatility)*coeff_haste(haste)
    
    return power_heal_direct + power_hot

def calc_delta(data):
    
    spell_coeff_direct = 2.5
    spell_coeff_hot = 2.5
    
    delta_int_direct = 1.05 * spell_coeff_direct * coeff_mastery(data) * coeff_crit(data) * coeff_haste(data) * coeff_vers(data)
    delta_int_hot = 1.05 * spell_coeff_hot * coeff_mastery(data) * coeff_crit(data) * coeff_haste(data) * coeff_vers(data)

    delta_crit_direct = 1.05 * data['int'] * spell_coeff_direct * coeff_mastery(data) * coeff_haste(data) * coeff_vers(data)
    delta_crit_hot = 1.05 * data['int'] * spell_coeff_hot * coeff_mastery(data) * coeff_haste(data) * coeff_vers(data)
    
    delta_intellect = delta_int_direct + delta_int_hot
    
    delta_crit = delta_crit_direct + delta_crit_hot
    
    return {'d_int':delta_intellect, 'd_crit':delta_crit}

def get_stats():

    data = request_test(False)
    
    # percentages
    intellect = data['int']
    crit = data['crit']
    haste = data['haste']
    mastery = data['mastery']
    vers = data['versatilityHealingDoneBonus']

    # values:
    crit_rating = data['critRating']
    haste_rating = data['hasteRating']
    mastery_rating = data['masteryRating']
    vers_rating = data['versatility']

    # riptide:
    # 2.5*spell_power + 2.5*spell_power (over 15s)

    spell_coef = 100

    mastery_perc = 1*mastery
    
    heal = calc_riptide(intellect, haste, crit, mastery, vers)

    a = calc_delta(data)
    
    stats_perc = [intellect, crit, haste, mastery, vers]
    stats_rating = [intellect, crit_rating, haste_rating, mastery_rating, vers_rating]
    stats_perc_calculated = conv_rating_to_perc(stats_rating)
    
    print(heal)


def main():
    get_stats()

if __name__ == '__main__':
    main()
