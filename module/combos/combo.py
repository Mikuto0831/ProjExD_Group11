import pygame as pg
from module.scores.scores import Score

def jadge_combo(a, b):
    if a == b or a + 10 == b or a == b + 10:
        return True
    else:
        return False

def jadge_double(lis:list[list], i:int, j:int, combo_type:int, combo_len:int = 3):
    T = combo_len
    if combo_type == 1:
        for n in range(3):
            for m in range(3):
                if lis[i+n][j+m] >= 10:
                    T -= 1

    elif combo_type == 11:
        for n in range(combo_len):
            if lis[i][j+n] >= 10:
                T -= 1

    elif combo_type == 12:
        for n in range(combo_len):
            if lis[i+n][j] >= 10:
                T -= 1

    elif combo_type == 21:
        if lis[i][j] >= 10 and lis[i][j+1] >= 10 and lis[i][j+2] >= 10 and lis[i-1][j+1] >= 10 and lis[i+1][j+1] >= 10:
            T -= combo_len

    elif combo_type == 22:
        if lis[i][j] >= 10 and lis[i][j+2] >= 10 and lis[i+1][j] >= 10 and lis[i+1][j+1] >= 10 and lis[i+1][j+2] >= 10 and lis[i+2][j] >= 10 and lis[i+2][j+2] >= 10:
            T -= combo_len
    
    elif combo_type == 23:
        if lis[i][j] >= 10 and lis[i][j+2] >= 10 and lis[i+2][j] >= 10 and lis[i+2][j+2] >= 10 and lis[i][j+1] >= 10 and lis[i+2][j+1] >= 10 and lis[i+2][j+1] >= 10:
            T -= combo_len

    elif combo_type == 31:
        for n in range(3):
            if lis[i+n][j] >= 10:
                    T -= 1
                    if n == 2:
                        for m in range(1, 3):
                            if lis[i+n][j+m] >= 10:
                                T -= 1

    elif combo_type == 32:
        for n in range(3):
            if lis[i+n][j] >= 10:
                    T -= 1
                    if n == 2:
                        for m in range(-2, 0):
                            if lis[i+n][j+m] >= 10:
                                T -= 1

    elif combo_type == 33:
        for n in range(3):
            if lis[i+n][j] >= 10:
                    T -= 1
                    if n == 0:
                        for m in range(1, 3):
                            if lis[i+n][j+m] >= 10:
                                T -= 1

    elif combo_type == 34:
        for n in range(3):
            if lis[i][j+n] >= 10:
                    T -= 1
                    if n == 2:
                        for m in range(1, 3):
                            if lis[i+m][j+n] >= 10:
                                T -= 1
    elif combo_type == 41:
        for n in range(3):
            if lis[i][j+n] >= 10:
                    T -= 1
                    if n == 1:
                        for m in range(1, 3):
                            if lis[i+m][j+n] >= 10:
                                T -= 1
    elif combo_type == 42:
        for n in range(3):
            if lis[i+n][j] >= 10:
                    T -= 1
                    if n == 2:
                        for m in range(-1, 2, 2):
                            if lis[i+n][j+m] >= 10:
                                T -= 1

    elif combo_type == 43:
        for n in range(3):
            if lis[i+n][j] >= 10:
                    T -= 1
                    if n == 1:
                        for m in range(1, 3):
                            if lis[i+n][j+m] >= 10:
                                T -= 1
    
    elif combo_type == 44:
        for n in range(3):
            if lis[i][j+n] >= 10:
                    T -= 1
                    if n == 2:
                        for m in range(-1, 2, 2):
                            if lis[i+m][j+n] >= 10:
                                T -= 1

    if T > 0:
        return True
    else:
        return False


class Combo:
    """
    コンボの判定をするクラス
    コンボの判定
        1:横
        2:縦
    担当:瀬尾
    """
    
    combo_all = 0
    score:Score
    screen:pg.surface

    def __init__(self, lis:list[list]):
        self.combo_count = 0
        self.lis = lis
        check = 0
        while True:
            self.box_combo()
            self.h_combo()
            self.i_combo()
            self.t_combo()
            self.t_combo_rev()
            self.t_left_combo()
            self.t_right_combo()
            self.l_combo_dl()
            self.l_combo_dr()
            self.l_combo_ul()
            self.l_combo_ur()
            self.cross_combo()
            self.row_combo()
            self.column_combo()
            if check == self.combo_count:
                break
            check = self.combo_count
        print("rep")
        print(self.lis[0], "\n", self.lis[1], "\n", self.lis[2], "\n", self.lis[3], "\n", self.lis[4], "\n", self.lis[5])
        self.elise(self.lis)
    
    def box_combo(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 1, 9) and jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+1][j]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+2]):
                    stack += 2
                    print("box", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 1, self.lis[i][j])
                    break

    def h_combo(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 22) and jadge_combo(self.lis[i][j], self.lis[i][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+1][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+2]):
                    stack += 2
                    print("H", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 22, self.lis[i][j])
                    break
        
    def i_combo(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 23) and jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+2]):
                    stack += 2
                    print("I", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 23, self.lis[i][j])
                    break

    def t_combo(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 41, 5) and jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+1]):
                    stack += 2
                    print("T", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 41, self.lis[i][j])
                    break
    
    def t_combo_rev(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 42, 5) and jadge_combo(self.lis[i][j], self.lis[i+2][j-1]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+1][j]):
                    stack += 2
                    print("T-rev", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 42, self.lis[i][j])
                    break

    def t_left_combo(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 43, 5) and jadge_combo(self.lis[i][j], self.lis[i+1][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+2]):
                    stack += 2
                    print("T-left", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 43, self.lis[i][j])
                    break
    
    def t_right_combo(self):
        for i in range(1, len(self.lis) - 1):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 44, 5) and jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]) and jadge_combo(self.lis[i][j], self.lis[i-1][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+2]):
                    stack += 2
                    print("T-right", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 44, self.lis[i][j])
                    break
    
    def l_combo_dl(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 31, 5) and jadge_combo(self.lis[i][j], self.lis[i+1][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+2]):
                    stack += 2
                    print("L-dl", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 31, self.lis[i][j])
                    break

    def l_combo_dr(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(2, len(self.lis)):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 32, 5) and jadge_combo(self.lis[i][j], self.lis[i+1][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j-1]) and jadge_combo(self.lis[i][j], self.lis[i+2][j-2]):
                    stack += 2
                    print("L-dr", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 32, self.lis[i][j])
                    break
    def l_combo_ul(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 33, 5) and jadge_combo(self.lis[i][j], self.lis[i+1][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]):
                    stack += 2
                    print("L-ul", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 31, self.lis[i][j])
                    break
    def l_combo_ur(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 34, 5) and jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+2]):
                    stack += 2
                    print("L-ur", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 34, self.lis[i][j])
                    break
    
    def cross_combo(self):
        for i in range(1, len(self.lis) - 1):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    stack -= 1
                    continue
                if jadge_double(self.lis, i, j, 21) and jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]) and jadge_combo(self.lis[i][j], self.lis[i-1][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+1]):
                    stack += 2
                    print("cross", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 21, self.lis[i][j])
                    break

    def row_combo(self):
       for i in range(len(self.lis)):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    stack -= 1
                    continue
                combo_len = 3
                if jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]):
                    if j <= 2 and jadge_combo(self.lis[i][j], self.lis[i][j+3]):
                        combo_len += 1
                        if j <= 1 and jadge_combo(self.lis[i][j], self.lis[i][j+4]):
                            combo_len += 1
                            if j <= 0 and jadge_combo(self.lis[i][j], self.lis[i][j+5]):
                                combo_len += 1
                    if jadge_double(self.lis, i, j, 11, combo_len):
                        self.combo_count += 1
                        stack += combo_len-1
                        print("row", [i, j], combo_len)
                        self.combo_add()
                        self.change(self.lis, i, j, 11, self.lis[i][j], combo_len)
                        break
                    
    def column_combo(self):
        for j in range(len(self.lis)):
            stack = 0
            for i in range(len(self.lis) - 2):
                if stack > 0:
                    stack -= 1
                    continue
                combo_len = 3
                if jadge_combo(self.lis[i][j], self.lis[i+1][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]):
                    if i <= 2 and jadge_combo(self.lis[i][j], self.lis[i+3][j]):
                        combo_len += 1
                        if i <= 1 and self.lis[i][j] == self.lis[i+4][j]:
                            combo_len += 1
                            if i <= 0 and jadge_combo(self.lis[i][j], self.lis[i+5][j]):
                                combo_len += 1
                    if jadge_double(self.lis, i, j, 12, combo_len):
                        self.combo_count += 1
                        stack += combo_len-1
                        print("column", [i, j], combo_len)
                        self.combo_add()
                        self.change(self.lis, i, j, 12, self.lis[i][j], combo_len)
                        
                        break

    def get_count(self):
        return self.combo_count
    
    def get_lis(self):
        return self.lis
    
    def change(self, lis:list[list], i:int, j:int, combo_type:int, ele:int = 0, combo_len:int = 1):
        #引数:lst　ボールの種類を保持するリスト
        #コンボ判定されたball_lstを0にする
        if ele >= 10:
            ele = ele - 10
        
        if combo_type == 1:
            for n in range(3):
                for m in range(3):
                    lis[i+n][j+m] = 10+ele

        if combo_type == 11:
            for n in range(combo_len):
                lis[i][j+n] = 10+ele

        elif combo_type == 12:
            for n in range(combo_len):
                lis[i+n][j] = 10+ele

        elif combo_type == 21:
            for n in range(3):
                lis[i][j+n] = 10+ele
            lis[i-1][j+1] = 10+ele
            lis[i+1][j+1] = 10+ele

        elif combo_type == 22:
            for n in range(3):
                lis[i+1][j+n] = 10+ele
            lis[i][j] = 10+ele
            lis[i][j+2] = 10+ele
            lis[i+2][j] = 10+ele
            lis[i+2][j+2] = 10+ele

        elif combo_type == 23:
                    for n in range(3):
                        lis[i+n][j+1] = 10+ele
                    lis[i][j] = 10+ele
                    lis[i][j+2] = 10+ele
                    lis[i+2][j] = 10+ele
                    lis[i+2][j+2] = 10+ele

        elif combo_type == 31:
            for n in range(3):
                lis[i+n][j] = 10+ele
                if n == 2:
                    for m in range(1, 3):
                        lis[i+n][j+m] = 10+ele
        
        elif combo_type == 32:
            for n in range(3):
                lis[i+n][j] = 10+ele
                if n == 2:
                    for m in range(-2, 0):
                        lis[i+n][j+m] = 10+ele
        
        elif combo_type == 33:
            for n in range(3):
                lis[i+n][j] = 10+ele
                lis[i][j+n] = 10+ele

        elif combo_type == 34:
            for n in range(3):
                lis[i][j+n] = 10+ele
                if n == 2:
                    for m in range(1, 3):
                        lis[i+m][j+n] = 10+ele
        
        elif combo_type == 41:
            for n in range(3):
                lis[i][j+n] = 10+ele
                if n == 1:
                    for m in range(1, 3):
                        lis[i+n][j] = 10+ele

        elif combo_type == 42:
            for n in range(3):
                lis[i+n][j] = 10+ele
                if n == 2:
                    for m in range(-1, 2, 2):
                        lis[i+n][j+m] = 10+ele

        elif combo_type == 43:
            for n in range(3):
                lis[i+n][j] = 10+ele
                if n == 1:
                    for m in range(1, 3):
                        lis[i+n][j+m] = 10+ele

        elif combo_type == 44:
            for n in range(3):
                lis[i][j+n] = 10+ele
                if n == 2:
                    for m in range(-1, 2, 2):
                        lis[i+m][j+n] = 10+ele

        self.lis = lis

    
    def elise(self, lis:list[list]):
        for i in range(len(lis)):
            for j in range(len(lis[i])):
                if lis[i][j] >= 10:
                    lis[i][j] = 0
        self.lis = lis
    
    @classmethod
    def combo_add(cls):
        import time
        cls.combo_all += 1
        cls.score.calculate_combo_score(cls.combo_all)
        cls.uppdate_screen()
        time.sleep(0.5)

    @classmethod
    def get_combo(cls):
        return cls.combo_all
    
    @classmethod
    def reset(cls):
        cls.combo_all = 0

    @classmethod
    def uppdate_screen(cls):
        """
        スクリーン情報を更新する
        担当: C0A23019
        """
        cls.score.update(cls.screen)
        # cls.combo.update(cls.screen)

    @classmethod
    def set_score(cls, score:Score):
        """
        scoreをセットする
        担当: C0A23019

        :param Score score: スコアクラス
        """
        cls.score = score
    
    @classmethod
    def set_screen(cls, screen:pg.surface):
        """
        screenをセットする
        担当: C0A23019

        :param pg.surface screen: スクリーン情報
        """
        cls.screen = screen
