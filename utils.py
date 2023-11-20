from model import Proxy


def is_ipv4(ip: str):
    items = ip.split('.')
    if len(items) != 4:
        return False
    for item in items:
        if not item.isdigit():
            return False
        value = int(item)
        if value < 0 or value > 255:
            return False
    return True


def is_port(port: str):
    return port.isdigit()
