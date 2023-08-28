<!-- omit from toc -->
# osutool

multipurpose tool for *osu!* files

![version](https://img.shields.io/pypi/v/osutool)
![status](https://img.shields.io/github/actions/workflow/status/silvncr/osutool/python-publish.yml)
![downloads](https://img.shields.io/pypi/dm/osutool)

![license](https://img.shields.io/github/license/silvncr/osutool)
![python](https://img.shields.io/pypi/pyversions/osutool)

## Summary

Provides utility for compiling and extracting *osu!*-related filetypes, designed to be user-friendly and efficient, with a focus on simplicity and ease of use.

- :snake: Supports Python 3.8 and above. Tested on Windows 10.
- :construction: Work in progress. Features are not finalised and may be unstable.
- :arrows_clockwise: Pull requests are welcome!
- :star: Show your support by leaving a star!

> osutool is not affiliated with *osu!*. For official information about *osu!*, visit [osu.ppy.sh](https://osu.ppy.sh).

## Contents

- [Summary](#summary)
- [Contents](#contents)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Compilation (folders to files)](#compilation-folders-to-files)
  - [Extraction (files to folders)](#extraction-files-to-folders)

## Features

- [x] convert beatmap/song folders to `.osz` files, and vice versa
- [ ] convert skin folders to `.osk` files, and vice versa

## Installation

```sh
python -m pip install --upgrade osutool
```

## Usage

Open a command line from the directory with the files you want to manipulate, then run osutool.

```sh
$ osutool

 [NOTICE]  | Mode is not set.
 [INPUT]   | Set mode to [c]ompile or [e]xtract. > _
```

### Compilation (folders to files)

```sh
> c
```

The program will create a file for every applicable folder and subfolder. Files generated from subfolders will be placed in the same subfolder.

Each file will be named after the folder it was created from.

### Extraction (files to folders)

```sh
> e
```

The program will generate a folder for every file in the current folder and its subfolders. Folders generated from subfolders will be placed in the same subfolder.

Each folder will be named after the file it was created from.
