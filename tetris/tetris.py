import random
import tkinter as tk

# 定义方块的形状和颜色
SHAPES = [
    ([[1, 1, 1, 1]], "cyan"),      # I
    ([[1, 1], [1, 1]], "yellow"),  # O
    ([[0, 1, 0], [1, 1, 1]], "purple"),  # T
    ([[0, 1, 1], [1, 1, 0]], "green"),   # S
    ([[1, 1, 0], [0, 1, 1]], "red"),     # Z
    ([[1, 1, 1], [1, 0, 0]], "orange"),  # L
    ([[1, 0, 0], [1, 1, 1]], "blue")     # J (新增)
]

# 游戏区域大小
WIDTH = 10
HEIGHT = 20
CELL_SIZE = 30  # 每个单元格的像素大小
INFO_WIDTH = 6  # 右侧信息栏宽度(单位为方格)

class Tetris:
    # 添加类变量来记录历史最高分
    best_score = 0
    
    def __init__(self, root):
        self.root = root
        # 创建包含游戏区和信息区的画布
        self.canvas = tk.Canvas(
            root, 
            width=(WIDTH + INFO_WIDTH) * CELL_SIZE,
            height=HEIGHT * CELL_SIZE, 
            bg='black'
        )
        self.canvas.pack()
        
        self.board = [[0] * WIDTH for _ in range(HEIGHT)]
        self.next_shape = self.generate_shape()  # 预生成下一个形状
        self.current_shape = self.new_shape()
        self.current_x = WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0
        self.game_over = False
        self.score = 0
        
        # 添加重新开始按钮到右侧信息栏
        self.restart_button = tk.Button(
            root, 
            text="Restart", 
            command=self.restart_game,
            width=10,
            height=2
        )
        # 使用窗口坐标来定位按钮
        self.restart_button.place(
            x=WIDTH * CELL_SIZE + INFO_WIDTH * CELL_SIZE // 2 - 45, 
            y=HEIGHT * CELL_SIZE - 40
        )
        
        self.draw_board()

    def drop(self):
        """让方块直接落到最底下"""
        if self.game_over:
            return  # 游戏结束时直接返回，不再产生新积木
        while self.valid_move(self.current_shape[0], self.current_x, self.current_y + 1):
            self.current_y += 1
        self.place_shape(self.current_shape[0], self.current_x, self.current_y)
        lines_cleared = self.clear_lines()
        if lines_cleared > 0:
            self.draw_board()
        self.current_shape = self.new_shape()
        self.current_x = WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0
        if not self.valid_move(self.current_shape[0], self.current_x, self.current_y):
            self.game_over = True
        self.draw_board()

    def move(self, dx, dy):
        """移动方块"""
        if self.valid_move(self.current_shape[0], self.current_x + dx, self.current_y + dy):
            self.current_x += dx
            self.current_y += dy
            self.draw_board()

    def rotate(self):
        """旋转方块"""
        rotated_shape = self.rotate_shape(self.current_shape[0])
        if self.valid_move(rotated_shape, self.current_x, self.current_y):
            self.current_shape = (rotated_shape, self.current_shape[1])
            self.draw_board()

    def generate_shape(self):
        """生成一个新形状"""
        shape, color = random.choice(SHAPES)
        return (shape, color)
    
    def new_shape(self):
        """返回下一个形状并生成新的下一个形状"""
        current = self.next_shape
        self.next_shape = self.generate_shape()
        return current

    def rotate_shape(self, shape):
        return [list(reversed(col)) for col in zip(*shape)]

    def valid_move(self, shape, x, y):
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell and (x + j < 0 or x + j >= WIDTH or y + i >= HEIGHT or self.board[y + i][x + j]):
                    return False
        return True

    def place_shape(self, shape, x, y):
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    self.board[y + i][x + j] = self.current_shape[1]  # 保存颜色信息

    def clear_lines(self):
        new_board = [row for row in self.board if 0 in row]
        lines_cleared = HEIGHT - len(new_board)
        self.board = [[0] * WIDTH for _ in range(lines_cleared)] + new_board
        self.score += lines_cleared * 100  # 每清除一行加100分
        
        # 更新最高分
        if self.score > Tetris.best_score:
            Tetris.best_score = self.score
            
        return lines_cleared

    def update(self):
        if self.game_over:
            # 游戏结束时检查是否需要更新最高分
            if self.score > Tetris.best_score:
                Tetris.best_score = self.score
            return  # 游戏结束时停止更新
        if self.valid_move(self.current_shape[0], self.current_x, self.current_y + 1):
            self.current_y += 1
        else:
            self.place_shape(self.current_shape[0], self.current_x, self.current_y)
            lines_cleared = self.clear_lines()
            if lines_cleared > 0:
                self.draw_board()
            self.current_shape = self.new_shape()
            self.current_x = WIDTH // 2 - len(self.current_shape[0]) // 2
            self.current_y = 0
            if not self.valid_move(self.current_shape[0], self.current_x, self.current_y):
                self.game_over = True
        self.draw_board()
        if not self.game_over:
            self.root.after(500, self.update)

    def draw_info_panel(self):
        """绘制右侧信息面板"""
        # 绘制信息区域背景
        info_x = WIDTH * CELL_SIZE
        self.canvas.create_rectangle(
            info_x, 0, 
            info_x + INFO_WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE,
            fill="black", outline="white"
        )
        
        # 显示当前分数
        self.canvas.create_text(
            info_x + INFO_WIDTH * CELL_SIZE // 2, 50,
            text="SCORE", fill="white", font=("Arial", 16, "bold")
        )
        self.canvas.create_text(
            info_x + INFO_WIDTH * CELL_SIZE // 2, 80,
            text=str(self.score), fill="white", font=("Arial", 24, "bold")
        )
        
        # 显示最高分
        self.canvas.create_text(
            info_x + INFO_WIDTH * CELL_SIZE // 2, 110,
            text="BEST SCORE", fill="white", font=("Arial", 14, "bold")
        )
        self.canvas.create_text(
            info_x + INFO_WIDTH * CELL_SIZE // 2, 135,
            text=str(Tetris.best_score), fill="gold", font=("Arial", 18, "bold")
        )
        
        # 显示"NEXT"标题
        self.canvas.create_text(
            info_x + INFO_WIDTH * CELL_SIZE // 2, 180,
            text="NEXT", fill="white", font=("Arial", 16, "bold")
        )
        
        # 显示下一个方块预览
        next_shape, next_color = self.next_shape
        shape_width = len(next_shape[0])
        shape_height = len(next_shape)
        
        # 计算预览区域的中心位置 - 稍微向下调整
        preview_center_x = info_x + INFO_WIDTH * CELL_SIZE // 2
        preview_center_y = 240
        
        # 计算方块左上角的位置
        offset_x = preview_center_x - shape_width * CELL_SIZE // 2
        offset_y = preview_center_y - shape_height * CELL_SIZE // 2
        
        for i, row in enumerate(next_shape):
            for j, cell in enumerate(row):
                if cell:
                    self.canvas.create_rectangle(
                        offset_x + j * CELL_SIZE, offset_y + i * CELL_SIZE,
                        offset_x + (j + 1) * CELL_SIZE, offset_y + (i + 1) * CELL_SIZE,
                        fill=next_color, outline="white"
                    )
        
        # 如果游戏结束，显示GAME OVER文本 - 位于下一个方块预览区的下方
        if self.game_over:
            self.canvas.create_text(
                info_x + INFO_WIDTH * CELL_SIZE // 2, 320,
                text="GAME OVER", fill="red", font=("Arial", 20, "bold"), anchor="center"
            )

    def draw_board(self):
        self.canvas.delete("all")
        
        # 绘制游戏区域边框
        self.canvas.create_rectangle(0, 0, WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE, outline="white")
        
        # 绘制已放置的方块
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.board[y][x]:
                    self.canvas.create_rectangle(
                        x * CELL_SIZE, y * CELL_SIZE,
                        (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                        fill=self.board[y][x], outline="white"
                    )
        
        # 绘制当前移动的方块
        color = self.current_shape[1]
        for i, row in enumerate(self.current_shape[0]):
            for j, cell in enumerate(row):
                if cell:
                    self.canvas.create_rectangle(
                        (self.current_x + j) * CELL_SIZE, (self.current_y + i) * CELL_SIZE,
                        (self.current_x + j + 1) * CELL_SIZE, (self.current_y + i + 1) * CELL_SIZE,
                        fill=color, outline="white"
                    )
        
        # 绘制右侧信息面板
        self.draw_info_panel()
        
        # 移除原来游戏区域中间的Game Over文本，现在显示在右侧状态栏中

    def restart_game(self):
        """重新开始游戏"""
        self.board = [[0] * WIDTH for _ in range(HEIGHT)]
        self.next_shape = self.generate_shape()  # 重新生成下一个形状
        self.current_shape = self.new_shape()
        self.current_x = WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0
        self.game_over = False
        self.score = 0
        self.draw_board()
        self.update()  # 重新开始游戏循环

def main():
    root = tk.Tk()
    root.title("Tetris")
    game = Tetris(root)
    
    def handle_key(event, action):
        if not game.game_over:  # 只有在游戏未结束时响应按键
            action()
    
    root.bind("<Left>", lambda event: handle_key(event, lambda: game.move(-1, 0)))
    root.bind("<Right>", lambda event: handle_key(event, lambda: game.move(1, 0)))
    root.bind("<Down>", lambda event: handle_key(event, lambda: game.move(0, 1)))
    root.bind("<Up>", lambda event: handle_key(event, lambda: game.rotate()))
    root.bind("<space>", lambda event: handle_key(event, game.drop))
    
    game.update()
    root.mainloop()

if __name__ == "__main__":
    main()
