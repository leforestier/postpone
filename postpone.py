""" An implementation of lazy strings. Can be used with gettext for the translation of web apps.

    Example of use:

    >>> from postpone import evalr, LazyString as _

    >>> translations = {
    ...     "Order {item}.": "Commander {item}.",
    ...     "Take a nap": "Faire une sieste",
    ...     "Stare at the wall for %s minutes.": "Fixer le mur pendant %s minutes." ,
    ...     "a new pillow": "un nouvel oreiller"           
    ... }

    >>> tasklist = [
    ...     _("Order {item}.").format(item = _("a new pillow")),
    ...     _("Take a nap") + '!', 
    ...     _("Stare at the wall for %s minutes.") % 30
    ... ]

    >>> evalr(tasklist, translations.get)
    ['Commander un nouvel oreiller.', 'Faire une sieste!', 'Fixer le mur pendant 30 minutes.']

    `evalr` walks python dictionnaries, lists, tuples or sets and apply
    a function to all the strings wrapped inside a `LazyString` object.

    To apply a function to the strings inside a single expression, you can use the `eval` method:

    >>> s = _("Take a nap") + '!'

    >>> s.eval(str.upper)
    'TAKE A NAP!'

    >>> s.eval(translations.get)
    'Faire une sieste!'

    For most projects containing more than a few strings or languages, you'll probably want to 
    use the gettext module to supply you with a translation function::

        import gettext
        translation = gettext.translation("myproject", "./locale", ["fr"])
        translated_tasklist = evalr(tasklist, translation.ugettext)
"""

__all__ = ['LazyString', 'evalr']

class StringLike(object):
        
    def format(self, *args, **kwargs):
        return Expression(str.format, self, *args, **kwargs)
        
    def __mod__(self, expr):
        return Expression(str.__mod__, self, expr)
        
    def __add__(self, expr):
        return Expression(str.__add__, self, expr)
        
    def replace(self, *args, **kwargs):
        return Expression(str.replace, self, *args, **kwargs)
        
    def capitalize(self):
        return Expression(str.capitalize, self)
        
    def lower(self):
        return Expression(str.lower, self)
        
    def upper(self):
        return Expression(str.upper, self)
        
    def encode(self, *args, **kwargs):
        return Expression(str.encode, self, *args, **kwargs)

    def __lt__(self, expr):
        return Expression(str.__lt__, self, expr)

    def __le__(self, expr):
        return Expression(str.__le__, self, expr)

    def eval(self, func):
        raise NotImplementedError

class Expression(StringLike):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def eval(self, func):
        return self.func(
            *(
                arg.eval(func) if isinstance(arg, StringLike) else arg
                for arg in self.args            
            ),
            **(
                dict((key,
                    (value.eval(func)
                    if isinstance(value, StringLike)
                    else value))
                    for key, value in self.kwargs.items()
                )
            )
        )

class LazyString(StringLike):
    def __init__(self, string):
        self.__value = string

    def eval(self, func):
        return func(self.__value)

def evalr(obj, func):
    if isinstance(obj, StringLike):
        return obj.eval(func)
    elif isinstance(obj, dict):
        return dict(
            (key,evalr(value, func))
            for key,value in obj.items()
        )
    elif isinstance(obj, list):
        return [evalr(elem, func) for elem in obj]
    elif isinstance(obj, tuple):
        return tuple(evalr(list(obj), func))
    elif isinstance(obj, set):
        return set(evalr(list(obj), func))
    else:
        return obj

if __name__ == '__main__':
    import doctest
    doctest.testmod()
     
