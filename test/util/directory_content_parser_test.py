import unittest
import subprocess

from app.util.directory_content_parser import DirectoryContentParser
from app.models.file_metadata import FileMetadata


class DirectoryContentParserTest(unittest.TestCase):

    def setUp(self):
        temp_dir = 'temp_directory'
        subprocess.run(['mkdir', temp_dir])

        for i in range(0, 5):
            with open(temp_dir + '/temp' + str(i) + '.txt', 'w') as file:
                file.write('Test test test')

        subprocess.run(['mkdir', temp_dir + '/temp_directory1'])

    def tearDown(self):
        subprocess.run(['rm', '-rf', 'temp_directory'])

    def test_parse_directory_content(self):
        file_metadata_list = DirectoryContentParser.parse_directory_content('./temp_directory')
        file_metadata_first_item = file_metadata_list[0]

        self.assertEqual(len(file_metadata_list), 6)
        self.assertTrue(isinstance(file_metadata_first_item, FileMetadata))
        self.assertEqual(file_metadata_first_item.filename, 'temp0.txt')
        self.assertEqual(file_metadata_first_item.file_type, '.txt')
        self.assertIsNotNone(file_metadata_first_item.modified_date)
        self.assertIsNotNone(file_metadata_first_item.file_size)
        self.assertFalse(file_metadata_first_item.is_directory)

    def test_get_file(self):
        file_metadata = DirectoryContentParser.get_file('./temp_directory/temp0.txt')

        self.assertTrue(isinstance(file_metadata, FileMetadata))
        self.assertEqual(file_metadata.filename, 'temp0.txt')
        self.assertEqual(file_metadata.file_type, '.txt')
        self.assertIsNotNone(file_metadata.modified_date)
        self.assertIsNotNone(file_metadata.file_size)
        self.assertFalse(file_metadata.is_directory)


if __name__ == '__main__':
    unittest.main()
