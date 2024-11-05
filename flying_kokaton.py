import numpy as np
import datetime
import os
import sys
import uuid
import pygame as pg
import pygame
from pygame.locals import *
from module.name import Text, event_loop
from random import randint as ran
from random import uniform
from typing import List


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


def jadge_combo(a, b):
    if a == b or a + 10 == b or a == b + 10:
        return True
    else:
        return False

def jadge_double(lis:list[list], i:int, j:int, combo_type:int, combo_len:int = 3):
    T = combo_len
    if combo_type == 1:
        for n in range(3):
            for m in range(3):
                if lis[i+n][j+m] >= 10:
                    T -= 1

    elif combo_type == 11:
        for n in range(combo_len):
            if lis[i][j+n] >= 10:
                T -= 1

    elif combo_type == 12:
        for n in range(combo_len):
            if lis[i+n][j] >= 10:
                T -= 1

    elif combo_type == 21:
        if lis[i][j] >= 10 and lis[i][j+1] >= 10 and lis[i][j+2] >= 10 and lis[i-1][j+1] >= 10 and lis[i+1][j+1] >= 10:
            T -= combo_len

    elif combo_type == 22:
        if lis[i][j] >= 10 and lis[i][j+2] >= 10 and lis[i+1][j] >= 10 and lis[i+1][j+1] >= 10 and lis[i+1][j+2] >= 10 and lis[i+2][j] >= 10 and lis[i+2][j+2] >= 10:
            T -= combo_len
    
    elif combo_type == 23:
        if lis[i][j] >= 10 and lis[i][j+2] >= 10 and lis[i+2][j] >= 10 and lis[i+2][j+2] >= 10 and lis[i][j+1] >= 10 and lis[i+2][j+1] >= 10 and lis[i+2][j+1] >= 10:
            T -= combo_len

    elif combo_type == 31:
        for n in range(3):
            if lis[i+n][j] >= 10:
                    T -= 1
                    if n == 2:
                        for m in range(1, 3):
                            if lis[i+n][j+m] >= 10:
                                T -= 1

    elif combo_type == 32:
        for n in range(3):
            if lis[i+n][j] >= 10:
                    T -= 1
                    if n == 2:
                        for m in range(-2, 0):
                            if lis[i+n][j+m] >= 10:
                                T -= 1

    elif combo_type == 33:
        for n in range(3):
            if lis[i+n][j] >= 10:
                    T -= 1
                    if n == 0:
                        for m in range(1, 3):
                            if lis[i+n][j+m] >= 10:
                                T -= 1

    elif combo_type == 34:
        for n in range(3):
            if lis[i][j+n] >= 10:
                    T -= 1
                    if n == 2:
                        for m in range(1, 3):
                            if lis[i+m][j+n] >= 10:
                                T -= 1
    elif combo_type == 41:
        for n in range(3):
            if lis[i][j+n] >= 10:
                    T -= 1
                    if n == 1:
                        for m in range(1, 3):
                            if lis[i+m][j+n] >= 10:
                                T -= 1
    elif combo_type == 42:
        for n in range(3):
            if lis[i+n][j] >= 10:
                    T -= 1
                    if n == 2:
                        for m in range(-1, 2, 2):
                            if lis[i+n][j+m] >= 10:
                                T -= 1

    elif combo_type == 43:
        for n in range(3):
            if lis[i+n][j] >= 10:
                    T -= 1
                    if n == 1:
                        for m in range(1, 3):
                            if lis[i+n][j+m] >= 10:
                                T -= 1
    
    elif combo_type == 44:
        for n in range(3):
            if lis[i][j+n] >= 10:
                    T -= 1
                    if n == 2:
                        for m in range(-1, 2, 2):
                            if lis[i+m][j+n] >= 10:
                                T -= 1

    if T > 0:
        return True
    else:
        return False



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
        self.col =__class__.color[ball_list[self.i][self.j]]
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

class ScoreLogDAO:
    """
    それぞれのスコアデータの入出力を管理するクラス
    TODO: できればデータベース化
    """
    def __init__(self,log_file_name:str = "score_log.csv", file_encoding:str = "utf-8") -> None:
        """
        スコアログを保存する先がなければ作成する
        また、任意のファイル名へと変更できる
        保存先のパスは"./logs"内になる

        :param str log_file_name: ファイル名
        :param str file_encoding: ファイルのエンコード方式
        """
        self.file_encoding = file_encoding
        self.log_file_path = "./logs"

        if not os.path.exists(self.log_file_path):
            # フォルダがなければ作成する
            os.mkdir(self.log_file_path)
        
        self.log_file = self.log_file_path + "/" + log_file_name
        if not os.path.exists(self.log_file):
            # ログファイルがなければ初期化する
            with open(self.log_file, "w", encoding=self.file_encoding) as f:
                f.write("uuid,player_name,score,created_time\n")

        # タイムスタンプ準備
        t_delta = datetime.timedelta(hours=9)
        jts = datetime.timezone(t_delta, 'JST')
        self.now = datetime.datetime.now(jts)
    
    def insert(self, uuid:str, player_name:str, score:int) -> bool:
        """
        プレイログを挿入する

        :param str uuid: UUID
        :param str player_name: プレイヤー名
        :param str score:
        :return: 成功したらTrueを返します
        :rtype: bool
        """
        with open(self.log_file, "a", encoding=self.file_encoding) as f:
            f.write(f"{uuid},{player_name},{score},{self.now.strftime('%Y/%m/%d %H:%M:%S')}\n")

        return True
    
    def get(self)->list[tuple[str,str,int,str]]:
        """
        保存されているプレイログデータを取得します

        :return: ログデータのtupleを返します
        :rtype: tuple[tuple[str,str,int,str]]
        """
        result = []
        with open(self.log_file, "r", encoding=self.file_encoding) as f:
            f.readline()
            result += [self.dismantling(row) for row in f]
        
        return result

    def dismantling(self,row:str)->tuple[str,str,str,str]:
        """
        プレイログデータの一行をそれぞれの要素に分解し、tupleで返します

        :return: uuid, player_name, score, created_time
        :rtype: tuple[str,str,str,str]
        """
        datas = row.rstrip("\n").rsplit(",")
        datas[2] = int(datas[2])

        return tuple(datas)

class Score:
    """
    スコア管理システム
    """
    def __init__(self, session:ScoreLogDAO, base_score:int = 1000, player_name:str = "guest"):
        """
        スコアをユーザと紐づけます
        担当 : c0a23019
        
        :param str player_name: プレイヤー名
        """
        self.session = session

        # スコア情報系
        self.value = 0
        self.player_name = player_name
        self.player_uuid = str(uuid.uuid1())
        self.base_score = base_score
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

    def calculate_combo_score(self, combo:int, bonus:float = 1.0):
        """
        コンボスコア計算
        工夫点: ランダム性を持たせることで、ゲーム性を向上させる

        :param int combo: 現在のコンボ数
        :param float bonus: ボーナス倍率
        """
        combo_score = self.base_score * (combo ** 1.25) * (uniform(0.8, 1.2)) * bonus
        self.add(round(combo_score))

    def save(self) -> None:
        """
        スコアをファイルに保存する
        """
        self.session.insert(self.player_uuid, self.player_name, self.value)


# クラス宣言部
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
            self.box_combo()
            self.h_combo()
            self.i_combo()
            self.t_combo()
            self.t_combo_rev()
            self.t_left_combo()
            self.t_right_combo()
            self.l_combo_dl()
            self.l_combo_dr()
            self.l_combo_ul()
            self.l_combo_ur()
            self.cross_combo()
            self.row_combo()
            self.column_combo()
            if check == self.combo_count:
                break
            check = self.combo_count
        print("rep")
        print(self.lis[0], "\n", self.lis[1], "\n", self.lis[2], "\n", self.lis[3], "\n", self.lis[4], "\n", self.lis[5])
        self.elise(self.lis)
    
    def box_combo(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 1, 9) and jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+1][j]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+2]):
                    stack += 2
                    print("box", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 1, self.lis[i][j])
                    break

    def h_combo(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 22) and jadge_combo(self.lis[i][j], self.lis[i][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+1][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+2]):
                    stack += 2
                    print("H", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 22, self.lis[i][j])
                    break
        
    def i_combo(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 23) and jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+2]):
                    stack += 2
                    print("I", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 23, self.lis[i][j])
                    break

    def t_combo(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 41, 5) and jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+1]):
                    stack += 2
                    print("T", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 41, self.lis[i][j])
                    break
    
    def t_combo_rev(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 42, 5) and jadge_combo(self.lis[i][j], self.lis[i+2][j-1]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+1][j]):
                    stack += 2
                    print("T-rev", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 42, self.lis[i][j])
                    break

    def t_left_combo(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 43, 5) and jadge_combo(self.lis[i][j], self.lis[i+1][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+2]):
                    stack += 2
                    print("T-left", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 43, self.lis[i][j])
                    break
    
    def t_right_combo(self):
        for i in range(1, len(self.lis) - 1):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 44, 5) and jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]) and jadge_combo(self.lis[i][j], self.lis[i-1][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+2]):
                    stack += 2
                    print("T-right", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 44, self.lis[i][j])
                    break
    
    def l_combo_dl(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 31, 5) and jadge_combo(self.lis[i][j], self.lis[i+1][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+2]):
                    stack += 2
                    print("L-dl", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 31, self.lis[i][j])
                    break

    def l_combo_dr(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(2, len(self.lis)):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 32, 5) and jadge_combo(self.lis[i][j], self.lis[i+1][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j-1]) and jadge_combo(self.lis[i][j], self.lis[i+2][j-2]):
                    stack += 2
                    print("L-dr", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 32, self.lis[i][j])
                    break
    def l_combo_ul(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 33, 5) and jadge_combo(self.lis[i][j], self.lis[i+1][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]):
                    stack += 2
                    print("L-ul", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 31, self.lis[i][j])
                    break
    def l_combo_ur(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 34, 5) and jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+2]):
                    stack += 2
                    print("L-ur", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 34, self.lis[i][j])
                    break
    
    def cross_combo(self):
        for i in range(1, len(self.lis) - 1):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    stack -= 1
                    continue
                if jadge_double(self.lis, i, j, 21) and jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]) and jadge_combo(self.lis[i][j], self.lis[i-1][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+1]):
                    stack += 2
                    print("cross", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 21, self.lis[i][j])
                    break

    def row_combo(self):
       for i in range(len(self.lis)):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    stack -= 1
                    continue
                combo_len = 3
                if jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]):
                    if j <= 2 and jadge_combo(self.lis[i][j], self.lis[i][j+3]):
                        combo_len += 1
                        if j <= 1 and jadge_combo(self.lis[i][j], self.lis[i][j+4]):
                            combo_len += 1
                            if j <= 0 and jadge_combo(self.lis[i][j], self.lis[i][j+5]):
                                combo_len += 1
                    if jadge_double(self.lis, i, j, 11, combo_len):
                        self.combo_count += 1
                        stack += combo_len-1
                        print("row", [i, j], combo_len)
                        self.combo_add()
                        self.change(self.lis, i, j, 11, self.lis[i][j], combo_len)
                        break
                    
    def column_combo(self):
        for j in range(len(self.lis)):
            stack = 0
            for i in range(len(self.lis) - 2):
                if stack > 0:
                    stack -= 1
                    continue
                combo_len = 3
                if jadge_combo(self.lis[i][j], self.lis[i+1][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]):
                    if i <= 2 and jadge_combo(self.lis[i][j], self.lis[i+3][j]):
                        combo_len += 1
                        if i <= 1 and self.lis[i][j] == self.lis[i+4][j]:
                            combo_len += 1
                            if i <= 0 and jadge_combo(self.lis[i][j], self.lis[i+5][j]):
                                combo_len += 1
                    if jadge_double(self.lis, i, j, 12, combo_len):
                        self.combo_count += 1
                        stack += combo_len-1
                        print("column", [i, j], combo_len)
                        self.combo_add()
                        self.change(self.lis, i, j, 12, self.lis[i][j], combo_len)
                        
                        break

    def get_count(self):
        return self.combo_count
    
    def get_lis(self):
        return self.lis
    
    def change(self, lis:list[list], i:int, j:int, combo_type:int, ele:int = 0, combo_len:int = 1):
        #引数:lst　ボールの種類を保持するリスト
        #コンボ判定されたball_lstを0にする
        if ele >= 10:
            ele = ele - 10
        
        if combo_type == 1:
            for n in range(3):
                for m in range(3):
                    lis[i+n][j+m] = 10+ele

        if combo_type == 11:
            for n in range(combo_len):
                lis[i][j+n] = 10+ele

        elif combo_type == 12:
            for n in range(combo_len):
                lis[i+n][j] = 10+ele

        elif combo_type == 21:
            for n in range(3):
                lis[i][j+n] = 10+ele
            lis[i-1][j+1] = 10+ele
            lis[i+1][j+1] = 10+ele

        elif combo_type == 22:
            for n in range(3):
                lis[i+1][j+n] = 10+ele
            lis[i][j] = 10+ele
            lis[i][j+2] = 10+ele
            lis[i+2][j] = 10+ele
            lis[i+2][j+2] = 10+ele

        elif combo_type == 23:
                    for n in range(3):
                        lis[i+n][j+1] = 10+ele
                    lis[i][j] = 10+ele
                    lis[i][j+2] = 10+ele
                    lis[i+2][j] = 10+ele
                    lis[i+2][j+2] = 10+ele

        elif combo_type == 31:
            for n in range(3):
                lis[i+n][j] = 10+ele
                if n == 2:
                    for m in range(1, 3):
                        lis[i+n][j+m] = 10+ele
        
        elif combo_type == 32:
            for n in range(3):
                lis[i+n][j] = 10+ele
                if n == 2:
                    for m in range(-2, 0):
                        lis[i+n][j+m] = 10+ele
        
        elif combo_type == 33:
            for n in range(3):
                lis[i+n][j] = 10+ele
                lis[i][j+n] = 10+ele

        elif combo_type == 34:
            for n in range(3):
                lis[i][j+n] = 10+ele
                if n == 2:
                    for m in range(1, 3):
                        lis[i+m][j+n] = 10+ele
        
        elif combo_type == 41:
            for n in range(3):
                lis[i][j+n] = 10+ele
                if n == 1:
                    for m in range(1, 3):
                        lis[i+n][j] = 10+ele

        elif combo_type == 42:
            for n in range(3):
                lis[i+n][j] = 10+ele
                if n == 2:
                    for m in range(-1, 2, 2):
                        lis[i+n][j+m] = 10+ele

        elif combo_type == 43:
            for n in range(3):
                lis[i+n][j] = 10+ele
                if n == 1:
                    for m in range(1, 3):
                        lis[i+n][j+m] = 10+ele

        elif combo_type == 44:
            for n in range(3):
                lis[i][j+n] = 10+ele
                if n == 2:
                    for m in range(-1, 2, 2):
                        lis[i+m][j+n] = 10+ele

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


# main関数
def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    # 名前入力用のTextインスタンスを作成

    # 背景画像の読み込み
    bg_img = pg.image.load("./ex5/fig/pg_bg.jpg")
    bg_imgs = [bg_img, pg.transform.flip(bg_img, True, False)]
    
    # キャラクター画像の読み込みと設定
    kk_img = pg.image.load("./ex5/fig/3.png")
    kk_img = pg.transform.flip(kk_img, True, False)

    # キャラクターの初期座標設定
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300,200
    # ここまで
    score_log_DAO = ScoreLogDAO()
    drop_list_x = 0
    drop_list_y = 0
    change_list_X = 0
    change_list_Y = 0
    text = Text()
    tmr = 0 # 時間保存

    ball = pg.sprite.Group()

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
                text = Text()  # Text クラスをインスタンス化
                status = "home:1"
            case "home:1":
                player_name = event_loop(screen, text, font)  # 名前入力後、イベントループから取得
                print(f"Player Name: {player_name}")
                if not player_name:
                    player_name = None
                elif player_name == "log":
                    status = "log:1"
                else:
                    status = "game:0"
            
            case "game:0":
                """
                ゲームの初期化
                """
                lis= PuzzleList()
                t = lis.get_lis()
                for i in range(len(t)):
                    for j in range(len(t[i])):
                        ball.add(KoukatonDrop(lis.get_lis(),(i,j)))
                status="game:1"

            case "game:1":     
                # 練習7
                for i in range(4):
                    screen.blit(bg_imgs[i%2], [-(tmr % 3200)+1600*i, 0])
                  
                key_lst = pg.key.get_pressed() # 練習8-3 全キーの押下状態取得
                
                for event in event_list:
                    if event.type == pg.QUIT: return
                    elif event.type == pg.KEYDOWN:
                        x, y = PuzzleList.move_lect([x, y], event.key)
                        if event.key == pg.K_RETURN: # ENTERが押されたとき
                                status = "game:2"
                for i in range(len(t)):
                    for j in range(len(t[i])):
                        ball.add(KoukatonDrop(lis.get_lis(),(i,j)))
                    ball.update(screen)                               
                    ball.draw(screen)

                    lis= PuzzleList()       
            case "game:2":
                for event in event_list:
                    if event.type == pg.QUIT: return
                    elif event.type == pg.KEYDOWN:
                        change_list_X,change_list_Y = PuzzleList.move_lect([change_list_X, change_list_Y], event.key)
                        if (change_list_X,change_list_Y) != (drop_list_x,drop_list_y): # X,Yとx,yの値が一致していないとき
                            PuzzleList.lis[change_list_X][change_list_Y],PuzzleList.lis[drop_list_x][drop_list_y] = PuzzleList.lis[drop_list_x][drop_list_y],PuzzleList.lis[change_list_X][change_list_Y] # PuzzleListクラスのlisの中身を入れ替える

                for i in range(len(t)):
                    for j in range(len(t[i])):
                        ball.add(KoukatonDrop(lis.get_lis(),(i,j)))
                    ball.update(screen)                               
                    ball.draw(screen)

                    lis= PuzzleList()      
              
                status = "game:1"
            
            case "log:0":
                lis = score_log_DAO.get()
                screen.fill((255, 255, 255))
                font = pygame.font.Font(None, 20)
                sor = sorted(lis, reverse=True, key=lambda x: x[3])
                # スコア表示
                for i, row in enumerate(sor):
                    screen.blit(font.render(str(row[1:]), True, (0,0,255)), (20, 50 + i*50))
                status = "log:1"
            case "log:1":
                for event in event_list:
                    if event.key == pg.K_ESCAPE:
                        status = "home:0"
                



        # 共通処理部
        pg.display.update()
        tmr += 1        
        clock.tick(200)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
