#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File Name: AB_test.py
@Create Time: 2019-08-24 10:37
@Author: wangyutian
@Version: 1.0
@Python Version: Python 3.6.4
@Modify Time: 2019-08-24 10:37
'''

from scipy.stats import norm
import math


class Sample:
    '''
    计算样本量
    https://www.abtasty.com/sample-size-calculator/
    '''

    def sample_size_u(self, u: float, s: float, a: float = 0.05, b: float = 0.2) -> int:
        '''
        已知双样本(A/B)均数，求实验样本量
        :param a: alpha
        :param b: beta
        :param u: 均值的差值
        :param s: 经验标准差
        :return: 样本量
        '''
        n = 2 * pow(((norm.ppf(1 - a / 2) + norm.ppf(1 - b)) / (u / s)), 2)
        return math.ceil(n)

    def sample_size_p(self, p1: float, p2: float, a: float = 0.05, b: float = 0.2) -> int:
        '''
        已知双样本(A/B)频数，求实验样本量
        :param a: alpha
        :param b: beta
        :param p1: 样本的频数，例如点击率50%，次日留存率80%
        :param p2: 样本的频数
        :return: 样本量
        '''
        n = pow((norm.ppf(1 - a / 2) + norm.ppf(1 - b)) / (p1 - p2), 2) * (p1 * (1 - p1) + p2 * (1 - p2))
        return math.ceil(n)


class ABtest_u():
    '''
    双样本双尾均值检验
    '''

    def __init__(self, x1: float, x2: float, s1: float, s2: float, n1: int, n2: int, a: float = 0.05, b: float = 0.2):
        self.x1 = x1  # 对照组均值
        self.x2 = x2  # 测试组均值
        self.s1 = s1  # 对照组标准差
        self.s2 = s2  # 测试组标准差
        self.n1 = n1  # 对照组样本量
        self.n2 = n2  # 测试组样本量
        self.a = a  # alpha
        self.b = b  # beta

    def significance_u(self) -> (int, float, float):
        '''
        双样本双尾均值显著性检验
        '''
        z = (self.x1 - self.x2) / pow(self.s1 ** 2 / self.n1 + self.s2 ** 2 / self.n2, 1 / 2)
        if z > 0:
            p = (1 - norm.cdf(z)) * 2
            if p < self.a:  # 拒绝原假设，接受备选假设
                f = 1
            else:  # 接受原假设
                f = 0
        else:
            p = 2 * norm.cdf(z)
            if p < self.a:  # 拒绝原假设，接受备选假设
                f = 1
            else:  # 接受原假设
                f = 0
        return f, format(z, '.2f'), format(p, '.2f')

    def confidence_u(self) -> tuple:
        '''
        双样本均值置信区间
        '''
        d = norm.ppf(1 - self.a / 2) * pow(self.s1 ** 2 / self.n1 + self.s2 ** 2 / self.n2, 1 / 2)
        floor = self.x1 - self.x2 - d
        ceil = self.x1 - self.x2 + d
        return (format(floor, '.2f'), format(ceil, '.2f'))

    def power_u(self) -> float:
        '''
        双样本均数功效
        '''
        z = abs(self.x1 - self.x2) / pow(self.s1 ** 2 / self.n1 + self.s2 ** 2 / self.n2, 1 / 2) - norm.ppf(
            1 - self.a / 2)
        b = 1 - norm.cdf(z)
        power = 1 - b
        return format(power, '.2%')

    def main(self):
        f, z, p = self.significance_u()
        ci = self.confidence_u()
        power = self.power_u()
        print(f'保留组均值：{self.x1}')
        print(f'测试组均值：{self.x2}')
        print('是否显著：' + ('统计效果不显著，拒绝原假设' if f == 1 else '统计效果显著，不能拒绝原假设'))
        print(f'变化度：' + format((self.x2 - self.x1) / self.x1, '.2%'))
        print(f'置信区间：{ci}')
        print(f'p-value：{p}')
        print(f'功效：{power}')


class ABtest_p():
    '''
    双样本双尾频数检验
    '''

    def __init__(self, p1: float, p2: float, n1: int, n2: int, a: float = 0.05, b: float = 0.2):
        self.p1 = p1
        self.p2 = p2
        self.n1 = n1
        self.n2 = n2
        self.a = a
        self.b = b

    def significance_p(self) -> (int, float, float):
        '''
        双样本双尾频数显著性检验
        '''
        p_pool = (self.n1 * self.p1 + self.n2 * self.p2) / (self.n1 + self.n2)

        z = (self.p1 - self.p2) / pow(p_pool * (1 - p_pool) * (1 / self.n1 + 1 / self.n2), 1 / 2)

        if z > 0:
            p = (1 - norm.cdf(z)) * 2
            if p < self.a:  # 拒绝原假设，接受备选假设
                f = 1
            else:  # 接受原假设
                f = 0
        else:
            p = 2 * norm.cdf(z)
            if p < self.a:  # 拒绝原假设，接受备选假设
                f = 1
            else:  # 接受原假设
                f = 0
        return f, format(z, '.2f'), format(p, '.2f')

    def confidence_p(self) -> tuple:
        '''
        双样本频数置信区间
        '''
        d = norm.ppf(1 - self.a / 2) * pow(self.p1 * (1 - self.p1) / self.n1 + self.p2 * (1 - self.p2) / self.n2, 1 / 2)
        floor = self.p1 - self.p2 - d
        ceil = self.p1 - self.p2 + d
        return (format(floor, '.2%'), format(ceil, '.2%'))

    def power_p(self) -> float:
        '''
        双样本频数功效
        '''
        z = abs(self.p1 - self.p2) / pow(self.p1 * (1 - self.p1) / self.n1 + self.p2 * (1 - self.p2) / self.n2,
                                         1 / 2) - norm.ppf(1 - self.a / 2)
        b = 1 - norm.cdf(z)
        power = 1 - b
        return format(power, '.2%')

    def main(self):
        f, z, p = self.significance_p()
        ci = self.confidence_p()
        power = self.power_p()
        print(f'保留组均值：{self.p1}')
        print(f'测试组均值：{self.p2}')
        print('是否显著：' + ('统计效果不显著，拒绝原假设' if f == 1 else '统计效果显著，不能拒绝原假设'))
        print(f'变化度：' + format((self.p2 - self.p1) / self.p1, '.2%'))
        print(f'置信区间：{ci}')
        print(f'p-value：{p}')
        print(f'功效：{power}')


if __name__ == '__main__':
    # 计算样本量
    # sample = Sample()
    #
    # n1 = sample.sample_size_p(p1=0.13, p2=0.14)
    # print(n1)
    #
    # n2 = sample.sample_size_u(u=1, s=38)
    # print(n2)

    # 双样本双尾均值检验
    # test1 = ABtest_u(x1=54.29, x2=54.50, s1=49.31, s2=48.89, n1=32058, n2=34515)
    # test1.main()

    # 双样本双尾频数检验
    # test2 = ABtest_p(p1=0.6488, p2=0.6530, n1=14667, n2=14193)
    # test2.main()

    test1 = ABtest_u(x1=5.08, x2=8.04, s1=2.06, s2=2.39, n1=32058, n2=34515)
    test1.main()
