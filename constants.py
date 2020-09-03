""" 项目静态资源地址 """
import os
import pygame

# 项目的根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 静态文件的目录
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')


# 背景图片
BG_IMG = os.path.join(ASSETS_DIR, 'images/background.png')
# 游戏图标
GAME_ICON_IMG = os.path.join(ASSETS_DIR, 'images/icon.ico')
# 游戏结束背景图片
BG_IMG_OVER = os.path.join(ASSETS_DIR, 'images/game_over.png')
# 标题图片
IMG_GAME_TITLE = os.path.join(ASSETS_DIR, 'images/game_title.png')
# 开始游戏的按钮
IMG_GAME_START_BTN = os.path.join(ASSETS_DIR, 'images/game_start.png')
# 游戏暂停标识符
IMG_GAME_STOP = os.path.join(ASSETS_DIR, 'images/game_stop.png')
# 游戏暂停的按钮
IMG_GAME_PAUSE_NOR_BTN = os.path.join(ASSETS_DIR, 'images/game_pause_nor.png')
IMG_GAME_PAUSE_BTN = os.path.join(ASSETS_DIR, 'images/game_pause_pressed.png')
# 游戏恢复的按钮
IMG_GAME_RESUME_NOR_BTN = os.path.join(ASSETS_DIR, 'images/game_resume_nor.png')
IMG_GAME_RESUME_BTN = os.path.join(ASSETS_DIR, 'images/game_resume_pressed.png')
# 游戏重新开始的按钮
IMG_GAME_RESTART_BTN = os.path.join(ASSETS_DIR, 'images/game_restart.png')
# 背景音乐
BG_MUSIC = os.path.join(ASSETS_DIR, 'sounds/game_bg_music.mp3')
# 游戏分数颜色
TEXT_SCORE_COLOR = pygame.Color(255,255,255)
# 游戏分数字体
TEXT_SCORE_FONT = os.path.join(ASSETS_DIR, 'fonts/font.ttf')
# 击中小型飞机获得10分
SCORE_SHOOT_SMALL = 50
# 击中小型飞机获得10分
SCORE_SHOOT_MEDIUM = 200
# 击中小型飞机获得10分
SCORE_SHOOT_BIG = 600
# 我方飞机生命值
OUR_PLANE_HP = 3
# 我方飞机hp图片
OUR_PLANE_HP_IMG = os.path.join(ASSETS_DIR, 'images/hp.png')
# 敌方小型飞机生命值
SMALL_ENEMY_HP = 1
# 敌方中型飞机生命值
MEDIUM_ENEMY_HP = 3
# 敌方大型飞机生命值
BIG_ENEMY_HP = 8
# 敌方飞机拥有HP的颜色
ENEMY_REST_HP_COLOR = (255, 0, 0)
# 敌方飞机损失HP颜色
ENEMY_REDUCE_HP_COLOR = (0, 255, 0)
# 游戏结果存储的文件地址
PLAY_RESULT_STORE_FILE = os.path.join(BASE_DIR, 'store/rest.txt')

# 我方飞机静态资源
OUR_PLANE_IMG_LIST = [
    os.path.join(ASSETS_DIR, 'images/hero1.png'),
    os.path.join(ASSETS_DIR, 'images/hero2.png')
]
OUR_DESTROY_IMG_LIST = [
    os.path.join(ASSETS_DIR, 'images/hero_broken_n1.png'),
    os.path.join(ASSETS_DIR, 'images/hero_broken_n2.png'),
    os.path.join(ASSETS_DIR, 'images/hero_broken_n3.png'),
    os.path.join(ASSETS_DIR, 'images/hero_broken_n4.png')
]

# 我方飞机子弹图片
BULLET_IMG = os.path.join(ASSETS_DIR, 'images/bullet1.png')
# 敌方大型飞机子弹图片
BIG_ENEMY_BULLET_IMG = os.path.join(ASSETS_DIR, 'images/bullet2.png')
# 我方飞机子弹发射声音
BULLET_SHOOT_SOUND = os.path.join(ASSETS_DIR, 'sounds/bullet.wav')

# 敌方小型飞机图片及音效
SMALL_ENEMY_PLANE_IMG_LIST = [os.path.join(ASSETS_DIR, 'images/enemy1.png')]
SMALL_PLANE_DESTROY_IMG_LIST = [
    os.path.join(ASSETS_DIR, 'images/enemy1_down1.png'),
    os.path.join(ASSETS_DIR, 'images/enemy1_down2.png'),
    os.path.join(ASSETS_DIR, 'images/enemy1_down3.png'),
    os.path.join(ASSETS_DIR, 'images/enemy1_down4.png')
]
SMALL_ENEMY_PLANE_DOWN_SOUND = os.path.join(ASSETS_DIR, 'sounds/enemy1_down.wav')

# 敌方中型飞机图片及音效
MEDIUM_ENEMY_PLANE_IMG_LIST = [os.path.join(ASSETS_DIR, 'images/enemy2.png')]
MEDIUM_PLANE_DESTROY_IMG_LIST = [
    os.path.join(ASSETS_DIR, 'images/enemy2_down1.png'),
    os.path.join(ASSETS_DIR, 'images/enemy2_down2.png'),
    os.path.join(ASSETS_DIR, 'images/enemy2_down3.png'),
    os.path.join(ASSETS_DIR, 'images/enemy2_down4.png')
]
MEDIUM_ENEMY_PLANE_DOWN_SOUND = os.path.join(ASSETS_DIR, 'sounds/enemy2_down.wav')

# 敌方大型飞机图片及音效
BIG_ENEMY_PLANE_IMG_LIST = [
    os.path.join(ASSETS_DIR, 'images/enemy3_n1.png'),
    os.path.join(ASSETS_DIR, 'images/enemy3_n2.png'),
    os.path.join(ASSETS_DIR, 'images/enemy3_hit.png')
]
BIG_PLANE_DESTROY_IMG_LIST = [
    os.path.join(ASSETS_DIR, 'images/enemy3_down1.png'),
    os.path.join(ASSETS_DIR, 'images/enemy3_down2.png'),
    os.path.join(ASSETS_DIR, 'images/enemy3_down3.png'),
    os.path.join(ASSETS_DIR, 'images/enemy3_down4.png')
]
BIG_ENEMY_PLANE_DOWN_SOUND = os.path.join(ASSETS_DIR, 'sounds/enemy3_down.wav')

# 炸弹包初始数量
BOMB_INIT_NUM = 3
# 炸弹包随机出现的时间间隔
BOMB_APPEAR_TIME = 15 * 1000  # 毫秒
# 炸弹包数量字体
BOMB_NUM_FONT = os.path.join(ASSETS_DIR, 'fonts/font.ttf')
# 炸弹包数量字体颜色
BOMB_NUM_FONT_COLOR = (255,255,255)
# 炸弹补给图片
BOMB_SUPPLY_IMG_LIST = [os.path.join(ASSETS_DIR, 'images/bomb_supply.png')]
# 炸弹包数量图片
BOMB_NUM_IMG = os.path.join(ASSETS_DIR, 'images/bomb.png')
# 血包补给图片
HP_SUPPLY_IMG = [os.path.join(ASSETS_DIR, 'images/hp_supply.png')]
# 血包随机出现的时间间隔
HP_APPEAR_TIME = 30 * 1000
# 子弹补给图片
BULLET_SUPPLY_IMG = [os.path.join(ASSETS_DIR, 'images/bullet_supply.png')]
# 每击败100敌机出现子弹补给
BULLET_SUPPLY_APPEAR_NUM = 100