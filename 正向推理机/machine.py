#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
正向链的策略是寻找出前提可以同数据库中的事实或断言相匹配的那些规则，并运用冲突的消除策略，
从这些都可满足的规则中挑选出一个执行，从而改变原来数据库的内容。这样反复地进行寻找，
直到数据库的事实与目标一致即找到解答，或者到没有规则可以与之匹配时才停止。
"""

import collections

rules = collections.OrderedDict()


# 加载规则
def load_rule(path):
    P_list = []
    Q_list = []
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line:
                pro = line.strip().split(' ')
                P_list.append(pro[:-1])
                Q_list.append(pro[-1])
    return P_list, Q_list


# 添加规则
def add_rule(k, v):
    if tuple(k) in rules.keys():
        print('特征已在数据库')
    else:
        rules[tuple(k)] = v
        print('特征成功添加 >>> %s ----> %s' % (k, v))


# 删除规则
def del_rule(k):
    if tuple(k) in rules.keys():
        rules.pop(tuple(k))
        print('特征成功删除 >>> %s' % k)
    else:
        print('特征不在数据库')


# 正向推理机
def infer(facts):
    visited = []
    flag = False
    ending = False

    while not ending:
        for key in rules.keys():
            if list_in_set(key, facts) and key not in visited:
                facts.append(rules[key])
                visited.append(key)
                print('{key} ----> {value}'.format(key=key, value=facts[-1]))
                flag = True
                break
            if key == list(rules.keys())[-1]:  # 推理结束
                ending = True

    if flag:
        print('最终推出 ----> %s' % facts[-1])
    else:
        print('无法推出')


# 判断list中所有元素是否都在集合set中
def list_in_set(list, set):
    for i in list:
        if i not in set:
            return False
    return True


if __name__ == '__main__':
    P_list, Qlist = load_rule('data.txt')
    for k, v in zip(P_list, Qlist):
        add_rule(k, v)

    while True:
        choice = input('请输入选择:')
        if choice == 'test':
            k = input('请输入测试的特征组合:').strip().split(' ')
            infer(k)

        elif choice == 'add':
            k = input('请输入添加的特征组合:').strip().split(' ')
            v = input('请输入添加的结论:')
            add_rule(k, v)

        elif choice == 'del':
            k = input('请输入删除的特征组合:').strip().split(' ')
            del_rule(k)

        elif choice == 'show':
            for k in rules.keys():
                print('%s ----> %s' % (k, rules[k]))

        elif choice == 'exit':
            exit(0)

"""
# 1. recall
# (recall fact)
# 判断变量fact中的一个事实是否在表facts中，若是，recall返回值是fact中的事实；否则，返回nil
def recall(fact):
    pass


# 2. test-if
# (test-if rule)
# 判断变量rule中的一条规则的前件包含的全部事实是否在表facts中，若是，test-if返回t；否则，返回nil
def test_if(rule):
    pass


# 3. remember
# (remember new)
# 判断变量new中的一个事实是否在表facts中，若是，remember返回nil；否则，将new中的事实添加到表facts的表头，
# 且remember返回new中的事实
def remember(new):
    pass


# 4. use-then
# (use-then rule)
# 判断变量rule中的一条规则的后件包含的全部结论是否在表facts中，若全部结论都在facts中，则use-then返回nil；
# 否则，将不在facts中的结论逐一添加到表facts中，且use-then返回t
def use_then(rule):
    pass


# 5. try-rule
# (try-raw rule)
# 判断规则变量rule中的一条规则的前件包含的全部事实是否在表facts中，若全部事实都在facts中，且规则后件有不在facts中的结论，
# 则把不在facts中的结论逐一添加到表facts中，try-rule返回t；否则，try-rule返回nil
def try_rule(rule):
    pass


# 6. step-forward
# (step-forward rules)
# 逐次扫描规则库rules中的规则，若发现rules中有一条可用规则，即该规则的前件包含的全部事实在表facts中，
# 则把该规则的后件中不在facts中的所有结论添加到facts中，且step-forward返回t；
# 若rules中没有一条可用规则，则step-forward返回nil
def step_forward(rules):
    pass


# 7. deduce
# (deduce facts)
# 连续不断地从规则库rules中选择可用规则，每选择到一条可用规则，则把该规则的后件中不在facts中的所有结论添加到facts中，
# 对facts扩充，由扩充了的facts来选择下一条可用规则对facts再次扩充，直至没有可用规则可选为止。
# 若曾找到一条可用规则对facts进行过一次扩充，则deduce返回t；否则，deduce返回nil
def deduce(facts):
    pass
"""
