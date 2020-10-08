#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py
@time: 2018-03-06 00:15
"""

from __future__ import unicode_literals

from wtforms import SelectField, BooleanField
from wtforms.compat import text_type
from wtforms.widgets import HTMLString
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
            'data-live-search': 'true',
            'data-live-search-placeholder': field.label.text,
            'title': kwargs.pop('placeholder', field.label.text),
            'data-header': kwargs.pop('data_header', field.label.text),
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
            if text_type(self.data) == text_type(v):
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))


class CheckBoxBSWidget(object):
    """
    自定义复选框组件
    """
    input_type = 'checkbox'

    def __call__(self, field, **kwargs):
        if getattr(field, 'checked', field.data):
            kwargs['checked'] = True
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        if 'value' not in kwargs:
            kwargs['value'] = 1
        html = [
            '<div class="checkbox">',
            '<label>',
            '<input %s>' % html_params(name=field.name, **kwargs),
            '</label>',
            '</div>'
        ]
        return HTMLString('\n'.join(html))


class CheckBoxBS(BooleanField):
    """
    自定义复选框控件
    """
    widget = CheckBoxBSWidget()
