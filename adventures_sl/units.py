from adventures_sl.abilities import Melee

class Unit:
    health: int = 0
    attack:int=0

    def __init__(self,
                 health:int=0,
                 attack:int=0
                 ):

        self.attack = attack
        self.health = health

    def set_callback_dead(self, f):
        self.callback_dead = f

    def reduce_hp(self, value:int):
        assert isinstance(value, int)
        assert value >= 0
        self.health = max(0, self.health-value)

        if self.health <= 0:
            print(f'{self} - dead')
            self.callback_dead()
        # TODO check dead state

    def get_attack(self):
        return self.attack

    def fight(self, battle):

        move = Melee(self, self.get_attack())
        move.do(battle)


class Enemy(Unit):
    def __init__(self,
                 lvl: int = 0,
                 health: int = 0,
                 attack: int = 0):
        self.health=health
        self.attack=attack
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
    def __init__(self):
        super(ExampleEnemy, self).__init__(health=250, attack=10)

    def __str__(self):
        return "Example enemy"

class ExampleFriendly(Friendly):
    def __init__(self):
        super(ExampleFriendly, self).__init__(health=180, attack=20)
    def __str__(self):
        return "Example friendly"
