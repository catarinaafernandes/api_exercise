# BloqIT Locker API

A **FASTAPI application built for BloqIT's technical challenge.** This API manages Bloqs -> Lockers -> Rents workflow, enabling parcel drop-off and retrieval while keeping logic clean, readable and scalable for future and real-world deployment.


WORKFLOW

| Step | Action          | Resulting Status |
|------|-----------------|------------------|
| 1    | Create rent     | `CREATED`        |
| 2    | Dropoff         | `WAITING_DROPOFF`|
| 3    | Confirm dropoff | `WAITING_PICKUP` |
| 4    | Retrieve parcel | `DELIVERED`      |



## Features
> List and fetch Bloqs, Lockers and Rents
> Create a rent with status
> Dropoff - assign rent to a locker
> Confirm dropoff (waiting pickup)
> Retrieve (delivered complete)
> JSON used as data storage(no DB)
> Change logs per entity("/bloqit_api/logs")
> Automated tests with pytest


## Structure

├── bloqit_api
│   ├── data
│   │   ├── bloqs.json
│   │   ├── json_db.py
│   │   ├── lockers.json
│   │   └── rents.json
│   ├── dto
│   │   └── rent_request.py
│   ├── logs
│   │   ├── bloqs.log
│   │   ├── lockers.log
│   │   └── rents.log
│   ├── main.py
│   ├── routes
│   │   ├── bloqs_routes.py
│   │   ├── lockers_routes.py
│   │   └── rent_routes.py
│   ├── schemas
│   │   ├── bloqs.py
│   │   ├── lockers.py
│   │   └── rents.py
│   ├── services
│   │   ├── bloqs_service.py
│   │   ├── lockers_service.py
│   │   ├── logger.py
│   │   └── rents_service.py
│   └── utils
│       └── errors.py
├── legacy
│   ├── index.js
│   └── README.md
├── logs
│   ├── bloqs.log
│   ├── lockers.log
│   └── rents.log
├── requirements.txt
├── struct.txt
└── tests
    ├── conftest.py
    ├── data
    │   ├── bloqs.json
    │   ├── lockers.json
    │   └── rents.json
    ├── older
    │   ├── test_json.py
    │   └── test_rent_manual.py
    ├── README.md
    ├── test_endpoints.py
    └── test_unit_rent.py



 ## How to run?
>Run locally
```bash
pip install -r requirements.txt
uvicorn bloqit_api.main:app --reload

```

>Optionally you can expose externally with ngrok
ngrok http 8000



## Main API Endpoints
- `POST /rents` -> Create rent  
- `POST /rents/{id}/dropoff` -> Assign locker  
- `POST /rents/{id}/confirm_dropoff` ->  Waiting Pickup  
- `POST /rents/{id}/retrieve` ->  Delivered  
- `GET /rents` ->  List rents  
- `GET /rents/{id}`->  Rent details  
- `GET /lockers` ->  List lockers  
- `GET /bloqs` ->  List bloqs  


Docs available at:
http://127.0.0.1:8000/docs


## Running tests
pytest

Uses temporary JSON copies - real files never changed (except in older tests)


## Design Notes
-Separation of layers: routes/services/schemas/data
-DTOs used for request validation
-Business logic lives in /services
-Logging for traceability



## Next Steps/Future improvements:

>Migrate from JSON to a real database (ex:SQLAlchemy) 
>Add authentication
>Implement a GUI to manage lockers,rents and delivery flow



## About
This project was developed for BloqIT where the fictional scenario assumed that the original locker system had been lost after a collective amnesia event  - leaving only JSON files and parts of the model behind.
This challenge provided an opportunity to reimplement the locker workflow while applying good programming practices in a simple way: service layer for logic, clean routes, validated data through schemas and architecture that is easy to understand, maintain and extend.

    KISS in implementation
    SOLID in structure
    CRUD in action


Made with love, coffee and many prints - powered by Python and FASTAPI 