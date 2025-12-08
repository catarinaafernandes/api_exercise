#Observer pattern

class EventBus:
    _subscribers = dict[str, list] = {}

    @classmethod
    def subscribe(cls, event_name: str, callback):
        cls._subscribers.setdefault(event_name, [].append(callback))

    @classmethod
    def emit(cls, event_name: str, data):
        for callback in cls._subscribers.get(event_name, []):
            callback(data)