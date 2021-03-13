from sqlalchemy import text
from app import db
from app.database.entities import DirectoryPath, Filename
from app.models.file_index import FileIndex
from app.util.directory_content_parser import DirectoryContentParser


class FileIndexService(object):

    @staticmethod
    def get_file_path_wildcard(user_id, partial_filename):
        file_paths = []

        sql = text("""SELECT
                        dp.absolute_path,
                        f.filename
                      FROM filename f
                      JOIN directory_path dp ON f.directory_id = dp.id AND f.user_id = dp.user_id
                      WHERE f.user_id = :user_id
                      AND f.filename LIKE :partial_filename""")

        results = db.engine.execute(sql, {'user_id': user_id, 'partial_filename': '%' + partial_filename + '%'})

        for result in results:
            absolute_path = result[0]
            filename = result[1]
            file_path = FileIndex(filename=filename, directory_name=None,
                                  absolute_path=absolute_path, is_directory=False)

            file_paths.append(file_path)

        return file_paths

    @staticmethod
    def save_file_path(user_id, file_path, absolute_path):
        # save the directory path to the database if it doesn't exist
        existing_directory_path = FileIndexService.get_directory_path(absolute_path)
        if existing_directory_path:
            directory_id = existing_directory_path.id
        else:
            new_directory_path = FileIndexService.save_directory_path(user_id, absolute_path)
            directory_id = new_directory_path.id

        # save the filename to the database
        file_metadata = DirectoryContentParser.get_file(file_path)
        file = Filename(user_id=user_id, directory_id=directory_id, filename=file_metadata.filename)

        db.session.add(file)
        db.session.commit()

        return file_metadata

    @staticmethod
    def get_directory_path(absolute_path):
        return DirectoryPath.query.filter_by(absolute_path=absolute_path).first()

    @staticmethod
    def get_directory_path_wildcard(user_id, partial_directory_name):
        directory_paths = []

        sql = text("""SELECT
                        absolute_path,
                        directory_name
                      FROM directory_path
                      WHERE user_id = :user_id
                      AND directory_name LIKE :partial_directory_name""")

        results = db.engine.execute(sql, {'user_id': user_id,
                                          'partial_directory_name': '%' + partial_directory_name + '%'})

        for result in results:
            absolute_path = result[0]
            directory_name = result[1]
            directory_path = FileIndex(filename=None, directory_name=directory_name,
                                       absolute_path=absolute_path, is_directory=True)

            directory_paths.append(directory_path)

        return directory_paths

    @staticmethod
    def save_directory_path(user_id, absolute_path):
        split_absolute_path = absolute_path.split('/')
        directory_name = split_absolute_path[-1]

        new_directory_path = DirectoryPath(user_id=user_id, absolute_path=absolute_path,
                                           directory_name=directory_name)

        db.session.add(new_directory_path)
        db.session.commit()

        return new_directory_path
