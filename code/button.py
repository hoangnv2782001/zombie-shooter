import pygame
from pygame.locals import *

'''
module button dùng để tạo các button trong game 
Button là class để tạo các nut bấm điều khiển
Button1 là class dùng để tạo các nut bấm có hình ảnh 
'''
pygame.init()
font = pygame.font.Font('../font/gamecuben.ttf', 20)
# các màu đc sử dụng
bg = (204, 102, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)


class Button:
    button_col = (255, 0, 0)
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = black
    width = 180
    height = 70

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw_button(self, screen):
        """
        vẽ button lên màn hình
        :param screen: đối tg màn hình vẽ lên
        :return: True nếu nhấn nút False nếu ngc lại
        """

        pos = pygame.mouse.get_pos()
        click = False  

        button_rect = Rect(self.x, self.y, self.width, self.height)

        # Kiểm tra việc nhấn nút
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                click = True
                pygame.draw.rect(screen, self.click_col, button_rect)
            else:
                pygame.draw.rect(screen, self.hover_col, button_rect)
        else:
            pygame.draw.rect(screen, self.button_col, button_rect)

        # Hiển thị button lên màn hình
        pygame.draw.line(screen, white, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(screen, white, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(screen, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(screen, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))

        return click


class Button1:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    
    def draw(self, surface):
        """
        Hiển thị button lên màn hình
        :param surface: đối tg màn hình vẽ lên bản chất chính là screen
        :return: True nếu nhấn nút False nếu ngc lại
        """
        click = False  
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and click == False:
                click = True
        
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return click
