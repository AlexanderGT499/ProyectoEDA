
from enum import Enum

# 1. DEFINICIÓN DE TIPOS (Osea los vértices del Grafo)
class TipoSala(Enum):
    NORMAL = "Normal"
    ENEMIGO = "Enemigo"
    POCION = "Pocion"
    TESORO = "Tesoro"
    EVENTO = "Evento Aleatorio"
    TRAMPA = "Trampa"
    FINAL = "Jefe Final"

# 2. CLASE SALA (El Nodo)
class Sala:
    def __init__(self, id_sala, tipo, dificultad=1):
        self.id = id_sala           # Identificador único del nodo
        self.tipo = tipo            # Tipo de nodo (Enemigo, Tesoro, etc.)
        self.dificultad = dificultad 
        self.conexiones = []       
        

        self.arbol_decision = None 

    def conectar(self, id_otra_sala):
        if id_otra_sala not in self.conexiones:
            self.conexiones.append(id_otra_sala)

    def asignar_arbol(self, raiz_arbol):
       
        self.arbol_decision = raiz_arbol

    def __repr__(self):
        return f"Sala[{self.id}] ({self.tipo.value}) -> Conecta con: {self.conexiones}"


class GrafoDungeon:
    def __init__(self):
        
        self.nodos = {} 

    def agregar_sala(self, sala):
        self.nodos[sala.id] = sala

    def crear_conexion(self, id_a, id_b, bidireccional=True):
      
        if id_a in self.nodos and id_b in self.nodos:
            self.nodos[id_a].conectar(id_b)
            if bidireccional:
                self.nodos[id_b].conectar(id_a)
        else:
            print(f"Error: No se pueden conectar {id_a} y {id_b} (¿Existen?)")

    def obtener_sala(self, id_sala):
        return self.nodos.get(id_sala)