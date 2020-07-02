cmake_minimum_required(VERSION 3.12)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Debug or Release" FORCE)
endif()
project(wmm LANGUAGES C)
enable_testing()

add_library(geo src/GeomagnetismLibrary.c)
set_target_properties(geo PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
if((NOT MSVC) AND
    NOT (WIN32 AND (CMAKE_C_COMPILER_ID STREQUAL Intel OR
                    CMAKE_C_COMPILER_ID STREQUAL PGI)))
  target_link_libraries(geo m)
endif()

add_library(wmm15 SHARED src/wmm_point_sub.c)
target_link_libraries(wmm15 PRIVATE geo)

add_executable(wmm src/wmm_point.c)
target_link_libraries(wmm geo)
