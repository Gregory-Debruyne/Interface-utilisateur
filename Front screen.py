from nicegui import ui

Exemple_bouton = 'w-[175px] h-[55px] text-lg'
bouton_rond = 'w-[60px] h-[60px] text-2xl rounded-full'
temps_c = 0
mode = "Aucun"
mode_label = None
value_label = None
temps_choisi = 0

def on_click_bouton(numero: str):
    global mode, mode_label
    mode = numero
    print(f'Mode changé : {mode}')
    # Mise à jour du label d'affichage du mode
    mode_label.set_text(f'Mode actuel : {mode}')

def start ():
    ui.notify('Démarrage du processus !')
    print(f'Processus démarré en mode : {mode} pour {temps_c} secondes.')  
def stop ():
    ui.notify('Processus arrêté !')
    print('Processus arrêté.')
    mode = "Aucun"
    mode_label.set_text(f'Mode actuel : {mode}')

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
            ui.button('Vidange', on_click=lambda: on_click_bouton("Vidange")).classes(Exemple_bouton)
            ui.button('Séparation', on_click=lambda: (on_click_bouton("Séparation"), valeur_temps(30))).classes(Exemple_bouton)
           

        # Deuxième rangée de 2 boutons
        with ui.row().classes():
            ui.button('Chaos', on_click=lambda: on_click_bouton("Chaos")).classes(Exemple_bouton)
            ui.button('Rassemblement', on_click=lambda: (on_click_bouton("Rassemblement"), valeur_temps(30))).classes(Exemple_bouton)
        

        # boutons maintenance et reset
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


