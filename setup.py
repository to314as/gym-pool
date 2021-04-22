from setuptools import setup

setup(name='gym_pool',
      version='0.0.1',
      url='https://github.com/to314as/gym-pool',
      author='Tobias Oberkofler',
      author_email='tobi20083@gmail.com',
      py_modules=['gym-pool'],
      install_requires=['gym>=0.2.3',
                        'numpy',
                        'pygame',
                        'zope.event',
                        'torch',
                        'torchvision']
)