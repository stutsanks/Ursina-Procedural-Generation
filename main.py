from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
app = Ursina()


class Block(Button):
    def __init__(self, pos, parent=scene):
        super().__init__(
            model='cube',
            color=color.green,
            position=pos,
            parent=parent,
            texture='white_cube'
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                destroy(self)
            elif key == 'right mouse down':
                Block(self.position+mouse.normal, self.parent)


chunks = {}

def check_chunk(x,z):
    if chunks.get(str(x)+str(z)):
        if chunks.get(str(x)+str(z))[0] != 'loaded':
            return True
        else:
            return False
    else:
        return True

def make_chunk(x, z):
    global chunks
    if str(x)+str(z) in chunks:
        chunk = chunks.get(str(x)+str(z))[1]
        chunk.enable()
        chunks[str(x)+str(z)] = ['loaded', chunk]
        return
    chunk = Entity()
    ground = 16
    for i in range(ground**2):
        Block(Vec3(floor(i / ground)+(x*16), 0, floor(i % ground)+(z*16)), chunk)  # noqa: E501
    chunks[str(x)+str(z)] = ['loaded', chunk]


def disable_chunk(chunk=None, x=None, z=None):
    if chunk is not None:
        chunk.disable()
    else:
        chunk = chunks.get(str(x)+str(z))[1]
        chunk.disable()
        chunks[str(x)+str(z)] = ['unloaded', chunk]


player = FirstPersonController()
current_chunk_x = floor(player.x/16)
current_chunk_z = floor(player.z/16)
last_chunk_x = floor(player.x/16)
last_chunk_z = floor(player.z/16)
make_chunk(current_chunk_x, current_chunk_z)

ground = 16  # Dont edit (Ancestor of chunk size)


def update():
    global current_chunk_x, current_chunk_z, last_chunk_x, last_chunk_z
    current_chunk_x = floor(player.x/16)
    current_chunk_z = floor(player.z/16)
    if check_chunk(current_chunk_x,current_chunk_z):
        make_chunk(current_chunk_x, current_chunk_z)
        disable_chunk(x=last_chunk_x, z=last_chunk_z)
        last_chunk_x = floor(player.x/16)
        last_chunk_z = floor(player.z/16)


app.run()
