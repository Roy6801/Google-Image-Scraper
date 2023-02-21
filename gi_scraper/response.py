'''
name=img_name,
position=index,
sourceName=img_src_name,
sourcePage=img_src_page,
thumbnail=img_thumb,
url=img_url
'''


class Response:

    def __init__(self, **kwargs):
        self.__kwargs = kwargs
        self.__dict__.update(kwargs)

    def to_dict(self):
        return {k: v for k, v in self.__kwargs.items()}
