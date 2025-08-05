#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math
from catch_them_all_interfaces.msg import TurtleCoordinates
from catch_them_all_interfaces.msg import TurtleArray
from catch_them_all_interfaces.srv import CatchTurtle
from functools import partial
from turtlesim.srv import SetPen
 
 
class turtleControllerNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("turtle_controller") # MODIFY NAME
        self.target_x = 1.0
        self.target_y = 4.0

        self.turtle_to_catch = None
        self.sub_Pose = self.create_subscription(Pose , "turtle1/pose" , self.callBackPoseSubscriber , 10)
        self.sub_spawn_turtle = self.create_subscription(TurtleArray , "turtles_alive" , self.callback_spawner_sub , 10)
        self.pub_cmdvel = self.create_publisher(Twist , "turtle1/cmd_vel" , 10)
        self.create_timer(0.01  , self.callbackTwistPublisher)
        self.pose = None
        self.call_set_pen_service(69 , 86 , 255 , 1 ,1)

    def call_set_pen_service(self , r ,g ,b , width , off):
        client = self.create_client(SetPen , "/turtle1/set_pen")
        while not client.wait_for_service(1.0):
            self.get_logger.warn("waiting for service...")

        self.request1 = SetPen.Request()
        self.request1.r = r
        self.request1.g = g
        self.request1.b = b
        self.request1.width = width
        self.request1.off = off

        future = client.call_async(self.request1)
        future.add_done_callback(partial(self.callback_set_pen))

    def callback_set_pen(self , future):
        try:
           response = future.result()
        except Exception as e:
            self.get_logger().error("service failed: %r"(e,))

    def callback_spawner_sub(self , msg):
        if(len(msg.turtles) >0):
            self.turtle_to_catch = msg.turtles[0]
    def callBackPoseSubscriber(self , msg):
        self.pose = msg
    def callbackTwistPublisher(self):
        if(self.pose == None or self.turtle_to_catch == None):
            return
        
        self.error_x = self.turtle_to_catch.x - self.pose.x 
        self.error_y = self.turtle_to_catch.y - self.pose.y 
        dist = math.sqrt((self.error_x*self.error_x)+(self.error_y*self.error_y))

        self.msg = Twist()       

        if(dist > 0.5):
            self.msg.linear.x = 2*dist

            fin_angle = math.atan2(self.error_y , self.error_x)
            error_ang = fin_angle - self.pose.theta

            if(error_ang > math.pi):
                error_ang -= 2* math.pi
            elif (error_ang< -math.pi):
                error_ang += 2*math.pi

            self.msg.angular.z = 6*error_ang
        else:
            
            self.msg.linear.x = 0.0
            self.msg.angular.z = 0.0
            self.call_catch_turtle_server(self.turtle_to_catch.name)
            self.turtle_to_catch = None
        self.pub_cmdvel.publish(self.msg)
    
    def call_catch_turtle_server(self ,turtle_name):
        client = self.create_client(CatchTurtle , "catch_turtle")
        while not client.wait_for_service(2.0):
            self.get_logger().warn("waiting for server add to ints")
        request = CatchTurtle.Request()
        request.name = turtle_name

        future = client.call_async(request)
        future.add_done_callback(partial(self.callBack_call_catch_turtle ,turtle_name = request.name))

    def callBack_call_catch_turtle(self , future ,turtle_name):
        responce = future.result()
        if not responce.success:
            self.get_logger().error("catch turtle failed")
            pass
        
 
 
def main(args=None):
    rclpy.init(args=args)
    node = turtleControllerNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()