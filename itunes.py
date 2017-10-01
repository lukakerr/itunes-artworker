import os
import urllib, urllib2
import re
import json
import sys
from pydub import AudioSegment
from mutagen import id3, mp3
from mutagen.mp4 import MP4, MP4Cover

# Current directory path
dir_path = os.path.dirname(os.path.realpath(__file__))

# iTunes music directory path
music_dir = "/Users/%s/Music/iTunes/iTunes Media/" % os.getlogin()

artists = []
albums = []
artists_and_albums = {}

# Method for choice 1
def single_album(artist_name, album_name):
	# Create query
	query = artist.replace(" ", "+") + "+" + album.replace(" ", "+") + "+album"

	# Story query album image URL
	album_url = search(query)

	# Album subfolder is just the given album name
	album_subfolder = album_name

	# Create the /album_art folder and the album subfolder
	make_img_folder(album_subfolder)

	# Download the image from the album_url URL and save it in given album name subfolder
	filename, headers = urllib.urlretrieve(album_url, "album_art/%s/" % album_subfolder + "img.jpg")

	print("\nDone!")
	print("\nAdding artwork to specified album...")

	# Check if album actually exists in music directory
	if os.path.exists(music_dir + artist_name + album_name):
		for dirpath, subdirs, files in os.walk(music_dir + artist_name + album_name):
			for song_name in files:
				if song_name != ".DS_Store":
					print("Replacing %s artwork" % song_name)
					path = music_dir + artist_name + album_name + "/"

					# If m4a file, convert to mp3
					if song_name.endswith("m4a"):
						# print("Converting to %s MP3" % song_name)

						# new_song = convert_song(artist_name, album_name, song_name)

						# Remove old m4a file
						# os.remove(music_dir + "%s/%s/%s" % (artist_name, album_name, song_name))

						song = MP4(music_dir + "%s/%s/%s" % (artist_name, album_name, song_name))

						with open(dir_path + "/album_art/%s/img.jpg" % album_subfolder, "rb") as f:
						    song["covr"] = [
						        MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
						    ]

						song.save()

						# song = mp3.MP3(path + new_song)

					elif song_name.endswith("mp3"):
						song = mp3.MP3(path + song_name)
						# Change album artwork
						imagedata = open(dir_path + "/album_art/%s/img.jpg" % album_subfolder,"rb").read()
						song.tags.add(id3.APIC(3, 'image/jpg', 3, 'Album Artwork', imagedata))
						song.save()

					print("Done!")

	else:
		print("Artist/album not found. Make sure you have spelt the name exactly correct.")

def all_albums():
	# Check if album actually exists
	if os.path.exists(music_dir):
		artists = os.walk(music_dir).next()[1]

		for i, v in enumerate(artists):
			album = os.walk(music_dir + v).next()[1]
			albums.append(album)

		artists_and_albums = dict(zip(artists, albums))
	else:
		print("Music folder not found.")

	for i in artists_and_albums.keys():
		for x in artists_and_albums[i]:
			if not x == "Unknown Album":
				query = "{}+{}+album".format(i.replace(" ", "+").replace("&", "").replace("++", "+"), x.replace(" ", "+"))
				album_url = search(query)

				# Album subfolder = album name
				album_subfolder = x

				make_img_folder(album_subfolder)

				filename, headers = urllib.urlretrieve(album_url, "album_art/%s/" % album_subfolder + "img.jpg")

				print("\nDone!")
				print("\nReplacing all album art...")

				# Check if album actually exists
				if os.path.exists(music_dir + "/%s/%s" % (i, x)):
					# Iterate over every artist and album in the music directory
					for dirpath, subdirs, files in os.walk(music_dir + "/%s/%s" % (i, x)):
						for song_name in files:
							if song_name != ".DS_Store":
								path = music_dir + "%s/%s/" % (i, x)
								if song_name.endswith("m4a"):
									print("Converting to MP3 - %s" % song_name)

									new_song = convert_song(i, x, song_name)

									os.remove(music_dir + "%s/%s/%s" % (i, x, song_name))

									song = mp3.MP3(path + new_song)

								elif song_name.endswith("mp3"):
									song = mp3.MP3(path + song_name)

								imagedata = open(dir_path + "/album_art/%s/img.jpg" % album_subfolder,"rb").read()
								song.tags.add(id3.APIC(3, 'image/jpg', 3, 'Album Artwork', imagedata))
								song.save()
				else:
				 	print("Artist/album not found. Make sure you have spelt the name exactly correct.")


def convert_song(i, x, song_name):
	unconverted_song = AudioSegment.from_file(music_dir + "%s/%s/%s" % (i, x, song_name), format="m4a")
	unconverted_song.export(music_dir + "%s/%s/%s.mp3" % (i, x, song_name[:-4]), format="mp3")
	new_song = song_name[:-4] + ".mp3"
	return new_song

def search(query):
	album_art_url = "https://www.google.com.au/search?as_st=y&tbm=isch&as_q=" + query + "&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:lt,islt:qsvga,iar:s"

	urllib.URLopener.version = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'

	request = urllib2.Request(album_art_url, None, {'User-agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30"})
	response = urllib2.urlopen(request)
	search_html = response.read()

	# # Find first image's JSON data
	url_pattern = re.compile(r"<div class=\"rg_meta\">([^<]*)<\/div>")
	re_find = url_pattern.search(search_html)

	# Remove HTML from JSON
	json_content = re_find.group().replace("<div class=\"rg_meta\">", "").replace("</div>", "")

	# Load JSON
	json_data = json.loads(json_content)

	# Album URL value is under "ou" key
	album_url = json_data['ou']

	return album_url

def make_img_folder(album_subfolder):
	# If album_art directory doesn't exist in current directory, create it
	if not os.path.exists(dir_path + "/album_art"):
		os.mkdir(dir_path + "/album_art")
		os.mkdir(dir_path + "/album_art/%s" % album_subfolder)

	# If album_art directory does exists, but album subfolder folder doesn't, create it
	elif not os.path.exists(dir_path + "/album_art/%s" % album_subfolder):
			os.mkdir(dir_path + "/album_art/%s" % album_subfolder)

	print("\nCreated /album_art/%s" % album_subfolder)

	print("\nDownloading album artwork now...")

if __name__ == "__main__":
	while True:
		try:
			choice = raw_input("What do you want to do? \n[1] Find and replace a single album \n[2] Find and replace every album in iTunes library \n: ")
			if choice == "1":
				artist = raw_input("Enter the exact artist name: ")
				album = raw_input("Enter the exact album name: ")

				artist_name = artist + "/"
				album_name = album

				# Check if entered artist and album exist
				if os.path.exists(music_dir + artist_name + album_name):
					print("\x1b[6;30;42m" + "Successfully found artist/album combination" + "\x1b[0m")
					single_album(artist_name, album_name)
				else:
					print("\x1b[0;37;41m" + "Artist/Album not found. Please try again" + "\x1b[0m")


			elif choice == "2":
				all_albums()
			else:
				print("You didn't enter a correct number")
		except KeyboardInterrupt:
			print("\nBye!")
		   	sys.exit(0)
