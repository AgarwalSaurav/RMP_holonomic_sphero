cmake_minimum_required(VERSION 3.0.2)
project(rviz_polygon_env)

## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++1z)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  visualization_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES rviz_polygon_env
#  CATKIN_DEPENDS roscpp visualization_msgs
#  DEPENDS system_lib
)

include_directories(
	include
  ${catkin_INCLUDE_DIRS}
)

add_executable(draw_polygon_env src/draw_polygon_env.cpp)
target_link_libraries(draw_polygon_env ${catkin_LIBRARIES})
