from django import template

register = template.Library()

@register.filter
def load_component(value):
    return "<script type=\"module\" src=\"/static/components/{}.mjs\"></script>".format(value)
load_component.is_safe = True
