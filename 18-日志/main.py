import traceback

from log import log
from test import test_fun
from util.util_file import util_fun


def my_function():
    log.debug("这是一个调试级别的日志")
    log.info("这是一个信息级别的日志")
    log.warning("这是一个警告级别的日志")
    log.error("这是一个错误级别的日志")


def error_function():
    try:
        result = 1 / 0
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())


if __name__ == "__main__":
    log.info('start')

    my_function()
    error_function()

    test_fun()

    util_fun()
