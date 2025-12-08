from bloqit_api.services.events.events_bus import EventBus


def on_rent_created(rent):
    print(f"Event: Rent created -> {rent.lockerId}")

def on_rent_dropped_off(rent):
     print(f"Event: Rent{rent.id} dropped of at locker{rent.lockerId}")

def on_rent_retrieved(rent):
     print(f"Event: Rent{rent.id} retrieved -> locker released")


#listeners regist
EventBus.subscribe("rent_created", on_rent_created)
EventBus.subscribe("rent_dropoff", on_rent_dropped_off)
EventBus.subscribe("rent_retrieved", on_rent_retrieved)
