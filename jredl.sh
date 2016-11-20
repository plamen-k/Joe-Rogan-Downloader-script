#!/bin/bash

PODCASTFOLDER=JoeRoganPodcast
CONCURRENT=5

from=$1
to=${2:-$1} 
echo from $from
echo to $to
if [ -z "$*" ]; then 
    echo "Usage: ./jredl.sh 500  or ./jredl.sh 600 700"; 
    exit 1
fi


function download_seq(){
    from=$1
    to=$2
    if [ ! -d $PODCASTFOLDER ]; then
        mkdir $PODCASTFOLDER
    fi

    for i in `seq $from $to`;
    do
        out=`wget http://traffic.libsyn.com/joeroganexp/p$i.mp3 -P $PODCASTFOLDER`
        echo $out
    done 
}

function download_thread(){
    from=$1
    to=$2
    
    current_batch=0
#    pids=""
    for i in `seq $from $to`;
        do  
        `wget -r -np -N http://traffic.libsyn.com/joeroganexp/p$i.mp3 -P $PODCASTFOLDER &`
        $current_batch++
        if [ $current_batch -eq $CONCURRENT] ;then
            $current_batch=0
            wait
        fi
    done
    wait

    
}

if [ -z "$THREAD" ] ;then 
    download_thread $from $to
else
    download_seq $from $to
fi

exit 0

