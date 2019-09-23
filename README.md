# rotation_angle_detection_image_processing

When you run the program, it gives you the rotation angle of the object encircles either a hexagon or a circle. The python script is coded in Jupyter Notebook using OpenCV.

To run python file called nut_angle_detection.py, please use a similar format to the following one: (specify an image name after --image)
python hexagon_circle_detection.py --image 10-11-2017-9.38.49_18.bmp

I used cv2.HoughCircles and cv2.grabCut to get rid of the background. After finding contour of s shaped object, I define a rectangle outside of it to determine the rotation angle. 
The output comes with a negative sign, this means rotation defined by clockwise direction.

One sample outcome is attached:

![angle_detection](https://github.com/mandalinadagi/rotation_angle_detection_image_processing/blob/master/angle_detection.png)

In case of any problem, please contact me via this e-mail address: mandalinadagi@gmail.com

Thank you- 
