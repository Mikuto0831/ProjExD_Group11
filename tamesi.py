import os
import sys
import uuid
import pygame as pg
from pygame.locals import *
from ex5.module.name import Text, draw_text
from random import randint as ran
from typing import List


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
    

# クラス宣言部

# テキスト描画用関数
def draw_text(screen, font, text, position):
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, position)

def event_loop(screen, text, font):
    """名前入力時のイベントループ処理"""
    editing_text = ""  # 変換中のテキストを一時的に格納

    while True:
        screen.fill((255, 255, 255))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:  # Enterキーで入力を確定
                    return str(text)
                elif event.key == pg.K_BACKSPACE:  # バックスペースで文字削除
                    text.delete_left_of_cursor()
                elif event.key == pg.K_LEFT:  # カーソルを左に移動
                    text.move_cursor_left()
                elif event.key == pg.K_RIGHT:  # カーソルを右に移動
                    text.move_cursor_right()

            elif event.type == pg.TEXTEDITING:
                # 編集中のテキストとカーソル位置を取得
                editing_text = event.text
                editing_cursor_pos = event.start
                displayed_text = text.edit(editing_text, editing_cursor_pos)
                draw_text(screen, font, displayed_text, (50, 300))

            elif event.type == pg.TEXTINPUT:
                # 確定したテキストを追加
                text.input(event.text)
                editing_text = ""  # 確定後は変換中のテキストをリセット

        # 現在の入力文字列を描画（変換中のテキストも含む）
        if editing_text:
            displayed_text = text.edit(editing_text, len(editing_text))
        else:
            displayed_text = str(text)
        
        draw_text(screen, font, displayed_text, (50, 300))
        pg.display.update()

# メイン処理関数
def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    # 名前入力用のTextインスタンスを作成
    font = pg.font.SysFont("yumincho", 30)
    text = Text()  # Text クラスをインスタンス化
    pg.key.start_text_input()  # テキスト入力を開始

    # 名前入力待ち
    player_name = event_loop(screen, text, font)  # 名前入力後、イベントループから取得
    pg.key.stop_text_input()  # テキスト入力を停止

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

    start_img = pg.image.load("fig/0D9A6898-HDR.jpg")

    start_rct = start_img.get_rect()
    start_rct.center = 300, 200

    text = Text()

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

    while True:
        # 共通処理部

        # 各statusに基づく処理部
        match status:
            case "home:0":
                for event in pg.event.get():
                    # キーが押されたらゲーム画面へ
                    if event.type == pg.QUIT:
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

                score.update(screen)

        # 共通処理部
        
        pg.display.update()
        tmr += 1        
        clock.tick(200)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
