class Level:
    '''Определяет вид уровня, его состояние.'''

    def __init__(self, filename):
        self.filename = filename
        self.loadLevel()

    def loadLevel(self):
        with open(self.filename, 'r') as mapFile:
            self.level = []
            for line in mapFile:
                self.level.append(line.strip())
        return self.level

    def generateLevel(self, obj_module, char_module, all_sprites):
        size = (50, 50)
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                if self.level[y][x] == "1":
                    block = obj_module.ObjectBlock('dirt_up', (size[0], size[1] - 25))
                    obj_module.BlockInWorld(block, (x * size[0], y * size[1]), all_sprites)
                elif self.level[y][x] == "-":
                    block = obj_module.ObjectBlock('dirt_up', size)
                    obj_module.BlockInWorld(block, (x * size[0], y * size[1]), all_sprites)
                elif self.level[y][x] == "_":
                    block = obj_module.ObjectBlock('dirt_down', size)
                    obj_module.BlockInWorld(block, (x * size[0], y * size[1]), all_sprites)
                elif self.level[y][x] == "!":
                    block = obj_module.ObjectBlock('lava', size)
                    obj_module.DamageBlockInWorld(block, (x * size[0], y * size[1]), all_sprites)
                elif self.level[y][x] == "@":
                    player = char_module.Player(100, (x * size[0], y * size[1]), all_sprites)
                elif self.level[y][x] == "#":
                    enemy = char_module.Enemy(100, (x * size[0] - 50, y * size[1] - 50), all_sprites)
        return player, x, y


class Camera:
    # зададим начальный сдвиг камеры и размер поля для возможности реализации циклического сдвига
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        # вычислим координату клетки, если она уехала влево за границу экрана
        if obj.rect.x < -obj.rect.width:
            obj.rect.x += (self.field_size[0] + 1) * 50
        # вычислим координату клетки, если она уехала вправо за границу экрана
        if obj.rect.x >= (self.field_size[0]) * 50:
            obj.rect.x += -obj.rect.width * (1 + self.field_size[0])
        obj.rect.y += self.dy
        # вычислим координату клетки, если она уехала вверх за границу экрана
        if obj.rect.y < -obj.rect.height:
            obj.rect.y += (self.field_size[1] + 1) * 50
        # вычислим координату клетки, если она уехала вниз за границу экрана
        if obj.rect.y >= (self.field_size[1]) * 50:
            obj.rect.y += -obj.rect.height * (1 + self.field_size[1])

    # позиционировать камеру на объекте target
    def update(self, target, size_screen):
        self.dx = -(target.rect.x + target.rect.w // 4 - size_screen[0] // 2)
        self.dy = -(target.rect.y + target.rect.h // 4 - size_screen[1] // 2)