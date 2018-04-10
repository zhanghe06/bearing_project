#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py.py
@time: 2018-03-06 00:15
"""


from wtforms import SelectField, BooleanField
from wtforms.widgets import HTMLString
from wtforms.compat import text_type, iteritems
from wtforms.widgets import html_params


class SelectBSWidget(object):
    """
    自定义选择组件
    """
    def __call__(self, field, **kwargs):
        params = {
            'id': field.id,
            'name': field.id,
            'class': 'selectpicker show-tick',
            # 'data-live-search': 'true',
            'title': kwargs.pop('placeholder', 'Choose one of the following...'),
            'data-header': kwargs.pop('data_header', 'Select a condiment'),
            'data-width': kwargs.pop('data_width', 'auto')
        }
        html = ['<select %s>' % html_params(**params)]
        for k, v in field.choices:
            html.append('<option value="%s" data-subtext="[%s]">%s</option>' % (k, k, v))
        html.append('</select>')
        return HTMLString('\n'.join(html))


class SelectBS(SelectField):
    """
    自定义选择表单控件
    """
    widget = SelectBSWidget()

    def pre_validate(self, form):
        """
        校验表单传值是否合法
        """
        for v, _ in self.choices:
            # print self.data, v, type(self.data), type(v)
            if str(self.data) == str(v):
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))

