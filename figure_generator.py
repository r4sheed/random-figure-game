import os
import matplotlib.pyplot as plt

class FigureGenerator:
    def __init__(self, directory='images'):
        self.directory = directory
        self.variations = [
            ('line_middle', 'top'),
            ('line_middle', 'bottom'),
            ('line_middle', 'left'),
            ('line_middle', 'right'),
            ('diagonal', 'top_left'),
            ('diagonal', 'top_right'),
            ('diagonal', 'bottom_left'),
            ('diagonal', 'bottom_right')
        ]
        self.ensure_directory_exists()

    def ensure_directory_exists(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def draw_square_with_variation(self, variation_type, position, filename):
        fig, ax = plt.subplots(figsize=(2, 2))
        
        # Draw square with thicker lines
        square = plt.Rectangle((0.1, 0.1), 0.8, 0.8, fill=None, edgecolor='black', linewidth=4)
        ax.add_patch(square)
        
        # Draw variation with thicker lines
        if variation_type == 'line_middle':
            if position == 'top':
                ax.plot([0.5, 0.5], [0.9, 1.1], color='black', linewidth=4)
            elif position == 'bottom':
                ax.plot([0.5, 0.5], [-0.1, 0.1], color='black', linewidth=4)
            elif position == 'left':
                ax.plot([-0.1, 0.1], [0.5, 0.5], color='black', linewidth=4)
            elif position == 'right':
                ax.plot([0.9, 1.1], [0.5, 0.5], color='black', linewidth=4)
        elif variation_type == 'diagonal':
            if position == 'top_left':
                ax.plot([0.1, -0.1], [0.9, 1.1], color='black', linewidth=4)
            elif position == 'top_right':
                ax.plot([0.9, 1.1], [0.9, 1.1], color='black', linewidth=4)
            elif position == 'bottom_left':
                ax.plot([0.1, -0.1], [0.1, -0.1], color='black', linewidth=4)
            elif position == 'bottom_right':
                ax.plot([0.9, 1.1], [0.1, -0.1], color='black', linewidth=4)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        plt.savefig(filename, bbox_inches='tight', pad_inches=0)
        plt.close(fig)

    def generate_figures(self):
        for i, (variation_type, position) in enumerate(self.variations):
            filename = f'{self.directory}/figure_{i+1}.png'
            if not os.path.exists(filename):
                self.draw_square_with_variation(variation_type, position, filename)
