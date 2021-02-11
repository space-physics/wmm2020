project('wmm20', 'c',
  default_options : ['default_library=static', 'buildtype=release', 'warning_level=0'])

os = host_machine.system()
cc = meson.get_compiler('c')
if not ['msvc', 'intel-cl']. contains(cc.get_id()) and not (os == 'windows' and cc.get_id() == 'pgi')
  math_lib = cc.find_library('m')
else
  math_lib = []
endif

geo_lib = library('geo', 'src/GeomagnetismLibrary.c',
  dependencies: math_lib)

wmm15_lib = shared_library('wmm15', 'src/wmm_point_sub.c',
  link_with: geo_lib)

wmm_exe = executable('wmm', 'src/wmm_point.c',
  link_with: geo_lib)
