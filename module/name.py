import pygame
from pygame.locals import QUIT, KEYDOWN, TEXTINPUT, TEXTEDITING, K_RETURN, K_BACKSPACE, K_DELETE, K_LEFT, K_RIGHT
import sys
from typing import List
import pygame as pg

class Text:
    """
    PygameのINPUT、EDITINGイベントで使うクラス
    カーソル操作や文字列処理に使う
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
        if text:
            self.is_editing = True
            self.editing = list(text)
            self.editing.insert(editing_cursor_pos, "|")
            disp = "[" + "".join(self.editing) + "]"
        else:
            self.is_editing = False
            disp = "|"
        return format(self)[0:self.cursor_pos] + disp + format(self)[self.cursor_pos+1:]

    def input(self, text: str) -> str:
        self.is_editing = False
        for x in text:
            self.text.insert(self.cursor_pos, x)
            self.cursor_pos += 1
        return format(self)

    def delete_left_of_cursor(self) -> str:
        if self.cursor_pos > 0:
            self.text.pop(self.cursor_pos - 1)
            self.cursor_pos -= 1
        return format(self)

    def delete_right_of_cursor(self) -> str:
        if len(self.text) > self.cursor_pos + 1:
            self.text.pop(self.cursor_pos + 1)
        return format(self)

    def enter(self) -> str:
        entered = "".join(self.text).replace("|", "")
        self.text = ["|"]
        self.cursor_pos = 0
        return entered

    def move_cursor_left(self) -> str:
        if self.cursor_pos > 0:
            self.text[self.cursor_pos], self.text[self.cursor_pos - 1] = (
                self.text[self.cursor_pos - 1],
                self.text[self.cursor_pos],
            )
            self.cursor_pos -= 1
        return format(self)

    def move_cursor_right(self) -> str:
        if self.cursor_pos < len(self.text) - 1:
            self.text[self.cursor_pos], self.text[self.cursor_pos + 1] = (
                self.text[self.cursor_pos + 1],
                self.text[self.cursor_pos],
            )
            self.cursor_pos += 1
        return format(self)

def event_loop(screen, text, font):
    """名前入力時のイベントループ処理"""
    editing_text = ""  # 変換中のテキストを一時的に格納

    while True:
        bg_img = pg.image.load("./ex5/fig/2A8A8887-518x800.jpg")
        bg_rct = bg_img.get_rect()

        font1 = pygame.font.SysFont("hg正楷書体pro", 35)
        text1 = font1.render("名前を入力してください", True, (255,0,0))

        font2 = pygame.font.SysFont("hg正楷書体pro", 35)
        text2 = font2.render("名前を入力後ENTERキー", True, (0,0,255))
        font3 = pygame.font.SysFont("hg正楷書体pro", 35)
        text3 = font3.render("押すとゲームスタート！", True, (0,0,255))

        screen.blit(bg_img, bg_rct)
        screen.blit(text1, (40,100))
        screen.blit(text2, (30,500))
        screen.blit(text3, (30,535))
        pygame.draw.rect(screen, (255,255,255), (50,300,330,30))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:  # Enterキーで入力を確定
                    return str(text)  # 名前を返す
                elif event.key == pg.K_BACKSPACE:  # バックスペースで文字削除
                    text.delete_left_of_cursor()
                elif event.key == pg.K_DELETE:  # デリートキーで右の文字削除
                    text.delete_right_of_cursor()
                elif event.key == pg.K_LEFT:  # カーソルを左に移動
                    text.move_cursor_left()
                elif event.key == pg.K_RIGHT:  # カーソルを右に移動
                    text.move_cursor_right()
                elif event.key == pg.K_ESCAPE:
                    return str()

            elif event.type == pg.TEXTEDITING:
                # 編集中のテキストとカーソル位置を取得
                editing_text = event.text
                editing_cursor_pos = event.start
                displayed_text = text.edit(editing_text, editing_cursor_pos)

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



def draw_text(screen, font, text, position):
    """テキストを指定の位置に描画する関数"""
    text_surface = font.render(text, True, (0, 0, 0))  # テキストを黒色で描画
    screen.blit(text_surface, position)
