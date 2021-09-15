from setuptools import setup

setup(
    name="ridgeplot-py",
    py_modules=["ridgeplot"],
    install_requires=["numpy", "scipy", "matplotlib", "more_itertools"],
    python_requires=">3.6.1",
)