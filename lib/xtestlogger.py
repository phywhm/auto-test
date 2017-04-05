#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging



#格式：\033[显示方式;前景色;背景色m
#显示方式：0（关闭所有效果），1（高亮），4（下划线），5（闪烁），7（反色），8（不可见）。
#前景色以3开头，背景色以4开头，具体颜色值有：0（黑色），1（红色），2（绿色），3（黄色），4（蓝色），5（紫色），6（青色），7（白色）。即前景绿色为32，背景蓝色为44。

COLOR_SCHEME = {"fore": {
    'black'    : 30,
    'red'      : 31,   #  红色
    'green'    : 32,   #  绿色
    'yellow'   : 33,   #  黄色
    'blue'     : 34,   #  蓝色
    'purple'   : 35,   #  紫红色
    'cyan'     : 36,   #  青蓝色
    'white'    : 37,   #  白色
    },
    'back':{
    'black'    : 40,
    'red'      : 41,   #  红色
    'green'    : 42,   #  绿色
    'yellow'   : 43,   #  黄色
    'blue'     : 44,   #  蓝色
    'purple'   : 45,   #  紫红色
    'cyan'     : 46,   #  青蓝色
    'white'    : 47,   #  白色
    },
    'mode': {'normal': 0,
    'bold'      : 1,   #  高亮显示
    'underline' : 4,   #  使用下划线
    'blink'     : 5,   #  闪烁
    'invert'    : 7,   #  反白显示
    'hide'      : 8,   #  不可见
    },
    'default' :
    {
        'end' : 0,
    },
}

info_style = "\033[%s;%sm" %(COLOR_SCHEME['mode']['bold'], COLOR_SCHEME['fore']['green'], )
debug_style = "\033[%s;%sm" %(COLOR_SCHEME['mode']['bold'], COLOR_SCHEME['fore']['cyan'])
warning_style = "\033[%s;%sm" %( COLOR_SCHEME['mode']['bold'], COLOR_SCHEME['fore']['yellow'])
error_style = "\033[%s;%sm" %(COLOR_SCHEME['mode']['bold'], COLOR_SCHEME['fore']['red'])
default = "\033[0m"


class ColorFilter(logging.Filter):
    def filter(self, record):
        print dir(record)
        return True

class ColorFormatter(logging.Formatter):
    def format(self, record):
        s = super(ColorFormatter, self).format(record)
        if record.levelno == 10:
            return debug_style + s + default
        elif record.levelno == 20:
            return info_style + s + default
        elif record.levelno == 30:
            return warning_style + s + default
        elif record.levelno in [40, 50]:
            return error_style + s + default
        else:
            return s

def get_logger(name, file_name = '/tmp/testrun.log', file_log_leve=logging.DEBUG, console_log_level=logging.ERROR):
    xx_formater = logging.Formatter(fmt='%(asctime)s [%(threadName)s] %(filename)s:%(lineno)d %(levelname)s %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(filename=file_name,
                                      mode='a',
                                      encoding='utf-8')
    file_handler.setLevel(file_log_leve)
    file_handler.setFormatter(xx_formater)
    logger.addHandler(file_handler)

    std_stream = logging.StreamHandler()
    color_formater = ColorFormatter(
        fmt='%(asctime)s [%(threadName)s] %(filename)s:%(lineno)d %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    std_stream.setFormatter(color_formater)
    std_stream.setLevel(console_log_level)
    #color_filter = ColorFilter()
    #std_stream.addFilter(color_filter)
    logger.addHandler(std_stream)
    return logger


