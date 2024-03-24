"""
Description: 业务层API,供前端JS调用
usage: 在Javascript中调用window.pywebview.api.<methodname>(<parameters>)
"""

from api.panda import Panda
from api.duck import Duck


class API(Panda, Duck):
    """ 业务层API,供前端JS调用 """

    def setWindow(self, window):
        """ 获取窗口实例 """
        Panda.window = window
