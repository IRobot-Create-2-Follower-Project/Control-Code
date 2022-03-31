from __future__ import print_function
from builtins import input
import cv2 as cv
import numpy as np
from numpy.linalg import norm


###########  utils ###########

def brightness(img):
    if len(img.shape) == 3:
        # Colored RGB or BGR (*Do Not* use HSV images with this function)
        # create brightness with euclidean norm
        return np.average(norm(img, axis=2)) / np.sqrt(3)
    else:
        # Grayscale
        return np.average(img)


##### main #####

image = cv.imread('Frame01.jpg')
if image is None:
    print('Could not open or find the image')
    exit(0)


new_image = np.zeros(image.shape, image.dtype)


alpha = 1.0 # Simple contrast control
#beta = 50   # Simple brightness control

####adjustable brightness control####

#check for actual brightness of the image
brightness_img = brightness(image)
print(brightness_img)

# goal brightness is =
goal_bn = 120
beta = goal_bn - brightness_img  #overwrite brightness


# Do the operation new_image(i,j) = alpha*image(i,j) + beta
# Instead of these 'for' loops we could have used simply:
# new_image = cv.convertScaleAbs(image, alpha=alpha, beta=beta)
# but we wanted to show you how to access the pixels :)

new_image = cv.convertScaleAbs(image, alpha=alpha, beta=beta)


# Show stuff
cv.imshow('Original Image', image)
cv.imshow('New Image', new_image)

# Wait until user press some key
cv.waitKey()


