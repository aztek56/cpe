import random

# Objeto que representa objetos a encontrarse en el mapa
class Elements(object):
    def __init__(self, type):
        self.type = type
        self.value = 0
        self.strength = 0
        self.magic = 0
        self.health = 0
        self.speed = 0
        self.protection = 0
        self.death = 0
        self.description = 'element'
        self.detail = 'detail'
        self.__init_element__(self.type)

    # Dependiendo del tipo de objeto tendra valores en campos distintos
    def __init_element__(self, type):
        if type == 1:  # oro
            self.description = "una pieza de oro"
            self.value += 1
        elif type == 2:  # comida
            self.description = "una bolsa de comida"
            self.health += 1
            self.strength += 1
        elif type == 3:  # escudo
            self.description = "2 placas de armadura"
            self.protection += 2
        elif type == 4:  # medicina
            self.description = "2 frascos de medicina"
            self.health += 2
        elif type == 5:  # armas
            self.description = "armas"
            self.strength += 3
            self.protection += 1
            self.magic += 1
        elif type == 6:  # pocion velocidad
            self.description = "una pocion de velocidad"
            self.speed += 3
        elif type == 7:  # pocion proteccion
            self.description = "una pocion de proteccion"
            self.protection += 3
        elif type == 8:  # pocion magia
            self.description = "una pocion magica"
            self.magic += 5
        elif type == 9:  # pocion fuerza
            self.description = "una pocion de fuerza"
            self.strength += 5
        elif type == 10:  # pocion muerte
            self.description = "una frasco con veneno"
            self.death += 2
        elif type == 11:     # bote
            self.description = "un bote"
        elif type == 12:    # aleta magica
            self.description = "la aleta magica"
        elif type == 13:    # equipo de montana
            self.description = "equipo de montana"
        elif type == 14:    # espada poderosa
            self.description = "la espada poderosa"
        elif type == 15:  # pocion de salud
            self.description = "una pocion de salud"
            self.health += 5

    def set_proteccion(self, protection):
        self.protection = protection

    def set_salud(self, health):
        self.health = health

    def set_fuerza(self, strength):
        self.strength = strength

    def set_valor(self, value):
        self.value = value
        if self.type == 1:
            self.description = str(value) + " piezas de oro"

    def get_muerte(self):
        return self.death

    def get_proteccion(self):
        return self.protection

    def get_velocidad(self):
        return self.speed

    def get_salud(self):
        return self.health

    def get_magia(self):
        return self.magic

    def get_fuerza(self):
        return self.strength

    def get_valor(self):
        return self.value


# Metodo que genera un elemento aleatorio
def elementosRandom():
    val = random.randint(0, 11)
    if val == 1:  # Oro
        value = random.randint(0, 10)
        gold = Elements(1)
        gold.set_valor(value)
        return gold
    elif val == 2:  # Comida
        value = random.randint(0, 5)
        food = Elements(2)
        food.set_fuerza(value)
        return food
    elif val == 3:  # Escudo
        value = random.randint(0, 7)
        armor = Elements(3)
        armor.set_proteccion(value)
        return armor
    elif val == 4:  # Medicina
        value = random.randint(0, 10)
        medicine = Elements(4)
        medicine.set_salud(value)
        return medicine
    elif val == 5:  # Armas
        return Elements(5)
    elif val == 6:  # Pocion velocidad
        return Elements(6)
    elif val == 7:  # Pocion proteccion
        return Elements(7)
    elif val == 8:  # Pocion magia
        return Elements(8)
    elif val == 9:  # Pocion fuerza
        return Elements(9)
    elif val == 10:  # Pocion muerte
        return Elements(10)
    else:           # Pocion vida
        return Elements(15)
