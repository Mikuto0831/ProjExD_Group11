import os
import random
import sys
import time
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 定数宣言部
HEIGHT = 650
WIDTH = 450
RAD =25#こうかとんボールの半径
BALL_X=75#ボールのⅹ距離
BALL_Y=75

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

class KoukatonDrop(pg.sprite.Sprite):
    """
    こうかとんに関するクラス
    """
    color=(
        None,
        (255,0,0),#赤
        (0,0,255),#青
        (0,255,0),#緑
        (255,255,0),#黄
        (136,72,152)#紫
    )
    def __init__(self,ball_list: list[list],num: tuple):
        super().__init__()
        self.kk_img = pg.image.load("fig/3.png")
        self.kk_img = pg.transform.flip(self.kk_img, True, False)
        self.kk_img.fill((255,255,255,128),None, pg.BLEND_RGBA_MULT)
        print(ball_list)
        #self.image = pg.Surface([WIDTH,HEIGHT])
        self.image = pg.Surface((2*RAD, 2*RAD))
        self.i=num[0]
        self.j=num[1]
        self.col =__class__.color[ball_list[self.i][self.j]]
        self.image.set_alpha(128)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.i*BALL_X,self.j*BALL_Y
                

    
    def update(self,screen:pg.surface):
        screen.set_alpha(128)
        screen.set_colorkey((0, 0, 0))
        if self.col is not None:
            # コンボして表示しない時を除いて表示する
            pg.draw.circle(screen, self.col, (self.rect.centerx+RAD,self.rect.centery+RAD), RAD)
            screen.blit(self.kk_img, [self.rect.centerx, self.rect.centery])
        self.kill()




class PuzzleList():
    """
    パズル画面を管理するリストに関係するクラス
    """

    def __init__(self):
        """
        3つ以上繋げることがないようにする
        """
        self.lis=self.puzzle_generate(6,6)
        

    def puzzle_generate(self,rows, cols):
        array = [[0] * cols for _ in range(rows)]  # 初期化

        for i in range(rows):
            for j in range(cols):
                while True:
                    num = random.randint(1, 5)  # 0から9の間のランダムな数
                    # 同じ行または列に3つ連続していないかを確認
                    if (j < 2 or array[i][j-1] != num or array[i][j-2] != num) and \
                    (i < 2 or array[i-1][j] != num or array[i-2][j] != num):
                        array[i][j] = num
                        break

        return array                        

    def get_lis(self):
        return self.lis
    



def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_imgs = [bg_img, pg.transform.flip(bg_img, True, False)]
    #ここから 練習8-1 rectの初期座標設定
    #ここまで

    tmr = 0 # 時間保存

    ball = pg.sprite.Group()
    lis= PuzzleList()
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
        
        event_list = pg.event.get()

        # 各statusに基づく処理部
        match status:
            case "home:0":
                for event in event_list:
                    if event.type == pg.QUIT: return
                    # キーが押されたらゲーム画面へ
                    if event.type == pg.KEYDOWN:
                        status = "game:0"
                        break
            
            case "game:0":
                """
                ゲームの初期化
                """
                t = lis.get_lis()
                for i in range(len(t)):
                    for j in range(len(t[i])):
                        ball.add(KoukatonDrop(lis.get_lis(),(i,j)))
                status="game:1"

            case "game:1":  
                if tmr%400==0:
                    for i in range(len(t)):
                        for j in range(len(t[i])):
                            ball.add(KoukatonDrop(lis.get_lis(),(i,j)))
                    ball.update(screen)                               
                    ball.draw(screen)
                    
                    lis= PuzzleList()

                

        # 共通処理部
        pg.display.update()
        tmr += 1        
        clock.tick(200)
        print(status)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()