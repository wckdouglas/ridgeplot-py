from setuptools import setup

setup(
    name="ridgeplot-py",
    packages=["ridgeplot",],
    install_requires=["numpy", "scipy", "matplotlib", "more_itertools"],
    python_requires=">3.6.1",
)
