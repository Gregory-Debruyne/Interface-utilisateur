from nicegui import ui

Exemple_bouton = 'w-[200px] h-[55px] text-lg'
temps_c= 0

def on_click_bouton(numero: int):
    ui.notify(f'{numero} cliqué !')
    info.set_text(f'Mode actuel : {numero}')


    
    


def increment():
    global temps_c
    temps_c += 1
    value_label.set_text(str(temps_c))

def decrement():
    global temps_c
    if temps_c > 0:
        temps_c -= 1
        value_label.set_text(str(temps_c))


# Mise en page plein écran avec centrage du contenu
with ui.row().classes('w-full h-screen'):
    with ui.column().classes('absolute left-[50%] top-[35%] -translate-x-1/2 -translate-y-1/2'):
        # Affichage du mode actuel
        
        ui.label(f'Mode actuel : {numero}').classes('text-xl')
        # Première rangée de 2 boutons
        with ui.row().classes():
            ui.button('Vidange', on_click=lambda: on_click_bouton("Vidange")).classes(Exemple_bouton)
            ui.button('Séparation', on_click=lambda: on_click_bouton("Séparation")).classes(Exemple_bouton)
           

        # Deuxième rangée de 2 boutons
        with ui.row().classes():
            ui.button('Chaos', on_click=lambda: on_click_bouton("Chaos")).classes(Exemple_bouton)
            ui.button('maintenance', on_click=lambda: on_click_bouton("maintenance")).classes(Exemple_bouton)

        # Troisième rangée de 2 boutons

        with ui.row().classes():
            ui.button('Rassemblement', on_click=lambda: on_click_bouton("Rassemblement")).classes(Exemple_bouton)
            ui.button('reset', on_click=lambda: on_click_bouton("reset")).classes(Exemple_bouton)

    with ui.column().classes('absolute left-[50%] top-[70%] -translate-x-1/2 -translate-y-1/2'):
        # Zone d'affichage du chiffre et Boutons + et -
        with ui.row().classes('gap-4'):
            ui.button('-', on_click=decrement).classes('w-[60px] h-[60px] text-2xl')
            value_label = ui.label(f'{temps_c}').classes('text-4xl font-bold')
            ui.label('S').classes('text-4xl font-bold')
            ui.button('+', on_click=increment).classes('w-[60px] h-[60px] text-2xl')

    # Bouton START en bas au centre

    with ui.column().classes('absolute left-[50%] top-[85%] -translate-x-1/2 -translate-y-1/2'):
        with ui.row().classes('gap-5'):
            ui.button('Start', on_click=lambda: on_click_bouton("Start")).classes(Exemple_bouton)


ui.run()


