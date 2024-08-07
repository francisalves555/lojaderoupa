from django import template

register = template.Library()


@register.filter
def formato_telefone(value):
    """ Formata o número de telefone no formato (XX) XXXXX-XXXX """
    telefone = str(value)
    if len(telefone) == 11:
        return f'({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}'
    if len(telefone) == 10:
        return f'({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}'
    else:
        return telefone