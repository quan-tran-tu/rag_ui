import dash

from rag_ui.ui.pages.speech.callbacks import register_callbacks
from rag_ui.ui.pages.speech.layout import layout as speech_layout

dash.register_page(__name__, path='/speech')

layout = speech_layout

register_callbacks()