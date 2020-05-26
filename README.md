# mlmanager

mlmanager is a python based manager to help maintain the state of iPhones running an iOS application in Guided Access Mode or Single App Mode.

## Prerequisites

1. Install [Homebrew](https://brew.sh) if not already installed `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"`
1. Update Homebrew `brew update`
1. Uninstall previous versions of of tools to make sure they don't cause issues

  ```shell
  brew uninstall --ignore-dependencies usbmuxd libplist libimobiledevice ideviceinstaller ios-deploy
  ```

1. Install command line tools

  ```shell
  brew install --HEAD usbmushellxd
  brew install --HEAD libplist
  brew install --HEAD libimobiledevice
  brew install ideviceinstaller
  brew install ios-deploy
  brew install python3
  ```

## Installation

1. `git clone https://github.com/clburlison/mlmanage`
1. `cd mlmanager`
1. `cp config.example.json config.json`
1. Fill out the config file (more details in the options category below)
1. Install python modules pip3 install -r requirements.txt
1. Start the manager with `pm2 start mlmanager.py --interpreter=python3` or `python3 mlmanager.py` if not using pm2

### Options

- `user` is an admin username for rdm dashboard
- `password` is the associated password for the rdm user
- `deviceHold` is how long mlmanager will wait before taking action on a device for repeat actions  
  IE - 300 seconds means 5 minutes after installing or rebooting a device we will attempt to apply a fix again
- `threshold` values are in seconds. This determines how long before a device is considered inactive and requires a fix.
- `saveScreenshots` if you want to store screenshots locally to help with debugging
- `ipa` is the path to an IPA file on disk. I recommend building and signing like normal then doing a copy to /Users/Shared with a static name since that directory has read access by default on macOS.
- `"devices": []` by default will take action on all attached devices. If you want to be selective on your actions add the **exact** device name as seen in Xcode.  
  IE - "devices": ["SE001", "SE002"]`

## FAQ

Q: **I receive a bunch of "Could not start screenshotr service!..." errors?**  
A: Make sure you have device support files for all attached devices. You can verify this via Xcode > Window > Devices and Simulators... If you have a yellow header like below then you need to install support files which can be obtained from [iGhibli/iOS-DeviceSupport](https://github.com/iGhibli/iOS-DeviceSupport)

```/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/DeviceSupport```

![device support files](https://i.imgur.com/wNXHsBm.png)
