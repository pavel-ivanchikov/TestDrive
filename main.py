from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()


def create_and_upload_file(file_name='test.txt', file_content='hey dude!', folder_id=None):
    try:
        drive = GoogleDrive(gauth)

        file_metadata = {'title': f'{file_name}'}
        if folder_id:
            file_metadata['parents'] = [{'id': folder_id}]

        my_file = drive.CreateFile(file_metadata)
        my_file.SetContentString(file_content)
        my_file.Upload()

        return f'File {file_name} was successfully uploaded to folder {folder_id}.'
    except Exception as ex:
        return f'Got some troubles: {str(ex)}'


def main():
    folder_id = '1tw7XLgqcdxDTLidZdXumd1DMdRRCiHYH'
    print(create_and_upload_file('my_file.txt', 'Hello World!', folder_id))


if __name__ == '__main__':
    main()
