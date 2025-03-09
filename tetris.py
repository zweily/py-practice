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

class Tetris:
    def __init__(self, root):
        self.root = root
        # 增加画布高度以容纳分数显示区域
        self.canvas = tk.Canvas(root, width=WIDTH * CELL_SIZE, height=HEIGHT * CELL_SIZE + 40, bg='black')
        self.canvas.pack()
        self.board = [[0] * WIDTH for _ in range(HEIGHT)]
        self.current_shape = self.new_shape()
        self.current_x = WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0
        self.game_over = False
        self.score = 0
        self.draw_board()
        
        # 添加重新开始按钮
        self.restart_button = tk.Button(root, text="Restart", command=self.restart_game)
        self.restart_button.pack()

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

    def new_shape(self):
        shape, color = random.choice(SHAPES)
        return (shape, color)

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
        return lines_cleared

    def update(self):
        if self.game_over:
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

    def draw_board(self):
        self.canvas.delete("all")
        
        # 创建分数显示区域在游戏区域上方
        self.canvas.create_rectangle(0, 0, WIDTH * CELL_SIZE, 40, fill="black", outline="white")
        self.score_text = self.canvas.create_text(
            WIDTH * CELL_SIZE // 2, 20, text=f"Score: {self.score}", 
            fill="white", anchor="center", font=("Arial", 16, "bold")
        )
        
        # 绘制游戏区域边框 - 向下偏移40像素
        game_top = 40  # 游戏区域顶部的Y坐标
        self.canvas.create_rectangle(0, game_top, WIDTH * CELL_SIZE, game_top + HEIGHT * CELL_SIZE, outline="white")
        
        # 绘制已放置的方块 - 需要考虑偏移
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.board[y][x]:
                    self.canvas.create_rectangle(
                        x * CELL_SIZE, y * CELL_SIZE + game_top,
                        (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE + game_top,
                        fill=self.board[y][x], outline="white"
                    )
        
        # 绘制当前移动的方块 - 需要考虑偏移
        color = self.current_shape[1]
        for i, row in enumerate(self.current_shape[0]):
            for j, cell in enumerate(row):
                if cell:
                    self.canvas.create_rectangle(
                        (self.current_x + j) * CELL_SIZE, (self.current_y + i) * CELL_SIZE + game_top,
                        (self.current_x + j + 1) * CELL_SIZE, (self.current_y + i + 1) * CELL_SIZE + game_top,
                        fill=color, outline="white"
                    )
                    
        # 如果游戏结束，显示Game Over文本
        if self.game_over:
            self.canvas.create_text(
                WIDTH * CELL_SIZE / 2, game_top + HEIGHT * CELL_SIZE / 2,
                text="Game Over", fill="red", font=("Arial", 36, "bold"), anchor="center"
            )

    def restart_game(self):
        """重新开始游戏"""
        self.board = [[0] * WIDTH for _ in range(HEIGHT)]
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
