from setuptools import setup
import os
from glob import glob

package_name = 'chronos_inspector'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yogesh',
    maintainer_email='yogesh@example.com',
    description='Autonomous Infrastructure Inspector for GPS-denied environments.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'navigator_node = chronos_inspector.navigator_node:main',
            'sensor_simulator = chronos_inspector.sensor_simulator:main',
            'camera_simulator = chronos_inspector.camera_simulator:main',
            'defect_detector = chronos_inspector.defect_detector:main',
            'report_generator = chronos_inspector.report_generator:main',
        ],
    },
)
