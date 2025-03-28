from src.back.personages import Personage, personages
from src.back.animation import Animation
from src.back.player import kSizeOfCharacter

kHealthPoints = 100


class EnemyPersonage:
    def __init__(self, size, health, personage: Personage):
        self.size = size
        self.health = health
        self.personage = personage


enemy_personages = []

enemy_skeleton_warior = EnemyPersonage(kSizeOfCharacter, kHealthPoints, personages[9])
enemy_goblin = EnemyPersonage(kSizeOfCharacter, kHealthPoints, personages[10])
enemy_mushroom = EnemyPersonage(kSizeOfCharacter, kHealthPoints, personages[11])
enemy_flying_eye = EnemyPersonage(kSizeOfCharacter, kHealthPoints, personages[12])

enemy_personages.append(enemy_skeleton_warior)
enemy_personages.append(enemy_goblin)
enemy_personages.append(enemy_mushroom)
enemy_personages.append(enemy_flying_eye)
