import pygame
import random
import sys
import os

# 初始化pygame
pygame.init()

# 游戏窗口设置
WIDTH = 400
HEIGHT = 600
FPS = 60

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 创建游戏窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("飞机射击游戏")
clock = pygame.time.Clock()

# 加载图像
def load_image(name, scale=1):
    img = pygame.Surface((50, 50))
    img.fill(WHITE)
    if scale != 1:
        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
    img.set_colorkey(BLACK)
    return img

# 玩家飞机类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 创建玩家飞机形状
        self.image = pygame.Surface((50, 40), pygame.SRCALPHA)
        # 绘制飞机主体
        pygame.draw.polygon(self.image, BLUE, [(25, 0), (5, 30), (20, 25), (25, 40), (30, 25), (45, 30)])
        # 绘制机翼
        pygame.draw.polygon(self.image, GREEN, [(5, 30), (20, 25), (20, 35), (0, 35)])
        pygame.draw.polygon(self.image, GREEN, [(45, 30), (30, 25), (30, 35), (50, 35)])
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.health = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        
    def update(self):
        # 键盘控制
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        
        # 限制移动范围
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < HEIGHT / 2:
            self.rect.top = HEIGHT / 2
            
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

# 敌机类
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 创建敌机形状
        self.image = pygame.Surface((30, 40), pygame.SRCALPHA)
        # 绘制敌机主体
        pygame.draw.polygon(self.image, RED, [(15, 40), (0, 10), (30, 10)])
        # 绘制敌机机翼
        pygame.draw.polygon(self.image, (200, 0, 0), [(0, 10), (15, 0), (30, 10)])
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # 创建子弹形状
        self.image = pygame.Surface((8, 20), pygame.SRCALPHA)
        # 绘制子弹
        pygame.draw.polygon(self.image, BLUE, [(4, 0), (0, 10), (8, 10), (4, 0)])
        pygame.draw.rect(self.image, (100, 100, 255), (2, 10, 4, 10))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        # 子弹飞出屏幕时删除
        if self.rect.bottom < 0:
            self.kill()

# 爆炸效果
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        # 创建爆炸效果表面
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == 8:
                self.kill()
            else:
                center = self.rect.center
                self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                # 绘制爆炸效果
                radius = int(self.size/2 * (1 - self.frame/8))
                color = (255, 255 * (1 - self.frame/8), 0)
                pygame.draw.circle(self.image, color, (self.size//2, self.size//2), radius)
                # 添加爆炸射线
                for angle in range(0, 360, 45):
                    end_x = self.size//2 + int(radius * 1.5 * pygame.math.Vector2(1, 0).rotate(angle).x)
                    end_y = self.size//2 + int(radius * 1.5 * pygame.math.Vector2(1, 0).rotate(angle).y)
                    pygame.draw.line(self.image, color, (self.size//2, self.size//2), (end_x, end_y), 3)
                self.rect = self.image.get_rect()
                self.rect.center = center

# 游戏初始化
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(8):
    e = Enemy()
    all_sprites.add(e)
    enemies.add(e)

score = 0
font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_health_bar(surf, x, y, health):
    if health < 0:
        health = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (health / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def show_game_over_screen():
    screen.fill(BLACK)
    draw_text(screen, "飞机射击游戏", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, f"最终得分: {score}", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "按任意键开始新游戏", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

# 游戏循环
game_over = True
running = True
while running:
    if game_over:
        show_game_over_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            e = Enemy()
            all_sprites.add(e)
            enemies.add(e)
        score = 0
        
    # 保持循环以正确速度运行
    clock.tick(FPS)
    
    # 处理输入事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    # 更新
    all_sprites.update()
    
    # 检查子弹是否击中敌机
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        expl = Explosion(hit.rect.center, 30)
        all_sprites.add(expl)
        e = Enemy()
        all_sprites.add(e)
        enemies.add(e)
    
    # 检查敌机是否撞到玩家
    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        player.health -= 20
        expl = Explosion(hit.rect.center, 30)
        all_sprites.add(expl)
        e = Enemy()
        all_sprites.add(e)
        enemies.add(e)
        if player.health <= 0:
            game_over = True
    
    # 渲染
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_health_bar(screen, 5, 5, player.health)
    
    # 更新显示
    pygame.display.flip()

pygame.quit()
