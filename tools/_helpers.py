import os
import re
import json
import hashlib


_metadata_filepath = f'{os.path.dirname(__file__)}/../output/metadata.json'
_feh_list_filepath = f'{os.path.dirname(__file__)}/../output/feh_filelist.txt'
_feh_last_viewed_filepath = f'{os.path.dirname(__file__)}/../output/feh_last_viewed.txt'
_placeholder_image_symlink_dir = f'{os.path.dirname(__file__)}/../output/img'
_placeholder_image_filepath = f'{os.path.dirname(__file__)}/../image_not_found.jpg'


def create_new_symlink_to_placeholder_image(game_name):
    symlink_path = os.path.join(_placeholder_image_symlink_dir, f'{game_name}.jpg')

    try:
        os.symlink(_placeholder_image_filepath, symlink_path)
    except OSError:
        ...

    return symlink_path


def write_metadata(json_data):
    with open(_metadata_filepath, 'w') as metadata_file:
        metadata_file.write(json_data)


def write_feh_filelist(file_list):
    with open(_feh_list_filepath, 'w') as filelist_file:
        for file in file_list:
            filelist_file.write(f'{file}\n')


def get_all_games():
    with open(_metadata_filepath) as metadata_file:
        metadata = json.load(metadata_file)
        return metadata['games']


def get_game_from_metadata(filepath):
    with open(_metadata_filepath) as metadata_file:
        metadata = json.load(metadata_file)

    filepath_hash = hashlib.sha1(filepath.encode()).hexdigest()

    for _filepath_hash, _game_name in metadata['filepath_hashes'].items():
        if _filepath_hash == filepath_hash:
            return _game_name, metadata['games'][_game_name]

    return None, None


def get_first_binary(binary_filepaths):
    if binary_filepaths:
        first_game_binary = re.compile('.*1\\..{3}$')

        for binary_filepath in binary_filepaths:
            if first_game_binary.match(binary_filepath):
                return binary_filepath

        return binary_filepaths[0]

    return None


def write_feh_last_viewed(image_filepath):
    with open(_feh_last_viewed_filepath, 'w') as feh_last_viewed_file:
        feh_last_viewed_file.write(image_filepath)
