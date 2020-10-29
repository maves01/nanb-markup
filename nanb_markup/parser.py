import re

from pypeg2 import attr, optional, some, maybe_some, ignore


r_inline = r'([^\n\[\]]|(?<=\\)[\[\]])*'
"""Inside an `Inline` match everything that is not a newline or square brackets
unless they are proceeded by a backslash"""

r_line = r'([^\n\[\]]|(?<=\\)[\[\]])+'
"""Match everything that is not a newline or square brackets unless they are
proceeded by a backslash. Also don't match anything inside square brackets."""

r_paragraph_condition = r'(^(?!(\t+\*|( {4})+\*|\||``(?!`)|````(?!`))))'
"""This is a match of length 0. It simply checks if the given block starts
like one of the other patterns."""

r_paragraph = r'([^\n\[\]]|(?<=\\)[\[\]]|(?<!\n)\n(?!\n))+'
"""Same as `r_line` but also matches \n that are not followed or preceeded bytearray
another \n."""

r_list_condition = r'(^(?=(\t+|( {4})+)\*))'
"""Checks the condition of the start of a list."""

r_table_line = r'([^\n\[\]\|]|(?<=\\)[\[\]\|])+'
"""Same as `r_line` but don't match |."""

r_table_line_condition = r'(^(?=\|.*\|$))'

r_rawblock_line_condition = r'(^(?!```$))'

r_block_line_condition = r'(^(?!````$))'

"""The `*_condition` regex are simply used to check if a block/line qualifies.
They are 0 length matches."""


class Nullary(object):
    def accept(self, visitor):
        tags = []
        if hasattr(self, 'tags'):
            tags = [x.accept(visitor) for x in self.tags]

        return visitor.visit(self, tags)


class Nary(object):
    def accept(self, visitor):
        tags = []
        if hasattr(self, 'tags'):
            tags = [x.accept(visitor) for x in self.tags]

        return visitor.visit(self, tags,
                             [x.accept(visitor) for x in self.content])


class Tag(Nullary):
    grammar = (
        attr('tag', re.compile(r'\w+', re.M)),
        optional(
            [(
                '"',
                attr('value', re.compile(r'[^"]*')),
                '"'
            ),
            (
                "'",
                attr('value', re.compile(r"[^']*")),
                "'",
            )]
        )
    )


class Inline(Nullary):
    grammar = (
        '[',
        attr('tags', some([' ', Tag])),
        ']',
        '[',
        attr('content', re.compile(r_inline, re.M)),
        ']',
    )


class ParagraphText(Nullary):
    grammar = attr('content', re.compile(r_paragraph, re.M))


class Paragraph(Nary):
    # Candidate: ^(?!(```|````|\t+\*|( {4})+\*|\|))
    # This way, the regex only need to not match [, ] and consecutive \n
    grammar = (
        ignore(re.compile(r_paragraph_condition, re.M)),
        attr('content', some([Inline, ParagraphText]))
    )


class ListLineText(Nullary):
    grammar = attr('content', re.compile(r_line, re.M))


class ListLine(Nary):
    grammar = (
        attr('indentation', re.compile(r'^(\t| {4})+', re.M)),
        ignore(re.compile(r'\* *', re.M)),
        attr('content', some([Inline, ListLineText])),
    )


class List(Nary):
    grammar = (
        ignore(re.compile(r_list_condition, re.M)),
        optional(
            ignore(re.compile(r'^(\t| {4})+\*[ \t]*!:', re.M)),
            attr('tags', some([' ', Tag])),
            '\n'
        ),
        attr('content', (ListLine, maybe_some('\n', ListLine)))
    )


class TableCellText(Nullary):
    grammar = attr('content', re.compile(r_table_line, re.M))


class TableCell(Nary):
    grammar = attr('content', some([Inline, TableCellText]))


class TableLine(Nary):
    grammar = (
        ignore(re.compile(r_table_line_condition, re.M)),
        attr('content', some(['|', TableCell]))
    )


class Table(Nary):
    grammar = (
        optional(
            ignore(re.compile(r'^\|[ \t]*!:', re.M)),
            attr('tags', some([' ', Tag])),
            '\n'
        ),
        attr('content', (TableLine, maybe_some('\n', TableLine))),
    )


class RawBlockLine(Nullary):
    grammar = (
        ignore(re.compile(r_rawblock_line_condition, re.M)),
        attr('content', re.compile(r'^.*\n', re.M))
    )


class RawBlock(Nary):
    grammar = (
        [
            ignore(re.compile('^```$', re.M)),
            (
                ignore(re.compile('^```[ \t]*!:', re.M)),
                attr('tags', some([' ', Tag])),
            )
        ],
        attr('content', maybe_some(RawBlockLine)),
        ignore(re.compile('^```$', re.M)),
    )


class BlockText(Nullary):
    grammar = attr('content', re.compile(r_line, re.M))


class BlockLine(Nary):
    grammar = (
        ignore(re.compile(r_block_line_condition, re.M)),
        attr('content', some([Inline, BlockText]))
    )


class Block(Nary):
    grammar = (
        [
            ignore(re.compile('^````$', re.M)),
            (
                ignore(re.compile('^````[ \t]*!:', re.M)),
                attr('tags', some([' ', Tag])),
            )
        ],
        attr('content', some(['\n', BlockLine])),  # NOTE: it's ok for a block to eat newlines
        ignore(re.compile('^````$', re.M)),
    )


class HeadingText(Nullary):
    grammar = attr('content', re.compile(r_line, re.M))


class Heading(Nary):
    grammar = (
        attr('heading', re.compile(r'#+', re.M)),
        ignore(re.compile(' *', re.M)),
        attr('content', some([Inline, HeadingText]))
    )


class Part(Nullary):
    grammar = attr('content', [
        List, Table, RawBlock, Block, Heading, Paragraph
    ])


class NewLines(Nullary):
    grammar = attr('foo', re.compile('\n\n+'))


class Document(Nary):
    grammar = attr('content', maybe_some([Part, NewLines]))

