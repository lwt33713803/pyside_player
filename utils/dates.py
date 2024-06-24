import datetime

def convert_milliseconds_to_time(milliseconds):
    # 创建一个 timedelta 对象
    delta = datetime.timedelta(milliseconds=milliseconds)
    # 获取总秒数，并转换为时、分、秒、毫秒格式
    hours, remainder = divmod(delta.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = delta.microseconds // 1000
    # 返回格式化的字符串
    return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))