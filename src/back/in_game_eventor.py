from src.back.Map.space import *


class Eventor:
    def __init__(self, player, map_processor, mini_map, enemies_processor):
        self.player = player
        self.map_processor = map_processor
        self.mini_map = mini_map
        self.prev_visited_rooms = None
        self.enemies_processor = enemies_processor
        self.room = self.map_processor.GetCurrentRoom()
        self.prev_position_of_player = None
        self.num_of_iterations = 0

    def EnterRoomEvent(self):
        current_room = self.map_processor.GetCurrentRoom()
        if current_room is not self.room and current_room is not self.map_processor.GetStartRoom() and current_room\
                not in self.prev_visited_rooms and current_room is not self.map_processor.GetFinishRoom():
            if isinstance(self.map_processor.GetCurrentRoom(), RoomSpace):
                vectors = {'D': (0, SIZE_OF_TILE // 4), 'U': (0, -SIZE_OF_TILE // 4), 'R': (SIZE_OF_TILE // 4, 0),
                           'L': (-SIZE_OF_TILE // 4, 0)}
                self.map_processor.CloseDoors()
                self.enemies_processor.SpawnInCurrentRoom()
                self.player.ChangePosition(vectors[self.map_processor.GetSideOfDoor(self.prev_position_of_player)])
                self.mini_map.MoveMiniMap((-vectors[self.map_processor.GetSideOfDoor(self.prev_position_of_player)][0],
                                           -vectors[self.map_processor.GetSideOfDoor(self.prev_position_of_player)][1]))
        self.room = self.map_processor.GetCurrentRoom()
        self.prev_position_of_player = self.player.GetStandPosition()

    def EnterExitRoom(self, render):
        current_room = self.map_processor.GetCurrentRoom()
        if current_room is self.map_processor.GetFinishRoom() and current_room not in self.prev_visited_rooms:
            self.map_processor.GenerateExit(render)

    def AllEnemiesDeadEvent(self, render):
        if self.enemies_processor.IsAllDead():
            if isinstance(self.map_processor.GetCurrentRoom(),
                          RoomSpace) and self.map_processor.GetCurrentRoom().IsDoorsClosed():
                self.map_processor.OpenDoors()
                self.map_processor.SpawnChestInCurrentRoom(render)

    def OnStart(self, render):
        pass

    def Update(self, render):
        if self.num_of_iterations == 0:
            self.OnStart(render)
        if self.prev_position_of_player is None:
            self.prev_position_of_player = self.player.GetStandPosition()
        self.EnterRoomEvent()
        self.EnterExitRoom(render)
        self.AllEnemiesDeadEvent(render)
        self.prev_visited_rooms = self.map_processor.GetVisitedRooms().copy()
        self.num_of_iterations += 1
