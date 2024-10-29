import os
from random import randint as ran
import sys
import pygame as pg
from typing import List
import pygame
from pygame.locals import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 定数宣言部
HEIGHT = 650
WIDTH = 450

# 関数宣言部
def draw_text(text: str) -> None:
    """
    入力文字を描画するための関数
    """
    text_surface = font.render(text, True, (0, 0, 0))
    screen.fill((112, 225, 112))
    # テキストに応じて上下左右中央揃えにする
    center_w = (800 / 2) - (text_surface.get_width() / 2)
    center_h = (600 / 2) - (text_surface.get_height() / 2)
    screen.blit(text_surface, (center_w, center_h))
    pygame.display.update()


def event_loop():
    # テキスト入力時のキーとそれに対応するイベント
    event_trigger = {
        K_BACKSPACE: text.delete_left_of_cursor,
        K_DELETE: text.delete_right_of_cursor,
        K_LEFT: text.move_cursor_left,
        K_RIGHT: text.move_cursor_right,
        K_RETURN: text.enter,
    }
    while True:
        font1 = pygame.font.SysFont("yumincho", 50)
        text1 = font1.render("名前を入力", True, (255, 0, 0))
        screen.blit(text1, (40, 30))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            # キーダウンかつ、全角のテキスト編集中でない
            elif event.type == KEYDOWN and not text.is_editing:
                if event.key in event_trigger.keys():
                    input_text = event_trigger[event.key]()
                # 入力の確定
                if event.unicode in ("\r", "") and event.key == K_RETURN:
                    print(input_text)  # 確定した文字列を表示
                    draw_text(format(text))  # テキストボックスに"|"を表示
                    input_text = format(text)  # "|"に戻す
                    break
            elif event.type == TEXTEDITING:  # 全角入力
                input_text = text.edit(event.text, event.start)
            elif event.type == TEXTINPUT:  # 半角入力、もしくは全角入力時にenterを押したとき
                input_text = text.input(event.text)
            # 描画しなおす必要があるとき
            if event.type in [KEYDOWN, TEXTEDITING, TEXTINPUT]:
                draw_text(input_text)


# クラス宣言部
class Text:
    """
    文字を入力するための関数
    """

    def __init__(self) -> None:
        self.text = ["|"]  # 入力されたテキストを格納していく変数
        self.editing: List[str] = []  # 全角の文字編集中(変換前)の文字を格納するための変数
        self.is_editing = False  # 編集中文字列の有無(全角入力時に使用)
        self.cursor_pos = 0  # 文字入力のカーソル(パイプ|)の位置

    def __str__(self) -> str:
        """self.textリストを文字列にして返す"""
        return "".join(self.text)

    def edit(self, text: str, editing_cursor_pos: int) -> str:
        """
        edit(編集中)であるときに呼ばれるメソッド
        全角かつ漢字変換前の確定していないときに呼ばれる
        """
        if text:  # テキストがあるなら
            self.is_editing = True
            for x in text:
                self.editing.append(x)  # 編集中の文字列をリストに格納していく
            self.editing.insert(editing_cursor_pos, "|")  # カーソル位置にカーソルを追加
            disp = "[" + "".join(self.editing) + "]"
        else:
            self.is_editing = False  # テキストが空の時はFalse
            disp = "|"
        self.editing = []  # 次のeditで使うために空にする
        # self.cursorを読み飛ばして結合する
        return (
            format(self)[0 : self.cursor_pos]
            + disp
            + format(self)[self.cursor_pos + 1 :]
        )

    def input(self, text: str) -> str:
        """半角文字が打たれたとき、もしくは全角で変換が確定したときに呼ばれるメソッド"""
        self.is_editing = False  # 編集中ではなくなったのでFalseにする
        for x in text:
            self.text.insert(self.cursor_pos, x)  # カーソル位置にテキストを追加
            # 現在のカーソル位置にテキストを追加したので、カーソル位置を後ろにずらす
            self.cursor_pos += 1
        return format(self)

    def delete_left_of_cursor(self) -> str:
        """カーソルの左の文字を削除するためのメソッド"""
        # カーソル位置が0であるとき
        if self.cursor_pos == 0:
            return format(self)
        self.text.pop(self.cursor_pos - 1)  # カーソル位置の一個前(左)を消す
        self.cursor_pos -= 1  # カーソル位置を前にずらす
        return format(self)

    def delete_right_of_cursor(self) -> str:
        """カーソルの右の文字を削除するためのメソッド"""
        # カーソル位置より後ろに文字がないとき
        if len(self.text[self.cursor_pos+1:]) == 0:
            return format(self)
        self.text.pop(self.cursor_pos + 1)  # カーソル位置の一個後(右)を消す
        return format(self)

    def enter(self) -> str:
        """入力文字が確定したときに呼ばれるメソッド"""
        # カーソルを読み飛ばす
        entered = (
            format(self)[0 : self.cursor_pos] + format(self)[self.cursor_pos + 1 :]
        )
        self.text = ["|"]  # 次回の入力で使うためにself.textを空にする
        self.cursor_pos = 0  # self.text[0] == "|"となる
        return entered

    def move_cursor_left(self) -> str:
        """inputされた文字のカーソル(パイプ|)の位置を左に動かすメソッド"""
        if self.cursor_pos > 0:
            # カーソル位置をカーソル位置の前の文字と交換する
            self.text[self.cursor_pos], self.text[self.cursor_pos - 1] = (
                self.text[self.cursor_pos - 1],
                self.text[self.cursor_pos],
            )
            self.cursor_pos -= 1  # カーソルが1つ前に行ったのでデクリメント
        return format(self)

    def move_cursor_right(self) -> str:
        """inputされた文字のカーソル(パイプ|)の位置を右に動かすメソッド"""
        if len(self.text) - 1 > self.cursor_pos:
            # カーソル位置をカーソル位置の後ろの文字と交換する
            self.text[self.cursor_pos], self.text[self.cursor_pos + 1] = (
                self.text[self.cursor_pos + 1],
                self.text[self.cursor_pos],
            )
            self.cursor_pos += 1  # カーソルが1つ後ろに行ったのでインクリメント
        return format(self)


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



def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((HEIGHT, WIDTH))
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
                    if event.type == pg.K_KP_ENTER:
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


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont("yumincho", 30)
    text = Text()  # テキスト処理のロジックTextクラスをインスタンス化
    pygame.key.start_text_input()  # input, editingイベントをキャッチするようにする
    draw_text(format(text))  # 起動時にカーソルを表示するようにする
    event_loop()