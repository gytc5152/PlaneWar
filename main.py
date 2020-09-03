from game.war import PlaneWar


def main():
    """ 游戏入口，main方法 """
    war = PlaneWar()
    # 添加小型敌方飞机
    war.add_small_enemies(6)
    war.add_medium_enemies(2)
    war.add_big_enemies(1)
    war.run_game()


if __name__ == '__main__':
    main()
