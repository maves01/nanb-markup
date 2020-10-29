import pypeg2

import nanb_markup as nm


def test_paragraph_1():
    text = 'This is a single line test.'

    res = pypeg2.parse(text, nm.parser.Paragraph, whitespace=None)

    assert len(res.content) == 1
    assert res.content[0].content == text


def test_paragraph_2():
    text = 'This is a more [bold][complicated] test.'

    res = pypeg2.parse(text, nm.parser.Paragraph, whitespace=None)

    assert len(res.content) == 3
    assert res.content[0].content == 'This is a more '
    assert res.content[1].content == 'complicated'
    assert res.content[2].content == ' test.'


def test_paragraph_3():
    text = 'This is a more [bold][stupid]| test.'

    res = pypeg2.parse(text, nm.parser.Paragraph, whitespace=None)

    assert len(res.content) == 3
    assert res.content[0].content == 'This is a more '
    assert res.content[1].content == 'stupid'
    assert res.content[2].content == '| test.'

def test_paragraph_4():
    text = 'This is a more [bold][stupid]    * test.'

    res = pypeg2.parse(text, nm.parser.Paragraph, whitespace=None)

    assert len(res.content) == 3
    assert res.content[0].content == 'This is a more '
    assert res.content[1].content == 'stupid'
    assert res.content[2].content == '    * test.'


def test_paragraph_5():
    text = 'This is a more [bold][stupid]     test.'

    res = pypeg2.parse(text, nm.parser.Paragraph, whitespace=None)

    assert len(res.content) == 3
    assert res.content[0].content == 'This is a more '
    assert res.content[1].content == 'stupid'
    assert res.content[2].content == '     test.'

def test_paragraph_6():
    text = 'This is a mutline\nparagraph test.'

    res = pypeg2.parse(text, nm.parser.Paragraph, whitespace=None)

    assert len(res.content) == 1
    assert res.content[0].content == text

def test_paragraph_7():
    text = 'This is a [bold][fancy] mutline\nparagraph [bold][test].'

    res = pypeg2.parse(text, nm.parser.Paragraph, whitespace=None)

    assert len(res.content) == 5
    assert res.content[0].content == 'This is a '
    assert res.content[1].content == 'fancy'
    assert res.content[2].content == ' mutline\nparagraph '
    assert res.content[3].content == 'test'
    assert res.content[4].content == '.'

def test_paragraph_8():
    text = '[bold][foo] bar baz'

    res = pypeg2.parse(text, nm.parser.Paragraph, whitespace=None)

    assert len(res.content) == 2
    assert res.content[0].content == 'foo'
    assert res.content[1].content == ' bar baz'


def test_paragraph_9():
    text = 'foo [bold][bar] baz'

    res = pypeg2.parse(text, nm.parser.Paragraph, whitespace=None)

    assert len(res.content) == 3
    assert res.content[0].content == 'foo '
    assert res.content[1].content == 'bar'
    assert res.content[2].content == ' baz'


def test_paragraph_10():
    text = 'foo bar [bold][baz]'

    res = pypeg2.parse(text, nm.parser.Paragraph, whitespace=None)

    assert len(res.content) == 2
    assert res.content[0].content == 'foo bar '
    assert res.content[1].content == 'baz'


def test_list_1():
    text = '    * Line 1\n    * Line 2\n    * Line 3'

    res = pypeg2.parse(text, nm.parser.List, whitespace=None)

    assert len(res.content) == 3

def test_list_2():
    text = '    * !:tag\n    * Line 1\n    * Line 2\n    * Line 3'

    res = pypeg2.parse(text, nm.parser.List, whitespace=None)

    assert len(res.tags) == 1
    assert len(res.content) == 3


def test_rawblock_1():
    text = '```\nThis is a rawblock\n```'

    res = pypeg2.parse(text, nm.parser.RawBlock, whitespace=None)

    res = res.accept(nm.visitor.Visitor())

    assert len(res['body']) == 1
    assert res['body'][0] == 'This is a rawblock'


def test_rawblock_2():
    text = '``` !:code"python"\nThis is a rawblock\n```'

    res = pypeg2.parse(text, nm.parser.RawBlock, whitespace=None)

    res = res.accept(nm.visitor.Visitor())

    assert len(res['body']) == 1
    assert res['body'][0] == 'This is a rawblock'


def test_block_1():
    text = '````\nThis is a block\n````'

    res = pypeg2.parse(text, nm.parser.Block, whitespace=None)

    assert len(res.content) == 1
    assert len(res.content[0].content) == 1
    assert res.content[0].content[0].content == 'This is a block'


def test_block_2():
    text = '````\nThis is a block\nThis is another line\n````'

    res = pypeg2.parse(text, nm.parser.Block, whitespace=None)

    assert len(res.content) == 2
    assert len(res.content[0].content) == 1
    assert res.content[0].content[0].content == 'This is a block'
    assert len(res.content[1].content) == 1
    assert res.content[1].content[0].content == 'This is another line'


def test_block_3():
    text = '````\nThis is a [bold][fancy] block\nThis is another line\n````'

    res = pypeg2.parse(text, nm.parser.Block, whitespace=None)

    assert len(res.content) == 2
    assert len(res.content[0].content) == 3
    assert res.content[0].content[0].content == 'This is a '
    assert res.content[0].content[1].content == 'fancy'
    assert res.content[0].content[2].content == ' block'
    assert len(res.content[1].content) == 1
    assert res.content[1].content[0].content == 'This is another line'


def test_block_4():
    text = '```` !:tag\nThis is a block\n````'

    res = pypeg2.parse(text, nm.parser.Block, whitespace=None)

    assert len(res.tags) == 1
    assert len(res.content) == 1
    assert len(res.content[0].content) == 1
    assert res.content[0].content[0].content == 'This is a block'


def test_table_1():
    text = '|foo|bar|baz|\n|banana|apple|mango|'

    res = pypeg2.parse(text, nm.parser.Table, whitespace=None)

    assert len(res.content) == 2
    assert len(res.content[0].content) == 3
    assert len(res.content[0].content[0].content) == 1
    assert res.content[0].content[0].content[0].content == 'foo'
    assert res.content[0].content[1].content[0].content == 'bar'
    assert res.content[0].content[2].content[0].content == 'baz'

    assert res.content[1].content[0].content[0].content == 'banana'
    assert res.content[1].content[1].content[0].content == 'apple'
    assert res.content[1].content[2].content[0].content == 'mango'


def test_table_2():
    text = '| !:tag\n|foo|bar|baz|\n|banana|apple|mango|'

    res = pypeg2.parse(text, nm.parser.Table, whitespace=None)

    assert len(res.tags) == 1
    assert len(res.content) == 2
