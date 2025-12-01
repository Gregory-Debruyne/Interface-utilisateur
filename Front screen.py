from nicegui import ui

def on_click_bouton(numero: int):
    ui.notify(f'{numero} cliqué !')

# Mise en page plein écran avec centrage du contenu
with ui.row().classes('w-full h-screen justify-center items-center'):
    with ui.column().classes('items-center gap-4'):
        # Première rangée de 3 boutons
        with ui.row().classes('gap-4'):
            ui.button('Vidange', on_click=lambda: on_click_bouton("Vidange"))
            ui.button('Séparation', on_click=lambda: on_click_bouton("Séparation"))
            ui.button('Rassemblement', on_click=lambda: on_click_bouton("Rassemblement"))

        # Deuxième rangée de 3 boutons
        with ui.row().classes('gap-1'):
            ui.button('ko', on_click=lambda: on_click_bouton("ko"))
            ui.button('maintenance', on_click=lambda: on_click_bouton("maintenance"))
            ui.button('reset', on_click=lambda: on_click_bouton("reset"))

ui.run()


