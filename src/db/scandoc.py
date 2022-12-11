import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from pyscanner import Scanner

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Document Scanner')
        self.setGeometry(100, 100, 600, 400)

        # Create a button to start the scan
        scan_button = QPushButton('Scan', self)
        scan_button.setGeometry(10, 10, 100, 50)

        # Connect the button's clicked signal to the scan() method
        scan_button.clicked.connect(self.scan)

    def scan(self):
        # Create an instance of the Scanner class
        scanner = Scanner('My Scanner')

        # Scan a document from the scanner and save it to a file
        scanner.scan(output_file='scanned_document.pdf')

        # Close the connection to the scanner
        scanner.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
