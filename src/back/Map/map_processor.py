from src.back.Map.Objects.map_objects import *
from src.back.Map.map import Map
from src.back.Map.space import *
from src.back.Map.map_generator import MapBuilder
import random


class MapProcessor:
    def __init__(self, mini_map):
        self.map = None
        self.mini_map = mini_map
        self.start_room = None
        self.finish_room = None
        self.current_room = None
        self.visited_rooms = []
        self.objects = []
        self.ConstructMap(SIZE_OF_MAP)

    def GetVisitedRooms(self):
        return self.visited_rooms

    def GetStartRoom(self):
        return self.start_room

    def GetFinishRoom(self):
        return self.finish_room

    def RedrawCurrentRoom(self):
        self.current_room.RedrawDoors(self.map.GetMatrix())

    def GetObjects(self):
        return self.objects

    def IsInCurrentRoom(self, position):
        return self.current_room.IsThere(position)

    def GetSideOfDoor(self, position):
        return MapBuilder.GetSideOfDoor(self.map.GetMatrix(), self.map.GetPositionOfTile(position))

    def AddObject(self, obj):
        self.objects.append(obj)

    def GenerateMap(self, size_of_map):
        self.map = Map(size_of_map)

    def GetCurrentRoom(self):
        return self.current_room

    def ConstructMap(self, size_of_map):
        self.GenerateMap(size_of_map)
        self.start_room = self.map.GetStartRoom()
        self.finish_room = self.map.GetFinishRoom(self.start_room)

    def GenerateExit(self, render):
        list_with_tiles = self.finish_room.GetCoordinatesOfTiles()
        while True:
            coord = random.choice(list_with_tiles)
            if self.finish_room.GetTile(coord) in [CHAR_FOR_FLOOR]:
                self.AddObject(Exit((coord[0] * SIZE_OF_TILE, coord[1] * SIZE_OF_TILE)))
                render.BlitItemOnMiniMap(Exit, (coord[0] * SIZE_OF_TILE, coord[1] * SIZE_OF_TILE))
                break

    def GetTilesOfCurrentRoom(self):
        return self.current_room.GetCoordinatesOfTiles()

    def UpdateCurrentRoom(self, player_position, minimap):
        self.current_room = self.map.GetCurrentRoom(player_position, self.current_room)
        if self.current_room not in self.visited_rooms:
            minimap.BlitOnMiniMap(self.current_room.GetTiles())
            self.visited_rooms.append(self.current_room)

    def GetSpawnPosition(self, minimap):
        spawn_position = random.choice([tile[0] for tile in self.start_room.GetTiles() if tile[1] in [CHAR_FOR_FLOOR]])
        minimap.SetStartPosition((-spawn_position[0], -spawn_position[1]))
        self.current_room = self.start_room
        return spawn_position[0] * SIZE_OF_TILE, spawn_position[1] * SIZE_OF_TILE

    def CanStandThere(self, position):
        return self.map.CanStandThere([int(position[0]), int(position[1])])

    def CloseDoors(self):
        if isinstance(self.current_room, RoomSpace):
            walls = [[tile, CHAR_FOR_CLOSED_DOOR] for tile in self.current_room.GetDoors()]
            self.map.SetSpecificTiles(walls)
            self.RedrawCurrentRoom()
        else:
            raise "when close door, current room is not room"

    def OpenDoors(self):
        if isinstance(self.current_room, RoomSpace):
            walls = [[tile, CHAR_FOR_DOOR] for tile in self.current_room.GetDoors()]
            self.map.SetSpecificTiles(walls)
            self.RedrawCurrentRoom()
        else:
            raise "when close door, current room is not room"

    def SpawnChest(self, position, render):
        self.AddObject(BasicChest(position))
        render.BlitItemOnMiniMap(BasicChest, position)

    def SpawnChestInCurrentRoom(self, render):
        if not self.current_room:
            raise "current room is empty"

        list_with_tiles = self.current_room.GetCoordinatesOfTiles()
        while True:
            coord = random.choice(list_with_tiles)
            if self.current_room.GetTile(coord) in [CHAR_FOR_FLOOR]:
                self.SpawnChest((coord[0] * SIZE_OF_TILE, coord[1] * SIZE_OF_TILE), render)
                break
