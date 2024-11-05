import datetime
import os
from random import randint as ran
import sys
import uuid
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 定数宣言部
HEIGHT = 650
WIDTH = 450



# クラス宣言部
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

        return tuple(datas)

class Score:
    """
    スコア管理システム
    """
    def __init__(self, session:ScoreLogDAO, player_name:str = "guest"):
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

    def save(self) -> None:
        # TODO: クラス削除時にスコアをファイルに保存する
        self.session.insert(self.player_uuid, self.player_name, self.value)

      
class PuzzleList:
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
    
    combo_all = 0

    def __init__(self, lis:list[list]):
        self.combo_count = 0
        self.lis = lis
        check = 0
        while True:
            self.h_combo()
            self.l_combo()
            self.cross_combo()
            self.row_combo()
            self.column_combo()
            if check == self.combo_count:
                break
            check = self.combo_count
        self.elise(self.lis)
    
    def h_combo(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 4) and jadge_combo(self.lis[i][j], self.lis[i][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+1][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+2]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+2]):
                    stack += 2
                    print("H", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 4, self.lis[i][j])
                    break
    
    def l_combo(self):
        for i in range(len(self.lis) - 2):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    continue
                if jadge_double(self.lis, i, j, 5, 5) and jadge_combo(self.lis[i][j], self.lis[i+1][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+2][j+2]):
                    stack += 2
                    print("L", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 5, self.lis[i][j])
                    break
    
    def cross_combo(self):
        for i in range(1, len(self.lis) - 1):
            stack = 0
            for j in range(len(self.lis) - 2):
                if stack > 0:
                    stack -= 1
                    continue
                if jadge_double(self.lis, i, j, 3) and jadge_combo(self.lis[i][j], self.lis[i][j+1]) and jadge_combo(self.lis[i][j], self.lis[i][j+2]) and jadge_combo(self.lis[i][j], self.lis[i-1][j+1]) and jadge_combo(self.lis[i][j], self.lis[i+1][j+1]):
                    stack += 2
                    print("cross", [i, j])
                    self.combo_add()
                    self.change(self.lis, i, j, 3, self.lis[i][j])
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
                    if jadge_double(self.lis, i, j, 1, combo_len):
                        self.combo_count += 1
                        stack += combo_len-1
                        print("row", [i, j], combo_len)
                        self.combo_add()
                        self.change(self.lis, i, j, 1, self.lis[i][j], combo_len)
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
                    if jadge_double(self.lis, i, j, 2, combo_len):
                        self.combo_count += 1
                        stack += combo_len-1
                        print("column", [i, j], combo_len)
                        self.combo_add()
                        self.change(self.lis, i, j, 2, self.lis[i][j], combo_len)
                        
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
            for n in range(combo_len):
                lis[i][j+n] = 10+ele
        elif combo_type == 2:
            for n in range(combo_len):
                lis[i+n][j] = 10+ele
        elif combo_type == 3:
            for n in range(3):
                lis[i][j+n] = 10+ele
            lis[i-1][j+1] = 10+ele
            lis[i+1][j+1] = 10+ele
        elif combo_type == 4:
            for n in range(3):
                lis[i+1][j+n] = 10+ele
            lis[i][j] = 10+ele
            lis[i][j+2] = 10+ele
            lis[i+2][j] = 10+ele
            lis[i+2][j+2] = 10+ele
        elif combo_type == 5:
            for n in range(3):
                lis[i+n][j] = 10+ele
                if n == 2:
                    for m in range(3):
                        lis[i+n][j+m] = 10+ele

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


# 関数宣言部
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
        for n in range(combo_len):
            if lis[i][j+n] >= 10:
                T -= 1
    elif combo_type == 2:
        for n in range(combo_len):
            if lis[i+n][j] >= 10:
                T -= 1
    elif combo_type == 3:
        if lis[i][j] >= 10 and lis[i][j+1] >= 10 and lis[i][j+2] >= 10 and lis[i-1][j+1] >= 10 and lis[i+1][j+1] >= 10:
            T -= combo_len
    elif combo_type == 4:
        if lis[i][j] >= 10 and lis[i][j+2] >= 10 and lis[i+1][j] >= 10 and lis[i+1][j+1] >= 10 and lis[i+1][j+2] >= 10 and lis[i+2][j] >= 10 and lis[i+2][j+2]:
            T -= combo_len
    elif combo_type == 5:
        for n in range(3):
            if lis[i+n][j] >= 10:
                    T -= 1
                    if n == 2:
                        for m in range(1, 3):
                            if lis[i+n][j+m] >= 10:
                                T -= 1
    if T > 0:
        return True
    else:
        return False
    
# 実行確認用
lis = [[1, 1, 1, 2, 4, 2], 
       [2, 2, 2, 3, 2, 4], 
       [5, 2, 2, 2, 2, 5], 
       [3, 4, 2, 5, 2, 5], 
       [3, 1, 2, 4, 4, 5], 
       [3, 3, 3, 2, 4, 1]]
# lis_m = PuzzleList()
# lis = lis_m.get_lis()
print(lis[0], "\n", lis[1], "\n", lis[2], "\n", lis[3], "\n", lis[4], "\n", lis[5], "\n")
while True:
    check = Combo(lis)
    co = check.get_count()
    if co <= 0:
        break
    lis = check.get_lis()
    print(lis[0], "\n", lis[1], "\n", lis[2], "\n", lis[3], "\n", lis[4], "\n", lis[5])
    print()
    lis = drop_down(lis)
    print()
    print(lis[0], "\n", lis[1], "\n", lis[2], "\n", lis[3], "\n", lis[4], "\n", lis[5])
    print("combo",Combo.get_combo(), "co", co)
Combo.reset()
