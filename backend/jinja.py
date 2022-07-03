from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime


env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())


def datetime_filter(val):
    return val.strftime("%d.%m.%Y %H:%M")


env.filters['datetime'] = datetime_filter
