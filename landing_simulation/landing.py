import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped, TwistStamped
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

        # Pose publisher (to send detected marker's pose)
        self.pose_publisher = self.create_publisher(
            PoseStamped, '/drone/aruco_pose', 10)

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

        if ids is not None:
            cv_image = aruco.drawDetectedMarkers(cv_image, corners, ids)

            # Get the pose of the marker (center of the marker in the image)
            for i in range(len(ids)):
                # We can compute the position of the marker based on its corners
                corner = corners[i][0]
                center_x = (corner[0][0] + corner[2][0]) / 2.0  # Convert to float
                center_y = (corner[0][1] + corner[2][1]) / 2.0  # Convert to float

                # Create PoseStamped message
                pose_msg = PoseStamped()
                pose_msg.header.frame_id = 'aruco_marker'
                pose_msg.pose.position.x = float(center_x)  # Ensure it's a float
                pose_msg.pose.position.y = float(center_y)  # Ensure it's a float
                pose_msg.pose.position.z = 0.0  # Assuming flat ground; adjust for height

                # Publish the detected pose
                self.pose_publisher.publish(pose_msg)

        # Display the result
        cv2.imshow('ArUco Marker Detection', cv_image)
        cv2.waitKey(1)


class DroneControllerNode(Node):
    def __init__(self):
        super().__init__('drone_controller_node')
        self.pose_subscriber = self.create_subscription(
            PoseStamped, '/drone/aruco_pose', self.aruco_pose_callback, 10)
        self.offboard_pose_publisher = self.create_publisher(
            PoseStamped, '/mavros/setpoint_position/local', 10)
        self.offboard_velocity_publisher = self.create_publisher(
            TwistStamped, '/mavros/setpoint_velocity/cmd_vel', 10)

        # Thresholds for controlling drone movement
        self.x_threshold = 20.0  # Adjust based on the image resolution
        self.y_threshold = 20.0

        # Target image center
        self.target_x = 320.0  # Assuming image size is 640x480 (center is at 320, 240)
        self.target_y = 240.0

    def aruco_pose_callback(self, pose_msg):
        # Extract the x and y position of the detected marker
        marker_x = pose_msg.pose.position.x
        marker_y = pose_msg.pose.position.y

        # Compute the difference between marker center and image center
        error_x = marker_x - self.target_x
        error_y = marker_y - self.target_y

        # If the marker is not centered, send velocity commands to move the drone
        if abs(error_x) > self.x_threshold or abs(error_y) > self.y_threshold:
            self.publish_offboard_control(error_x, error_y)
        else:
            # If the drone is over the marker, descend
            if pose_msg.pose.position.z > 0.5:  # Still above the ground
                self.publish_descent_control()

    def publish_offboard_control(self, error_x, error_y):
        # 속도 제어 메시지 생성
        twist_msg = TwistStamped()

        # x, y 방향의 이동을 제어 (error_x, error_y에 비례)
        twist_msg.twist.linear.x = -0.01 * error_x  # Adjust this gain as needed
        twist_msg.twist.linear.y = -0.01 * error_y  # Adjust this gain as needed

        twist_msg.twist.linear.z = 0.0  # hovers at the same altitude
        twist_msg.twist.angular.z = 0.0  # yaw 제어

        self.offboard_velocity_publisher.publish(twist_msg)

    def publish_descent_control(self):
        # 하강 제어 메시지 생성
        twist_msg = TwistStamped()
        twist_msg.twist.linear.x = 0.0  # 전방 속도
        twist_msg.twist.linear.y = 0.0  # 측면 속도
        twist_msg.twist.linear.z = -0.2  # 하강 속도

        twist_msg.twist.angular.z = 0.0  # yaw 제어
        self.offboard_velocity_publisher.publish(twist_msg)
        

def main(args=None):
    rclpy.init(args=args)

    # Instantiate both the marker detector and drone controller
    detector = ArucoMarkerDetector()
    controller = DroneControllerNode()

    # Create a multithreaded executor to handle both nodes
    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(detector)
    executor.add_node(controller)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass

    detector.destroy_node()
    controller.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
