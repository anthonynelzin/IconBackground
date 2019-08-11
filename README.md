# IconBackground

IconBackground extracts the icon from a macOS app and puts it on a colour-matched background. This script should be useful for anyone writing about apps.

## Example

IconBackground takes this app:

![](example1.jpg)

And makes this image:

![](example2.jpg)

The colour of the background is the dominant colour of the central part of the original icon. IconBackground might produce different results on different occasions, as the position of the central part is slightly shifted from launch to launch.

## Usage

	python3 icon-background.py -a <path_of_the_app>
	
## Licence

EUPL 1.2.