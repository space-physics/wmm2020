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

add_library(wmm20 SHARED src/wmm_point_sub.c)
target_link_libraries(wmm20 PRIVATE geo)

# https://www.ngdc.noaa.gov/geomag/WMM/data/WMM2020/WMM2020testvalues.pdf
add_executable(wmm20_file src/wmm_file.c)
target_link_libraries(wmm20_file geo)

if(APPLE)
# wmm_file.c has bug from original authors on MacOS
  add_test(NAME MacOS-noop COMMAND "ls")
else()
  add_test(NAME WMM20file
  COMMAND $<TARGET_FILE:wmm20_file> f ${CMAKE_CURRENT_SOURCE_DIR}/test_input.asc  ${CMAKE_CURRENT_BINARY_DIR}/test_output.asc
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
endif()
