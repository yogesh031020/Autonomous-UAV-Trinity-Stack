from setuptools import find_packages, setup

package_name = 'guardian_system'

setup(
    name=package_name,
    version='2.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yogesh',
    maintainer_email='yogesh@example.com',
    description='Senior Fail-Resilient Autonomy System for VANGUARD.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'guardian_node = guardian_system.guardian_node:main',
            'black_box_logger = guardian_system.black_box_logger:main',
            'offboard_control = guardian_system.offboard_control:main',
        ],
    },
)
