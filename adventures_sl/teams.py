from adventures_sl.units import Enemy, Friendly, Unit
import abc
from typing import List


class Team:
    """
    Abstract class for teams
    """

    def __init__(self, units_ordered: List[Unit]):
        self.units_ordered = units_ordered

    def get_units_ordered(self):
        return self.units_ordered

    def fight(self, battle):

        logs = []
        for unit in self.get_units_ordered():
            if unit:
                log = unit.fight(battle)
                logs.append(log)

        return logs


class EnemyTeam(Team):
    def __init__(self,
                 f0: Enemy = None,  # Front roz
                 f1: Enemy = None,
                 f2: Enemy = None,
                 f3: Enemy = None,
                 b0: Enemy = None,  # back row
                 b1: Enemy = None,
                 b2: Enemy = None,
                 b3: Enemy = None,
                 ):
        """ The enemy team

        b0 b1 b2 b3
        f0 f1 f2 f3

        """

        def test_input(e):
            if e is not None:
                assert isinstance(e, Enemy)

        test_input(f0)
        test_input(f1)
        test_input(f2)
        test_input(f3)
        test_input(b0)
        test_input(b1)
        test_input(b2)
        test_input(b3)

        # TODO not so sure this is the right order!
        units_ordered = [f0, f1, f2, f3, b0, b1, b2, b3]
        super(EnemyTeam, self).__init__(units_ordered)


class FriendlyTeam(Team):
    def __init__(self,
                 f0: Friendly = None,  # Front row
                 f1: Friendly = None,
                 f2: Friendly = None,
                 b0: Friendly = None,  # back row
                 b1: Friendly = None,
                 ):
        """ The friendly team

        f0 f1 f2
         b0 b1

        """

        def test_input(f):
            if f is not None:
                assert isinstance(f, Friendly)

        test_input(f0)
        test_input(f1)
        test_input(f2)
        test_input(b0)
        test_input(b1)

        # TODO not so sure this is the right order!
        units_ordered = [f0, f1, f2, b0, b1]
        super(FriendlyTeam, self).__init__(units_ordered)
