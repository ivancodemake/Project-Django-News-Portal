from django import template

register = template.Library()

stop_words = [
    'козел',
    'олух',
    'нехороший человек',
    'дурак',
    'тубзик'
]


@register.filter(name='censor')
def censor(value):
    for a in stop_words:
        value = value.replace(a, a[:1]+(len(a)-1) * '*')
    return value


if __name__ == '__main__':
    print(censor())
