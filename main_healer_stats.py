""" trying to calculate what stats I want/need """

import requests2
import numpy as np


def request_test(new = True):
    file_name = 'data/data_user'
    if new:
        key = "g4s923e95jgmyq5w24cra8gpc746b7rt"
        char_name = 'neurochain'
        realm_name = 'kazzak'
        fields = 'stats'
    
        url = 'https://eu.api.battle.net/wow/character/{}/{}?fields={}&locale=en_EU&apikey='.format(realm_name, char_name, fields) + key
        
        data = requests2.json_openener(url)
        requests2.save_obj(data, file_name)

    else:
        data = requests2.load_obj(file_name)
        
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

def get_conv():
    conv = np.array([1, 400, 375, 400/3., 475])
    return conv

def conv_rating_to_perc(a):
    """ correct conversion from rating to percentages """
    # int, crit, haste, mastery (3 times as strong for resto shaman), versatility
    conv = get_conv()
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

def data2list_percentage(data):
    return np.array([data['int'], data['crit'], data['haste'], data['mastery'], data['versatilityHealingDoneBonus']])

def data2list_rating(data):
    return np.array([data['int'], data['critRating'], data['hasteRating'], data['masteryRating'], data['versatility']])

def print_data(lst, title):
    print('\n{}:'.format(title))
    print('\tInt: \t{}'.format(lst[0]))
    print('\tCrit: \t{}'.format(lst[1]))
    print('\tHaste: \t{}'.format(lst[2]))
    print('\tMast: \t{}'.format(lst[3]))
    print('\tVers: \t{}'.format(lst[4]))

def calc_delta(data):
    
    spell_coeff_direct = 2.5
    spell_coeff_hot = 2.5
    
    delta_int_direct = 1.05 * spell_coeff_direct * coeff_mastery(data) * coeff_crit(data) * coeff_haste(data) * coeff_vers(data)
    delta_int_hot = 1.05 * spell_coeff_hot * coeff_mastery(data) * coeff_crit(data) * coeff_haste(data) * coeff_vers(data)

    delta_crit_direct = 1.05 * data['int'] * spell_coeff_direct * coeff_mastery(data) * coeff_haste(data) * coeff_vers(data)
    delta_crit_hot = 1.05 * data['int'] * spell_coeff_hot * coeff_mastery(data) * coeff_haste(data) * coeff_vers(data)
    
    delta_intellect = delta_int_direct + delta_int_hot
    
    delta_crit = delta_crit_direct + delta_crit_hot
    
    stats_perc = conv_rating_to_perc(data2list_rating(data))
    
    delta_direct = np.ones((5,))
    delta_hot = np.ones((5,))
    
    conv = get_conv()
    
    mean_coef_direct = spell_coeff_direct
    mean_coef_hot = spell_coeff_hot
    
    # direct
    for i in range(5):
        delta_direct[i] *= 1.05
        for j in range(5):
            if i != j:
                if j == 0:
                    delta_direct[i] *= stats_perc[j]
                elif j == 2:
                    delta_direct[i] *= 1
                else:
                    delta_direct[i] *= coeff_gen(stats_perc[j])
    
        if i != 0:
            # to take into account percentages
            delta_direct[i] /= 100.
            
        if i == 2:
            # haste has no effect
            delta_direct[i] *= 0

        delta_direct[i] *= mean_coef_direct
    
        # TODO take into account that haste increases amount of casts
        # TODO take into account that for shaman crit increases mana refund => amount of heals you can cast
        # TODO take into account does not always give the same percentage

        delta_direct[i] /= conv[i]
    
    # hot
    for i in range(5):
        delta_hot[i] *= 1.05
        for j in range(5):
            if  i != j:
                if j == 0:
                    delta_hot[i] *= stats_perc[j]
                else:
                    delta_hot[i] *= coeff_gen(stats_perc[j])
                    
        if i != 0:
            # to take into account percentages
            delta_hot[i] /= 100.
    
        # HOT directly uses haste
        delta_hot[i] *= mean_coef_hot


        # TODO take into account that haste increases amount of casts
        # TODO take into account that for shaman crit increases mana refund => amount of heals you can cast

        delta_hot[i] /= conv[i]
            
                # delta[i] *= coeff_gen(stats_perc[j])
    delta = delta_direct + delta_hot
    print_data(delta, 'delta')
    
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

    print(stats_perc)
    print(stats_perc_calculated)
    
    print(heal)


def main():
    get_stats()

if __name__ == '__main__':
    main()
