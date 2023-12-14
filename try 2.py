import sys
import json
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class BrowserTab(QWidget):
    def __init__(self, url="http://google.com"):
        super().__init__()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))

        self.nav_bar = QToolBar()
        self.setup_toolbar()

        layout = QVBoxLayout(self)
        layout.addWidget(self.nav_bar)
        layout.addWidget(self.browser)

    def setup_toolbar(self):
        actions = {
            'Back': self.browser.back,
            'Forward': self.browser.forward,
            'Reload': self.browser.reload,
            'Home': lambda: self.browser.setUrl(QUrl('http://google.com')),
            'Bookmark': self.add_bookmark,
        }

        for action_text, action_method in actions.items():
            action = QAction(action_text, self)
            action.triggered.connect(action_method)
            self.nav_bar.addAction(action)

        url_bar = QLineEdit()
        url_bar.returnPressed.connect(lambda: self.browser.setUrl(QUrl(url_bar.text())))
        self.nav_bar.addWidget(url_bar)

        self.add_close_button()

        self.browser.urlChanged.connect(lambda q: self.update_tab_name())

    def add_bookmark(self):
        bookmark_url = self.browser.url().toString()
        QMessageBox.information(None, 'Bookmark Added', f'Bookmark for {bookmark_url} added successfully.')

    def add_close_button(self):
        close_btn = QPushButton("X")
        close_btn.clicked.connect(self.close_tab)
        self.nav_bar.addWidget(close_btn)

    def close_tab(self):
        index = browser_window.tab_widget.indexOf(self)
        browser_window.tab_widget.removeTab(index)

    def update_tab_name(self):
        title = self.browser.page().title()
        if not title:
            title = "New Tab"
        index = browser_window.tab_widget.indexOf(self)
        browser_window.tab_widget.setTabText(index, title)
        browser_window.tab_widget.setTabToolTip(index, title)

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('My Chrome-like Browser')
        self.setGeometry(100, 100, 1200, 800)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.add_tab()  # Initial tab

        self.setup_toolbar()
        self.showMaximized()

    def add_tab(self, url="http://ecosia.org"):
        browser_tab = BrowserTab(url)
        index = self.tab_widget.addTab(browser_tab, browser_tab.browser.page().title())
        self.tab_widget.setCurrentIndex(index)

    def setup_toolbar(self):
        toolbar = self.addToolBar("Toolbar")

        # Add a "+" button to create a new tab
        plus_btn = QPushButton("+")
        plus_btn.clicked.connect(self.add_new_tab)
        toolbar.addWidget(plus_btn)

        # Add other actions to the toolbar if needed
        actions = {
            'Back': self.tab_widget.currentWidget().browser.back,
            'Forward': self.tab_widget.currentWidget().browser.forward,
            'Reload': self.tab_widget.currentWidget().browser.reload,
            'Home': lambda: self.tab_widget.currentWidget().browser.setUrl(QUrl('http://google.com')),
        }

        for action_text, action_method in actions.items():
            action = QAction(action_text, self)
            action.triggered.connect(action_method)
            toolbar.addAction(action)

    def add_new_tab(self):
        self.add_tab()

def main():
    app = QApplication(sys.argv)
    global browser_window
    browser_window = BrowserWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
