class NodoDecision:
    def __init__(self, texto, es_hoja=False, efecto=None):
        self.texto = texto
        self.es_hoja = es_hoja
        self.efecto = efecto if efecto is not None else {}
        self.opciones = [] # Ahora usamos una lista flexible, no solo izq/der

    def agregar_opciones(self, *nodos):
        """
        Permite agregar cualquier cantidad de opciones.
        Ejemplo: agregar_opciones(opcion1)
        Ejemplo: agregar_opciones(atacar, huir, pocion)
        """
        for n in nodos:
            self.opciones.append(n)
            
    @property
    def izquierda(self):
        return self.opciones[0] if len(self.opciones) > 0 else None

    @property
    def derecha(self):
        return self.opciones[1] if len(self.opciones) > 1 else None