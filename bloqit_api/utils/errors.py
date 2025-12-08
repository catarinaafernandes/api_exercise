from fastapi import HTTPException


#error handling (for exceptions)
def http_error(message: str):
    msg = message.lower()

    if "not found" in msg:
        return HTTPException(status_code=404, detail=message)
    #404 for rent_id or locker_id not found

    if "occupied" in msg or "unavailable" in msg:
        return HTTPException(status_code=409, detail=message)
    #409 for conflict of states - ex:trying to use a already occupied locker
    

    if "state" in msg:
        return HTTPException(status_code=400, detail=message)
    #400 -not authorized ex: try to drop off a rent that is in waiting pickup state

    return HTTPException(status_code=400, detail=message)
    #400 bad request, other errors, default error - error form client
