import pypeg2

from .formatter import format as _format
from .parser import Document
from .visitor import Visitor


def parse(document):
    tags, document = document.split('\n', 1)
    tags = [tag for tag in tags.split(' ') if tag]
    document = document.strip('\n')

    visitor = Visitor()
    res = pypeg2.parse(document, Document, whitespace=None)

    return {
        'tags': tags,
        'body': res.accept(visitor),
    }


def parse_without_tags(document):
    document = document.strip('\n')

    visitor = Visitor()
    res = pypeg2.parse(document, Document, whitespace=None)

    return res.accept(visitor)


def format(document):
    tags = ' '.join(document['tags'])
    content = _format(document['body'])
    return f'{tags}\n\n{content}'


def format_without_tags(document):
    return _format(document['body'])
