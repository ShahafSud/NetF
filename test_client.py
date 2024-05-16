import unittest
from client import divide_file_into_chunks


class TestClient(unittest.TestCase):
    """
    Unit tests for the client component.
    """

    def test_file_division(self):
        """
        Test the behavior of the divide_file_into_chunks function.

        This test verifies that the divide_file_into_chunks function correctly divides
        a file into chunks of the specified buffer size. It creates a mock file with known
        content, divides it into chunks using the function, and compares the result with
        the expected chunks.

        The mock file content is 'abcdefghijk' and the buffer size is set to 4. Therefore,
        the expected chunks should be ['abcd', 'efgh', 'ijk'].

        This test checks if the function behaves as expected for file division.
        """
        # Create a mock file with known content
        mock_file_content = b'abcdefghijk'
        with open('mock_file.txt', 'wb') as f:
            f.write(mock_file_content)

        # Divide the mock file into chunks
        chunks = divide_file_into_chunks('mock_file.txt', buffer_size=4)

        # Verify that the file is divided correctly
        expected_chunks = [b'abcd', b'efgh', b'ijk']
        self.assertEqual(chunks, expected_chunks)


if __name__ == '__main__':
    unittest.main()
