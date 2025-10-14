# gui/ui_app.py
from nicegui import ui
import requests

API = 'http://127.0.0.1:5050/cmd'

def send(cmd, **kwargs):
    try:
        requests.post(API, json={'cmd': cmd, 'kwargs': kwargs}, timeout=0.5)
    except Exception as e:
        print('POST failed:', e)

@ui.page('/')
def index():
    ui.label('Manim ↔ NiceGUI control')
    ui.button('Add Square', on_click=lambda: send('add_square'))
    ui.button('Spin 30°',   on_click=lambda: send('rotate', angle=3.14159/6))
    ui.button('Fade In',    on_click=lambda: send('fade_in'))
    ui.button('Quit',       on_click=lambda: send('quit'))

ui.run(native=True, reload=True, port=8090)        # or native=True if you prefer a desktop window
