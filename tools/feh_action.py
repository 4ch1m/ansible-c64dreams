#!/usr/bin/env python3

import sys
import os
import subprocess
import webbrowser
import urllib.parse
import _helpers


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Not enough arguments.')
        sys.exit(os.EX_USAGE)

    game_name, game = _helpers.get_game_from_metadata(sys.argv[1])

    if game:
        match sys.argv[2]:
            case 'run_game':
                first_binary = _helpers.get_first_binary(game['binary_filepaths'])

                if first_binary:
                    subprocess.run([
                        'x64',
                        first_binary
                    ])

            case 'show_manual':
                if game['manual_filepaths']:
                    subprocess.run([
                        'open',
                        game['manual_filepaths'][0]
                    ])

            case 'open_game_folder':
                subprocess.run([
                    'open',
                    os.path.dirname(game['binary_filepaths'][0])
                ])

            case 'search_wikipedia':
                webbrowser.open(
                    f'https://en.wikipedia.org/w/index.php?search=commodore%2064+{urllib.parse.quote(game_name)}',
                    new=2
                )
