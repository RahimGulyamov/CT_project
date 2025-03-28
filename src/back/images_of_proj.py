class ImageOfProj:
    def __init__(self, move_path, move_num, blast_path, blast_num, name, frequency):
        self.move_path = move_path
        self.move_num = move_num
        self.blast_path = blast_path
        self.blast_num = blast_num
        self.name = name
        self.frequency = frequency


projectiles = []

fireball = ImageOfProj("src/tile_sets/tiles_for_chars/ranged_attack/fireball/move/sprite_", 3,
                       "src/tile_sets/tiles_for_chars/ranged_attack/fireball/blast/sprite_", 11, "fireball", 3)
projectiles.append(fireball)

flash = ImageOfProj("src/tile_sets/tiles_for_chars/ranged_attack/flash/move/sprite_", 3,
                    "src/tile_sets/tiles_for_chars/ranged_attack/flash/blast/flash_", 11, "flash", 3)
projectiles.append(flash)

blue_fire = ImageOfProj("src/tile_sets/tiles_for_chars/ranged_attack/blue_fire/move/sprite_", 3,
                        "src/tile_sets/tiles_for_chars/ranged_attack/blue_fire/blast/sprite_", 11, "blue_fire", 3)
projectiles.append(blue_fire)

purple_fire = ImageOfProj("src/tile_sets/tiles_for_chars/ranged_attack/purple_fire/move/sprite_", 3,
                          "src/tile_sets/tiles_for_chars/ranged_attack/purple_fire/blast/sprite_", 11, "purple_fire", 3)
projectiles.append(purple_fire)

blood = ImageOfProj("src/tile_sets/tiles_for_chars/ranged_attack/blood/move/sprite_", 3,
                    "src/tile_sets/tiles_for_chars/ranged_attack/blood/blast/sprite_", 11, "blood", 3)
projectiles.append(blood)

ice_ball = ImageOfProj("src/tile_sets/tiles_for_chars/ranged_attack/ice_ball/move/sprite_", 4,
                       "src/tile_sets/tiles_for_chars/ranged_attack/ice_ball/blast/sprite_", 6, "ice_ball", 4)
projectiles.append(ice_ball)
