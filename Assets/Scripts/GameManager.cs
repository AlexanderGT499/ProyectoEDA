using UnityEngine;
using UnityEngine.UI;
using System.IO;
using System.Collections;
using System.Collections.Generic;

// ------------------------------------------------------------
// ESTRUCTURA DE DATOS
// ------------------------------------------------------------
[System.Serializable]
public class GameState {
    public JugadorData jugador;
    public string mensaje_sistema;
    public string texto_evento;
    public int imagen_evento_id;
    public int fondo_id;
    public List<OpcionData> opciones_disponibles;
}

[System.Serializable]
public class JugadorData {
    public int vida;
    public int puntaje;      // Oro
    public int nodo_actual;  // Sala
    public bool vivo;
    public int pociones;
    public int estrategia;   
}

[System.Serializable]
public class OpcionData {
    public string texto;
    public string accion;
    public int target_id;
}

// ------------------------------------------------------------
// CLASE PRINCIPAL
// ------------------------------------------------------------
public class GameManager : MonoBehaviour {

    [Header("UI - HUD")]
    public Text textoVida;
    public Text textoOro;
    public Text textoPociones;
    public Text textoSala; // Ahora mostrará la SALA
    
    [Header("UI - Controles")]
    public Button botonUsarPocion; 

    [Header("UI - Narrativa")]
    public Text textoHistoria;
    public Transform contenedorBotones;
    public GameObject prefabBoton; 
    
    [Header("Visuales")]
    public Image fondoPantalla;
    public Image imagenEnemigoUI; 
    public GameObject panelTutorial;

    [Header("Colecciones")]
    public Sprite[] fondosPorSala; 
    public Sprite[] spritesEnemigos; 

    private string rutaEstado;
    private string rutaAccion;
    private float temporizador = 0f;
    private string ultimoTexto = "";
    private int ultimoIdImagen = -1;
    private int ultimoIdFondo = -1;
    private bool juegoIniciado = false;
    private int pocionesActuales = 0;

    void Start() {
        string raiz = Directory.GetParent(Application.dataPath).ToString();
        rutaEstado = Path.Combine(raiz, "../Shared_Data/game_state.json");
        rutaAccion = Path.Combine(raiz, "../Shared_Data/player_action.json");
        
        if (imagenEnemigoUI) imagenEnemigoUI.gameObject.SetActive(false);
        if (panelTutorial) panelTutorial.SetActive(true);
        juegoIniciado = false;

        if (botonUsarPocion) botonUsarPocion.onClick.AddListener(EnviarAccionPocion);
    }

    public void BotonCerrarTutorial() {
        if (panelTutorial) panelTutorial.SetActive(false);
        juegoIniciado = true;
        LeerJSON(); 
    }

    void Update() {
        if (!juegoIniciado) return;
        if (botonUsarPocion) botonUsarPocion.interactable = (pocionesActuales > 0);

        temporizador += Time.deltaTime;
        if (temporizador >= 0.5f) {
            LeerJSON();
            temporizador = 0f;
        }
    }

    void LeerJSON() {
        if (!File.Exists(rutaEstado)) return;
        try {
            string json = File.ReadAllText(rutaEstado);
            GameState estado = JsonUtility.FromJson<GameState>(json);
            if (estado != null) ActualizarJuego(estado);
        } catch {}
    }

    void ActualizarJuego(GameState estado) {
        // --- 1. HUD ---
        if (estado.jugador != null) {
            textoVida.text = "VIDA: " + estado.jugador.vida + "%";
            textoOro.text = "DINERO RECOGIDO: " + estado.jugador.puntaje;
            textoPociones.text = "POCIONES: " + estado.jugador.pociones;
            
            // --- AQUÍ ESTÁ EL CAMBIO ---
            // Ahora mostramos la SALA en lugar de la Sabiduría
            textoSala.text = "SALA: " + estado.jugador.nodo_actual;

            pocionesActuales = estado.jugador.pociones;

            // Color Vida (Verde/Rojo)
            if (estado.jugador.vida < 30) textoVida.color = Color.red;
            else textoVida.color = Color.green;
        }

        string textoNuevo = !string.IsNullOrEmpty(estado.texto_evento) ? estado.texto_evento : estado.mensaje_sistema;

        // --- 2. ACTUALIZAR HISTORIA Y VISUALES ---
        if (textoNuevo != ultimoTexto || estado.imagen_evento_id != ultimoIdImagen || estado.fondo_id != ultimoIdFondo) {
            ultimoTexto = textoNuevo;
            ultimoIdImagen = estado.imagen_evento_id;
            ultimoIdFondo = estado.fondo_id; 
            
            StopAllCoroutines();
            StartCoroutine(EscribirTexto(textoNuevo));
            
            ActualizarVisuales(estado.fondo_id, estado.imagen_evento_id);
            GenerarBotones(estado.opciones_disponibles);
        }
    }

    void ActualizarVisuales(int idFondo, int enemigoId) {
        if (enemigoId >= 0 && enemigoId < spritesEnemigos.Length) {
            if(imagenEnemigoUI) {
                if (enemigoId == 0) {
                    imagenEnemigoUI.gameObject.SetActive(false);
                } else {
                    imagenEnemigoUI.gameObject.SetActive(true);
                    if (spritesEnemigos[enemigoId] != null) imagenEnemigoUI.sprite = spritesEnemigos[enemigoId];

                    RectTransform rt = imagenEnemigoUI.GetComponent<RectTransform>();
                    
                    // Tamaños especiales
                    if (enemigoId == 6 || enemigoId == 7) { // Pantalla completa (Game Over / Win)
                        rt.anchorMin = new Vector2(0, 0); rt.anchorMax = new Vector2(1, 1); 
                        rt.offsetMin = Vector2.zero; rt.offsetMax = Vector2.zero;
                    }
                    else if (enemigoId == 8) { // Hada pequeña
                        rt.anchorMin = new Vector2(0.5f, 0.5f); rt.anchorMax = new Vector2(0.5f, 0.5f);
                        rt.sizeDelta = new Vector2(250, 250); 
                    }
                    else { // Enemigo estándar
                        rt.anchorMin = new Vector2(0.5f, 0.5f); rt.anchorMax = new Vector2(0.5f, 0.5f);
                        rt.sizeDelta = new Vector2(450, 450); 
                    }
                }
            }
        } 

        if (fondosPorSala != null && idFondo < fondosPorSala.Length) {
             if (fondosPorSala[idFondo] != null) fondoPantalla.sprite = fondosPorSala[idFondo];
        } 
    }
    
    IEnumerator EscribirTexto(string frase) {
        textoHistoria.text = "";
        foreach (char letra in frase.ToCharArray()) {
            textoHistoria.text += letra;
            yield return new WaitForSeconds(0.005f); 
        }
    }

    void GenerarBotones(List<OpcionData> opciones) {
        foreach (Transform child in contenedorBotones) Destroy(child.gameObject);
        
        if (opciones != null) {
            foreach (OpcionData opcion in opciones) {
                GameObject btn = Instantiate(prefabBoton, contenedorBotones);
                
                Text txtBtn = btn.GetComponentInChildren<Text>();
                txtBtn.text = opcion.texto; 

                // Mantiene la fuente del texto principal
                if(textoHistoria != null) txtBtn.font = textoHistoria.font;

                // Colores para pistas visuales
                if (opcion.texto.Contains("Oro")) txtBtn.color = new Color(1f, 0.9f, 0.4f);
                else if (opcion.texto.Contains("HP") || opcion.texto.Contains("Vida")) txtBtn.color = new Color(1f, 0.6f, 0.6f);

                OpcionData op = opcion;
                btn.GetComponent<Button>().onClick.AddListener(() => EnviarAccion(op));
            }
        }
    }

    void EnviarAccion(OpcionData opcion) {
        string json = "{ \"accion\": \"elegir_opcion\", \"texto\": \"" + opcion.texto + "\" }";
        File.WriteAllText(rutaAccion, json);
        foreach (Transform child in contenedorBotones) Destroy(child.gameObject); 
        textoHistoria.text = "..."; 
    }

    void EnviarAccionPocion() {
        string json = "{ \"accion\": \"usar_pocion\", \"texto\": \"beber\" }";
        File.WriteAllText(rutaAccion, json);
    }
}