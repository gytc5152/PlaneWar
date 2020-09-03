import pygame
import sys
import constants
from game.plane import OurPlane, SmallEnemyPlane, MediumEnemyPlane, BigEnemyPlane
from game.supply import BombSupply, HPSupply, BulletsSupply
from store.result import PlayRest


class PlaneWar(object):
    """ 飞机大战 """
    # 游戏状态
    READY = 0    # 游戏准备中
    PLAYING = 1  # 游戏中
    PAUSED = 2  # 游戏暂停
    OVER = 3     # 游戏结束
    status = READY  # 0 准备中 1 游戏中 2 游戏暂停 3 游戏结束

    # 计数器
    frame = 0  # 播放帧数
    delay = 100  # 延迟播放计数
    kill_enemies_num = 0  # 记录击落敌机数目

    # 我方飞机
    our_plane = None
    # 添加敌方飞机（一架飞机可以属于多个精灵组）
    small_enemies = pygame.sprite.Group()   # 小型敌机
    medium_enemies = pygame.sprite.Group()  # 中型敌机
    big_enemies = pygame.sprite.Group()     # 大型敌机
    enemies = pygame.sprite.Group()
    # 游戏结果
    rest = PlayRest()

    def __init__(self):
        # pgame游戏初始化
        pygame.init()
        # 设置屏幕游戏宽度和高度
        self.width, self.height = 480, 852
        # 加载屏幕对象
        self.screen = pygame.display.set_mode((self.width, self.height))
        # 设置窗口标题
        pygame.display.set_caption('飞机大战')
        # 加载游戏图标
        gameIcon = pygame.image.load(constants.GAME_ICON_IMG)
        pygame.display.set_icon(gameIcon)
        # 加载游戏背景图片
        self.bg = pygame.image.load(constants.BG_IMG)
        # 加载游戏结束背景图片
        self.bg_over = pygame.image.load(constants.BG_IMG_OVER)
        # 加载游戏标题图片
        self.img_game_title = pygame.image.load(constants.IMG_GAME_TITLE)
        # 设置游戏标题宽度和高度
        self.img_game_title_rect = self.img_game_title.get_rect()
        t_width, t_height = self.img_game_title.get_size()
        self.img_game_title_rect.topleft = (int((self.width - t_width) / 2),
                                       int(self.height / 2 - t_height))
        # 加载游戏开始按钮图片
        self.btn_start = pygame.image.load(constants.IMG_GAME_START_BTN)
        # 设置游戏开始按钮宽度和高度
        self.btn_start_rect = self.btn_start.get_rect()
        self.btn_width, btn_height = self.btn_start.get_size()
        self.btn_start_rect.topleft = (int((self.width - self.btn_width) / 2),
                                  int(self.height / 2 + btn_height))
        # 加载暂停按钮图片
        self.btn_paused_nor = pygame.image.load(constants.IMG_GAME_PAUSE_NOR_BTN)
        self.btn_paused = pygame.image.load(constants.IMG_GAME_PAUSE_BTN)
        # 加载暂停恢复按钮图片
        self.btn_resume_nor = pygame.image.load(constants.IMG_GAME_RESUME_NOR_BTN)
        self.btn_resume = pygame.image.load(constants.IMG_GAME_RESUME_BTN)
        # 暂停键按钮范围值
        self.paused_rect = self.btn_paused_nor.get_rect()
        self.paused_rect.left, self.paused_rect.top = self.width - self.paused_rect.width - 10, 10
        self.paused_image = self.btn_paused_nor
        self.resume_image = self.btn_resume_nor
        # 加载暂停标识符
        self.img_game_paused = pygame.image.load(constants.IMG_GAME_STOP)
        # 暂停标识符位置
        self.img_game_paused_rect = self.img_game_paused.get_rect()
        # 游戏文字对象
        self.score_font = pygame.font.Font(constants.TEXT_SCORE_FONT, 35)
        # 加载背景音乐s
        pygame.mixer.music.load(constants.BG_MUSIC)
        pygame.mixer.music.play(-1)  # 无限循环播放
        pygame.mixer.music.set_volume(0.2)  # 设置音量
        # 我方飞机对象
        self.our_plane = OurPlane(self.screen, speed=5)
        # 炸弹补给对象
        self.bomb = BombSupply(self.screen, 3)
        # 炸弹包每隔一定随机出现
        self.bomb_appear_time = pygame.USEREVENT
        pygame.time.set_timer(self.bomb_appear_time, constants.BOMB_APPEAR_TIME)
        # 血包补给对象
        self.hp_supply = HPSupply(self.screen, 3)
        # 子弹补给对象
        self.bullet_supply = BulletsSupply(self.screen, 3)
        # 炸弹包每隔一定随机出现
        self.hp_supply_appear_time = pygame.USEREVENT + 1
        pygame.time.set_timer(self.hp_supply_appear_time, constants.HP_APPEAR_TIME)
        # 设置帧速率
        self.clock = pygame.time.Clock()
        # 上次按的键盘上的某一个键，用于控制飞机
        self.key_down = None

    def bind_event(self):
        """ 绑定事件 """
        # 飞机连续移动键盘事件检测
        self.key_down = pygame.key.get_pressed()
        # 1. 监听事件
        for event in pygame.event.get():
            # 右上角关闭按钮检测
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 鼠标点击检测
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 游戏正在准备中，点击才能进入游戏
                if self.status == self.READY and self.btn_start_rect.collidepoint(event.pos):
                    # 游戏开始
                    self.status = self.PLAYING
                    # 重置英雄飞机位置
                    self.our_plane.reset_pos()
                    # 重置英雄飞机生命值
                    self.our_plane.hp = constants.OUR_PLANE_HP
                    # 重置本局分数
                    self.rest.score = 0
                elif self.status == self.PLAYING and self.paused_rect.collidepoint(event.pos):
                    # 游戏暂停
                    self.status = self.PAUSED
                    # 暂停音效
                    pygame.mixer.music.pause()
                    pygame.mixer.pause()
                    # 游戏音乐暂停
                elif self.status == self.PAUSED and self.paused_rect.collidepoint(event.pos):
                    # 游戏继续
                    self.status = self.PLAYING
                    # 恢复音效
                    pygame.mixer.music.unpause()
                    pygame.mixer.unpause()
                elif self.status == self.OVER:
                    self.status = self.READY
                    # 添加敌方飞机
                    self.add_small_enemies(6)
                    self.add_medium_enemies(2)
                    self.add_big_enemies(1)
                    # 如果游戏结束时补给包在屏幕中，则重置其位置
                    if self.bomb.active:
                        self.bomb.reset()
                    if self.hp_supply.active:
                        self.hp_supply.reset()
                    # 重置击落敌机数量
                    self.kill_enemies_num = 0
            # 鼠标放置坐标检测
            elif event.type == pygame.MOUSEMOTION:
                if self.paused_rect.collidepoint(event.pos):
                    if self.status == self.PAUSED:
                        self.paused_image = self.btn_resume
                    else:
                        self.paused_image = self.btn_paused
                else:
                    if self.status == self.PAUSED:
                        self.paused_image = self.btn_resume_nor
                    else:
                        self.paused_image = self.btn_paused_nor
            # 单次敲击键盘事件监测
            elif event.type == pygame.KEYDOWN:
                if self.status == self.PLAYING:
                    # J键发射子弹
                    if event.key == pygame.K_j:
                        self.our_plane.shoot()
                    # 空格键发射导弹包
                    if event.key == pygame.K_SPACE and self.bomb.bomb_num:
                        self.bomb.boom(self)
            # 炸弹包补给时间检测
            elif event.type == self.bomb_appear_time:
                self.bomb.active = True
                self.bomb.reset()
            # 血包补给时间检测
            elif event.type == self.hp_supply_appear_time:
                self.hp_supply.active = True
                self.hp_supply.reset()

    def add_small_enemies(self, num):
        """
        随机产生n架小型敌机
        :param num: 飞机产生数量
        :return:
        """
        for i in range(num):
            plane = SmallEnemyPlane(self.screen, 4)
            plane.add(self.small_enemies, self.enemies)

    def add_medium_enemies(self, num):
        """
        随机产生n架中型敌机
        :param num: 飞机产生数量
        :return:
        """
        for i in range(num):
            plane = MediumEnemyPlane(self.screen, 2)
            plane.add(self.medium_enemies, self.enemies)

    def add_big_enemies(self, num):
        """
        随机产生n架大型敌机
        :param num: 飞机产生数量
        :return:
        """
        for i in range(num):
            plane = BigEnemyPlane(self.screen, 1)
            plane.add(self.big_enemies, self.enemies)

    def run_game(self):
        """ 游戏主循环部分 """
        while True:
            # 设置帧速率
            self.clock.tick(60)
            # 处理计数器
            self.frame += 1
            self.delay -= 1
            if self.frame >= 60:
                self.frame = 0
            if not self.delay:
                self.delay = 100
            # 事件处理
            self.bind_event()
            # 更新游戏的状态
            if self.status == self.READY:  # 游戏正在准备中
                # 绘制背景
                self.screen.blit(self.bg, self.bg.get_rect())
                # 标题
                self.screen.blit(self.img_game_title, self.img_game_title_rect)
                # 开始按钮
                self.screen.blit(self.btn_start, self.btn_start_rect)
                self.key_down = None
            elif self.status == self.PLAYING:  # 游戏进行中
                # 绘制背景
                self.screen.blit(self.bg, self.bg.get_rect())
                # 绘制暂停按钮
                self.screen.blit(self.paused_image, self.paused_rect)
                # 绘制我方飞机
                self.our_plane.update(self)
                # 绘制敌方飞机
                self.small_enemies.update(self)
                self.medium_enemies.update(self)
                self.big_enemies.update(self)
                # 绘制炸弹补给包
                self.bomb.update(self)
                # 绘制血包
                self.hp_supply.update(self)
                # 每击败一定数量敌机，出现子弹补给包
                self.bullet_supply.update(self)
                if self.kill_enemies_num > 0 and not self.kill_enemies_num % constants.BULLET_SUPPLY_APPEAR_NUM:
                    self.bullet_supply.active = True
                    self.bullet_supply.reset()
                    self.bullet_supply.update(self)
                # 游戏分数
                score_text = self.score_font.render(
                    'Score : {0}'.format(self.rest.score),
                    False,
                    constants.TEXT_SCORE_COLOR
                )
                self.screen.blit(score_text, score_text.get_rect())
            elif self.status == self.PAUSED:
                # 绘制背景
                self.screen.blit(self.bg, self.bg.get_rect())
                # 绘制暂停恢复按钮
                self.screen.blit(self.paused_image, self.paused_rect)
                # 绘制暂停标识符
                self.screen.blit(
                    self.img_game_paused,
                    (
                        (self.width - self.img_game_paused_rect.width) / 2,
                        (self.height - self.img_game_paused_rect.height) / 2,
                    )
                )
            elif self.status == self.OVER:
                # 游戏背景
                self.screen.blit(self.bg_over, self.bg_over.get_rect())
                # 分数统计
                # 本次总分
                score_text = self.score_font.render(
                    '{0}'.format(self.rest.score),
                    False,
                    constants.TEXT_SCORE_COLOR
                )
                score_text_rect = score_text.get_rect()
                text_w, text_h = score_text.get_size()
                # 改变文字的位置
                score_text_rect.topleft = (
                    int((self.width - text_w) / 2),
                    int(self.height / 2)
                )
                self.screen.blit(score_text, score_text_rect)
                # 历史最高分
                score_his = self.score_font.render(
                    '{0}'.format(self.rest.get_max_score()),
                    False,
                    constants.TEXT_SCORE_COLOR
                )
                self.screen.blit(score_his, (150, 40))
            pygame.display.flip()
