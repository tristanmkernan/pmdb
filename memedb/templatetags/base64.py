from django import template
import base64

register = template.Library()


# thanks to https://gist.github.com/Genarito/208164e1da82f0fd08e62cbac31e79f6
@register.simple_tag
def base64ify(binary: bytes, mimetype: str) -> str:
    """
    A template tag that returns an encoded string representation of a binary input
    Usage::
        {% base64 path %}
    Examples::
        <img src="{% base64 object.content %}">
    """
    base64_str = base64.b64encode(binary).decode("utf-8")
    return f"data:{mimetype};base64,{base64_str}"
