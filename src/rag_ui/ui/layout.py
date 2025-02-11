from dash import Dash, html, dcc

# Base style shared by both center and bottom input containers.
base_input_style = {
    "position": "absolute",
    "left": "50%",
    "width": "50%",
    "maxWidth": "600px",
    "display": "flex",
    "alignItems": "center",
    "background": "#212121",
    "borderRadius": "25px",
    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
    "overflow": "hidden",
    "padding": "15px",
}

# For center placement, add vertical centering properties.
center_style = base_input_style.copy()
center_style.update({
    "top": "50%",
    "transform": "translate(-50%, -50%)",
    "flexDirection": "column",
})

# For bottom placement, override with bottom properties.
bottom_style = base_input_style.copy()
bottom_style.update({
    "bottom": "20px",
    "transform": "translateX(-50%)",
    "flexDirection": "row",
})

# Define the common input row (the text input plus icon buttons).
input_row = html.Div(
    style={"display": "flex", "width": "100%"},
    children=[
        dcc.Input(
            id="center-input",
            type="text",
            placeholder="Type your message here...",
            style={
                "flex": "1",
                "background": "#303030",
                "border": "none",
                "padding": "15px",
                "fontSize": "16px",
                "outline": "none",
                "color": "#fff",
                "boxShadow": "none",
                "-webkit-appearance": "none",
                "-moz-appearance": "none",
                "appearance": "none"
            }
        ),
        html.Button(
            id="record-btn",
            n_clicks=0,
            className="icon-button",
            children=html.I(className="fas fa-microphone")
        ),
        html.Button(
            id="enter-btn",
            n_clicks=0,
            className="icon-button",
            children=html.I(className="fas fa-arrow-up")
        )
    ]
)

# The layout includes:
# - A top widget bar with icon buttons,
# - Hidden dcc.Stores for conversation, alerts, and recording state,
# - A chat container, and
# - An input container (with a header, text input, and icon buttons).
layout = html.Div(
    style={
        "height": "100vh",
        "width": "100vw",
        "backgroundColor": "#212121",
        "position": "relative",
    },
    children=[
        # ---------------------- Widget Bar ----------------------
        html.Div(
            id="widget-bar",
            style={
                "position": "absolute",
                "top": "0",
                "left": "0",
                "width": "100%",
                "height": "60px",
                "backgroundColor": "#212121",
                "display": "flex",
                "alignItems": "center",
                "padding": "0 20px",
                "color": "#fff",
                "zIndex": "1000"
            },
            children=[
                # New chat button
                html.Button(
                    html.I(className="fas fa-plus"),
                    id="new-chat-btn",
                    className="icon-button",
                    style={"marginRight": "10px", "background": "#212121"}
                ),
                # Upload document button
                html.Div([
                    dcc.Upload(
                        id="upload-doc",
                        children=html.Button(
                            html.I(className="fas fa-upload"),
                            id="upload-doc-btn",
                            className="icon-button",
                            style={"marginLeft": "10px", "background": "#212121"}
                        ),
                        multiple=False
                    )
                ])
            ]
        ),
        # ----------------------------------------------------------
        # Stores for conversation history, alerts, and recording state
        dcc.Store(id="conversation-store", data=[]),
        dcc.Store(id="alert-store", data=""),
        dcc.ConfirmDialog(id="alert-box"),
        dcc.Store(id="recording-store", data=False),

        # Chat container (positioned below the widget bar).
        html.Div(
            id="chat-container",
            style={
                "position": "absolute",
                "top": "80px",  # Positioned below the widget bar.
                "left": "50%",
                "transform": "translateX(-50%)",
                "width": "90%",
                "maxWidth": "600px",
                "bottom": "120px",
                "overflowY": "auto",
                "overflowX": "hidden",
                "overflowY": "auto",
                "display": "flex",
                "flexDirection": "column",
            }
        ),
        html.Div(
            id="input-container",
            style=center_style,
            children=[
                html.H1(
                    "Hello World!",
                    style={
                        "margin": "0 0 10px 0",
                        "color": "#fff",
                        "fontSize": "36px",
                        "textAlign": "center",
                        "width": "100%",
                        "borderRadius": "10px"
                    }
                ),
                input_row
            ]
        )
    ]
)


