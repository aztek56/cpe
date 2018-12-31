from enum import Enum


# Objeto que declara las direcciones a donde nos podemos mover
class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4


# El objeto que contiene el mapa
class GameMap(object):
    # Constructor
    def __init__(self, size):
        self._size = size
        # El mapa que el usuario va revelando segun se mueve
        self._map = []
        # El mapa que contiene la informacion completa original
        self._hidden = []
        self.__init_map__()

    # Inicializar el mapa con valores default
    def __init_map__(self):
        for i in range(self._size):
            m_row = []
            h_row = []
            for j in range(self._size):
                m_row.append("U")   # U representa lo desconocido
                h_row.append("PL")  # PL representa una planicie
            self._map.append(m_row)
            self._hidden.append(h_row)

    # Imprimir el mapa
    def printMap(self, x, y):
        for i in range(self._size):
            line = str(i) + " "
            if i < 10: line += " "
            for j in range(self._size):
                # X marca la posicion actual
                if i == x and j == y:
                    line += "X  "
                else:
                    line += self._map[i][j] + " "
                    # Agregamos un espacio para que el mapa aparezca alineado
                    if len(self._map[i][j]) == 1:
                        line += " "
            print(line)

    # Asignar el valor al mapa oculto cuando lo leemos de archivo
    def setMapValue(self, row, col, value):
        self._hidden[row][col] = value

    # Metodo que verifica si he llegado o no a el borde del mapa
    def canMove(self, direction, row, col):
        if direction == Direction.NORTH and row > 0:
            return True
        elif direction == Direction.SOUTH and row < self._size-1:
            return True
        elif direction == Direction.WEST and col > 0:
            return True
        elif direction == Direction.EAST and col < self._size-1:
            return True
        return False

    # Metodo que me regresa el valor de una posicion del mapa para verificar si es valida.
    def validMove(self, row, col):
        return self._map[row][col]

    def visitPos(self, row, col):
        key = self._hidden[row][col]
        # Si es alguno de los objetos que son trampas, premios u objetos magicos no deben de mostrarse hasta que se
        # hayan visitado
        if key == 'CH' or key == 'FR' or key == 'TR' or key == 'G' or key == 'MR' or key == 'MG' \
                or key == 'MS' or key == 'WH':
            if col - 1 >= 0:
                self._map[row][col] = self._hidden[row][col - 1]
            else:
                self._map[row][col] = self._hidden[row][col + 1]
        else:
            self._map[row][col] = self._hidden[row][col]

    # Actualizar el mapa del jugador con los valores del mapa oculto
    def visitMap(self, row, col):
        self._map[row][col] = self._hidden[row][col]
        # Necesitamos verificar que todos las orillas de la posicion actual para mostrarla en el mapa
        if row - 1 >= 0:
            if col - 1 >= 0:
                # top-left
                self.visitPos(row - 1, col - 1)
            # top
                self.visitPos(row - 1, col)
            if col + 1 < self._size:
                # top-right
                self.visitPos(row - 1, col + 1)
        if row + 1 < self._size:
            if col - 1 >= 0:
                # bottom-left
                self.visitPos(row + 1, col - 1)
            # bottom
            self.visitPos(row + 1, col)
            if col + 1 < self._size:
                # bottom-right
                self.visitPos(row + 1, col + 1)
        if col - 1 >= 0:
            # left
            self.visitPos(row, col - 1)
        if col + 1 < self._size:
            # right
            self.visitPos(row, col + 1)

    # Obtiene un diccionario con los valores de todas las posiciones alrededor de mi posicion actual.
    def getVicinity(self, row, col):
        viewPort = {}
        viewPort["over"] = self._map[row][col]
        if row - 1 >= 0:
            if col - 1 >= 0:
                # top-left
                viewPort["topLeft"] = self._map[row - 1][col - 1]
            # top
            viewPort["top"] = self._map[row - 1][col]
            if col + 1 < self._size:
                # top-right
                viewPort["topRight"] = self._map[row - 1][col + 1]
        if row + 1 < self._size:
            if col - 1 >= 0:
                # bottom-left
                viewPort["botLeft"] = self._map[row + 1][col - 1]
            # bottom
            viewPort["bottom"] = self._map[row + 1][col]
            if col + 1 < self._size:
                # bottom-right
                viewPort["botRight"] = self._map[row + 1][col + 1]
        if col - 1 >= 0:
            # left
            viewPort["left"] = self._map[row][col - 1]
        if col + 1 < self._size:
            # right
            viewPort["right"] = self._map[row][col + 1]
        return viewPort

    # Cambiamos la marca de los baules para no repetir
    def consumeChest(self, row, col):
        self._map[row][col] = 'EH'
        self._hidden[row][col] = 'EH'

    # Cambiamos la marca de las bolsas de oro para no repetir
    def consumeGold(self, row, col):
        self._map[row][col] = 'T'
        self._hidden[row][col] = 'T'

    # Cambiamos la marca de la uarida del dragon para no repetir la batalla
    def consumeLair(self, row, col):
        self._map[row][col] = 'LD'
        self._hidden[row][col] = 'LD'

    # Cambiamos la marca de los elementos en el mapa para no repetir
    def consumeItem(self, row, col):
        self._map[row][col] = 'K'
        self._hidden[row][col] = 'K'

    # Cambiamos la marca de la sirena para no repetir la entrega
    def consumeMermid(self, row, col):
        self._map[row][col] = 'ME'
        self._hidden[row][col] = 'ME'

# Metodo que inicializa el mapa desde el archivo.
def startMap():
    file = open("map.txt")
    cnt = -1
    for line in file:
        line = line.strip()
        if cnt == -1:
            cnt = int(line)
            my_map = GameMap(cnt)
        else:
            row, col, lbl = line.split(',')
            my_map.setMapValue(int(row) - 1, int(col) - 1, lbl)
    return my_map
