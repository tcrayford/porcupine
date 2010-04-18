#!/bin/python
import os, sys, zlib, pprint

from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from porcupine.backend import Backend

pp = pprint.PrettyPrinter(indent=4)

def scan( dir, types, backend ):
	print dir
	for name in os.listdir( dir ):
		path = os.path.join( dir, name )
		if name.split( "." )[-1].lower() in types:
			add( backend, path )
		if os.path.isdir(path):
			r = scan( path, types, backend )
			if r is not None:
				return r

def count( dir, types ):
	c = 0
	for name in os.listdir( dir ):
		path = os.path.join( dir, name )
		if name.split( "." )[-1].lower() in types:
			c += 1
		if os.path.isdir(path):
			c += count( path, types )
	return c
        
def print_add_line( fn, error=0 ):
	if error == 0:
		print "[%s/%s] Added: %s" % ( globals()[ "current" ], globals()[ "total" ], fn )
	else:
		print "[%s/%s] Failed (%s): %s" % ( globals()[ "current" ], globals()[ "total" ], error, fn )

def add( backend, track ):
	#print audio
	globals()[ "current" ] += 1
	
	track = {
		"_FILENAME": 	track
	}
	
	if track[ "_FILENAME" ].split( "." )[-1].lower() == "mp3":
		try:
			audio = MP3( track[ "_FILENAME" ] )
		except:
			print_add_line( track[ "_FILENAME" ], error="Header Not Found" )
			return
		# See: http://wiki.hydrogenaudio.org/index.php?title=Foobar2000:ID3_Tag_Mapping
		fields = {
			"TALB": "ALBUM",
			"TPE1": "ARTIST",
			"WOAR": "ARTIST WEBPAGE URL",
			"BAND": "TPE2",
			"TBPM": "BPM",
			"COMM": "COMMENT",
			"WCOM": "COMMERCIAL INFORMATION URL",
			"TCOM": "COMPOSER",
			"TYER": "YEAR",
			"TDRC": "YEAR",
			"TENC": "ENCODED BY",
			"TSSE": "ENCODED SETTINGS",
			"WOAF": "FILE WEBPAGE URL",
			"TCON": "GENRE",
			"WORS": "INTERNET WEBPAGE RADIO",
			"TSRC": "ISRC",
			"TOAL": "ORIGINAL ALBUM",
			"TOPE": "ORIGINAL ARTIST",
			"TORY": "ORIGINAL RELEASE DATE",
			"TOWN": "OWNER",
			"WPAY": "PAYMENT URL",
			"TPUB": "PUBLISHER",
			"WPUB": "PUBLISHER URL",
			"TRSN": "RADIO STATION",
			"TPE4": "REMIXED BY",
			"WOAS": "SOURCE WEBPAGE URL",
			"TIT3": "SUBTITLE",
			"TIT2": "TITLE",
			"USLT": "UNSYNCED LYRICS",
			"TEXT": "WRITER"
		}


		for k, v in audio.items():
			if k == "TRCK":
				try:
					v = "%s" % (v)
					v = v.split( '/' )
					track[ "TRACKNUMBER" ] = v[0]
					track[ "TOTALTRACKS" ] = v[1]
				except IndexError:
					pass
			elif k == "TPOS":
				try:
					v = "%s" % (v)
					v.split( '/' )
					track[ "DISCNUMBER" ] = v[0]
					track[ "TOTALDISCS" ] = v[1]
				except IndexError:
					pass
				except AttributeError:
					print v, AttributeError, sys.exc_info()[0]
					raise
					exit()
				
			elif k[:5] == "TXXX:" or  k[:5] == "WXXX:":
				track[ k[ 5:] ] = "%s" % v
			elif k in fields:
				track[ fields[ k ] ] = "%s" % v
	elif track[ "_FILENAME" ].split( "." )[-1].lower() == "flac":
		audio = FLAC( track[ "_FILENAME" ] )
		#track = audio
#	pp.pprint( track )
	try:
		backend.Add( track )
		#print_add_line( track[ "_FILENAME" ] )
		return
	except:
		print_add_line( track[ "_FILENAME" ], error="Backend error." )
		return

if __name__ == "__main__":
	types = [ "mp3", "flac" ]
	globals()[ "current" ] = 0
	#globals()[ "total" ] = count( sys.argv[ 1 ], types )
	globals()[ "total" ] = "?"
	backend = Backend()
	
	print "Scanning %s files in %s. " % ( total, sys.argv[ 1 ] )

	scan( sys.argv[ 1 ],
		types,
		backend
	)
	
#	add( backend, "/media/hindsight/music/Black Sun Empire/Driving Insane/220. Sinthetix - Cryogenic (BSE remix).flac" )
#	add( backend, "/media/hindsight/music/Noisia/FabricLive. 40 - Noisia/02. The Qemists - Stompbox (Spor Remix).mp3" )
