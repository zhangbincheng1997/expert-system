from math import log
import operator


# 计算信息熵
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)  # H=−∑p(xi)log(p(xi))
    return shannonEnt


# 以axis为界，将特征值等于value的数据集划分成两个数据集
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]  # 左边一个
            reducedFeatVec.extend(featVec[axis + 1:])  # 右边一个
            retDataSet.append(reducedFeatVec)
    return retDataSet


# 寻找最佳特征，用来划分数据集
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1  # 获取特征数量
    baseEntropy = calcShannonEnt(dataSet)  # 计算数据集的熵
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):  # 遍历所有特征
        featList = [example[i] for example in dataSet]  # 获取当前特征列表
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:  # 遍历当前特征列表
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)  # 计算特征对数据集的熵
        infoGain = baseEntropy - newEntropy  # 计算信息增益
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain  # 选择信息增益最大的特征
            bestFeature = i
    return bestFeature


# 辅助函数：实例数量最大的类作为该结点的类标记
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


# ID3
def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]  # 获取标签列表
    if classList.count(classList[0]) == len(classList):  # 全部属于同一类型
        return classList[0]  # 只有这种类型
    if len(dataSet[0]) == 1:  # 只有一种类型
        return majorityCnt(classList)  # 返回标签(例如Y/N)
    bestFeat = chooseBestFeatureToSplit(dataSet)  # 寻找最佳特征，用来划分数据集
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}
    del (labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]  # 获取最佳特征列表
    uniqueVals = set(featValues)  # 特征去重(例如a1 a2 a3)
    for value in uniqueVals:  # 对每个最佳特征，分割成若干个非空子集
        subLabels = labels[:]

        """
        [a1, b1, c2]
        [a2, b1, c3]
        
        [a3, b2, c1]
        [a1, b2, c2]
        
        [a2, b3, c3]
        [a3, b3, c1]
        
        假设b为最佳特征，对每个最佳特征，分割成若干个非空子集====>
        
        b1: [a1, c2], [a2, c3]
        b2: [a3, c1], [a1, c2]
        b3: [a2, c3], [a3, c1]
        """

        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)  # 递归创建子树
    return myTree


# 分类
def classify(inputTree, featLabels, testVec):
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    key = testVec[featIndex]
    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict):  # 递归遍历子树
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else:  # 直到叶子节点
        classLabel = valueOfFeat
    return classLabel
