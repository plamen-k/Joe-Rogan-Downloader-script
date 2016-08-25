import sys, os,time, random

# bucket of episodes
# global episodes

def forker(episode, processing_list):
    processing_list.append(episode)
    # a bucket of pids
    # the maximum number of pids in the bucket
    bucket_limit = 5

    childpid = os.fork()
    if childpid == 0:
        time.sleep(2)
        # write_checksum(episode, random.randint())
        print "I am the kid\n"
        os._exit(0)

    else:
        processing_list.append(childpid)
        # when the bucket limit is reached, wait for all the children to exit and fill the bucket again
        if len(processing_list) == bucket_limit:
            for pid in processing_list:
                print "Waiting for %d items to exit" % len(processing_list)
                pid, status = os.waitpid(pid, 0)
                processing_list.remove(pid)
            # resets bucket

    print 'Having items, '.join(processing_list)
