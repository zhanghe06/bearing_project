#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: tpl_form.py
@time: 2018-07-18 14:09
"""


from __future__ import unicode_literals


CODE_TEMPLATE_FORM = '''
#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: %(section)s.py
@time: %(time)s
"""


from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from six import iteritems
from datetime import datetime, timedelta

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, DateTimeField, IntegerField, SelectField, DecimalField
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange, EqualTo, Email, ValidationError, IPAddress
from wtforms.fields import FieldList, FormField


class %(model)sSearchForm(FlaskForm):
    # TODO 完善筛选表单
    start_create_time = DateField(
        _('start time'),
        validators=[],
        default=datetime.utcnow() - timedelta(days=30),
        description=_('start time'),
        render_kw={
            'placeholder': _('start time'),
            'type': 'date',
            'rel': 'tooltip',
            'title': _('start time'),
        }
    )
    end_create_time = DateField(
        _('end time'),
        validators=[],
        default=datetime.utcnow(),
        description=_('end time'),
        render_kw={
            'placeholder': _('end time'),
            'type': 'date',
            'rel': 'tooltip',
            'title': _('end time'),
        }
    )
    op = IntegerField(
        _('operation'),
        validators=[],
        default=0,
    )


class %(model)sAddForm(FlaskForm):
    """
    创建表单（字段一般带有默认选项）
    """
    pass
    # TODO 完善创建表单


class %(model)sEditForm(FlaskForm):
    """
    编辑表单（字段默认选项需要去除）
    """
    id = IntegerField(
        _('customer id'),
        validators=[
            DataRequired(),
        ],
        render_kw={
            'type': 'hidden',
        }
    )
    create_time = DateField(
        _('create time'),
        validators=[DataRequired()],
        description=_('create time')
    )
    update_time = DateField(
        _('update time'),
        validators=[DataRequired()],
        description=_('update time')
    )
    # TODO 完善编辑表单
'''
