# -*- coding:utf8 -*-


class DemoProjectInit:
    def init(self, is_init=False):
        if not is_init:
            return
        # 每次测试前先清除上次构造的数据
        self._deinit()
        # 初始化必要的数据，如在数据库中构建多种类型的账号，
        pass

    def _deinit(self):
        # 清除构造的数据
        pass
