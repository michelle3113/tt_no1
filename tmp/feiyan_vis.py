from skimage import measure
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def HU2uint8(image, HU_min=-1200.0, HU_max=600.0, HU_nan=-2000.0):
    """
    Convert HU unit into uint8 values. First bound HU values by predfined min
    and max, and then normalize
    image: 3D numpy array of raw HU values from CT series in [z, y, x] order.
    HU_min: float, min HU value.
    HU_max: float, max HU value.
    HU_nan: float, value for nan in the raw CT image.
    """
    image_new = np.array(image)
    image_new[np.isnan(image_new)] = HU_nan

    # normalize to [0, 1]
    image_new = (image_new - HU_min) / (HU_max - HU_min)
    image_new = np.clip(image_new, 0, 1)
    image_new = (image_new * 255).astype('uint8')

    return image_new

def plot_3d(image, threshold=-300):
    # Position the scan upright,
    # so the head of the patient would be at the top facing the camera
    p = image.transpose(2, 1, 0)

    verts, faces, norm, val = measure.marching_cubes_lewiner(p, threshold)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Fancy indexing: `verts[faces]` to generate a collection of triangles
    mesh = Poly3DCollection(verts[faces], alpha=0.70)
    face_color = [0.45, 0.45, 0.75]
    mesh.set_facecolor(face_color)
    ax.add_collection3d(mesh)

    ax.set_xlim(0, p.shape[0])
    ax.set_ylim(0, p.shape[1])
    ax.set_zlim(0, p.shape[2])

    plt.show()


if __name__ == '__main__':
    filename = 'C:\\Users\\yifan\\Desktop\\feiyan\\tmp\\1.npy'
    volume = np.load(filename)
    plot_3d(volume, 0)

    # volume_vis = HU2uint8(volume)
    # plt.imshow(volume_vis[10], cmap=plt.cm.gray)
    # plt.show()

    pass
