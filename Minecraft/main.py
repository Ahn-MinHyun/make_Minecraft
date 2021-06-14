from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

window.fps_counter.enabled = False
window.exit_button.visible = False

# 효과음
punch = Audio('assets/magic', autoplay = False) # 자동 재생 방지


# 블럭 텍스쳐
blocks =[
    load_texture('assets/Dirt.png'),
    load_texture('assets/Dirt.png'), # 1
    load_texture('assets/stone.png'), # 2
    load_texture('assets/Lava.png'), # 3
    load_texture('assets/Diamond.png') # 4
]

block_id = 1

def input(key):
    global block_id, hand
    if key.isdigit():
        block_id = int(key)
        if block_id >= len(blocks):
            block_id = len(blocks) -1
        
        hand.texture = blocks[block_id]
    print(key)

# 하늘
sky = Entity(
    parent = scene,
    model = 'sphere', # 구형모양
    texture = load_texture('assets/2226755375_af16424e03_b.jpeg'),
    scale = 500,
    double_sided = True
)

# 오른손 추가 
hand = Entity(
    parent = camera.ui,
    model = 'assets/cube',
    texture = blocks[block_id],
    scale = 0.5,
    rotation = Vec3(-10, -10, 10),
    position = Vec2(0.6, -0.6)
)

# 손의 움직임 표현
def update():
    if held_keys['left mouse'] or held_keys['right_mouse']:
        punch.play()
        hand.position = Vec2(0.4, -0.5)
    else :
        hand.position = position = Vec2(0.6, -0.6)

class Voxel(Button):
    def __init__(self, position= (0,0,0), texture='assets/Dirt.png'):
        super().__init__(
            parent= scene,
            position =position,
            model ='assets/cube',
            origin_y= 0.5,
            texture = texture,
            color = color.color(0,0, random.uniform(0.9, 1.0)),
            scale = 1.0
        )
    # 블록 파괴 생성 
    def input(self, key):
        if self.hovered: 
            if key == 'left mouse down':
                Voxel(position = self.position +mouse.normal, texture = blocks[block_id])
            elif key =='right mouse down':
                destroy(self)

# 서있을 땅
for z in range(20):
    for x in range(20):
        voxel = Voxel(position=(x,0,z))

# 컨트롤 유저
player = FirstPersonController()

app.run()