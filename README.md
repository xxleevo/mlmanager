# mlmanager

mlmanager is a python based manager to help maintain the state of iPhones running an iOS application in Guided Access Mode or Single App Mode.

## Prerequisites
1. Install [Homebrew](https://brew.sh) if not already installed `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"`
1. Update Homebrew `brew update`
1. Uninstall previous `libimobiledevice` versions `brew uninstall --ignore-dependencies libimobiledevice`
1. Uninstall previous `usbmuxd` versions `brew uninstall --ignore-dependencies usbmuxd`
1. Uninstall previous `libplist` versions `brew uninstall --ignore-dependencies libplist`
1. Install latest `usbmuxd` `brew install --HEAD usbmuxd`
1. Install latest `libplist` `brew install --HEAD libplist`
1. Install latest `libimobiledevice` `brew install --HEAD libimobiledevice`
1. Install `ideviceinstaller` `brew install ideviceinstaller`
1. Install `ios-deploy` `brew install ios-deploy`

## Installation
1. `git clone ...`
1. `cd mlmanager`
1. `cp config.example.json config.json`
1. Fill out the config file (more details in the options category below)
1. Install dependencies `npm install` and `brew install python3`
1. Install pm2 (optional) `npm install pm2 -g`
1. Start the manager with `pm2 start mlmanager.py --interpreter=python3` or `python3 mlmanager.py` if not using pm2

### Options

- `deviceHold` is how long before mlmanager will take action on a device for repeat fix
  IE - 300 seconds means 5 minutes after installing or rebooting a device we will attempt to apply a fix again
- `"devices": []` will take action on all attached devices. If you want to be selective on your actions add the **exact** device name as seen in Xcode.
  IE - "devices": ["SE001", "SE002"]`
- `threshold` values are in seconds and are how long before an action should be applied
- `saveScreenshots` if you want to store screenshots locally to help with debugging
- `ipa` is the path to an IPA file on disk. I recommend building and signing like normal then doing a copy to /Users/Shared with a static name since that directory has read access by default on macOS.
