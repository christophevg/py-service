from distutils.core import setup
setup(
  name             = 'servicefactory',
  packages         = [ 'servicefactory' ],
  version          = '0.7',
  description      = 'A highly opinionated and very convention-driven framework for creating Python "services"',
  long_description = "See https://github.com/christophevg/py-servicefactory for more information and examples.",
  author           = 'Christophe VG',
  author_email     = 'contact@christophe.vg',
  url              = 'https://github.com/christophevg/py-servicefactory',
  download_url     = 'https://github.com/christophevg/py-servicefactory/archive/0.7.tar.gz',
  keywords         = [ 'services', 'framework', 'rest', 'api', 'ipc' ],
  classifiers      = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development',
    'License :: OSI Approved :: MIT License',
  ],
  python_requires  = '>=2.7',
  install_requires = [ 'werkzeug', 'requests' ]
)
