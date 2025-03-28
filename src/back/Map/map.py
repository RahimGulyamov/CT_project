import pygame

from src.back.Map.map_generator import *
from src.back.Map.space import *
from src.back.constants_with_paths_to_files import *

random.seed(time.time())

list_with_up_walls = []
list_with_down_walls = []
list_with_left_walls = []
list_with_right_walls = []
list_with_floor = []

image_for_door = pygame.image.load(PATH_TO_DOOR_IMG)

image_for_empty = pygame.image.load(PATH_TO_EMPTY_IMG)

image_for_left_down_in_corner = pygame.image.load(PATH_TO_LEFT_DOWN_IN_CORNER)

image_for_left_down_out_corner = pygame.image.load(PATH_TO_LEFT_DOWN_OUT_CORNER)

image_for_right_down_in_corner = pygame.image.load(PATH_TO_RIGHT_DOWN_IN_CORNER)

image_for_right_down_out_corner = pygame.image.load(PATH_TO_RIGHT_DOWN_OUT_CORNER)

image_for_closed_door = pygame.image.load(PATH_TO_DEFINITELY_CLOSED_UP_DOOR)

generated_floor = {}


def SetImage(path, number):
    result = pygame.image.load(path + str(number) + EXTENSION_OF_IMG_FILES)
    return result


def ScaleImage(image, size_of_tile=SIZE_OF_TILE):
    image = pygame.transform.scale(image, (size_of_tile, size_of_tile))
    return image


def SetTiles():
    for i in range(1, NUM_OF_UP_WALLS + 1):
        list_with_up_walls.append(SetImage(PATH_TO_UP_WALLS, i))
    for i in range(1, NUM_OF_DOWN_WALLS + 1):
        list_with_down_walls.append(SetImage(PATH_TO_DOWN_WALLS, i))

    for i in range(1, NUM_OF_RIGHT_WALLS + 1):
        list_with_right_walls.append(SetImage(PATH_TO_RIGHT_WALLS, i))

    for i in range(1, NUM_OF_LEFT_WALLS + 1):
        list_with_left_walls.append(SetImage(PATH_TO_LEFT_WALLS, i))

    for i in range(1, NUM_OF_FLOORS + 1):
        list_with_floor.append(SetImage(PATH_TO_FLOORS, i))


class Map:
    SetTiles()

    def __init__(self, size_of_map):

        self.matrix_with_map = MapBuilder.GenerateMap(size_of_map)

        self.dfs = DFSAlgoForMapBuilder()

        self.spaces_as_dict = {}
        self.spaces = []

        self.SetSpaces()

    def GetMatrix(self):
        return self.matrix_with_map

    def GetStartRoom(self):
        result = None
        num_of_iterations = 0
        min_size = 1000000
        rooms = [space for space in self.spaces if isinstance(space, RoomSpace)]
        while num_of_iterations != 50:
            num_of_iterations += 1
            space = random.choice(rooms)
            if isinstance(space, RoomSpace):
                if space.GetSizeOfSpace() < min_size:
                    result = space
                    min_size = space.GetSizeOfSpace()
                if space.GetSizeOfSpace() <= MAX_SIZE_OF_START_ROOM:
                    return space
        return result

    def GetFinishRoom(self, start_room):
        result = None
        min_size = 1000000
        for space in self.spaces:
            if isinstance(space, RoomSpace):
                if min_size > space.GetSizeOfSpace() > 9 and space is not start_room:
                    result = space
                    min_size = space.GetSizeOfSpace()
        return result

    def SetSpaces(self):
        used = {}
        for i in range(len(self.matrix_with_map)):
            for j in range(len(self.matrix_with_map[i])):
                if (i, j) not in used and self.GetTile((i, j)) in [CHAR_FOR_FLOOR, CHAR_FOR_PATH]:
                    intermediate = []
                    keys = {}
                    room = None
                    if self.GetTile((i, j)) in [CHAR_FOR_PATH]:
                        self.dfs.DFSOnTheSpecificTiles(main_matrix=self.matrix_with_map, vertex=(i, j),
                                                       final_matrix=intermediate, tiles=[CHAR_FOR_PATH, CHAR_FOR_DOOR],
                                                       depth=DEPTH_OF_DFS_FOR_PATHS)
                        keys[(i, j)] = (i, j)
                        used[(i, j)] = (i, j)

                        room = PathSpace(intermediate, keys)
                        for key in keys:
                            self.spaces_as_dict[key] = room
                    elif self.GetTile((i, j)) in [CHAR_FOR_FLOOR]:
                        keys = [{}, {}]
                        self.dfs.DFSOnTheSpecificTiles(main_matrix=self.matrix_with_map, vertex=(i, j),
                                                       final_matrix=intermediate, tiles=SET_WITH_WALLS + [CHAR_FOR_DOOR,
                                                                                                          CHAR_FOR_FLOOR],
                                                       keys=keys, flag='room')
                        for tile in intermediate:
                            used[tile[0]] = tile[0]
                        room = RoomSpace(intermediate, keys[0], keys[1])
                        for key in keys[0]:
                            self.spaces_as_dict[key] = room
                    self.spaces.append(room)

    @staticmethod
    def BlitTileOnMap(surface, tile, position_for_blit, size_of_tile=SIZE_OF_TILE, left_upper_corner=(0, 0)):

        if tile[1] in [CHAR_FOR_PATH, CHAR_FOR_FLOOR]:
            if (tile[0][0] + left_upper_corner[0], tile[0][1] + left_upper_corner[1]) not in generated_floor:
                generated_floor[tile[0][0] + left_upper_corner[0], tile[0][1] + left_upper_corner[1]] = random.choice(
                    list_with_floor)

            surface.blit(
                ScaleImage(generated_floor[tile[0][0] + left_upper_corner[0], tile[0][1] + left_upper_corner[1]],
                           size_of_tile), position_for_blit)
        elif tile[1] == CHAR_FOR_DOOR:
            surface.blit(ScaleImage(image_for_door, size_of_tile), position_for_blit)
        elif tile[1] == CHAR_FOR_UP_WALL:
            surface.blit(ScaleImage(random.choice(list_with_up_walls), size_of_tile), position_for_blit)
        elif tile[1] == CHAR_FOR_DOWN_WALL:
            surface.blit(ScaleImage(random.choice(list_with_down_walls), size_of_tile), position_for_blit)
        elif tile[1] == CHAR_FOR_RIGHT_WALL:
            surface.blit(ScaleImage(random.choice(list_with_right_walls), size_of_tile), position_for_blit)
        elif tile[1] == CHAR_FOR_LEFT_WALL:
            surface.blit(ScaleImage(random.choice(list_with_left_walls), size_of_tile), position_for_blit)
        elif tile[1] == CHAR_FOR_LEFT_DOWN_IN_CORNER:
            surface.blit(ScaleImage(image_for_left_down_in_corner, size_of_tile), position_for_blit)
        elif tile[1] == CHAR_FOR_LEFT_DOWN_OUT_CORNER:
            surface.blit(ScaleImage(image_for_left_down_out_corner, size_of_tile), position_for_blit)
        elif tile[1] == CHAR_FOR_RIGHT_DOWN_IN_CORNER:
            surface.blit(ScaleImage(image_for_right_down_in_corner, size_of_tile), position_for_blit)
        elif tile[1] == CHAR_FOR_DOWN_OUT_CORNER:
            surface.blit(ScaleImage(image_for_right_down_out_corner, size_of_tile), position_for_blit)
        elif tile[1] == CHAR_FOR_CLOSED_DOOR:
            surface.blit(ScaleImage(image_for_closed_door, size_of_tile), position_for_blit)
        else:
            surface.blit(ScaleImage(image_for_empty, size_of_tile), position_for_blit)

    @staticmethod
    def SetSpecificTilesOnMatrix(matrix, list_of_tiles):
        """set tiles on matrix according to following list"""

        for tile in list_of_tiles:
            matrix[tile[0][0]][tile[0][1]] = tile[1]

    def SetSpecificTiles(self, list_of_tiles):
        for tile in list_of_tiles:
            self.matrix_with_map[tile[0][0]][tile[0][1]] = tile[1]

    @staticmethod
    def GetLeftUpperCornerForListOfTiles(list_with_tiles):
        left_upper_corner = (
            min(list_with_tiles, key=lambda item: item[0][0])[0][0],
            min(list_with_tiles, key=lambda item: item[0][1])[0][1])
        return left_upper_corner

    @staticmethod
    def GetRightDownCornerForListOfTiles(list_with_tiles):
        right_down_corner = (
            max(list_with_tiles, key=lambda item: item[0][0])[0][0],
            max(list_with_tiles, key=lambda item: item[0][1])[0][1])
        return right_down_corner

    @staticmethod
    def RedrawSurface(surface, list_with_tiles, left_upper_corner):
        interm_with_tiles = []
        for tile in list_with_tiles:
            interm_with_tiles.append(((tile[0][0] - left_upper_corner[0], tile[0][1] - left_upper_corner[1]), tile[1]))
        Map.BlitSpecificTilesOnSurface(surface, interm_with_tiles, left_upper_corner=left_upper_corner)
        return surface

    @staticmethod
    def GetSurface(list_with_tiles):
        left_upper_corner = Map.GetLeftUpperCornerForListOfTiles(list_with_tiles)
        right_down_corner = Map.GetRightDownCornerForListOfTiles(list_with_tiles)
        width = right_down_corner[0] - left_upper_corner[0] + 1
        height = right_down_corner[1] - left_upper_corner[1] + 1
        surface = pygame.Surface((width * SIZE_OF_TILE,
                                  height * SIZE_OF_TILE), flags=pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        interm_with_tiles = []
        for tile in list_with_tiles:
            interm_with_tiles.append(((tile[0][0] - left_upper_corner[0], tile[0][1] - left_upper_corner[1]), tile[1]))
        Map.BlitSpecificTilesOnSurface(surface, interm_with_tiles, left_upper_corner=left_upper_corner)
        return surface

    @staticmethod
    def BlitSpecificTilesOnSurface(surface, list_of_tiles, size_of_tile=SIZE_OF_TILE, left_upper_corner=(0, 0)):
        """blit tiles on map according to following list"""

        for tile in list_of_tiles:
            x_coord = size_of_tile * tile[0][0]
            y_coord = size_of_tile * tile[0][1]
            Map.BlitTileOnMap(surface=surface, tile=tile, position_for_blit=(x_coord, y_coord),
                              size_of_tile=size_of_tile, left_upper_corner=left_upper_corner)

    @staticmethod
    def BlitTilesOnMap(surface, matrix, left_corner, size_of_tile=SIZE_OF_TILE):
        x, y = 0, 0
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                Map.BlitTileOnMap(surface=surface,
                                  tile=((i + left_corner[0], j + left_corner[1]), matrix[i][j]),
                                  position_for_blit=(x, y),
                                  size_of_tile=size_of_tile)
                y += size_of_tile
            x += size_of_tile
            y = 0

    def GetTile(self, position):
        return self.matrix_with_map[position[0]][position[1]]

    @staticmethod
    def GetPositionOfTile(position):
        return position[0] // SIZE_OF_TILE, position[1] // SIZE_OF_TILE

    def CanStandThere(self, position):
        try:
            tile = self.GetTile(self.GetPositionOfTile(position))
        except:
            return False
        return tile in [CHAR_FOR_FLOOR, CHAR_FOR_DOOR, CHAR_FOR_PATH]

    def GetCurrentRoom(self, player_position, current_room):
        if self.GetTile(self.GetPositionOfTile(player_position)) in [CHAR_FOR_PATH]:
            if self.GetPositionOfTile(player_position) not in current_room.GetKeys():
                return self.spaces_as_dict[self.GetPositionOfTile(player_position)]
        else:
            if self.GetPositionOfTile(player_position) not in current_room.GetCoordinatesOfTiles():
                return self.spaces_as_dict[self.GetPositionOfTile(player_position)]

        return current_room
