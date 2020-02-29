# -*- coding: utf-8 -*-

import os

class get_path:
    """统一文件获取入口
        pathName：文件目录的路径
        fileName：文件名称
    """
    def get_driPath(self,pathName,fileName):
        path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
        dirPath = os.path.join(path, pathName, fileName)
        return dirPath