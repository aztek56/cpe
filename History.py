from Mapa import Direction, GameMap, startMap
from Pepe import Pepe, battle
from nayel import Elements, elementosRandom
import random

# Objeto principal, controla el flujo de todo el juego
class Engine(object):
    # Constructor de nuestro engine
    def __init__(self):
        self._hero = Pepe(1)
        self._movement = Movement(self._hero)

    # Iniciamos un nuevo juego
    def newGame(self):
        print("Bienvenidos a ~RPGame~")
        # El ciclo eterno solo terminara cuando el usuario decia terminar o muera en el juego
        while True:
            retVal = self._movement.move()
            if retVal == -1:
                break
        print("Juego terminado")


# El objeto movement es el que se encarga de controlar todos los elementos del juego.
# Este objeto tiene control del personaje y del mapa, asi como de la narracion de la historia.
class Movement(object):
    # Constructor
    def __init__(self, hero):
        self._hero = hero
        self.posActual_x = 1
        self.posActual_y = 1
        self.my_map = startMap()
        self.my_map.visitMap(self.posActual_x, self.posActual_y)
        # print(self.my_map.getVicinity(self.posActual_x,self.posActual_y))
        # self.my_map.printMap()

    # Metodo que se encarga de solicitar al usuario y ejecutar los pasos para mover al personaje en el mapa.
    def move(self):
        print(self.narrar())
        while True:
            mov = input("\n--PARA MOVERTE USA ESTAS TECLAS:\n"
                        ".(W) _ Hacia el norte  "
                        ".(S) _ Hacia el sur  "
                        ".(D) _ Hacia el este  "
                        ".(A) _ Hacia el oeste  "
                        ".(X) _ Mostrar mapa  "
                        ".(M) _ Terminar juego\n :")
            mov = mov.upper()
            if mov == "W":
                # En cada option verificamos si no hemos llegado a la orilla del mapa
                if self.my_map.canMove(Direction.NORTH, self.posActual_x, self.posActual_y):
                    # Pero tambien tenemos ciertas restricciones en el tablero, sobretodo en los terrenos
                    # en los que necesitamos equipo especial.
                    if self.validLocation(self.my_map.validMove(self.posActual_x-1, self.posActual_y)):
                        self.posActual_x -= 1
                    else:
                        print("No tienes el equipo para avanzar por ese terreno\n")
                    break
                else:
                    print("Has llegado al limite del mapa\n")
            elif mov == "S":
                if self.my_map.canMove(Direction.SOUTH, self.posActual_x, self.posActual_y):
                    if self.validLocation(self.my_map.validMove(self.posActual_x+1, self.posActual_y)):
                        self.posActual_x += 1
                    else:
                        print("No tienes el equipo para avanzar por ese terreno\n")
                    break
                else:
                    print("Has llegado al limite del mapa\n")
            elif mov == "D":
                if self.my_map.canMove(Direction.EAST, self.posActual_x, self.posActual_y):
                    if self.validLocation(self.my_map.validMove(self.posActual_x, self.posActual_y+1)):
                        self.posActual_y += 1
                    else:
                        print("No tienes el equipo para avanzar por ese terreno\n")
                    break
                else:
                    print("Has llegado al limite del mapa\n")
            elif mov == "A":
                if self.my_map.canMove(Direction.WEST, self.posActual_x, self.posActual_y):
                    if self.validLocation(self.my_map.validMove(self.posActual_x, self.posActual_y-1)):
                        self.posActual_y -= 1
                    else:
                        print("No tienes el equipo para avanzar por ese terreno\n")
                    break
                else:
                    print("Has llegado al limite del mapa\n")
            elif mov == "M":
                return -1
            elif mov == "X":
                self.my_map.printMap(self.posActual_x, self.posActual_y)
        # Una vez que comprobamos que el movimiento es valido, lo ejecutamos y actualizamos el mapa
        self.my_map.visitMap(self.posActual_x, self.posActual_y)
        # En algunas posiciones del mapa tendremos que ejecutar ciertas acciones
        contd = self.processLocation()
        # Si esas acciones terminan en nuestra muerte, el juego termina
        if not contd:
            return -1
        # self.my_map.printMap(self.posActual_x, self.posActual_y)

    # Metodo que se encarga de ejecutar las acciones pertinentes segun cada cuadro del tablero
    def processLocation(self):
        key = self.my_map.validMove(self.posActual_x, self.posActual_y)
        if key == 'TR':     # batalla con troll
            return battle(self._hero, Pepe(2))
        elif key == 'FR':   # encuentro con hada
            print("Has encontrado una hada!\nSu magia te ayuda a recuperarte al maximo.")
            self._hero.maxSanar()
            self._hero.maxFortaleza()
            self._hero.maxVelocidad()
            self._hero.maxArmadura()
        elif key == 'ST':   # Entrada a tienda
            # Aun hay que trabajar en la tienda
            print("Estamos de vacaciones volvemos pronto!")
        elif key == 'SW':   # Terreno pantanoso
            print("El pantano es un lugar dificil de cruzar y toma parte de tu fuerza y energia. No podemos "
                  "permanecer mucho tiempo aqui!")
            self._hero.consumeEnergy()
        elif key == 'CH':   # Encontramos un baul
            print("Has encontrado un baul. Al abrirlo encuentras varios objetos.\n")
            for i in range(6):      # cada baul nos dara 6 objetos.
                item = elementosRandom()
                print("Has encontrado " + item.description)
                self._hero.addItem(item)
            self.my_map.consumeChest(self.posActual_x, self.posActual_y)
        elif key == 'CS':   # Llegamos al castillo y ejecutamos la batall final
            print("Has llegado al castillo. La batalla final se acerca preparate!")
            contd = input("Estas listo para la batalla?\t(Y) - Si\t(N) - Huir\t :")
            contd = contd.upper()
            if contd == "Y":
                # Batalla contra el rey malvado
                result = battle(self._hero, Pepe(4))
                if result:
                    print("Felicidades! Has logrado vencer al rey malvado! Ahora un aire de paz domina el reino. "
                          "De aqui en adelante las generaciones por venir cantaran canciones vitoreando tu nombre "
                          "y celebrando tus exitos. El futuro es un lugar brillante gracias a ti!")
                else:
                    print("El rey malvado ahora rie sobre tus restos. Tu osadia ha causado su ira y su reino de "
                          "terror se ha vuelto mas cruel. Tu nombre sera olvidado y nadie recordara tus acciones "
                          "con el tiempo habra otros que inicien una cruzada como la tuya, mas sus logros no los "
                          "podras atestiguar.")
                return False
        elif key == 'LR':   # Llegamos a la guarida del dragon y peleamos contra el.
            print("Has llegado a la guarida del dragon. La batalla se acerca preparate!")
            contd = input("Estas listo para la batalla?\t(Y) - Si\t(N) - Huir\t :")
            contd = contd.upper()
            if contd == "Y":
                # batalla contra el dragon
                result = battle(self._hero, Pepe(3))
                if result:
                    print("Felicidades! Has logrado vencer al dragon! Una luz de esperanza ilumina ahora el reino. "
                          "Con la espada magica que has liberado ahora tienes la posibilidad de enfrentar al rey "
                          "malvado. Sigamos, la liberacion del reino aguarda!")
                    self.my_map.consumeLair(self.posActual_x, self.posActual_y)
                    self._hero.addItem(Elements(14))
                else:
                    print("El dragon tiene un festin con tus restos. Tu nombre sera olvidado y nadie recordara tus "
                          "acciones con el tiempo habra otros que inicien una cruzada como la tuya,\nmas sus logros "
                          "no los podras atestiguar. El reino esta de luto ya que su esperanza ha sido defraudada.")
                return False
        elif key == 'LD':   # Guarida si la visitas despues de la batalla
            print("La guarida ahora esta vacia, mas los recuerdos de la batalla monumental aun permanecen en tu "
                  "memoria. Esto te ayudara a vencer al rey malvado.")
        elif key == 'WH':   # Remolino en el lago
            print("Has caido en un remolino.")
            if self._hero.getMagicFin():
                self._hero.addGold(-self._hero.gold)
                print("Has sobrevivido milagrosamente gracias a la ayuda de la aleta magica. "
                      "Mas para poder escapar has tenido que deshacerte de todo tu oro! Al menos aun vives para "
                      "contarlo.\n")
            else:
                print("El bote no lo ha podido soportar y por el peso de tu equipo no has logrado escapar. "
                      "Mejor suerte para la proxima")
                return False
        else:   # Otras posiciones donde hay actividad
            # Si es bosque o planicie hay probabilidad de tener que pelear con un murcielago
            if key == 'F' or key == 'PL':
                enemy = self.fightEnemy(key)
                if enemy is not None:
                    contd = battle(self._hero, enemy)
                    if not contd:
                        return False
            # en cualquier otra opcion podemos encontrar objetos
            item = self.getLocationElement(key)
            if item is not None:
                if key == 'MR' or key == 'ME':
                    print("Has encontrado a una sirena.")
                    if self._hero.getMagicFin():
                        print("A ella le da gusto volverte a ver. "
                              "'Espero la aleta magica te este ayudando en tu aventura'")
                    else:
                        print("'Al encontrarme has demostrado ser un caballero digno y valiente. Yo no puedo "
                              "salir de mi reino, mas te entrego esta aleta magica que te permitira\nentrar "
                              "y salir de mis dominios como si estuvieras en la tierra. Usala sabiamente y que "
                              "pronto logres tu objetivo de liberar a tu reino'\nLa sirena te ha dado un artefacto "
                              "que te permitira pasar por los cuerpos de agua sin necesidad de usar un bote.\n")
                        self._hero.addItem(item)
                else:
                    print("Has encontrado " + item.description)
                    self._hero.addItem(item)
                    if key == 'G':
                        self.my_map.consumeGold(self.posActual_x, self.posActual_y)
                    elif key == 'MG' or key == 'MS':
                        self.my_map.consumeItem(self.posActual_x, self.posActual_y)
        return True

    def getLocationElement(self, key):
        if key == 'F' or key == 'PL' or key == 'G' or key == 'MR' or key == 'MG' or key == 'MS' or key == 'M':
            return self.mapElement(key)
        return None

    def validLocation(self, key):
        curr_key = self.my_map.validMove(self.posActual_x, self.posActual_y)
        if curr_key == 'W':
            if self._hero.getMagicFin():
                return True
            elif key == 'P' or key == 'WH' or key == 'CH' or key == 'EH' or key == 'ME' or key == 'MR' or key == 'W':
                return True
            return False
        elif curr_key == 'P':
            if key == 'W':
                self._hero.onBoat(1)
            else:
                self._hero.onBoat(0)
        elif key == 'M':
            if not self._hero.canClimbMountain():
                return False
        elif key == 'W':
            return self._hero.canMoveOnWater()
        return True

    # Metodo que traduce las posiciones del mapa para la narracion
    def mapLocation(self, key):
        if key == 'F':
            return 'un bosque'
        elif key == 'M':
            return 'una montana'
        elif key == 'G':
            return 'un saco de oro'
        elif key == 'TR':
            return 'un troll'
        elif key == 'FR':
            return 'una hada'
        elif key == 'W':
            return 'un rio o lago'
        elif key == 'ST':
            return 'una tienda'
        elif key == 'SW':
            return 'un pantano'
        elif key == 'CH':
            return 'un baul'
        elif key == 'P':
            return 'un puerto'
        elif key == 'MR' or key == 'ME':
            return 'una sirena'
        elif key == 'PH':
            return 'un camino'
        elif key == 'MG':
            return 'un equipo de montana'
        elif key == 'CS':
            return 'un castillo'
        elif key == 'LR' or key == 'LD':
            return 'una guarida'
        elif key == 'WH':
            return 'un remolino'
        elif key == 'MS':
            return 'una espada poderosa'
        elif key == 'PL':
            return 'en una planicie'
        elif key == 'EH':
            return 'un baul vacio'
        elif key == 'T':
            return 'un saco vacio'
        elif key == 'K':
            return 'muestras de que habia algo ahi'

    # Metodo que de manera aleatoria define si el personaje peleara o no con un murcielago
    def fightEnemy(self, key):
        val = random.randint(0, 10)
        if (key == 'F' and val < 6) or (key == 'PL' and val < 3):
            return Pepe(5)
        return None

    # Metodo que de manera aleatoria decide si se encuentra un objeto en el terreno o
    # un objeto marcado en el mapa
    def mapElement(self, key):
        val = random.randint(0, 10)
        if key == 'F':
            if val < 7:     # con una probabilidad del 70% en el bosque encontrara un elemento
                return elementosRandom()
        elif key == 'PL':
            if val < 3:     # con una probabilidad del 30% en la planicie encontrara un elemento
                return elementosRandom()
        elif key == 'M':
            if val < 1:     # con una probabilidad del 10% en la planicie encontrara un elemento
                return elementosRandom()
        elif key == 'G':    # Oro
            gold = Elements(1)
            gold.set_valor(200)
            return gold
        elif key == 'MR':   # sirena
            return Elements(12)
        elif key == 'MG':   # Equipo de montana
            return Elements(13)
        elif key == 'MS':   # Mighty sword
            return Elements(14)
        return None

    # Metodo que se encarga de la narracion de la posicion actual
    def narrar(self):
        elementos = self.my_map.getVicinity(self.posActual_x, self.posActual_y)
        texto = "\n============================\nAhora te encuentras " + self.mapLocation(elementos["over"]) + ".\n"
        if "right" in elementos.keys():
            texto += "Al ESTE puedes ver " + self.mapLocation(elementos["right"]) + ". "
        if "left" in elementos.keys():
            texto += "Al OESTE puedes ver " + self.mapLocation(elementos["left"]) + ". "
        if "top" in elementos.keys():
            texto += "Al NORTE puedes ver " + self.mapLocation(elementos["top"]) + ". "
        if "bottom" in elementos.keys():
            texto += "Al SUR puedes ver " + self.mapLocation(elementos["bottom"]) + "."
        return texto


# Inicio del programa
engine = Engine()
engine.newGame()
