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
client.loop_start()  # boucle réseau MQTT en arrière-plan


# ------------------ VARIABLES UI ------------------

Exemple_bouton = 'w-[175px] h-[55px] text-xl rounded-lg'
bouton_rond = 'w-[60px] h-[60px] text-2xl rounded-full'
temps_c = 0
mode = "Aucun"
mode_label = None
value_label = None
temps_choisi = 0
led_on = False
btn_led_on = None
btn_led_off = None
led_indicator = None
led_label = None
Servo_on = False
Servo_led_on = None
Servo_led_off = None
Servo_indicator = None
Servo_label = None
# ------------------ FONCTIONS UI ------------------
     
def update_led_ui():
    """Met à jour boutons + LED visuelle selon l'état led_on."""
    global btn_led_on, btn_led_off, led_indicator, led_label, led_on

    if led_on:
        btn_led_on.visible = False
        btn_led_off.visible = True
        led_indicator.classes('bg-green-500', remove='bg-gray-400')
    else:
        btn_led_on.visible = True
        btn_led_off.visible = False
        led_indicator.classes('bg-gray-400', remove='bg-green-500')

def toggle_led(force: bool | None = None):
    if mode == "maintenance":
        global led_on
        led_on = (not led_on) if force is None else force
        update_led_ui()
        publier({
            "action": "led",
            "state": led_on
    })
    if mode != "maintenance":
        ui.notify('Activation LED uniquement en mode maintenance')

def update_Servo_ui():
    global btn_Servo_on, btn_Servo_off, Servo_indicator, Servo_on

    if Servo_on:
        btn_Servo_on.visible = False
        btn_Servo_off.visible = True
        Servo_indicator.classes('bg-green-500', remove='bg-gray-400')
    else:
        btn_Servo_on.visible = True
        btn_Servo_off.visible = False
        Servo_indicator.classes('bg-gray-400', remove='bg-green-500')

def toggle_Servo(force: bool | None = None):
    if mode == "maintenance":
        global Servo_on
        Servo_on = (not Servo_on) if force is None else force
        update_Servo_ui()
        publier({
            "action": "Servo",
            "state": Servo_on})
    if mode != "maintenance":
        ui.notify('Activation Servo uniquement en mode maintenance')
def sortir_mode_maintenance():
    global mode, led_on, Servo_on
    if mode == "maintenance":
        led_on = False
        update_led_ui()
        Servo_on = False
        update_Servo_ui()
        ui.notify('Sortie du mode maintenance : LED et Servo désactivés.')
        publier({
            "action": "led",
            "state": led_on
    })
        publier({
            "action": "Servo",
            "state": Servo_on})


def publier(message: dict):
    """Envoie un message JSON au Raspberry via MQTT."""
    client.publish(MQTT_TOPIC, json.dumps(message))
    print("Publié sur MQTT :", message)


def Pression_boutton(numero: str):
    global mode, mode_label
    sortir_mode_maintenance()
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
    global mode
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
            ui.button('Vidange', on_click=lambda: Pression_boutton("vidange")).classes(Exemple_bouton)
            ui.button('Séparation', on_click=lambda: (Pression_boutton("separation"), valeur_temps(30))).classes(Exemple_bouton)
           

        # Deuxième rangée de 2 boutons
        with ui.row().classes():
            ui.button('Chaos', on_click=lambda: Pression_boutton("ko")).classes(Exemple_bouton)
            ui.button('Rassemblement', on_click=lambda: (Pression_boutton("rassemblement"), valeur_temps(30))).classes(Exemple_bouton)
        

        # boutons de maintenance en haut à droite
    with ui.row().classes('absolute left-[90%] top-[40%] -translate-x-1/2 -translate-y-1/2 gap-5'):
        with ui.row().classes():
            ui.button('maintenance', on_click=lambda: Pression_boutton("maintenance")).classes(Exemple_bouton)
            ui.button('reset', on_click=lambda: Pression_boutton("reset")).classes(Exemple_bouton)
            btn_Servo_on = ui.button('Servo ouvert', on_click=lambda: toggle_Servo(True))\
                    .classes(Exemple_bouton)
            btn_Servo_off = ui.button('Servo fermé', on_click=lambda: toggle_Servo(False))\
                    .classes(Exemple_bouton)
            # indicateur (petit rond) sous le bouton
            Servo_indicator = ui.element('div').classes('mt-2 w-16 h-16 rounded-full bg-gray-400')
            update_Servo_ui()

            btn_led_on = ui.button('LED ON', on_click=lambda: toggle_led(True))\
                    .classes(Exemple_bouton)
            btn_led_off = ui.button('LED OFF', on_click=lambda: toggle_led(False))\
                    .classes(Exemple_bouton)

            # indicateur (petit rond) sous le bouton
            led_indicator = ui.element('div').classes('mt-2 w-16 h-16 rounded-full bg-gray-400')

            update_led_ui()

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


