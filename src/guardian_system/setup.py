from setuptools import setup

package_name = 'guardian_system'

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
    maintainer='Yogesh',
    maintainer_email='yogesh@example.com',
    description='Failure-Resilient Guardian Stack for Autonomous Inspection',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'guardian_node = guardian_system.guardian_node:main',
            'black_box_logger = guardian_system.black_box_logger:main',
        ],
    },
)
