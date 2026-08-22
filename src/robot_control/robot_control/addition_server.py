import rclpy
from rclpy.node import Node

#at this point, we need to provide the interface we've just defined,
#to add two numbers

# intrface says request (int64, int64)-> return a response of int64
#why does this have to be manually defined the way it is?
#in CMakeLists.txt and then in a robot_interfaces/package.xml?
#nobody knows.


from robot_interfaces.srv import AddTwoInts

class ServerThatDoesAddition(Node):
    def __init__(self):
        super().__init__("server_doing_addition")

        self.service=self.create_service(AddTwoInts, "/add_two_ints", self.addition_callback)
        # type (defined by interface =custom, name=actual name of the service
        #(NOT the name of the topic, or name of a socket or name of TCP channel)

        #and then, specify callback function.
        #whenever request is received, ros acknowledges the event,
        #middleware passes it to rclpy
        #and then rclpy injects "a" and "b" into the addition callback
        #presubably "response" is an empty object of type int64 at this time
        #and then will be populated when "return" hits


    def addition_callback(self, request,response):
        response.sum=request.a+request.b #as defined by the interface (a,b,sum)
        #ros knows that this is the shape of 'request' and 'response' when
        #injecting fata into addition_callback

        self.get_logger().info(f"{request.a}+{request.b}={response.sum}")

        return response


def main():
    rclpy.init()
    node=ServerThatDoesAddition()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__=="__main__":
    main()



