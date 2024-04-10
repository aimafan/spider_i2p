from setuptools import setup, find_packages

setup(
    name='spider_i2p',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'spider_i2p = spider_i2p.cli.main:main'
        ]
    },
    author='aimafan',
    author_email='chongrufan@nuaa.edu.cn',
    description='for spider i2p traffic by aimafan',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/aimafan/spider_i2p',
    keywords='spider, i2p, ntcp2, aimafan',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)