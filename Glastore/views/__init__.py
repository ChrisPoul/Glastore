from flask import request


def get_form(heads):
    form = {}
    for head in heads:
        try:
            form[head] = request.form[head]
        except KeyError:
            form[head] = ""

    return form