import pygame
from plane_sprites import *


pygame.font.init()
pygame.mixer.init()


class PlaneGame(object):
    '''
    飞机大战主程序
    '''

    def __init__(self):
        print('游戏初始化')

        # 加载游戏音效

        pygame.mixer.music.load('./music/background.mp3')
        pygame.mixer.music.set_volume(0.2)
        self.bullet_sound = pygame.mixer.Sound("./music/bullet.wav")
        self.bullet_sound.set_volume(0.2)
        self.enemy1_die = pygame.mixer.Sound('./music/enemy1_down.wav')
        self.enemy1_die.set_volume(0.2)
        self.enemy2_die = pygame.mixer.Sound('./music/enemy2_down.wav')
        self.enemy2_die.set_volume(0.2)
        self.me_down = pygame.mixer.Sound('./music/me_down.wav')
        self.me_down.set_volume(0.2)
        self.pause_effect = pygame.mixer.Sound('./music/pause.ogg')
        self.rec_effect = pygame.mixer.Sound('./music/continue.ogg')
        self.rec_effect.set_volume(0.2)
        # 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 标题
        pygame.display.set_caption("飞机大战")
        # 创建游戏时钟
        self.clock = pygame.time.Clock()
        # 调用私有方法创建精灵
        self.__create_sprites()
        # 设置定时器常量 - 创建敌方飞机 1秒
        pygame.time.set_timer(CREATE_ENEMY, 1000)
        # 设置定时器常量 - 我方飞机发射子弹 1秒
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)
        # 设置游戏得分
        self.score = 0
        self.paused = False

    def __create_sprites(self):
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)
        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()
        # 创建我方飞机和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
        # 创建静态精灵和精灵组
        self.static_pause = Static_item('./images/pause.png', 400, 5)
        self.static_group = pygame.sprite.Group(self.static_pause)

    def start_game(self):

        print('游戏开始')
        while True:
            # 播放BGM
            # 检查音乐流播放，有返回True，没有返回False
            # 如果没有音乐流则选择播放
            # print(pygame.mixer.music.get_busy()) reutrn 0 or 1
            # ↓↓↓↓↓↓↓↓↓↓↓↓
            if pygame.mixer.music.get_busy() == 0:  # is false

                pygame.mixer.music.play()

            ticks = pygame.time.get_ticks()
            # 1.设置刷新帧率
            self.clock.tick(FRAME_PER_SECOND)

            # 2.事件监听
            self.__event_handler()

            # 3.碰撞检测
            self.__check_collide(ticks)

            # 4.更新/绘制精灵
            if self.paused is False:
                self.__update_sprites(ticks)

            # 5.更新显示
            pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            # 键盘事件
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_RIGHT]:
                self.hero.speed = 10
            elif keys_pressed[pygame.K_LEFT]:
                self.hero.speed = -10
            elif keys_pressed[pygame.K_DOWN]:
                self.hero.vertical_speed = 10
            elif keys_pressed[pygame.K_UP]:
                self.hero.vertical_speed = -10
            else:
                self.hero.speed = 0
                self.hero.vertical_speed = 0

            # 鼠标事件
            click = pygame.mouse.get_pressed()  # 鼠标点击
            # mouse = pygame.mouse.get_pos()  # 鼠标位置
            if click[0] == 1:
                mouse = pygame.mouse.get_pos()
                if 400 < mouse[0] < 440 and 5 < mouse[1] < 33 and \
                        self.paused is False:
                    self.pause()
                if 220 < mouse[0] < 270 and 170 < mouse[1] < 240 and \
                        self.paused is True:
                    self.continue_play()

            # 退出事件
            if event.type == pygame.QUIT:
                PlaneGame.__gameover()
            if self.paused is True:
                break
            elif event.type == CREATE_ENEMY:
                print(event.type)
                print("敌方飞机出场")
                # 1.创建敌机精灵
                enemy_type = random.randint(1, 2)
                if enemy_type == 1:
                    enemy = Enemy1()
                else:
                    enemy = Enemy2()
                # 2.将敌机精灵添加进精灵组
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                print(self.hero)
                print(self.hero_group)
                if self.hero_group:
                    if self.hero.fire() != -1 and self.paused is False:
                        self.bullet_sound.play()
            # elif event.type == pygame.KEYDOWN and \+
            #       event.key == pygame.K_RIGHT:
            #   print('向右移 动')

    def __check_collide(self, ticks):
        # 子弹击中敌机 返回敌机列表
        for b in self.hero.bullet_group:
            enemys = pygame.sprite.spritecollide(b, self.enemy_group, False)
            if len(enemys) > 0:
                b.kill()
                if enemys[0].explode is False:  # <重点,难点>判断是否第一次击中,后续击中不加分
                    if enemys[0].enemy_type == 1:
                        self.enemy1_die.play()
                    else:
                        self.enemy2_die.play()
                    self.score += enemys[0].score
                enemys[0].explode = True

        #  敌机击中我方飞机 返回击中我方飞机敌方飞机列表
        enemys = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemys) > 0:
            print('↓↓↓↓↓')
            print(enemys[0])
            print('↓↓↓↓↓')
            if self.hero.explode is False:
                self.me_down.play()
            self.hero.explode = True

    def __update_sprites(self, ticks):
        self.back_group.update()
        self.back_group.draw(self.screen)
        self.static_group.update()
        self.static_group.draw(self.screen)
        self.enemy_group.update(ticks)
        self.enemy_group.draw(self.screen)

        self.hero_group.update(ticks)
        self.hero_group.draw(self.screen)
        self.hero.bullet_group.update()

        self.hero.bullet_group.draw(self.screen)

        score_font = pygame.font.Font('./fonts/GuRu-hand1-2008.ttf', 25)

        score_text = score_font.render(
            "Score : %s" % str(self.score), True, (0, 0, 0))
        self.screen.blit(score_text, (10, 5))
        # 绘制文字在(10,10)位置

    def pause(self):
        self.pause_effect.play()
        self.paused = True
        score_font = pygame.font.Font('./fonts/GuRu-hand1-2008.ttf', 50)

        score_text = score_font.render(
            "PAUSE", True, (0, 0, 0))  # true 开启平滑字体

        self.screen.blit(score_text, (165, 100))
        rec_game = pygame.image.load('./images/continue.png')
        self.screen.blit(rec_game, (220, 170))
        # 绘制继续按钮

    def continue_play(self):
        self.rec_effect.play()
        self.paused = False

    @staticmethod
    def __gameover():
        print("游戏结束")
        pygame.quit()
        exit()


if __name__ == '__main__':
    # 创建游戏对象

    game = PlaneGame()
    game.start_game()
