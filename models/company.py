class Company:
    def __init__(self, id=None, name=None, parent_id=None, source=None, index_url=None, request_method=None,
                 post_params=None):
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.source = source
        self.index_url = index_url
        self.request_method = request_method
        self.post_params = post_params