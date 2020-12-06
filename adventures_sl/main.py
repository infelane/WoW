from adventures_sl.battles import Battle
from adventures_sl.teams import EnemyTeam, FriendlyTeam
from adventures_sl.units import Friendly, ExampleEnemy, ExampleFriendly


def main():
    plague_deviser_marileth = Friendly()

    enemy_team = EnemyTeam()
    friendly_team = FriendlyTeam(f0=plague_deviser_marileth)

    battle = Battle(friendly_team,
                    enemy_team)

    outcome = battle.start()
    print('outcome:', outcome)

    return


if __name__ == '__main__':
    main()
