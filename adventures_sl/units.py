from adventures_sl.abilities import Melee, GoliathSlam, FleshEruption

MELEE = 'melee'
RANGED = 'ranged'


class Unit:
    health: int = 0
    attack: int = 0

    def __init__(self,
                 health: int = 0,
                 attack: int = 0
                 ):
        self.attack = attack
        self.health = health

    def set_callback_dead(self, f):
        self.callback_dead = f

    def reduce_hp(self, value: int):
        assert isinstance(value, int)
        assert value >= 0
        self.health = max(0, self.health - value)

        if self.health <= 0:
            print(f'{self} - dead')
            self.callback_dead()
        # TODO check dead state

    def get_attack(self):
        return self.attack

    def fight(self, battle):
        move = Melee(self, self.get_attack())
        log = move.do(battle)

        return log

    def __str__(self):
        return f'{self.__class__.__name__}(hp={self.health})'

class Enemy(Unit):
    def __init__(self,
                 lvl: int = 0,
                 health: int = 0,
                 attack: int = 0):
        self.health = health
        self.attack = attack
        self.lvl = lvl


class Friendly(Unit):

    def __init__(self,
                 lvl: int = 0,
                 health: int = 0,
                 attack: int = 0):
        self.health = health
        self.attack = attack
        self.lvl = lvl


# For testing
class ExampleEnemy(Enemy):
    def __init__(self,
                 health=250,
                 attack=10):
        super(ExampleEnemy, self).__init__(health=health, attack=attack)

    def __str__(self):
        return "Example enemy"


class ExampleFriendly(Friendly):
    def __init__(self, health=180,
                 attack=20):
        super(ExampleFriendly, self).__init__(health=health, attack=attack)

    def __str__(self):
        return "Example friendly"


class DarkGoliath(Enemy):
    """
    From "Dark Goliath's Rampage".
    """

    def __init__(self, lvl):
        if lvl == 14:
            health = 4452
            attack = 72
        else:
            # TODO
            raise NotImplemented()

        super(DarkGoliath, self).__init__(health=health, attack=attack)

        self.abilities = [GoliathSlam(lvl=lvl)]


class Gorgelimb(Friendly):
    """Necrolords"""

    def __init__(self, lvl):
        if lvl == 16:
            health = 1040
            attack = 52
        else:
            # TODO
            raise NotImplemented()

        super(Gorgelimb, self).__init__(health=health, attack=attack)

        self.abilities = [FleshEruption(lvl=lvl)]


class Emeni(Friendly):
    """Necrolords"""

    def __init__(self, lvl):
        self.role = MELEE
        if lvl == 8:
            health = 540
            attack = 108
        else:
            # TODO
            raise NotImplemented()

        super(Emeni, self).__init__(health=health, attack=attack)

        # self.abilities = [SulfuricEmission(lvl=lvl),
        #                   GnashingChompers(lvl=lvl)]


class SecutorMevix(Friendly):
    """Necrolords"""

    def __init__(self, lvl):
        if lvl == 13:
            health = 805
            attack = 92

        else:
            # TODO
            raise NotImplemented()

        super(SecutorMevix, self).__init__(health=health, attack=attack)

#         self.abilities = [SecutorsJudgement(lvl=lvl),
#                           ]


class PlagueDeviserMarileth(Friendly):
    """Necrolords"""

    def __init__(self, lvl):
        if lvl == 20:  # TODO
            health = 1  # TODO
            attack = 180
        else:
            # TODO
            raise NotImplemented()

        super(PlagueDeviserMarileth, self).__init__(health=health, attack=attack)

#         self.abilities = [VolatileSolvent(lvl=lvl),
#                           OozeFrictionlessCoating(lvl=lvl)]


class MaldraxxusPlaguesinger(Friendly):
    """Necrolords normal unit"""

    def __init__(self, lvl):
        self.role = RANGED
        # TODO lvl
        if lvl == 14:
            health = 240
            attack = 222
        else:
            raise NotImplementedError()

        super(MaldraxxusPlaguesinger, self).__init__(health=health, attack=attack)

#         self.abilities = [PlagueSong(lvl=lvl)]
