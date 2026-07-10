cmake_minimum_required(VERSION 3.10)
project(EdgeGuardEngine)

set(CMAKE_CXX_STANDARD 17)

# Set ONNX Runtime path (use environment or default to /opt/onnxruntime)
if(NOT DEFINED ONNXRUNTIME_DIR)
    set(ONNXRUNTIME_DIR "/opt/onnxruntime")
endif()

# Include headers
include_directories(${ONNXRUNTIME_DIR}/include)

# Link library directory
link_directories(${ONNXRUNTIME_DIR}/lib)

# Create executable
add_executable(edge_guard_engine main.cpp)

# Link ONNX Runtime
target_link_libraries(edge_guard_engine onnxruntime)
