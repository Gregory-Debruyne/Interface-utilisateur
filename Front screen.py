from nicegui import ui
import paho.mqtt.client as mqtt

# ------------ CONFIG MQTT ------------
MQTT_BROKER = "172.11.1.35"      # IP du Raspberry
MQTT_PORT = 1883
MQTT_TOPIC_CMD = "machinesight/ordre"
MQTT_TOPIC_STATUS = "machinesight/status"

client = mqtt.Client()

last_status_label = None
log_area = None

# ------------ FONCTIONS MQTT ------------

def on_connect(client, userdata, flags, rc):
    print("MQTT connecté, code retour :", rc)
    client.subscribe(MQTT_TOPIC_STATUS)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Message reçu sur {msg.topic} : {payload}")

    def update_ui():
        # badge "dernier statut"
        last_status_label.text = payload

        # log
        if log_area.value:
            log_area.value += "\n" + payload
        else:
            log_area.value = payload

        ui.notify(f"Statut: {payload}", timeout=2)

    ui.call_from_thread(update_ui)

client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# ------------ UI ------------

def envoyer_commande(cmd: str):
    cmd = cmd.strip().lower()
    print(f"Envoi commande : {cmd}")
    client.publish(MQTT_TOPIC_CMD, cmd)
    ui.notify(f"Envoyé : {cmd}", timeout=1.5)

# Styles (Tailwind via NiceGUI)
BTN_BASE = "px-6 py-3 rounded-xl font-semibold shadow-lg transition-all duration-200"
BTN_PRIMARY = f"{BTN_BASE} bg-white text-black hover:bg-gray-200"
BTN_DARK = f"{BTN_BASE} bg-zinc-900 text-white border border-zinc-700 hover:bg-zinc-800"
BTN_ALERT = f"{BTN_BASE} bg-red-600 text-white hover:bg-red-500"
BTN_GLOW = "hover:shadow-[0_0_18px_rgba(255,255,255,0.15)]"

CARD = "w-[900px] max-w-[94vw] bg-zinc-950/60 border border-zinc-800 rounded-2xl p-6 shadow-2xl"
TITLE = "text-3xl font-bold tracking-wide"
SUB = "text-sm text-zinc-400"
SECTION = "text-xs uppercase tracking-widest text-zinc-500"
DIVIDER = "w-full border-t border-zinc-800 my-6"

with ui.column().classes("w-screen min-h-screen bg-black text-white items-center justify-center p-6"):
    # Card principale
    with ui.column().classes(CARD):
        ui.label("MachineSight Control").classes(TITLE)
        ui.label("Pilotage MQTT : vibration, trappe, LED.").classes(SUB)

        ui.element("div").classes(DIVIDER)

        # --- Ligne 1 : vibration ---
        ui.label("Vibration").classes(SECTION)
        with ui.row().classes("w-full gap-4 flex-wrap"):
            ui.button("Vidange", on_click=lambda: envoyer_commande("vidange")).classes(f"{BTN_PRIMARY} {BTN_GLOW}")
            ui.button("Séparation", on_click=lambda: envoyer_commande("separation")).classes(f"{BTN_PRIMARY} {BTN_GLOW}")
            ui.button("Rassemblement", on_click=lambda: envoyer_commande("rassemblement")).classes(f"{BTN_PRIMARY} {BTN_GLOW}")
            ui.button("KO", on_click=lambda: envoyer_commande("ko")).classes(f"{BTN_ALERT} {BTN_GLOW}")

        ui.element("div").classes("h-6")

        # --- Ligne 2 : actuateurs ---
        ui.label("Actuateurs").classes(SECTION)
        with ui.row().classes("w-full gap-4 flex-wrap"):
            ui.button("LED ON", on_click=lambda: envoyer_commande("led_on")).classes(f"{BTN_DARK} {BTN_GLOW}")
            ui.button("LED OFF", on_click=lambda: envoyer_commande("led_off")).classes(f"{BTN_DARK} {BTN_GLOW}")
            ui.button("Ouvrir trappe", on_click=lambda: envoyer_commande("servo_on")).classes(f"{BTN_DARK} {BTN_GLOW}")
            ui.button("Fermer trappe", on_click=lambda: envoyer_commande("servo_off")).classes(f"{BTN_DARK} {BTN_GLOW}")

        ui.element("div").classes(DIVIDER)

        # --- Statut + log (sans le texte “Messages d'état reçus”) ---
        with ui.row().classes("w-full items-center justify-between gap-4 flex-wrap"):
            ui.label("Dernier statut").classes(SECTION)
            last_status_label = ui.label("-").classes(
                "px-3 py-1 rounded-full bg-zinc-900 border border-zinc-700 text-zinc-200 text-sm"
            )

        log_area = ui.textarea().props("readonly").classes(
            "w-full h-[180px] bg-black text-white border border-zinc-700 rounded-xl p-3 text-sm"
        )

        # Petit bouton utilitaire
        with ui.row().classes("w-full justify-end mt-3"):
            ui.button("Clear log", on_click=lambda: setattr(log_area, "value", "")).classes(f"{BTN_DARK}")

ui.run()
