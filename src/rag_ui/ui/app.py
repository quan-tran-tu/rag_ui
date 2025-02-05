import dash

from rag_ui.db.vectorstore import init_milvus_client, create_collection
from rag_ui.core.config import EMBEDDING_DIM

# Include Font Awesome for icons.
external_stylesheets = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

milvus_client = init_milvus_client()
create_collection(milvus_client, "documents", EMBEDDING_DIM)

# Override the default index to remove margins/padding, hide overflow,
# and include extra CSS for the loading animation.
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <meta charset="utf-8">
        <title>Chat Mock App</title>
        {%favicon%}
        {%css%}
        <style>
            html, body {
                margin: 0;
                padding: 0;
                overflow: hidden;
                width: 100%;
                height: 100%;
            }
            /* Loading dots animation for machine “typing” indicator */
            .loading-dots {
                display: flex;
                align-items: center;
            }
            .loading-dots span {
                display: block;
                width: 8px;
                height: 8px;
                margin: 0 2px;
                background: #555;
                border-radius: 50%;
                animation: loading 1.4s infinite ease-in-out both;
            }
            .loading-dots span:nth-child(1) {
                animation-delay: -0.32s;
            }
            .loading-dots span:nth-child(2) {
                animation-delay: -0.16s;
            }
            @keyframes loading {
                0%, 80%, 100% {
                    transform: scale(0);
                } 40% {
                    transform: scale(1);
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Import the layout defined in layout.py
from rag_ui.ui.layout import layout
app.layout = layout

# Register all callbacks with the app.
from rag_ui.ui.callbacks import register_callbacks
register_callbacks(app, milvus_client)


if __name__ == '__main__':
    app.run_server(debug=False)
