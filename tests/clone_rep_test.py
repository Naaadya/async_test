from async_load import clone_rep
import asyncio
import os
import unittest
import stat


class CloneRepositoryTest(unittest.IsolatedAsyncioTestCase):
    TEST_DATA_FOLDER = "test_data"

    def setUp(self):
        isExist = os.path.exists(CloneRepositoryTest.TEST_DATA_FOLDER)
        if not isExist:
            # create folder if not exists
            os.makedirs(CloneRepositoryTest.TEST_DATA_FOLDER)
        else:
            # clear TEST_DATA_FOLDER folder
            CloneRepositoryTest.clearTree(CloneRepositoryTest.TEST_DATA_FOLDER)

    def tearDown(self):
        # clear TEST_DATA_FOLDER folder
        CloneRepositoryTest.clearTree(CloneRepositoryTest.TEST_DATA_FOLDER)

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

    async def test_clone_repository(self):
        loop = asyncio.get_event_loop()
        folder_path = f"{CloneRepositoryTest.TEST_DATA_FOLDER}\\1"
        res = await clone_rep(
            "https://github.com/Naaadya/tree_menu.git", folder_path, loop)
        self.assertTrue(res)
