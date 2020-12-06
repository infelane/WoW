import unittest

from adventures_sl.teams import EnemyTeam, FriendlyTeam
from adventures_sl.units import Friendly, ExampleEnemy, ExampleFriendly
from adventures_sl.battles import Battle

class TestBattle(unittest.TestCase):
    def test_fight(self):
        enemy_team = EnemyTeam(f0=ExampleEnemy())
        friendly_team = FriendlyTeam(f0=ExampleFriendly())

        battle = Battle(friendly_team,
                        enemy_team)

        outcome = battle.start()
        print('outcome:', outcome)

        # TODO assertion
        self.assertTrue(outcome)
        self.assertFalse(outcome)

if __name__ == '__main__':
    unittest.main()