#!/usr/bin/env python

import os.path
import MySQLdb
import features

def main():
    print "Beginning feature strip"
    db = MySQLdb.connect(host="localhost", user="root", passwd="", db="genrebot")
    cursor = db.cursor()
    basepath = "/Users/Atta/Desktop/songs/"
    directory = os.listdir(basepath)
    for genre in directory:
        print "---NOW STARTING {0} SONGS---".format(genre.upper())
        # Get the id in the db for the genre
        cursor.execute("""Select id from Genres where name = %s""", (genre))
        genre_id = cursor.fetchone()[0]
        genre_path = os.path.join(basepath, genre)
        genre_dir = os.listdir(genre_path)
        for song in genre_dir:
            # Remove the .DS_Store file and out special output.wav file, Quick and Dirty style
            if (song != ".DS_Store" and song != "output.wav"):
                print "Current Song is: " + os.path.join(genre_path, song)
                f1, f2 = features.strip(os.path.join(genre_path, song), genre_path)
                # Add ALL the features to the database!
                cursor.execute("INSERT INTO features (title,genre,amp1mean,amp1std,amp1skew,amp1kurt,amp1dmean,amp1dstd,amp1dskew,"
                                  "amp1dkurt,amp10mean,amp10std,amp10skew,amp10kurt,amp10dmean,amp10dstd,amp10dskew,"
                                  "amp10dkurt,amp100mean,amp100std,amp100skew,amp100kurt,amp100dmean,amp100dstd,"
                                  "amp100dskew,amp100dkurt,amp1000mean,amp1000std,amp1000skew,amp1000kurt,amp1000dmean,"
                                  "amp1000dstd,amp1000dskew,amp1000dkurt,power1,power2,power3,power4,power5,power6,power7,power8,power9,power10)"
                                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (song, genre_id) + tuple(f1))
                cursor.execute("INSERT INTO features (title,genre,amp1mean,amp1std,amp1skew,amp1kurt,amp1dmean,amp1dstd,amp1dskew,"
                                  "amp1dkurt,amp10mean,amp10std,amp10skew,amp10kurt,amp10dmean,amp10dstd,amp10dskew,"
                                  "amp10dkurt,amp100mean,amp100std,amp100skew,amp100kurt,amp100dmean,amp100dstd,"
                                  "amp100dskew,amp100dkurt,amp1000mean,amp1000std,amp1000skew,amp1000kurt,amp1000dmean,"
                                  "amp1000dstd,amp1000dskew,amp1000dkurt,power1,power2,power3,power4,power5,power6,power7,power8,power9,power10)"
                                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (song, genre_id) + tuple(f2))
                print "Finished!"
    print "All done!"

if __name__ == "__main__":
    main()