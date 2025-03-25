class ProjectRootSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            import os
            cls._instance = super().__new__(cls)
            cls._instance.root_path = os.path.dirname(os.path.abspath(__file__))
        return cls._instance

    def get_root_path(self):
        return self.root_path