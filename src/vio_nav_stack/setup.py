from setuptools import setup
import os
from glob import glob

package_name = 'vio_nav_stack'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yogesh',
    maintainer_email='yogesh@example.com',
    description='Vision-Inertial Odometry and AI Obstacle Avoidance for Project Zenith.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'obstacle_avoidance = vio_nav_stack.obstacle_avoidance:main',
            'perception_simulator = vio_nav_stack.perception_simulator:main',
        ],
    },
)
