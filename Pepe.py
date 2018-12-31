from nayel import Elements
from enum import Enum

# Este objeto es una Enumeracion
class CharacterTypes(Enum):
    PEPE = 1
    TROLL = 2
    DRAGON = 3
    E_KING = 4
    BAT = 5

# Declaramos nuestro objeto Pepe que representara los personajes de nuestra aventura
class Pepe(object):
    # Constructor
    def __init__(self, c_type):
        self.life = 0
        self.strength = 0
        self.speed = 0
        self.gold = 0
        self.armor = 0
        self.inventory = {}
        self.max_life = 0
        self.max_strength = 0
        self.max_speed = 0
        self.max_armor = 0
        if c_type == CharacterTypes.PEPE.value:  # Pepe
            self.type = CharacterTypes.PEPE
            self.life = 100
            self.strength = 20
            self.armor = 10
            self.gold = 10
            self.speed = 5
            self.max_life = 100
            self.max_strength = 20
            self.max_speed = 5
            self.max_armor = 10
        elif c_type == CharacterTypes.TROLL.value:  # Troll
            self.type = CharacterTypes.TROLL
            self.life = 50
            self.strength = 30
            self.gold = 30
            self.speed = 1
            self.armor = 20
        elif c_type == CharacterTypes.DRAGON.value:  # Dragon
            self.type = CharacterTypes.DRAGON
            self.life = 400
            self.strength = 70
            self.gold = 1000
            self.speed = 5
            self.armor = 100
        elif c_type == CharacterTypes.E_KING.value:  # Rey Maloso (Francisco)
            self.type = CharacterTypes.E_KING
            self.life = 800
            self.strength = 150
            self.gold = 5000
            self.speed = 20
            self.armor = 100
        elif c_type == CharacterTypes.BAT.value:
            self.type = CharacterTypes.BAT
            self.life = 10
            self.strength = 5
            self.speed = 10
            self.armor = 1
            self.gold = 5

    # Este metodo es parte de Python y nos permite definir como queremos imprimir
    # el objeto para mostrar su informacion
    def __repr__(self):
        description = "Character: "
        description += self.getName()
        description += "\nLife: " + str(self.life)
        description += "\tStrength: " + str(self.strength)
        description += "\tSpeed: " + str(self.speed)
        description += "\tArmor: " + str(self.armor)
        if self.type == CharacterTypes.PEPE:
            description += "\tGold: " + str(self.gold)
        return description

    # Metodo que nos regresara cual es el nombre de nuestro heroe
    def getName(self):
        if self.type == CharacterTypes.PEPE:  # Pepe
            return "Pepe"
        elif self.type == CharacterTypes.TROLL:  # Troll
            return "Troll"
        elif self.type == CharacterTypes.DRAGON:  # Dragon
            return "Dragon"
        elif self.type == CharacterTypes.E_KING:  # Rey Maloso (Francisco)
            return "King Francisco"
        elif self.type == CharacterTypes.BAT:
            return "Bat"
        return "Unknown"

    # Para usarse en una pantalla de inventario
    # No implementado!!
    def getItem(self, element):
        element.get_muerte()
        element.get_proteccion()
        element.get_velocidad()
        element.get_salud()
        element.get_magia()
        element.get_fuerza()
        element.get_valor()

    # Para usarse en una pantalla de inventario
    # No implementado!!
    def revisaInventario(self, key):
        if key in self.inventory.keys():
            return self.inventory[key]
        return 0

    # Metodo que agrega salud a nuestro personaje
    def sanar(self, valor):
        if self.life == self.max_life:
            self.max_life += valor
        self.life = self.max_life

    # Metodo que pone nuestra salud al maximo
    def maxSanar(self):
        self.life = self.max_life

    # Metodo que aumenta la fuerza de nuestro personaje
    def fortaleza(self, valor):
        if self.strength == self.max_strength:
            self.max_strength += valor
        self.strength = self.max_strength

    # Metodo que pone nuestra fuerza al maximo
    def maxFortaleza(self):
        self.strength = self.max_strength

    # Metodo que aumenta la velocidad de nuestro personaje
    def velocidad(self, valor):
        if self.speed == self.max_speed:
            self.max_speed += valor
        self.speed = self.max_speed

    # Metodo que pone la velocidad al maximo
    def maxVelocidad(self):
        self.speed = self.max_speed

    # Metodo que aumenta la fuerza de nuestra armadura
    def armadura(self, valor):
        if self.armor == self.max_armor:
            self.max_armor += valor
        self.armor = self.max_armor

    # Metodo que aumenta al maximo nuestra armadura
    def maxArmadura(self):
        self.armor = self.max_armor

    # Metodo que se activa con una pocion maxima y aumenta la fuerza,
    # la salud, la velocidad y la armadura
    def magic(self, valor):
        self.fortaleza(valor)
        self.sanar(valor)
        self.velocidad(valor)
        self.armadura(valor)

    # Metodo que consume energia en nuestro personaje
    def consumeEnergy(self):
        if self.strength > 0:
            self.strength -= 1
        elif self.life > 0:
            self.life -=1
        else:
            return False
        return True

    # Metodo que agrega un nuevo elemento a nuestro jugador
    # Este se encarga de distribuir los valores apropiados segun el objeto.
    def addItem(self, element):
        key = element.type
        if key == 1:  # oro
            self.gold = element.get_valor()
        elif key == 2:  # comida
            self.life += element.get_salud()
            self.strength += element.get_fuerza()
            if self.life > self.max_life:
                self.life = self.max_life
            if self.strength > self.max_strength:
                self.strength = self.max_strength
        elif key == 3:  # escudo
            self.armor += element.get_proteccion()
            if self.armor > self.max_armor:
                self.armor = self.max_armor
        elif key == 4:  # medicina
            self.life += element.get_salud()
            if self.life > self.max_life:
                self.life = self.max_life
        elif key == 5:  # armas
            self.strength = element.get_fuerza()
            self.armor = element.get_proteccion()
            self.magic(element.get_magia())
        elif key == 6:  # pocion velocidad
            self.velocidad(element.get_velocidad())
        elif key == 7:  # pocion proteccion
            self.armadura(element.get_proteccion())
        elif key == 8:  # pocion magia
            self.magic(element.get_magia())
        elif key == 9:  # pocion fuerza
            self.fortaleza(element.get_fuerza())
        elif key == 15:  # pocion de salud
            self.sanar(element.get_salud())
        elif key == 10:  # veneno
            self.life /= element.get_salud()
        elif key == 12:  # Aleta magica
            self.setMagicFin()
        elif key == 13:  # equipo de montana
            self.setMountainGear()
        elif key == 14:  # espada poderosa
            self.setMightySword()

    # Asignamos la aleta magica
    def setMagicFin(self):
        self.inventory["fin"] = 1

    # Preguntamos si tenemos la aleta magica
    def getMagicFin(self):
        return "fin" in self.inventory

    # Asignamos el equipo de montana
    def setMountainGear(self):
        self.inventory["mountain"] = 1

    # Preguntamos si tenemos el equipo de montana
    def getMountainGear(self):
        return "mountain" in self.inventory

    # Asignamos la espada poderosa
    def setMightySword(self):
        self.max_strength = 150
        self.max_life *= 2
        self.maxFortaleza()
        self.maxSanar()
        self.maxArmadura()
        self.inventory["mighty"] = 1

    # Preguntamos si tenemos la espada poderosa
    def getMightySword(self):
        return "mighty" in self.inventory

    # Asignamos al jugador sobre el bote o fuera de el
    def onBoat(self, ride):
        if ride == 1:
            self.inventory["boat"] = 1
        else:
            self.inventory.pop("boat", None)

    # Preguntamos si podemos movernos en el agua, ya sea con el bote o la aleta
    def canMoveOnWater(self):
        if "fin" in self.inventory or "boat" in self.inventory:
            return True
        return False

    # Preguntamos si podemos escalar la montana
    def canClimbMountain(self):
        if "mountain" in self.inventory:
            return True
        return False

    # Gastamos oto
    # Se usara en la tienda. Aun sin implementar!!
    def spendGold(self, valor):
        if self.gold < valor:
            return False
        self.gold -= valor
        return True

    # Agregamos oro a la cuenta del jugador
    def addGold(self, valor):
        self.gold += valor

    # Metodo que se ejecuta cuando se esta peleando con un enemigo
    def fight(self, enemy):
        attack_val = enemy.strength
        # si aun tenemos armadura y fuerza el factor de velocidad reducira
        # la fuerza del ataque
        if self.armor > 0 and self.strength > 0:
            # el factor de la velocidad reduce la fuerza del ataque
            speed_f = (enemy.speed - self.speed) / 100
            if speed_f != 0.0:
                attack_val *= speed_f
        if self.armor > 1:
            attack_val -= attack_val * (self.armor/100)
            self.armor -= round(self.armor * .1)    # reduce armor 10%
        else:
            self.armor = 0
        self.life -= abs(round(attack_val))
        if enemy.strength > 0:
            enemy.strength -= max(round(self.armor * .1), 1)
        return self.life <= 0


# Metodo que ejecuta la batalla
def battle(personaje, enemigo):
    print("Haz encontrado a un " + enemigo.getName() + ". Preparate para la batalla")
    print(personaje)
    print(enemigo)
    while True:
        print("Atacas a " + enemigo.getName())
        dead = enemigo.fight(personaje)
        # revisamos si el enemigo ha soportado nuestro ataque
        if not dead:
            print(enemigo.getName() + " ha resistido tu ataque y se prepara a atacar")
            dead = personaje.fight(enemigo)
            if dead:
                # Si nos vencio, se acaba el juego.
                print(enemigo.getName() + " te ha vencido!")
                return False
        else:
            # revisamos si hemos vencido al enemigo
            print("Haz vencido a " + enemigo.getName())
            personaje.addGold(enemigo.gold)
            print("Haz ganado " + str(enemigo.gold) + " piezas de oro")
            break
        print("Has resistido el ataque!")
        print(personaje)
        print(enemigo)
        if enemigo.type != CharacterTypes.DRAGON and enemigo.type != CharacterTypes.E_KING:
            # damos la opcion de huir
            contd = input("\nQuieres continuar luchando?\t(Y) - Si\t(N) - Huir\t :")
            contd = contd.upper()
            if contd == "N":
                break
    return True
