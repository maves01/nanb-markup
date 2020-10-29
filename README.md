# nanb-markup

A markdown inspired markup language allowing for

* Headers
* Paragraphs
* Emphasis
* Lists
* Tables
* Raw Blocks
* Code Blocks
* Math Blocks
* Inline Math

## Usage

```python
import nanb_markup as nm
doc = nm.parse_without_tags("#Hello, World!\n\nFoo Bar Baz")
```

`nm.parse*` returns a list of dictionaries, which can contain other dictionaries in their bodies, like: 

    [{'parameters': {'heading': 1}, 'body': ['Hello, World!']},
     {'parameters': {'paragraph': True},
      'body': ['A ',
       {'parameters': {'bold': True, 'inline': True}, 'body': ['simple']},
       ' test']}]

## Example Syntax

    # Heading1

    ## Heading2

    This is a normal paragraph.

    This is a [bold][special] paragraph with some math: [mathinline][\sum_{i=0}^{N}i]

    Here is a list:

        * List Item 1
        * List Item 2

    Here is a table:

    |c1|c2|c3|
    |c1|c2|c3|

    ```
    This is a raw block
    ```

    ``` !:math
    \sum_{i=0}^{N}i = \frac{N(N+1)}{2}
    ```

    ``` !:code"python"
    print("Hello, World!")
    ```
