import copy
import os

from jinja2 import Environment, FileSystemLoader


path = os.path.split(os.path.realpath(__file__))[0]


def _format_parameters(parameters, to_pop):
    tmp = copy.copy(parameters)
    if to_pop:
        tmp.pop(to_pop, None)

    res = []
    for key, value in tmp.items():
        if value is True:
            res.append(key)
        else:
            if '"' in value:
                res.append(key + "'" + value + "'")
            else:
                res.append(key + '"' + value + '"')

    return ' '.join(res)


def format_heading(heading):
    return ('#' * heading) + ' '


def list_has_parameters(parameters):
    return len(parameters.keys()) - 1 > 0


def list_format_parameters(parameters):
    return '    * !:' + _format_parameters(parameters, 'list') + '\n'


def get_list_indentation(in_list):
    return ('    ' * (in_list+1)) + '* '


def list_new_line(in_list):
    return in_list > 0


def table_has_parameters(parameters):
    return len(parameters.keys()) - 1 > 0


def table_format_parameters(parameters):
    return '| !:' + _format_parameters(parameters, 'table') + '\n'


def block_has_parameters(parameters):
    return len(parameters.keys()) - 1 > 0


def block_format_parameters(parameters):
    return ' !:' + _format_parameters(parameters, 'block')


def rawblock_has_parameters(parameters):
    return len(parameters.keys()) - 1 > 0


def rawblock_format_parameters(parameters):
    return ' !:' + _format_parameters(parameters, 'rawblock')


def inline_needs_formatting(parameters):
    # return len(parameters.keys()) - 1 > 0
    # return len(parameters.keys()) > 0
    if len(parameters.keys())  == 0:
        return False
    elif len(parameters.keys()) == 1:
        if list(parameters.keys())[0] == 'listitem':
            return False
        if list(parameters.keys())[0] == 'paragraph':
            return False
        if list(parameters.keys())[0] == 'inline':
            return False
    return True


def format_parameters(parameters):
    return _format_parameters(parameters, 'inline')


def newline(_):
    return '\n'


def escape_special(part, in_table):
    if in_table:
        part = part.replace('|', '\|')
    return part.replace('[', '\[').replace(']', '\]')


environment = Environment(loader=FileSystemLoader(searchpath=path+'/'))
environment.filters['format_heading'] = format_heading
environment.filters['list_has_parameters'] = list_has_parameters
environment.filters['list_format_parameters'] = list_format_parameters
environment.filters['get_list_indentation'] = get_list_indentation
environment.filters['list_new_line'] = list_new_line
environment.filters['table_has_parameters'] = table_has_parameters
environment.filters['table_format_parameters'] = table_format_parameters
environment.filters['block_has_parameters'] = block_has_parameters
environment.filters['block_format_parameters'] = block_format_parameters
environment.filters['rawblock_has_parameters'] = rawblock_has_parameters
environment.filters['rawblock_format_parameters'] = rawblock_format_parameters
environment.filters['inline_needs_formatting'] = inline_needs_formatting
environment.filters['format_parameters'] = format_parameters
environment.filters['newline'] = newline
environment.filters['escape_special'] = escape_special
template = environment.get_template('template.tmpl')


def format(document):
    return '\n\n'.join([template.render(meta=part) for part in document])
