
class Ability:
    pass


class Melee(Ability):
    # TODO define which targets to hit!

    # Ability is FROM A TO B. B depends on A and type of attack!
    def __init__(self,
                 unit,
                 attack):
        self.unit=unit
        self.damage = attack

    def do(self, battle):
        # Who to target(can be multiple, do one by one)

        target = battle.nearest_melee(self.unit)

        # What to do with it

        value = self.damage

        print(f'{self.unit} - {self} - {target} - {value}')
        target.reduce_hp(value)


    def get_damage(self):
        return self.damage

    def __str__(self):
        return "melee"
