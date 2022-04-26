## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

#For rubbermaid lid: 0-4, 160-255, 29-128
#pants: 0-180, 121-255, 184-255

from __future__ import print_function
import pyrealsense2 as rs
import numpy as np
import cv2

from builtins import input
from numpy.linalg import norm

from run_code import Bot
import keyboard

COMPORT = 'COM12'
start_robot = False
# from adjust_brightness.py import adjust_brightness


def brightness(img):
    if len(img.shape) == 3:
        # Colored RGB or BGR (*Do Not* use HSV images with this function)
        # create brightness with euclidean norm
        return np.average(norm(img, axis=2)) / np.sqrt(3)
    else:
        # Grayscale
        return np.average(img)


##### main #####
def adjust_brightness(image):
    # image = cv.imread('Frame01.jpg')
    if image is None:
        print('Could not open or find the image')
        exit(0)


    new_image = np.zeros(image.shape, image.dtype)


    alpha = 1.0 # Simple contrast control
    #beta = 50   # Simple brightness control

    ####adjustable brightness control####

    #check for actual brightness of the image
    brightness_img = brightness(image)
    # print(brightness_img)

    # goal brightness is =
    goal_bn = 120
    beta = goal_bn - brightness_img  #overwrite brightness


    # Do the operation new_image(i,j) = alpha*image(i,j) + beta
    # Instead of these 'for' loops we could have used simply:
    # new_image = cv.convertScaleAbs(image, alpha=alpha, beta=beta)
    # but we wanted to show you how to access the pixels :)

    new_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
  #  print('old_image', brightness_img, 'new_image', brightness(new_image))
    return new_image



def main():
    start_robot = False
    #initialize Bot
    bot = Bot(COMPORT)
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()

    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    device_product_line = str(device.get_info(rs.camera_info.product_line))

    found_rgb = False
    for s in device.sensors:
        if s.get_info(rs.camera_info.name) == 'RGB Camera':
            found_rgb = True
            break
    if not found_rgb:
        print("The demo requires Depth camera with Color sensor")
        exit(0)

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start streaming
    profile = pipeline.start(config)

    # define a null callback function for Trackbar
    def null(x):
        pass

    # create six trackbars for H, S and V - lower and higher masking limits
    cv2.namedWindow('HSV')
    # arguments: trackbar_name, window_name, default_value, max_value, callback_fn
    cv2.createTrackbar("HL", "HSV", 0, 180, null)
    cv2.createTrackbar("HH", "HSV", 180, 180, null)
    cv2.createTrackbar("SL", "HSV", 192, 255, null)
    cv2.createTrackbar("SH", "HSV", 255, 255, null)
    cv2.createTrackbar("VL", "HSV", 0, 255, null)
    cv2.createTrackbar("VH", "HSV", 213, 255, null)

    0-180, 121-255, 184-255

    align_to = rs.stream.color
    align = rs.align(align_to)
    last_bin = 0


    try:
        while True:

            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            img = adjust_brightness(color_image)

            # convert BGR image to HSV
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # read the Trackbar positions
            hl = cv2.getTrackbarPos('HL','HSV')
            hh = cv2.getTrackbarPos('HH','HSV')
            sl = cv2.getTrackbarPos('SL','HSV')
            sh = cv2.getTrackbarPos('SH','HSV')
            vl = cv2.getTrackbarPos('VL','HSV')
            vh = cv2.getTrackbarPos('VH','HSV')

            # create a manually controlled mask
            # arguments: hsv_image, lower_trackbars, higher_trackbars
            mask = cv2.inRange(hsv, np.array([hl, sl, vl]), np.array([hh, sh, vh]))

            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # c = max(contours, )
            #draw the obtained contour lines(or the set of coordinates forming a line) on the original image

            # derive masked image using bitwise_and method
            final = cv2.bitwise_and(img, img, mask=mask)
            # depth_frame = cv2.bitwise_and(depth_image, depth_image, mask=mask)
            # distance = np.mean(np.nonzero(depth_frame))
            # print(distance)

            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

            depth_colormap_mask = cv2.bitwise_and(depth_colormap, depth_colormap, mask=mask)
            color_image_mask = cv2.bitwise_and(color_image, color_image, mask=mask)
            color_image_mask = cv2.morphologyEx(color_image_mask, cv2.MORPH_OPEN, kernel) #Erosion-dilation
            try:
                cv2.drawContours(color_image_mask, max(contours, key = cv2.contourArea), -1, (0,255,0), 3)
            except:
                t = 0
                # print("error")

            depth_colormap_dim = depth_colormap.shape
            color_colormap_dim = color_image.shape

            # calculate moments of binary image
            M = cv2.moments(mask)
            # calculate x,y coordinate of center
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
                # print(depth_scale)
                box_size = 10
                sum = 0
                for x in range(-box_size, box_size):
                    for y in range(-box_size, box_size):
                        pX = cX + x
                        pY = cY + y
                        if pX <= 0:
                            pX = 1
                        if pY <= 0:
                            pY = 1
                        if pX >= depth_image.shape[1]:
                            pX = depth_image.shape[1] - 1
                        if pY >= depth_image.shape[0]:
                            pY = depth_image.shape[0] - 1
                        dist_pixel = depth_frame.get_distance(pX, pY)
                        sum += dist_pixel
                dist_ave = sum / (box_size*2)**2
                depth_colormap = cv2.rectangle(depth_colormap, (cX-box_size, cY-box_size), (cX+box_size, cY+box_size), (255,0,0),2)
                # put text and highlight the center
                cv2.circle(color_image_mask, (cX, cY), 5, (255, 255, 255), -1)
                cv2.putText(color_image_mask, str(dist_ave), (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            else:
                bin_centroid = 5
                dist_ave = 1
                cX = 320
            # If depth and color resolutions are different, resize color image to match depth image for display
            if depth_colormap_dim != color_colormap_dim:
                resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
                images = np.hstack((resized_color_image, depth_colormap))
            else:
                images = np.hstack((color_image_mask, depth_colormap))


            # display image, mask and masked_image
            cv2.imshow('Original', img)
            cv2.imshow('Mask', mask)
            cv2.imshow('Masked Image', final)
            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', images)


            key = cv2.waitKey(10) & 0xFF
            if key == ord('q'):
                break

            if keyboard.is_pressed('s'):
                print('starting robot')
                start_robot = True


            bins = depth_image.shape[1] / 10
            bin_centroid = int((cX + 5) / bins)
            if np.sum(mask) / 255 < 30000:
                if last_bin < 5:
                    print('right')
                    bin_centroid = -1
                if last_bin > 5:
                    print('left')
                    bin_centroid = 11

            if start_robot:
                # print(bin_centroid, dist_ave)
                bot.drive(bin_centroid, dist_ave)
            last_bin = bin_centroid


        cv2.destroyAllWindows()


    finally:

        # Stop streaming
        pipeline.stop()

if __name__ == '__main__':
    main()
