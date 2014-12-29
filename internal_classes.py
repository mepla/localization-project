__author__ = 'Soheil'


class Factor:
    name = ""
    description = ""
    weight = 0

    def __init__(self, name, weight, desc="factor"):
        self.name = name
        self.description = desc
        self.weight = weight


class Place:
    name = ""
    description = ""
    x = 0.0
    y = 0.0

    def __init__(self, name, desc="place"):
        self.name = name
        self.description = desc