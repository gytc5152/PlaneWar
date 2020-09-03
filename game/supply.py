"""
             补给类
      /        |        \
炸弹补给包  血量补给包   英雄升级包
"""
import random
import pygame
import constants


class Supply(pygame.sprite.Sprite):
    """ 补给品基类 """
    # 补给图片
    supply_images = []
    # 补给碰撞时的图片
    supply_collide_images = []
    # 补给碰撞时的音乐地址
    collide_sound_src = None
    # 补给的状态
    active = False

    def __init__(self, screen, speed=None):
        super().__init__()
        self.screen = screen
        # 初始化静态资源
        self.img_list = []
        self.collide_img_list = []
        self.collide_sound = None
        # 加载静态资源
        self.load_src()
        # 补给飞行速度
        self.speed = speed or 10  # 默认为10
        # 补给的位置
        self.rect = self.img_list[0].get_rect()
        # 补给的宽度和高度
        self.supply_w, self.supply_h = self.img_list[0].get_size()
        # 游戏窗口的宽度和高度
        self.width, self.height = self.screen.get_size()

    def load_src(self):
        """ 加载静态资源 """
        # 补给品图片
        for img in self.supply_images:
            self.img_list.append(pygame.image.load(img))
        # 补给品碰撞的图像
        if self.supply_collide_images:
            for img in self.supply_collide_images:
                self.collide_img_list.append(pygame.image.load(img))
        # 坠毁的音乐
        if self.collide_sound_src:
            self.collide_sound = pygame.mixer.Sound(self.collide_sound_src)

    def move(self):
        """ 补给品自上而下移动 """
        self.rect.top += self.speed

    @property
    def image(self):
        return self.img_list[0]

    def blit_me(self):
        self.screen.blit(self.image, self.rect)


class BombSupply(Supply):
    """ 炸弹包类 """
    # 补给图片
    supply_images = constants.BOMB_SUPPLY_IMG_LIST
    # 补给碰撞时的图片
    supply_collide_images = []
    # 补给碰撞时的音乐地址
    collide_sound_src = None
    # 炸弹包数量文字
    bomb_num_text = None
    # 炸弹包数量文字位置
    bomb_num_text_rect = None

    def __init__(self, screen, speed):
        super().__init__(screen, speed)
        self.init_pos()
        # 炸弹数量
        self.bomb_num = constants.BOMB_INIT_NUM
        # 加载补给品静态图片
        self.bomb_static_img = pygame.image.load(constants.BOMB_NUM_IMG)
        # 补给品静态图片位置
        self.bomb_static_img_rect = self.bomb_static_img.get_rect()
        # 炸弹数量字体
        self.bomb_num_text_font = pygame.font.Font(constants.BOMB_NUM_FONT, 30)

    def init_pos(self):
        """ 改变补给位置 """
        # 屏幕的宽度-补给的宽度
        self.rect.left = random.randint(0, self.width - self.supply_w)
        # 屏幕之外的随机高度
        self.rect.top = random.randint(-5 * self.supply_h, -self.supply_h)

    def update(self, war):
        """ 更新补给品 """
        # 更新补给包文字数量
        self.bomb_num_text = self.bomb_num_text_font.render(
            " x {0}".format(self.bomb_num),
            False,
            constants.BOMB_NUM_FONT_COLOR
        )
        # 更新补给包文字数量范围
        self.bomb_num_text_rect = self.bomb_num_text.get_rect()
        # 绘制炸弹包数量图片
        self.screen.blit(
            self.bomb_static_img,
            (10, self.height - 10 - self.bomb_static_img_rect.height)
        )
        # 绘制炸弹包数量文字
        self.screen.blit(
            self.bomb_num_text,
            (15 + self.bomb_static_img_rect.width, self.height - 12 - self.bomb_num_text_rect.height)
        )
        if self.active:
            # 补给移动
            self.move()
            # 绘制补给
            self.blit_me()
            # 超出范围
            if self.rect.top >= self.height:
                self.active = False
            # 碰撞检测
            if pygame.sprite.collide_mask(self, war.our_plane):
                self.active = False
                if self.bomb_num < 3:
                    self.bomb_num += 1
                self.reset()

    def reset(self):
        """ 重置补给 """
        # 改变随机位置
        self.init_pos()

    def boom(self, war):
        """ 炸弹爆炸，清空所有敌方飞机"""
        if self.bomb_num:
            self.bomb_num -= 1
        for each in war.enemies:
            if each.rect.bottom > 0:
                each.active = False


class HPSupply(Supply):
    """ 血包类 """
    # 补给图片
    supply_images = constants.HP_SUPPLY_IMG
    # 补给碰撞时的图片
    supply_collide_images = []
    # 补给碰撞时的音乐地址
    collide_sound_src = None

    def __init__(self, screen, speed):
        super().__init__(screen, speed)
        self.init_pos()

    def init_pos(self):
        """ 改变补给位置 """
        # 屏幕的宽度-补给的宽度
        self.rect.left = random.randint(0, self.width - self.supply_w)
        # 屏幕之外的随机高度
        self.rect.top = random.randint(-6 * self.supply_h, -self.supply_h)

    def update(self, war):
        """ 更新补给品 """
        if self.active:
            # 补给移动
            self.move()
            # 绘制补给
            self.blit_me()
            # 超出范围
            if self.rect.top >= self.height:
                self.active = False
            # 碰撞检测
            if pygame.sprite.collide_mask(self, war.our_plane):
                self.active = False
                if war.our_plane.hp < 3:
                    war.our_plane.hp += 1
                self.reset()

    def reset(self):
        """ 重置补给 """
        # 改变随机位置
        self.init_pos()


class BulletsSupply(Supply):
    """ 子弹升级道具 """
    # 补给图片
    supply_images = constants.BULLET_SUPPLY_IMG
    # 补给碰撞时的图片
    supply_collide_images = []
    # 补给碰撞时的音乐地址
    collide_sound_src = None

    def __init__(self, screen, speed):
        super().__init__(screen, speed)
        self.init_pos()

    def init_pos(self):
        """ 改变补给位置 """
        # 屏幕的宽度-补给的宽度
        self.rect.left = random.randint(0, self.width - self.supply_w)
        # 屏幕之外的随机高度
        self.rect.top = random.randint(-6 * self.supply_h, -self.supply_h)

    def update(self, war):
        """ 更新补给品 """
        if self.active:
            # 补给移动
            self.move()
            # 绘制补给
            self.blit_me()
            # 超出范围
            if self.rect.top >= self.height:
                self.active = False
            # 碰撞检测
            if pygame.sprite.collide_mask(self, war.our_plane):
                war.our_plane.bullet_mode = 'super'
                self.active = False

    def reset(self):
        """ 重置补给 """
        # 改变随机位置
        self.init_pos()