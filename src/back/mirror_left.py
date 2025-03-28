from PIL import Image


for i in range(8):
    # Загрузка изображения
    img = Image.open("../tile_sets/tiles_for_chars/personages/wizard/stat/sprite_" + str(0) + ".png")

    # Отражение изображения
    img_mirror = img.transpose(Image.FLIP_LEFT_RIGHT)

    # Сохранение полученного изображения
    img_mirror.save("../tile_sets/tiles_for_chars/personages/wizard/stat_left/sprite_" + str(i) + ".png")
