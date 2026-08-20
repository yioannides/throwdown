pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'throwdown'
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'gtk/shortcuts-dialog.blp',
    'gtk/window.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile','@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('throwdown',
  'throwdown.gresource.xml',
  dependencies: blueprints,
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'throwdown.in',
  output: 'throwdown',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x'
)

throwdown_sources = [
  '__init__.py',
  'main.py',
  'randomizer.py',
  'window.py',
]

install_data(throwdown_sources, install_dir: moduledir)
install_data('assets/tricks.json', install_dir: moduledir)
