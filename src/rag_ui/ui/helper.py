import os
import json
from dash import html

def save_uploaded_file(file_content, filename, folder):
    """Saves uploaded file to the specified directory."""
    file_path = os.path.join(folder, filename)
    with open(file_path, "wb") as f:
        f.write(file_content)
    return file_path

def get_history(conversation, depth: int = 2) -> list:
    """
    Get past user messages to add more context
    Args:
        depth: The number of past messages to retrieve
    """
    history = []
    l = len(conversation)
    while l > 0 and depth > 0:
        print("l", l)
        l -= 1
        if conversation[l]["role"] == "user":
            history.append(conversation[l]["content"])
            depth -= 1
    return history

def create_product_div(json_res):
    """
    Create a clean product display with each product on its own row,
    image on the right, and light grey background.
    
    Args:
        json_res (str): JSON string containing product information
        
    Returns:
        html.Div: A styled Dash HTML Div component displaying product information in rows
    """
    try:
        # Parse JSON string to list of product dictionaries
        products = json.loads(json_res)

        # Create product rows
        product_rows = []
        
        for product in products:
            product_row = html.Div([
                # Product details section (left side)
                html.Div([
                    # Merchant tag
                    html.Div(
                        html.Span(product.get('merchantDomain', ''), 
                            style={
                                'backgroundColor': '#e6e6e6',
                                'padding': '2px 8px',
                                'borderRadius': '4px',
                                'fontSize': '11px',
                                'color': '#666'
                            }
                        ),
                        style={'marginBottom': '10px'}
                    ),
                    
                    # Product name
                    html.A([
                        html.H4(product.get('productName', ''), 
                            style={
                                'fontSize': '16px',
                                'fontWeight': '500',
                                'margin': '0 0 12px 0',
                                'color': '#333',
                                'overflow': 'hidden',
                                'textOverflow': 'ellipsis',
                                'display': '-webkit-box',
                                'WebkitLineClamp': '2',
                                'WebkitBoxOrient': 'vertical'
                            })
                    ], href=product.get('detailUrl', '#'), target="_blank", style={'textDecoration': 'none'}),
                    
                    # Price
                    html.Div([
                        html.Span(f"{product.get('price', '')}",
                            style={
                                'color': '#e63946',
                                'fontSize': '18px',
                                'fontWeight': '500',
                            }
                        )
                    ], style={'marginBottom': '8px'}),
                    
                    # Location
                    html.Div([
                        html.Span(product.get('provins', ''),
                            style={
                                'fontSize': '13px',
                                'color': '#666',
                            }
                        )
                    ])
                ], style={
                    'flex': '1', 
                    'padding': '15px 20px'
                }),
                
                # Product image (right side)
                html.Div([
                    html.A([
                        html.Img(
                            src=product.get('image', ''),
                            style={
                                'height': '120px',
                                'width': '120px',
                                'objectFit': 'contain'
                            }
                        )
                    ], href=product.get('detailUrl', '#'), target="_blank")
                ], style={
                    'width': '150px', 
                    'display': 'flex', 
                    'alignItems': 'center', 
                    'justifyContent': 'center',
                    'padding': '10px'
                })
            ], style={
                'display': 'flex',
                'backgroundColor': '#f5f5f5',
                'borderRadius': '6px',
                'marginBottom': '12px',
                'boxShadow': '0 1px 2px rgba(0,0,0,0.05)',
                'overflow': 'hidden'
            }, className='product-row')
            
            product_rows.append(product_row)
        
        # Return container with all product rows
        return html.Div([
            html.Div([
                html.H3("Kết quả tìm kiếm", className="search-title", style={
                    'textAlign': 'center',
                    'margin': '5px 0',
                    'color': '#fff',
                    'fontWeight': '500'
                })
            ]),
            html.Div(product_rows, style={
                'maxWidth': '800px',
                'margin': '0 auto',
                'padding': '10px 20px'
            }),
            html.Div([
                html.P("Tìm kiếm sản phẩm khác?", style={
                    'textAlign': 'center',
                    'fontWeight': '500',
                    'color': '#fff',
                    'margin': '5px 0 5px 0'
                })
            ])
        ])
    
    except Exception as e:
        return html.Div(f"Lỗi hiển thị sản phẩm: {str(e)}", 
                      style={'color': 'red', 'padding': '20px'})