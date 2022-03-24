import cv2


# define a video capture object
# Opens the inbuilt camera of laptop to capture video.
vid = cv2.VideoCapture(0)
i = 0

while(True):
#while(vid.isOpened()):

    # Capture the video frame by frame
    ret, frame = vid.read()

    # This condition prevents from infinite looping incase video ends.
    if ret == False:
        break

    # Save Frame by Frame into disk using imwrite method - save every nth frame
    n = 10
    if i%n ==0:
        cv2.imwrite('Frame'+str(i)+'.jpg', frame)
    i += 1

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()



