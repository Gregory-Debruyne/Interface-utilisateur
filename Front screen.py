from nicegui import ui
import json
import time
import paho.mqtt.client as mqtt

# ------------------ CONFIG MQTT ------------------

MQTT_BROKER = "172.11.1.35"
MQTT_PORT = 1883
MQTT_TOPIC = "machinesight/ordre"
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)
MQTT_TOPIC_STATUS = "machinesight/status"


def on_connect(client, userdata, flags, rc):
    print("MQTT connecté, code retour :", rc)
    # Si tu veux recevoir des infos du Pi:
    client.subscribe(MQTT_TOPIC_STATUS)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Message reçu sur {msg.topic} : {payload}")
    # Tu peux aussi afficher dans l'interface:
    ui.notify(f"MQTT: {payload}")

client.on_connect = on_connect
client.on_message = on_message

# Connexion au broker du Raspberry Pi
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()  # boucle réseau MQTT en arrière-plan


# ------------------ VARIABLES UI ------------------

Exemple_bouton = 'w-[175px] h-[55px] text-lg'
bouton_rond = 'w-[60px] h-[60px] text-2xl rounded-full'
temps_c = 0
mode = "Aucun"
mode_label = None
value_label = None
temps_choisi = 0
def publier(message: dict):
    """Envoie un message JSON au Raspberry via MQTT."""
    client.publish(MQTT_TOPIC, json.dumps(message))
    print("Publié sur MQTT :", message)


def on_click_bouton(numero: str):
    global mode, mode_label
    mode = numero
    print(f'Mode changé : {mode}')
    # Mise à jour du label d'affichage du mode
    mode_label.set_text(f'Mode actuel : {mode}')

def start ():
    ui.notify('Démarrage du processus !')
    print(f'Processus démarré en mode : {mode} pour {temps_c} secondes.')

    publier({
        "action": "start",
        "mode": mode,
        "durée": temps_c  
         })
def stop ():
    ui.notify('Processus arrêté !')
    print('Processus arrêté.')
    mode = "Aucun"
    mode_label.set_text(f'Mode actuel : {mode}')
    publier({
        "action": "stop"
         })

def increment():
    global temps_c
    temps_c += 1
    value_label.set_text(str(temps_c))

def decrement():
    global temps_c
    if temps_c > 0:
        temps_c -= 1
        value_label.set_text(str(temps_c))
def valeur_temps(value):
    global temps_c
    temps_c = value
    value_label.set_text(str(temps_c))
    return temps_c


# Mise en page plein écran avec centrage du contenu
with ui.row().classes('w-full h-screen'):
    with ui.column().classes('absolute left-[50%] top-[35%] -translate-x-1/2 -translate-y-1/2'):

        # Affichage du mode actuel

        mode_label = ui.label(f'Mode actuel : {mode}').classes('text-xl')

        # Première rangée de 2 boutons

        with ui.row().classes():
            ui.button('Vidange', on_click=lambda: on_click_bouton("vidange")).classes(Exemple_bouton)
            ui.button('Séparation', on_click=lambda: (on_click_bouton("separation"), valeur_temps(30))).classes(Exemple_bouton)
           

        # Deuxième rangée de 2 boutons
        with ui.row().classes():
            ui.button('Chaos', on_click=lambda: on_click_bouton("ko")).classes(Exemple_bouton)
            ui.button('Rassemblement', on_click=lambda: (on_click_bouton("rassemblement"), valeur_temps(30))).classes(Exemple_bouton)
        

        # boutons de maintenance en haut à droite
    with ui.row().classes('absolute left-[90%] top-[25%] -translate-x-1/2 -translate-y-1/2 gap-5'):
        with ui.row().classes():
            ui.button('maintenance', on_click=lambda: on_click_bouton("maintenance")).classes(Exemple_bouton)
            ui.button('reset', on_click=lambda: on_click_bouton("reset")).classes(Exemple_bouton)
            ui.button('ouverture trappe', on_click=lambda: on_click_bouton("ouverture trappe")).classes(Exemple_bouton)
            ui.button('LED ON', on_click=lambda: on_click_bouton("LED ON")).classes(Exemple_bouton)

    with ui.column().classes('absolute left-[50%] top-[70%] -translate-x-1/2 -translate-y-1/2'):
        # Zone d'affichage du chiffre et Boutons + et -
        with ui.row().classes('gap-4'):
            ui.button('-', on_click=decrement).classes('w-[60px] h-[60px] text-2xl')
            value_label = ui.label(f'{temps_c}').classes('text-4xl font-bold')
            ui.label('S').classes('text-4xl font-bold')
            ui.button('+', on_click=increment).classes('w-[60px] h-[60px] text-2xl')
    with ui.column().classes('absolute left-[50%] top-[57%] -translate-x-1/2 -translate-y-1/2'):
        # Zone d'affichage du chiffre et Boutons + et -
        with ui.row().classes('gap-4'):
            ui.button('15s', on_click=lambda: valeur_temps(15)).classes(bouton_rond)
            ui.button('30s', on_click=lambda: valeur_temps(30)).classes(bouton_rond)
            ui.button('45s', on_click=lambda: valeur_temps(45)).classes(bouton_rond)
            ui.button('60s', on_click=lambda: valeur_temps(60)).classes(bouton_rond)

    # Bouton START en bas au centre

    with ui.column().classes('absolute left-[50%] top-[85%] -translate-x-1/2 -translate-y-1/2'):
        with ui.row().classes('gap-5'):
            ui.button('Start', on_click=start).classes(Exemple_bouton)
            ui.button('Stop', on_click=stop).classes(Exemple_bouton)


ui.run()


