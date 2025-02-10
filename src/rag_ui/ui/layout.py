from dash import html, dcc

# Define two style dictionaries for the input container.
center_style = {
    "position": "absolute",
    "top": "50%",
    "left": "50%",
    "transform": "translate(-50%, -50%)",
    "display": "flex",
    "alignItems": "center",
    "width": "50%",
    "maxWidth": "600px",
    "background": "#fff",
    "borderRadius": "25px",
    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
    "overflow": "hidden",
}

bottom_style = {
    "position": "absolute",
    "left": "50%",
    "bottom": "20px",
    "transform": "translate(-50%, 0)",
    "display": "flex",
    "alignItems": "center",
    "width": "50%",
    "maxWidth": "600px",
    "background": "#fff",
    "borderRadius": "25px",
    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
    "overflow": "hidden",
}

# The layout includes:
# - A top widget bar with a "New Chat" button,
# - Two hidden Stores (one for submission state and one for conversation history),
# - A hidden Interval component (to update pending machine answers),
# - The chat container, and
# - The input container.
layout = html.Div(
    style={
        "height": "100vh",
        "width": "100vw",
        "backgroundColor": "#f0f0f0",
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
                "backgroundColor": "#007BFF",
                "display": "flex",
                "alignItems": "center",
                "padding": "0 20px",
                "color": "#fff",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                "zIndex": "1000"
            },
            children=[
                html.Button(
                    "New Chat",
                    id="new-chat-btn",
                    style={
                        "background": "#fff",
                        "color": "#007BFF",
                        "border": "none",
                        "padding": "10px 15px",
                        "borderRadius": "5px",
                        "cursor": "pointer",
                        "fontWeight": "bold"
                    }
                ),
                html.Div([
                    dcc.Upload(
                        id="upload-doc",
                        children=html.Button("Upload Document", id="upload-doc-btn", style={
                        "background": "#fff",
                        "color": "#007BFF",
                        "border": "none",
                        "padding": "10px 15px",
                        "borderRadius": "5px",
                        "cursor": "pointer",
                        "marginLeft": "20px",
                        "fontWeight": "bold"
                    }),
                        multiple=False
                    )
                ])
            ]
        ),
        # ----------------------------------------------------------
        
        # Store for the conversation history; initially an empty list.
        dcc.Store(id="conversation-store", data=[]),
        # Store for alerts
        dcc.Store(id="alert-store", data=""),
        # Alert box
        dcc.ConfirmDialog(id="alert-box"),
        # Recording state
        dcc.Store(id="recording-store", data=False),
        
        # Chat container (positioned below the widget bar).
        html.Div(
            id="chat-container",
            style={
                "position": "absolute",
                "top": "80px",  # Positioned below the 60px high widget bar with some spacing.
                "left": "50%",
                "transform": "translateX(-50%)",
                "width": "90%",
                "maxWidth": "600px",
                "bottom": "120px",  # Leaves room for the input container at the bottom.
                "overflowY": "auto",
                "display": "flex",
                "flexDirection": "column",
            }
        ),

        # Input container for the text field and button.
        html.Div(
            id="input-container",
            style=center_style,
            children=[
                # Text input field.
                dcc.Input(
                    id="center-input",
                    type="text",
                    placeholder="Type your message here...",
                    style={
                        "flex": "1",
                        "border": "none",
                        "padding": "15px",
                        "fontSize": "16px",
                        "outline": "none",
                    }
                ),
                html.Button(
                    id="record-btn",
                    n_clicks=0,
                    style={
                        "background": "#007BFF",
                        "border": "none",
                        "padding": "15px",
                        "color": "#fff",
                        "cursor": "pointer",
                        "fontSize": "16px",
                    },
                    children=html.I(id="record-icon", className="fas fa-microphone")
                ),
                html.Button(
                    id="enter-btn",
                    n_clicks=0,
                    style={
                        "background": "#007BFF",
                        "border": "none",
                        "padding": "15px",
                        "color": "#fff",
                        "cursor": "pointer",
                        "fontSize": "16px",
                    },
                    children=html.I(id="enter-icon", className="fas fa-arrow-up")
                )
            ]
        )
    ]
)
