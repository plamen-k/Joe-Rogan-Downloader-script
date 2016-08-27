from sqlite_plugin import write_checksum, read_checksum
import sys, getopt, os, urllib, hashlib, requests, syslog, time

DOWNLOAD_FOLDER = "podcasts"

def fork(episode):
    pid = os.fork()
    if pid == 0:
        process(episode)
        os._exit(0)
    return pid

def process(episode):
    download_url = find_episode(episode)
    path_to_file = "%s/%s.mp3" % (DOWNLOAD_FOLDER, episode)
    # if file looks like it is downloaded
    if os.path.isfile(path_to_file):
        # see if it was properly downloaded (the db contains proper hashes)
        file_hash = md5_file(path_to_file)
        db_hash = read_checksum(episode)
        # print("Episode %d\nFile hash: %s\ndatabase hash: %s" % (episode,file_hash, db_hash)) if os.environ['DEBUG'] else 0
        if file_hash == db_hash:
            print ("Episode %s already downloaded" % episode)
            return 1

    # else record the downloaded file's checksum in the db
    download(download_url, path_to_file)
    file_checksum = md5_file(path_to_file)
    write_checksum(episode, file_checksum)
    time.sleep(10)

def find_episode(episode_number):
    possible_urls = (
        "http://traffic.libsyn.com/joeroganexp/",
        "http://traffic.libsyn.com/joeroganexp/podcast",
        "http://traffic.libsyn.com/joeroganexp/joecast",
        "http://traffic.libsyn.com/joeroganexp/jre",
        "http://traffic.libsyn.com/joeroganexp/p",
        "http://traffic.libsyn.com/joeroganexp/pocast",

        "http://traffic.libsyn.com/joeroganexp/_p"
    )

    for possible_url in possible_urls:
        episode_url = ''
        if episode_number == 9:
            return "http://traffic.libsyn.com/joeroganexp/p3.mp3"
        elif episode_number == 133:
            return "http://traffic.libsyn.com/joeroganexp/podcast132.mp3"
        elif episode_number == 142:
            return "http://traffic.libsyn.com/joeroganexp/jre141.mp3"
        elif episode_number == 149:
            return "http://traffic.libsyn.com/joeroganexp/icehouse1.mp3"
        elif episode_number == 202:
            return "http://traffic.libsyn.com/joeroganexp/p203.mp3"
        elif episode_number == 224:
            return "http://traffic.libsyn.com/joeroganexp/p234.mp3"
        # default case
        elif episode_number == 491:
            return "http://traffic.libsyn.com/joeroganexp/491_-_Steve_Maxwell.mp3"
        else:
            episode_url = str(possible_url) + str(episode_number) + ".mp3"

        if exists(episode_url):
            return episode_url
        else:
             # those are letters that sometimes are prependet to an episode like 141a
            appends = ["x","xx","a","b"]
            for suffix in appends:
                episode_url = "%s%d%s.mp3" % (possible_url,episode_number,suffix);
                if exists(episode_url):
                    return episode_url

    syslog.syslog(syslog.LOG_ERR, 'Unable to download episode %d, tried url %s' % (episode_number, episode_url) )
    print("Unable to find url for episode %d, we tried url %s.\n"
          "Please contact p.kolev22@gmail.com with the episode number for resolution.\n"
          "Thank You !"
          % (episode_number, episode_url)
    )


# check if the url is reachable
def exists(url):
    try:
        request = urllib.urlopen(url)
        if request.getcode() == 200:
            return 1
        else:
            return 0

    except urllib.error.HTTPError as e:
        print(e)
        return 0


def help_message():
    print("""
    Usage: {0} episode [optional episode to]
    Example for single episode {0} {1} # will download episode {1}:
    Example for episode range: {0} {1} {2} # will download from episode {1} to episode {2}
    """
    .format(os.path.basename(__file__), 456, 500))
    sys.exit()


# return proper args
def parse_args(arguments):
    if len(arguments):
        episode_from = int(arguments[0])

        if len(arguments) == 2:
            episode_to = int(arguments[1])
        else:
            episode_to = int(arguments[0])
    else:
        help_message()
        sys.exit()
    return (episode_from, episode_to)


# Stolen snipped from http://code.activestate.com/recipes/576530-download-a-url-with-a-console-progress-meter/

def _reporthook(numblocks, blocksize, filesize, url=None):
    #print "reporthook(%s, %s, %s)" % (numblocks, blocksize, filesize)
    base = os.path.basename(url)
    #XXX Should handle possible filesize=-1.
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
    except:
        percent = 100
    if numblocks != 0:
        sys.stdout.write("\b"*70)
    if percent % 100 == 0:
        sys.stdout.write("%-66s%3d%%" % (base, percent))

def download(url, dst="a.mp3"):
    # print("get url %s to %s" % (url,  dst))
    if sys.stdout.isatty():
        urllib.urlretrieve(url, dst,
                           lambda nb, bs, fs, url=url: _reporthook(nb,bs,fs,url))
        sys.stdout.write('\n')
    else:
        urllib.urlretrieve(url, dst)

######### ENDSTOLENSNIPPET


def md5_file(file):
    md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()
#
# if __name__ == '__main__':
#     main()
