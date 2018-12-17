# 博弈

## 极大极小值算法
1. 下面，最佳移动位于中间，因为最大值位于左侧的第二个节点上。
![alt text](tree.png "title")

2. 简化游戏树：
![alt text](tree2.png "title")

3. 在更复杂的游戏中，例如国际象棋，很难搜索整个游戏树。 但是，Alpha-beta Pruning是minimax算法的一种优化方法，它允许我们忽略搜索树中的某些分支，因为他在搜索中剪切了不相关的节点（子树）。 

>>> 更多信息，请参阅 https://github.com/Cledersonbc/tic-tac-toe-minimax
