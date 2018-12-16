#!/usr/bin/python
# -*- coding: UTF-8 -*-


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


# 拓扑排序
def topological(rules):
    # 规则
    topo_rules = collections.OrderedDict()
    P_list = list(rules.keys())
    Q_list = list(rules.values())

    # 计算入度
    ind_list = []
    for i in P_list:
        sum = 0
        for x in i:
            if Q_list.count(x) > 0:
                sum += Q_list.count(x)
        ind_list.append(sum)

    # 拓扑排序
    while True:
        if ind_list.count(-1) == len(ind_list):
            break

        for i, ind in enumerate(ind_list):
            if ind == 0:
                topo_rules[tuple(P_list[i])] = Q_list[i]
                ind_list[i] = -1
                # 更新入度
                for j, P in enumerate(P_list):
                    if Q_list[i] in P:
                        ind_list[j] -= 1
    return topo_rules

# 反向推理机
def infer(facts, topo_rules):
    flag = False
    for key in topo_rules.keys():
        # 如果所有规则都在输入中
        if list_in_set(key, facts):
            # 添加推导出的条件
            facts.append(topo_rules[key])
            flag = True
            print('{key} ----> {value}\n'.format(key=key, value=facts[-1]))

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
    topo_rules = topological(rules)

    while True:
        choice = input("请输入选择：'test/add/del/show/exit'，默认'test' >>> ")
        if choice == 'add':
            k = input('请输入添加的特征组合：').strip().split(' ')
            v = input('请输入添加的结论：')
            add_rule(k, v, rules)
            topo_rules = topological(rules) # 与正向不同，每次都要更新

        elif choice == 'del':
            k = input('请输入删除的特征组合：').strip().split(' ')
            del_rule(k, rules)
            topo_rules = topological(rules) # 与正向不同，每次都要更新

        elif choice == 'show':
            for k in rules.keys():
                print('%s ----> %s' % (k, rules[k]))

        elif choice == 'exit':
            exit(0)

        else:
            k = input('请输入测试的特征组合：').strip().split(' ')
            infer(k, topo_rules)
