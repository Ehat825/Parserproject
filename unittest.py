import unittest
from unittest.mock import mock_open, patch

from c:/Users/ehatt/OneDrive - Metropolitan State University of Denver (MSU Denver)/proglangs.parser import write_output_file

class TestWriteOutputFile(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    def test_write_output_file(self, mock_open):
        output_path = "test_output.txt"
        original_code = "public class Test {}"
        updated_code = "public class Test {\n}"

        write_output_file(output_path, original_code, updated_code)

        # Check that the file was opened correctly
        mock_open.assert_called_once_with(output_path, 'w')

        # Check the content written to the file
        handle = mock_open()
        handle.write.assert_any_call("Original Java Program:\n")
        handle.write.assert_any_call(original_code)
        handle.write.assert_any_call("\n\nUpdated Java Program:\n")
        handle.write.assert_any_call(updated_code)

if __name__ == "__main__":
    unittest.main()