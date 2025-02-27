import os


def save_uploaded_file(file_content, filename, folder):
    """Saves uploaded file to the specified directory."""
    file_path = os.path.join(folder, filename)
    with open(file_path, "wb") as f:
        f.write(file_content)
    return file_path

def get_latest_user_message(conversation) -> str:
    """
    Get the latest user message in the conversation list.
    """
    l = len(conversation)
    while l > 0:
        l -= 1
        if conversation[l]["role"] == "user":
            return conversation[l]["content"]
    return ""

import json
from dash import html, dcc

def create_product_div(json_res):
    """
    Create a beautiful product display div from JSON product data.
    
    Args:
        json_res (str): JSON string containing product information
        
    Returns:
        html.Div: A styled Dash HTML Div component displaying product information
    """
    try:
        intro_text = html.Div([
            html.H3("Kết quả tìm kiếm sản phẩm", style={
                'textAlign': 'center',
                'margin': '20px 0',
                'color': '#fff',
                'fontWeight': 'bold'
            }),
            html.P("Dưới đây là các sản phẩm phù hợp với yêu cầu tìm kiếm của bạn. Nhấp vào sản phẩm để xem chi tiết.", style={
                'textAlign': 'center',
                'fontSize': '14px',
                'color': '#fff',
                'marginBottom': '20px',
                'maxWidth': '800px',
                'margin': '0 auto 30px auto'
            })
        ])
        conclusion_text = html.Div([
            html.Hr(style={'marginTop': '30px', 'marginBottom': '20px'}),
            html.Div([
                html.P("Bạn có cần tìm kiếm thêm sản phẩm nào khác không?", style={
                    'fontSize': '14px',
                    'color': '#fff',
                    'marginBottom': '10px',
                    'textAlign': 'center'
                }),
            ], style={'maxWidth': '800px', 'margin': '0 auto'})
        ])
        # Parse JSON string to list of product dictionaries
        products = json.loads(json_res)
        
        # Container for all products
        product_cards = []
        
        for product in products:
            # Create individual product card
            product_card = html.Div([
                # Product image and merchant section
                html.Div([
                    html.A([
                        html.Img(
                            src=product.get('image', ''),
                            style={
                                'maxWidth': '100%',
                                'height': '180px',
                                'objectFit': 'contain',
                                'margin': 'auto',
                                'display': 'block'
                            }
                        )
                    ], href=product.get('detailUrl', '#'), target="_blank"),
                    html.Div([
                        html.Span(product.get('merchantDomain', 'Không rõ'), 
                                  style={
                                      'backgroundColor': '#f8f9fa',
                                      'padding': '3px 8px',
                                      'borderRadius': '12px',
                                      'fontSize': '12px',
                                      'color': '#666'
                                  })
                    ], style={'textAlign': 'center', 'marginTop': '8px'})
                ], style={'padding': '15px 10px'}),
                
                # Product details section
                html.Div([
                    html.A([
                        html.H4(product.get('productName', 'Không có tên'), 
                              style={
                                  'fontSize': '16px',
                                  'fontWeight': 'bold',
                                  'margin': '0 0 10px 0',
                                  'height': '40px',
                                  'overflow': 'hidden',
                                  'textOverflow': 'ellipsis',
                                  'display': '-webkit-box',
                                  'WebkitLineClamp': '2',
                                  'WebkitBoxOrient': 'vertical',
                                  'color': '#333'
                              })
                    ], href=product.get('detailUrl', '#'), target="_blank", style={'textDecoration': 'none'}),
                    
                    html.Div([
                        html.Span(f"{product.get('price', 'Giá không rõ')}",
                              style={
                                  'color': '#e63946',
                                  'fontSize': '18px',
                                  'fontWeight': 'bold',
                              })
                    ], style={'marginBottom': '8px'}),
                    
                    html.Div([
                        html.Span(f"Địa điểm: {product.get('provins', 'Không có địa điểm')}",
                              style={
                                  'fontSize': '13px',
                                  'color': '#666',
                              })
                    ]),
                ], style={'padding': '0 15px 15px 15px'})
            ], style={
                'width': '300px',
                'margin': '10px',
                'border': '1px solid #e1e4e8',
                'borderRadius': '8px',
                'backgroundColor': 'white',
                'boxShadow': '0 2px 5px rgba(0,0,0,0.05)',
                'transition': 'transform 0.3s, box-shadow 0.3s',
                'display': 'inline-block',
                'verticalAlign': 'top',
                'overflow': 'hidden'
            }, className='product-card')
            
            product_cards.append(product_card)
        
        # Return container with all product cards
        return html.Div([
            intro_text,
            html.Div(product_cards, style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'justifyContent': 'left',
                'gap': '20px',
                'padding': '10px'
            }),
            conclusion_text
        ])
    
    except Exception as e:
        # Return error message if JSON parsing fails
        return html.Div(f"Error displaying products: {str(e)}", 
                      style={'color': 'red', 'padding': '20px'})

