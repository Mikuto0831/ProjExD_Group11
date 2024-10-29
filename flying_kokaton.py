import os
from random import randint as ran
import sys
import pygame as pg
import pygame
from typing import List
import sys
import pygame
from pygame.locals import *

from module.otamesi import Text, draw_text, event_loop

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 定数宣言部
HEIGHT = 650
WIDTH = 450

# クラス宣言部


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


# def homemenu(screen):
#     font1 = pygame.font.SysFont("yumincho", 50)
#     text1 = font1.render("名前を入力", True, (0, 255, 0))
#     screen.blit(text1, (40, 30))
#     text = Text()  # テキスト処理のロジックTextクラスをインスタンス化
#     pygame.key.start_text_input()  # input, editingイベントをキャッチするようにする
#     draw_text(format(text, screen))



def main():
    #初期値宣言部
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

    font = pygame.font.SysFont("yumincho", 30)

    start_img = pg.image.load("fig/0D9A6898-HDR.jpg")

    start_rct = start_img.get_rect()
    start_rct.center = 300, 200

    text = Text()

    event_trigger = {
        K_BACKSPACE: text.delete_left_of_cursor,
        K_DELETE: text.delete_right_of_cursor,
        K_LEFT: text.move_cursor_left,
        K_RIGHT: text.move_cursor_right,
        K_RETURN: text.enter,
    }

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
                status = "home:1"
            case "home:1":
                if pg.key.get_pressed()[pg.K_LALT]:
                        status = "game:0"
                        continue
                for event in pg.event.get():
                    screen.blit(start_img, start_rct)
                    # キーダウンかつ、全角のテキスト編集中でない
                    if event.type == KEYDOWN and not text.is_editing:
                        if event.key in event_trigger.keys():
                            input_text = event_trigger[event.key]()
                    # 入力の確定
                        if event.unicode in ("\r", "") and event.key == K_RETURN:
                            print(input_text)  # 確定した文字列を表示
                            draw_text(text, screen)  # テキストボックスに"|"を表示
                            input_text = text, screen  # "|"に戻す
                            break
                    elif event.type == TEXTEDITING:  # 全角入力
                        input_text = text.edit(event.text, event.start)
                    elif event.type == TEXTINPUT:  # 半角入力、もしくは全角入力時にenterを押したとき
                        input_text = text.input(event.text)
                    # 描画しなおす必要があるとき
                    if event.type in [KEYDOWN, TEXTEDITING, TEXTINPUT]:
                        draw_text(input_text, screen)
                    font1 = pygame.font.SysFont("yumincho", 50)
                    text1 = font1.render("名前を入力", True, (0, 255, 0))
                    screen.blit(text1, (100, 130))
                    text = Text()  # テキスト処理のロジックTextクラスをインスタンス化
                    pygame.key.start_text_input()  # input, editingイベントをキャッチするようにする
                    draw_text(text, screen)
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


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()