def pluralize(number, base, suffix):
    if number < 2:
        return '{} {}'.format(number, base)
    return '{} {}{}'.format(number, base, suffix)
