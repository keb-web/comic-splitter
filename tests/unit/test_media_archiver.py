# from unittest.mock import patch


# don't actually need an archiver since we shouldn't save templates,
# should be provided by the user, simply just check if a template exists
# class TestMediaArchiver:
#
#     def test_archiver_saves_payload(self, tmp_path):
#         path = '/media/dummy-comic-dummy-author/ch-1/pg-1'
#         file_path = tmp_path / path / ''
#         payload = b'page_data'
#         archiver = MediaArchiver()
#         archiver.archive(path, payload)
#         print(tmp_path)
