import trees
import pandas as pd

df = pd.read_csv('data/1.csv')
col = df.columns.tolist()
data = df.values.tolist()
tree = trees.createTree(data, col)
print(tree)

col = df.columns.tolist()[:-1]
input1 = ['a3', 'b1', 'c2', 'd1']  # N
input2 = ['a3', 'b3', 'c1', 'd1']  # N
input3 = ['a2', 'b1', 'c1', 'd2']  # Y
input4 = ['a1', 'b1', 'c1', 'd1']  # Y
print(trees.classify(tree, col, input1))
print(trees.classify(tree, col, input2))
print(trees.classify(tree, col, input3))
print(trees.classify(tree, col, input4))

df = pd.read_csv('data/2.csv')
col = df.columns.tolist()
data = df.values.tolist()
tree = trees.createTree(data, col)
print(tree)

col = df.columns.tolist()[:-1]
input1 = ['undergraduate', 'man', 'cet6', 'a1', 'b1']  # N
input2 = ['undergraduate', 'man', 'cet4', 'a1', 'b1']  # Y
input3 = ['postgraduate', 'man', 'no', 'a1', 'b2']  # Y
input4 = ['undergraduate', 'man', 'no', 'a1', 'b3']  # Y
input5 = ['undergraduate', 'man', 'no', 'a3', 'b3']  # Y
print(trees.classify(tree, col, input1))
print(trees.classify(tree, col, input2))
print(trees.classify(tree, col, input3))
print(trees.classify(tree, col, input4))
print(trees.classify(tree, col, input5))
