import time
import os
import json 
from game_logic import DungeonLogic
from data_manager import DataManager

def main():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    carpeta_raiz = os.path.dirname(directorio_actual)
    ruta_shared = os.path.join(carpeta_raiz, "Shared_Data")
    if not os.path.exists(ruta_shared): os.makedirs(ruta_shared)

    print("--- RPG TORNEO DUNGEON: LISTO ---")
    logic = DungeonLogic()
    logic.iniciar_juego()
    
    data_mgr = DataManager()
    data_mgr.ruta_estado = os.path.join(ruta_shared, "game_state.json")
    data_mgr.ruta_accion = os.path.join(ruta_shared, "player_action.json")

    sala_inicio = logic.grafo.obtener_sala(logic.jugador.nodo_actual)
    nodo_arbol_actual = sala_inicio.arbol_decision
    
    texto_historia_fijo = nodo_arbol_actual.texto 
    texto_feedback_temporal = "" 
    
    logic.imagen_evento_id = nodo_arbol_actual.efecto.get('tipo_enemigo', 0)
    fondo_actual = nodo_arbol_actual.efecto.get('fondo_id', 0)
    
    ultimo_tiempo_pocion = 0 
    COOLDOWN_POCION = 1.5 
    
    ultimo_tiempo_accion = 0
    COOLDOWN_ACCION = 0.5 
    
    veces_necio = 0 
    toggle_visual = False 

    print("Esperando a Unity...")
    
    try:
        while True:
            # 1. RENDERIZADO
            if texto_feedback_temporal != "":
                logic.texto_evento = f"{texto_feedback_temporal}\n----------------\n{texto_historia_fijo}"
            else:
                logic.texto_evento = texto_historia_fijo

            # 2. GUARDAR
            logic.fondo_visual_id = fondo_actual 
            data_mgr.guardar_estado_juego(logic, nodo_arbol_actual)

            # 3. LEER ACCIÓN
            accion = data_mgr.leer_accion_jugador()
            
            if accion:
                with open(data_mgr.ruta_accion, 'w') as f:
                    f.write("{}") 
                
                tipo = accion.get("accion")
                tiempo_actual = time.time()
                
                if (tiempo_actual - ultimo_tiempo_accion) < COOLDOWN_ACCION and tipo == "elegir_opcion":
                    pass 

                elif tipo == "usar_pocion":
                    if logic.jugador.nodo_actual == 0:
                        texto_feedback_temporal = "" 
                    elif (tiempo_actual - ultimo_tiempo_pocion) < COOLDOWN_POCION:
                        print("Ignorando spam pocion...") 
                    elif logic.jugador.vida <= 0:
                        texto_feedback_temporal = "Estas muerto. No puedes beber."
                    elif logic.jugador.pociones > 0:
                        logic.jugador.pociones -= 1
                        logic.jugador.modificar_vida(15)
                        ultimo_tiempo_pocion = tiempo_actual 
                        texto_feedback_temporal = f"Bebes el elixir carmesi (+15 HP).\n(Te quedan {logic.jugador.pociones} pociones)."
                    else:
                        toggle_visual = not toggle_visual
                        space = " " if toggle_visual else ""
                        texto_feedback_temporal = f"Buscas en tu bolsa, pero esta vacia.{space}"
                        ultimo_tiempo_pocion = tiempo_actual

                elif tipo == "elegir_opcion":
                    ultimo_tiempo_accion = tiempo_actual 
                    texto_boton = accion.get("texto")
                    nodo_dest = next((n for n in nodo_arbol_actual.opciones if n.texto == texto_boton), None)
                    
                    if nodo_dest:
                        fx = nodo_dest.efecto
                        costo = fx.get('costo_oro', 0)
                        
                        # --- VERIFICACIÓN DE ORO ---
                        if costo > 0 and logic.jugador.puntaje < costo:
                            if veces_necio == 0:
                                texto_feedback_temporal = f"[ ORO INSUFICIENTE ]\nRequieres {costo} monedas. Elige otra opcion."
                                veces_necio += 1 
                            else:
                                logic.jugador.modificar_vida(-10) 
                                if logic.jugador.vida <= 0:
                                    nodo_arbol_actual = logic.obtener_nodo_game_over()
                                    texto_historia_fijo = nodo_arbol_actual.texto
                                    logic.imagen_evento_id = nodo_arbol_actual.efecto.get('tipo_enemigo', 0)
                                    fondo_actual = nodo_arbol_actual.efecto.get('fondo_id', 0)
                                    texto_feedback_temporal = "+++ HAS MUERTO POR TU CODICIA Y OBSTINACION +++"
                                    veces_necio = 0 
                                else:
                                    toggle_visual = not toggle_visual
                                    space = " " if toggle_visual else ""
                                    texto_feedback_temporal = f"*** CASTIGO POR NECEDAD (-10 HP) ***\nEl enemigo aprovecha tu distraccion y te golpea.{space}"
                                    veces_necio += 1 
                        else:
                            veces_necio = 0 
                            texto_feedback_temporal = "" 
                            toggle_visual = False

                            if costo > 0:
                                logic.jugador.puntaje -= costo

                            nodo_arbol_actual = nodo_dest
                            
                            logic.jugador.modificar_vida(fx.get('vida', 0))
                            logic.jugador.puntaje += fx.get('puntaje', 0)
                            
                            if 'estrategia' in fx: logic.jugador.estrategia += fx['estrategia']
                            if 'pocion' in fx: logic.jugador.pociones += fx['pocion']
                            if 'fuerza' in fx: logic.jugador.fuerza += fx['fuerza']
                            if 'defensa' in fx: logic.jugador.defensa += fx['defensa']

                            if 'cambiar_turno' in fx:
                                logic.turno_jugador = 2
                                logic.iniciar_juego()
                                sala_inicio = logic.grafo.obtener_sala(0)
                                nodo_arbol_actual = sala_inicio.arbol_decision
                                texto_historia_fijo = nodo_arbol_actual.texto
                                logic.imagen_evento_id = 0
                                fondo_actual = 0
                                texto_feedback_temporal = "" 

                            elif 'reiniciar_total' in fx:
                                logic.reiniciar_torneo()
                                sala_inicio = logic.grafo.obtener_sala(0)
                                nodo_arbol_actual = sala_inicio.arbol_decision
                                texto_historia_fijo = nodo_arbol_actual.texto
                                logic.imagen_evento_id = 0
                                fondo_actual = 0
                                texto_feedback_temporal = "" 

                            elif 'finalizar_ronda' in fx:
                                nodo_arbol_actual = logic.finalizar_turno_actual(causa_muerte=False)
                                texto_historia_fijo = nodo_arbol_actual.texto
                                logic.imagen_evento_id = nodo_arbol_actual.efecto.get('tipo_enemigo', 0)
                                fondo_actual = nodo_arbol_actual.efecto.get('fondo_id', 0)
                            
                            elif logic.jugador.vida <= 0:
                                nodo_arbol_actual = logic.obtener_nodo_game_over()
                                texto_historia_fijo = nodo_arbol_actual.texto
                                logic.imagen_evento_id = nodo_arbol_actual.efecto.get('tipo_enemigo', 0)
                                fondo_actual = nodo_arbol_actual.efecto.get('fondo_id', 0)
                            
                            else:
                                if 'texto_custom' in fx:
                                    texto_historia_fijo = fx['texto_custom']
                                else:
                                    texto_historia_fijo = nodo_arbol_actual.texto

                                if 'tipo_enemigo' in fx: logic.imagen_evento_id = fx['tipo_enemigo']
                                if 'fondo_id' in fx: fondo_actual = fx['fondo_id']

                                if 'mover_a_nodo' in fx:
                                    id_new = fx['mover_a_nodo']
                                    logic.intentar_moverse(id_new)
                                    new_sala = logic.grafo.obtener_sala(id_new)
                                    nodo_arbol_actual = new_sala.arbol_decision
                                    texto_historia_fijo = nodo_arbol_actual.texto
                                    logic.imagen_evento_id = nodo_arbol_actual.efecto.get('tipo_enemigo', 0)
                                    if 'fondo_id' in nodo_arbol_actual.efecto:
                                        fondo_actual = nodo_arbol_actual.efecto['fondo_id']

            time.sleep(0.2)
    except KeyboardInterrupt:
        print("OFF")

if __name__ == "__main__":
    main()