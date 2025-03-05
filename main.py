from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# Инициализация GoogleAuth
gauth = GoogleAuth()

# Проверяем, существует ли уже сохраненный токен
if os.path.exists('token.json'):
    gauth.LoadCredentialsFile('token.json')  # Загружаем сохраненные учетные данные
else:
    # Если токена нет, запускаем полный процесс авторизации
    gauth.LocalWebserverAuth()
    gauth.SaveCredentialsFile('token.json')  # Сохраняем токен для будущих запусков

# Инициализация GoogleDrive
drive = GoogleDrive(gauth)


def change_file(file_name='test.txt', additional_content='hey dude!', folder_id=None):
    try:
        # Поиск файла по имени и папке
        query = f"title = '{file_name}' and trashed = false"
        if folder_id:
            query += f" and '{folder_id}' in parents"

        file_list = drive.ListFile({'q': query}).GetList()

        if not file_list:
            return f"File '{file_name}' not found in folder '{folder_id}'."

        # Получаем первый найденный файл (предполагаем, что файл с таким именем один)
        my_file = file_list[0]

        # Читаем текущее содержимое файла
        current_content = my_file.GetContentString()

        # Добавляем новое содержимое
        updated_content = current_content + "\n" + additional_content

        # Обновляем файл
        my_file.SetContentString(updated_content)
        my_file.Upload()

        return f"File '{file_name}' was successfully updated in folder '{folder_id}'."
    except Exception as ex:
        return f'Got some troubles: {str(ex)}'


def create_and_upload_file(file_name='test.txt', file_content='hey dude!', folder_id=None):
    try:

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

    # Создаем и загружаем файл
    print(create_and_upload_file('my_file1.txt', 'Hello World!', folder_id))

    # Изменяем файл
    print(change_file('my_file1.txt', 'This is additional content.', folder_id))


if __name__ == '__main__':
    main()