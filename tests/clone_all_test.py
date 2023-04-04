from async_load import clone_all
import unittest
from unittest.mock import patch
import os
import stat


class CloneAllTest(unittest.IsolatedAsyncioTestCase):
    TEST_DATA_FOLDER = "test_data"
    EXP_H = '3b1e30ead589eec67801b99a0ef147145db02b05f35376b30137691d97b96ac3'

    def setUp(self):
        isExist = os.path.exists(CloneAllTest.TEST_DATA_FOLDER)
        if not isExist:
            # create folder if not exists
            os.makedirs(CloneAllTest.TEST_DATA_FOLDER)
        else:
            # clear TEST_DATA_FOLDER folder
            CloneAllTest.clearTree(CloneAllTest.TEST_DATA_FOLDER)
        self.create_test_data("1")
        self.create_test_data("2")
        self.create_test_data("3")

    def create_test_data(self, sub_dir):
        os.makedirs(os.path.join(CloneAllTest.TEST_DATA_FOLDER, sub_dir))
        f1 = os.path.join(CloneAllTest.TEST_DATA_FOLDER, sub_dir, "test.txt")
        with open(f1, "w") as file:
            file.write("hash calculation test")

    def tearDown(self):
        # clear TEST_DATA_FOLDER folder
        CloneAllTest.clearTree(CloneAllTest.TEST_DATA_FOLDER)

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

    async def test_success_loading(self):
        with patch('async_load.clone_rep') as mock:
            mock.return_value = True
            result = await clone_all(CloneAllTest.TEST_DATA_FOLDER)
            self.assertEqual(result[0], CloneAllTest.EXP_H)
            self.assertEqual(result[1], CloneAllTest.EXP_H)
            self.assertEqual(result[2], CloneAllTest.EXP_H)
