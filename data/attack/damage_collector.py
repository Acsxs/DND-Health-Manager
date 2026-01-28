from ..global_const import *


def damage_type_convert(damage_type, magical):
    return f"{damage_type}-{int(magical)}"


def damage_type_deconvert(string):
    damage_type, magical = string.split('-')
    return damage_type, bool(int(magical))


class DamageCollector(dict):
    def __init__(self, damage_dictionary=None, *args):
        super().__init__()
        self.update(damage_dictionary if damage_dictionary is not None else {})
        if args:
            for i in args:
                self.add(i)

    def add(self, *args):
        if not args:
            return
        if isinstance(args[0], list):
            args = args[0]
        damage_type, damage, magical = args
        key = damage_type_convert(damage_type, magical if damage_type in NON_MAGICAL else True)
        self[key] = self[key] + damage if key in self.keys() else damage

    def extend(self, collector):
        for k, v in collector.items():
            self[k] = self[k] + v if k in self.keys() else v
        return self

    def __add__(self, other):
        return DamageCollector(damage_dictionary=self.extend(other))

    def __truediv__(self, other):
        for damage_type, damage in self.items():
            self[damage_type] = damage / other
        return self

    def __mul__(self, other):
        for damage_type, damage in self.items():
            self[damage_type] = damage * other
        return self
