import re

from django import template
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from wagtail.images.image_operations import MinMaxOperation

from wagtail.images.models import Filter
from wagtail.images.shortcuts import get_rendition_or_not_found

register = template.Library()
allowed_filter_pattern = re.compile("^[A-Za-z0-9_\-\.]+$")


@register.tag(name="image")
def image(parser, token):
    bits = token.split_contents()[1:]
    image_expr = parser.compile_filter(bits[0])
    bits = bits[1:]

    filter_specs = []
    attrs = {}
    output_var_name = None

    as_context = False  # if True, the next bit to be read is the output variable name
    is_valid = True

    for bit in bits:
        if bit == 'as':
            # token is of the form {% image self.photo max-320x200 as img %}
            as_context = True
        elif as_context:
            if output_var_name is None:
                output_var_name = bit
            else:
                # more than one item exists after 'as' - reject as invalid
                is_valid = False
        else:
            try:
                name, value = bit.split('=')
                attrs[name] = parser.compile_filter(value)  # setup to resolve context variables as value
            except ValueError:
                if allowed_filter_pattern.match(bit):
                    filter_specs.append(bit)
                else:
                    raise template.TemplateSyntaxError(
                        "filter specs in 'image' tag may only contain A-Z, a-z, 0-9, dots, hyphens and underscores. "
                        "(given filter: {})".format(bit)
                    )

    if as_context and output_var_name is None:
        # context was introduced but no variable given ...
        is_valid = False

    if output_var_name and attrs:
        # attributes are not valid when using the 'as img' form of the tag
        is_valid = False

    if len(filter_specs) == 0:
        # there must always be at least one filter spec provided
        is_valid = False

    if len(bits) == 0:
        # no resize rule provided eg. {% image page.image %}
        raise template.TemplateSyntaxError(
            "no resize rule provided. "
            "'image' tag should be of the form {% image self.photo max-320x200 [ custom-attr=\"value\" ... ] %} "
            "or {% image self.photo max-320x200 as img %}"
        )

    if is_valid:
        return ImageNode(image_expr, '|'.join(filter_specs), attrs=attrs, output_var_name=output_var_name)
    else:
        raise template.TemplateSyntaxError(
            "'image' tag should be of the form {% image self.photo max-320x200 [ custom-attr=\"value\" ... ] %} "
            "or {% image self.photo max-320x200 as img %}"
        )

def operation_to_imgix_params(operation):
    if isinstance(operation, MinMaxOperation):
        return f'w={operation.width}&h={operation.height}'

    return ''

def filter_to_imgix_params(filter):
    params = ''

    for operation in filter.operations:
        params = params + operation_to_imgix_params(operation)

    return params

class ImageNode(template.Node):
    def __init__(self, image_expr, filter_spec, output_var_name=None, attrs={}):
        self.image_expr = image_expr
        self.output_var_name = output_var_name
        self.attrs = attrs
        self.filter_spec = filter_spec

    @cached_property
    def filter(self):
        return Filter(spec=self.filter_spec)

    def render(self, context):
        try:
            image = self.image_expr.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        if not image:
            return ''

        return mark_safe(f'<img src="https://su.imgix.net/{image.file}?{filter_to_imgix_params(self.filter)}" />')