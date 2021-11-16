from setuptools import find_packages, setup

setup(
    name="pyExpTools",
    packages=find_packages(include=["pyExpTools"]),
    version="0.1.0",
    description="A library for setting up repeating computational experiments and plotting behavior",
    author="Joel Kelsey",
    license="MIT",
    install_requires=["pandas", "matplotlib"],
    setup_requires=["pytest-runner"],
    tests_requires=["pytest==6.2.5"],
    test_suite="tests"
)