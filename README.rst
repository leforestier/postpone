An implementation of lazy strings. Can be used in combination with *gettext* for the translation of web apps.

It's less beautiful than *speaklater* (an other implementation
of lazy strings), but I wanted lazy strings that work even if a
single thread interleaves the processing of many http requests (this happens with async frameworks).

*postpone* doesn't rely on a global state. And it doesn't use the ``thread.local()`` trick that *speaklater* uses either.

Example of use:

.. code:: python

    >>> from postpone import evalr, LazyString as _

    >>> translations = {
            "Order {item}.": "Commander {item}.",
            "Take a nap": "Faire une sieste",
            "Stare at the wall for %s minutes.": "Fixer le mur pendant %s minutes." ,
            "a new pillow": "un nouvel oreiller"           
        }

    >>> tasklist = [
            _("Order {item}.").format(item = _("a new pillow")),
            _("Take a nap") + '!', 
            _("Stare at the wall for %s minutes.") % 30
        ]

    >>> evalr(tasklist, translations.get)
    ['Commander un nouvel oreiller.', 'Faire une sieste!', 'Fixer le mur pendant 30 minutes.']

`evalr` walks python dictionaries, lists, tuples or sets and apply
a function to all the strings wrapped inside a `LazyString` object.

To apply a function to the strings inside a single expression, you can use the `eval` method:

.. code:: python

    >>> s = _("Take a nap") + '!'

    >>> s.eval(str.upper)
    'TAKE A NAP!'

    >>> s.eval(translations.get)
    'Faire une sieste!'

Or, again, the `evalr` function

.. code:: python

    >>> evalr(_("a new pillow").capitalize(), translations.get)
    'Un nouvel oreiller'


For most projects containing more than a few strings or languages, you'll probably want to 
use the gettext_ module to supply you with a translation function.

.. code:: python

    import gettext
    translation = gettext.translation("myproject", "./locale", ["fr"])
    translated_tasklist = evalr(tasklist, translation.ugettext)

GitHub repo: https://github.com/leforestier/postpone

.. _gettext: https://docs.python.org/3/library/gettext.html
