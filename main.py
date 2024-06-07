import sys
import random
import time
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QVBoxLayout, 
                             QDialog, QDialogButtonBox, QHBoxLayout, QComboBox, QPushButton)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QCoreApplication
from figure_generator import FigureGenerator

class Game:
    def __init__(self):
        self.figure_size = 25
        self.figure_paths = [f'images/figure_{i}.png' for i in range(1, 9)]
        self.target_figures = ['images/figure_2.png', 'images/figure_4.png', 'images/figure_6.png', 'images/figure_7.png']
        self.pixmaps = {}
        self.generate_figures()
        self.load_pixmaps()

    def generate_figures(self):
        figure_generator = FigureGenerator()
        figure_generator.generate_figures()

    def load_pixmaps(self):
        self.pixmaps = {path: QPixmap(path).scaled(self.figure_size, self.figure_size, Qt.KeepAspectRatio)
                        for path in self.figure_paths}

class InstructionDialog(QDialog):
    def __init__(self, game, on_start_game):
        super().__init__()
        self.setWindowTitle('Game Instructions')
        self.setFixedSize(400, 400)
        self.game = game
        self.on_start_game = on_start_game
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title
        title_label = QLabel("<h2>Game Instructions</h2>")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Instruction label
        instruction_label = QLabel("The task is to identify the following 4 figures:")
        instruction_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(instruction_label)

        # Figures layout
        figure_layout = QHBoxLayout()
        for figure in self.game.target_figures:
            label = QLabel()
            pixmap = QPixmap(figure).scaled(30, 30, Qt.KeepAspectRatio)
            label.setPixmap(pixmap)
            figure_layout.addWidget(label)
        figure_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(figure_layout)

        # Detailed usage information
        usage_label = QLabel(
            "<p><b>Objective:</b> Identify the target figures as you navigate through the grid.</p>"
            "<p><b>Instructions:</b></p>"
            "<ul>"
            "<li>Use the left arrow key (←) to mark a figure as 'Yes' if it matches one of the target figures.</li>"
            "<li>Use the right arrow key (→) to mark a figure as 'No' if it does not match any of the target figures.</li>"
            "</ul>"
            "<p>Navigate through the grid and make your selections to complete the game.</p>"
        )
        usage_label.setWordWrap(True)
        layout.addWidget(usage_label)

        # Combo box label
        combo_label = QLabel("Select the number of squares:")
        combo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(combo_label)

        # Combo box
        self.combo_box = QComboBox()
        self.combo_box.addItems(['100', '200', '300', '400'])
        layout.addWidget(self.combo_box)

        # Button box
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.start_game)
        button_box.rejected.connect(QCoreApplication.instance().quit)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def start_game(self):
        grid_size = int(self.combo_box.currentText())
        self.on_start_game(grid_size)
        self.accept()

    def closeEvent(self, event):
        QCoreApplication.instance().quit()

class MainWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.setWindowTitle('Random Figures Game')
        self.setMinimumSize(400, 400)
        self.setMaximumSize(600, 600)

        self.game = game
        self.grid_size = 10
        self.page = 0
        self.total_pages = 1
        self.current_x = 0
        self.current_y = 0
        self.score = 0
        self.errors = 0
        self.start_time = None
        self.can_move = True

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.grid_layout = QGridLayout(self.central_widget)
        self.labels = []

    def start_game(self, total_elements):
        self.total_pages = total_elements // 100
        self.page = 0
        self.current_x = 0
        self.current_y = 0
        self.score = 0
        self.errors = 0
        self.start_time = time.time()
        self.setup_grid()

    def setup_grid(self):
        self.clear_grid()
        self.labels = []
        for i in range(self.grid_size):
            row_labels = []
            for j in range(self.grid_size):
                label = QLabel()
                pixmap = random.choice(list(self.game.pixmaps.values()))
                label.setPixmap(pixmap)
                label.setFixedSize(self.game.figure_size + 6, self.game.figure_size + 6)
                self.grid_layout.addWidget(label, i, j)
                row_labels.append(label)
            self.labels.append(row_labels)

        self.update_cursor()

    def clear_grid(self):
        for i in reversed(range(self.grid_layout.count())):
            widget_to_remove = self.grid_layout.itemAt(i).widget()
            self.grid_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

    def keyPressEvent(self, event):
        if self.can_move:
            if event.key() == Qt.Key_Left:
                self.check_figure(False)
            elif event.key() == Qt.Key_Right:
                self.check_figure(True)
            self.can_move = False

    def keyReleaseEvent(self, event):
        if event.key() in (Qt.Key_Left, Qt.Key_Right):
            self.can_move = True

    def move_cursor(self, dx, dy):
        self.current_x += dx
        if self.current_x >= self.grid_size:
            self.current_x = 0
            self.current_y += 1

        if self.current_y >= self.grid_size:
            self.current_y = 0
            self.page += 1
            if self.page >= self.total_pages:
                self.show_statistics()
                return
            self.setup_grid()
            return

        self.update_cursor()

    def update_cursor(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                label = self.labels[i][j]
                label.setStyleSheet("border: none;")

        cursor_label = self.labels[self.current_y][self.current_x]
        cursor_label.setStyleSheet("border: 2px solid black; padding: 0px;")

    def check_figure(self, is_target):
        pixmap = self.labels[self.current_y][self.current_x].pixmap()
        figure_path = [key for key, value in self.game.pixmaps.items() if value.cacheKey() == pixmap.cacheKey()][0]
        if (figure_path in self.game.target_figures) == is_target:
            self.score += 1
        else:
            self.errors += 1
        self.move_cursor(1, 0)

    def show_statistics(self):
        elapsed_time = time.time() - self.start_time
        total_attempts = self.score + self.errors
        success_rate = (self.score / total_attempts) * 100 if total_attempts > 0 else 0
        error_rate = (self.errors / total_attempts) * 100 if total_attempts > 0 else 0

        # Save statistics to a file
        self.save_statistics(elapsed_time, success_rate, error_rate)

        stats_dialog = QDialog(self)
        stats_dialog.setWindowTitle("Game Over")
        stats_dialog.setMinimumSize(300, 150)
        stats_dialog.setMaximumSize(300, 150)

        layout = QVBoxLayout()
        message = QLabel(f"Time: {elapsed_time:.2f} seconds\n"
                         f"Correct hits: {self.score} ({success_rate:.2f}%)\n"
                         f"Errors: {self.errors} ({error_rate:.2f}%)")
        layout.addWidget(message)

        button_layout = QHBoxLayout()
        new_game_button = QPushButton("New Game")
        new_game_button.clicked.connect(lambda: (stats_dialog.accept(), self.show_instructions()))
        button_layout.addWidget(new_game_button)

        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(QCoreApplication.instance().quit)
        button_layout.addWidget(exit_button)

        layout.addLayout(button_layout)
        stats_dialog.setLayout(layout)

        stats_dialog.rejected.connect(QCoreApplication.instance().quit)

        stats_dialog.exec_()

    def save_statistics(self, elapsed_time, success_rate, error_rate):
        with open('game_statistics.txt', 'a') as f:
            f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M")}\n')
            f.write(f'Time: {elapsed_time:.2f} seconds\n')
            f.write(f'Correct hits: {self.score} ({success_rate:.2f}%)\n')
            f.write(f'Errors: {self.errors} ({error_rate:.2f}%)\n\n')

    def show_instructions(self):
        dialog = InstructionDialog(self.game, self.start_game)
        if dialog.exec_() == QDialog.Rejected:
            QCoreApplication.instance().quit()

    def closeEvent(self, event):
        QCoreApplication.instance().quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create game instance
    game = Game()

    # Show instructions dialog before showing the main window
    dialog = InstructionDialog(game, lambda grid_size: None)
    if dialog.exec_() == QDialog.Rejected:
        QCoreApplication.instance().quit()
    else:
        window = MainWindow(game)
        window.start_game(int(dialog.combo_box.currentText()))
        window.show()

    sys.exit(app.exec_())