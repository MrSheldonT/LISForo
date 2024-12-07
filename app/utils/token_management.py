import jwt
from functools import wraps
from flask import current_app
from datetime import datetime, timedelta
from flask import request
def create_jwt_token(user_id:int, role:int):
    
    #check utcnow
    expiration_time = datetime.utcnow() + timedelta(seconds=current_app.config["JWT_EXPIRATION_TIME"])
    payload = {
        "id_user": user_id
        , "id_role": role
        , "exp": expiration_time
    }
    
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    
    return token

def decode_jwt_token(token:str):
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
    

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get("Authorization")
        if not token:
            return {"message": "Token is missing"}
        
        decoded_token = decode_jwt_token(token)
        
        if "error" in decoded_token:
            return {"message": decoded_token["error"]}
        
        request.id_user = decoded_token["id_user"]
        request.id_role = decoded_token["id_role"]
        return f(*args, **kwargs)
    
    return decorated