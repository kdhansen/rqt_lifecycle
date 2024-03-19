from setuptools import setup

package_name = 'rqt_lifecycle'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    package_dir={'': 'src'},
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['plugin.xml']),
        ('share/' + package_name, ['launch/standalone_launch.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Karl D. Hansen',
    maintainer='Karl D. Hansen',
    maintainer_email='karl.hansen@turftank.com',
    description='An rqt plugin for monitoring and interacting with the state of lifecycle nodes.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'rqt_lifecycle = ' + package_name + '.main:main',
        ],
    },
)
