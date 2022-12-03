# Ansible-C64Dreams
> A helper script to obtain and enjoy the _C64 Dreams_ project on Linux.

Table of Contents
=================

* [Introduction](#introduction)
* [What it does](#what-it-does)
* [What it does NOT](#what-it-does-not)
* [How it works](#how-it-works)
* [Requirements](#requirements)
* [Installation](#installation)
   * [Clone repo](#clone-repo)
   * [Execute playbook](#execute-playbook)
* [Usage](#usage)
   * [Start feh](#start-feh)
   * [Keyboard shortcuts](#keyboard-shortcuts)
* [Contributions](#contributions)
* [License](#license)

## Introduction

[C64 Dreams](https://www.zombs-lair.com/c64-dreams) is a curated collection of [Commodore 64](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiXrZX5ktv7AhXy87sIHSTSDFQQFnoECCwQAQ&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FCommodore_64&usg=AOvVaw3Pb3qpxP_1beW2T1TyDUuP) games :joystick: (and other related stuff).  
(Check "[YouTube - C64 Dreams - Project Overview](https://www.youtube.com/watch?v=ZJ_hVPqUDqg)" for a more indepth explanation.)

However, _C64 Dreams_ aims to be run on _Windows_ systems; utilizing the [LaunchBox](https://www.launchbox-app.com/) GUI as frontend/launcher.  
To date, no official Linux build is available. :frowning_face:

## What it does

This project will use [feh](https://feh.finalrewind.org) as viewer/frontend/launcher; so the huge _C64 Dreams_ collection can be enjoyed natively on Linux :penguin:.

Basic functionality like ...

* viewing game artwork (covers, screenshots, etc.)
* sending the game binary to the [VICE](https://vice-emu.sourceforge.io/) emulator
* directly viewing game manuals (with a native application)

... should work.

## What it does NOT

* look as fancy as _LaunchBox_
* provide all the features of _LaunchBox_ (scrollable gallery, sorting, filtering, etc.)
* re-implement all the extra features that come with the customized Windows tools of _C64 Dreams_
* work for everyone :upside_down_face:

## How it works

The [Ansible script](c64dreams-playbook.yml) will automatically ...

* install all necessary packages on your system (_p7zip_, _feh_, _vice_, ...)
* download and unpack the original _C64 Dreams_ archive
* call [scripts](tools) to ...
  * scan the archive and create a metadata file (containing the location of game binaries, manuals, artwork images, etc.)
  * create the actual _feh_ filelist
* create a run-script that lets you start _feh_ with all necessary parameters
* create a (GNOME) desktop launcher

## Requirements

* a Linux distribution with a decent package manager/repository
* sudo rights on your machine
* a working Ansible installation
* (Python3; which should be a dependency of Ansible anyway)

## Installation

### Clone repo

```
git clone https://github.com/4ch1m/ansible-c64dreams.git
```

### Execute playbook

```
cd ansible-c64dreams
./c64dreams-playbook.sh
```
(You'll be prompted to enter your sudo-password here; which is necessary to install _feh_, _vice_, etc. via your system's package manager. -> `BECOME password:`) 

## Usage

### Start feh

Now change to the just created `output` directory and finally start `feh`: 

```
cd output
./run.sh
```

### Keyboard shortcuts

While viewing the game images in `feh` you can use these keyboard shortcuts to trigger certain "actions":

|       Key        |  Action   | Description                                                                                                                           |
|:----------------:|:---------:|:--------------------------------------------------------------------------------------------------------------------------------------|
| <kbd>ENTER</kbd> |    RUN    | sends the associated game binary to `VICE`; if there are multiple binaries (e.g. disk images) the first one gets chosen automatically |
|   <kbd>0</kbd>   |    RUN    | same as <kbd>ENTER</kbd>                                                                                                              |
|   <kbd>1</kbd>   |  MANUAL   | opens existing manual files (PDF, CBZ, etc.) using the system's registered viewer application                                         |
|   <kbd>2</kbd>   |  FOLDER   | opens the game's folder with the native file browser                                                                                  |
|   <kbd>3</kbd>   | WIKIPEDIA | runs a Wikipedia search for this game using the system's web browser                                                                  |

All actions are handled by this Python script: [feh_action.py](tools/feh_action.py)

## Contributions

Contributions (preferably via Pull-Request) are welcome!

## License

Please read the [LICENSE](LICENSE) file.
