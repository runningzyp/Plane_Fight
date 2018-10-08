import random
import pygame

# 屏幕大小
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 屏幕帧率
FRAME_PER_SECOND = 60
# 创建敌方飞机定时器常量
CREATE_ENEMY = pygame.USEREVENT
# 创建英雄发射子弹定时器常量
HERO_FIRE_EVENT = pygame.USEREVENT+1


class GameSprite(pygame.sprite.Sprite):
    '''
    飞机精灵总类
    '''

    def __init__(self, image_name, speed=1):
        # 调用父类初始化方法
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.last_time = 0
        #  设置是否撞机
        self.explode = False

    def update(self):
        # 在屏幕y轴移动
        self.rect.y += self.speed


class Background(GameSprite):
    '''
    游戏背景精灵类
    '''

    def __init__(self, is_alt=False):
        # 调用父类创建
        super().__init__("./images/background.png")
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -SCREEN_RECT.height


class Enemy(GameSprite):
    '''
    敌方飞机
    '''

    def __init__(self):
        # 1.调用父类方法,创建敌方飞机,同时指定飞机图片
        # 默认飞机类型 default tyoe
        super().__init__('./images/enemy1.png')

        # 2.设置飞机速度 1~3
        self.speed = random.randint(1, 3)

        # 3.指定飞机位置
        self.rect.bottom = 0  # 飞机底部位置
        max_x = SCREEN_RECT.width - self.rect.width
        # self.rect.x = random.randint(0, max_x)
        self.rect.x = random.randrange(0, max_x, self.rect.width)

    def update(self, current_time, rate=100):
        # 1.调用父类方法
        super().update()

        # 2.判断是否飞出屏幕,从精灵组中删除
        if self.rect.y > SCREEN_RECT.height:
            # print("飞机飞出屏幕,删除")
            # kill方法将精灵从精灵组中删除
            self.kill()
        self.last_time = current_time

    def __del__(self):
        # print("敌机挂了")
        pass


class Enemy1(Enemy):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./images/enemy1.png")
        self.enemy_type = 1
        self.score = 300  # 飞机分值
        self.explode_image = []
        self.explode_image.append(
            pygame.image.load('./images/enemy1_explode1.png'))
        self.explode_image.append(
            pygame.image.load('./images/enemy1_explode2.png'))
        self.explode_image.append(
            pygame.image.load('./images/enemy1_explode3.png'))
        self.explode_image.append(
            pygame.image.load('./images/enemy1_explode4.png'))
        self.explode_image.append(
            pygame.image.load('./images/enemy1_explode5.png'))

    def update(self, current_time, rate=100):

        if self.explode is True:
            if current_time > self.last_time + rate:
                self.image = self.explode_image[0]
            if current_time > self.last_time + 2*rate:
                self.image = self.explode_image[1]
            if current_time > self.last_time + 3*rate:
                self.image = self.explode_image[2]
            if current_time > self.last_time + 4*rate:
                self.image = self.explode_image[3]
            if current_time > self.last_time + 5*rate:
                self.image = self.explode_image[4]
            if current_time > self.last_time + 6*rate:
                self.kill()
        else:
            super().update(current_time)


class Enemy2(Enemy):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./images/enemy2.png")
        self.enemy_type = 2
        self.score = 200  # 飞机分值
        self.explode_image = []
        self.explode_image.append(
            pygame.image.load('./images/enemy2_explode1.png'))
        self.explode_image.append(
            pygame.image.load('./images/enemy2_explode2.png'))
        self.explode_image.append(
            pygame.image.load('./images/enemy2_explode3.png'))
        self.explode_image.append(
            pygame.image.load('./images/enemy2_explode4.png'))

    def update(self, current_time, rate=100):
        if self.explode is True:
            if current_time > self.last_time + rate:
                self.image = self.explode_image[0]
            if current_time > self.last_time + 2*rate:
                self.image = self.explode_image[1]
            if current_time > self.last_time + 3*rate:
                self.image = self.explode_image[2]
            if current_time > self.last_time + 4*rate:
                self.image = self.explode_image[3]
            if current_time > self.last_time + 5*rate:
                self.kill()
        else:
            super().update(current_time)


class Hero(GameSprite):
    '''
    我方飞机
    '''

    def __init__(self):
        # 1.调用父类方法,创建我方飞机
        super().__init__('./images/me1.png', 0)
        #  设置飞机动态flag
        self.flag = True

        #  设置飞机垂直方向速度,默认为0
        self.vertical_speed = 0
        # 设置飞机飞行动画帧
        self.flay_image = []
        self.flay_image.append(pygame.image.load('./images/me1.png'))
        self.flay_image.append(pygame.image.load('./images/me2.png'))
        # 设置飞机爆炸帧
        self.explode_image = []
        self.explode_image.append(
            pygame.image.load('./images/me_explode0.png'))
        self.explode_image.append(
            pygame.image.load('./images/me_explode1.png'))
        self.explode_image.append(
            pygame.image.load('./images/me_explode2.png'))
        self.explode_image.append(
            pygame.image.load('./images/me_explode3.png'))
        # 2.设置飞机初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 100

        # 3.创建子弹组
        self.bullet_group = pygame.sprite.Group()

    def update(self, current_time, rate=150):
        # 飞机是否阵亡
        if self.explode is True:
            if current_time > self.last_time + rate:
                self.image = self.explode_image[0]
            if current_time > self.last_time + 2*rate:
                self.image = self.explode_image[1]
            if current_time > self.last_time + 3*rate:
                self.image = self.explode_image[2]
            if current_time > self.last_time + 4*rate:
                self.image = self.explode_image[1]
            if current_time > self.last_time + 6*rate:
                self.image = self.explode_image[2]
            if current_time > self.last_time + 7*rate:
                self.image = self.explode_image[3]
            if current_time > self.last_time + 8*rate:
                self.kill()

        else:
            # 飞机水平移动
            self.rect.x += self.speed
            # 判断飞机是否出界
            if self.rect.x < -20:  # 飞机模型有黑边
                self.rect.x = -20
            # if self.rect.x > SCREEN_RECT.width-self.rect.width:
            #    self.rect.x = SCREEN_RECT.width-self.rect.width
            elif self.rect.right > SCREEN_RECT.right+20:
                self.rect.right = SCREEN_RECT.right+20

            # 飞机垂直移动
            self.rect.y += self.vertical_speed
            if self.rect.y < -20:
                self.rect.y = -20
            elif self.rect.bottom > SCREEN_RECT.bottom+20:
                self.rect.bottom = SCREEN_RECT.bottom+20
            # 飞机尾部喷火
            if current_time > self.last_time + rate:
                if self.flag:
                    self.image = self.flay_image[1]
                    self.flag = False
                else:
                    self.image = self.flay_image[0]
                    self.flag = True
                self.last_time = current_time

    def fire(self):
        if self.explode:
            return -1
        print('发射子弹')
        for i in (1, 2, 3):
            # 1.创建子弹
            bullet = Bullet()
            # 2.设置子弹位置
            bullet.rect.bottom = self.rect.y - i*20
            bullet.rect.centerx = self.rect.centerx

            # 3.将子弹添加精灵组
            self.bullet_group.add(bullet)
    # 飞机爆炸方法

        # for i in (0, 1, 2):
        #    self.image = self.explode_image[i]


class Bullet(GameSprite):

    def __init__(self):
        super().__init__('./images/bullet.png', -10)

    def update(self):
        super().update()

        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        print("子弹被销毁")


class Static_item(pygame.sprite.Sprite):
    def __init__(self, image_name, x, y, speed=0):
        # 调用父类初始化方法
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        # 在屏幕y轴移动
        self.rect.y += self.speed
