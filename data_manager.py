import json
import os

class DataManager:
    def __init__(self):
        self.ruta_estado = "game_state.json"
        self.ruta_accion = "player_action.json"

    def guardar_estado_juego(self, logic, nodo_actual):
        # Obtenemos opciones
        opciones = []
        for op in nodo_actual.opciones:
            opciones.append({
                "texto": op.texto,
                "accion": "elegir_opcion",
                "target_id": 0
            })

        # Obtenemos el fondo (si no existe, usa 0)
        fondo = getattr(logic, 'fondo_visual_id', 0)

        estado = {
            "jugador": {
                "vida": logic.jugador.vida,
                "puntaje": logic.jugador.puntaje,
                "nodo_actual": logic.jugador.nodo_actual,
                "vivo": logic.jugador.vivo,
                "pociones": logic.jugador.pociones
            },
            "mensaje_sistema": "...",
            "texto_evento": logic.texto_evento,
            "imagen_evento_id": logic.imagen_evento_id,
            "fondo_id": fondo, # ¡CAMPO NUEVO!
            "opciones_disponibles": opciones
        }

        try:
            with open(self.ruta_estado, 'w') as f:
                json.dump(estado, f, indent=4)
        except Exception as e:
            print(f"Error guardando JSON: {e}")

    def leer_accion_jugador(self):
        if not os.path.exists(self.ruta_accion):
            return None
        try:
            with open(self.ruta_accion, 'r') as f:
                contenido = f.read().strip()
                if not contenido: return None
                return json.loads(contenido)
        except:
            return None