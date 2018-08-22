#!/usr/bin/env bash

app_directory=${1:-app_backend}

echo "# 编译翻译文件\n"
echo "pybabel compile -d ${app_directory}/translations\n"
pybabel compile -d ${app_directory}/translations
