import sys, getopt, os, requests, urllib

def main(argv):
    opts, args = getopt.getopt(argv,"hi:o:",["help","ofile="])        
    episode_to = 0
    episode_from = 0

    from_ep, to_ep =parse_args(argv)
    for episode in range(from_ep,to_ep+1):
        download_url = find_episode(episode)

        download_folder = "joerogan"
        if( not os.path.exists(download_folder)):
            os.makedirs(download_folder)
        download(download_url, download_folder + '/' + str(episode) + ".mp3")

def find_episode(episode_number):
    possible_urls = (
        "http://traffic.libsyn.com/joeroganexp/podcast",
        "http://traffic.libsyn.com/joeroganexp/joecast",
        "http://traffic.libsyn.com/joeroganexp/jre",
        "http://traffic.libsyn.com/joeroganexp/p",
        "http://traffic.libsyn.com/joeroganexp/podcast",
        "http://traffic.libsyn.com/joeroganexp/"
    )

    for possible_url in possible_urls:
        episode_url = ''
        if(episode_url == 9):
            episode_url = "http://traffic.libsyn.com/joeroganexp/p3.mp3"
        if(episode_url == 133):
            episode_url = "http://traffic.libsyn.com/joeroganexp/podcast132.mp3"
        # default case
        else:
            episode_url = str(possible_url) + str(episode_number) + ".mp3"

        url = episode_url
        if(exists(url)):
            return episode_url
        
    print("Unable to find url for episode %d, we tried url %s.\nPlease contact p.kolev22@gmail.com with the episode number for resolution.\nThank You !" % (episode_number, episode_url))
        # url = direct_url(episode_url)



# check if the url is reachable
def exists(url):
    try:
        request=urllib.request.urlopen(url)
        return 1
    except:
        return 0

def help():
    print("""
    Usage: {0} episode [optional episode to]
    Example for single episode {0} {1} # will download episode {1}:
    Example for episode range: {0} {1} {2} # will download from episode {1} to episode {2}
    """
    .format(os.path.basename(__file__), 456, 500))
    sys.exit()



# returnes proper args
def parse_args(arguments):
    if(len(arguments)):
        episode_from = int(arguments[0])

        if(len(arguments) == 2 ):
            episode_to = int(arguments[1])
        else:
            episode_to = int(arguments[0])
    else:
        help()
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
    sys.stdout.write("%-66s%3d%%" % (base, percent))

def download(url, dst="a.mp3"):
    print("get url %s to %s" % (url, dst))
    if sys.stdout.isatty():
        urllib.request.urlretrieve(url, dst,
                           lambda nb, bs, fs, url=url: _reporthook(nb,bs,fs,url))
        sys.stdout.write('\n')
    else:
        urllib.request.urlretrieve(url, dst)

######### ENDSTOLENSNIPPET

if __name__ == '__main__':
    main(sys.argv[1:])
