import json

class Vessel:
    def __init__(self, name="", imo="", master="", owner="", operator="") -> None:
        self.name = name
        self.imo = imo
        self.master = Person(master)
        self.owner = Owner(owner)
        self.operator = Operator(operator)
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)

class Company:
    def __init__(self, name="") -> None:
        self.name = name

class Owner(Company):
    def __init__(self, name="") -> None:
        super().__init__(name)

class Operator(Company):
    def __init__(self, name="") -> None:
        super().__init__(name)

        self.address = ""
        self.zip = ""
        self.city = ""
        self.phone = ""
        self.www = ""
        self.vat = ""
        self.icon = ""
        self.logo = ""

class Person:
    def __init__(self, name="") -> None:
        self.name = name
