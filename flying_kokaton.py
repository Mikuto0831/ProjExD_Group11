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
    score_log_DAO = ScoreLogDAO()
    drop_list_x = 0
    drop_list_y = 0
    change_list_X = 0
    change_list_Y = 0
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
                if event.type == pg.KEYDOWN:
                    status = "game:1"     
        
            case "game:1":
                status = "game:2"
                for event in pg.event.get():
                    if event.type == pg.QUIT: return
                    elif event.type == pg.KEYDOWN:
                        x, y = PuzzleList.move_lect([x, y], event.key)
                        if event.key == pg.K_RETURN: # ENTERが押されたとき
                                status = "game:2"
            case "game:2":
                for event in pg.event.get():
                    if event.type == pg.QUIT: return
                    elif event.type == pg.KEYDOWN:
                        change_list_X,change_list_Y = PuzzleList.move_lect([change_list_X, change_list_Y], event.key)
                        if (change_list_X,change_list_Y) != (drop_list_x,drop_list_y): # X,Yとx,yの値が一致していないとき
                            PuzzleList.lis[change_list_X][change_list_Y],PuzzleList.lis[drop_list_x][drop_list_y] = PuzzleList.lis[drop_list_x][drop_list_y],PuzzleList.lis[change_list_X][change_list_Y] # PuzzleListクラスのlisの中身を入れ替える
               
                
                


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