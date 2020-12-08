import abc


class Log(list):
    def __init__(self, caster, ability, target, value):
        super(Log, self).__init__([caster, ability, target, value])


class Ability:
    def __init__(self, cd=0):
        self.cd = cd

        self.cd_state = 0

    @abc.abstractmethod
    def do(self) -> Log:
        pass


class Melee(Ability):

    # Ability is FROM A TO B. B depends on A and type of attack!
    def __init__(self,
                 unit,
                 damage):
        super(Melee, self).__init__()

        self.unit = unit
        self.damage = damage
        self.cd = 0
        self.cd_state = 0

    def do(self, battle):
        # Who to target(can be multiple, do one by one)

        if self.cd_state > 0:  # Can't cast ability
            self.cd_state -= 1

            return

        self.cd_state = self.cd

        target = battle.nearest_melee(self.unit)

        # What to do with it

        value = self.damage

        print(f'{self.unit} - {self} - {target} - {value}')
        target.reduce_hp(value)

        return Log(self.unit, self, target, value)

    def get_damage(self):
        return self.damage

    def __str__(self):
        return "melee"


class GoliathSlam(Ability):
    """
    Slams A nearby enemy, dealing x shadow damage to them and an enemy behind them.
    TODO according to vid, hitting behind is not working
    """

    def __init__(self, lvl):
        if lvl == 14:
            attack = 108
        else:
            raise NotImplemented()

        self.attack = attack

        super(GoliathSlam, self).__init__(cd=1)


class FleshEruption(Ability):
    """
    TODO
    """

    def __init__(self, lvl):
        if lvl == 16:
            attack = 108
        else:
            raise NotImplemented()

        self.attack = attack
        super(FleshEruption, self).__init__(cd=2)
