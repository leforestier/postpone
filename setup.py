from distutils.core import setup

with open('README.rst') as fd:
    long_description = fd.read()

setup(
    name='postpone',
    version='0.2.0',
    py_modules=['postpone'],
    author = 'Benjamin Le Forestier',
    author_email = 'benjamin@leforestier.org',
    url = 'https://github.com/leforestier/postpone',
    keywords = [
        "lazy", "string", "i18n", "internationalization", "translation", "translate", "gettext", "ugettext", 
        "delayed", "evaluation", "message", "strings", "web"],
    description = """\
A lazy string implementation that doesn't rely on a global or thread local state.""",
    long_description = long_description,
    classifiers = [
        'Environment :: Web Environment',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]  
)
