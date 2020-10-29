import copy
import re

from .parser import Inline, HeadingText, Heading, Tag, Paragraph, \
                    ParagraphText, ListLineText, ListLine, List, \
                    TableCellText, TableCell, TableLine, Table, \
                    RawBlock, RawBlockLine, \
                    BlockText, BlockLine, Block, \
                    Part, NewLines, Document

space_indentation = re.compile('( {4})+')


def _create_list_body(list_lines):
    lines = []
    current_indentation = 0
    append_target = {0: lines}

    for line in list_lines:
        if line['indentation'] > current_indentation:
            tmp = {'body': [], 'parameters': {'list': True}}
            append_target[current_indentation][-1]['body'].append(tmp)
            append_target[line['indentation']] = tmp['body']
            current_indentation = line['indentation']
        elif line['indentation'] < current_indentation:
            current_indentation = line['indentation']

        tmp = copy.copy(line)
        del tmp['indentation']
        append_target[current_indentation].append(tmp)

    return lines


class MethodDispatcher(object):
    def __init__(self):
        self.methods = {}

    def __call__(self, argument_type):
        def decorator(func):
            def call(visitor_self, arg, *args, **kwargs):
                for option in [Inline, HeadingText, Heading, Tag, Paragraph,
                               ParagraphText, ListLineText, ListLine, List,
                               TableCellText, TableCell, TableLine, Table,
                               RawBlock, RawBlockLine,
                               BlockText, BlockLine, Block,
                               Part, NewLines, Document]:
                    if isinstance(arg, option):
                        return self.methods[option](visitor_self, arg,
                                                    *args, **kwargs)
            self.methods[argument_type] = func
            return call

        return decorator


class Visitor(object):
    dispatch = MethodDispatcher()

    def __init__(self):
        self.excludes_inline = set(['mathinline'])

    @dispatch(Tag)  # noqa
    def visit(self, nullary, tags):
        try:
            return {nullary.tag: nullary.value}
        except AttributeError:
            return {nullary.tag: True}

    @dispatch(Inline)   # noqa
    def visit(self, nullary, tags):
        parameters = {key: value for d in tags for key, value in d.items()}
        # parameters.update({'inline': True})
        if not self.excludes_inline.intersection(set(parameters.keys())):
            parameters.update({'inline': True})

        content = nullary.content.replace(r'\[', '[').replace(r'\]', ']')
        return {'parameters': parameters, 'body': [content]}

    @dispatch(HeadingText)  # noqa
    def visit(self, nullary, tags):
        return nullary.content.replace(r'\[', '[').replace(r'\]', ']')

    @dispatch(Heading)  # noqa
    def visit(self, nary, tags, content):
        return {'parameters': {'heading': len(nary.heading)},
                'body': content}

    @dispatch(ParagraphText)    # noqa
    def visit(self, nullary, tags):
        return nullary.content.replace(r'\[', '[').replace(r'\]', ']')

    @dispatch(Paragraph)    # noqa
    def visit(self, nary, tags, content):
        return {'parameters': {'paragraph': True}, 'body': content}

    @dispatch(ListLineText) # noqa
    def visit(self, nullary, tags):
        return nullary.content.replace(r'\[', '[').replace(r'\]', ']')

    @dispatch(ListLine) # noqa
    def visit(self, nary, tags, content):
        if space_indentation.match(nary.indentation):
            indentation = (len(nary.indentation) / 4) - 1
        else:
            indentation = len(nary.indentation) - 1

        return {'parameters': {'listitem': True}, 'body': content,
                'indentation': indentation}

    @dispatch(List) # noqa
    def visit(self, nary, tags, content):
        parameters = {key: value for d in tags for key, value in d.items()}
        parameters.update({'list': True})

        body = _create_list_body(content)

        return {'parameters': parameters, 'body': body}

    @dispatch(TableCellText)    # noqa
    def visit(self, nullary, tags):
        return (nullary.content.replace(r'\[', '[')
                               .replace(r'\]', ']')
                               .replace(r'\|', '|'))

    @dispatch(TableCell)    # noqa
    def visit(self, nary, tags, content):
        # return content TODO
        return {'parameters': {'tablecell': True}, 'body': content}

    @dispatch(TableLine)    # noqa
    def visit(self, nary, tags, content):
        # return content TODO
        return {'parameters': {'tablerow': True}, 'body': content}

    @dispatch(Table)    # noqa
    def visit(self, nary, tags, content):
        parameters = {key: value for d in tags for key, value in d.items()}
        parameters.update({'table': True})

        del content[0]['parameters']['tablerow']
        content[0]['parameters']['tablehead'] = True

        return {'parameters': parameters, 'body': content}

    @dispatch(RawBlockLine) # noqa
    def visit(self, nullary, tags):
        return nullary.content

    @dispatch(RawBlock) # noqa
    def visit(self, nary, tags, content):
        parameters = {key: value for d in tags for key, value in d.items()}
        parameters.update({'rawblock': True})

        return {'parameters': parameters,
                'body': [''.join(content).strip('\n')]}

    @dispatch(BlockText)    # noqa
    def visit(self, nullary, tags):
        return nullary.content

    @dispatch(BlockLine)    # noqa
    def visit(self, nary, tags, content):
        return {'parameters': {'inline': True}, 'body': content}

    @dispatch(Block)    # noqa
    def visit(self, nary, tags, content):
        parameters = {key: value for d in tags for key, value in d.items()}
        parameters.update({'block': True})

        return {'parameters': parameters, 'body': content}

    @dispatch(Part) # noqa
    def visit(self, nullary, tags):
        return nullary.content.accept(self)

    @dispatch(NewLines) # noqa
    def visit(self, nullary, tags):
        return None

    @dispatch(Document) # noqa
    def visit(self, nary, tags, content):
        return [x for x in content if x]
