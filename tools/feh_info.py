#!/usr/bin/env python3

import sys
import os
import _helpers


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Not enough arguments.')
        sys.exit(os.EX_USAGE)

    game_name, game = _helpers.get_game_from_metadata(sys.argv[1])

    if game:
        print(f'{"":=>{len(game_name)}}')
        print(f'{game_name}')
        print(f'{"":=>{len(game_name)}}')

        print(f'\nBinaries:')
        for binary_filepath in game['binary_filepaths']:
            print(f'* {os.path.basename(binary_filepath)}')

        manual_filepaths = game['manual_filepaths']

        if manual_filepaths:
            print(f'\nManuals:')
            for manual_filepath in game['manual_filepaths']:
                print(f'* {os.path.basename(manual_filepath)}')

    _helpers.write_feh_last_viewed(sys.argv[1])
