from setuptools import find_packages, setup

# Add install requirements
setup(
    author="Shuaib Ahmed",
    description="""A package that demonstrates the utility of budgeting,
                    saving, and investing through financial algorithms.""",
    name="budgetools",
    packages=find_packages(include=["budgetools", "budgetools.*"]),
    version="0.1.0",
    install_requires=["numpy>=1.18.0", "numpy-financial>=1.0.0", "pandas"],
    python_requires=">=3.6",
)
