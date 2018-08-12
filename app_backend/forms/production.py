#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: production.py
@time: 2018-04-05 00:54
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, Length

from wtforms.widgets import HTMLString
from wtforms.compat import text_type, iteritems
from wtforms.widgets import html_params

from app_backend.api.production import get_production_row
from app_backend.models.bearing_project import Production
from app_common.maps.default import default_choice_option_str


class AddProductionModelRepeatValidate(object):
    """
    创建产品型号重复校验
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        condition = [
            Production.production_brand == form.production_brand.data.upper(),
            Production.production_model == field.data.upper(),
        ]
        row = get_production_row(*condition)
        if row:
            raise ValidationError(self.message or _('Data duplication'))


class EditProductionModelRepeatValidate(object):
    """
    编辑产品型号重复校验
    (编辑重复校验排除当前产品型号)
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        condition = [
            Production.production_brand == form.production_brand.data.upper(),
            Production.production_model == field.data.upper(),
        ]
        row = get_production_row(*condition)
        if row and row.id != form.id.data:
            raise ValidationError(self.message or _('Data duplication'))


class ProductionSearchForm(FlaskForm):
    """
    搜索表单
    """
    production_brand = SelectField(
        _('production brand'),
        validators=[],  # 字符类型，非必填
        default=default_choice_option_str,
        description=_('production brand'),
        render_kw={
            'rel': 'tooltip',
            'title': _('production brand'),
        }
    )
    production_model = StringField(
        _('production model'),
        validators=[],
        description=_('production model'),
        render_kw={
            'placeholder': _('production model'),
            'rel': 'tooltip',
            'title': _('production model'),
            'autocomplete': 'off',
        }
    )
    op = IntegerField(
        _('operation'),
        validators=[],
        default=0,
    )
    page = IntegerField(
        _('page'),
        validators=[],
        default=1,
    )


class ProductionAddForm(FlaskForm):
    """
    创建表单
    """
    production_brand = StringField(
        _('production brand'),
        validators=[
            DataRequired(),
        ],
        default='',
        description='产品品牌（例如：SKF、FAG、NSK...）',
        render_kw={
            'placeholder': _('production brand'),
            'rel': 'tooltip',
            'title': _('production brand'),
            'autocomplete': 'off',
        }
    )
    production_model = StringField(
        _('production model'),
        validators=[
            DataRequired(),
            AddProductionModelRepeatValidate(),
        ],
        default='',
        description='产品型号（例如：7008CEGA/HCP4A）',
        render_kw={
            'placeholder': _('production model'),
            'rel': 'tooltip',
            'title': _('production model'),
            'autocomplete': 'off',
        }
    )
    note = StringField(
        _('production note'),
        validators=[],
        default='',
        description='产品备注（例如：最小起订量12个）',
        render_kw={
            'placeholder': _('production note'),
            'rel': 'tooltip',
            'title': _('production note'),
            'autocomplete': 'off',
        }
    )


class ProductionEditForm(FlaskForm):
    """
    编辑表单
    """
    id = IntegerField(
        _('production id'),
        validators=[
            DataRequired(),
        ],
        render_kw={
            'type': 'hidden',
        }
    )
    production_brand = StringField(
        _('production brand'),
        validators=[
            DataRequired(),
            Length(min=2, max=16),
        ],
        description='产品品牌（例如：SKF、FAG、NSK...）',
        render_kw={
            'placeholder': _('production brand'),
            'rel': 'tooltip',
            'title': _('production brand'),
            'autocomplete': 'off',
        }
    )
    production_model = StringField(
        _('production model'),
        validators=[
            DataRequired(),
            EditProductionModelRepeatValidate(),
        ],
        description='产品型号（例如：7008CEGA/HCP4A）',
        render_kw={
            'placeholder': _('production model'),
            'rel': 'tooltip',
            'title': _('production model'),
            'autocomplete': 'off',
        }
    )
    note = StringField(
        _('production note'),
        validators=[],
        description='产品备注（例如：最小起订量12个）',
        render_kw={
            'placeholder': _('production note'),
            'rel': 'tooltip',
            'title': _('production note'),
            'autocomplete': 'off',
        }
    )
    create_time = DateField(
        _('create time'),
        validators=[],
        description=_('create time'),
    )
    update_time = DateField(
        _('update time'),
        validators=[],
        description=_('update time'),
    )


# class SelectProductionWidget(object):
#     """
#     自定义选择组件 - 产品
#     """
#     def __call__(self, field, **kwargs):
#         params = {
#             'id': field.id,
#             'name': field.id,
#             'class': 'selectpicker show-tick',
#             'data-live-search': 'true',
#             'title': kwargs.pop('title', 'Choose one of the following...'),
#             'data-header': kwargs.pop('data-header', 'Select a condiment'),
#         }
#         html = ['<select %s>' % html_params(**params)]
#         for _, area_data in field.choices:
#             for area_name, area_list in area_data.items():
#                 html.append('\t<optgroup label="%s">' % area_name)
#                 for country_data in area_list:
#                     # html.append('\t\t<option value="%s" data-subtext="%s(%s)">[%s] %s</option>' % (country_data['id'], country_data['name_c'], country_data['name_e'], country_data['short_code'], country_data['phone_pre']))
#                     html.append('\t\t<option value="%s" data-subtext="%s">[%s] %s</option>' % (country_data['id'], country_data['name_c'], country_data['short_code'], country_data['phone_pre']))
#                 html.append('\t</optgroup>')
#         html.append('</select>')
#         return HTMLString('\n'.join(html))
#
#
# class SelectProduction(SelectField):
#     """
#     自定义选择表单控件 - 产品
#     """
#     widget = SelectProductionWidget()
#
#     # def pre_validate(self, form):
#     #     """
#     #     校验表单传值是否合法
#     #     """
#     #     is_find = False
#     #     for _, area_data in self.choices:
#     #         for area_list in area_data.values():
#     #             if self.data in [str(i['id']) for i in area_list]:
#     #                 is_find = True
#     #                 break
#     #         if is_find:
#     #             break
#     #     else:
#     #         raise ValueError(self.gettext('Not a valid choice'))


class SelectProductionWidget(object):
    """
    自定义选择组件 - 产品选择
    """

    def __call__(self, field, **kwargs):
        params = {
            'id': field.id,
            'name': field.id,
            'class': 'selectpicker show-tick',
            'data-live-search': 'true',
            'data-live-search-placeholder': _('Type production model'),
            'title': kwargs.pop('placeholder', field.label),
            'data-header': kwargs.pop('data_header', field.label),
            'data-width': kwargs.pop('data_width', 'auto')
        }
        html = ['<select %s>' % html_params(**params)]
        for data_id, data_value, data_label, data_ext in field.choices:
            html.append('<option value="%s" data-subtext="[%s]" data-content=\'%s\'>%s</option>' % (
            data_id, data_ext, data_label, data_value))
        html.append('</select>')
        return HTMLString('\n'.join(html))


class SelectProductionField(SelectField):
    """
    自定义选择表单控件 - 产品选择
    """
    widget = SelectProductionWidget()

    def pre_validate(self, form):
        """
        校验表单传值是否合法
        """
        for v, _ in self.choices:
            if text_type(self.data) == text_type(v):
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))


class ProductionSelectForm(FlaskForm):
    production_model = SelectProductionField(
        _('production model'),
        validators=[
            DataRequired(),
        ],
        description='产品型号（例如：7008CEGA/HCP4A）',
        render_kw={
            'placeholder': _('production model'),
            'rel': 'tooltip',
            'title': _('production model'),
        }
    )
