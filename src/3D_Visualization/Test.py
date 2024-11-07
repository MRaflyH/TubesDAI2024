import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.widgets import CheckButtons, RadioButtons

axes = [5, 5, 5]
data = np.zeros(axes, dtype=np.bool)

# Create figure with space for check buttons and plane selection
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Disable mouse interaction
ax._button_press = lambda event: None
ax._button_release = lambda event: None
ax._button_dragging = lambda event: None

# Create separate axes for check buttons and plane selection
check_ax = plt.axes([0.02, 0.7, 0.1, 0.2])
plane_ax = plt.axes([0.02, 0.5, 0.1, 0.1])

# Store selected layers for each plane orientation
plane_selections = {
    'XY Plane': [True, False, False, False, False],
    'XZ Plane': [True, False, False, False, False],
    'YZ Plane': [True, False, False, False, False]
}

# Create check buttons for layers and radio buttons for plane selection
check = CheckButtons(check_ax, ('Layer 1', 'Layer 2', 'Layer 3', 'Layer 4', 'Layer 5'), plane_selections['XY Plane'])
plane_radio = RadioButtons(plane_ax, ('XY Plane', 'XZ Plane', 'YZ Plane'))

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
alpha_selected = 0.3
alpha_others = 0.05

current_plane = 'XY Plane'

def create_text_objects():
    # Clear existing text objects
    for texts in text_objects.values():
        for text in texts:
            text.remove()
        texts.clear()
    
    # Create new text objects based on current plane orientation
    count = 1
    for x in range(5):
        for y in range(5):
            for z in range(5):
                # Adjust position based on plane orientation
                if current_plane == 'XY Plane':
                    layer_num = z + 1
                elif current_plane == 'XZ Plane':
                    layer_num = y + 1
                else:  # YZ Plane
                    layer_num = x + 1
                
                text = ax.text(x + 0.5, y + 0.5, z + 0.5, str(count), 
                        horizontalalignment='center',
                        verticalalignment='center',
                        color='black',
                        fontsize=10,
                        fontweight='bold',
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'),
                        zorder=100)
                
                text_objects[f'Layer {layer_num}'].append(text)
                text.set_visible(False)
                
                count += 1

def get_layer_number(x, y, z):
    if current_plane == 'XY Plane':
        return z + 1
    elif current_plane == 'XZ Plane':
        return y + 1
    else:  # YZ Plane
        return x + 1

def update_view():
    # Save current selections
    plane_selections[current_plane] = list(check.get_status())
    
    selected_layers = [i+1 for i, status in enumerate(check.get_status()) if status]
    
    # Update colors based on selected layers and current plane
    for x in range(5):
        for y in range(5):
            for z in range(5):
                layer_num = get_layer_number(x, y, z)
                if layer_num in selected_layers:
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
    
    # Set view angle based on plane
    if current_plane == 'XY Plane':
        ax.view_init(45, 45)
    elif current_plane == 'XZ Plane':
        ax.view_init(0, 45)
    else:  # YZ Plane
        ax.view_init(45, 0)
    
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

def update_layer(label):
    update_view()

def update_plane(label):
    global current_plane
    current_plane = label
    
    # Load saved selections for the new plane
    saved_selections = plane_selections[current_plane]
    
    # Update checkboxes to match saved selections
    current_selections = check.get_status()
    for i in range(5):
        if current_selections[i] != saved_selections[i]:
            check.set_active(i)
    
    update_view()

# Connect callbacks
check.on_clicked(update_layer)
plane_radio.on_clicked(update_plane)

# Initial setup
ax.view_init(45, 45)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(-1, 6)
ax.set_ylim(-1, 6)
ax.set_zlim(-1, 6)

# Initial plot
ax.voxels(data, facecolors=colors, edgecolors='black', linewidth=0.1)
create_text_objects()
update_view()

plt.show()