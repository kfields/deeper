class Event:
    pass

class LayerDirtyEvent(Event):
    pass

class LayerDeletedEvent(Event):
    def __init__(self, layer) -> None:
        super().__init__()
        self.layer = layer

class Subscription:
    def __init__(self, callback) -> None:
        self.callback = callback

class EventSource:
    def __init__(self) -> None:
        self.subscriptions = []

    def subscribe(self, callback):
        subscription = Subscription(callback)
        self.subscriptions.append(subscription)
        return subscription

    def unsubscribe(self, subscription):
        self.subscriptions.remove(subscription)

    def publish(self, event):
        for subscription in self.subscriptions:
            subscription.callback(event)
