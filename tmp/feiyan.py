import SimpleITK as sitk
import numpy as np
import os.path as osp

if __name__ == '__main__':
    filename = 'D:\\迅雷下载\\LUNA16\\LUNA16\\0\\0.mhd'
    if osp.exists(filename):
        print('find it!!!')
    else:
        print('not find it!!!')
    itkimage = sitk.ReadImage(filename)
    numpyImage = sitk.GetArrayFromImage(itkimage)

    numpyOrigin = np.array(list(reversed(itkimage.GetOrigin())))
    numpySpacing = np.array(list(reversed(itkimage.GetSpacing())))
    pass
