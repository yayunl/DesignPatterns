from abc import ABC, abstractmethod
from collections import namedtuple

class Side:
    NORTH = "North"
    SOUTH = "South"
    WEST = "West"
    EAST = "East"

def create_new_room(room_number):
    class Room:
        def __init__(self, room_number):
            self.room_number = room_number
            self.NORTH = None
            self.SOUTH = None
            self.WEST = None
            self.EAST = None

        def __str__(self):
            return f"Room<Number: {self.room_number}, " \
                   f"North: {self.NORTH}, " \
                   f"South: {self.SOUTH}, " \
                   f"West: {self.WEST}, " \
                   f"East: {self.EAST}>"

    rm = Room(room_number=room_number)
    return rm


def create_new_door(room1, room2):
    class Door:
        def __init__(self, room1, room2):
            self.room1 = room1
            self.room2 = room2
        def __str__(self):
            return f"Door<room:{self.room1}>"
    return Door(room1=room1, room2=room2)

# Abstract Product classes
class Maze(ABC):

    def __init__(self):
        self.maze = list()

    def __str__(self):
        """
        Print a maze
        :return:
        """
        if not self.maze:
            return "The maze is empty!"
        else:
            prints = ""
            for obj in self.maze:
                prints += f"Object: {obj}\n"
            return prints


    @abstractmethod
    def add_room(self, room):
        pass

class Room(ABC):
    
    def __init__(self, room_number):
        self.room = create_new_room(room_number)

    def __str__(self):
        return f"Room<Number: {self.room.room_number}, " \
               f"North: {self.room.NORTH}, " \
               f"South: {self.room.SOUTH}, " \
               f"West: {self.room.WEST}, " \
               f"East: {self.room.EAST}>"

    @abstractmethod
    def set_side(self, side, obj):
        """
        The interface for placing an object (i.e. `Wall` or `Door`) on the side (i.e. North, East, South, West) of a room
        :param side:
        :param obj:
        :return:
        """
        pass

class Wall(ABC):

    def __str__(self):
        return "A wall"

class Door(ABC):

    def __init__(self, room1, room2):
        self.door = create_new_door(room1, room2)

    def __str__(self):
        return f"Door<Room1: {self.door.room1.room.room_number}," \
               f"Room2: {self.door.room2.room.room_number}>"



# Concrete Product classes
class OrdinaryMaze(Maze):
    def add_room(self, room):
        # Implement the interface `add_room` declared in the Abstract Product `Maze`
        self.maze.append(room)

class OrdinaryRoom(Room):

    def __init__(self, room_number):
        super().__init__(room_number)

    def set_side(self, side, obj):
        # Implements the interface
        if side == Side.NORTH:
            self.room.NORTH = obj
        elif side == Side.SOUTH:
            self.room.SOUTH = obj
        elif side == Side.WEST:
            self.room.WEST = obj
        else:
            self.room.EAST = obj


class OrdinaryWall(Wall):
    pass

class OrdinaryDoor(Door):

    def __init__(self, room1, room2):
        super().__init__(room1, room2)


class EnchantedMaze(Maze):
    def add_room(self, room):
        self.maze.append(room)

class EnchantedRoom(Room):
    def __init__(self, room_number):
        super().__init__(room_number)

    def __str__(self):
        return f"EnchantedRoom<Number: {self.room.room_number}, " \
               f"North: {self.room.NORTH}, " \
               f"South: {self.room.SOUTH}, " \
               f"West: {self.room.WEST}, " \
               f"East: {self.room.EAST}>"

    def set_side(self, side, obj):
        # Implements the interface
        if side == Side.NORTH:
            self.room.NORTH = obj
        elif side == Side.SOUTH:
            self.room.SOUTH = obj
        elif side == Side.WEST:
            self.room.WEST = obj
        else:
            self.room.EAST = obj


class EnchantedWall(Wall):
    pass

class EnchantedDoor(Door):

    def __init__(self, room1, room2):
        super().__init__(room1=room1, room2=room2)


    def __str__(self):
        return f"DoorNeedingSpell<EnchantedRoom1: {self.door.room1.room.room_number}," \
               f"EnchantedRoom2: {self.door.room2.room.room_number}>"


# Abstract Factory class
class MazeFactory(ABC):
    @abstractmethod
    def create_maze(self):
        pass

    @abstractmethod
    def create_room(self, room_number):
        pass

    @abstractmethod
    def create_wall(self):
        pass

    @abstractmethod
    def create_door(self, room1, room2):
        # Abstract method to create a door between two rooms
        pass

# Concrete Factory classes
class OrdinaryMazeFactory(MazeFactory):

    # Implements the interfaces declared in the abstract factory `MazeFactory`
    def create_maze(self):
        # Defines a concrete product
        return OrdinaryMaze()

    def create_room(self, room_number):
        return OrdinaryRoom(room_number)

    def create_wall(self):
        return OrdinaryWall()

    def create_door(self, room1, room2):
        return OrdinaryDoor(room1, room2)

class EnchantedMazeFactory(MazeFactory):
    # Implements the interfaces declared in the abstract factory `MazeFactory`
    def create_maze(self):
        # Defines a concrete product
        return EnchantedMaze()

    def create_room(self, room_number):
        rm= EnchantedRoom(room_number)
        rm.room
        return rm

    def create_wall(self):
        return EnchantedWall()

    def create_door(self, room1, room2):
        return EnchantedDoor(room1, room2)

# Client code
class MazeGame:
    def __init__(self, factory):
        self.factory = factory

    def create_maze(self):
        maze = self.factory.create_maze()
        room1 = self.factory.create_room(1)
        room2 = self.factory.create_room(2)
        door = self.factory.create_door(room1, room2)

        # Assemble the maze using the created objects
        maze.add_room(room1)
        maze.add_room(room2)

        room1.set_side(Side.NORTH, self.factory.create_wall())
        room1.set_side(Side.EAST, door)
        room1.set_side(Side.SOUTH, self.factory.create_wall())
        room1.set_side(Side.WEST, self.factory.create_wall())

        room2.set_side(Side.NORTH, self.factory.create_wall())
        room2.set_side(Side.EAST, self.factory.create_wall())
        room2.set_side(Side.SOUTH, self.factory.create_wall())
        room2.set_side(Side.WEST, door)

        return maze

if __name__ == "__main__":
    # Usage

    older_than_5 = input("Are you older than 5 years?") or "y"
    if older_than_5.lower() == 'y':
        factory = EnchantedMazeFactory()  # Can be changed to OrdinaryMazeFactory

    else:
        factory = OrdinaryMazeFactory()
    game = MazeGame(factory)
    maze = game.create_maze()

    print(maze)
