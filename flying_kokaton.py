import numpy as np
import sys
import pygame as pg
import pygame
from pygame.locals import *
from module.audios.audio import Audio
from module.name.name import Text, event_loop
from module.scores.scores import Score, ScoreLogDAO
from module.combos.combo import Combo
from random import randint as ran


# 定数宣言部
HEIGHT = 650
WIDTH = 450
RAD =25#こうかとんボールの半径
BALL_X=75#ボールのⅹ距離
BALL_Y=75
TIMES  = 480

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
    return lis



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

        self.kk_img = pg.image.load("./ex5/fig/3.png")

        self.kk_img = pg.transform.flip(self.kk_img, True, False)
        self.kk_img.fill((255,255,255,128),None, pg.BLEND_RGBA_MULT)
        self.image = pg.Surface((2*RAD, 2*RAD))
        self.i=num[0]
        self.j=num[1]
        self.col =__class__.color[ball_list[self.j][self.i]]
        self.image.set_alpha(128)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.i*BALL_X+12,self.j*BALL_Y+215
    
    def update(self,screen:pg.surface):
        screen.set_alpha(128)
        screen.set_colorkey((0, 0, 0))
        if self.col is not None:
            # コンボして表示しない時を除いて表示する
            pg.draw.circle(screen, self.col, (self.rect.centerx+RAD,self.rect.centery+RAD), RAD)
            screen.blit(self.kk_img, [self.rect.centerx, self.rect.centery])
        self.kill()

class Time_circulate():
    """
    タイマーに関わるクラス
    """
    def __init__(self,past_time):
        self.past_time= past_time
        self.font=pg.font.SysFont("ha正楷書体pro",30)
        self.mode=0
    
    def set_mode(self,count):
        self.mode =count
    
    def settime(self,past_time):
        self.past_time=past_time
    def update(self,tmr,screen):
        if self.mode==0:
            txt = self.font.render(f"Operatinon time is 7second",True,(0,0,0))
        else:
            txt = self.font.render(f"Operatinon limit {7-(tmr-self.past_time)//60}second",True,(0,0,0))
        screen.blit(txt,[0,100])

class PuzzleList():
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
        3つ以上繋げることがないようにする
        """
        self.lis=self.puzzle_generate(6,6)
    
    def get_lis(self):
        return self.lis
    
    def set_lis(self, lis:list[list]):
        self.lis = lis

    def move_lect(pos:list, key)-> int:
        """
        引数1: 現在の位置 (x, y) または (X, Y) を含むリスト
        引数2: イベントキー（pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT）
        返り値：int型のxとy
        """
        y, x = pos # xとyを引数posとする
        if key == pg.K_UP and y > 0: # 上矢印キーが押されたときかつyがフレーム内
            y -= 1 # yを-1する
            if y <0:
                y = 0
        elif key == pg.K_DOWN and y < 6: # 下矢印キーが押されたときかつyがフレーム内
            y += 1 # yを-1する
            if y>5:
                y = 5
        elif key == pg.K_LEFT and x > 0: # 左矢印キーが押されたときかつxがフレーム内
            x -= 1 # xを-1する
            if x < 0:
                x = 0
        elif key == pg.K_RIGHT and x < 6: # 右矢印キーが押されたときかつxがフレーム内
            x += 1 # xを+1する
            if x >5:
                x = 5
        return y, x # xとyを返す        

    def puzzle_generate(self,rows:int, cols:int)->np.ndarray:
        array = np.array([[0] * cols for _ in range(rows)])  # 初期化

        for i in range(rows):
            for j in range(cols):
                while True:
                    num = np.random.randint(1, 6)  # 1から5の間のランダムな数
                    # 同じ行または列に3つ連続していないかを確認
                    if (j < 2 or array[i][j-1] != num or array[i][j-2] != num) and \
                    (i < 2 or array[i-1][j] != num or array[i-2][j] != num):
                        array[i][j] = num
                        break
        return array                        

class ComboLog:
    """
    combo表示に関わるクラス
    """
    def __init__(self) -> None:
        self.combo = 0
        # 表示系
        self.font = pg.font.Font(None, 50)
        self.color = (0, 0, 255)
        self.image = self.font.render(f"Now Combo: {self.combo}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 127, 55
    
    def add_combo(self, combo:int):
        self.combo += combo
    
    def reset_combo(self):
        self.combo = 0

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"Now Combo: {self.combo}", 0, self.color)
        screen.blit(self.image, self.rect)

class NowLoding:
    """
    ロード画面に関わるクラス
    """
    def __init__(self, width:int, height:int) -> None:
        self.font = pg.font.Font(None, 50)
        self.color = (0, 0, 255)
        self.image = self.font.render("Now Loding...", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = width//2, height//2

    def update(self, screen: pg.Surface):
        screen.blit(self.image, self.rect)

# main関数
def main():
    pg.display.set_caption("パズル&こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    # ローディング画面
    now_loding = NowLoding(width=WIDTH, height=HEIGHT)
    now_loding.update(screen)
    pg.display.update()

    # 背景画像の読み込み
    bg_img = pg.image.load("./ex5/fig/pg_bg.jpg")
    bg_imgs = [bg_img, pg.transform.flip(bg_img, True, False)]
    
    # キャラクター画像の読み込みと設定
    kk_img = pg.image.load("./ex5/fig/3.png")
    kk_img = pg.transform.flip(kk_img, True, False)
    ball_img = pg.image.load("./ex5/fig/カーソル.png")
    # キャラクターの初期座標設定
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300,200
    # ここまで
    score_log_DAO = ScoreLogDAO()
    score = Score(score_log_DAO)
    Combo.set_score(score)
    Combo.set_screen(screen)
    show_combo = ComboLog()
    drop_list_x = 0
    drop_list_y = 0
    change_list_X = 0
    change_list_Y = 0
    tmr = 0 # 時間保存
    tmrs=Time_circulate(tmr)
    lis_m = PuzzleList()
    lis = lis_m.get_lis()
    
    ball = pg.sprite.Group()

    audio: Audio = Audio()
    text:Text

    """
    status変数について
    本変数では画面・実行機能を選択する値を管理します。
    次の状態を代入してあげるだけで簡単に遷移を実現できます
    以下の範囲に基づいて使用してください

    例
    ホーム画面に関する機能
    status = "home:0"
    """
    status:str = "home:0"

    while True:
        # 共通処理部
        event_list = pg.event.get()
        for event in event_list:
            if event.type == pg.QUIT: return

        # 各statusに基づく処理部
        match status:
            case "home:0":
                pg.key.start_text_input()  # テキスト入力を開始
                font = pg.font.SysFont("yumincho", 30)
                text = Text(audio)  # Text クラスをインスタンス化
                audio.bgm_play()
                audio.open_window_play()
                status = "home:1"
            case "home:1":
                player_name = event_loop(screen, text, font)  # 名前入力後、イベントループから取得
                print(f"Player Name: {player_name}")
                if not player_name:
                    player_name = None
                elif player_name == "log":
                    status = "log:0"
                else:
                    status = "game:0"
            
            case "game:0":
                """
                ゲームの初期化
                """
                for i in range(len(lis)):
                    for j in range(len(lis[i])):
                        ball.add(KoukatonDrop(lis,(i,j)))
                status="game:1"
                audio.open_window_play()

            case "game:1":                    
                for i in range(4):
                    screen.blit(bg_imgs[i%2], [-(tmr % 3200)+1600*i, 0])
                  
                key_lst = pg.key.get_pressed() # 練習8-3 全キーの押下状態取得
                
                for event in event_list:
                    if event.type == pg.QUIT: return
                    elif event.type == pg.KEYDOWN:
                        drop_list_x, drop_list_y = PuzzleList.move_lect([drop_list_x, drop_list_y], event.key)
                        if event.key == pg.K_RETURN: # ENTERが押されたとき
                                status = "game:2"
                                tmrs.settime(tmr)
                for i in range(len(lis)):
                    for j in range(len(lis[i])):
                        ball.add(KoukatonDrop(lis,(i,j)))
                    ball.update(screen)                               
                    ball.draw(screen)
                screen.blit(ball_img,[drop_list_y*75+12,drop_list_x*75+215])
                tmrs.set_mode(0)
                tmrs.update(tmr,screen)    
                score.update(screen)
                show_combo.update(screen)

            case "game:2":
                tmrs.set_mode(1)
                show_combo.reset_combo() 
                for event in event_list:
                    if event.type == pg.QUIT: return
                    elif event.type == pg.KEYDOWN:
                        change_list_X,change_list_Y=drop_list_x,drop_list_y
                        change_list_X,change_list_Y = PuzzleList.move_lect([change_list_X, change_list_Y], event.key)
                        if (change_list_X,change_list_Y) != (drop_list_x,drop_list_y): # X,Yとx,yの値が一致していないとき
                            lis[change_list_X][change_list_Y],lis[drop_list_x][drop_list_y] = lis[drop_list_x][drop_list_y],lis[change_list_X][change_list_Y] # PuzzleListクラスのlisの中身を入れ替える
                            drop_list_x,drop_list_y = change_list_X,change_list_Y
                            audio.cursor_control_play()
                            print(lis)
                        if event.key == pg.K_RETURN: # ENTERが押されたとき
                            status = "game:3"
                            
                if tmr-tmrs.past_time>=TIMES:
                    status = "game:3"

                for i in range(4):
                    screen.blit(bg_imgs[i%2], [-(tmr % 3200)+1600*i, 0])
                for i in range(len(lis)):
                    for j in range(len(lis[i])):
                        ball.add(KoukatonDrop(lis,(i,j)))
                    ball.update(screen)                               
                    ball.draw(screen)
                screen.blit(ball_img,[drop_list_y*75+12,drop_list_x*75+215])
                tmrs.update(tmr,screen)
                score.update(screen)
                show_combo.update(screen)

            case "game:3":
                check = Combo(lis)
                co = check.get_count()
                if co <= 0:
                    status="game:1"
                check = check.get_lis()
                check = drop_down(check)
                show_combo.add_combo(Combo.get_combo())
                Combo.reset()
                lis_m.set_lis(check)
                print(check)
                screen.blit(ball_img,[drop_list_y*75+12,drop_list_x*75+215])
                tmrs.update(tmr,screen)
                score.update(screen)
                show_combo.update(screen)
                
            
            case "log:0":
                lis_log = score_log_DAO.get()
                screen.fill((255, 255, 255))
                font = pygame.font.Font(None, 20)
                sor = sorted(lis_log, reverse=True, key=lambda x: x[3])
                # スコア表示
                for i, row in enumerate(sor):
                    screen.blit(font.render(str(row[1:]), True, (0,0,255)), (20, 50 + i*50))
                status = "log:1"
            case "log:1":
                for event in event_list:
                    if event.type == pg.KEYDOWN:
                        status = "home:0"

        # 共通処理部
        pg.display.update()
        tmr += 1        
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
