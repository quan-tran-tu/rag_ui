
from dash import html, dcc

layout = html.Div(
    style={
        "height": "100vh",
        "width": "100vw",
        "backgroundColor": "#212121",
        "position": "relative",
    },
    children=[
        # Stores
        dcc.Store(id="raw-audio-state", data=False), # Track if uploaded raw audio or recorded audio
        dcc.Store(id="speech-recording-store", data=False), # Track record button
        dcc.Store(id="enhanced-audio-state", data=False), # Track if enhanced audio
        dcc.Store(id="transcription-results-store", data=""), # Track transcription results
        dcc.Store(id="raw-audio-path", data=""), # Track raw audio path
        dcc.Store(id="trash", data=""), # Placeholder for unused store

        html.Div(
            id="speech-widget-bar",
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
                html.Button(
                    html.I(className="fas fa-refresh"),
                    id="refresh-btn",
                    className="icon-button",
                    style={"marginRight": "10px"}
                ),
            ]
        ),
        html.Div(
            style={
                "position": "absolute",
                "top": "60px",
                "left": "0",
                "right": "0",
                "bottom": "0",
                "padding": "20px",
                "overflowY": "auto"
            },
            children=[

                # Audio Processing Section
                html.Div(
                    style={
                        "display": "flex",
                        "gap": "20px",
                        "marginBottom": "30px",
                        "flexWrap": "wrap"
                    },
                    children=[
                        # Original Audio Section
                        html.Div(
                            style={"flex": "1", "minWidth": "300px"},
                            children=[
                                html.H3("Original Audio", style={"color": "#fff"}),
                                html.Div(
                                    id="audio-upload-container",
                                    style={
                                        "border": "2px dashed #616161",
                                        "borderRadius": "5px",
                                        "padding": "20px",
                                        "marginBottom": "10px",
                                        "height": "130px"
                                    },
                                    children=[
                                        dcc.Upload(
                                            id="upload-audio",
                                            children=html.Div([
                                                "Drag & Drop or ",
                                                html.A("Select Audio File")
                                            ]),
                                            style={"color": "#fff"},
                                            multiple=False
                                        ),
                                        html.Audio(id="raw-audio-player", controls=True,
                                                   style={"width": "100%", "marginTop": "10px"}),
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Div(
                                            style={"marginTop": "20px"},
                                            children=[
                                                html.Button(
                                                    "Enhance Audio",
                                                    id="enhance-audio-btn",
                                                    className="icon-button",
                                                    style={"marginRight": "10px"}
                                                ),
                                                dcc.Loading(
                                                    id="enhance-loading",
                                                    type="default",
                                                    children=html.Div(id="enhance-status")
                                                )
                                            ]
                                        ),
                                        html.Div(
                                            style={"marginTop": "20px"},
                                            children=[
                                                html.Button(
                                                    "Transcribe Raw Audio",
                                                    id="transcribe-raw-btn",
                                                    className="icon-button",
                                                    style={"marginRight": "10px"}
                                                ),
                                                dcc.Loading(
                                                    id="enhance-loading",
                                                    type="default",
                                                    children=html.Div(id="enhance-status")
                                                )
                                            ]
                                        ),
                                    ],
                                    style={"display": "flex"}
                                )
                            ]
                        ),

                        # Enhanced Audio Section
                        html.Div(
                            style={"flex": "1", "minWidth": "300px"},
                            children=[
                                html.H3("Enhanced Audio", style={"color": "#fff"}),
                                html.Div(
                                    id="enhanced-audio-container",
                                    style={
                                        "border": "2px dashed #616161",
                                        "borderRadius": "5px",
                                        "padding": "20px",
                                        "minHeight": "10px",
                                        "height": "130px",
                                    },
                                    children=[
                                        html.Audio(id="enhanced-audio-player", controls=True,
                                                  style={"width": "100%", "marginTop": "28px"}),
                                    ]
                                ),
                                
                                html.Div(
                                    style={"marginTop": "28px"},
                                    children=[
                                        html.Button(
                                            "Transcribe Clean Audio",
                                            id="transcribe-clean-btn",
                                            className="icon-button",
                                            style={"marginRight": "10px"}
                                        ),
                                        dcc.Loading(
                                            id="transcribe-loading",
                                            type="default",
                                            children=html.Div(id="transcribe-status")
                                        )
                                    ]
                                )
                            ]
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Button(
                            "Record",
                            n_clicks=0,
                            id="speech-record-btn",
                            className="icon-button",
                            style={
                                "border": "2px solid lightgrey",
                            }
                        ),
                    ],
                    style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center",
                    }
                ),
                # Transcription Results
                html.Div(
                    children=[
                        html.H3("Transcription Results", style={"color": "#fff"}),
                        html.Pre(
                            id="transcription-results",
                            style={
                                "backgroundColor": "#424242",
                                "color": "#fff",
                                "padding": "20px",
                                "borderRadius": "5px",
                                "whiteSpace": "pre-wrap",
                                "maxHeight": "300px",
                                "overflowY": "auto"
                            }
                        ),
                    ]
                )
            ]
        )
    ]
)
