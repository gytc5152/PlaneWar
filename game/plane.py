"""
                   飞机类
我方的飞机  敌方小型飞机  敌方中型飞机  敌方大型飞机
"""
import random
import pygame
import constants
from game.bullet import OurPlaneBullet, BigEnemyPlaneBullet, OurPlaneBulletLeft, OurPlaneBulletRight


class Plane(pygame.sprite.Sprite):
    """ 飞机的基础类 """
    # 飞机的移动的图片
    plane_images = []
    # 飞机爆炸的图片
    destroy_images = []
    # 坠毁的音乐地址
    down_sound_src = None
    # 飞机的状态：True, 活的；False, 死的
    active = True
    # 飞机坠毁索引
    destroy_index = 0

    def __init__(self, screen, speed=None):
        super().__init__()
        self.screen = screen
        # 初始化静态资源
        self.img_list = []
        self.destroy_img_list = []
        self.down_sound = None
        # 加载静态资源
        self.load_src()
        # 飞行的速度
        self.speed = speed or 10  # 默认为10
        # 获取飞机的位置
        self.rect = self.img_list[0].get_rect()
        # 飞机的宽度和高度
        self.plane_w, self.plane_h = self.img_list[0].get_size()
        # 游戏窗口的宽度和高度
        self.width, self.height = self.screen.get_size()

    def load_src(self):
        """加载静态资源"""
        # 飞机图像
        for img in self.plane_images:
            self.img_list.append(pygame.image.load(img))
        # 飞机坠毁的图像
        for img in self.destroy_images:
            self.destroy_img_list.append(pygame.image.load(img))
        # 坠毁的音乐
        if self.down_sound_src:
            self.down_sound = pygame.mixer.Sound(self.down_sound_src)

    # property:可以用调用属性的形式来调用方法,后面不需要加()
    @property
    def image(self):
        return self.img_list[0]

    def blit_me(self):
        self.screen.blit(self.image, self.rect)

    def move_up(self):
        """ 飞机向上移动 """
        self.rect.top -= self.speed

    def move_down(self):
        """ 飞机向下移动 """
        self.rect.top += self.speed

    def move_left(self):
        """ 飞机向左移动 """
        self.rect.left -= self.speed

    def move_right(self):
        """ 飞机向右移动 """
        self.rect.left += self.speed


class OurPlane(Plane):
    """ 我方的飞机 """

    # 飞机的图片
    plane_images = constants.OUR_PLANE_IMG_LIST
    # 飞机爆炸的图片
    destroy_images = constants.OUR_DESTROY_IMG_LIST
    # 飞机坠毁的音乐地址
    down_sound_src = None
    # 飞机发射的子弹精灵组
    bullets = pygame.sprite.Group()
    # 飞机血量
    hp = constants.OUR_PLANE_HP
    # 飞机生命值图片
    hp_image_src = constants.OUR_PLANE_HP_IMG
    # 飞机子弹模式
    bullet_mode = 'normal'

    def __init__(self, screen, speed):
        super().__init__(screen, speed)  # 继承父类中的属性和方法并添加新属性
        self.hp_w, self.hp_h = self.hp_image.get_size()

    def update(self, war):
        """ 更新飞机的动画效果 """
        if self.active:
            # 我方飞机发射子弹
            self.bullets.update(war)
            # 控制我方飞机移动
            self.move(war.key_down)

            # 切换飞机的动画效果，喷气式效果
            if war.frame % 5:
                self.screen.blit(self.img_list[0], self.rect)
            else:
                self.screen.blit(self.img_list[1], self.rect)

            # 我方飞机血量绘制
            for i in range(self.hp):
                hp_left = self.width - 10 - (i + 1) * self.hp_w
                hp_top = self.height - 10 - self.hp_h
                self.screen.blit(self.hp_image, (hp_left, hp_top))

            # 检测飞机是否碰撞到敌机
            rest = pygame.sprite.spritecollide(self, war.enemies, False)
            if rest:
                self.active = False
                # 清除碰撞后的敌机S
                for r in rest:
                    r.active = False
        else:
            # 飞机坠毁
            self.broken_down(war)

    def move(self, key):
        """ 飞机移动自动控制 """
        if key[pygame.K_UP] or key[pygame.K_w]:
            self.move_up()
        elif key[pygame.K_DOWN] or key[pygame.K_s]:
            self.move_down()
        elif key[pygame.K_LEFT] or key[pygame.K_a]:
            self.move_left()
        elif key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.move_right()

    def move_up(self):
        """ 向上移动，超出范围之后，拉回来 """
        super().move_up()
        if self.rect.top <= 0:
            self.rect.top = 0

    def move_down(self):
        """ 向下移动，超出范围之后，拉回来 """
        super().move_down()
        if self.rect.top >= self.height - self.plane_h:
            self.rect.top = self.height - self.plane_h

    def move_left(self):
        """ 向左移动，超出范围之后，拉回来 """
        super().move_left()
        if self.rect.left <= 0:
            self.rect.left = 0

    def move_right(self):
        """ 向右移动，超出范围之后，拉回来 """
        super().move_right()
        if self.rect.left >= self.width - self.plane_w:
            self.rect.left = self.width - self.plane_w

    def shoot(self):
        """ 我方飞机发射子弹 """
        bullet = OurPlaneBullet(self.screen, self, 15)
        self.bullets.add(bullet)
        if self.bullet_mode == 'super':
            bullet_left = OurPlaneBulletLeft(self.screen, self, 15)
            bullet_right = OurPlaneBulletRight(self.screen, self, 15)
            self.bullets.add(bullet_left, bullet_right)

    def load_src(self):
        """ 继承并重写飞机类静态资源加载方法 """
        super().load_src()
        self.hp_image = pygame.image.load(self.hp_image_src)

    def reset_pos(self):
        """ 重置飞机位置 """
        self.rect.left = int((self.width - self.plane_w) / 2)
        self.rect.top = int(self.height / 2)
        # 重置飞机状态
        self.active = True

    def broken_down(self, war):
        """ 飞机坠毁效果 """
        # 播放坠毁音乐
        if self.destroy_index == 0 and self.down_sound:
            self.down_sound.play()

        if not(war.delay % 2):
            # 播放坠毁动画
            self.screen.blit(self.destroy_img_list[self.destroy_index], self.rect)
            self.destroy_index = (self.destroy_index + 1) % len(self.destroy_img_list)
            if self.destroy_index == 0:
                # 飞机生命值减1
                self.hp -= 1
                # 重置飞机位置
                self.reset_pos()
                if not self.hp:
                    # 游戏结束
                    war.status = war.OVER
                    # 清除敌方飞机
                    war.enemies.empty()
                    war.small_enemies.empty()
                    war.medium_enemies.empty()
                    war.big_enemies.empty()


class SmallEnemyPlane(Plane):
    """ 敌方小型飞机 """
    # 飞机的图片
    plane_images = constants.SMALL_ENEMY_PLANE_IMG_LIST
    # 飞机爆炸的图片
    destroy_images = constants.SMALL_PLANE_DESTROY_IMG_LIST
    # 坠毁的音乐地址
    down_sound_src = constants.SMALL_ENEMY_PLANE_DOWN_SOUND
    # 血量
    hp = constants.SMALL_ENEMY_HP

    def __init__(self, screen, speed):
        super().__init__(screen, speed)
        # 每次生成一架新的小型飞机的时候，随机位置出现在屏幕中
        # 改变飞机的随机位置
        self.init_pos()

    def init_pos(self):
        """ 改变飞机的随机位置 """
        # 屏幕的宽度-飞机的宽度
        self.rect.left = random.randint(0, self.width - self.plane_w)
        # 屏幕之外的随机高度，
        self.rect.top = random.randint(-5 * self.plane_h, -self.plane_h)

    def update(self, war):
        """ 更新飞机 """
        if self.active:
            # 飞机移动
            self.move_down()
            # 绘制飞机
            self.blit_me()
            # 超出范围后飞机回收飞机
            if self.rect.top >= self.height:
                self.active = False
                self.reset()
        else:
            # 飞机坠毁
            self.broken_down(war)

    def reset(self):
        """ 重置飞机的状态、达到复用效果 """
        # 改变飞机的随机位置
        self.init_pos()
        # 改变飞机状态
        self.active = True
        # 重置hp的值
        self.hp = constants.SMALL_ENEMY_HP

    def broken_down(self, war):
        """ 飞机坠毁效果 """
        # 播放坠毁音乐
        if self.destroy_index == 0 and self.down_sound:
            self.down_sound.play()

        if not(war.delay % 2):
            # 播放坠毁动画
            self.screen.blit(self.destroy_img_list[self.destroy_index], self.rect)
            self.destroy_index = (self.destroy_index + 1) % len(self.destroy_img_list)
            if self.destroy_index == 0:
                # 统计游戏成绩
                war.rest.score += constants.SCORE_SHOOT_SMALL
                # 保存历史记录
                war.rest.set_history()
                # 重置敌方飞机
                self.reset()


class MediumEnemyPlane(Plane):
    """ 敌方中型飞机 """
    # 飞机的图片
    plane_images = constants.MEDIUM_ENEMY_PLANE_IMG_LIST
    # 飞机爆炸的图片
    destroy_images = constants.MEDIUM_PLANE_DESTROY_IMG_LIST
    # 坠毁的音乐地址
    down_sound_src = constants.MEDIUM_ENEMY_PLANE_DOWN_SOUND
    # 血量
    hp = constants.MEDIUM_ENEMY_HP

    def __init__(self, screen, speed):
        super().__init__(screen, speed)
        # 改变飞机的随机位置
        self.init_pos()

    def init_pos(self):
        """ 改变飞机的随机位置 """
        # 屏幕的宽度-飞机的宽度
        self.rect.left = random.randint(0, self.width - self.plane_w)
        # 屏幕之外的随机高度
        self.rect.top = random.randint( -6 * self.plane_h, -2 * self.plane_h)

    def update(self, war):
        """ 更新飞机的移动 """
        if self.active:
            # 敌方飞机移动
            self.move_down()
            # 画在屏幕上
            self.blit_me()
            # 绘制血条
            self.update_blood()

            # 超出范围后如何处理
            # 1.重用
            if self.rect.top >= self.height:
                self.active = False
                self.reset()
        else:
            self.broken_down(war)

    def reset(self):
        """ 重置飞机的状态、达到复用效果 """
        self.active = True
        # 改变飞机的随机位置
        self.init_pos()
        # 重置hp的值
        self.hp = constants.MEDIUM_ENEMY_HP

    def broken_down(self, war):
        """ 飞机坠毁效果 """
        # 播放坠毁音乐
        if self.destroy_index == 0 and self.down_sound:
            self.down_sound.play()

        if not(war.delay % 2):
            # 播放坠毁动画
            self.screen.blit(self.destroy_img_list[self.destroy_index], self.rect)
            self.destroy_index = (self.destroy_index + 1) % len(self.destroy_img_list)
            if self.destroy_index == 0:
                # 统计游戏成绩
                war.rest.score += constants.SCORE_SHOOT_MEDIUM
                # 保存历史记录
                war.rest.set_history()
                # 重置敌方飞机
                self.reset()

    def update_blood(self):
        """ 绘制并更新血条 """
        # 绘制血槽
        draw_start = (self.rect.left, self.rect.top - constants.MEDIUM_ENEMY_HP)
        draw_end = (self.rect.right, self.rect.top - constants.MEDIUM_ENEMY_HP)
        pygame.draw.line(
            self.screen,
            constants.ENEMY_REST_HP_COLOR,
            draw_start,
            draw_end,
            3
        )
        # 计算并绘制剩余血量
        surplus_hp = self.hp / constants.MEDIUM_ENEMY_HP
        draw_end = (
            self.rect.left + self.rect.width * surplus_hp,
            self.rect.top - constants.MEDIUM_ENEMY_HP
        )
        pygame.draw.line(
            self.screen,
            constants.ENEMY_REDUCE_HP_COLOR,
            draw_start,
            draw_end,
            3
        )


class BigEnemyPlane(Plane):
    """ 敌方大型飞机 """
    # 飞机的图片
    plane_images = constants.BIG_ENEMY_PLANE_IMG_LIST
    # 飞机爆炸的图片
    destroy_images = constants.BIG_PLANE_DESTROY_IMG_LIST
    # 坠毁的音乐地址
    down_sound_src = constants.BIG_ENEMY_PLANE_DOWN_SOUND
    # 敌方飞机发射子弹的精灵组
    big_enemy_plane_bullets = pygame.sprite.Group()
    # 血量
    hp = constants.BIG_ENEMY_HP

    def __init__(self, screen, speed):
        super().__init__(screen, speed)
        # 改变飞机的随机位置
        self.init_pos()

    def init_pos(self):
        """ 改变飞机的随机位置 """
        # 屏幕的宽度-飞机的宽度
        self.rect.left = random.randint(0, self.width - self.plane_w)
        # 屏幕之外的随机高度
        self.rect.top = random.randint(-int(1.8 * self.plane_h), -int(1 * self.plane_h))

    def update(self, war):
        """ 更新飞机 """
        if self.active:
            self.move_down()  # 飞机移动
            self.play_hit_animation(war)  # 自动射击动画
            self.auto_shoot(war)  # 自动射击

            # 绘制血条
            self.update_blood()
            if len(self.big_enemy_plane_bullets) > 0:
                self.big_enemy_plane_bullets.update(war)

            # 超出范围后如何处理
            if self.rect.top >= self.height:
                self.active = False
                self.reset()
        else:
            self.broken_down(war)

    def play_hit_animation(self, war):
        """ 播放敌方飞机发射子弹时动画效果 """
        if war.frame % 5 > 2:
            self.screen.blit(self.img_list[0], self.rect)
        elif 0 < war.frame % 5 <= 2:
            self.screen.blit(self.img_list[1], self.rect)
        else:
            self.screen.blit(self.img_list[2], self.rect)

    def reset(self):
        """ 重置飞机的状态、达到复用效果 """
        self.active = True
        # 改变飞机的随机位置
        self.init_pos()
        # 重置hp的值
        self.hp = constants.BIG_ENEMY_HP

    def broken_down(self, war):
        """ 飞机爆炸 """
        super().broken_down(war)
        # 重复利用飞机对象
        self.reset()

    def auto_shoot(self, war):
        """ 敌方飞机自动发射子弹 """
        if war.frame % 60 == 0:
            bullet = BigEnemyPlaneBullet(self.screen, self, 10)
            self.big_enemy_plane_bullets.add(bullet)

    def update_blood(self):
        """ 绘制并更新血条 """
        draw_start = (self.rect.left, self.rect.top - constants.BIG_ENEMY_HP)
        draw_end = (self.rect.right, self.rect.top - constants.BIG_ENEMY_HP)
        pygame.draw.line(
            self.screen,
            constants.ENEMY_REST_HP_COLOR,
            draw_start,
            draw_end,
            3
        )
        # 计算并绘制剩余血量
        surplus_hp = self.hp / constants.BIG_ENEMY_HP
        draw_end = (
            self.rect.left + self.rect.width * surplus_hp,
            self.rect.top - constants.BIG_ENEMY_HP
        )
        pygame.draw.line(
            self.screen,
            constants.ENEMY_REDUCE_HP_COLOR,
            draw_start,
            draw_end,
            3
        )

    def broken_down(self, war):
        """ 飞机坠毁效果 """
        # 播放坠毁音乐
        if self.destroy_index == 0 and self.down_sound:
            self.down_sound.play()

        if not (war.delay % 2):
            # 播放坠毁动画
            self.screen.blit(self.destroy_img_list[self.destroy_index], self.rect)
            self.destroy_index = (self.destroy_index + 1) % len(self.destroy_img_list)
            if self.destroy_index == 0:
                # 清空敌机子弹
                self.big_enemy_plane_bullets.empty()
                # 统计游戏成绩
                war.rest.score += constants.SCORE_SHOOT_BIG
                # 保存历史记录
                war.rest.set_history()
                # 重置敌方飞机
                self.reset()