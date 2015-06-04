from setuptools import setup


setup(name='short',
      version='0.2',
      description='Simple url shorter',
      classifiers=[
          "License :: OSI Approved :: BSD License",
          "Operating System :: POSIX",
          "Programming Language :: Python :: 3.4",
          "Topic :: Internet :: WWW/HTTP",
      ],
      author='Alexander Zelenyak',
      author_email='zzz.sochi@gmail.com',
      license='BSD',
      url='https://github.com/zzzsochi/short',
      keywords=['asyncio', 'aiohttp', 'traversal'],
      packages=['short'],
      install_requires=[
          'aiohttp',
          'aiohttp_traversal',
          'aioredis',
      ],
      tests_require=['pytest'],
      entry_points={
          'console_scripts': [
              'short = short.__main__:main',
          ],
      },
)
