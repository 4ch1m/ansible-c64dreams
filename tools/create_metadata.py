#!/usr/bin/env python3

import sys
import os
import re
import json
import hashlib
import _helpers

from collections import OrderedDict


C64_FILE = re.compile('.*(\\.d64|\\.t64|\\.tap|\\.crt|\\.prg)$', re.IGNORECASE)
IMAGE_FILE = re.compile('.*(\\.png|\\.jpeg|\\.jpg)$', re.IGNORECASE)
MANUAL_FILE = re.compile('.*(\\.cbz|\\.pdf)$', re.IGNORECASE)

EXCLUDED_PATH = re.compile('.*/!(Backup|EasyFlash).*', re.IGNORECASE)
GAMES_PATH = re.compile('.*/Games/.*', re.IGNORECASE)
IMAGES_PATH = re.compile('.*/Images/.*', re.IGNORECASE)


class Game:
    def __init__(self, binary_filepaths, image_filepaths, manual_filepaths):
        self.binary_filepaths = binary_filepaths
        self.image_filepaths = image_filepaths
        self.manual_filepaths = manual_filepaths

    def json_dict(self):
        return self.__dict__


class MetaData:
    def __init__(self, games, filepath_hashes):
        self.games = games
        self.filepath_hashes = filepath_hashes

    def json_dict(self):
        return self.__dict__


def _check_image_filepath(game_name, image_filepath):
    return (  # trying to mitigate inconsistencies in file-/path-naming of images ...
        (f'/{game_name}-' in image_filepath) or
        ("'" in game_name and f'''/{game_name.replace("'", "_")}-''' in image_filepath) or
        (" - " in game_name and f'''/{game_name.replace(' - ', '_ ')}-''' in image_filepath) or
        (("'" in game_name and " - " in game_name) and f'''/{game_name.replace("'", '_').replace(' - ', '_ ')}-''' in image_filepath) or
        (game_name.endswith(", the") and f'''the {game_name.replace(", the", "")}-''' in image_filepath) or
        (game_name.endswith(", a") and f'''a {game_name.replace(", a", "")}-''' in image_filepath) or
        (f'/{game_name} (' in image_filepath) or
        (f'/{game_name}_ ' in image_filepath) or
        (f"/{game_name.replace(' ', '-')}-" in image_filepath)
    )


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Not enough arguments.')
        sys.exit(os.EX_USAGE)

    all_game_binary_files = []
    all_game_image_files = []
    all_game_manual_files = []

    for root_dir, _, file_names in os.walk(sys.argv[1]):
        for file_name in file_names:
            file_path = os.path.join(root_dir, file_name)

            if EXCLUDED_PATH.match(file_path):
                continue

            if C64_FILE.match(file_path):
                if GAMES_PATH.match(root_dir):
                    all_game_binary_files.append(file_path)
            elif IMAGE_FILE.match(file_path):
                if IMAGES_PATH.match(root_dir):
                    all_game_image_files.append(file_path)
            elif MANUAL_FILE.match(file_path):
                if GAMES_PATH.match(root_dir):
                    all_game_manual_files.append(file_path)

    games = {}

    for game_binary_file in all_game_binary_files:
        game_name = os.path.basename(os.path.dirname(game_binary_file))

        if games.get(game_name):
            continue

        game_binaries = [
            _game_binary_file
            for _game_binary_file in all_game_binary_files
            if f'/{game_name}/' in _game_binary_file
        ]
        game_binaries.sort()

        game_images = [
            _game_image_file
            for _game_image_file in all_game_image_files
            if _check_image_filepath(game_name.lower(), _game_image_file.lower())
        ]
        game_images.sort()

        if not game_images:
            game_images.append(_helpers.create_new_symlink_to_placeholder_image(game_name))

        game_manuals = [
            _game_manual_file
            for _game_manual_file in all_game_manual_files
            if f'/{game_name}/'.lower() in _game_manual_file.lower()
        ]
        game_manuals.sort()

        games[game_name] = Game(
            game_binaries,
            game_images,
            game_manuals
        )
        games = OrderedDict(sorted(games.items()))

    filepath_hashes = {}

    for _name, _game in games.items():
        for file_paths in (_game.binary_filepaths, _game.image_filepaths, _game.manual_filepaths):
            for file_path in file_paths:
                filepath_hashes[hashlib.sha1(file_path.encode()).hexdigest()] = _name

    json_dump = json.dumps(
        MetaData(games, filepath_hashes),
        indent=4,
        default=lambda _object: _object.json_dict() if hasattr(_object, 'json_dict') else None
    )

    _helpers.write_metadata(json_dump)

    print(f'{len(games.items())} games found.')
