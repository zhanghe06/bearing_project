#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: system.py
@time: 2018-04-12 10:32
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import FileField


class CatalogueUploadForm(FlaskForm):
    file = FileField(
        _('catalogue'),
        validators=[],
        description=_('catalogue'),
        render_kw={
            'rel': 'tooltip',
            'title': _('catalogue'),
        }
    )


class ProductionUploadForm(FlaskForm):
    file = FileField(
        _('production'),
        validators=[],
        description=_('production'),
        render_kw={
            'rel': 'tooltip',
            'title': _('production'),
        }
    )


class QuotationUploadForm(FlaskForm):
    file = FileField(
        _('quotation'),
        validators=[],
        description=_('quotation'),
        render_kw={
            'rel': 'tooltip',
            'title': _('quotation'),
        }
    )
