from sqlite_plugin import write_checksum, read_checksum, nuke
import unittest, time
from shutil import copyfile
from helpers import fork

class JRETester(unittest.TestCase):
    def setUp(self):

        nuke()
        # copyfile("checksum.db", "checksum.db.bak")


    # def tearDown(self):
    #     copyfile("checksum.db", "checksum.test")
    #     copyfile("checksum.db.bak", "checksum.db")


    def test_download_episode(self):
        pass

    def test_already_downloaded_episode(self):
        pass
    def test_download_broken_episode(self):
        pass
        
    def test_can_write_to_database(self):
        episode = 9000
        hashsum = "foobar"
        write_checksum(episode, hashsum)
        read_hash = read_checksum(episode)[0]
        self.assertEqual(hashsum, read_hash)

    def test_threading(self):

        for i in range(1,200):
            fork(i)


if __name__ == '__main__':
    unittest.main()
