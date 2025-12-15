from nicegui import ui
import paho.mqtt.client as mqtt

# ------------ CONFIG MQTT ------------
MQTT_BROKER = "172.11.1.35"
MQTT_PORT = 1883
MQTT_TOPIC_CMD = "machinesight/ordre"
MQTT_TOPIC_STATUS = "machinesight/status"

# (Optionnel) retire le warning "Callback API v1 deprecated" si dispo
# Sinon, laisse client = mqtt.Client()
try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
except Exception:
    client = mqtt.Client()

last_status_label = None
log_area = None

# On stocke le dernier message reçu ici (thread MQTT -> OK)
last_status_payload = None
pending_notif = None

# ------------ FONCTIONS MQTT ------------

def on_connect(client, userdata, flags, rc, properties=None):
    print("MQTT connecté, code retour :", rc)
    client.subscribe(MQTT_TOPIC_STATUS)


def on_message(client, userdata, msg):
    global last_status_payload, pending_notif
    payload = msg.payload.decode()
    # print(f"Message reçu sur {msg.topic} : {payload}")

    if msg.topic == MQTT_TOPIC_STATUS:
        last_status_payload = payload
        pending_notif = payload  # optionnel: déclencher une notif côté UI

client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# ------------ UI ------------

VIBRATION_MODES = {"vidange", "separation", "rassemblement", "ko"}

def afficher_table_occupee():
    message = "la table est occupée à vibrer"
    if last_status_label:
        last_status_label.text = message
    if log_area:
        log_area.value = (log_area.value + "\n" if log_area.value else "") + message
    ui.notify(message, timeout=3)

def afficher_table_prete():
    message = "la table est prête à vibrer"
    if last_status_label:
        last_status_label.text = message
    if log_area:
        log_area.value = (log_area.value + "\n" if log_area.value else "") + message
    ui.notify(message, timeout=3)

def envoyer_commande(cmd: str):
    cmd = cmd.strip().lower()
    print(f"Envoi commande : {cmd}")
    client.publish(MQTT_TOPIC_CMD, cmd)
    ui.notify(f"Envoyé : {cmd}", timeout=1.5)

    # ---- Gestion délai avant vibration ----
    if cmd in VIBRATION_MODES:
        ui.timer(0.1, afficher_table_occupee, once=True)

    # ---- Gestion délai après vibration ----
    if cmd in VIBRATION_MODES:
        ui.timer(10, afficher_table_prete, once=True)

def refresh_status_from_mqtt():
    """Tourne dans le thread UI (safe) et applique les updates reçues via MQTT."""
    global last_status_payload, pending_notif

    if last_status_payload is None:
        return

    payload = last_status_payload
    last_status_payload = None  # on consomme l'update

    if last_status_label:
        last_status_label.text = payload

    if log_area:
        log_area.value = (log_area.value + "\n" if log_area.value else "") + payload

    if pending_notif:
        ui.notify(f"Statut: {pending_notif}", timeout=2)
        pending_notif = None

# ---------- STYLES ----------
BTN_WHITE = (
    "px-6 py-3 rounded-xl font-semibold shadow-lg "
    "bg-white text-black "
    "hover:bg-gray-200 "
    "transition-all duration-200 "
    "hover:shadow-[0_0_18px_rgba(255,255,255,0.15)]"
)

CARD = "w-[900px] max-w-[94vw] bg-zinc-950/60 border border-zinc-800 rounded-2xl p-6 shadow-2xl"
TITLE = "text-3xl font-bold tracking-wide"
SUB = "text-sm text-zinc-400"
SECTION = "text-xs uppercase tracking-widest text-zinc-500"
DIVIDER = "w-full border-t border-zinc-800 my-6"

# ---------- LAYOUT ----------
with ui.column().classes("w-screen min-h-screen bg-black text-white items-center justify-center p-6"):
    with ui.column().classes(CARD):
        ui.label("MachineSight Control").classes(TITLE)
        ui.label("Pilotage MQTT : vibration, trappe, LED.").classes(SUB)

        ui.element("div").classes(DIVIDER)

        # --- Vibration ---
        ui.label("Vibration").classes(SECTION)
        with ui.row().classes("w-full gap-4 flex-wrap"):
            ui.button("Vidange", on_click=lambda: envoyer_commande("vidange")).classes(BTN_WHITE)
            ui.button("Séparation", on_click=lambda: envoyer_commande("separation")).classes(BTN_WHITE)
            ui.button("Rassemblement", on_click=lambda: envoyer_commande("rassemblement")).classes(BTN_WHITE)
            ui.button("Chaos", on_click=lambda: envoyer_commande("ko")).classes(BTN_WHITE)

        ui.element("div").classes("h-6")

        # --- Actuateurs ---
        ui.label("Actuateurs").classes(SECTION)
        with ui.row().classes("w-full gap-4 flex-wrap"):
            ui.button("LED ON", on_click=lambda: envoyer_commande("led_on")).classes(BTN_WHITE)
            ui.button("LED OFF", on_click=lambda: envoyer_commande("led_off")).classes(BTN_WHITE)
            ui.button("Ouvrir trappe", on_click=lambda: envoyer_commande("servo_on")).classes(BTN_WHITE)
            ui.button("Fermer trappe", on_click=lambda: envoyer_commande("servo_off")).classes(BTN_WHITE)

        ui.element("div").classes(DIVIDER)

        # --- Statut ---
        with ui.row().classes("w-full items-center justify-between gap-4 flex-wrap"):
            ui.label("Dernier statut").classes(SECTION)
            last_status_label = ui.label("-").classes(
                "px-3 py-1 rounded-full bg-zinc-900 border border-zinc-700 text-zinc-200 text-sm"
            )

        log_area = ui.textarea().props("readonly").classes(
            "w-full h-[180px] bg-black text-white border border-zinc-700 rounded-xl p-3 text-sm"
        )

        with ui.row().classes("w-full justify-end mt-3"):
            ui.button("Clear log", on_click=lambda: setattr(log_area, "value", "")).classes(BTN_WHITE)

# Timer UI: on applique les messages MQTT ici (thread-safe)
ui.timer(0.2, refresh_status_from_mqtt)

ui.run()
