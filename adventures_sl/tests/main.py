import unittest

from adventures_sl.teams import EnemyTeam, FriendlyTeam
from adventures_sl.units import ExampleEnemy, ExampleFriendly, DarkGoliath, Gorgelimb, SecutorMevix, Emeni, \
    MaldraxxusPlaguesinger, PlagueDeviserMarileth
from adventures_sl.battles import Battle, WON, LOST


class TestBattle(unittest.TestCase):
    def test_fight(self):
        enemy_team = EnemyTeam(f0=ExampleEnemy(health=20, attack=20))
        friendly_team = FriendlyTeam(f0=ExampleFriendly())

        battle = Battle(friendly_team,
                        enemy_team)

        outcome = battle.start()
        self.assertEqual(WON, outcome, 'should win')

    def test_fight2(self):
        """Balanced, starter, friendly, should win"""
        health = 20
        attack = 10
        enemy_team = EnemyTeam(f0=ExampleEnemy(health=health, attack=attack))
        friendly_team = FriendlyTeam(f0=ExampleFriendly(health=health, attack=attack))

        battle = Battle(friendly_team,
                        enemy_team)

        outcome = battle.start()
        self.assertEqual(WON, outcome, 'should win')

    def test_fight_loss(self):
        """Barely lose"""
        health = 20
        attack = health
        enemy = ExampleEnemy(health=health, attack=attack)
        enemy_team = EnemyTeam(f0=enemy)
        friendly_team = FriendlyTeam(f0=ExampleFriendly(health=health, attack=attack - 1))

        battle = Battle(friendly_team,
                        enemy_team)

        outcome = battle.start()
        with self.subTest('outcome'):
            self.assertEqual(LOST, outcome, 'should win')
        with self.subTest('hp'):
            self.assertEqual(1, enemy.health)
        with self.subTest('logs'):
            logs = battle.get_logs()

            self.assertEqual(attack - 1, logs[0][-1], 'friendly attack')
            self.assertEqual(attack, logs[1][-1], 'enemy attack')

    def test_vid1(self):
        """
        based on video I recorded from fight

        :return:
        """

        enemy_team = EnemyTeam(f2=DarkGoliath(lvl=14))

        friendly_team = FriendlyTeam(f0=Gorgelimb(lvl=16),
                                     f1=SecutorMevix(lvl=13),
                                     f2=Emeni(lvl=8),
                                     b0=PlagueDeviserMarileth(lvl=20),
                                     b1=MaldraxxusPlaguesinger(lvl=14))

        battle = Battle(friendly_team,
                        enemy_team)

        outcome = battle.start()

        self.assertTrue(outcome)  # TODO


if __name__ == '__main__':
    unittest.main()
