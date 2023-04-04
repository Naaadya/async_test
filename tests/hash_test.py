from async_load import dir_hash
import os
import unittest
import stat


class HashTest(unittest.IsolatedAsyncioTestCase):
    TEST_DATA_FOLDER = "test_data"
    EXP_H = '3b1e30ead589eec67801b99a0ef147145db02b05f35376b30137691d97b96ac3'

    def setUp(self):
        isExist = os.path.exists(HashTest.TEST_DATA_FOLDER)
        if not isExist:
            # create folder if not exists
            os.makedirs(HashTest.TEST_DATA_FOLDER)
        else:
            # clear TEST_DATA_FOLDER folder
            HashTest.clearTree(HashTest.TEST_DATA_FOLDER)
        test_file_path = os.path.join(HashTest.TEST_DATA_FOLDER, "test.txt")
        with open(test_file_path, "w") as file:
            file.write("hash calculation test")

    def tearDown(self):
        # clear TEST_DATA_FOLDER folder
        HashTest.clearTree(HashTest.TEST_DATA_FOLDER)

    def clearTree(root):
        isExist = os.path.exists(root)
        if isExist:
            for root, dirs, files in os.walk(root, topdown=False):
                for name in files:
                    filename = os.path.join(root, name)
                    os.chmod(filename, stat.S_IWUSR)
                    os.remove(filename)
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

    def test_hash(self):
        actual = dir_hash(HashTest.TEST_DATA_FOLDER)
        self.assertEqual(actual, HashTest.EXP_H)
