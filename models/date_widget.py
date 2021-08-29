__author__ = 'Jorgito'


def date_widget(f, v):
    wrapper = DIV()
    inp = SQLFORM.widgets.string.widget(f, v, _class="form-control")
    jqscr = SCRIPT(
        "jQuery(document).ready(function(){jQuery('#%s').datepicker({format: 'dd/mm/yyyy', language: 'es',});});" % inp[
            '_id'],
        _type="text/javascript")
    wrapper.components.extend([inp, jqscr])
    return wrapper
