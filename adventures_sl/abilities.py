import abc
from typing import List


class Log(list):
    def __init__(self, caster, ability, target, value, verbose=1):
        super(Log, self).__init__([caster, ability, target, value])

        if verbose:
            print(f'{caster} - {ability} - {target} - {value}')


class Ability(abc.ABC):
    def __init__(self,
                 unit,
                 cd=0):
        self.unit = unit
        self.cd = cd

        self.cd_state = 0

    @abc.abstractmethod
    def do(self, battle) -> Log:
        pass

    def cd_ready(self):
        """ Don't forget to check this if ability uses a CD """
        if self.cd_state > 0:  # Can't cast ability
            self.cd_state -= 1

            return False

        self.cd_state = self.cd

        return True

    def __str__(self):
        return self.__class__.__name__


class Melee(Ability):

    # Ability is FROM A TO B. B depends on A and type of attack!
    def __init__(self,
                 unit,
                 damage):
        super(Melee, self).__init__(unit)

        self.damage = damage
        self.cd = 0
        self.cd_state = 0

    def do(self, battle):
        # Who to target(can be multiple, do one by one)

        if not self.cd_ready():
            return

        target = battle.nearest_melee(self.unit)
        if target is None:
            return

        # What to do with it

        value = self.damage

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

    def __init__(self, unit, lvl):
        if lvl == 14:
            attack = 108
        else:
            raise NotImplemented()

        self.attack = attack

        super(GoliathSlam, self).__init__(unit, cd=1)

    def do(self, battle) -> List[Log]:

        if not self.cd_ready():
            return

        nearby_enemy = battle.nearest_melee(self.unit)

        value = self.attack

        l_logs = []

        nearby_enemy.reduce_hp(value)
        l_logs.append(Log(self.unit, self, nearby_enemy, self.attack))

        return l_logs


class FleshEruption(Ability):
    """
    Sacrefices own flesh, dealing x damage to enemies in melee and y to himself
    """

    def __init__(self,
                 unit,
                 lvl):
        if lvl == 16:
            attack = 156
            self_damage = 26
        else:
            raise NotImplemented()

        self.attack = attack
        super(FleshEruption, self).__init__(unit, cd=2)

        self.self_damage = self_damage

    def do(self, battle) -> Log:
        # Hit all melees and self

        if not self.cd_ready():
            return

        enemies_melee = battle.all_enemies_melee(self.unit)

        value = self.attack

        l_logs = []
        for target_melee in enemies_melee:
            target_melee.reduce_hp(value)
            l_logs.append(Log(self.unit, self, target_melee, self.attack))

        self.unit.reduce_hp(self.self_damage)
        l_logs.append(Log(self.unit, self, self.unit, self.self_damage))

        return l_logs


class SecutorsJudgement(Ability):
    """
    Judges his opponents wanting, dealing x shadowfrost damage to all enemies in a cone in front of him
    """

    def __init__(self,
                 unit,
                 lvl):
        if lvl == 13:
            attack = 110

        else:
            raise NotImplemented()

        self.attack = attack
        super(SecutorsJudgement, self).__init__(unit, cd=4)

    def do(self, battle) -> List[Log]:
        # Hit in conce

        if not self.cd_ready():
            return

        enemies = battle.all_enemies_cone(self.unit)

        value = self.attack

        l_logs = []
        for target in enemies:
            target.reduce_hp(value)
            l_logs.append(Log(self.unit, self, target, self.attack))

        return l_logs


class SulfuricEmission(Ability):
    """
    Emeni's fumes deal x damage to all enemies in melee range
    """

    def __init__(self,
                 unit,
                 lvl):
        if lvl == 8:
            attack = 108

        else:
            raise NotImplemented()

        self.attack = attack
        super(SulfuricEmission, self).__init__(unit, cd=3)

    def do(self, battle) -> List[Log]:
        # Melee

        if not self.cd_ready():
            return

        enemies = battle.all_enemies_melee(self.unit)

        value = self.attack

        l_logs = []
        for target in enemies:
            target.reduce_hp(value)
            l_logs.append(Log(self.unit, self, target, self.attack))

        return l_logs


class GnashingChompers(Ability):
    """
    inspires adjacent allies, increasing their damage by 32
    """

    def __init__(self,
                 unit,
                 lvl):
        if lvl == 8:

            attack_bonus = 32

        else:
            raise NotImplemented()

        self.attack_bonus = attack_bonus
        super(GnashingChompers, self).__init__(unit, cd=5)

    def do(self, battle) -> List[Log]:
        # Buff adjacent

        if not self.cd_ready():
            return

        friendlies = battle.all_adjecent_allies(self.unit)

        value = self.attack_bonus

        l_logs = []
        for target in friendlies:
            target.buff_attack(value)
            l_logs.append(Log(self.unit, self, target, value))

        return l_logs


class VolatileSolvent(Ability):
    """
    douses nearest enemy, dealing x damage and y more when target is struck, for 3 rounds
    """

    def __init__(self,
                 unit,
                 lvl):
        if lvl == 20:

            damage = 72
            dot = 54

        else:
            raise NotImplemented()

        self.damage = damage
        self.dot = dot
        super(VolatileSolvent, self).__init__(unit, cd=5)

    def do(self, battle) -> List[Log]:

        if not self.cd_ready():
            return

        enemy = battle.nearest_enemy(self.unit)

        value = self.damage

        l_logs = []

        enemy.reduce_hp(value)
        l_logs.append(Log(self.unit, self, enemy, value))

        # TODO implement the dot: probably as "buff/debuff" to apply to the enemy

        return l_logs


class OozeFrictionlessCoating(Ability):
    """
    Heals a nearby ally for x and increases their max hp by 10%
    """

    def __init__(self,
                 unit,
                 lvl):
        if lvl == 20:

            heal = 72

        else:
            raise NotImplemented()

        self.heal = heal
        super(OozeFrictionlessCoating, self).__init__(unit, cd=3)

    def do(self, battle) -> List[Log]:
        # Heal nearby

        if not self.cd_ready():
            return

        friendlies = battle.all_allies(self.unit)

        friendly = friendlies[0]

        l_logs = []

        friendly.increase_hp(self.heal)
        l_logs.append(Log(self.unit, self, friendly, self.heal))
        friendly.max_health = int(1.1 * friendly.max_health)
        l_logs.append(Log(self.unit, self, friendly, "buff"))

        return l_logs



class PlagueSong(Ability):
    """
    Scream at enemies at range, inflicting x damage each round for 4.
    """

    def __init__(self,
                 unit,
                 lvl):
        if lvl == 14:

            damage = 50

        else:
            raise NotImplemented()

        self.damage = damage
        super(PlagueSong, self).__init__(unit, cd=5)

    def do(self, battle) -> List[Log]:
        # ranged

        if not self.cd_ready():
            return

        enemies = battle.all_enemies_ranged(self.unit)

        l_logs = []

        for target in enemies:
            target.reduce_hp(self.damage)
            l_logs.append(Log(self.unit, self, target, self.damage))

        return l_logs
