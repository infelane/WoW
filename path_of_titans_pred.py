import numpy as np
np.random.seed(735)

def trinket_names():
    
    return ["Khaz'Goroth's Courage",
            "Golganneth's Vitality",
            "Norgannon's Prowess",
            "Eonar's Compassion",
            "Aggramar's Conviction",
            "Aman'Thul's Vision"]

def numbers():
    Kh = 1
    Go = 1
    No = 1
    Eg = 1
    Ag = 1
    Am = 1  # amantul, everyone
    lst_nr = [Kh, Go, No, Eg, Ag, Am]
    
    # TODO Convert the numbers in some argument list stuff

    lst_nr_arg = np.empty(20)    # -1 is just 'not'
    lst_nr_arg[...] = -1

    lst_nr_cumsum = [None]*6

    for i_trinket in range(6):
        lst_nr_cumsum[i_trinket] = np.sum(lst_nr[0:i_trinket+1])
    
    for i_trinket in range(6):
        if i_trinket == 0:
            lst_nr_arg[0: lst_nr_cumsum[i_trinket]] = i_trinket
        else:
            lst_nr_arg[lst_nr_cumsum[i_trinket-1] : lst_nr_cumsum[i_trinket]] = i_trinket
    
    return lst_nr_arg


class Player():
    def __init__(self, index, trinket_nr=-1):
        self.index = index  # nr of player
        self.trinket_nr = trinket_nr    # nr of the trinket
        
        self.active = False
        self.internal_cd = 0
        self.t_active = 0

        self.chance = 0.15
        
    def next_step(self):
        """
        
        :return: True if the buff started
        """
        if self.internal_cd > 0:
            self.internal_cd -= 1
        
        else:   # only if internal CD is 0, the proc can happen again
            val_rand = np.random.random()
            if val_rand < self.chance:
                self.active = True
                self.t_active = 12
                
                return True
            
        return False


class RaidTeam():
    def __init__(self):
        self.n_players = 20
        self.players = [None]*self.n_players
        nmbrs = numbers()
        for i in range(self.n_players):
            nr_i = nmbrs[i]
            
            self.players[i] = Player(i, trinket_nr = nr_i)
            
        buff_list = [None]*6    # save stuff in here to calculate buff
        
    def next_step(self):
        for i in range(self.n_players):
            player_i = self.players[i]
            bool_start = player_i.next_step()
            
            if bool_start:
                print('active')
                ...


def main():
    t = 500     # seconds
    t_rot = 60
    n_chance = 1
    chance = float(n_chance)/float(t_rot)
    
    raid_team = RaidTeam()
    
    for t_i in range(t):
        print(t_i)
        raid_team.next_step()


if __name__ == '__main__':
    main()
