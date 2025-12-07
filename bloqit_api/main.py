from fastapi import FastAPI
from bloqit_api.routes.rent_routes import router as rent_routes
from bloqit_api.routes.lockers_routes import router as lockers_routes
from bloqit_api.routes.bloqs_routes import router as bloqs_routes


#create and config fastapi
def create_app():

    app = FastAPI(

        title = "BloqIT locker API",
        version= "1.0.1", #increment after memory loss :)
        description= ("BloqIT Locker API — Bloqs, Lockers and Rents management. \n"
        "Back online after the amnesia event, allowing customers to create, drop off and retrieve parcels.")   
     )


    app.include_router(rent_routes, prefix="/rents", tags=["Rents"])
    app.include_router(lockers_routes, prefix="/lockers", tags=["Lockers"])
    app.include_router(bloqs_routes, prefix="/bloqs", tags=["Bloqs"])


    @app.get("/" , tags = ["Status"])
    def home():     #root endpoint for BloqIT API
        return {    
            "service": "BloqIT API",
            "status": "alive",
            "docs" :"/docs"
        }

    return app


app = create_app() 

#TODO: tests + test outside local + add doc, update requirements