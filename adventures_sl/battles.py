from adventures_sl.teams import FriendlyTeam, EnemyTeam
from adventures_sl.units import Unit
from typing import List
WON = 'Won'
LOST = 'Lost'


class Battle:
    game_over: str = None

    def __init__(self,
                 friendly_team: FriendlyTeam,
                 enemy_team: EnemyTeam
                 ):
        assert isinstance(friendly_team, FriendlyTeam)
        assert isinstance(enemy_team, EnemyTeam)

        self.friendly_team = friendly_team
        self.enemy_team = enemy_team
        self.logs = []

        def foo(unit):
            i = self.friendly_team.get_units_ordered().index(unit)
            self.friendly_team.get_units_ordered()[i] = None

        def foo_enemy(unit):
            i = self.enemy_team.get_units_ordered().index(unit)
            self.enemy_team.get_units_ordered()[i] = None

        for unit in self.friendly_team.get_units_ordered():
            if unit is not None:
                unit.set_callback_dead(lambda a=unit: foo(a))

        for unit in self.enemy_team.get_units_ordered():
            if unit is not None:
                unit.set_callback_dead(lambda a=unit: foo_enemy(a))

    def get_logs(self):
        return self.logs

    def start(self) -> bool:
        """
        TODO
        Go over all the units
        Let them do their auto attack
        If their ability(/ies) is of cooldown, use it.
        After each unit, check if win condition?

        :return:
            Boolean if friendly team won or not
        """

        i = 0

        while True:  # Fight until fight is over

            print(f'Round {i + 1}')

            # Friendlies go first
            logs_f = self.friendly_team.fight(self)
            self.logs.extend(logs_f)

            logs_e = self.enemy_team.fight(self)
            self.logs.extend(logs_e)

            if not any(self.friendly_team.get_units_ordered()):
                return LOST

            if not any(self.enemy_team.get_units_ordered()):
                return WON

            i += 1
            print(f'--')

    def nearest_melee(self, unit: Unit):

        friendly_ordered = self.friendly_team.get_units_ordered()
        enemy_ordered = self.enemy_team.get_units_ordered()

        if unit in friendly_ordered:

            i = friendly_ordered.index(unit)

            d_order = {0: [0, 1, 4, 5, 2, 6, 3, 7],  # TODO confirm if correct!
                       1: [0, 1, 2, 3, 4, 5, 6, 7],  # TODO
                       2: [0, 1, 2, 3, 4, 5, 6, 7],  # TODO
                       3: [0, 1, 2, 3, 4, 5, 6, 7],  # TODO
                       4: [0, 1, 2, 3, 4, 5, 6, 7],  # TODO
                       }

            order = d_order.get(i)

            for j in order:
                unit_j = enemy_ordered[j]
                if unit_j:
                    return unit_j

        elif unit in enemy_ordered:

            i = enemy_ordered.index(unit)

            l_order = {0: [0, 1, 2, 3, 4],  # TODO confirm if correct!
                       2: [1, 2, 0, None, None],  # TODO confirm if correct!
                       }

            order = l_order.get(i, [None, None, None, None, None])  # TODO basically raises an error

            for j in order:
                unit_j = friendly_ordered[j]
                if unit_j:
                    return unit_j

        else:
            raise KeyError('unit not found on board')

    def all_enemies_ranged(self, unit: Unit):

        friendly_ordered = self.friendly_team.get_units_ordered()
        enemy_ordered = self.enemy_team.get_units_ordered()

        if unit in friendly_ordered:

            l = [a for a in enemy_ordered[4:] if a is not None]
            if len(l) >= 1:
                return l
            else:
                return [a for a in enemy_ordered[:4] if a is not None]

        elif unit in enemy_ordered:

            raise NotImplementedError()

        else:
            raise KeyError('unit not found on board')

    def nearest_enemy(self, unit: Unit):

        return self.nearest_melee(unit)

    def all_enemies_melee(self, unit: Unit):

        friendly_ordered = self.friendly_team.get_units_ordered()
        enemy_ordered = self.enemy_team.get_units_ordered()

        if unit in friendly_ordered:

            return [a for a in enemy_ordered[:4] if a is not None]
        elif unit in enemy_ordered:

            return [a for a in friendly_ordered[:3] if a is not None]

        else:
            raise KeyError('unit not found on board')

    def all_enemies_cone(self, unit:Unit):


        friendly_ordered = self.friendly_team.get_units_ordered()
        enemy_ordered = self.enemy_team.get_units_ordered()

        if unit in friendly_ordered:

            i = friendly_ordered.index(unit)

            d_options = {0: [1, 4, 5, 6],  # TODO confirm if correct!
                       1: [2, 5, 6, 7],  # TODO
                       2: [2, 5, 6, 7],  # TODO
                       3: [1, 4, 5, 6],  # TODO
                       4: [2, 5, 6, 7],  # TODO
                       }

            options = d_options.get(i)

            return [enemy_ordered[a] for a in options if enemy_ordered[a] is not None]

        elif unit in enemy_ordered:

            raise NotImplementedError()

        else:
            raise KeyError('unit not found on board')

    def all_allies(self, unit) -> List[Unit]:

        friendly_ordered = self.friendly_team.get_units_ordered()
        enemy_ordered = self.enemy_team.get_units_ordered()

        if unit in friendly_ordered:

            return [a for a in friendly_ordered if a is not None]

        elif unit in enemy_ordered:

            raise NotImplementedError()

        else:
            raise KeyError('unit not found on board')

    def all_adjecent_allies(self, unit) -> List[Unit]:

        friendly_ordered = self.friendly_team.get_units_ordered()
        enemy_ordered = self.enemy_team.get_units_ordered()

        if unit in friendly_ordered:

            i = friendly_ordered.index(unit)

            d_options = {
                       1: [0, 2, 3, 4],  # TODO order
                       2: [4, 1],
                       }

            options = d_options.get(i)

            return [friendly_ordered[a] for a in options if friendly_ordered[a] is not None]

        elif unit in enemy_ordered:

            raise NotImplementedError()

        else:
            raise KeyError('unit not found on board')