from distutils.core import setup

setup(
    name='crowdflower-fdw',
    version='1.0',
    author='Ilja Everilä',
    author_email='saarni@gmail.com',
    maintainer='Ilja Everilä',
    maintainer_email='saarni@gmail.com',
    url='http://github.com/everilae/crowdflower-fdw',
    description='PostgreSQL foreign data wrapper for CrowdFlower.',
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    requires=[
        'requests',
        'multicorn',
    ],
    packages=['crowdflower_fdw'],
)
