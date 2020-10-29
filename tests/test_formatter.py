import pytest


import nanb_markup as nm


@pytest.mark.parametrize(
    "text",
    [
        'foo\n\nThis is a single line test.',
        'foo\n\nThis is a more [bold][complicated] test.',
        'foo\n\nThis is a more [bold][stupid]| test.',
        'foo\n\nThis is a more [bold][stupid]    * test.',
        'foo\n\nThis is a more [bold][stupid]     test.',
        'foo\n\nThis is a mutline\nparagraph test.',
        'foo\n\nThis is a [bold][fancy] mutline\nparagraph [bold][test].',
        'foo\n\n[bold][foo] bar baz',
        'foo\n\nfoo [bold][bar] baz',
        'foo\n\nfoo bar [bold][baz]',
        'foo\n\n    * Line 1\n    * Line 2\n    * Line 3',
        'foo\n\n    * !:tag\n    * Line 1\n    * Line 2\n    * Line 3',
        'foo\n\n```\nThis is a rawblock\n```',
        'foo\n\n``` !:code"python"\nThis is a rawblock\n```',
        'foo\n\n````\nThis is a block\n````',
        'foo\n\n````\nThis is a block\nThis is another line\n````',
        'foo\n\n````\nThis is a [bold][fancy] block\nThis is another line\n````',
        'foo\n\n```` !:tag\nThis is a block\n````',
        'foo\n\n|foo|bar|baz|\n|banana|apple|mango|',
        'foo\n\n| !:tag\n|foo|bar|baz|\n|banana|apple|mango|',
    ],
)
def test_formatter(text):
    assert nm.format(nm.parse(text)) == text
