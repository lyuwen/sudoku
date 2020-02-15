from setuptools import setup


if __name__ == '__main__':
  name = 'generic-sudoku'
  version = '0.0.1'
  setup(
      name=name,
      version=version,
      description='This is the {} module.'.format(name),
      author='Lyuwen Fu',
      url='https://github.com/lyuwen/sudoku',
      packages=[
        "sudoku",
        ],
      install_requires=[
        "numpy>=1.16.0",
        ],
      provides=[
        "sudoku",
        ],
      python_requires='>=3.6',
      )
