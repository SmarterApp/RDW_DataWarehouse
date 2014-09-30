'''
Created on Aug 11, 2014

@author: tosako
'''
import unittest
import tempfile
import os
from smarter_score_batcher.utils.metadata_generator import metadata_generator_top_down, \
    metadata_generator_bottom_up, FileMetadata
import uuid
from smarter_score_batcher.error.exceptions import MetadataDirNotExistException


class Test(unittest.TestCase):

    def setUp(self):
        self.__temp_dir = tempfile.TemporaryDirectory()
        self.__prepare_dirs()

    def tearDown(self):
        self.__temp_dir.cleanup()

    def __prepare_dirs(self):
        self.__dir1 = os.path.join(self.__temp_dir.name, 'dir1')
        self.__dir2 = os.path.join(self.__temp_dir.name, 'dir2')
        self.__dir3 = os.path.join(self.__dir1, 'dir3')
        os.makedirs(self.__dir1, exist_ok=True)
        os.makedirs(self.__dir2, exist_ok=True)
        os.makedirs(self.__dir3, exist_ok=True)
        self.__file1 = os.path.join(self.__dir1, 'file1')
        self.__file2 = os.path.join(self.__dir1, 'file2')
        self.__file3 = os.path.join(self.__dir2, 'file3')
        self.__file4 = os.path.join(self.__dir3, 'file4')
        with open(self.__file1, 'w') as f:
            f.write('hello word')
        with open(self.__file2, 'w') as f:
            f.write('good morning')
        with open(self.__file3, 'w') as f:
            f.write('this is test file')
        with open(self.__file4, 'w') as f:
            f.write('good bye')

    def __assertMetadata(self):
        root_metadata = os.path.join(self.__temp_dir.name, '.metadata')
        metadata1 = os.path.join(self.__dir1, '.metadata')
        metadata2 = os.path.join(self.__dir2, '.metadata')
        metadata3 = os.path.join(self.__dir3, '.metadata')
        self.assertTrue(os.path.exists(root_metadata))
        self.assertTrue(os.path.exists(metadata1))
        self.assertTrue(os.path.exists(metadata2))
        self.assertTrue(os.path.exists(metadata3))
        lines = []
        with open(root_metadata) as metadata_root:
            for l in metadata_root:
                lines.append(l.rstrip())
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].startswith('d:dir1:30:'))
        self.assertTrue(lines[1].startswith('d:dir2:17:'))
        lines = []
        with open(metadata1) as metadata_f1:
            for l in metadata_f1:
                lines.append(l.rstrip())
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith('d:dir3:8:'))
        self.assertTrue(lines[1].startswith('f:file1:10:'))
        self.assertTrue(lines[2].startswith('f:file2:12:'))

        lines = []
        with open(metadata2) as metadata_f2:
            for l in metadata_f2:
                lines.append(l.rstrip())
        self.assertEqual(len(lines), 1)
        self.assertTrue(lines[0].startswith('f:file3:17:'))

        lines = []
        with open(metadata3) as metadata_f3:
            for l in metadata_f3:
                lines.append(l.rstrip())
        self.assertEqual(len(lines), 1)
        self.assertTrue(lines[0].startswith('f:file4:8:'))

    def test_metadata_generator_top_down(self):
        metadata_generator_top_down(self.__temp_dir.name)
        self.__assertMetadata()

    def test_metadata_generator_bottom_up(self):
        metadata_generator_top_down(self.__temp_dir.name)
        file5 = os.path.join(self.__dir3, 'file5')
        with open(file5, 'w') as f:
            f.write('well hello again')
        metadata_generator_bottom_up(file5)
        metadata3 = os.path.join(self.__dir3, '.metadata')
        lines = []
        with open(metadata3) as metadata_f3:
            for l in metadata_f3:
                lines.append(l.rstrip())
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].startswith('f:file4:8:'))
        self.assertTrue(lines[1].startswith('f:file5:16:'))
        root_metadata = os.path.join(self.__temp_dir.name, '.metadata')
        lines = []
        with open(root_metadata) as metadata_f:
            for l in metadata_f:
                lines.append(l.rstrip())
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].startswith('d:dir1:46:'))
        self.assertTrue(lines[1].startswith('d:dir2:17:'))

        os.remove(file5)
        metadata_generator_bottom_up(file5)
        self.__assertMetadata()

    def test_metadata_generator_top_down_invalid_dir(self):
        fake_dir = os.path.join(self.__temp_dir.name, 'fake')
        self.assertRaises(MetadataDirNotExistException, metadata_generator_top_down, fake_dir)

    def test_FileMetadata_invalid_dir(self):
        fake_dir = os.path.join(self.__temp_dir.name, 'fake')
        self.assertRaises(MetadataDirNotExistException, FileMetadata, fake_dir)

    def test_FileMetadata_read_skip(self):
        dir_path = os.path.join(self.__temp_dir.name, str(uuid.uuid4()))
        os.makedirs(dir_path)
        open(os.path.join(dir_path, '.metadata'), 'a').close()
        with FileMetadata(dir_path) as meta:
            read_meta = meta.read_files(force=False)
        self.assertFalse(read_meta)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
