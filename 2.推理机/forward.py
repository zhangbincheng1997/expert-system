#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
正向推理（数据驱动），其基本思想是：
1. 从问题已有的事实（初始证据）出发，正向使用规则，
2. 当规则的条件部分与已有的事实匹配时，就把该规则作为可用规则放入候选规则队列中，
3. 然后通过冲突消解，在候选队列中选择一条规则作为启用规则进行推理，并将其结论放入数据库中，作为下一步推理时的证据。
4. 如此重复这个过程，直到再无可用规则可被选用或者求得了所要求的解为止。

冲突消解：
1. 优先度排序。事先给知识库中每条规则设定优先度参数，优先度高的规则先执行。
2. 规则的条件详细度排序。条件较多、较详细的规则，其结论一般更接近于目标，优先执行。
3. 匹配度排序。事先给知识库中每条规则设定匹配度参数，匹配度高的规则先执行。
4. 根据领域问题的特点排序。根据领域知识可以知道的某些特点，事先设定知识库中的规则的使用顺序。
"""


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
def add_rule(k, v, rules):
    if tuple(k) in rules.keys():
        print('特征已在数据库')
    else:
        rules[tuple(k)] = v
        print('特征成功添加 >>> %s ----> %s' % (k, v))


# 删除规则
def del_rule(k, rules):
    if tuple(k) in rules.keys():
        rules.pop(tuple(k))
        print('特征成功删除 >>> %s' % k)
    else:
        print('特征不在数据库')


# 冲突消解
def resolve(candidate_rule, method=1):
    if method == 1: # 1. 最长匹配策略
        return max(candidate_rule, key=lambda x:len(x[0]))
    elif method == 2: # 2. 最早匹配策略
        return candidate_rule[0]
    elif method == 3: # 3. 最晚匹配策略
        return candidate_rule[-1]
    else:
        exit(0)


# 正向推理机
def infer(facts, rules):
    candidate_rule = []
    visited_rule = []
    flag = False
    
    while True:
        candidate_rule.clear()
        for rule in rules.items(): # 1. 从问题已有的事实（初始证据）出发，正向使用规则
            k, v = rule
            if list_in_set(k, facts) and rule not in visited_rule: # 2. 当规则的条件部分与已有的事实匹配时，就把该规则作为可用规则放入候选规则队列中
                candidate_rule.append(rule)
                visited_rule.append(rule)
                print('规约：{key} ----> {value}'.format(key=k, value=v))
        
        if len(candidate_rule) != 0: # 3. 然后通过冲突消解，在候选队列中选择一条规则作为启用规则进行推理，并将其结论放入数据库中，作为下一步推理时的证据
            k, v = resolve(candidate_rule)
            facts.append(v)
            flag = True
            print('冲突消解：{key} ====> {value}\n'.format(key=k, value=v))
        else: # 4. 如此重复这个过程，直到再无可用规则可被选用或者求得了所要求的解为止
            break

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
    import collections
    rules = collections.OrderedDict()
    P_list, Q_list = load_rule('data.txt')
    for k, v in zip(P_list, Q_list):
        add_rule(k, v, rules)

    while True:
        choice = input("请输入选择：'test/add/del/show/exit'，默认'test' >>> ")
        if choice == 'add':
            k = input('请输入添加的特征组合：').strip().split(' ')
            v = input('请输入添加的结论：')
            add_rule(k, v, rules)

        elif choice == 'del':
            k = input('请输入删除的特征组合：').strip().split(' ')
            del_rule(k, rules)

        elif choice == 'show':
            for k in rules.keys():
                print('%s ----> %s' % (k, rules[k]))

        elif choice == 'exit':
            exit(0)
        
        else:
            k = input('请输入测试的特征组合：').strip().split(' ')
            infer(k, rules)
