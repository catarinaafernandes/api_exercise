from fastapi import HTTPException


#error handling (for exceptions)
def http_error(message: str):
    msg = message.lower()

    if "not found" in msg:
        return HTTPException(status_code=404, detail=message)
    #404 for rent_id or locker_id not found

    if "occupied" in msg or "unavailable" in msg:
        return HTTPException(status_code=409, detail=message)
    #409 for conflict of states - ex:

    if "state" in msg:
        return HTTPException(status_code=400, detail=message)
    #400 - ex:

    return HTTPException(status_code=400, detail=message)
    #400 bad request, default error - error form client
