import json


# --- Funciones de Lógica de Negocio (Simuladas) ---
def handle_get_request(path, params):
    return {"message": f"GET request to '{path}' successful (LOCAL)", "query_params": params}


def handle_post_request(path, body):
    return {"message": f"POST request to '{path}' successful (LOCAL)", "received_body": body}


# --- Diccionario de Enrutamiento ---
ROUTE_HANDLERS = {
    ('GET', '/'): lambda params, body: {"message": "API de simulación local funcionando. ¡Bienvenido!"},
    ('POST', '/email'): lambda params, body: handle_post_request('/email', body),
    ('POST', '/login'): lambda params, body: handle_post_request('/login', body),
    ('POST', '/register'): lambda params, body: handle_post_request('/register', body),
    ('POST', '/recovery'): lambda params, body: handle_post_request('/recovery', body),
    # ... Añade todas las demás rutas aquí ...
    ('POST', '/token/transition'): lambda params, body: handle_post_request('/token/transition', body),
    ('GET', '/token'): lambda params, body: handle_get_request('/token', params),
}


def handle_not_found(method, path):
    return {"error": f"Ruta no encontrada", "details": f"No hay manejador para {method} en la ruta '{path}'."}


# --- Función Lambda Principal ---
def lambda_handler(event, context):
    path = event.get('path', '/')
    http_method = event.get('httpMethod', 'UNKNOWN').upper()
    query_params = event.get('queryStringParameters')
    
    print(f"Petición LOCAL recibida: Método={http_method}, Ruta='{path}'")


    body = {}
    if event.get('body'):
        try: body = json.loads(event['body'])
        except: return {"statusCode": 400, "body": json.dumps({"error": "Cuerpo no es JSON válido."})}


    handler = ROUTE_HANDLERS.get((http_method, path))
    
    if handler:
        response_body, status_code = handler(query_params, body), 200
    else:
        response_body, status_code = handle_not_found(http_method, path), 404


    return {
        "statusCode": status_code,
        "headers": { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
        "body": json.dumps(response_body)
    }
