import cv2 as cv
import numpy as np
from skimage import transform
from skimage import feature
from matplotlib import pyplot as plt

imagN = cv.imread('imag1.jpg', cv.IMREAD_GRAYSCALE) # CARGANDO IMAGEN NATURAL

# modifing natural image
imagN_rot = transform.rotate(imagN,180) #rotation
tform = transform.AffineTransform(scale=(1.5,1), rotation=0.5, translation=(0, -200))
imagN_aff = transform.warp(imagN, tform) #Affine

# ORB decriptor in original
ORB_descriptor = feature.ORB(n_keypoints=200)
ORB_descriptor.detect_and_extract(imagN)
keypts1 = ORB_descriptor.keypoints
decript1 = ORB_descriptor.descriptors

# ORB descriptor in rotate
ORB_descriptor.detect_and_extract(imagN_rot)
keypts2 = ORB_descriptor.keypoints
decript2 = ORB_descriptor.descriptors

# ORB descriptor in Affine
ORB_descriptor.detect_and_extract(imagN_aff)
keypts3 = ORB_descriptor.keypoints
decript3 = ORB_descriptor.descriptors

# find matches
matches12 = feature.match_descriptors(decript1, decript2)
matches13 = feature.match_descriptors(decript1, decript3)

fig, ax = plt.subplots(nrows=2, ncols=1)
feature.plot_matches(ax[0], imagN, imagN_rot, keypts1, keypts2, matches12)
ax[0].set_title('Original vs Rotate')
feature.plot_matches(ax[1], imagN, imagN_aff, keypts1, keypts3, matches13)
ax[1].set_title('Original vs Affine')

plt.show()

imagS = cv.imread('dibujo.png', cv.IMREAD_GRAYSCALE) # CARGANDO IMAGEN SINTÉTICA

# modifing synthetic image
imagS_rot = transform.rotate(imagS,180) #rotation
tform = transform.AffineTransform(scale=(2,1.5), rotation=0.5, translation=(0, -200))
imagS_aff = transform.warp(imagS, tform) #Affine

# ORB decriptor for synthetic
ORB_descriptor.detect_and_extract(imagS)
keypts1 = ORB_descriptor.keypoints
decript1 = ORB_descriptor.descriptors

# ORB descriptor in rotate
ORB_descriptor.detect_and_extract(imagS_rot)
keypts2 = ORB_descriptor.keypoints
decript2 = ORB_descriptor.descriptors

# ORB descriptor in Affine
ORB_descriptor.detect_and_extract(imagS_aff)
keypts3 = ORB_descriptor.keypoints
decript3 = ORB_descriptor.descriptors

# find matches
matches12 = feature.match_descriptors(decript1, decript2)
matches13 = feature.match_descriptors(decript1, decript3)

fig, ax = plt.subplots(nrows=2, ncols=1)
feature.plot_matches(ax[0], imagS, imagS_rot, keypts1, keypts2, matches12)
ax[0].set_title('Original vs Rotate')
feature.plot_matches(ax[1], imagS, imagS_aff, keypts1, keypts3, matches13)
ax[1].set_title('Original vs Affine')

plt.show()