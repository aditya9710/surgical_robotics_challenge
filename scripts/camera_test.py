#!/usr/bin/env python
from __future__ import print_function

import cPickle
import roslib
# roslib.load_manifest('my_package')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("imageFromROS",Image,queue_size=10)

    self.bridge = CvBridge()
    self.image_subL = rospy.Subscriber("/ambf/env/cameras/cameraL/ImageData",Image,self.callbackL)
    self.image_subR = rospy.Subscriber("/ambf/env/cameras/cameraR/ImageData",Image, self.callbackR)
    self.cvmsg_L = []
    self.cvmsg_R = []

  def callbackL(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    # self.cvmsg_L.append(cv_image)

    # print(type(cv_image))
    # print(cv_image.shape)
    # print(cv_image)

    (rows,cols,channels) = cv_image.shape
    if cols > 60 and rows > 60 :
      cv2.circle(cv_image, (50,50), 10, 255)

    #cv2.startWindowThread()
    cv2.namedWindow("Image window Left")
    cv2.imshow("Image window Left", cv_image)
    cv2.waitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

  def callbackR(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    # self.cvmsg_R.append(cv_image)

    (rows,cols,channels) = cv_image.shape
    if cols > 60 and rows > 60 :
      cv2.circle(cv_image, (50,50), 10, 255)

    #cv2.startWindowThread()
    cv2.namedWindow("Image window Right")
    cv2.imshow("Image window Right", cv_image)
    cv2.waitKey(0)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

def main(args):
  ic = image_converter()
  # cv_msg_L = ic.cvmsg_L
  # cv_msg_R = ic.cvmsg_R
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  # cv2.destroyAllWindows()

  # return cv_msg_L,cv_msg_R

if __name__ == '__main__':
    # msg_l, msg_r = main(sys.argv)

    # a_msg = [msg_l, msg_r]
    # main(sys.argv)

    # with open('cvmsg_R.pickle','w') as fp:
    #     cPickle.dump(a_msg,fp)
    #     fp.close()

    with open('cvmsg_R.pickle','r') as fp:
        itemlist = cPickle.load(fp)
