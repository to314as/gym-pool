from setuptools import setup, find_packages


setup(name='gym-pool',
      version='0.1.11',
      url='https://github.com/to314as/gym-pool',
      author='Tobias Oberkofler',
      author_email='tobi20083@gmail.com',
      package_dir={"": "."},
      packages=find_packages(),
      install_requires=['gym>=0.2.3',
                        'numpy',
                        'pygame',
                        'zope.event',
                        'torch',
                        'torchvision'],
      classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent"],
)