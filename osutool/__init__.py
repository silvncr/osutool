'''
Provides utility for compiling and extracting *osu!*-related filetypes,
designed to be user-friendly and efficient, with a focus on simplicity and ease
of use.

osutool is not affiliated with *osu!*. For official information about *osu!*, \
visit [osu.ppy.sh](https://osu.ppy.sh).
'''

from __future__ import annotations

import sys
from contextlib import suppress
from os import listdir, walk
from os import path as os_path
from pathlib import Path
from sys import executable
from sys import path as sys_path
from zipfile import BadZipFile, ZipFile

from colorama import init as colorama_init

# metadata
__author__ = 'silvncr'
__license__ = 'MIT'
__module_name__ = 'osutool'
__python_version__ = '3.8'
__version__ = '0.1.0'


# main function
def main() -> None:
	'''
	Provides the functionality for the entrypoint function.

	```sh
	$ python -m osutool
	```

	Not intended to be used within scripts, except in this library's
	`__main__.py`.
	'''

	# determine working directory
	app_path = (
		os_path.dirname(executable)
		if getattr(sys, 'frozen', False)
		else sys_path[0]
	)

	# initialise colour conversion
	colorama_init(convert=True)

	class C:
		blue = '\033[96m'
		green = '\033[92m'
		grey = '\033[90m'
		purple = '\033[35m'
		red = '\033[91m'
		reset = '\033[0m'
		yellow = '\033[93m'

	# define alert function
	def alert(
		alert_colour: str,
		alert_type: str,
		alert_body: str,
		filenames: list[str],
	) -> str:
		for filename in filenames:
			alert_body = alert_body.replace(
				'[]', f'{C.blue}[{filename}]{C.reset}', 1,
			)
		return (
			f' {alert_colour}[{alert_type.upper()}]{C.reset}'
			+ (' ' * (8 - len(alert_type)))
			+ f'| {alert_body}'
		)

	# if mode is set as an argument
	try:
		mode = sys.argv[1]

	# if mode is not set as an argument
	except IndexError:
		mode = ''

	# alert user of mode options and get user input
	print('')
	if not any(mode.lower().startswith(char) for char in ['c', 'e']):
		print(alert(C.yellow, 'NOTICE', 'Mode is not set.', []))
		while not any(mode.lower().startswith(char) for char in ['c', 'e']):
			mode = input(
				alert(
					C.purple,
					'INPUT', 'Set mode to []ompile or []xtract. > ',
					['c', 'e'],
				),
			)

	# alert user of which mode was selected
	print(alert(C.grey, 'RUNNING', 'Mode is set to [].', [mode]))

	# determine whether actions were performed
	found_valid_files = False

	# failsafe
	try:

		# alert user of working directory
		print(alert(C.grey, 'RUNNING', f'Working directory: {app_path}', []))

		# for every path
		for _dir in walk(app_path):

			# get folder name
			fn = _dir[0]

			# alert user of current directory
			print(alert(
				C.grey, 'RUNNING', 'Checking folder:' +
				(fn.replace(app_path, '') or '(root)'),
				[],
			))

			# if folder contains .osu files and mode is set to compile
			if mode.lower().startswith('c') and any(
				filename.endswith('.osu')
				for filename in (
					listdir(os_path.join(app_path, fn))
					+ listdir(Path.cwd())
				)
			):
				c_name = (fn.replace(app_path, '') + '.osz')[1:]

				# failsafe
				try:

					# failsafe
					try:

						# create .osz file
						with ZipFile(
							os_path.join(app_path, f'{fn}.osz'), 'x',
						) as zf:
							for _, _, files in walk(
								os_path.join(app_path, fn),
							):
								for file in files:
									zf.write(
										os_path.join(app_path, fn, file),
										file,
									)
								print(alert(
									C.green, 'SUCCESS', 'Created []!',
									[c_name],
								))

					# alert user if file already exists
					except FileExistsError:
						with suppress(NameError):
							print(alert(
								C.yellow, 'NOTICE', '[] already exists.',
								[c_name],
							))

					# alert user if access is denied
					except PermissionError:
						with suppress(NameError):
							print(alert(
								C.red, 'ERROR', 'Access is denied to [].',
								[c_name],
							))

					# found valid file
					found_valid_files = True

				# catch errors
				except (
					BadZipFile, FileNotFoundError, PermissionError,
				) as e:
					print(alert(C.red, 'ERROR', f'{e}', []))

			# if folder contains .osz files and mode is set to extract
			elif mode.lower().startswith('e') and any(
				filename.endswith('.osz')
				for filename in (
					listdir(os_path.join(app_path, fn))
					+ listdir(Path.cwd())
				)
			):

				# for every .osz file
				for dirname, subdirs, files in walk(
					os_path.join(app_path, fn),
				):
					for filename in subdirs + files:
						if filename.endswith('.osz'):

							# failsafe
							try:

								# extract .osz file
								with ZipFile(
									os_path.join(
										app_path, dirname, f'{filename}',
									), 'r',
								) as zf:
									Path(os_path.join(
										app_path,
										fn,
										dirname,
										filename[:filename.rfind('.')],
									)).mkdir(parents=True, exist_ok=True)
									zf.extractall(os_path.join(
										app_path,
										fn,
										dirname,
										filename[:filename.rfind('.')],
									))
								print(alert(
									C.green, 'SUCCESS', 'Extracted []!',
									[filename],
								))

							# alert user is file is corrupted
							except BadZipFile:
								print(alert(
									C.red, 'ERROR',
									'[] is corrupted'
									'and could not be extracted.',
									[filename],
								))

							# alert user if access is denied
							except PermissionError:
								print(alert(
									C.red, 'ERROR',
									'Access is denied to [].',
									[filename],
								))

							# catch errors
							except (
								FileExistsError, FileNotFoundError,
								IsADirectoryError, NotADirectoryError,
							) as e:
								print(alert(C.red, 'ERROR', f'{e}', []))

							# if no errors were caught
							else:
								found_valid_files = True

	except KeyboardInterrupt:
		print(alert(C.yellow, 'NOTICE', 'Interrupted by user.', []))

	except (
		FileExistsError, FileNotFoundError, IsADirectoryError,
		NotADirectoryError, PermissionError,
	) as e:
		print(alert(C.red, 'ERROR', f'{e}', []))

	# alert user if no actions were performed
	if not found_valid_files:
		print(alert(C.yellow, 'NOTICE', 'No valid files/folders found.', []))

	# alert user of completion
	input('\n\tFinished! Press Enter to exit.')
