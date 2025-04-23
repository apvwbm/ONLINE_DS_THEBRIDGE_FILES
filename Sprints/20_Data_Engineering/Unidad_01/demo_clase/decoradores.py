# decoradores.py

import time
from functools import wraps
from flask import request, abort

def medir_tiempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"[DEBUG] Tiempo de ejecución de {func.__name__}: {fin - inicio:.4f} segundos")
        return resultado
    return wrapper

def require_apikey(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        apikey = request.args.get('apikey')
        if apikey != "123456":
            abort(401, description="API Key inválida o ausente")
        return func(*args, **kwargs)
    return wrapper