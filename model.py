from attr import attrs, attr


@attrs
class Proxy:
    host = attr(type=str, default=None)
    port = attr(type=int, default=None)

    def __str__(self):
        return f'{self.host}:{self.port}'
