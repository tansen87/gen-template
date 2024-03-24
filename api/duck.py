"""
Description: 使用duckdb来生成模板
usage: 调用window.pywebview.api.<methodname>(<parameters>)从Javascript执行
"""

import os
import json

import duckdb
import webview

from src_py.config.log import Log


class Duck:
    """ duck """
    window = None

    def system_py2js(self, func, info):
        ''' 调用js中挂载到window的函数 '''
        infoJson = json.dumps(info)
        Duck.window.evaluate_js(f"{func}('{infoJson}')")

    def system_open_file(self):
        ''' 打开文件 '''
        file_types = [
            'All files (*.*)',
            'CSV (*.csv;*.txt;*.dat;*.spec;*.tsv)',
            'Excel (*.xlsx;*.xlsb;*.xlsm)'
        ]
        directory = ''
        try:
            file_types = tuple(file_types)
            self.result = Duck.window.create_file_dialog(
                dialog_type=webview.OPEN_DIALOG, directory=directory, allow_multiple=True, file_types=file_types)
            file_type = os.path.splitext(self.result[0])[1].lower()
            print('test')
        except Exception as e:
            Log.error(repr(e))
    
    