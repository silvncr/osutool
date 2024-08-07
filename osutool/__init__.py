'''
Provides utility for compiling and extracting *osu!*-related filetypes.

osutool is not affiliated with *osu!*. For official information about *osu!*,
visit [osu.ppy.sh](https://osu.ppy.sh).
'''

__author__ = 'silvncr'
__license__ = 'MIT'
__module__ = 'osutool'
__version__ = '0.1.3'


import sys
from contextlib import suppress
from os import listdir, walk
from os import path as os_path
from pathlib import Path
from sys import executable
from sys import path as sys_path
from zipfile import BadZipFile, ZipFile

from colorama import init as colorama_init

getch_loaded = False

try:
	from msvcrt import getch  # type: ignore
except ImportError:
	try:
		from getch import getch  # type: ignore
	except ImportError:
		pass
	else:
		getch_loaded = True
else:
	getch_loaded = True


# main function
def main() -> None:
	"""
	Provides the functionality for the entrypoint function.

	```sh
	$ python -m osutool
	```

	Not intended to be used within scripts, except in this library's `__main__.py`.
	"""

	# determine working directory
	app_path = str(Path().cwd().absolute()) or (
		os_path.dirname(executable) if getattr(sys, 'frozen', False) else sys_path[0]
	)

	# initialise colour conversion
	colorama_init(convert=True)

	class TextColour:
		blue = '\033[96m'
		green = '\033[92m'
		grey = '\033[90m'
		purple = '\033[35m'
		red = '\033[91m'
		reset = '\033[0m'
		yellow = '\033[93m'

	# define alert function
	def alert(
		_colour: str, _type: str, _body: str, _names: 'list[str] | None' = None,
	) -> str:
		for filename in _names or []:
			_body = _body.replace(
				'[]', f'{TextColour.blue}[{filename}]{TextColour.reset}', 1,
			)
		return (
			f' {_colour}[{_type.upper()}]{TextColour.reset}'
			+ (' ' * (8 - len(_type)))
			+ f'| {_body}'
		)

	# if mode is set as an argument
	try:
		mode = sys.argv[1]

	# if mode is not set as an argument
	except IndexError:
		mode = ''

	# alert user of working directory
	print()
	print(alert(TextColour.grey, 'RUNNING', f'Working directory: {app_path}'))

	# alert user of mode options and get user input
	if not any(mode.lower().startswith(char) for char in ['c', 'e']):
		print(alert(TextColour.yellow, 'NOTICE', 'Mode is not set.'))
		while not any(mode.lower().startswith(char) for char in ['c', 'e']):
			mode = input(
				alert(
					TextColour.purple,
					'INPUT',
					'Set mode to []ompile or []xtract. > ',
					['c', 'e'],
				),
			)

	# alert user of which mode was selected
	print(alert(TextColour.grey, 'RUNNING', 'Mode is set to [].', [mode]))

	# determine whether actions were performed
	found_valid_files = False

	# failsafe
	try:
		# for every path
		for _dir in walk(app_path):
			# get folder name
			fn = _dir[0]

			# alert user of current directory
			print(
				alert(
					TextColour.grey,
					'RUNNING',
					'Checking folder: ' + (fn.replace(app_path, '') or '(root)'),
				),
			)

			# if folder contains .osu files and mode is set to compile
			if mode.lower().startswith('c') and any(
				filename.endswith('.osu')
				for filename in (
					listdir(os_path.join(app_path, fn)) + listdir(Path.cwd())
				)
			):
				c_name = (fn.replace(app_path, '') + '.osz')[1:]

				# failsafe
				try:
					# failsafe
					try:
						# create .osz file
						with ZipFile(os_path.join(app_path, f'{fn}.osz'), 'x') as zf:
							for _, _, files in walk(os_path.join(app_path, fn)):
								for file in files:
									zf.write(os_path.join(app_path, fn, file), file)
								print(
									alert(
										TextColour.green,
										'SUCCESS',
										'Created []!',
										[c_name],
									),
								)

					# alert user if file already exists
					except FileExistsError:
						with suppress(NameError):
							print(
								alert(
									TextColour.yellow,
									'NOTICE',
									'[] already exists.',
									[c_name],
								),
							)

					# alert user if access is denied
					except PermissionError:
						with suppress(NameError):
							print(
								alert(
									TextColour.red,
									'ERROR',
									'Access is denied to [].',
									[c_name],
								),
							)

					# found valid file
					found_valid_files = True

				# catch errors
				except (BadZipFile, FileNotFoundError, PermissionError) as e:
					print(alert(TextColour.red, 'ERROR', f'{e}'))

			# if folder contains .osz files and mode is set to extract
			elif mode.lower().startswith('e') and any(
				filename.endswith('.osz')
				for filename in (
					listdir(os_path.join(app_path, fn)) + listdir(Path.cwd())
				)
			):
				# for every .osz file
				for dirname, subdirs, files in walk(os_path.join(app_path, fn)):
					for filename in subdirs + files:
						if filename.endswith('.osz'):
							# failsafe
							try:
								# extract .osz file
								with ZipFile(
									os_path.join(app_path, dirname, f'{filename}'), 'r',
								) as zf:
									Path(
										os_path.join(
											app_path,
											fn,
											dirname,
											filename[: filename.rfind('.')],
										),
									).mkdir(parents=True, exist_ok=True)
									zf.extractall(
										os_path.join(
											app_path,
											fn,
											dirname,
											filename[: filename.rfind('.')],
										),
									)
								print(
									alert(
										TextColour.green,
										'SUCCESS',
										'Extracted []!',
										[filename],
									),
								)

							# alert user is file is corrupted
							except BadZipFile:
								print(
									alert(
										TextColour.red,
										'ERROR',
										'[] is corruptedand could not be extracted.',
										[filename],
									),
								)

							# alert user if access is denied
							except PermissionError:
								print(
									alert(
										TextColour.red,
										'ERROR',
										'Access is denied to [].',
										[filename],
									),
								)

							# catch errors
							except (
								FileExistsError,
								FileNotFoundError,
								IsADirectoryError,
								NotADirectoryError,
							) as e:
								print(alert(TextColour.red, 'ERROR', f'{e}'))

							# success
							else:
								found_valid_files = True

	except KeyboardInterrupt:
		print(alert(TextColour.yellow, 'NOTICE', 'Interrupted by user.'))

	except (
		FileExistsError,
		FileNotFoundError,
		IsADirectoryError,
		NotADirectoryError,
		PermissionError,
	) as e:
		print(alert(TextColour.red, 'ERROR', f'{e}'))

	# alert user if no actions were performed
	if not found_valid_files:
		print(alert(TextColour.yellow, 'NOTICE', 'No valid files/folders found.'))

	# alert user of completion
	if getch_loaded:
		print('\n\tFinished! Press any key to exit.')
		getch()
	else:
		input('\n\tFinished! Press Enter to exit.')

	# exit
	sys.exit(0)


# run main
if __name__ == '__main__':
	with suppress(KeyboardInterrupt):
		main()
