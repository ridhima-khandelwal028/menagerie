from fastapi import status

def response(status_code=status.HTTP_200_OK, message="", data=None):
    return {"status_code": status_code, "message": message, "data": data}

