"""
子弹类的封装
"""
import pygame
import constants


class Bullet(pygame.sprite.Sprite):
    """ 子弹的基类 """

    # 子弹的图片
    bullte_image = None
    # 子弹发射的音乐
    shoot_sound_src = None
    # 子弹状态，True：活着
    active = True

    def __init__(self, screen, plane, speed=None):
        super().__init__()
        self.screen = screen
        self.plane = plane
        self.speed = speed or 10   # 速度
        self.load_src()
        self.init_bullet_pos(self.plane)

    def init_bullet_pos(self, plane):
        """ 初始化子弹的位置 """
        self.rect = self.image.get_rect()
        self.rect.centerx = plane.rect.centerx
        self.rect.top = plane.rect.top

    def load_src(self):
        """ 加载子弹的静态资源 """
        # 加载子弹的图片
        self.image = pygame.image.load(self.bullte_image)
        # 发射的音乐效果
        if self.shoot_sound_src:
            self.shoot_sound = pygame.mixer.Sound(self.shoot_sound_src)
            self.shoot_sound.set_volume(0.3)
            self.shoot_sound.play()


class OurPlaneBullet(Bullet):
    """ 我方飞机子弹类 """

    # 子弹的图片
    bullte_image = constants.BULLET_IMG
    # 子弹发射的音乐
    shoot_sound_src = constants.BULLET_SHOOT_SOUND
    # 子弹状态，True：活着
    active = True

    def update(self, war):
        """ 更新子弹的位置"""
        # 子弹移动
        self.rect.top -= self.speed
        # 超出屏幕的范围
        if self.rect.top < 0:
            self.remove(self.plane.bullets)
        # 绘制子弹
        self.screen.blit(self.image, self.rect)

        # 检测子弹是否已经碰撞到了敌方飞机
        rest = pygame.sprite.spritecollide(self, war.enemies, False)
        for r in rest:
            # 清除子弹
            self.kill()
            # 敌机对象的hp减1
            r.hp -= 1
            # hp为0时飞机死亡
            if not r.hp:
                war.kill_enemies_num += 1
                r.active = False


class OurPlaneBulletLeft(OurPlaneBullet):
    """ 飞机左侧子弹类 """

    def init_bullet_pos(self, plane):
        # 左侧子弹位置
        self.rect = self.image.get_rect()
        self.rect.centerx = plane.rect.centerx + 31
        self.rect.top = plane.rect.top + 50


class OurPlaneBulletRight(OurPlaneBullet):
    """ 飞机右侧子弹类 """

    def init_bullet_pos(self, plane):
        # 左侧子弹位置
        self.rect = self.image.get_rect()
        self.rect.centerx = plane.rect.centerx - 32
        self.rect.top = plane.rect.top + 50


class BigEnemyPlaneBullet(Bullet):

    # 子弹的图片
    bullte_image = constants.BIG_ENEMY_BULLET_IMG
    # 子弹发射的音乐
    shoot_sound_src = None
    # 子弹状态，True：活着
    active = True

    def init_bullet_pos(self, plane):
        self.rect = self.image.get_rect()
        self.rect.center = (plane.rect.centerx, plane.rect.centery + 0.5 * plane.plane_h)

    def update(self, war):
        """ 事件更新 """
        self.rect.top += self.speed
        # 超出屏幕的范围
        if self.rect.top > war.height:
            self.remove(self.plane.big_enemy_plane_bullets)
        # 绘制子弹
        self.screen.blit(self.image, self.rect)

        # 碰撞检测(检测子弹是否已经碰撞到了我方飞机)
        rest = pygame.sprite.collide_rect(self, war.our_plane)
        if rest:
            # 清除所有子弹
            self.plane.big_enemy_plane_bullets.empty()
            war.our_plane.active = False