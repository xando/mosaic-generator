Tool to create image mosaic
===========================

    $ mosaic.py {Big Picture} {Tiles Pictures} {Tile Size} [-o {Output File}]

eg.
	
    $ mosaic.py awesome.jpg MeAndMyFreindsDrunk/ 64 -o mosaic.jpg 

Requirements
------------
  * numpy
  * clint
  * PIL

Plugin
------

Download Photos from Flickr group

    $ python plugin/flickr_download.py {group_id]} {output directory}

eg.

    $ python plugin/flickr_download.py 37996612603@N01 MontyPython