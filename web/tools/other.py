import json
import ast


def generate_merge_intersect(dict):
    intersection = set(dict[next(iter(dict))])
    for key in dict:
        intersection &= set(dict[key])
    return list(intersection)


def generate_merge_union(dict):
    union = set(dict[next(iter(dict))])
    for key in dict:
        union |= set(dict[key])
    return list(union)


def format_json_string(jstr):
    jstr = jstr.replace("'", '"')
    data = json.loads(jstr)
    return json.dumps(data, indent=4, ensure_ascii=False)


def is_valid_list_format(s):
    try:
        result = ast.literal_eval(s)
        return isinstance(result, list)
    except (ValueError, SyntaxError):
        return False
