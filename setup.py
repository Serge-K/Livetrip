# _*_ coding: utf-8 _*_
from setuptools import setup

setup(
	name = 'Livetrip',
	version = '1.0',
	license = 'BSD',
	platforms = 'Unix',
	url = '',
	author = 'Livetrip Team',
	author_email = 'lord@const.ru',
	packages = ['app', 'admin', 'async_task', 'models', 'lib'],
	entry_points = {'paste.app_factory': [
		'main = app:main',
		'admin = admin:admin_main'
	],
	'console_scripts': ['initialize_db = scripts.initializedb:main']},
)
