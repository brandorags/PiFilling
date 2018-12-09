class FileMetadata(object):

    def __init__(self, filename, file_size, file_type, modified_date, is_directory):
        self.filename = filename
        self.file_size = file_size
        self.file_type = file_type
        self.modified_date = modified_date
        self.is_directory = is_directory

    def to_json(self):
        """
        Returns a dictionary with keys in the JSON standard
        camel case format.

        :return: a JSON version of FileMetadata
        """
        return {
            'filename': self.filename,
            'fileSize': self.file_size,
            'fileType': self.file_type,
            'modifiedDate': self.modified_date,
            'isDirectory': self.is_directory
        }
