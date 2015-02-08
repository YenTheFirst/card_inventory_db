from setuptools import setup

setup(
	name="card_inventory_db",
	version="0.1.0",
	license="GPL",
	py_modules=["card_inventory_db"],
	install_requires=[
		"SQLAlchemy < 0.8",
		"Elixir"
	]
)
