"""Trying to optimize the best healing rotation. Although this doesn't make sense, it should give me some ideas how to
opitimize healing done at a certain moment."""

class Spell(object):
    def __init__(self,cast_time:float = 0,  mana = 0, amount = 0, cd = 0):
        self.cast_time = cast_time
        self.mana = mana
        self.amount = amount
        self.cd = cd


def healing_surge():
    return Spell(cast_time= 1.27, mana= 4400, amount=176902, cd = 0 )


class Healing_wave(object):
    cast_time = 2.11
    mana = 19800
    amount = 176902
    cd = 0


class Healing_stream_totem(object):
    cast_time = 0
    mana = 24200
    cd = 30
    time = 15 #s
    amount = 22669
    every = 1.5 #s

def something(options, tot_heal, total_time, t, best_tot_heal):
    # TODO Check which option is off cooldown


    # reached end of time
    if t > total_time:
        if tot_heal > best_tot_heal:
            best_tot_heal = tot_heal
            print("New best hps: {}".format(best_tot_heal/total_time))
        return best_tot_heal

    else:
        for option in options:

            if option.cd == 0:
                tot_heal += option.amount
                t += option.cast_time
                result = something(options, tot_heal, total_time, t, best_tot_heal)
                if result != -1:
                    if result > best_tot_heal:
                        best_tot_heal = result

            # TODO check this....
        return best_tot_heal

hs = healing_surge()
hst = Healing_stream_totem()
hw = Healing_wave()

options = [hw, hs]

total_time = 40 #s
t = 0
tot_heal = 0
best_tot_heal = 0
result = something(options, tot_heal, total_time, t, best_tot_heal)

print("spamming HS: {} HPS".format(hs.amount/hs.cast_time))
print("the ultimate best HPS is {}".format(result/total_time))
