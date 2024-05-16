import unittest
from unittest.mock import patch, MagicMock
from server import handle_stream


class TestServer(unittest.TestCase):
    async def test_handle_stream(self):
        with patch('sys.argv', ['test_server.py', '0']):  # Patch sys.argv within the context
            # Mock the reader and writer objects
            mock_reader = MagicMock()
            mock_writer = MagicMock()

            # Call the handle_stream function with mocked reader and writer
            await handle_stream(mock_reader, mock_writer)

            # Assert the behavior of the mocked objects
            mock_writer.write_eof.assert_called_once()  # Ensure write_eof is called once
            mock_reader.read.assert_called()  # Ensure read is called
            mock_writer.write.assert_called()  # Ensure write is called


if __name__ == '__main__':
    unittest.main()
