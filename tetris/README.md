# Tetris Game | 俄罗斯方块游戏

## English

A Python implementation of the classic Tetris game.

### Game Design

This Tetris implementation follows the traditional game mechanics:

- Different shaped blocks (tetrominoes) fall from the top of the screen
- Player can move blocks left/right and rotate them
- When a row is filled completely, it disappears and the player scores points
- Game ends when blocks stack up to the top of the screen

### Technical Implementation

- Game built using Python's [pygame](https://www.pygame.org/) library for graphics and user input
- Object-oriented design with classes for:
  - Game board
  - Tetromino pieces
  - Game state management
  - Scoring system

### How to Play

1. Make sure you have Python and pygame installed
2. Navigate to the tetris directory
3. Run the game:
   ```
   python main.py
   ```

#### Controls

- **Left/Right Arrows**: Move tetromino horizontally
- **Down Arrow**: Accelerate falling
- **Up Arrow**: Rotate tetromino
- **Spacebar**: Hard drop
- **P**: Pause game
- **Esc**: Quit game

### Future Improvements

- Add high score tracking
- Implement different difficulty levels
- Add sound effects and music
- Create a more polished UI

---

## 中文

一个使用Python实现的经典俄罗斯方块游戏。

### 游戏设计

这个俄罗斯方块实现遵循传统的游戏机制：

- 不同形状的方块（俄罗斯方块）从屏幕顶部下落
- 玩家可以左右移动方块并旋转它们
- 当一行完全填满时，该行消失并且玩家得分
- 当方块堆叠到屏幕顶部时游戏结束

### 技术实现

- 游戏使用Python的[pygame](https://www.pygame.org/)库构建，用于图形和用户输入
- 面向对象设计，包含以下类：
  - 游戏板
  - 俄罗斯方块
  - 游戏状态管理
  - 计分系统

### 如何游玩

1. 确保你安装了Python和pygame
2. 导航到tetris目录
3. 运行游戏：
   ```
   python main.py
   ```

#### 控制

- **左/右箭头**：水平移动方块
- **下箭头**：加速下落
- **上箭头**：旋转方块
- **空格键**：硬下落
- **P键**：暂停游戏
- **Esc键**：退出游戏

### 未来改进

- 添加高分记录
- 实现不同的难度级别
- 添加音效和音乐
- 创建更精致的用户界面