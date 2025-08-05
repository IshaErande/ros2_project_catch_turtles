#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from turtlesim.srv import Kill
from functools import partial
import random
import math
from catch_them_all_interfaces.msg import TurtleCoordinates
from catch_them_all_interfaces.msg import TurtleArray
from catch_them_all_interfaces.srv import CatchTurtle
 
 
class spawnTurtleNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("spawn_turtle_node") # MODIFY NAME
        self.name_prefix = "Turtle"
        self.name_counter = 0
        self.alive_turtles = []
        self.aliveTurtlePub = self.create_publisher(TurtleArray , "turtles_alive" , 10)

        self.spawing_time = self.create_timer(2.0 , self.spawn_new_turtle)
        self.catch_turtle_service = self.create_service(CatchTurtle , "catch_turtle" , self.callback_catch_turtle)
    def callback_catch_turtle(self,request , responce):
        self.call_kill_server(request.name)
        responce.success = True
        return responce
    def alive_turtles_pub(self):
        msg = TurtleArray()
        msg.turtles = self.alive_turtles
        self.aliveTurtlePub.publish(msg)
    def spawn_new_turtle(self):
        self.name_counter +=1
        name =  f"Turtle{str(self.name_counter)}"
        self.get_logger().info(f"Spawning turtle {name}")
        x = random.uniform(0.0 , 11.0)
        y = random.uniform(0.0 , 11.0)
        theta = random.uniform(0.0 , 2*math.pi)
        self.call_spawn_server(name ,x,y,theta)

    def call_spawn_server(self ,turtle_name, x ,y , theta):
        client = self.create_client(Spawn , "/spawn")
        while not client.wait_for_service(2.0):
            self.get_logger().warn("waiting for server add to ints")
        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = turtle_name

        future = client.call_async(request)
        future.add_done_callback(partial(self.callBack_call_spawn , x=request.x , y =request.y , theta = request.theta , turtle_name = request.name))

    def callBack_call_spawn(self , future ,turtle_name,x ,y , theta):
        response = future.result()
        if response.name != "":
            self.get_logger().info(f"x = {x} , y = {y} , theta = {theta} , name = {turtle_name} \n")
            self.new_turtle = TurtleCoordinates()
            self.new_turtle.x = x
            self.new_turtle.y = y
            self.new_turtle.theta = theta
            self.new_turtle.name = turtle_name
            self.alive_turtles.append(self.new_turtle)
            self.alive_turtles_pub()

    

    def call_kill_server(self ,turtle_name):
        client = self.create_client(Kill , "/kill")
        while not client.wait_for_service(2.0):
            self.get_logger().warn("waiting for server add to ints")
        request = Kill.Request()
        request.name = turtle_name

        future = client.call_async(request)
        future.add_done_callback(partial(self.callBack_call_kill ,turtle_name = request.name))

    def callBack_call_kill(self , future ,turtle_name):
        future.result()
        self.get_logger().info(f"Killed turtle {turtle_name}")
        for (i, turtle) in enumerate(self.alive_turtles):
            if(turtle.name == turtle_name):
                del self.alive_turtles[i]
                self.alive_turtles_pub()
                break

    
 
 
def main(args=None):
    rclpy.init(args=args)
    node = spawnTurtleNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()