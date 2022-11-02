# -*- coding: utf-8 -*-
def get_tracks(distance, rate=0.6, t=0.2, v=0):
    """
    将distance分割成小段的距离
    :param distance: 总距离
    :param rate: 加速减速的临界比例
    :param a1: 加速度
    :param a2: 减速度
    :param t: 单位时间
    :param t: 初始速度
    :return: 小段的距离集合
    """
    tracks = []
    # 加速减速的临界值
    mid = rate * distance
    # 当前位移
    s = 0
    # 循环
    while s < distance:
        # 初始速度
        v0 = v
        if s < mid:
            a = 40
        else:
            a = -3
        # 计算当前t时间段走的距离
        s0 = v0 * t + 0.5 * a * t * t
        # 计算当前速度
        v = v0 + a * t
        # 四舍五入距离，因为像素没有小数
        tracks.append(round(s0))
        # 计算当前距离
        s += s0

    return tracks


print(get_tracks(260))