import random
import time

from src.back.Map.constants_for_map import *

random.seed(time.time())


# random.seed(12)


class MapBuilder:
    basic_rooms = []
    columns = []

    @staticmethod
    def GenerateMap(size=(30, 20)):
        result = MapBuilder.GetClearMap(size)
        MapBuilder.SetBoardsOfMap(result)
        MapBuilder.GenerateColumns()
        MapBuilder.GenerateBasicRooms()
        MapBuilder.GenerateMapWithRooms(result)
        MapBuilder.AdditionalGeneration(result)
        MapBuilder.PostProcessing(result)
        return result

    @staticmethod
    def GetSideOfDoor(main_matrix, position):
        if main_matrix[position[0]][position[1]] in SET_WITH_DOORS:
            if main_matrix[position[0]][position[1] - 1] is CHAR_FOR_PATH:
                return 'D'
            elif main_matrix[position[0]][position[1] + 1] is CHAR_FOR_PATH:
                return 'U'
            elif main_matrix[position[0] - 1][position[1]] is CHAR_FOR_PATH:
                return 'R'
            elif main_matrix[position[0] + 1][position[1]] is CHAR_FOR_PATH:
                return 'L'

    @staticmethod
    def IsItWallForDoor(main_matrix, position: tuple):
        if MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_UP_WALL]:
            if MapBuilder.GetTile(main_matrix, (position[0], position[1] + 1)) in [CHAR_FOR_UP_WALL,
                                                                                   CHAR_FOR_DOOR] and MapBuilder.GetTile(
                main_matrix,
                (position[0], position[1] - 1)) in [CHAR_FOR_UP_WALL, CHAR_FOR_DOOR]:
                if MapBuilder.GetTile(main_matrix, (position[0] - 1, position[1])) in [
                    CHAR_FOR_EMPTY] and MapBuilder.GetTile(main_matrix,
                                                           (position[0] + 1, position[1])) in [CHAR_FOR_FLOOR]:
                    return True
                if MapBuilder.GetTile(main_matrix, (position[0] - 1, position[1])) in [
                    CHAR_FOR_FLOOR] and MapBuilder.GetTile(main_matrix,
                                                           (position[0] + 1, position[1])) in [CHAR_FOR_EMPTY]:
                    return True
            if MapBuilder.GetTile(main_matrix, (position[0] + 1, position[1])) in [CHAR_FOR_UP_WALL,
                                                                                   CHAR_FOR_DOOR] and MapBuilder.GetTile(
                main_matrix,
                (position[0] - 1, position[1])) in [CHAR_FOR_UP_WALL, CHAR_FOR_DOOR]:
                if MapBuilder.GetTile(main_matrix, (position[0], position[1] - 1)) in [
                    CHAR_FOR_EMPTY] and MapBuilder.GetTile(main_matrix,
                                                           (position[0], position[1] + 1)) in [CHAR_FOR_FLOOR]:
                    return True
                if MapBuilder.GetTile(main_matrix, (position[0], position[1] - 1)) in [
                    CHAR_FOR_FLOOR] and MapBuilder.GetTile(main_matrix,
                                                           (position[0], position[1] + 1)) in [CHAR_FOR_EMPTY]:
                    return True
        return False

    @staticmethod
    def IsThereCorner(main_matrix, position: tuple):
        if MapBuilder.IsThereAnyTile(main_matrix, position, [CHAR_FOR_EMPTY]):
            if MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (
                    position[0] - 1, position[1])) in [
                CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (position[0], position[1] + 1)) in [
                CHAR_FOR_UP_WALL]:
                return True
            if MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (
                    position[0] - 1, position[1])) in [
                CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (position[0], position[1] - 1)) in [
                CHAR_FOR_UP_WALL]:
                return True
            if MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (
                    position[0] + 1, position[1])) in [
                CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (position[0], position[1] + 1)) in [
                CHAR_FOR_UP_WALL]:
                return True
            if MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (
                    position[0] + 1, position[1])) in [
                CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (position[0], position[1] - 1)) in [
                CHAR_FOR_UP_WALL]:
                return True
        return False

    @staticmethod
    def IsThereCutCorner(main_matrix, position: tuple):
        if MapBuilder.IsThereAnyTile(main_matrix, position, [CHAR_FOR_EMPTY]):
            if MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_FLOOR] and MapBuilder.GetTile(main_matrix, (
                    position[0] - 1, position[1])) in [
                CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (position[0], position[1] + 1)) in [
                CHAR_FOR_UP_WALL]:
                return True
            if MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_FLOOR] and MapBuilder.GetTile(main_matrix, (
                    position[0] - 1, position[1])) in [
                CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (position[0], position[1] - 1)) in [
                CHAR_FOR_UP_WALL]:
                return True
            if MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_FLOOR] and MapBuilder.GetTile(main_matrix, (
                    position[0] + 1, position[1])) in [
                CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (position[0], position[1] + 1)) in [
                CHAR_FOR_UP_WALL]:
                return True
            if MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_FLOOR] and MapBuilder.GetTile(main_matrix, (
                    position[0] + 1, position[1])) in [
                CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (position[0], position[1] - 1)) in [
                CHAR_FOR_UP_WALL]:
                return True
        return False

    @staticmethod
    def IsThereCutCornerAfterCreate(main_matrix, position: tuple):
        if MapBuilder.IsThereAnyTile(main_matrix, position, [CHAR_FOR_FLOOR]):
            if MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_EMPTY] and MapBuilder.GetTile(main_matrix, (
                    position[0] - 1, position[1])) in [
                CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (position[0], position[1] + 1)) in [
                CHAR_FOR_UP_WALL]:
                return True
            if MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_EMPTY] and MapBuilder.GetTile(main_matrix, (
                    position[0] - 1, position[1])) in [
                CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (position[0], position[1] - 1)) in [
                CHAR_FOR_UP_WALL]:
                return True
            if MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_EMPTY] and MapBuilder.GetTile(main_matrix, (
                    position[0] + 1, position[1])) in [
                CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (position[0], position[1] + 1)) in [
                CHAR_FOR_UP_WALL]:
                return True
            if MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_EMPTY] and MapBuilder.GetTile(main_matrix, (
                    position[0] + 1, position[1])) in [
                CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (position[0], position[1] - 1)) in [
                CHAR_FOR_UP_WALL]:
                return True
        return False

    @staticmethod
    def GetTile(main_matrix, position: tuple):
        return main_matrix[position[0]][position[1]]

    @staticmethod
    def GetNeighbours(main_matrix, position: tuple):
        result = []
        if position[0] > 0:
            result.append((position[0] - 1, position[1]))
        if position[0] < len(main_matrix) - 1:
            result.append((position[0] + 1, position[1]))
        if position[1] > 0:
            result.append((position[0], position[1] - 1))
        if position[1] < len(main_matrix[0]) - 1:
            result.append((position[0], position[1] + 1))
        return result

    @staticmethod
    def GetAround(main_matrix, position: tuple):
        result = []
        interm = []

        if position[0] > 0 and position[1] > 0:
            interm.append((position[0] - 1, position[1] - 1))
        else:
            interm.append((-1, -1))
        if position[0] > 0:
            interm.append((position[0] - 1, position[1]))
        else:
            interm.append((-1, -1))
        if position[0] > 0 and position[1] < len(main_matrix[0]) - 1:
            interm.append((position[0] - 1, position[1] + 1))
        else:
            interm.append((-1, -1))
        result.append(interm.copy())

        interm.clear()

        if position[1] > 0:
            interm.append((position[0], position[1] - 1))
        else:
            interm.append((-1, -1))
        interm.append((position[0], position[1]))
        if position[1] < len(main_matrix[0]) - 1:
            interm.append((position[0], position[1] + 1))
        else:
            interm.append((-1, -1))
        result.append(interm.copy())

        interm.clear()

        if position[0] < len(main_matrix) - 1 and position[1] > 0:
            interm.append((position[0] + 1, position[1] - 1))
        else:
            interm.append((-1, -1))
        if position[0] < len(main_matrix) - 1:
            interm.append((position[0] + 1, position[1]))
        else:
            interm.append((-1, -1))
        if position[0] < len(main_matrix) - 1 and position[1] < len(main_matrix[0]) - 1:
            interm.append((position[0] + 1, position[1] + 1))
        else:
            interm.append((-1, -1))
        result.append(interm.copy())

        interm.clear()

        return result

    @staticmethod
    def GetLeftAround(main_matrix, position):
        around = MapBuilder.GetAround(main_matrix, position).copy()
        around.pop()
        return around

    @staticmethod
    def GetUpAround(main_matrix, position):
        around = MapBuilder.GetAround(main_matrix, position)
        res = []
        for i in range(len(around)):
            interm = []
            for j in range(len(around[0]) - 1):
                interm.append(around[i][j])
            res.append(interm)
        return res

    @staticmethod
    def GetRightAround(main_matrix, position):
        around = MapBuilder.GetAround(main_matrix, position)
        res = []
        for i in range(1, len(around)):
            res.append(around[i])
        return res

    @staticmethod
    def GetDownAround(main_matrix, position):
        around = MapBuilder.GetAround(main_matrix, position)
        res = []
        for i in range(len(around)):
            interm = []
            for j in range(1, len(around[0])):
                interm.append(around[i][j])
            res.append(interm)
        return res

    @staticmethod
    def GetAroundForDFS(main_matrix, position, parent):
        if position[0] > parent[0]:
            return MapBuilder.GetLeftAround(main_matrix, parent)
        if position[0] < parent[0]:
            return MapBuilder.GetRightAround(main_matrix, parent)
        if position[1] > parent[1]:
            return MapBuilder.GetUpAround(main_matrix, parent)
        if position[1] < parent[1]:
            return MapBuilder.GetDownAround(main_matrix, parent)

    @staticmethod
    def GetAroundForDeadEnds(main_matrix, position, parent):
        if position[0] > parent[0]:
            return MapBuilder.GetRightAround(main_matrix, position)
        if position[0] < parent[0]:
            return MapBuilder.GetLeftAround(main_matrix, position)
        if position[1] > parent[1]:
            return MapBuilder.GetDownAround(main_matrix, position)
        if position[1] < parent[1]:
            return MapBuilder.GetUpAround(main_matrix, position)

    @staticmethod
    def NumOfTiles(main_matrix, list_of_tiles, position):
        res = 0
        for i in list_of_tiles:
            for j in i:
                if j not in [(-1, -1), position]:
                    if MapBuilder.GetTile(main_matrix, j) not in [CHAR_FOR_EMPTY, CHAR_FOR_MAP_BOARD]:
                        res += 1
        return res

    @staticmethod
    def IsThereDeadEnd(main_matrix, position, parent_position):
        if MapBuilder.NumOfTiles(main_matrix, MapBuilder.GetAroundForDeadEnds(main_matrix, position, parent_position),
                                 position) == 0:
            return True
        return False

    @staticmethod
    def GetClearMap(size):
        result = []
        for i in range(size[0]):
            interm = []
            for j in range(size[1]):
                interm.append(CHAR_FOR_EMPTY)
            result.append(interm)
        return result

    @staticmethod
    def GenerateBasicRooms():
        for i in range(NUM_OF_GENERATED_BASIC_ROOMS):
            interm = []
            x_coord = random.randrange(
                MIN_WIDTH_OF_BASIC_ROOM, MAX_WIDTH_OF_BASIC_ROOM)
            y_coord = random.randrange(
                MIN_WIDTH_OF_BASIC_ROOM, MAX_WIDTH_OF_BASIC_ROOM)
            right_down_corner = (x_coord, y_coord)
            for i in range(right_down_corner[0]):
                interm_array = []
                for j in range(right_down_corner[1]):
                    interm_array.append(CHAR_FOR_FLOOR)
                interm.append(interm_array)
            MapBuilder.basic_rooms.append(interm)

    @staticmethod
    def GenerateColumns():
        for i in range(NUM_OF_GENERATED_COLUMNS):
            interm = []
            x_coord = random.randrange(
                MIN_WIDTH_OF_COLUMN, MAX_WIDTH_OF_COLUMN)
            y_coord = random.randrange(
                MIN_WIDTH_OF_COLUMN, MAX_WIDTH_OF_COLUMN)
            right_down_corner = (x_coord, y_coord)
            for i in range(right_down_corner[0]):
                interm_array = []
                for j in range(right_down_corner[1]):
                    interm_array.append(CHAR_FOR_EMPTY)
                interm.append(interm_array)
            MapBuilder.columns.append(interm)

    @staticmethod
    def GetSizeRoom(basic_room):
        width = len(basic_room)
        height = len(basic_room[0])
        return width, height

    @staticmethod
    def IsThereIntersec(main_matrix, room, pos_of_room: tuple, list_of_tiles=[CHAR_FOR_EMPTY]) -> bool:
        size_of_room = MapBuilder.GetSizeRoom(room)
        bounds_for_loop = []
        if pos_of_room[0] > 1:
            bounds_for_loop.append(-2)
        else:
            bounds_for_loop.append(-1)

        if pos_of_room[0] + size_of_room[0] < len(main_matrix) - 1:
            bounds_for_loop.append(size_of_room[0] + 2)
        else:
            bounds_for_loop.append(size_of_room[0] + 1)

        if pos_of_room[1] > 1:
            bounds_for_loop.append(-2)
        else:
            bounds_for_loop.append(-1)

        if pos_of_room[1] + size_of_room[1] < len(main_matrix[0]) - 1:
            bounds_for_loop.append(size_of_room[1] + 2)
        else:
            bounds_for_loop.append(size_of_room[1] + 1)

        for i in range(bounds_for_loop[0], bounds_for_loop[1]):
            for j in range(bounds_for_loop[2], bounds_for_loop[3]):
                if main_matrix[pos_of_room[0] + i][pos_of_room[1] + j] not in list_of_tiles:
                    return True
        return False

    @staticmethod
    def GenerateMapWithRooms(main_matrix):
        num_of_generated_rooms = 0
        num_of_generations = 0
        while num_of_generated_rooms != NUM_OF_BASIC_ROOMS_ON_MAP:

            if num_of_generations == 1000:
                break
            num_of_generations += 1

            num_of_basic_room = random.randrange(0, NUM_OF_GENERATED_BASIC_ROOMS)
            basic_room = MapBuilder.basic_rooms[num_of_basic_room]
            width_of_basic_room, height_of_basic_room = MapBuilder.GetSizeRoom(basic_room)
            x_coord = random.randrange(2, len(main_matrix) - width_of_basic_room - 1)
            y_coord = random.randrange(2, len(main_matrix[0]) - height_of_basic_room - 1)
            left_corner_position = (x_coord, y_coord)
            sign = False
            counter = 0
            while sign is not True:
                if counter == 50:
                    break

                counter += 1
                if not MapBuilder.IsThereIntersec(main_matrix, basic_room, left_corner_position):
                    sign = True
                    num_of_generated_rooms += 1
                    for i in range(-1, width_of_basic_room + 1):
                        for j in range(-1, height_of_basic_room + 1):
                            if i == -1 or i == width_of_basic_room or j == -1 or j == height_of_basic_room:
                                main_matrix[left_corner_position[0] +
                                            i][left_corner_position[1] + j] = CHAR_FOR_UP_WALL
                            else:
                                main_matrix[left_corner_position[0] +
                                            i][left_corner_position[1] + j] = CHAR_FOR_FLOOR

    @staticmethod
    def GenerateMapWithColumns(main_matrix):
        num_of_generated_rooms = 0
        num_of_generations = 0
        while num_of_generated_rooms != NUM_OF_COLUMNS_ON_MAP:
            if num_of_generations == 1000:
                break
            num_of_generations += 1

            num_of_column = random.randrange(0, NUM_OF_COLUMNS_ON_MAP)
            column = MapBuilder.columns[num_of_column]
            width_of_column = MapBuilder.GetSizeRoom(column)[0] + 2
            height_of_column = MapBuilder.GetSizeRoom(column)[1] + 2
            x_coord = random.randrange(2, len(main_matrix) - width_of_column - 2)
            y_coord = random.randrange(2, len(main_matrix[0]) - height_of_column - 2)
            left_corner_position = (x_coord - 2, y_coord - 2)
            sign = False
            counter = 0
            while sign is not True:
                if counter == 50:
                    break

                counter += 1
                if not MapBuilder.IsThereIntersec(main_matrix, column, left_corner_position,
                                                  list_of_tiles=[CHAR_FOR_FLOOR]):
                    width_of_column -= 2
                    height_of_column -= 2
                    x_coord += 2
                    y_coord += 2
                    sign = True
                    num_of_generated_rooms += 1
                    for i in range(-1, width_of_column + 1):
                        for j in range(-1, height_of_column + 1):
                            if i == -1 or i == width_of_column or j == -1 or j == height_of_column:
                                main_matrix[left_corner_position[0] +
                                            i][left_corner_position[1] + j] = CHAR_FOR_UP_WALL
                            else:
                                main_matrix[left_corner_position[0] +
                                            i][left_corner_position[1] + j] = CHAR_FOR_COLUMN

    @staticmethod
    def IsInCrossAnyTile(main_matrix, position, tiles) -> bool:
        if position[0] > 0:
            if main_matrix[position[0] - 1][position[1]] in tiles:
                return True
        if position[0] < len(main_matrix) - 1:
            if main_matrix[position[0] + 1][position[1]] in tiles:
                return True
        if position[1] > 0:
            if main_matrix[position[0]][position[1] - 1] in tiles:
                return True
        if position[1] < len(main_matrix) - 1:
            if main_matrix[position[0]][position[1] + 1] in tiles:
                return True
        if position[0] == 0 or position[0] == len(main_matrix) - 1 or position[1] == 0 or position[1] == len(
                main_matrix[0]) - 1:
            return True
        return False

    @staticmethod
    def IsThereAnyTile(main_matrix, position, tiles) -> bool:
        if main_matrix[position[0] - 1][position[1]] in tiles:
            return True
        if main_matrix[position[0] + 1][position[1]] in tiles:
            return True
        if main_matrix[position[0]][position[1] - 1] in tiles:
            return True
        if main_matrix[position[0]][position[1] + 1] in tiles:
            return True
        if main_matrix[position[0] - 1][position[1] + 1] in tiles:
            return True
        if main_matrix[position[0] - 1][position[1] - 1] in tiles:
            return True
        if main_matrix[position[0] + 1][position[1] + 1] in tiles:
            return True
        if main_matrix[position[0] + 1][position[1] - 1] in tiles:
            return True
        return False

    @staticmethod
    def AdditionalGeneration(main_matrix):
        num_of_generated = 0
        while num_of_generated != NUM_OF_ADDITION_ROOMS_ON_MAP:
            num_of_generated += 1
            num_of_basic_room = random.randrange(0, NUM_OF_GENERATED_BASIC_ROOMS)
            basic_room = MapBuilder.basic_rooms[num_of_basic_room]
            width_of_basic_room = MapBuilder.GetSizeRoom(basic_room)[0]
            height_of_basic_room = MapBuilder.GetSizeRoom(basic_room)[1]
            x_coord = random.randrange(2, len(main_matrix) - width_of_basic_room - 1)
            y_coord = random.randrange(2, len(main_matrix[0]) - height_of_basic_room - 1)
            left_corner_position = (x_coord, y_coord)

            for i in range(-1, width_of_basic_room + 1):
                for j in range(-1, height_of_basic_room + 1):
                    if i == -1 or i == width_of_basic_room or j == -1 or j == height_of_basic_room:
                        if main_matrix[left_corner_position[0] +
                                       i][left_corner_position[1] + j] == CHAR_FOR_EMPTY:
                            main_matrix[left_corner_position[0] +
                                        i][left_corner_position[1] + j] = CHAR_FOR_UP_WALL
                        elif main_matrix[left_corner_position[0] +
                                         i][
                            left_corner_position[1] + j] == CHAR_FOR_UP_WALL and not MapBuilder.IsInCrossAnyTile(
                            main_matrix, (left_corner_position[0] + i, left_corner_position[1] + j),
                            [CHAR_FOR_EMPTY, CHAR_FOR_MAP_BOARD]):
                            main_matrix[left_corner_position[0] +
                                        i][left_corner_position[1] + j] = CHAR_FOR_FLOOR
                    else:
                        main_matrix[left_corner_position[0] +
                                    i][left_corner_position[1] + j] = CHAR_FOR_FLOOR

    @staticmethod
    def IsThereAllFloors(main_matrix, position):
        counter = 0
        if position[0] > 0:
            if main_matrix[position[0] - 1][position[1]] in [CHAR_FOR_FLOOR, CHAR_FOR_UP_WALL]:
                counter += 1

        if position[0] < len(main_matrix[0]) - 1:
            if main_matrix[position[0] + 1][position[1]] in [CHAR_FOR_FLOOR, CHAR_FOR_UP_WALL]:
                counter += 1

        if position[1] > 0:
            if main_matrix[position[0]][position[1] - 1] in [CHAR_FOR_FLOOR, CHAR_FOR_UP_WALL]:
                counter += 1

        if position[1] < len(main_matrix) - 1:
            if main_matrix[position[0]][position[1] + 1] in [CHAR_FOR_FLOOR, CHAR_FOR_UP_WALL]:
                counter += 1

        if counter > 2:
            return True
        return False

    @staticmethod
    def DeleteWallsOnDiagonal(main_matrix):
        for i in range(len(main_matrix) - 1):
            for j in range(len(main_matrix[0]) - 1):
                if main_matrix[i][j] == CHAR_FOR_UP_WALL and main_matrix[i + 1][j] == CHAR_FOR_FLOOR and \
                        main_matrix[i][
                            j + 1] == CHAR_FOR_FLOOR and main_matrix[i + 1][j + 1] == CHAR_FOR_UP_WALL:
                    main_matrix[i + 1][j] = CHAR_FOR_UP_WALL
                    main_matrix[i][j + 1] = CHAR_FOR_UP_WALL
                elif main_matrix[i][j] == CHAR_FOR_FLOOR and main_matrix[i + 1][j] == CHAR_FOR_UP_WALL and \
                        main_matrix[i][
                            j + 1] == CHAR_FOR_UP_WALL and main_matrix[i + 1][j + 1] == CHAR_FOR_FLOOR:
                    main_matrix[i][j] = CHAR_FOR_UP_WALL
                    main_matrix[i + 1][j + 1] = CHAR_FOR_UP_WALL

    @staticmethod
    def DeleteWallsInsideRooms(main_matrix):
        for i in range(len(main_matrix)):
            for j in range(len(main_matrix[0])):
                if main_matrix[i][j] == CHAR_FOR_UP_WALL:
                    if MapBuilder.IsThereAllFloors(main_matrix, (i, j)) and not MapBuilder.IsInCrossAnyTile(
                            main_matrix, (i, j), [CHAR_FOR_EMPTY, CHAR_FOR_MAP_BOARD]):
                        main_matrix[i][j] = CHAR_FOR_FLOOR

    @staticmethod
    def IsThereDoorBetweenRooms(main_matrix, position: tuple):
        if (MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_EMPTY] and MapBuilder.GetTile(main_matrix, (
                position[0] - 1, position[1])) in [
                CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (position[0] + 1, position[1])) in [
                CHAR_FOR_UP_WALL]) or (
                MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_EMPTY] and MapBuilder.GetTile(main_matrix, (
                position[0], position[1] - 1)) in [
                    CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (position[0], position[1] + 1)) in [
                    CHAR_FOR_UP_WALL]):
            if MapBuilder.GetTile(main_matrix, (position[0] - 1, position[1] + 1)) in [
                CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix,
                                                         (position[0] - 1, position[1] - 1)) in [CHAR_FOR_UP_WALL]:
                if MapBuilder.GetTile(main_matrix, (position[0] + 1, position[1] + 1)) in [
                    CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix,
                                                             (position[0] + 1, position[1] - 1)) in [CHAR_FOR_UP_WALL]:
                    return True
        return False

    @staticmethod
    def PostProcessing(main_matrix):
        MapBuilder.DeleteWallsInsideRooms(main_matrix)
        MapBuilder.DeleteWallsOnDiagonal(main_matrix)
        MapBuilder.DeleteQuaterWalls(main_matrix)
        MapBuilder.SetPathsOnMap(main_matrix)
        MapBuilder.GenerateMapWithColumns(main_matrix)
        MapBuilder.SetDoors(main_matrix)
        MapBuilder.DeleteCutCorners(main_matrix)
        MapBuilder.SetDoorsBetweenRooms(main_matrix)
        MapBuilder.DeleteDoubleDoors(main_matrix)
        MapBuilder.SetFloorInFrontOfDoor(main_matrix)
        MapBuilder.DeleteDeadEnds(main_matrix)
        MapBuilder.DeleteFakeDoors(main_matrix)
        list_of_corners = []
        MapBuilder.MakeCutCorners(main_matrix, list_of_corners)
        MapBuilder.DeleteNotConnectedComponents(main_matrix)
        MapBuilder.DeleteCutCornersAfterCreate(main_matrix, list_of_corners)
        MapBuilder.DeleteWrongWall(main_matrix)
        MapBuilder.DeleteCutCorners(main_matrix)
        MapBuilder.ParseWalls(main_matrix)
        MapBuilder.ParseCorners(main_matrix)

    @staticmethod
    def DeleteQuaterWalls(main_matrix):
        for i in range(2, len(main_matrix) - 3):
            for j in range(2, len(main_matrix[0]) - 3):
                MapBuilder.SupportDeleteQuater(main_matrix, (i, j))

    @staticmethod
    def SupportDeleteQuater(main_matrix, position):
        counter_for_walls = 0
        counter_for_floors = 0
        counter_for_empty = 0
        for i in range(3):
            for j in range(3):
                if main_matrix[position[0] + i][position[1] + j] in [CHAR_FOR_FLOOR]:
                    counter_for_floors += 1
                elif main_matrix[position[0] + i][position[1] + j] in [CHAR_FOR_UP_WALL]:
                    counter_for_walls += 1
                elif main_matrix[position[0] + i][position[1] + j] in [CHAR_FOR_EMPTY]:
                    counter_for_empty += 1
        if counter_for_walls >= 5 and counter_for_floors >= 1 and counter_for_empty >= 1:
            for i in range(3):
                for j in range(3):
                    main_matrix[position[0] + i][position[1] + j] = CHAR_FOR_EMPTY
            for i in range(3):
                for j in range(3):
                    if MapBuilder.GetTile(main_matrix, (position[0] + i, position[1] + j)) in [CHAR_FOR_EMPTY]:
                        if MapBuilder.IsThereAnyTile(main_matrix, (position[0] + i, position[1] + j),
                                                     tiles=[CHAR_FOR_FLOOR]):
                            main_matrix[position[0] + i][position[1] + j] = CHAR_FOR_UP_WALL

    @staticmethod
    def SetDoors(main_matrix):
        dfs = DFSAlgoForMapBuilder()
        for i in range(1, len(main_matrix) - 2):
            for j in range(1, len(main_matrix[0]) - 2):
                if MapBuilder.GetTile(main_matrix, (i, j)) in [CHAR_FOR_POTENTIAL_DOOR]:
                    dfs.DFSForSetDoors(main_matrix, (i, j))
        for i in range(1, len(main_matrix) - 2):
            for j in range(1, len(main_matrix[0]) - 2):
                if MapBuilder.GetTile(main_matrix, (i, j)) in [CHAR_FOR_POTENTIAL_DOOR]:
                    main_matrix[i][j] = CHAR_FOR_UP_WALL

    @staticmethod
    def IsItRightWall(main_matrix, position):
        return MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (
            position[0] - 1, position[1])) in [
            CHAR_FOR_FLOOR] and MapBuilder.GetTile(main_matrix, (position[0] + 1, position[1])) in [CHAR_FOR_EMPTY,
                                                                                                    CHAR_FOR_COLUMN,
                                                                                                    CHAR_FOR_MAP_BOARD]

    @staticmethod
    def IsItLeftWall(main_matrix, position):
        return MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (
            position[0] - 1, position[1])) in [
            CHAR_FOR_EMPTY,
            CHAR_FOR_COLUMN,
            CHAR_FOR_MAP_BOARD] and MapBuilder.GetTile(main_matrix, (position[0] + 1, position[1])) in [CHAR_FOR_FLOOR]

    @staticmethod
    def IsItDownWall(main_matrix, position):
        return MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (
            position[0], position[1] - 1)) in [
            CHAR_FOR_FLOOR] and MapBuilder.GetTile(main_matrix, (position[0], position[1] + 1)) in [CHAR_FOR_EMPTY,
                                                                                                    CHAR_FOR_COLUMN,
                                                                                                    CHAR_FOR_MAP_BOARD]

    @staticmethod
    def IsItUpWall(main_matrix, position):
        return MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_UP_WALL] and MapBuilder.GetTile(main_matrix, (
            position[0], position[1] - 1)) in [
            CHAR_FOR_EMPTY,
            CHAR_FOR_COLUMN,
            CHAR_FOR_MAP_BOARD] and \
            MapBuilder.GetTile(main_matrix,
                               (position[0], position[1] + 1)) in [CHAR_FOR_FLOOR]

    @staticmethod
    def ParseWalls(main_matrix):
        for i in range(1, len(main_matrix) - 2):
            for j in range(1, len(main_matrix[0]) - 2):
                if MapBuilder.IsItRightWall(main_matrix, (i, j)):
                    main_matrix[i][j] = CHAR_FOR_RIGHT_WALL
                elif MapBuilder.IsItDownWall(main_matrix, (i, j)):
                    main_matrix[i][j] = CHAR_FOR_DOWN_WALL
                elif MapBuilder.IsItUpWall(main_matrix, (i, j)):
                    main_matrix[i][j] = CHAR_FOR_UP_WALL
                elif MapBuilder.IsItLeftWall(main_matrix, (i, j)):
                    main_matrix[i][j] = CHAR_FOR_LEFT_WALL

    @staticmethod
    def IsItLeftDownOutCorner(main_matrix, position):
        return MapBuilder.GetTile(main_matrix, position) in SET_WITH_WALLS and MapBuilder.GetTile(main_matrix,
                                                                                                  (position[0],
                                                                                                   position[
                                                                                                       1] - 1)) in SET_WITH_WALLS \
            and MapBuilder.GetTile(main_matrix,
                                   (position[0] + 1, position[1])) in SET_WITH_WALLS and MapBuilder.GetTile(main_matrix,
                                                                                                            (position[
                                                                                                                 0] + 1,
                                                                                                             position[
                                                                                                                 1] - 1)) in [
                CHAR_FOR_FLOOR]

    @staticmethod
    def IsItLeftDownInCorner(main_matrix, position):
        return MapBuilder.GetTile(main_matrix, position) in SET_WITH_WALLS and MapBuilder.GetTile(main_matrix,
                                                                                                  (position[0],
                                                                                                   position[
                                                                                                       1] + 1)) in SET_WITH_WALLS \
            and MapBuilder.GetTile(main_matrix,
                                   (position[0] - 1, position[1])) in SET_WITH_WALLS and MapBuilder.GetTile(main_matrix,
                                                                                                            (position[
                                                                                                                 0] - 1,
                                                                                                             position[
                                                                                                                 1] + 1)) in [
                CHAR_FOR_EMPTY, CHAR_FOR_COLUMN]

    @staticmethod
    def IsItRightDownOutCorner(main_matrix, position):
        return MapBuilder.GetTile(main_matrix, position) in SET_WITH_WALLS and MapBuilder.GetTile(main_matrix,
                                                                                                  (position[0],
                                                                                                   position[
                                                                                                       1] - 1)) in SET_WITH_WALLS \
            and MapBuilder.GetTile(main_matrix,
                                   (position[0] - 1, position[1])) in SET_WITH_WALLS and MapBuilder.GetTile(main_matrix,
                                                                                                            (position[
                                                                                                                 0] - 1,
                                                                                                             position[
                                                                                                                 1] - 1)) in [
                CHAR_FOR_FLOOR]

    @staticmethod
    def IsItRightDownInCorner(main_matrix, position):
        return MapBuilder.GetTile(main_matrix, position) in SET_WITH_WALLS and MapBuilder.GetTile(main_matrix,
                                                                                                  (position[0],
                                                                                                   position[
                                                                                                       1] + 1)) in SET_WITH_WALLS \
            and MapBuilder.GetTile(main_matrix,
                                   (position[0] + 1, position[1])) in SET_WITH_WALLS and MapBuilder.GetTile(main_matrix,
                                                                                                            (position[
                                                                                                                 0] + 1,
                                                                                                             position[
                                                                                                                 1] + 1)) in [
                CHAR_FOR_EMPTY, CHAR_FOR_COLUMN]

    @staticmethod
    def IsItLeftUpCorner(main_matrix, position):
        return MapBuilder.GetTile(main_matrix, position) in SET_WITH_WALLS and MapBuilder.GetTile(main_matrix,
                                                                                                  (position[0],
                                                                                                   position[
                                                                                                       1] + 1)) in SET_WITH_WALLS \
            and MapBuilder.GetTile(main_matrix,
                                   (position[0] + 1, position[1])) in SET_WITH_WALLS and MapBuilder.GetTile(main_matrix,
                                                                                                            (position[
                                                                                                                 0] + 1,
                                                                                                             position[
                                                                                                                 1] + 1)) in [
                CHAR_FOR_FLOOR]

    @staticmethod
    def IsItRightUpCorner(main_matrix, position):
        return MapBuilder.GetTile(main_matrix, position) in SET_WITH_WALLS and MapBuilder.GetTile(main_matrix, (
            position[0], position[1] + 1)) in SET_WITH_WALLS and MapBuilder.GetTile(main_matrix, (
            position[0] - 1, position[1])) in SET_WITH_WALLS and MapBuilder.GetTile(main_matrix,
                                                                                    (position[0] - 1,
                                                                                     position[1] + 1)) in [
            CHAR_FOR_FLOOR]

    @staticmethod
    def ParseCorners(main_matrix):
        for i in range(1, len(main_matrix) - 2):
            for j in range(1, len(main_matrix[0]) - 2):
                if MapBuilder.IsItLeftDownInCorner(main_matrix, (i, j)):
                    main_matrix[i][j] = CHAR_FOR_LEFT_DOWN_IN_CORNER
                elif MapBuilder.IsItLeftDownOutCorner(main_matrix, (i, j)):
                    main_matrix[i][j] = CHAR_FOR_LEFT_DOWN_OUT_CORNER
                elif MapBuilder.IsItRightDownInCorner(main_matrix, (i, j)):
                    main_matrix[i][j] = CHAR_FOR_RIGHT_DOWN_IN_CORNER
                elif MapBuilder.IsItRightDownOutCorner(main_matrix, (i, j)):
                    main_matrix[i][j] = CHAR_FOR_DOWN_OUT_CORNER
                elif MapBuilder.IsItRightUpCorner(main_matrix, (i, j)):
                    main_matrix[i][j] = CHAR_FOR_RIGHT_WALL
                elif MapBuilder.IsItLeftUpCorner(main_matrix, (i, j)):
                    main_matrix[i][j] = CHAR_FOR_LEFT_WALL

    @staticmethod
    def CountEmptyTiles(main_matrix, position):
        list = MapBuilder.GetAround(main_matrix, position)
        res = 0
        for i in list:
            for j in i:
                if MapBuilder.GetTile(main_matrix, (j[0], j[1])) in [CHAR_FOR_EMPTY, CHAR_FOR_MAP_BOARD]:
                    res += 1
        return res

    @staticmethod
    def IsThereWrongWall(main_matrix, position):
        if MapBuilder.GetTile(main_matrix, position) in [CHAR_FOR_UP_WALL] and MapBuilder.CountEmptyTiles(main_matrix,
                                                                                                          position) > 5:
            return True
        return False

    @staticmethod
    def DeleteWrongWall(main_matrix):
        for i in range(1, len(main_matrix) - 2):
            for j in range(1, len(main_matrix[0]) - 2):
                if MapBuilder.IsThereWrongWall(main_matrix, (i, j)):
                    main_matrix[i][j] = CHAR_FOR_EMPTY

    @staticmethod
    def IsThereFakeDoor(main_matrix, position):
        if MapBuilder.GetTile(main_matrix, (position[0] - 1, position[1])) in [CHAR_FOR_PATH]:
            if MapBuilder.GetTile(main_matrix, (position[0] - 2, position[1])) in [CHAR_FOR_EMPTY, CHAR_FOR_MAP_BOARD]:
                return position[0] - 1, position[1]
        if MapBuilder.GetTile(main_matrix, (position[0] + 1, position[1])) in [CHAR_FOR_PATH]:
            if MapBuilder.GetTile(main_matrix, (position[0] + 2, position[1])) in [CHAR_FOR_EMPTY, CHAR_FOR_MAP_BOARD]:
                return position[0] + 1, position[1]
        if MapBuilder.GetTile(main_matrix, (position[0], position[1] + 1)) in [CHAR_FOR_PATH]:
            if MapBuilder.GetTile(main_matrix, (position[0], position[1] + 2)) in [CHAR_FOR_EMPTY, CHAR_FOR_MAP_BOARD]:
                return position[0], position[1] + 1
        if MapBuilder.GetTile(main_matrix, (position[0], position[1] - 1)) in [CHAR_FOR_PATH]:
            if MapBuilder.GetTile(main_matrix, (position[0], position[1] - 2)) in [CHAR_FOR_EMPTY, CHAR_FOR_MAP_BOARD]:
                return position[0], position[1] - 1
        return False

    @staticmethod
    def DeleteFakeDoors(main_matrix):
        for i in range(1, len(main_matrix) - 1):
            for j in range(1, len(main_matrix[0]) - 1):
                if MapBuilder.GetTile(main_matrix, (i, j)) in [CHAR_FOR_DOOR]:
                    interm = MapBuilder.IsThereFakeDoor(main_matrix, (i, j))
                    if interm is not False:
                        main_matrix[i][j] = CHAR_FOR_UP_WALL
                        main_matrix[interm[0]][interm[1]] = CHAR_FOR_EMPTY

    @staticmethod
    def SetBoardsOfMap(main_matrix):
        for i in range(len(main_matrix)):
            main_matrix[i][0] = CHAR_FOR_MAP_BOARD
        for i in range(len(main_matrix[0])):
            main_matrix[len(main_matrix) - 1][i] = CHAR_FOR_MAP_BOARD
        for i in range(len(main_matrix)):
            main_matrix[i][len(main_matrix[0]) - 1] = CHAR_FOR_MAP_BOARD
        for i in range(len(main_matrix[0])):
            main_matrix[0][i] = CHAR_FOR_MAP_BOARD

    @staticmethod
    def DeleteCutCorners(main_matrix):
        for i in range(1, len(main_matrix) - 1):
            for j in range(1, len(main_matrix[0]) - 1):
                if MapBuilder.IsThereCutCorner(main_matrix, (i, j)):
                    main_matrix[i][j] = CHAR_FOR_UP_WALL

    @staticmethod
    def DeleteCutCornersAfterCreate(main_matrix, list_of_corners):
        for i in list_of_corners:
            main_matrix[i[0]][i[1]] = CHAR_FOR_UP_WALL

    @staticmethod
    def MakeCutCorners(main_matrix, list_of_corners):
        for i in range(1, len(main_matrix) - 1):
            for j in range(1, len(main_matrix[0]) - 1):
                if MapBuilder.IsThereCorner(main_matrix, (i, j)):
                    list_of_corners.append((i, j))
                    main_matrix[i][j] = CHAR_FOR_EMPTY

    @staticmethod
    def SetPathsOnMap(main_matrix):
        dfs = DFSAlgoForMapBuilder()
        for i in range(1, len(main_matrix) - 1):
            for j in range(1, len(main_matrix[0]) - 1):
                if main_matrix[i][j] == CHAR_FOR_EMPTY:
                    dfs.DFSForPaths(main_matrix, (i, j))
                    for k in dfs.GetPath():
                        main_matrix[k[0]][k[1]] = CHAR_FOR_PATH
                    dfs.counter_for_doors = 1
        dfs.Clear()

    @staticmethod
    def SetDoorsBetweenRooms(main_matrix):
        counter = 1
        freq_of_door = random.randrange(MIN_FREQ_OF_DOOR, MAX_FREQ_OF_DOOR)
        for i in range(1, len(main_matrix) - 1):
            for j in range(1, len(main_matrix[0]) - 1):
                if MapBuilder.IsThereDoorBetweenRooms(main_matrix, (i, j)):
                    counter += 1
                    if counter % freq_of_door == 0:
                        if MapBuilder.GetTile(main_matrix, (i + 1, j)) in CHAR_FOR_UP_WALL:
                            main_matrix[i - 1][j] = CHAR_FOR_DOOR
                            main_matrix[i + 1][j] = CHAR_FOR_DOOR
                        else:
                            main_matrix[i][j - 1] = CHAR_FOR_DOOR
                            main_matrix[i][j + 1] = CHAR_FOR_DOOR

                        counter = 1
                        freq_of_door = random.randrange(
                            MIN_FREQ_OF_DOOR, MAX_FREQ_OF_DOOR)

    @staticmethod
    def DeleteDoubleDoors(main_matrix):
        dfs = DFSAlgoForMapBuilder()
        for i in range(1, len(main_matrix) - 1):
            for j in range(1, len(main_matrix[0]) - 1):
                if dfs.used.get((i, j)) is None:
                    if MapBuilder.GetTile(main_matrix, (i, j)) in [CHAR_FOR_DOOR] and MapBuilder.GetTile(main_matrix, (
                            i - 1, j)) in [CHAR_FOR_DOOR]:
                        main_matrix[i - 1][j] = CHAR_FOR_UP_WALL
                    if MapBuilder.GetTile(main_matrix, (i, j)) in [CHAR_FOR_DOOR] and MapBuilder.GetTile(main_matrix, (
                            i, j - 1)) in [CHAR_FOR_DOOR]:
                        main_matrix[i][j - 1] = CHAR_FOR_UP_WALL

    @staticmethod
    def SetFloorInFrontOfDoor(main_matrix):
        for i in range(1, len(main_matrix) - 1):
            for j in range(1, len(main_matrix[0]) - 1):
                if MapBuilder.GetTile(main_matrix, (i, j)) in [CHAR_FOR_DOOR]:
                    if MapBuilder.GetTile(main_matrix, (i + 1, j)) in [CHAR_FOR_FLOOR]:
                        main_matrix[i - 1][j] = CHAR_FOR_PATH
                    if MapBuilder.GetTile(main_matrix, (i - 1, j)) in [CHAR_FOR_FLOOR]:
                        main_matrix[i + 1][j] = CHAR_FOR_PATH
                    if MapBuilder.GetTile(main_matrix, (i, j + 1)) in [CHAR_FOR_FLOOR]:
                        main_matrix[i][j - 1] = CHAR_FOR_PATH
                    if MapBuilder.GetTile(main_matrix, (i, j - 1)) in [CHAR_FOR_FLOOR]:
                        main_matrix[i][j + 1] = CHAR_FOR_PATH

    @staticmethod
    def DeleteDeadEnds(main_matrix):
        dfs = DFSAlgoForMapBuilder()
        for i in range(1, len(main_matrix) - 1):
            for j in range(1, len(main_matrix[0]) - 1):
                if MapBuilder.GetTile(main_matrix, (i, j)) in [CHAR_FOR_PATH] and MapBuilder.IsThereAnyTile(main_matrix,
                                                                                                            (i, j), [
                                                                                                                CHAR_FOR_DOOR]):
                    dfs.DFSForDeletingDeadEnds(main_matrix, (i, j))
        dfs.Clear()

    @staticmethod
    def ClearMatrix(main_matrix):
        for i in range(len(main_matrix)):
            for j in range(len(main_matrix[0])):
                main_matrix[i][j] = CHAR_FOR_EMPTY

    @staticmethod
    def DeleteNotConnectedComponents(main_matrix):
        matrix = []
        sign = False
        dfs = DFSAlgoForMapBuilder()
        for i in range(1, len(main_matrix) - 1):
            for j in range(1, len(main_matrix[0]) - 1):
                if MapBuilder.GetTile(main_matrix, (i, j)) in [CHAR_FOR_DOOR]:
                    dfs.DFSOnTheSpecificTiles(main_matrix, (i, j), matrix,
                                              SET_WITH_WALLS + [CHAR_FOR_FLOOR, CHAR_FOR_DOOR, CHAR_FOR_PATH])
                    sign = True
                    break
            if sign:
                break

        MapBuilder.ClearMatrix(main_matrix)
        for i in matrix:
            main_matrix[i[0][0]][i[0][1]] = i[1]


class DFSAlgoForMapBuilder:
    def __init__(self):
        self.used = {}
        self.parents = {}
        self.path = []
        self.counter_for_doors = 1
        self.freq_of_doors = random.randrange(MIN_FREQ_OF_DOOR, MAX_FREQ_OF_DOOR)

    def RandFreq(self):
        self.freq_of_doors = random.randrange(MIN_FREQ_OF_DOOR, MAX_FREQ_OF_DOOR)

    def GetPath(self):
        return self.path

    def Clear(self):
        self.parents.clear()
        self.path.clear()
        self.used.clear()
        self.counter_for_doors = 1

    def DFSForPaths(self, main_matrix, vertex):
        sign = False
        for i in MapBuilder.GetAround(main_matrix, vertex):
            for j in i:
                if j not in [(-1, -1), vertex]:
                    if self.parents.get(vertex) is not None:
                        if MapBuilder.IsItWallForDoor(main_matrix, j):
                            if self.used.get((j[0], j[1] - 2)) is not None or self.used.get(
                                    (j[0], j[1] + 2)) is not None or self.used.get(
                                (j[0] - 2, j[1])) is not None or self.used.get((j[0] + 2, j[1])) is not None:
                                if self.parents.get(vertex)[0] == j[0] or self.parents.get(vertex)[1] == j[1]:
                                    main_matrix[j[0]][j[1]] = CHAR_FOR_POTENTIAL_DOOR
                    if j == self.parents.get(vertex):
                        continue

                    if MapBuilder.GetTile(main_matrix, j) not in [CHAR_FOR_EMPTY, CHAR_FOR_MAP_BOARD]:
                        sign = True
                        continue

                    if self.used.get(j):
                        second_sign = False
                        for line in MapBuilder.GetAroundForDFS(main_matrix, vertex, self.parents[vertex]):
                            if j in line:
                                second_sign = True
                                break
                        if second_sign:
                            continue
                        sign = True
                        continue
        if sign:
            return
        self.used[vertex] = True
        self.path.append(vertex)

        neighbours = MapBuilder.GetNeighbours(main_matrix, vertex).copy()
        while len(neighbours) != 0:
            i = random.choice(neighbours)
            neighbours.remove(i)
            if self.used.get(i) is None and i != self.parents.get(vertex) and MapBuilder.GetTile(main_matrix,
                                                                                                 i) not in [
                CHAR_FOR_MAP_BOARD]:
                self.parents[i] = vertex
                self.DFSForPaths(main_matrix, i)

    def DFSForDeletingDeadEnds(self, main_matrix, vertex):
        self.used[vertex] = True
        self.path.append(vertex)

        for i in MapBuilder.GetNeighbours(main_matrix, vertex):
            if self.used.get(i) is None and i != self.parents.get(vertex) and MapBuilder.GetTile(main_matrix, i) in [
                CHAR_FOR_PATH]:
                self.parents[i] = vertex
                self.DFSForDeletingDeadEnds(main_matrix, i)
        if self.parents.get(vertex) is not None:
            if MapBuilder.IsThereDeadEnd(main_matrix, vertex, self.parents.get(vertex)):
                main_matrix[vertex[0]][vertex[1]] = CHAR_FOR_EMPTY

    def DFSForSetDoors(self, main_matrix, vertex):
        if self.used.get(vertex) is not None:
            return
        self.used[vertex] = True
        if self.counter_for_doors < self.freq_of_doors:
            self.counter_for_doors += 1
        self.path.append(vertex)
        if MapBuilder.GetTile(main_matrix, vertex) in [
            CHAR_FOR_POTENTIAL_DOOR] and self.counter_for_doors % self.freq_of_doors == 0:
            # if MapBuilder.GetTile(vertex) in [kProbDoor]:
            main_matrix[vertex[0]][vertex[1]] = CHAR_FOR_DOOR
            self.RandFreq()
            self.counter_for_doors = 0
        for i in MapBuilder.GetNeighbours(main_matrix, vertex):
            if self.used.get(i) is None and i != self.parents.get(vertex) and MapBuilder.GetTile(main_matrix, i) in [
                CHAR_FOR_POTENTIAL_DOOR, CHAR_FOR_DOOR,
                CHAR_FOR_UP_WALL]:
                self.parents[i] = vertex
                self.DFSForSetDoors(main_matrix, i)

    def RecursiveDFSOnTheSpecific(self, main_matrix, vertex, final_matrix, tiles, current_depth, flag=None, keys=None,
                                  depth=100000):
        self.used[vertex] = True
        self.path.append(vertex)
        final_matrix.append((vertex, MapBuilder.GetTile(main_matrix, vertex)))
        if flag == 'room' and MapBuilder.GetTile(main_matrix,
                                                 vertex) in SET_WITH_WALLS:
            for i in MapBuilder.GetNeighbours(main_matrix, vertex):
                if self.used.get(i) is None and i != self.parents.get(vertex):
                    if MapBuilder.GetTile(main_matrix,
                                                 i) in SET_WITH_WALLS:
                        self.path.append(i)
                        final_matrix.append((i, MapBuilder.GetTile(main_matrix, i)))
            return
        if current_depth >= depth:
            return
        for i in MapBuilder.GetNeighbours(main_matrix, vertex):
            if MapBuilder.GetTile(main_matrix, i) in tiles:
                if flag == 'path':
                    if MapBuilder.GetTile(main_matrix, i) in [CHAR_FOR_DOOR] and MapBuilder.GetTile(
                            main_matrix, vertex) in [CHAR_FOR_PATH]:
                        keys.append(vertex)
                if flag == 'room':
                    if MapBuilder.GetTile(main_matrix, i) in [CHAR_FOR_DOOR]:
                        keys[0][vertex] = vertex
                        keys[1][i] = i
                if self.used.get(i) is None and i != self.parents.get(vertex):
                    self.parents[i] = vertex
                    self.RecursiveDFSOnTheSpecific(main_matrix, i, final_matrix, tiles, current_depth=current_depth + 1,
                                                   flag=flag,
                                                   keys=keys, depth=depth)

    def DFSOnTheSpecificTiles(self, main_matrix, vertex, final_matrix, tiles, keys=None, flag=None, depth=1000000):
        self.Clear()
        self.RecursiveDFSOnTheSpecific(main_matrix, vertex, final_matrix, tiles, keys=keys, current_depth=0, flag=flag,
                                       depth=depth)
