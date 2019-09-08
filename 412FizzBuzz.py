'''
使用哈希表保存数字的映射关系，之后遍历数字进行判断
空间复杂度O(1)，时间复杂度O(n)
'''


class Solution:
    def fizzBuzz(self, n: int) -> List[str]:
        fizz_buzz_dict = {3: 'Fizz', 5: 'Buzz'}
        res = []

        for num in range(1, n + 1):
            res_str = ''
            for key in fizz_buzz_dict.keys():
                if num % key == 0:
                    res_str += fizz_buzz_dict[key]
            if not res_str:
                res_str = str(num)
            res.append(res_str)

        return res
