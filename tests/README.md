#BloqIT Locker API


Features
> List and fetch Bloqs, Lockers and Rents
> Create a rent
> Dropoff
> Confirm dropoff
> Retrieve
> JSON used as data storage(no DB in requirements)
> Change logs epr entity(´/bloqit_api/logs´)
> Automated tests with pytest


Structure

├── bloqit_api
│   ├── data
│   │   ├── bloqs.json
│   │   ├── __init__.py
│   │   ├── json_db.py
│   │   ├── lockers.json
│   │   └── rents.json
│   ├── dto
│   │   ├── __init__.py
│   │   └── rent_request.py
│   ├── __init__.py
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
    ├── __init__.py
    ├── older
    │   ├── test_json.py
    │   └── test_rent_manual.py
    ├── README.md
    ├── test_endpoints.py
    └── test_unit_rent.py



How to run?

pip install -r requirements.txt
uvicorn bloqit_api.main:app --reload


Main API Endpoints


Running tests


Next Steps/Future improvements:

>Migrate from JSON to a real database (ex:SQLAchemy) 
>Add authentication
>Implement a GUI to manage lockers,rents and delivery flow



Made with Py



About


