from adventures_sl.teams import FriendlyTeam, EnemyTeam
from adventures_sl.units import Unit


class Battle:

    game_over:str = None

    def __init__(self,
                 friendly_team: FriendlyTeam,
                 enemy_team: EnemyTeam
                 ):
        assert isinstance(friendly_team, FriendlyTeam)
        assert isinstance(enemy_team, EnemyTeam)

        self.friendly_team = friendly_team
        self.enemy_team = enemy_team

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

        while True:  # Fight until fight is over

            # Friendlies go first
            self.friendly_team.fight(self)

            self.enemy_team.fight(self)

            if not any(self.friendly_team.get_units_ordered()):
                return 'Lost'

            if not any(self.enemy_team.get_units_ordered()):
                return 'Won'

    def nearest_melee(self, unit:Unit):

        friendly_ordered = self.friendly_team.get_units_ordered()
        enemy_ordered = self.enemy_team.get_units_ordered()

        if unit in friendly_ordered:

            i = friendly_ordered.index(unit)

            if i == 0:
                #
                order = [0, 1, 4, 5, 2, 6, 3, 7]  # TODO confirm if correct!
            else:
                raise

            for j in order:
                unit_j = enemy_ordered[j]
                if unit_j:
                    return unit_j

        elif unit in enemy_ordered:

            i = enemy_ordered.index(unit)

            if i == 0:

                order = [0, 1, 2, 3, 4] # TODO confirm if correct!
            else:
                raise

            for j in order:
                unit_j = friendly_ordered[j]
                if unit_j:
                    return unit_j

        else:
            raise KeyError('unit not found on board')
