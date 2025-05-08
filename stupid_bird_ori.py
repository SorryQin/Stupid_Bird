import pygame
import random

# 初始化 Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 400, 600
BIRD_SIZE = 30
OBSTACLE_WIDTH = 50
OBSTACLE_GAP = 180  # 适当增大间隙，方便通过
BIRD_X = 50
GRAVITY = 0.25
JUMP = -6
SPEED = 3

# 创建游戏窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("笨鸟先飞")

# 加载图片
bird_img = pygame.Surface((BIRD_SIZE, BIRD_SIZE))
bird_img.fill((255, 255, 0))


# 定义小鸟类
class Bird:
    def __init__(self):
        self.y = HEIGHT // 2
        self.vel = 0

    def jump(self):
        self.vel = JUMP

    def move(self):
        self.vel += GRAVITY
        self.y += self.vel

    def draw(self):
        screen.blit(bird_img, (BIRD_X, self.y))

    def collide(self, obstacles):
        for obs in obstacles:
            if (BIRD_X + BIRD_SIZE > obs[0] and BIRD_X < obs[0] + OBSTACLE_WIDTH) and (
                    self.y < obs[1] or self.y + BIRD_SIZE > obs[1] + OBSTACLE_GAP
            ):
                return True
        return self.y < 0 or self.y + BIRD_SIZE > HEIGHT


# 定义障碍物生成函数
def generate_obstacle():
    # 让障碍物生成的范围更合理
    min_height = 80
    max_height = HEIGHT - OBSTACLE_GAP - 80
    top_height = random.randint(min_height, max_height)
    return [WIDTH, top_height]


# 初始化小鸟和障碍物
bird = Bird()
obstacles = [generate_obstacle()]

# 游戏主循环
clock = pygame.time.Clock()
score = 0
running = True
while running:
    screen.fill((0, 0, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    # 移动小鸟
    bird.move()

    # 移动障碍物
    new_obstacles = []
    for obs in obstacles:
        obs[0] -= SPEED
        if obs[0] + OBSTACLE_WIDTH > 0:
            new_obstacles.append(obs)
        else:
            score += 1

    # 生成新的障碍物
    if len(new_obstacles) == 0 or new_obstacles[-1][0] < WIDTH - 200:
        new_obstacles.append(generate_obstacle())

    obstacles = new_obstacles

    # 绘制障碍物
    for obs in obstacles:
        # 绘制上半部分障碍物
        pygame.draw.rect(screen, (0, 255, 0), (obs[0], 0, OBSTACLE_WIDTH, obs[1]))
        # 绘制下半部分障碍物
        pygame.draw.rect(screen, (0, 255, 0),
                         (obs[0], obs[1] + OBSTACLE_GAP, OBSTACLE_WIDTH, HEIGHT - obs[1] - OBSTACLE_GAP))

    # 绘制小鸟
    bird.draw()

    # 检查碰撞
    if bird.collide(obstacles):
        running = False

    # 显示分数
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

# 游戏结束
print(f"游戏结束，你的分数是: {score}")
pygame.quit()
