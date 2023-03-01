import setuptools

with open("README.md", "r", encoding="utf-8") as fi:
    long_description = fi.read()

setuptools.setup(
	name="shunting-yard",
	version="1.0",
	author="Paul 'charon25' Kern",
	description="Compute any math expression",
	long_description=long_description,
    long_description_content_type='text/markdown',
	python_requires=">=3.9",
	url="https://www.github.com/charon25/ShuntingYard",
	license="MIT",
	packages=['shunting_yard']
)
