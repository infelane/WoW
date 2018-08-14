from api.item import get_item, get_craft


def get_all_pots():
    # TODO
    lst_id = []
    
    return lst_id


def get_all_flasks():
    lst_id = [152639]

    return lst_id


def print_name(lst_id):
    
    for id in lst_id:
        dict_item = get_item(id)

        print('{} : {}'.format(id, dict_item['name']))


def profit(id):
    dict_item = get_item(id)
    
    end_name = dict_item['name']
    
    
    'itemSource', 'buyPrice', 'sellPrice'
    
    sell_price = dict_item['sellPrice']
    
    craft_spell = get_craft(dict_item['itemSource']['sourceId'])
    
    

def main():
    
    all_pots = get_all_pots()
    all_flasks = get_all_flasks()
    
    print_name(all_flasks)

    profit(all_flasks[0])
    

if __name__ == '__main__':
    main()