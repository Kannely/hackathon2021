from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
def load_component(value):
    return "<script type=\"module\" src=\"/static/components/{}.mjs\"></script>".format(value)

@register.simple_tag()
def load_vue_chart():
    return mark_safe("<script type=\"text/javascript\" src=\"https://unpkg.com/vue-chartjs@2.5.7-rc3/dist/vue-chartjs.full.min.js\"></script>")
