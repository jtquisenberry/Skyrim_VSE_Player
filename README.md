# Skyrim VSE Player

Skyrim Very Special Edition Player is a Python 3.x application to play the Amazon Alexa skill Skyrim Very Special Edition on an Android device.


# What is Skyrim Very Special Edition

Skyrim Very Special Edition is a skill for Amazon Alexa devices. 

From Amazon:

"Bethesda Game Studios is proud to present Skyrim... for Alexa. Yes, that’s right, the version of Skyrim you never saw coming has finally arrived on the platform you never asked for.

For the very first time ever, take your rightful place as the Dragonborn of legend (again) and explore Skyrim using the power of your own voice...your Thu’um!"
https://www.amazon.com/Bethesda-Game-Studios-Special-Edition/dp/B07D6STSX8

The first version of Skyrim VSE was played using voice input. Alexa gained chatbot functionality and began accepting typed input late in 2020. 
https://voicebot.ai/2020/12/01/alexa-becomes-a-chatbot-you-can-now-talk-to-alexa-by-typing/


# Usage

List android devices connected to the PC.

```
> python list_devices.py
BEGIN DEVICES

Serial: emulator-5554, State: device

END DEVICES
```

Set the properties of the device you want to connect to and the log file location in `skyrim_vesp.py`.

``` python
SERIAL = 'emulator-5554'
HOST = '127.0.0.1'
PORT = 5037
LOG = r'D:\Projects\skyrim.txt'
```

Run Skyrim VSE Player.

```
> python skyrim_vsep.py
STARTING
ELAPSED TIME: 0:00:00 CURRENT TIME 2024-08-30 22:18:33.565291
last_responses count 0
last_requests count 0
ELAPSED TIME: 0:01:09.308853 CURRENT TIME 2024-08-30 22:19:42.874144
last_responses count 1
last_requests count 0
Startup	Skyrim	1	1	1	Unrelenting Force			Flames		Dagger				Hello, Alexa here. Happy to help. Ask me anything or search the app.
```


# Requirements

Unless stated otherwise, these requirements assume that the user runs an emulated Android device.

## Python

Python 3.12

## Python Packages

```
uiautomator2==3.2.2
adbutils==2.8.0
```

## PC

Skyrim VSE Player must be run on a PC capable of connecting to an Android device - physical or virtual.

### Virtual

Running an Android emulator requires a computer with hardware virtualization enabled. The ability to run HAXM is recommended.

### Physical

This application also works with a physical Android device running in debug mode and connected to a PC with a USB cable. I ran an early version of the application with a Motorola Droid Turbo (2014). The Android device must be configured to support USB debugging.

## Android Studio

Skyrim VSE Player connects to an Android device. These requirements assume that the user is running an emulated Android device using Android Studio.

Android Studio may be downloaded from this location: https://developer.android.com/studio

## Alexa App

Skyrim VSE Player has been tested with Alexa version 2.2.436689.0. Other versions may have UI layouts not compatible with the Player. It is possible to download an APK file of that version from here: https://www.apkmirror.com/apk/amazon-mobile-llc/amazon-alexa/amazon-alexa-2-2-436689-0-release/ . 



# Example

## Log

```
Timestamp	Setting	Command	ShoutLevel	SpellLevel	WeaponLevel	NewShout	NewShout2	CurrentShout	NewSpell	CurrentSpell	NewWeapon	CurrentWeapon	NewEnemy	CurrentEnemy	Dialog
...
2022-01-09 21:25:13.720634	Path	Hill	1	1	98					Battleaxe				Imperial Gladiator	Your Battleaxe cleaves the Imperial Gladiator. The Imperial Gladiator falls dead. He'll never be Grand Champion now. How sad.. You survived the battle. Your health is at 100.  There are three paths forward: a root-covered hill, a stream-filled glade, and a steep hill. Which do you choose?
```

### Fields

* __Timestamp__: The time at which the log message was written.
* __Setting__: The location of the current quest.
* __Command__: The command sent by the player.
* __ShoutLevel__: The level of the character's Shout skill.
* __SpellLevel__: The level of the character's Spell skill.
* __WeaponLevel__: The level of the character's Weapon skill.
* __NewShout__: Reports the name of a previously unseen shout.
* __NewShout2__: Reports the name of a previously unseen shout, using a different technique.
* __CurrentShout__: The shout used in the last command, if any.
* __NewSpell__: Reports the name of a previously unseen spell.
* __CurrentSpell__: The spell used in the last command, if any.
* __NewWeapon__: Reports the name of a previously unseen weapon.
* __CurrentWeapon__: The weapon used in the last command, if any.
* __Dialog__: The text of the response given by Alexa.

## Screenshot

This screenshot shows dialog of defeating an Ascendant Necromancer.

![Ascendant Necromancer](images/ascendant_necromancer.png?raw=true "Ascendant Necromancer - Alexa 2.2.585588.0")


# Setup

# Emulator Setup in Android Studio

Screenshots of Android Studio show Android Studio Giraffe | 2022.3.1.

Within Android Studio, open Device Manager, and click "Create Device". 

![Create Device](images/android_studio_device_manager.png?raw=true "Create Device")

From the list of device definitions, select a device with the Play Store. The Pixel 4 device works well.

![Pixel 4 Selected](images/android_studio_configuration.png?raw=true "Pixel 4 Selected")

Run the emulated device from the list of devices. After the device starts for the first time, you must logon with a Google account to access the Play Store. You may also have to verify your identity in the Play Store.

![Play Store](images/play_store_login.png?raw=true "Play Store")

Install the Alexa app and start it.

![Alexa App](images/alexa_app.png?raw=true "Alexa App")

Click the typewrite icon to access chat bot mode.

![Alexa App](images/alexa_keyboard.png?raw=true "Alexa App")

Alexa displays the chat dialog.

![Alexa App](images/alexa_dialog.png?raw=true "Alexa App")



# Credits

## `adbutils`

"Python adb library for adb service" is a Python library for interfacing with the Android Debug Bridge (ADB) service. It is used for listing devices and rebooting a device.

* https://github.com/openatx/adbutils
* https://pypi.org/project/adbutils/

## `uiautomator2`

"Python Wrapper for Android UiAutomator2 test tool" is a Python library for interfacing with the Android UI. It is used for communicating with Alexa.

* https://github.com/openatx/uiautomator2
* https://pypi.org/project/uiautomator2/





