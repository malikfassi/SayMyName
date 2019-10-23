class singleton:
    def __init__(self, decorated_class):
        self.decorated_class = decorated_class
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.decorated_class(*args, **kwargs)
        return self.instance

    def __getattr__(self, item):
        # Redirect getattr to the decorated class when it is missing
        # This allows getting class attributes and methods of the decorated class
        return getattr(self.decorated_class, item)

