from dash import html, dcc

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
                    style={"marginRight": "10px"}
                ),
                # Upload document button
                html.Div([
                    dcc.Upload(
                        id="upload-doc",
                        children=html.Button(
                            html.I(className="fas fa-upload"),
                            id="upload-doc-btn",
                            className="icon-button",
                            style={"marginLeft": "10px"}
                        ),
                        multiple=False
                    )
                ]),
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
                "top": "80px",
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
            id="center-container",
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
                html.Div(
                    style={
                        "display": "flex", 
                        "width": "100%", 
                        "flexDirection": "column",
                        "borderRadius": "8px",
                        "overflow": "hidden" 
                    },
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
                        html.Div(
                            id="under-input",
                            style={
                                "width": "100%",
                                "background": "#303030",
                                "display": "flex",
                                "justifyContent": "flex-end",  # Align buttons to the right
                                "padding": "10px"
                            },
                            children=[
                                html.Button(
                                    html.I(id="record-icon", className="fas fa-microphone"),
                                    id="record-btn",
                                    n_clicks=0,
                                    style={
                                        "borderRadius": "50%",   
                                        "background": "#EEEAEA",    
                                        "border": "none",
                                        "width": "40px",
                                        "height": "40px",
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                        "marginLeft": "5px"
                                    }
                                ),
                                html.Button(
                                    html.I(className="fas fa-arrow-up"),
                                    id="enter-btn",
                                    n_clicks=0,
                                    style={
                                        "borderRadius": "50%",   
                                        "background": "#EEEAEA",    
                                        "border": "none",
                                        "width": "40px",
                                        "height": "40px",
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                        "marginLeft": "5px"
                                    }
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


