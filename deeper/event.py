class Event:
    pass

class DirtyEvent(Event):
    pass

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
