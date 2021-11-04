# README
game_tree的max_min极大极小搜索与alpha_beta剪枝搜索的简单应用——井字棋
## Contents
- [max_min极大极小搜索](#max_min极大极小搜索)
  - [构造一个棋盘类chessboard](#一、构造一个棋盘类chessboard)
  - [alpha_beta剪枝搜索核心算法](### 二、max_min搜索核心算法)
  - [主函数](###三、主函数)
  - [结果](###四、结果)
  - [最后](###五、最后)
- [alpha_beta剪枝搜索](##alpha_beta剪枝搜索)
  - [构造一个棋盘类chessboard](###一、构造一个棋盘类chessboard)
  - [alpha_beta剪枝搜索核心算法](###二、alpha_beta剪枝搜索核心算法)
  - [主函数](###三、主函数)
  - [结果](###四、结果)
  - [最后](###五、最后)

## max_min极大极小搜索
博弈树max_min搜索的简单应用——一字棋（井字棋），用一个较为简单的游戏实现，抛砖引玉。
### 一、构造一个棋盘类chessboard
#### 1.棋盘初始化与展示函数show
这一部分比较简单，不作详细介绍。
```
def __init__(self):  # 初始化

	self.grid = [['_', '_', '_'],
				 ['_', '_', '_'],
				 ['_', '_', '_']]
	self.num = 0

def show(self):    # 展示棋盘
	for i in range(3):
		print(self.grid[i][0], self.grid[i][1], self.grid[i][2])
```
#### 2.棋盘估值函数value
对于场上局势的评估，对于我方（算法）有利的值较大，这里采用一个比较简单的估值方法：棋盘上我方胜利方式的数目减去敌方胜利方式的数目；对于一个必胜（必败）的局势，对其赋值无穷大（负无穷大）。
```
    def value(self):
        # 算法（MAX）下'X'棋，敌方（MIN）下'O'棋

        # 必胜的情况估价函数赋值
        # MAX必胜赋+100，MIN必输赋-100
        # 横竖
        for i in range(0, 3):
            if self.grid[i] == ['X', 'X', 'X']:
                return 100
            if self.grid[0][i] == 'X' and self.grid[1][i] == 'X' and self.grid[2][i] == 'X':
                return 100
            if self.grid[i] == ['O', 'O', 'O']:
                return -100
            if self.grid[0][i] == 'O' and self.grid[1][i] == 'O' and self.grid[2][i] == 'O':
                return -100

        # 斜线
        if self.grid[0][0] == 'X' and self.grid[1][1] == 'X' and self.grid[2][2] == 'X':
            return 100
        if self.grid[2][0] == 'X' and self.grid[1][1] == 'X' and self.grid[0][2] == 'X':
            return 100
        if self.grid[0][0] == 'O' and self.grid[1][1] == 'O' and self.grid[2][2] == 'O':
            return -100
        if self.grid[2][0] == 'O' and self.grid[1][1] == 'O' and self.grid[0][2] == 'O':
            return -100

        # 双方均不是必胜情况
        # 某条线全不是'O'（敌方），则加1分，刻画算法有机会在这条线上赢下
        # 某条线全不是'X'（算法），则减一分，刻画算法不可能在这条线赢下
        value_temp = 0
        # 横竖
        for i in range(0, 3):

            if self.grid[0][i] != 'O' and self.grid[1][i] != 'O' and self.grid[2][i] != 'O':
                value_temp += 1
            if self.grid[0][i] != 'X' and self.grid[1][i] != 'X' and self.grid[2][i] != 'X':
                value_temp -= 1

            if self.grid[0][i] != 'O' and self.grid[1][i] != 'O' and self.grid[2][i] != 'O':
                value_temp += 1
            if self.grid[0][i] != 'X' and self.grid[1][i] != 'X' and self.grid[2][i] != 'X':
                value_temp -= 1
        # 斜线
        if self.grid[0][0] != 'O' and self.grid[1][1] != 'O' and self.grid[2][2] != 'O':
            value_temp += 1
        if self.grid[0][0] != 'X' and self.grid[1][1] != 'X' and self.grid[2][2] != 'X':
            value_temp -= 1
        if self.grid[0][2] != 'O' and self.grid[1][1] != 'O' and self.grid[2][0] != 'O':
            value_temp += 1
        if self.grid[0][2] != 'X' and self.grid[1][1] != 'X' and self.grid[2][0] != 'X':
            value_temp -= 1

        return value_temp
```
### 二、max_min搜索核心算法
首先对该方法进行简单的介绍，双人对弈，轮流下，一人走一步，双方看到的信息一样，双方均追求胜利。利用极大极小搜索时，每次搜索都生成规定深度内的所有结点，通过一定规则倒推得到节点的估值。

