import pygame
import os

'''
module map gồm có 1 class map có dùng để xây dựng map cho game
Game hiện tại sẽ gồm 6 map khi vượt qua hết map ngươi chơi sẽ chiến thắng game
'''

screen_width = 1000
screen_height = 600
#  Từ điển number_zombie chứa số zombie mỗi map người chơi cần tiêu diệt để vượt qua map hiện tại
number_zombie = {'map1': 10, 'map2': 15, 'map3': 20, 'map4': 25, 'map5': 30, 'map6': 40}


class Map:
    def __init__(self):
        self.maps = {}
        # Đọc các hình ảnh của từng map và lưu vào trong từ điển maps
        for i in os.listdir('../map'):
            arr = []
            for j in os.listdir(f'../map/{i}'):
                arr.append(pygame.image.load(f'../map/{i}/{j}'))
            self.maps[str(i)] = arr
        for image in self.maps.values():
            self.tranfom(image)

    def tranfom(self, image_list):
        """
        Phương thức chỉnh sửa hình ảnh kích cỡ của map
        :param image_list: danh sách chứa 2 hình ảnh là hình ảnh map và phần mặt đát của map
        :return:
        """
        if image_list[0].get_height() > image_list[1].get_height():
            tmp = image_list[0].get_height() // image_list[1].get_height()
        else:
            tmp = image_list[1].get_height() // image_list[0].get_height()
        image_list[0] = pygame.transform.scale(image_list[0], (screen_width, screen_height))
        image_list[1] = pygame.transform.scale(image_list[1], (screen_width, screen_height // tmp))

    def get_map(self, map_name):
        """
         Phương thức lấy map hiện tại người chơi đang chơi
        :param map_name: tên map hiện tại
        :return:
        """
        return self.maps[map_name]
