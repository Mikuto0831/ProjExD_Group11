import os
from random import randint as ran
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 定数宣言部
HEIGHT = 650
WIDTH = 450
pg.mixer.init

# 関数宣言部
def elise(ball_lst: list,judge: list)-> list:
    """
    引数:ball_lst　ボールの色やなしを保持するリスト
    引数:judge判定された
    コンボ判定されたball_lstを0にする
    judge =[[0,1],[0,2]]etc
    """
    for i in judge:
        ball_lst[i[0]][i[1]] =0
    return ball_lst
# クラス宣言部
        
        
class PuzzleList():
    """
    パズル画面を管理するリストに関係するクラス
    """

    def __init__(self):
        """
        """
        self.lis = [[ran(1,5) for d in range(6)] for n in range(6)]
    
    def get_lis(self):
        return self.lis
    
    def move_lect(pos:list, key)-> int:
        """
        引数1: 現在の位置 (x, y) または (X, Y) を含むリスト
        引数2: イベントキー（pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT）
        返り値：int型のxとy
        """
        x, y = pos # xとyを引数posとする
        if key == pg.K_UP and y > 0: # 上矢印キーが押されたときかつyがフレーム内
            y -= 1 # yを-1する
        elif key == pg.K_DOWN and y < 6: # 下矢印キーが押されたときかつyがフレーム内
            y += 1 # yを-1する
        elif key == pg.K_LEFT and x > 0: # 左矢印キーが押されたときかつxがフレーム内
            x -= 1 # xを-1する
        elif key == pg.K_RIGHT and x < 6: # 右矢印キーが押されたときかつxがフレーム内
            x += 1 # xを+1する
        return x, y # xとyを返す
    
def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_imgs = [bg_img, pg.transform.flip(bg_img, True, False)]
    # ここから 練習2
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.flip(kk_img, True, False)
    # ここから 練習8-1 rectの初期座標設定
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300,200
    # ここまで
    x = 0
    y = 0
    X = 0
    Y = 0
    mode = 0
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
                if mode == 0: #　モード０：始める場所を設定する　                     
                    for event in pg.event.get():
                        if event.type == pg.QUIT: return
                        elif event.type == pg.KEYDOWN:
                            x, y = PuzzleList.move_lect([x, y], event.key)
                            if event.key == pg.K_RETURN: # ENTERが押されたとき
                                mode = 1 #modeを1にする
                elif mode == 1: # モード１：ゲームを開始する
                    if event.type == pg.KEYDOWN:
                        X, Y = PuzzleList.move_lect([X, Y], event.key)
                        if (X,Y) != (x,y): # X,Yとx,yの値が一致していないとき
                            PuzzleList.lis[X][Y],PuzzleList.lis[x][y] = PuzzleList.lis[x][y],PuzzleList.lis[X][Y] # PuzzleListクラスのlisの中身を入れ替える
                            
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


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()