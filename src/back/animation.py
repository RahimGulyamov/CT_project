import pygame


class Animation:
    def __init__(self, path_to_dir, amount_of_paints, size, frequency=1):
        self.path_to_dir = path_to_dir
        self.image = []
        for i in range(amount_of_paints):
            self.image.append(pygame.image.load(self.path_to_dir + str(i) + ".png").convert_alpha())
            self.image[i] = pygame.transform.scale(
                self.image[i], size)

        self.amount_of_paints = amount_of_paints
        self.frequency = frequency
        self.num_of_image = 0

    def get_image(self):
        self.num_of_image += 1
        self.num_of_image %= (self.amount_of_paints * self.frequency)
        return self.image[self.num_of_image // self.frequency]

