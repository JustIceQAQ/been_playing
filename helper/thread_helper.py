import sys
import threading
import traceback

from helper.notify_helper import NotifyInit


class RuntimeThread(threading.Thread):
    def __init__(self, use_notify: NotifyInit, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.use_notify = use_notify
        self.thread_name = kwargs.get("name", None)

    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        except Exception as e:
            error_class = e.__class__.__name__  # 取得錯誤類型
            detail = e.args[0]  # 取得詳細內容
            cl, exc, tb = sys.exc_info()  # 取得Call Stack
            last_call_stack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
            file_name = last_call_stack[0]  # 取得發生的檔案名稱
            line_num = last_call_stack[1]  # 取得發生的行號
            func_name = last_call_stack[2]  # 取得發生的函數名稱

            err_msg = '[{}] File "{}", line {}, in {}: [{}] {}'.format(
                self.thread_name, file_name, line_num, func_name, error_class, detail
            )
            self.use_notify.send_message(err_msg)
        finally:
            del self._target, self._args, self._kwargs
