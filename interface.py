from nicegui import ui
import paho.mqtt.client as mqtt

# ------------ CONFIG MQTT ------------
MQTT_BROKER = "172.11.1.35"      # <<< MET ICI L'IP DE TON RASPBERRY
MQTT_PORT = 1883
MQTT_TOPIC_CMD = "machinesight/ordre"
MQTT_TOPIC_STATUS = "machinesight/status"

client = mqtt.Client()

# Ces variables seront créées plus bas dans l'UI,
# on les déclare ici pour pouvoir les modifier dans on_message
last_status_label = None
log_area = None


# ------------ FONCTIONS MQTT ------------

def on_connect(client, userdata, flags, rc):
    print("MQTT connecté, code retour :", rc)
    # On s'abonne aux messages de statut venant du RPi
    client.subscribe(MQTT_TOPIC_STATUS)


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Message reçu sur {msg.topic} : {payload}")

    # Mise à jour de l'interface depuis le thread MQTT
    def update_ui():
        last_status_label.text = payload
        # On ajoute le message à l'historique (une ligne par message)
        if log_area.value:
            log_area.value += "\n" + payload
        else:
            log_area.value = payload
        ui.notify(f"Statut: {payload}")

    ui.call_from_thread(update_ui)


client.on_connect = on_connect
client.on_message = on_message

# Connexion au broker du Raspberry Pi
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()  # boucle réseau MQTT en arrière-plan


# ------------ FONCTIONS UI ------------

def envoyer_commande(cmd: str):
    """Envoie une commande simple (string) au Raspberry via MQTT."""
    print(f"Envoi commande : {cmd}")
    client.publish(MQTT_TOPIC_CMD, cmd)
    ui.notify(f"Commande envoyée : {cmd}")


# ------------ CONSTRUCTION DE L'INTERFACE ------------

with ui.column().classes(
    "w-screen h-screen bg-black text-white items-center justify-center gap-8"
):

    ui.label("Interface MachineSight").classes("text-3xl font-bold")

    ui.label("Commandes de base").classes("text-lg text-gray-300")

    # Grille de boutons de commande
    with ui.grid(columns=3).classes("gap-4"):
        ui.button("Vidange", on_click=lambda: envoyer_commande("vidange")) \
            .classes("bg-white text-black font-semibold px-6 py-3 rounded-xl shadow-lg hover:bg-gray-200")
        ui.button("Séparation", on_click=lambda: envoyer_commande("separation")) \
            .classes("bg-white text-black font-semibold px-6 py-3 rounded-xl shadow-lg hover:bg-gray-200")
        ui.button("Rassemblement", on_click=lambda: envoyer_commande("rassemblement")) \
            .classes("bg-white text-black font-semibold px-6 py-3 rounded-xl shadow-lg hover:bg-gray-200")

        ui.button("KO", on_click=lambda: envoyer_commande("ko")) \
            .classes("bg-white text-black font-semibold px-6 py-3 rounded-xl shadow-lg hover:bg-gray-200")
        ui.button("Maintenance", on_click=lambda: envoyer_commande("maintenance")) \
            .classes("bg-white text-black font-semibold px-6 py-3 rounded-xl shadow-lg hover:bg-gray-200")
        ui.button("Reset", on_click=lambda: envoyer_commande("reset")) \
            .classes("bg-white text-black font-semibold px-6 py-3 rounded-xl shadow-lg hover:bg-gray-200")

    ui.separator().props("color=grey-8").classes("w-1/2")

    # Zone d'affichage du dernier statut + historique
    ui.label("Messages d'état reçus").classes("text-lg text-gray-300")

    last_status_label = ui.label("-").classes("text-sm text-gray-200")

    log_area = ui.textarea() \
        .props("readonly") \
        .classes(
            "w-[420px] h-[140px] bg-black text-white border border-gray-600 "
            "rounded-lg p-2 text-sm"
        )

# Lancement du serveur NiceGUI
ui.run()
