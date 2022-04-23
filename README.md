# README
game_tree的max_min极大极小搜索与alpha_beta剪枝搜索的简单应用——井字棋
## Contents
- [max_min极大极小搜索](#max_min极大极小搜索)
  - [构造一个棋盘类chessboard](#max_min构造一个棋盘类chessboard)
  - [剪枝搜索核心算法](#max_min搜索核心算法)
  - [主函数](#max_min主函数)
  - [结果](#max_min结果)
  - [最后](#max_min最后)
- [alpha_beta剪枝搜索](#alpha_beta剪枝搜索)
  - [构造一个棋盘类chessboard](#alpha_beta构造一个棋盘类chessboard)
  - [alpha_beta剪枝搜索核心算法](#alpha_beta剪枝搜索核心算法)
  - [主函数](#alpha_beta主函数)
  - [结果](#alpha_beta结果)
  - [最后](#alpha_beta最后)

## max_min极大极小搜索
博弈树max_min搜索的简单应用——一字棋（井字棋），用一个较为简单的游戏实现，抛砖引玉。
### max_min构造一个棋盘类chessboard
```
class chessboard:
```
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
### max_min搜索核心算法
首先对该方法进行简单的介绍，双人对弈，轮流下，一人走一步，双方看到的信息一样，双方均追求胜利。利用极大极小搜索时，每次搜索都生成规定深度内的所有结点，通过一定规则倒推得到节点的估值。
<div align=center>
<img src="https://github.com/Luxlios/Figure/blob/main/game_tree%E5%8D%9A%E5%BC%88%E6%A0%91/max_min/1.png" height="300">
</div>
下面对于max_min搜索的过程进行介绍，我方（算法）的节点为与节点，由于我方（算法）下棋时需要考虑敌方（人类）的所有应对情况，敌方（人类）应对方式我们无法确定，因此取敌方所有应对方式的最小值作为我方节点的估值；敌方（人类）的节点为或节点，敌方（人类）下棋时，应对情况掌握在我方（算法）自己手中，应选估值最大的应对方式，作为敌方节点的估值。

由搜索的过程可以看到，估值采用倒推的方式，从最底层开始倒推到最顶层，即可得到最优的搜索路径（落子方式），通过一个例子来理解，假设已知四个节点的值。
<div align=center>
<img src="https://github.com/Luxlios/Figure/blob/main/game_tree%E5%8D%9A%E5%BC%88%E6%A0%91/max_min/2.png" height="300">
</div>
第一步读取到的点为-3和1，其父节点为或节点，则通过取最大值倒推得其父节点的估值为1。
<div align=center>
<img src="https://github.com/Luxlios/Figure/blob/main/game_tree%E5%8D%9A%E5%BC%88%E6%A0%91/max_min/3.png" height="300">
</div>
第二步读取到的点为5和-1，其父节点为或节点，则通过取最大值倒推得其父节点的估值为5。
<div align=center>
<img src="https://github.com/Luxlios/Figure/blob/main/game_tree%E5%8D%9A%E5%BC%88%E6%A0%91/max_min/4.png" height="300">
</div>
第三步读取到得点为1和5，其父节点为与节点，则通过取最小值倒推得其父节点的估值为1。
<div align=center>
<img src="https://github.com/Luxlios/Figure/blob/main/game_tree%E5%8D%9A%E5%BC%88%E6%A0%91/max_min/5.png" height="300">
</div>
循环上述步骤，即可得到各节点的值。

在博弈树中每一个子树引入一个节点，不改变树中各节点的取值，同时方便遍历和递归的过程。在或节点引入一个负无穷子节点，在与节点中引入一个正无穷子节点，由max_min搜索规则容易知道不影响各节点的估值，算法中会体现这一技巧。
<div align=center>
<img src="https://github.com/Luxlios/Figure/blob/main/game_tree%E5%8D%9A%E5%BC%88%E6%A0%91/max_min/6.png" height="300">
</div>
max_min搜索过程由子节点的值倒推节点的值，一步一步往上，容易想到，这是一个函数递归调用的过程，下面将用递归的方法实现倒推得到节点赋值的算法。

```
# 递归，得到当前这一步的估值
# alpha_beta剪枝 
def getvalue(chess, alpha, beta, player=True):
    if chess.num == 9 or chess.value() == 100 or chess.value() == -100:
        return chess.value()

    if player:
        beta_1 = 200
        alpha_1 = 0

        for i in range(0, 3):
            for j in range(0, 3):
                if chess.grid[i][j] == '_':
                    chess.grid[i][j] = 'O'
                    chess.num += 1
                    temp = getvalue(chess, alpha_1, beta_1, player=False)
                    chess.num -= 1
                    chess.grid[i][j] = '_'
                    if temp < beta_1:        # 更新
                        beta_1 = temp
                    if beta_1 <= alpha:     # 剪枝
                        return beta_1
        return beta_1     # 计算添加节点（-200or+200）时,无法返回值，在这里加个return
                          # 为添加的节点设计，对于其他节点没用用处

    else:
        alpha_1 = -200
        beta_1 = 0

        for i in range(0, 3):
            for j in range(0, 3):
                if chess.grid[i][j] == '_':
                    chess.grid[i][j] = 'X'
                    chess.num += 1
                    temp = getvalue(chess, alpha_1, beta_1, player=True)
                    chess.num -= 1
                    chess.grid[i][j] = '_'
                    if temp > alpha_1:      # 更新
                        alpha_1 = temp
                    if alpha_1 >= beta:    # 剪枝
                        return alpha_1
        return alpha_1
```

函数输入的两个参数分别为落子后的棋盘局势和落子的玩家，玩家默认为True，表示算法，False表示人类，算法大致流程如下：

①当player为True时，即计算算法落子的估值，添加一个子节点估值为200，则该落子首先满足估值≤200。通过循环递归调用该算法（player为False），得到其子节点的值，每次得到比估值小的值则更新估值。

②当player为False时，即计算算法落子的估值，添加一个子节点估值为-200，则该落子首先满足估值≥-200。通过循环递归调用该算法（player为False），得到其子节点的值，每次得到比估值大的值则更新估值。

①和②相互递归调用，实现倒推求节点值的过程。
### max_min主函数
这一部分比较简单，不作详细介绍。
```
game = chessboard()
game.show()
step = 0

while True:
if game.value() == 100 or game.value() == -100:
    break

# Step 1
print("YOUR TURN TO PLAY")
x, y = input("PLEASE INPUT THE COORDINATE(SPLIT WITH SPACE):").split()
x = int(x) - 1
y = int(y) - 1
game.grid[x][y] = 'O'
game.num += 1
print("THE GAME AFTER YOU PLAY:")
game.show()

step = step + 1
if step == 9:  # 下满了棋盘
    break

alpha = -200
beta = 0
# 遍历、寻找一个估值最高的下棋位置
for i in range(0, 3):
    for j in range(0, 3):
	if game.grid[i][j] == '_':

	    game.num += 1
	    game.grid[i][j] = 'X'
	    temp = getvalue(game, alpha, beta, player=True)
	    game.grid[i][j] = '_'
	    game.num -= 1
	    if temp > alpha:
		alpha = temp
		x, y = i, j
game.grid[x][y] = 'X'
game.num += 1
step = step + 1
print("THE GAME AFTER ALGORITHM PLAY:")
game.show()

if game.value() == -100:
print("YOU WIN!")
elif game.value() == 100:
print("YOU LOSE!")
else:
print("DRAW!")
```
### max_min结果
```
_ _ _
_ _ _
_ _ _
YOUR TURN TO PLAY
PLEASE INPUT THE COORDINATE(SPLIT WITH SPACE):2 2
THE GAME AFTER YOU PLAY:
_ _ _
_ O _
_ _ _
THE GAME AFTER ALGORITHM PLAY:
X _ _
_ O _
_ _ _
YOUR TURN TO PLAY
PLEASE INPUT THE COORDINATE(SPLIT WITH SPACE):1 3
THE GAME AFTER YOU PLAY:
X _ O
_ O _
_ _ _
THE GAME AFTER ALGORITHM PLAY:
X _ O
_ O _
X _ _
YOUR TURN TO PLAY
PLEASE INPUT THE COORDINATE(SPLIT WITH SPACE):2 1
THE GAME AFTER YOU PLAY:
X _ O
O O _
X _ _
THE GAME AFTER ALGORITHM PLAY:
X _ O
O O X
X _ _
YOUR TURN TO PLAY
PLEASE INPUT THE COORDINATE(SPLIT WITH SPACE):3 3
THE GAME AFTER YOU PLAY:
X _ O
O O X
X _ O
THE GAME AFTER ALGORITHM PLAY:
X X O
O O X
X _ O
YOUR TURN TO PLAY
PLEASE INPUT THE COORDINATE(SPLIT WITH SPACE):3 2
THE GAME AFTER YOU PLAY:
X X O
O O X
X O O
DRAW!

Process finished with exit code 0
```
### max_min最后
max_min搜索算法最重要的部分是第二个部分，可以反复观看去理解它。可以明显的感觉到，max_min搜索算法通过倒推得到各节点估值时，需要计算所有的节点，这会花费多余的时间，在复杂的游戏中使用时间复杂度较高，因此可以看看第二部分alpha_beta剪枝搜索，有效降低时间复杂度。

这里用到了一个比较简单的游戏来实现这个算法，抛砖引玉，如果有帮助的话，可以点个Star，同时也欢迎批评指正，谢谢！

## alpha_beta剪枝搜索
博弈树alpha_beta剪枝法的简单应用——一字棋（井字棋），用一个较为简单的游戏实现，抛砖引玉。
### alpha_beta构造一个棋盘类chessboard
```
class chessboard:
```
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
# 棋盘赋值函数
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
### alpha_beta剪枝搜索核心算法
首先对该方法进行简单的介绍，与博弈树极大极小搜索（Min_max）相似，详情可见第一部分。双人对弈，轮流下，一人走一步，双方看到的信息一样，双方均追求胜利。但利用极大极小搜索时，每次搜索都需要生成规定深度内的所有结点，搜索效率较低。alpha_beta剪枝搜索可以有效提升搜索效率，边生成节点，边对节点估值，从而可以剪去一些没用的分支。
<div align=center>
<img src="https://github.com/Luxlios/Figure/blob/main/game_tree%E5%8D%9A%E5%BC%88%E6%A0%91/alpha_beta%E5%89%AA%E6%9E%9D/1.png" height="300">
</div>
下面对于alpha_beta剪枝搜索的过程进行介绍，我方（算法）的节点为与节点，由于我方（算法）下棋时需要考虑敌方（人类）的所有应对情况，敌方（人类）应对方式我们无法确定，因此取敌方所有应对方式的最小值作为我方节点的估值，称作beta；敌方（人类）的节点为或节点，敌方（人类）下棋时，应对情况掌握在我方（算法）自己手中，应选估值最大的应对方式，作为敌方节点的估值，称作alpha。

与极大极小搜索过程一样，估值采用倒推的方式，不一样的是，alpha_beta剪枝采用边生成节点，边对节点估值的方式，与节点的beta值要用其子节点（或节点）的alpha值的最小值倒推，或节点的alpha值要用其子节点（与节点）的beta值的最大值倒推。
alpha_beta剪枝的两个规则是：

①任何与节点的beta值如果不能升高其父节点的alpha值，则对该节点以下的分枝可停止搜索，使得该节点的倒推值为beta。

②任何或节点的alpha值如果不能降低其父节点的beta值，则对该节点以下的分枝可停止搜索，使得该节点的倒推值为alpha。
下面用一个动画来演示剪枝的流程:
<div align=center>
<img src="https://github.com/Luxlios/Figure/blob/main/game_tree%E5%8D%9A%E5%BC%88%E6%A0%91/alpha_beta%E5%89%AA%E6%9E%9D/%E5%89%AA%E6%9E%9D%E6%BC%94%E7%A4%BA.gif" height="300">
</div>
对于动画进行详细的解释，假设博弈树中有三个已知节点，从左往右读取数据，如图所示。
<div align=center>
<img src="https://github.com/Luxlios/Figure/blob/main/game_tree%E5%8D%9A%E5%BC%88%E6%A0%91/alpha_beta%E5%89%AA%E6%9E%9D/2.png" height="300">
</div>
第一步读取到的点为d，值为-3，则其父节点b（或节点）的alpha值满足α≥-3。
<div align=center>
<img src="https://github.com/Luxlios/Figure/blob/main/game_tree%E5%8D%9A%E5%BC%88%E6%A0%91/alpha_beta%E5%89%AA%E6%9E%9D/3.png" height="300">
</div>
第二步读取到的点为e，值为1，其父节点b的子节点均已读取完毕，可以确定b的alpha值为α=1。
<div align=center>
<img src="https://github.com/Luxlios/Figure/blob/main/game_tree%E5%8D%9A%E5%BC%88%E6%A0%91/alpha_beta%E5%89%AA%E6%9E%9D/4.png" height="300">
</div>
第三步可以确定b的父节点a（或结点）的beta值满足β≤1。
<div align=center>
<img src="https://github.com/Luxlios/Figure/blob/main/game_tree%E5%8D%9A%E5%BC%88%E6%A0%91/alpha_beta%E5%89%AA%E6%9E%9D/5.png" height="300">
</div>
第四步读取的点为f，值为5，则可以确定其父节点c（或节点）的alpha值满足α≥5。
<div align=center>
<img src="https://github.com/Luxlios/Figure/blob/main/game_tree%E5%8D%9A%E5%BC%88%E6%A0%91/alpha_beta%E5%89%AA%E6%9E%9D/6.png" height="300">
</div>
第五步判断是否进行剪枝，由于已经知道a的beta值≤1，而其子节点c的alpha值≥5，因此c的alpha值不可能降低其父节点a的beta值，所以对于c节点的其他分支可以进行剪枝操作，使得c的alpha值有α=5，同时可以确定a节点的beta值有β=1。
<div align=center>
<img src="https://github.com/Luxlios/Figure/blob/main/game_tree%E5%8D%9A%E5%BC%88%E6%A0%91/alpha_beta%E5%89%AA%E6%9E%9D/7.png" height="300">
</div>
与节点剪枝情况类似，循环上述步骤，即可得到各节点的值，并且忽略掉一些冗余的分支，可以重新回看一下剪枝的动画演示，理清思路，下面开始讲述算法的设计。
在博弈树中每一个子树引入一个节点，不改变树中各节点的取值，同时方便遍历和递归的过程。在或节点引入一个负无穷子节点，在与节点中引入一个正无穷子节点，由alpha_beta剪枝规则容易知道不影响各节点的估值，算法中会体现这一技巧。
<div align=center>
<img src="https://github.com/Luxlios/Figure/blob/main/game_tree%E5%8D%9A%E5%BC%88%E6%A0%91/alpha_beta%E5%89%AA%E6%9E%9D/8.png" height="300">
</div>
alpha_beta剪枝过程由子节点的值倒推节点的值，一步一步往上，容易想到，这是一个函数递归调用的过程，下面将用递归的方法实现倒推得到节点赋值的算法。

函数输入的四个参数分别为落子后的棋盘局势、节点父节点当前的alpha值、节点父节点当前的beta值（或节点只存在alpha值，beta值为0；与节点alpha值为0，只存在beta值）和落子的玩家，玩家默认为True，表示算法，False表示人类。算法大致流程如下：

①当player为True时，即计算算法落子的估值，添加一个子节点α=200，则该落子首先满足β≤200。通过循环递归调用该算法（player为False），得到其子节点的值，每次得到比β小的值则更新β，并且判断β是否小于其父节点当前的α值，若小于则剪枝，跳出循环，将当前的β值作为该落子的估值。

②当player为False时，即计算人类落子的估值，添加一个子节点β=-200，则该落子首先满足α≥-200。通过循环递归调用该算法（player为True），得到其子节点的值，每次得到比α大的值则更新α，并且判断α是否大于其父节点当前的β值，若大于则剪枝，跳出循环，将当前的α值作为该落子的估值。

①和②相互递归调用，实现倒推求节点值的过程。

```
# 递归，得到当前这一步的估值
# alpha_beta剪枝 
def getvalue(chess, alpha, beta, player=True):
    if chess.num == 9 or chess.value() == 100 or chess.value() == -100:
        return chess.value()

    if player:
        beta_1 = 200
        alpha_1 = 0

        for i in range(0, 3):
            for j in range(0, 3):
                if chess.grid[i][j] == '_':
                    chess.grid[i][j] = 'O'
                    chess.num += 1
                    temp = getvalue(chess, alpha_1, beta_1, player=False)
                    chess.num -= 1
                    chess.grid[i][j] = '_'
                    if temp < beta_1:        # 更新
                        beta_1 = temp
                    if beta_1 <= alpha:     # 剪枝
                        return beta_1
        return beta_1     # 计算添加节点（-200or+200）时,无法返回值，在这里加个return
                          # 为添加的节点设计，对于其他节点没用用处

    else:
        alpha_1 = -200
        beta_1 = 0

        for i in range(0, 3):
            for j in range(0, 3):
                if chess.grid[i][j] == '_':
                    chess.grid[i][j] = 'X'
                    chess.num += 1
                    temp = getvalue(chess, alpha_1, beta_1, player=True)
                    chess.num -= 1
                    chess.grid[i][j] = '_'
                    if temp > alpha_1:      # 更新
                        alpha_1 = temp
                    if alpha_1 >= beta:    # 剪枝
                        return alpha_1
        return alpha_1
```
### alpha_beta主函数
这一部分比较简单，这里不作介绍。
```
game = chessboard()
    game.show()
    step = 0

    while True:
        if game.value() == 100 or game.value() == -100:
            break

        # Step 1
        print("YOUR TURN TO PLAY")
        x, y = input("PLEASE INPUT THE COORDINATE(SPLIT WITH SPACE):").split()
        x = int(x) - 1
        y = int(y) - 1
        game.grid[x][y] = 'O'
        game.num += 1
        print("THE GAME AFTER YOU PLAY:")
        game.show()

        step = step + 1
        if step == 9:  # 下满了棋盘
            break
        
        alpha = -200
        beta = 0
        # 遍历、寻找一个估值最高的下棋位置
        for i in range(0, 3):
            for j in range(0, 3):
                if game.grid[i][j] == '_':

                    game.num += 1
                    game.grid[i][j] = 'X'
                    temp = getvalue(game, alpha, beta, player=True)
                    game.grid[i][j] = '_'
                    game.num -= 1
                    if temp > alpha:
                        alpha = temp
                        x, y = i, j
        game.grid[x][y] = 'X'
        game.num += 1
        step = step + 1
        print("THE GAME AFTER ALGORITHM PLAY:")
        game.show()

    if game.value() == -100:
        print("YOU WIN!")
    elif game.value() == 100:
        print("YOU LOSE!")
    else:
        print("DRAW!")
```
### alpha_beta结果
```
_ _ _
_ _ _
_ _ _
YOUR TURN TO PLAY
PLEASE INPUT THE COORDINATE(SPLIT WITH SPACE):2 2
THE GAME AFTER YOU PLAY:
_ _ _
_ O _
_ _ _
THE GAME AFTER ALGORITHM PLAY:
X _ _
_ O _
_ _ _
YOUR TURN TO PLAY
PLEASE INPUT THE COORDINATE(SPLIT WITH SPACE):3 2
THE GAME AFTER YOU PLAY:
X _ _
_ O _
_ O _
THE GAME AFTER ALGORITHM PLAY:
X X _
_ O _
_ O _
YOUR TURN TO PLAY
PLEASE INPUT THE COORDINATE(SPLIT WITH SPACE):1 3
THE GAME AFTER YOU PLAY:
X X O
_ O _
_ O _
THE GAME AFTER ALGORITHM PLAY:
X X O
_ O _
X O _
YOUR TURN TO PLAY
PLEASE INPUT THE COORDINATE(SPLIT WITH SPACE):2 1
THE GAME AFTER YOU PLAY:
X X O
O O _
X O _
THE GAME AFTER ALGORITHM PLAY:
X X O
O O X
X O _
YOUR TURN TO PLAY
PLEASE INPUT THE COORDINATE(SPLIT WITH SPACE):3 3
THE GAME AFTER YOU PLAY:
X X O
O O X
X O O
DRAW!

Process finished with exit code 0
```
### alpha_beta最后
alpha_beta剪枝算法最重要的部分是第二个部分，可以反复观看去理解它。

这里用到了一个比较简单的游戏来实现这个算法，抛砖引玉，如果有帮助的话，可以点个Star，同时也欢迎批评指正，谢谢！
