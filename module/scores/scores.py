import datetime
import os
from random import uniform
import uuid

import pygame as pg

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
        self.rect.center = 75, 25

    def set_player_name(self, player_name:str):
        """
        プレイヤー名を設定する

        :param str player_name: プレイヤー名
        """
        self.player_name = player_name

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
        ただし、guestの0scoreは保存しない
        """
        if self.player_name == "guest" and self.value <= 0:
            return
        self.session.insert(self.player_uuid, self.player_name, self.value)
