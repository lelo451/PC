cmake_minimum_required(VERSION 3.23)
project(PC)

set(CMAKE_CXX_STANDARD 23)
# Add PTHREAD packet to project
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")

# Add MPI Package to Project
#find_package(MPI REQUIRED)

add_executable(PC knn_pthread.cpp knn_mpi.cpp)

# Add libraries for code completion and compiling
#target_link_libraries(PC PUBLIC MPI::MPI_CXX)
