# IconBackground

IconBackground extracts the icon from a macOS app and puts it on a colour-matched background. This script should be useful for anyone writing about apps.

## Example

IconBackground takes this app:

![](example-1.jpg)

And makes this image:

![](example-2.png)

The colour of the background is the dominant colour of the central part of the original icon. IconBackground might produce different results on different occasions, as the position of the central part is slightly shifted from launch to launch.

## Usage

	python3 icon-background.py -a <path_of_the_app>
	
## Requirements

- argparse
- biplist
- collections
- pillow
- random
- sklearn

## Licence

EUPL 1.2.