# -*- coding = utf-8 -*-
# @Author : Luxlios
# @File : max_min过程.py
# @Software : PyCharm

# game_tree___max_min过程
# 博弈树max_min搜索玩井字棋

class chessboard:

    def __init__(self):  # 初始化

        self.grid = [['_', '_', '_'],
                     ['_', '_', '_'],
                     ['_', '_', '_']]
        self.num = 0

    def show(self):  # 展示棋盘
        for i in range(3):
            print(self.grid[i][0], self.grid[i][1], self.grid[i][2])

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


# 递归，得到当前这一步的估值
# max_min过程
def getvalue(chess, player=True):
    if chess.num == 9 or chess.value() == 100 or chess.value() == -100:
        return chess.value()

    if player:
        min = 200

        for i in range(0, 3):
            for j in range(0, 3):
                if chess.grid[i][j] == '_':
                    chess.grid[i][j] = 'O'
                    chess.num += 1
                    temp = getvalue(chess, player=False)
                    chess.num -= 1
                    chess.grid[i][j] = '_'
                    if temp < min:  # 更新
                        min = temp
        return min

    else:
        max = -200

        for i in range(0, 3):
            for j in range(0, 3):
                if chess.grid[i][j] == '_':
                    chess.grid[i][j] = 'X'
                    chess.num += 1
                    temp = getvalue(chess, player=True)
                    chess.num -= 1
                    chess.grid[i][j] = '_'
                    if temp > max:  # 更新
                        max = temp
        return max



if __name__ == '__main__':
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

        max = -200
        # 遍历、寻找一个估值最高的下棋位置
        for i in range(0, 3):
            for j in range(0, 3):
                if game.grid[i][j] == '_':

                    game.num += 1
                    game.grid[i][j] = 'X'
                    temp = getvalue(game, player=True)
                    game.grid[i][j] = '_'
                    game.num -= 1
                    if temp > max:
                        max = temp
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
