import pygame

'''
module heath gồm 2 class
HP dùng để hiển thị thanh sinh lực của nhân vật cũng như zombies
MP dùng để hiển thị thanh năng lượng của nhân vật
'''


class HP:
    def __init__(self, x, y, max, width, height):
        self.x = x
        self.y = y
        self.max_hp = max
        self.width = width
        self.height = height
        self.hp = self.max_hp

    def draw(self, screen, hp):
        """
        hiển thị thanh hp của nhan vật lên màn hình
        :param screen: đối tượng màn hình hiển thị
        :param hp: hp hiện tại
        :return:
        """
        self.hp = hp
        tmp = self.hp / self.max_hp
        pygame.draw.rect(screen, (0, 0, 0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width * tmp, self.height))

    def update(self, x, y):
        """
        cập nhật vị trí thanh hp sử dụng cho zombie
        :param x: toạ đọ x
        :param y: toạ độ y
        :return:
        """
        self.x = x
        self.y = y


class MP:
    def __init__(self):
        self.x = 10
        self.y = 34
        self.max_mp = 100
        self.mp = self.max_mp


    def draw(self, screen, mp):
        """
         Hiển thị thanh mp của nhân vật lên màn hình
        :param screen: đối tượng màn hình hiển thị
        :param mp: hp hiện tại
        :return:
        """
        self.mp = mp
        tmp = self.mp / self.max_mp
        pygame.draw.rect(screen, (0, 0, 0), (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, (255, 0, 255), (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, 150 * tmp, 20))
