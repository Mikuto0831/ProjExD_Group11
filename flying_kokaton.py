import os
from random import randint as ran
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 定数宣言部
HEIGHT = 650
WIDTH = 450

# 関数宣言部

# クラス宣言部
class PuzzleList:
    """
    パズル画面を管理するリストに関係するクラス
    担当:瀬尾
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
    combo_lis = []
    combo_count = 0

    def __init__(self, lis:list[list]):
        self.lis = lis
        self.row_combo()
        self.column_combo()

    def row_combo(self):
       for i in range(6):
            stack = 0
            for j in range(4):
                if stack > 0:
                    stack -= 1
                    continue
                combo_len = 3
                if self.lis[i][j] == self.lis[i][j+1] and self.lis[i][j] == self.lis[i][j+2]:
                    if j <= 2 and self.lis[i][j] == self.lis[i][j+3]:
                        combo_len += 1
                        if j <= 1 and self.lis[i][j] == self.lis[i][j+4]:
                            combo_len += 1
                            if j <= 0 and self.lis[i][j] == self.lis[i][j+5]:
                                combo_len += 1
                    self.combo_lis.append([1, i, j, combo_len])
                    self.combo_count += 1
                    stack += combo_len-1
                    print("j", [i, j], combo_len)
    
    def column_combo(self):
        for j in range(6):
            stack = 0
            for i in range(4):
                if stack > 0:
                    stack -= 1
                    continue
                combo_len = 3
                if self.lis[i][j] == self.lis[i+1][j] and self.lis[i][j] == self.lis[i+2][j]:
                    if i <= 2 and self.lis[i][j] == self.lis[i+3][j]:
                        combo_len += 1
                        if i <= 1 and self.lis[i][j] == self.lis[i+4][j]:
                            combo_len += 1
                            if i <= 0 and self.lis[i][j] == self.lis[i+5][j]:
                                combo_len += 1
                    self.combo_lis.append([2, i, j, combo_len])
                    self.combo_count += 1
                    stack += combo_len-1
                    print("i", [i, j], combo_len)

    
    def get_count(self):
        return self.combo_count
    
    def elise(self, lis:list):
        #引数:lst　ボールの種類を保持するリスト
        #コンボ判定されたball_lstを0にする
        for set in self.combo_lis:
            combo_type, i, j, combo_len = set
            if combo_type == 1:
                for n in range(combo_len):
                    lis[i][j+n] = 0
            elif combo_type == 2:
                for n in range(combo_len):
                    lis[i+n][j] = 0
        return lis
            
lis = [[1, 1, 1, 2, 2, 2], 
       [1, 2, 2, 2, 2, 2],
       [1, 3, 3, 2, 2, 2],
       [4, 5, 4, 4, 4, 4],
       [5, 5, 5, 3, 3, 3],
       [6, 5, 6, 6, 6, 6]]
check = Combo(lis)

print(check.get_count())
print(check.elise(lis))




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

#         # 共通処理部
        
#         pg.display.update()
#         tmr += 1        
#         clock.tick(200)


# if __name__ == "__main__":
#     pg.init()
#     main()
#     pg.quit()
#     sys.exit()