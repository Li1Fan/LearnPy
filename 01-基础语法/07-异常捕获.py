# -*- coding: utf-8 -*-
import sys
import traceback


def my_excepthook(exc_type, exc_value, tb):
    msg = ' Traceback (most recent call last):\n'
    while tb:
        filename = tb.tb_frame.f_code.co_filename
        name = tb.tb_frame.f_code.co_name
        lineno = tb.tb_lineno
        msg += '   File "%.500s", line %d, in %.500s\n' % (filename, lineno, name)
        tb = tb.tb_next
    msg += ' %s: %s\n' % (exc_type.__name__, exc_value)
    print(f'msg:{msg}')
    # log.error('\n' + msg)
    # if info_widget:
    #     info_widget.error_pysignal.emit(msg)


def fun_error():
    print(a)


if __name__ == '__main__':
    try:
        fun_error()
    except Exception as e:
        print(e)
        # traceback.print_exc()
        print(traceback.format_exc())

    sys.excepthook = my_excepthook
    fun_error()
