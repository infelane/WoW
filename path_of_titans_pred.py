import numpy as np
np.random.seed(735)
import matplotlib.pyplot as plt
import matplotlib.patches as patches


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
        
        # Only when trinket nr is >= 0
        
        if self.trinket_nr < 0:
            # no trinket
            return False
        
        elif self.t_active > 0:
            self.t_active -= 1
            self.internal_cd -= 1
            return False
        
        elif self.internal_cd > 0:
            self.internal_cd -= 1
        
        else:   # only if internal CD is 0, the proc can happen again
            val_rand = np.random.random()
            if val_rand < self.chance:
                self.active = True
                self.t_active = 12
                self.internal_cd = 45   # set internal CD
                
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
        self.p_active = []
        
        self.chart = np.zeros((self.n_players, 0))
        
    def next_step(self):
        i_active = 0

        chart_i = np.zeros((self.n_players, 1))
        
        for i in range(self.n_players):
            player_i = self.players[i]
            bool_start = player_i.next_step()
            
            if bool_start:
                print('active')
                ...
                i_active += 1

                chart_i[i] = 1
        
        self.p_active.append(i_active)

        self.chart = np.concatenate([self.chart, chart_i], axis=1)
        
    def get_p_active(self):
        return np.array(self.p_active)
    
    def calc_procs_avg(self):
        # multiply by:
        #   average per minute: now average per sec, so * 60
        # divide by:
        #   12 seconds buff
        #   6 player that have trinket
        return np.mean(self.get_p_active())*60/(6)

def main():
    t = 500     # seconds
    t_rot = 60
    n_chance = 1
    chance = float(n_chance)/float(t_rot)
    
    raid_team = RaidTeam()
    
    for t_i in range(t):
        print(t_i)
        raid_team.next_step()

    p_active = raid_team.get_p_active()
    p_active_mean = np.mean(p_active)
    procs_avg = raid_team.calc_procs_avg()
    plt.plot(p_active)
    plt.title('p_active_mean = {}, procs_avg = {}'.format(p_active_mean, procs_avg))

    fig1 = plt.figure()
    
    # plt.xlim([0, t])
    # plt.ylim([0, 20])
    # plt.xlabel('time [s]')
    # plt.ylabel('player nr.')
    ax1 = fig1.add_subplot(111) #, aspect='equal')
    ax1.set_xlim([0, t])
    ax1.set_ylim([0, 20])
    ax1.set_xlabel('time [s]')
    ax1.set_ylabel('player nr.')

    for i_p in range(20):
        active_i = raid_team.chart[i_p, :]
        
        for i_t in range(t):
            if active_i[i_t] == 1:
                ax1.add_patch(
                    patches.Rectangle(
                        (i_t, i_p),  # (x,y)
                        0.5,  # width
                        0.5,  # height
                        )
                    )

    plt.show()


if __name__ == '__main__':
    main()
