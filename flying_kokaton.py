import os
from random import randint as ran
import sys
import time
import uuid
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 定数宣言部
HEIGHT = 650
WIDTH = 450



# クラス宣言部
class Score:
    """
    スコア管理システム
    """
    def __init__(self, player_name:str = "guest"):
        """
        スコアをユーザと紐づけます
        担当 : c0a23019
        
        :param str player_name: プレイヤー名
        """
        # スコア情報系
        self.value = 0
        self.player_name = player_name
        self.player_uuid = uuid.uuid1()
        # TODO: 遊んだ時間のlog取得

        # 表示系
        self.font = pg.font.Font(None, 50)
        self.color = (0, 0, 255)
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 100, 100

    def update(self, screen: pg.Surface):
        """
        スコア表示

        :param Surface screen: スクリーン情報
        """
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)
        screen.blit(self.image, self.rect)

    def add(self, add_score:int):
        """
        スコア加算

        :param int add_score: 加算したい値
        """
        self.value += add_score

    def __delattr__(self) -> None:
        # TODO: クラス削除時にスコアをファイルに保存する
        pass

      
class PuzzleList:
    """
    パズル画面を管理するリストに関係するクラス
    担当:瀬尾
    get_lis():生成した盤面を取得する
    selt_lis(list[list]):盤面をlist[list]に置き換える
    """

    def __init__(self):
        """
        盤面を生成する
        list[縦行数][横列数]
        """
        self.lis = [[ran(1,5) for d in range(6)] for n in range(6)]
    
    def get_lis(self):
        return self.lis
    
    def set_lis(self, lis:list[list]):
        self.lis = lis


class Combo:
    """
    コンボの判定をするクラス
    コンボの判定
        1:横
        2:縦
    担当:瀬尾
    """
    
    combo_all = 0

    def __init__(self, lis:list[list]):
        self.combo_count = 0
        self.lis = lis
        check = 0
        while True:
            self.cross_combo()
            self.row_combo()
            self.column_combo()
            if check == self.combo_count:
                break
            check = self.combo_count
        self.elise(self.lis)
    
    def cross_combo(self):
        for i in range(1, 5):
            stack = 0
            for j in range(4):
                if stack > 0:
                    stack -= 1
                    continue
                if jadge_double(self.lis[i][j], self.lis[i][j+1], self.lis[i][j+2], self.lis[i-1][j+1], self.lis[i+1][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]) and jadge_combo(self.lis[i][j], self.lis[i-1][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+1]):
                    stack += 2
                    print("cross", [i, j])
                    self.combo_add()
                    self.change(3, i, j, ele = self.lis[i][j])
                    time.sleep(0.5)
                    break

    def row_combo(self):
       for i in range(6):
            stack = 0
            for j in range(4):
                if stack > 0:
                    stack -= 1
                    continue
                combo_len = 3
                if jadge_double(self.lis[i][j], self.lis[i][j+1], self.lis[i][j+2]) and jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]):
                    if j <= 2 and jadge_combo(self.lis[i][j], self.lis[i][j+3]):
                        combo_len += 1
                        if j <= 1 and jadge_combo(self.lis[i][j], self.lis[i][j+4]):
                            combo_len += 1
                            if j <= 0 and jadge_combo(self.lis[i][j], self.lis[i][j+5]):
                                combo_len += 1
                    self.combo_count += 1
                    stack += combo_len-1
                    print("row", [i, j], combo_len)
                    self.combo_add()
                    self.change(1, i, j, self.lis[i][j],combo_len)
                    time.sleep(0.5)
                    break
                    
    def column_combo(self):
        for j in range(6):
            stack = 0
            for i in range(4):
                if stack > 0:
                    stack -= 1
                    continue
                combo_len = 3
                if jadge_double(self.lis[i][j], self.lis[i+1][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i+1][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]):
                    if i <= 2 and jadge_combo(self.lis[i][j], self.lis[i+3][j]):
                        combo_len += 1
                        if i <= 1 and self.lis[i][j] == self.lis[i+4][j]:
                            combo_len += 1
                            if i <= 0 and jadge_combo(self.lis[i][j], self.lis[i+5][j]):
                                combo_len += 1
                    self.combo_count += 1
                    stack += combo_len-1
                    print("column", [i, j], combo_len)
                    self.combo_add()
                    self.change(2, i, j, self.lis[i][j],combo_len)
                    time.sleep(0.5)
                    break

    def get_count(self):
        return self.combo_count
    
    def get_lis(self):
        return self.lis
    
    def change(self, combo_type:int, i:int, j:int, ele:int = 0, combo_len:int = 1):
        #引数:lst　ボールの種類を保持するリスト
        #コンボ判定されたball_lstを0にする
        if ele >= 10:
            ele = ele - 10
        if combo_type == 1:
            for n in range(combo_len):
                lis[i][j+n] = 10+ele
        elif combo_type == 2:
            for n in range(combo_len):
                lis[i+n][j] = 10+ele
        elif combo_type == 3:
            for n in range(3):
                lis[i][j+n] = 10+ele
            lis[i-1][j+1] = 10+ele
            lis[i+1][j+1] = 10+ele

        self.lis = lis

    
    def elise(self, lis:list[list]):
        for i in range(len(lis)):
            for j in range(len(lis[i])):
                if lis[i][j] >= 10:
                    lis[i][j] = 0
        self.lis = lis
    
    @classmethod
    def combo_add(self):
        Combo.combo_all += 1

    @classmethod
    def get_combo(self):
        return Combo.combo_all
    
    @classmethod
    def reset(self):
        Combo.combo_all = 0

# 関数宣言部
def drop_down(lis:list[list])->list[list]:
    check = True
    while check:
        for j in range(6):
            if lis[0][j] == 0:
                lis[0][j] = ran(1, 5)
        for i in range(1, 6):
            for j in range(6):
                if lis[i][j] == 0:
                    lis[i][j] = lis[i-1][j]
                    lis[i-1][j] = 0
        
        jadge = [0 for n in range(6)]
        for i in range(6):
            if all(lis[i]):
                jadge[i] = 1
        if all(jadge):
            check = False
    time.sleep(1)
    return lis


def jadge_combo(a, b):
    if a == b or a + 10 == b or a == b + 10:
        return True
    else:
        return False

def jadge_double(a:int = 10, b:int = 10, c:int = 10, d:int = 10, e:int = 10, f:int = 10, g:int = 10, h:int = 10, i:int = 10):
    if a >= 10 and b >= 10 and c >= 10 and d >= 10 and e >= 10 and f >= 10 and g >= 10 and h >= 10 and i >= 10:
        return False
    else:
        return True

# 実行確認用
lis = [[1, 1, 1, 2, 4, 2], 
       [2, 2, 2, 3, 4, 4], 
       [3, 2, 2, 2, 4, 5], 
       [4, 4, 2, 5, 4, 5], 
       [3, 1, 3, 4, 4, 5], 
       [3, 3, 3, 2, 4, 1]]
# lis_m = PuzzleList()
# lis = lis_m.get_lis()
print(lis[0], "\n", lis[1], "\n", lis[2], "\n", lis[3], "\n", lis[4], "\n", lis[5], "\n")
while True:
    check = Combo(lis)
    co = check.get_count()
    if co <= 0:
        break
    lis = check.get_lis()
    print(lis[0], "\n", lis[1], "\n", lis[2], "\n", lis[3], "\n", lis[4], "\n", lis[5])
    print()
    lis = drop_down(lis)
    print()
    print(lis[0], "\n", lis[1], "\n", lis[2], "\n", lis[3], "\n", lis[4], "\n", lis[5])
    print("combo",Combo.get_combo(), "co", co)
Combo.reset()

# # main関数
# def main():
#     pg.display.set_caption("はばたけ！こうかとん")
#     screen = pg.display.set_mode((WIDTH, HEIGHT))
#     clock  = pg.time.Clock()
#     bg_img = pg.image.load("fig/pg_bg.jpg")
#     bg_imgs = [bg_img, pg.transform.flip(bg_img, True, False)]
#     # ここから 練習2
#     kk_img = pg.image.load("fig/3.png")
#     kk_img = pg.transform.flip(kk_img, True, False)
#     # ここから 練習8-1 rectの初期座標設定
#     kk_rct = kk_img.get_rect()
#     kk_rct.center = 300,200
#     # ここまで

#     score = Score()

#     tmr = 0 # 時間保存

#     """
#     status変数について
#     本変数では画面・実行機能を選択する値を管理します。
#     次の状態を代入してあげるだけで簡単に遷移を実現できます
#     以下の範囲に基づいて使用してください

#     {機能名}:{状態番号}

#     例
#     ホーム画面に関する機能
#     status = "home:0"
#     """
#     status:str = "home:0"
#     # ここまで

#     while True:
#         # 共通処理部

#         # 各statusに基づく処理部
#         match status:
#             case "home:0":
#                 for event in pg.event.get():
#                     # キーが押されたらゲーム画面へ
#                     if event.type == pg.KEYDOWN:
#                         status = "game:0"
#                         break
#             case "game:0":                                 
#                 for event in pg.event.get():
#                     if event.type == pg.QUIT: return

#                 key_lst = pg.key.get_pressed() # 練習8-3 全キーの押下状態取得
                
#                 # 練習8-4 方向キーの押下状態を繁栄
#                 kk_rct_tmp = (
#                     key_lst[pg.K_RIGHT] * 2 + key_lst[pg.K_LEFT] * (-1) - 1,
#                     key_lst[pg.K_UP] * (-1) + key_lst[pg.K_DOWN] * 1
#                     )
#                 kk_rct.move_ip(kk_rct_tmp)
                


#                 # 練習7
#                 for i in range(4):
#                     screen.blit(bg_imgs[i%2], [-(tmr % 3200)+1600*i, 0])
                
#                 screen.blit(kk_img, kk_rct)

#                 score.update(screen)

#         # 共通処理部
        
#         pg.display.update()
#         tmr += 1        
#         clock.tick(200)


# if __name__ == "__main__":
#     pg.init()
#     main()
#     pg.quit()
#     sys.exit()