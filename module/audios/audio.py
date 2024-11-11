import pygame

class Audio:
    """
    音声に関するクラス
    """
    def __init__(self):
        pygame.mixer.init(frequency=44100)
        self.play_flag = False
        try :
            # 効果音
            self.cursor_control = pygame.mixer.Sound('./ex5/audio/cursor_control.mp3')
            self.open_window = pygame.mixer.Sound('./ex5/audio/open_window.mp3')
            self.open_window.set_volume(0.5)
            self.key_push = pygame.mixer.Sound('./ex5/audio/key_push.mp3')

            self.combos = [pygame.mixer.Sound(f'./ex5/audio/combo/{i}.mp3') for i in range(1, 16)]

            # BGM
            self.bgm = pygame.mixer.Sound('./ex5/audio/パズドラ風.mp3')
            self.bgm.set_volume(0.03)
            self.play_flag = True
        except FileNotFoundError:
            print("Error: No such file or directory")
        except AttributeError:
            print("Error: No such file or directory")
        if not self.play_flag:
            print("No sound Mode")

    def sound_deco(func):
        """
        デコレータ
        音声が一つでもなかった場合再生しない
        """
        def wrapper(self, *args, **kwargs):
            if self.play_flag:
                func(self, *args, **kwargs)
        return wrapper

    @sound_deco
    def open_window_play(self):
        """
        ウィンドウ開閉音
        (メニューを開く4: https://soundeffect-lab.info/sound/button/)
        """
        self.open_window.play()

    @sound_deco
    def cursor_control_play(self):
        """
        カーソル移動音
        (決定ボタンを押す48: https://soundeffect-lab.info/sound/button/)
        """
        self.cursor_control.play()
    
    @sound_deco
    def key_push_play(self):
        """
        キー入力音
        (決定ボタンを押す50: https://soundeffect-lab.info/sound/button/)
        """
        self.key_push.play()

    @sound_deco
    def combo_play(self, combo:int):
        """
        コンボ音
        (コンボ数によって音が変わる)
        """
        if combo >= 15:
            combo = 15
        self.combos[combo-1].play()

    # BGM
    @sound_deco
    def bgm_play(self):
        """
        パズドラっぽいBGM
        C0A23019が「departure/パズドラ」をアレンジした物
        voice: Synthesizer V 重音テトAI
        """
        self.bgm.play(-1)