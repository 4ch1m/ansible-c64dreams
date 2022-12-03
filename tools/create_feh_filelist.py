#!/usr/bin/env python3

import _helpers

if __name__ == '__main__':
    file_list = []

    for _, game_metadata in _helpers.get_all_games().items():
        file_list.extend(game_metadata['image_filepaths'])

    _helpers.write_feh_filelist(file_list)
