import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import cv2.aruco as aruco

class ArucoMarkerDetector(Node):
    def __init__(self):
        super().__init__('aruco_marker_detector')

        # Create a CvBridge object
        self.bridge = CvBridge()

        # Subscribe to the camera image topic
        self.image_sub = self.create_subscription(
            Image,
            '/downward_camera/image_raw',  # Gazebo에서 퍼블리시되는 카메라 토픽 이름
            self.image_callback,
            10)

        # ArUco marker dictionary
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_1000)
        self.parameters = aruco.DetectorParameters_create()

        # Window to display the results
        cv2.namedWindow('ArUco Marker Detection')

    def image_callback(self, data):
        # Log to indicate the callback was triggered
        self.get_logger().info('Image received')

        # Convert ROS Image message to OpenCV image
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
        except CvBridgeError as e:
            self.get_logger().error(f'CvBridge Error: {e}')
            return

        # Convert the image to grayscale
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Detect ArUco markers
        corners, ids, rejected = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)

        # Draw detected markers on the image
        if ids is not None:
            cv_image = aruco.drawDetectedMarkers(cv_image, corners, ids)

        # Display the result
        cv2.imshow('ArUco Marker Detection', cv_image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    detector = ArucoMarkerDetector()
    
    try:
        rclpy.spin(detector)
    except KeyboardInterrupt:
        pass
    
    detector.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

