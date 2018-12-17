import trees
import pandas as pd

df = pd.read_csv('data/1.csv')
col = df.columns.tolist()
data = df.values.tolist()
tree = trees.createTree(data, col)
print(tree)

df = pd.read_csv('data/2.csv')
col = df.columns.tolist()
data = df.values.tolist()
tree = trees.createTree(data, col)
print(tree)
