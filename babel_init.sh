#!/usr/bin/env bash

app_directory=${1:-app_backend}


echo "# 创建模板文件\n"
echo "pybabel extract -F babel.cfg -k lazy_gettext -o ${app_directory}/messages.pot .\n"
pybabel extract -F babel.cfg -k lazy_gettext -o ${app_directory}/messages.pot .


echo "# 创建翻译文件（注意translations在Flask项目目录下）"
echo "pybabel init -i ${app_directory}/messages.pot -d ${app_directory}/translations -l en"
pybabel init -i ${app_directory}/messages.pot -d ${app_directory}/translations -l en
echo "pybabel init -i ${app_directory}/messages.pot -d ${app_directory}/translations -l zh"
pybabel init -i ${app_directory}/messages.pot -d ${app_directory}/translations -l zh


echo "# 编辑翻译文件\n"
echo "# 编辑完成回车\n"
read edit_ok
echo ${edit_ok}


echo "# 编译翻译文件\n"
echo "pybabel compile -d ${app_directory}/translations\n"
pybabel compile -d ${app_directory}/translations
