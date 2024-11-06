import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.widgets import CheckButtons

axes = [5, 5, 5]
data = np.zeros(axes, dtype=np.bool)

# Create figure with space for check buttons
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Disable mouse interaction
ax._button_press = lambda event: None  # Disable pan/zoom
ax._button_release = lambda event: None  # Disable pan/zoom
ax._button_dragging = lambda event: None  # Disable pan/zoom

# Create a separate axes for check buttons
rax = plt.axes([0.02, 0.7, 0.1, 0.2])
check = CheckButtons(rax, ('Layer 1', 'Layer 2', 'Layer 3', 'Layer 4', 'Layer 5'), (True, False, False, False, False))

# Create cubes
for x in range(5):
    for y in range(5):
        for z in range(5):
            data[x, y, z] = True

colors = np.empty(axes + [4], dtype=np.float32)
colors.fill(0)

# Store text objects by layer
text_objects = {
    'Layer 1': [],
    'Layer 2': [],
    'Layer 3': [],
    'Layer 4': [],
    'Layer 5': []
}

# Set initial colors
alpha_selected = 0.3  # Alpha for selected layer
alpha_others = 0.05   # Alpha for other layers

def create_text_objects():
    # Clear existing text objects
    for texts in text_objects.values():
        for text in texts:
            text.remove()
        texts.clear()
    
    # Create new text objects
    count = 1
    for x in range(5):
        for y in range(5):
            for z in range(5):
                text = ax.text(x + 0.5, y + 0.5, z + 0.5, str(count), 
                        horizontalalignment='center',
                        verticalalignment='center',
                        color='black',
                        fontsize=10,
                        fontweight='bold',
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'),
                        zorder=100)
                
                # Store text objects by layer
                layer_num = z + 1
                text_objects[f'Layer {layer_num}'].append(text)
                text.set_visible(False)
                
                count += 1

def update_layer(label):
    # Get all selected layers
    selected_layers = [i+1 for i, status in enumerate(check.get_status()) if status]
    
    # Update colors
    for x in range(5):
        for y in range(5):
            for z in range(5):
                current_layer = z + 1
                if current_layer in selected_layers:
                    colors[x, y, z] = [1, 1, 1, alpha_selected]
                else:
                    colors[x, y, z] = [1, 1, 1, alpha_others]
    
    # Clear and redraw
    ax.clear()
    ax.voxels(data, facecolors=colors, edgecolors='black', linewidth=0.1)
    
    # Recreate text objects
    create_text_objects()
    
    # Show text for all selected layers
    for layer_num in selected_layers:
        for text in text_objects[f'Layer {layer_num}']:
            text.set_visible(True)
    
    # Reset view settings
    ax.view_init(45, 45)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(-1, 6)
    ax.set_ylim(-1, 6)
    ax.set_zlim(-1, 6)
    
    # Disable mouse interaction after redraw
    ax._button_press = lambda event: None
    ax._button_release = lambda event: None
    ax._button_dragging = lambda event: None
    
    fig.canvas.draw_idle()

# Connect the callback
check.on_clicked(update_layer)

# Set initial view
ax.view_init(45, 45)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(-1, 6)
ax.set_ylim(-1, 6)
ax.set_zlim(-1, 6)

# Initial plot with thin lines
ax.voxels(data, facecolors=colors, edgecolors='black', linewidth=0.1)

# Create initial text objects
create_text_objects()

# Show Layer 1 initially
update_layer('Layer 1')

plt.show()