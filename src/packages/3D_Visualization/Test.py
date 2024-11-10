import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.widgets import CheckButtons, RadioButtons
from ..adt.magicCube import buildRandomMagicCube, printMagicCube

def visualizeCube(magicCube):
    axes = [5, 5, 5]
    data = np.zeros(axes, dtype=np.bool)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    check_ax = plt.axes([0.02, 0.7, 0.1, 0.2])
    plane_ax = plt.axes([0.02, 0.5, 0.1, 0.1])

    plane_selections = {
        'XY Plane': [True, False, False, False, False],
        'XZ Plane': [True, False, False, False, False],
        'YZ Plane': [True, False, False, False, False]
    }

    check = CheckButtons(check_ax, ('Layer 1', 'Layer 2', 'Layer 3', 'Layer 4', 'Layer 5'), plane_selections['XY Plane'])
    plane_radio = RadioButtons(plane_ax, ('XY Plane', 'XZ Plane', 'YZ Plane'))

    for x in range(5):
        for y in range(5):
            for z in range(5):
                data[x, y, z] = True

    colors = np.empty(axes + [4], dtype=np.float32)
    colors.fill(0)

    text_objects = {
        'Layer 1': [],
        'Layer 2': [],
        'Layer 3': [],
        'Layer 4': [],
        'Layer 5': []
    }

    alpha_selected = 0.3
    alpha_others = 0.05

    current_plane = 'XY Plane'

    def create_text_objects(magicCube):
        for texts in text_objects.values():
            for text in texts:
                text.remove()
            texts.clear()
        
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    index = x + (y*5) + (z*25)
                    value = magicCube[index]  
                    
                    if current_plane == 'XY Plane':
                        layer_num = z + 1
                    elif current_plane == 'XZ Plane':
                        layer_num = y + 1
                    else:  
                        layer_num = x + 1
                    
                    text = ax.text(x + 0.5, y + 0.5, z + 0.5, str(value), 
                            horizontalalignment='center',
                            verticalalignment='center',
                            color='black',
                            fontsize=10,
                            fontweight='bold',
                            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'),
                            zorder=100)
                    
                    text_objects[f'Layer {layer_num}'].append(text)
                    text.set_visible(False)

    def get_layer_number(x, y, z):
        if current_plane == 'XY Plane':
            return z + 1
        elif current_plane == 'XZ Plane':
            return y + 1
        else:  
            return x + 1

    def update_view():
        nonlocal current_plane
        plane_selections[current_plane] = list(check.get_status())
        
        selected_layers = [i+1 for i, status in enumerate(check.get_status()) if status]
        
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    layer_num = get_layer_number(x, y, z)
                    if layer_num in selected_layers:
                        colors[x, y, z] = [1, 1, 1, alpha_selected]
                    else:
                        colors[x, y, z] = [1, 1, 1, alpha_others]
        
        ax.clear()
        ax.voxels(data, facecolors=colors, edgecolors='black', linewidth=0.1)
        
        create_text_objects(magicCube)
        
        for layer_num in selected_layers:
            for text in text_objects[f'Layer {layer_num}']:
                text.set_visible(True)
        
        if current_plane == 'XY Plane':
            ax.view_init(45, 45)
        elif current_plane == 'XZ Plane':
            ax.view_init(0, 45)
        else:  
            ax.view_init(45, 0)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim(-1, 6)
        ax.set_ylim(-1, 6)
        ax.set_zlim(-1, 6)
        
        ax._button_press = lambda event: None
        ax._button_release = lambda event: None
        ax._button_dragging = lambda event: None
        
        fig.canvas.draw_idle()

    def update_layer(label):  # Added label parameter
        update_view()

    def update_plane(label):
        nonlocal current_plane
        current_plane = label
        
        saved_selections = plane_selections[current_plane]
        
        current_selections = check.get_status()
        for i in range(5):
            if current_selections[i] != saved_selections[i]:
                check.set_active(i)
        
        update_view()

    check.on_clicked(update_layer)
    plane_radio.on_clicked(update_plane)

    ax.view_init(45, 45)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(-1, 6)
    ax.set_ylim(-1, 6)
    ax.set_zlim(-1, 6)

    ax.voxels(data, facecolors=colors, edgecolors='black', linewidth=0.1)
    create_text_objects(magicCube)
    update_view()

    plt.show()


if __name__ == "__main__":
    test = buildRandomMagicCube()
    print(test)
    printMagicCube(test)
    visualizeCube(test)