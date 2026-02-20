import random
from graph_system import GrafoDungeon, Sala, TipoSala
from tree_system import NodoDecision

class Jugador:
    def __init__(self, nodo_inicial):
        self.vida = 100
        self.puntaje = 0 # ORO
        self.estrategia = 0 # PUNTOS DE BUENAS DECISIONES
        self.pociones = 0
        self.fuerza = 0   
        self.defensa = 0  
        self.nodo_actual = nodo_inicial
        self.nodo_anterior = 0 
        self.vivo = True 

    def modificar_vida(self, cantidad):
        self.vida += cantidad
        if self.vida > 100: self.vida = 100
        if self.vida <= 0:
            self.vida = 0
            self.vivo = False
        else:
            self.vivo = True

class DungeonLogic:
    DATOS_ENEMIGOS = [
        {"id": 1, "nombre": "Goblin Recluta", "hp": 20, "dano_min": 5, "dano_max": 10, "soborno": 30},
        {"id": 2, "nombre": "Orco Berserker", "hp": 50, "dano_min": 10, "dano_max": 20, "soborno": 60},
        {"id": 3, "nombre": "ESPECTRO DE HIELO", "hp": 80, "dano_min": 15, "dano_max": 30, "soborno": 90},
        {"id": 4, "nombre": "CABALLERO CORRUPTO", "hp": 120, "dano_min": 20, "dano_max": 35, "soborno": 120},
        {"id": 5, "nombre": "GRAN DRAGON ROJO", "hp": 500, "dano_min": 40, "dano_max": 60, "soborno": 9999}
    ]

    def __init__(self):
        self.grafo = GrafoDungeon()
        self.jugador = None
        self.texto_evento = ""
        self.imagen_evento_id = 0 
        self.turno_jugador = 1 
        
        # Datos finales
        self.vida_jugador_1 = 0
        self.oro_jugador_1 = 0
        self.est_jugador_1 = 0
        
        self.vida_jugador_2 = 0
        self.oro_jugador_2 = 0
        self.est_jugador_2 = 0

    def iniciar_juego(self):
        self.jugador = Jugador(0)
        self._generar_ruta_aleatoria()
        self.imagen_evento_id = 0 
        print(f"--- SISTEMA: Turno Jugador {self.turno_jugador} Iniciado ---")

    def reiniciar_torneo(self):
        print("--- REINICIANDO TORNEO COMPLETO ---")
        self.turno_jugador = 1
        self.vida_jugador_1 = 0
        self.oro_jugador_1 = 0
        self.est_jugador_1 = 0
        self.vida_jugador_2 = 0
        self.oro_jugador_2 = 0
        self.est_jugador_2 = 0
        self.iniciar_juego()
        self.texto_evento = "NUEVA PARTIDA: JUGADOR 1, TU TURNO."

    def finalizar_turno_actual(self, causa_muerte=False):
        vida_final = self.jugador.vida if not causa_muerte else 0
        oro_final = self.jugador.puntaje
        est_final = self.jugador.estrategia
        
        if self.turno_jugador == 1:
            self.vida_jugador_1 = vida_final
            self.oro_jugador_1 = oro_final 
            self.est_jugador_1 = est_final
            
            txt_resumen = f"EL JUGADOR 1 HA CAIDO.\n(HP: {vida_final} | Oro: {oro_final} | Sabiduria: {est_final})"
            if not causa_muerte:
                txt_resumen = f"EL JUGADOR 1 HA SOBREVIVIDO.\n(HP: {vida_final} | Oro: {oro_final} | Sabiduria: {est_final})"
            
            raiz = NodoDecision(f"{txt_resumen}\n\nAHORA EL DESTINO LLAMA AL JUGADOR 2.\n¿Tienes el valor suficiente?", 
                                efecto={'tipo_enemigo': 0, 'fondo_id': 0})
            btn_p2 = NodoDecision("TOMAR EL LUGAR", es_hoja=True, 
                                  efecto={'cambiar_turno': True, 'texto_custom': "Iniciando J2..."})
            raiz.agregar_opciones(btn_p2)
            return raiz
        else: 
            self.vida_jugador_2 = vida_final
            self.oro_jugador_2 = oro_final
            self.est_jugador_2 = est_final
            return self._calcular_ganador()

    def _calcular_ganador(self):
        v1 = self.vida_jugador_1
        o1 = self.oro_jugador_1
        e1 = self.est_jugador_1
        
        v2 = self.vida_jugador_2
        o2 = self.oro_jugador_2
        e2 = self.est_jugador_2
        
        # --- AQUÍ ESTÁ EL ARREGLO GRACIOSO ---
        def formatear_sabiduria(puntos):
            if puntos < 0: return "¡CEREBRO DE GOBLIN!" # Mensaje gracioso si es negativo
            return f"{puntos} Ptos"

        txt_e1 = formatear_sabiduria(e1)
        txt_e2 = formatear_sabiduria(e2)
        
        detalles = f"\n\n[ J1: {txt_e1} | {o1} Oro ]\nVS\n[ J2: {txt_e2} | {o2} Oro ]"
        
        if e1 > e2:
            ganador = f"¡VICTORIA PARA JUGADOR 1!\nHa demostrado mayor inteligencia.{detalles}"
        elif e2 > e1:
            ganador = f"¡VICTORIA PARA JUGADOR 2!\nSus decisiones fueron mas sabias.{detalles}"
        else:
            if o1 > o2:
                ganador = f"¡EMPATE EN SABIDURIA!\nPero JUGADOR 1 gana por RIQUEZA.{detalles}"
            elif o2 > o1:
                ganador = f"¡EMPATE EN SABIDURIA!\nPero JUGADOR 2 gana por RIQUEZA.{detalles}"
            else:
                if v1 > v2:
                    ganador = f"EMPATE TOTAL... Pero J1 esta mas sano. ¡Victoria J1!{detalles}"
                elif v2 > v1:
                    ganador = f"EMPATE TOTAL... Pero J2 esta mas sano. ¡Victoria J2!{detalles}"
                else:
                    ganador = f"EMPATE ABSOLUTO Y LEGENDARIO.{detalles}"

        raiz = NodoDecision(ganador, efecto={'tipo_enemigo': 7, 'fondo_id': 9}) 
        btn_reset = NodoDecision("REINICIAR EL CICLO", es_hoja=True, 
                                 efecto={'reiniciar_total': True, 'texto_custom': "El tiempo retrocede..."})
        raiz.agregar_opciones(btn_reset)
        return raiz

    def obtener_nodo_game_over(self):
        return self.finalizar_turno_actual(causa_muerte=True)

    def _generar_ruta_aleatoria(self):
        self.grafo.salas = {}
        for i in range(10): self.grafo.agregar_sala(Sala(i, TipoSala.NORMAL))
        for i in range(9): self.grafo.crear_conexion(i, i+1)

        self.grafo.obtener_sala(0).asignar_arbol(self._arbol_inicio())
        self.grafo.obtener_sala(9).asignar_arbol(self._arbol_jefe_final(5, 0))

        combates = [
            (self._arbol_combate, 1, 1, "El aire huele a humedad y sangre vieja.", "El Goblin exhala su ultimo aliento."),
            (self._arbol_combate, 2, 3, "El calor es insoportable. Hay huesos en el suelo.", "El Orco cae con un ruido sordo."),
            (self._arbol_combate, 3, 5, "Una niebla helada congela tus pulmones.", "El espectro se disuelve en el aire."),
            (self._arbol_combate, 4, 7, "Estandartes rotos y metal oxidado.", "La armadura vacia se desploma.")
        ]
        
        eventos = [
            (self._arbol_sorpresa, 2, "Un pasillo largo cubierto de polvo de siglos."),
            (self._arbol_evento_mistico, 4, "Un altar antiguo con inscripciones prohibidas."),
            (self._arbol_evento_trampa, 6, "El suelo tiene patrones extraños e irregulares."),
            (self._arbol_hada, 10, "Un resplandor antinatural ilumina la oscuridad."), 
            (self._arbol_mercader, 11, "Una tienda improvisada con pieles y huesos."), 
            (self._arbol_portal_caos, 12, "La realidad se distorsiona frente a ti."),
            (self._arbol_fuente, 8, "Una fuente de agua cristalina.") 
        ]
        
        bolsa_total = combates + eventos
        random.shuffle(bolsa_total)
        seleccionados = bolsa_total[:8]

        for i in range(1, 9): 
            data = seleccionados[i-1]
            func = data[0]
            if func == self._arbol_combate:
                arbol = func(data[1], i+1, data[2], data[3], data[4])
            elif func == self._arbol_fuente:
                arbol = func(i+1)
            else:
                arbol = func(i+1, data[1], data[2])
            self.grafo.obtener_sala(i).asignar_arbol(arbol)

    # --- ARBOLES DE DECISIÓN ---

    def _arbol_inicio(self):
        txt = f"TURNO DEL JUGADOR {self.turno_jugador}\n\nLas puertas del Dungeon se cierran tras de ti.\nSolo queda la oscuridad y el eco de tus pasos."
        raiz = NodoDecision(txt, es_hoja=False, efecto={'fondo_id': 0})
        raiz.agregar_opciones(NodoDecision("Adentrarse en la oscuridad", es_hoja=True, efecto={'mover_a_nodo': 1}))
        return raiz

    def _arbol_combate(self, id_enemigo, id_siguiente, id_fondo, desc_ambiente, desc_victoria):
        datos = next(e for e in self.DATOS_ENEMIGOS if e['id'] == id_enemigo)
        raiz = NodoDecision(f"{desc_ambiente}\nUna figura emerge de las sombras: {datos['nombre']}.", efecto={'tipo_enemigo': id_enemigo, 'fondo_id': id_fondo})

        dano = random.randint(datos['dano_min'], datos['dano_max'])
        oro = datos['hp']
        costo_soborno = datos.get('soborno', 999)

        fx_win_normal = {'vida': -dano, 'puntaje': oro, 'estrategia': 10, 'texto_custom': f"El enemigo cae derrotado. Limpias tu arma.\n(+{oro} Oro / +10 Ptos Estrategia).", 'tipo_enemigo': 0}
        fx_huir = {'vida': -35, 'estrategia': -5, 'texto_custom': "Corres sin mirar atras. (-35 HP / -5 Ptos Estrategia)", 'tipo_enemigo': 0}
        
        dado_destino = random.random()
        if dado_destino > 0.7: 
            txt_res = f"[ SOBORNO ACEPTADO ]\nHas evitado el combate con astucia.\n(+30 Ptos Estrategia)."
            fx_soborno = {'costo_oro': costo_soborno, 'estrategia': 30, 'texto_custom': txt_res, 'tipo_enemigo': 0}
        else:
            txt_res = f"[ ¡TRAICION! ]\nFuiste ingenuo al confiar en el monstruo.\n(-10 Ptos Estrategia)."
            fx_soborno = {'costo_oro': costo_soborno, 'vida': -dano, 'estrategia': -10, 'texto_custom': txt_res, 'tipo_enemigo': 0}
            
        nodo_resultado_soborno = NodoDecision(txt_res, es_hoja=False, efecto=fx_soborno)
        if dado_destino > 0.7:
             nodo_resultado_soborno.agregar_opciones(NodoDecision("Continuar a salvo", es_hoja=True, efecto={'mover_a_nodo': id_siguiente}))
        else:
             nodo_resultado_soborno.agregar_opciones(NodoDecision("Escapar malherido", es_hoja=True, efecto={'mover_a_nodo': id_siguiente}))

        nodo_atacar = NodoDecision("Atacar", es_hoja=False, efecto=fx_win_normal)
        nodo_atacar.agregar_opciones(NodoDecision("Continuar", es_hoja=True, efecto={'mover_a_nodo': id_siguiente}))

        nodo_huir = NodoDecision("Huir", es_hoja=False, efecto=fx_huir)
        nodo_huir.agregar_opciones(NodoDecision("Avanzar herido", es_hoja=True, efecto={'mover_a_nodo': id_siguiente}))
        
        raiz.agregar_opciones(nodo_atacar)
        if id_enemigo != 5: 
            btn_sobornar = NodoDecision(f"Sobornar ({costo_soborno} Oro)", es_hoja=False, efecto=nodo_resultado_soborno.efecto)
            for op in nodo_resultado_soborno.opciones: btn_sobornar.agregar_opciones(op)
            raiz.agregar_opciones(btn_sobornar)
        raiz.agregar_opciones(nodo_huir)

        return raiz

    def _arbol_sorpresa(self, id_siguiente, id_fondo, texto_intro):
        raiz = NodoDecision(texto_intro + "\nUn cofre antiguo reposa en el centro.", efecto={'tipo_enemigo': 0, 'fondo_id': id_fondo})
        roll = random.random()
        if roll > 0.5: 
            res = NodoDecision("Abrir con cuidado", es_hoja=False, efecto={'puntaje': 80, 'estrategia': 15, 'texto_custom': "¡FORTUNA! (+80 Oro / +15 Ptos Estrategia)"})
        else: 
            res = NodoDecision("Abrir con cuidado", es_hoja=False, efecto={'vida': -20, 'estrategia': 0, 'texto_custom': "¡TRAMPA! (-20 HP)"})
        res.agregar_opciones(NodoDecision("Seguir camino", es_hoja=True, efecto={'mover_a_nodo': id_siguiente}))
        raiz.agregar_opciones(res, NodoDecision("Ignorar y seguir", es_hoja=True, efecto={'mover_a_nodo': id_siguiente, 'estrategia': 5}))
        return raiz

    def _arbol_evento_mistico(self, id_siguiente, id_fondo, texto_intro):
        raiz = NodoDecision(texto_intro, efecto={'tipo_enemigo': 0, 'fondo_id': id_fondo})
        rezar = NodoDecision("Ofrecer plegaria", es_hoja=False, efecto={'vida': 20, 'estrategia': 10, 'texto_custom': "Sientes paz. (+20 HP / +10 Ptos Estrategia)"})
        rezar.agregar_opciones(NodoDecision("Avanzar", es_hoja=True, efecto={'mover_a_nodo': id_siguiente}))
        robar = NodoDecision("Profanar altar", es_hoja=False, efecto={'vida': -20, 'puntaje': 100, 'estrategia': 5, 'texto_custom': "El oro quema. (-20 HP / +100 Oro / +5 Ptos Estrategia)"})
        robar.agregar_opciones(NodoDecision("Avanzar", es_hoja=True, efecto={'mover_a_nodo': id_siguiente}))
        raiz.agregar_opciones(rezar, robar)
        return raiz

    def _arbol_evento_trampa(self, id_siguiente, id_fondo, texto_intro):
        raiz = NodoDecision(texto_intro, efecto={'tipo_enemigo': 0, 'fondo_id': id_fondo})
        saltar = NodoDecision("Intentar saltar", es_hoja=False, efecto={'estrategia': 10, 'texto_custom': "Salto perfecto. (+10 Ptos Estrategia)"})
        saltar.agregar_opciones(NodoDecision("Seguir", es_hoja=True, efecto={'mover_a_nodo': id_siguiente}))
        correr = NodoDecision("Correr rapido", es_hoja=False, efecto={'vida': -15, 'estrategia': -5, 'texto_custom': "Te cortaste. (-15 HP / -5 Ptos Estrategia)"})
        correr.agregar_opciones(NodoDecision("Seguir", es_hoja=True, efecto={'mover_a_nodo': id_siguiente}))
        raiz.agregar_opciones(saltar, correr)
        return raiz
    
    def _arbol_hada(self, id_siguiente, id_fondo, texto_intro):
        raiz = NodoDecision(f"{texto_intro}\nUna pequeña luz revolotea, un Hada te observa con curiosidad.", efecto={'tipo_enemigo': 8, 'fondo_id': id_fondo})
        aceptar = NodoDecision("Extender la mano", es_hoja=False, efecto={'pocion': 2, 'estrategia': 10, 'texto_custom': "El hada te bendice. (+2 Pociones / +10 Ptos Estrategia)", 'tipo_enemigo': 8})
        aceptar.agregar_opciones(NodoDecision("Agradecer y partir", es_hoja=True, efecto={'mover_a_nodo': id_siguiente}))
        ignorar = NodoDecision("Ahuyentar", es_hoja=True, efecto={'mover_a_nodo': id_siguiente, 'estrategia': 0})
        raiz.agregar_opciones(aceptar, ignorar)
        return raiz

    def _arbol_mercader(self, id_siguiente, id_fondo, texto_intro):
        raiz = NodoDecision(f"{texto_intro}\nEl Mercader te mira con ojos inyectados en sangre.\n'Oro... o Vida. Todo tiene un precio aqui'.", efecto={'tipo_enemigo': 9, 'fondo_id': id_fondo})
        
        btn_pocion = NodoDecision("Comprar Pocion (50 Oro)", es_hoja=False, 
                                  efecto={'costo_oro': 50, 'pocion': 1, 'estrategia': 10, 'texto_custom': "Buena compra. (+1 Pocion / +10 Ptos Estrategia)", 'tipo_enemigo': 9})
        btn_pocion.agregar_opciones(NodoDecision("Despedirse", es_hoja=True, efecto={'mover_a_nodo': id_siguiente}))

        roll_robo = random.random()
        if roll_robo > 0.5:
            txt_robo = "¡WOW JAJA! Le has quitado la bolsa.\n(+100 Oro / +20 Ptos Estrategia)"
            fx_robo = {'puntaje': 100, 'estrategia': 20, 'texto_custom': txt_robo, 'tipo_enemigo': 9}
        else:
            txt_robo = "¡TE ATRAPO! Te rompe un dedo.\n(-30 HP / -15 Ptos Estrategia)"
            fx_robo = {'vida': -30, 'estrategia': -15, 'texto_custom': txt_robo, 'tipo_enemigo': 9}

        nodo_res_robo = NodoDecision(txt_robo, es_hoja=False, efecto=fx_robo)
        nodo_res_robo.agregar_opciones(NodoDecision("Huir indignado", es_hoja=True, efecto={'mover_a_nodo': id_siguiente}))

        btn_robar = NodoDecision("ROBAR AL MERCADER (50% Riesgo)", es_hoja=False, efecto=nodo_res_robo.efecto)
        for op in nodo_res_robo.opciones: btn_robar.agregar_opciones(op)

        roll_caja = random.random()
        if roll_caja > 0.5:
            txt_caja = "¡JOYA BRILLANTE!\n(+150 Oro / +20 Ptos Estrategia)"
            fx_caja = {'costo_oro': 30, 'puntaje': 150, 'estrategia': 20, 'texto_custom': txt_caja, 'tipo_enemigo': 9}
        else:
            txt_caja = "¡BOMBA DE BROMA!\n(-15 HP / -5 Ptos Estrategia)"
            fx_caja = {'costo_oro': 30, 'vida': -15, 'estrategia': -5, 'texto_custom': txt_caja, 'tipo_enemigo': 9}

        nodo_res_caja = NodoDecision(txt_caja, es_hoja=False, efecto=fx_caja)
        nodo_res_caja.agregar_opciones(NodoDecision("Cerrar caja", es_hoja=True, efecto={'mover_a_nodo': id_siguiente}))

        btn_caja = NodoDecision("CAJA MISTERIOSA (30 Oro)", es_hoja=False, efecto=nodo_res_caja.efecto)
        for op in nodo_res_caja.opciones: btn_caja.agregar_opciones(op)

        btn_sangre = NodoDecision("VENDER VITALIDAD (+50 Oro / -25 HP)", es_hoja=False, 
                                  efecto={'vida': -25, 'puntaje': 50, 'estrategia': -10, 'texto_custom': "Medida desesperada.\n(+50 Oro / -25 HP / -10 Ptos Estrategia)", 'tipo_enemigo': 9})
        btn_sangre.agregar_opciones(NodoDecision("Despedirse debil", es_hoja=True, efecto={'mover_a_nodo': id_siguiente}))
        
        btn_irse = NodoDecision("No comprar nada", es_hoja=True, efecto={'mover_a_nodo': id_siguiente, 'estrategia': 0})

        raiz.agregar_opciones(btn_pocion, btn_robar, btn_caja, btn_sangre, btn_irse)
        return raiz

    def _arbol_portal_caos(self, id_siguiente, id_fondo, texto_intro):
        raiz = NodoDecision(f"{texto_intro}\nUn vortice inestable palpita frente a ti.", efecto={'tipo_enemigo': 10, 'fondo_id': id_fondo})
        roll = random.random()
        
        if roll > 0.5: 
            efecto_cruzar = {'vida': 100, 'estrategia': 5, 'texto_custom': "Curacion total. (+5 Ptos Estrategia)"}
        else: 
            efecto_cruzar = {'vida': -40, 'estrategia': 5, 'texto_custom': "Dolor agonico. (-40 HP / +5 Ptos Estrategia)"}
        
        entrar = NodoDecision("Cruzar el umbral", es_hoja=False, efecto=efecto_cruzar)
        entrar.agregar_opciones(NodoDecision("Recuperarse y avanzar", es_hoja=True, efecto={'mover_a_nodo': id_siguiente}))
        
        roll_sorpresa = random.random()
        if roll_sorpresa > 0.5:
            efecto_sorpresa = {'fuerza': 15, 'estrategia': 15, 'texto_custom': "El vacio te otorga poder. (+15 Fuerza / +15 Ptos Estrategia)"}
        else:
            efecto_sorpresa = {'vida': -20, 'puntaje': -50, 'estrategia': -10, 'texto_custom': "La locura te consume. (-20 HP / -10 Ptos Estrategia)"}
            
        btn_sorpresa = NodoDecision("MIRAR AL VACIO (Sorpresa)", es_hoja=False, efecto=efecto_sorpresa)
        btn_sorpresa.agregar_opciones(NodoDecision("Alejarse aturdido", es_hoja=True, efecto={'mover_a_nodo': id_siguiente}))

        raiz.agregar_opciones(entrar, btn_sorpresa, NodoDecision("Rodear con temor", es_hoja=True, efecto={'mover_a_nodo': id_siguiente}))
        return raiz

    def _arbol_fuente(self, id_siguiente):
        raiz = NodoDecision("Una fuente de agua cristalina en medio de la podredumbre.", efecto={'tipo_enemigo': 0, 'fondo_id': 8})
        
        texto_boton = "Continuar explorando"
        if id_siguiente == 9:
            texto_boton = "ENFRENTAR AL DESTINO FINAL"
            
        beber = NodoDecision("Beber del agua", es_hoja=False, efecto={'vida': 50, 'pocion': 1, 'estrategia': 10, 'texto_custom': "Agua pura. (+50 HP / +10 Ptos Estrategia)"})
        beber.agregar_opciones(NodoDecision(texto_boton, es_hoja=True, efecto={'mover_a_nodo': id_siguiente}))
        raiz.agregar_opciones(beber)
        return raiz

    def _arbol_jefe_final(self, id_enemigo, id_siguiente):
        datos = next(e for e in self.DATOS_ENEMIGOS if e['id'] == id_enemigo)
        raiz = NodoDecision("EL GRAN DRAGON ROJO DESPIERTA.\nSus escamas arden como el infierno. La temperatura es insoportable.", efecto={'tipo_enemigo': id_enemigo, 'fondo_id': 9})
        dano_masivo = 60 
        
        txt_misterio = "Sueltas tu arma y abres tus brazos...\n¡TE FUSIONAS CON EL DRAGON Y TE CONVIERTES EN DIOS!\n(Victoria Suprema: +5000 Oro / +100 Ptos Estrategia)."
        nodo_resultado_misterio = NodoDecision(txt_misterio, es_hoja=False, 
            efecto={'vida': 100, 'puntaje': 5000, 'estrategia': 100, 'texto_custom': txt_misterio, 'tipo_enemigo': id_enemigo})
        nodo_resultado_misterio.agregar_opciones(NodoDecision("ASCENDER AL TRONO", es_hoja=True, efecto={'finalizar_ronda': True}))

        btn_misterio = NodoDecision("CANALIZAR ENERGIA ANCESTRAL (???)", es_hoja=False, efecto=nodo_resultado_misterio.efecto)
        for op in nodo_resultado_misterio.opciones: btn_misterio.agregar_opciones(op)

        txt_derrumbe = "Disparas a las columnas. El techo colapsa sobre la bestia.\nRecuperas el tesoro intacto.\n(Sobrevives y ganas +5000 Oro / +50 Ptos Estrategia)."
        nodo_resultado_derrumbe = NodoDecision(txt_derrumbe, es_hoja=False,
            efecto={'vida': -10, 'puntaje': 5000, 'estrategia': 50, 'texto_custom': txt_derrumbe, 'tipo_enemigo': id_enemigo})
        nodo_resultado_derrumbe.agregar_opciones(NodoDecision("ESCAPAR DE LOS ESCOMBROS", es_hoja=True, efecto={'finalizar_ronda': True}))

        btn_derrumbe = NodoDecision("DERRUMBAR TECHO (Estrategia)", es_hoja=False, efecto=nodo_resultado_derrumbe.efecto)
        for op in nodo_resultado_derrumbe.opciones: btn_derrumbe.agregar_opciones(op)

        die = NodoDecision("INTENTAR HUIR", es_hoja=True, efecto={'vida': -999, 'estrategia': -100, 'texto_custom': "Mueres quemado por cobarde.\nGAME OVER."})
        
        raiz.agregar_opciones(btn_misterio, btn_derrumbe, die)
        return raiz

    def intentar_moverse(self, id_destino):
        self.jugador.nodo_actual = id_destino
        return True, "..."