import unittest
from unittest.mock import patch
from plotting import main
import os


class TestPlotting(unittest.TestCase):
    """
    Unit tests for the plotting component.
    """

    @patch('plotting.plt.savefig')
    @patch('plotting.plt.plot')
    @patch('plotting.plt.xlabel')
    @patch('plotting.plt.ylabel')
    @patch('plotting.plt.title')
    @patch('plotting.pd.read_csv')
    def test_plotting(self, mock_read_csv, mock_title, mock_ylabel, mock_xlabel, mock_plot, mock_savefig):
        """
        Test the behavior of the main function in generating a plot.

        This test verifies that the main function correctly generates a plot with RTT data
        loaded from a mock CSV file. It mocks the necessary plotting functions and pandas
        read_csv function to simulate plotting without actually generating a plot.

        It checks if the plot functions are called with the correct arguments and if the
        plot is saved with the expected filename.

        After running the test, it cleans up by deleting the generated plot file.
        """
        # Create a mock CSV file with RTT data
        mock_read_csv.return_value = {'RTT': [10, 20, 30], 'Smoothed RTT': [12, 22, 32]}

        # Run the main function to generate the plot
        main()

        # Verify that the plot functions are called with the correct arguments
        mock_title.assert_called_once_with('RTT across time - FILE_NAME')
        mock_ylabel.assert_called_once_with('RTT value')
        mock_xlabel.assert_called_once_with('Packets')
        mock_plot.assert_called_once_with([10, 20, 30], color='blue', label='RTT')
        mock_plot.assert_called_once_with([12, 22, 32], color='red', label='Smoothed RTT')
        mock_savefig.assert_called_once_with('plots/RTTs_FILE_NAME.png')

        # Clean up - delete the generated plot file
        os.remove('plots/RTTs_FILE_NAME.png')


if __name__ == '__main__':
    unittest.main()
