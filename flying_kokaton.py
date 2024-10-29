import os
from random import randint as ran
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 定数宣言部


# 関数宣言部


# クラス宣言部





class stage():
    """
    パズル画面を管理するリストに関係するクラス
    """

    def __init__(self):
        self.lis = [[ran(1,5) for d in range(6)] for n in range(6)]
    
    def get_lis(self):
        return self.lis



lis = stage()
print(lis.get_lis())


# def main():
#     pg.display.set_caption("はばたけ！こうかとん")
#     screen = pg.display.set_mode((800, 600))
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

    tmr = 0 # 時間保存

    """
    status変数について
    本変数では画面・実行機能を選択する値を管理します。
    次の状態を代入してあげるだけで簡単に遷移を実現できます
    以下の範囲に基づいて使用してください

    {機能名}:{状態番号}

    例
    ホーム画面に関する機能
    status = "home:0"
    """
    status:str = "home:0"
    # ここまで

    while True:
        # 共通処理部

        # 各statusに基づく処理部
        match status:
            case "home:0":
                for event in pg.event.get():
                    # キーが押されたらゲーム画面へ
                    if event.type == pg.KEYDOWN:
                        status = "game:0"
                        break
            case "game:0":                                 
                for event in pg.event.get():
                    if event.type == pg.QUIT: return

                key_lst = pg.key.get_pressed() # 練習8-3 全キーの押下状態取得
                
                # 練習8-4 方向キーの押下状態を繁栄
                kk_rct_tmp = (
                    key_lst[pg.K_RIGHT] * 2 + key_lst[pg.K_LEFT] * (-1) - 1,
                    key_lst[pg.K_UP] * (-1) + key_lst[pg.K_DOWN] * 1
                    )
                kk_rct.move_ip(kk_rct_tmp)
                


                # 練習7
                for i in range(4):
                    screen.blit(bg_imgs[i%2], [-(tmr % 3200)+1600*i, 0])
                
                screen.blit(kk_img, kk_rct)

        # 共通処理部
        
        pg.display.update()
        tmr += 1        
        clock.tick(200)


# if __name__ == "__main__":
#     pg.init()
#     main()
#     pg.quit()
#     sys.exit()