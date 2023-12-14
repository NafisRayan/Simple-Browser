import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import *
from qdarkstyle import load_stylesheet_pyqt5

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.setCentralWidget(self.tabs)

        # Tab Counter
        self.tab_count = 0

        # Other initialization code
        self.initialize_ui()

    def initialize_ui(self):
        # Apply dark stylesheet
        self.setStyleSheet(load_stylesheet_pyqt5())

        # Navigation Bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Back Button
        back_btn = QAction('⏮️', self)
        back_btn.setStatusTip('Back to the previous page')
        back_btn.triggered.connect(self.back_button_clicked)
        navbar.addAction(back_btn)

        # Forward Button
        forward_btn = QAction('⏭️', self)
        forward_btn.setStatusTip('Forward to the next page')
        forward_btn.triggered.connect(self.forward_button_clicked)
        navbar.addAction(forward_btn)

        # Reload Button
        reload_btn = QAction('🔄️', self)
        reload_btn.setStatusTip('Reload the page')
        reload_btn.triggered.connect(self.reload_button_clicked)
        navbar.addAction(reload_btn)

        # Home Button
        home_btn = QAction('🏡', self)
        home_btn.setStatusTip('Go home')
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Adding Spacer
        navbar.addSeparator()

        # Search Button
        search_btn = QAction('🔍', self)
        search_btn.setStatusTip('Search the web')
        search_btn.triggered.connect(self.search)
        navbar.addAction(search_btn)

        # New Tab Button
        new_tab_btn = QAction('➕', self)
        new_tab_btn.setStatusTip('Open a new tab')
        new_tab_btn.triggered.connect(self.new_tab)
        navbar.addAction(new_tab_btn)

        # Close Tab Button
        close_tab_btn = QAction('❌', self)
        close_tab_btn.setStatusTip('Close the current tab')
        close_tab_btn.triggered.connect(self.close_current_tab)
        navbar.addAction(close_tab_btn)

        # Stop Button
        stop_btn = QAction('⛔', self)
        stop_btn.setStatusTip('Stop loading the current page')
        stop_btn.triggered.connect(self.stop_button_clicked)
        navbar.addAction(stop_btn)

        # Home Page
        self.add_new_tab(QUrl("http://www.ecosia.org"))

    def back_button_clicked(self):
        if self.current_browser() is not None:
            self.current_browser().back()

    def forward_button_clicked(self):
        if self.current_browser() is not None:
            self.current_browser().forward()

    def reload_button_clicked(self):
        if self.current_browser() is not None:
            self.current_browser().reload()

    def stop_button_clicked(self):
        if self.current_browser() is not None:
            self.current_browser().stop()

    def new_tab(self, qurl=None):
        if qurl is None or isinstance(qurl, bool):
            qurl = QUrl('http://www.ecosia.org')

        browser = QWebEngineView()
        browser.setUrl(qurl)
        browser.titleChanged.connect(lambda title, browser=browser: self.update_tab_title(browser, title))

        i = self.tabs.addTab(browser, browser.title())
        self.tabs.setCurrentIndex(i)

        # Update the tab count
        self.tab_count += 1

        # Update the URL bar
        self.update_urlbar(qurl, browser)

    def update_tab_title(self, browser, title):
        index = self.tabs.indexOf(browser)
        if index != -1:
            self.tabs.setTabText(index, title)

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.new_tab()

    def current_tab_changed(self, i):
        qurl = self.current_browser().url()
        self.update_urlbar(qurl, self.current_browser())

    def close_current_tab(self):
        if self.tabs.count() < 2:
            return

        index = self.tabs.currentIndex()
        self.tabs.removeTab(index)

    def current_browser(self):
        if self.tabs.count() > 0:
            return self.tabs.currentWidget()
        else:
            return None

    def update_urlbar(self, q, browser=None):
        if browser is None:
            browser = self.current_browser()

        if browser is not None and browser != self.current_browser():
            return

        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.current_browser().setUrl(q)

    def navigate_home(self):
        self.current_browser().setUrl(QUrl("http://www.ecosia.org"))

    def search(self):
        search_query = self.url_bar.text()
        search_url = QUrl(f"http://www.google.com/search?q={search_query}")

        if search_query and search_query.strip():
            self.current_browser().setUrl(search_url)
        else:
            QMessageBox.warning(self, "Search", "Please enter a search query.")

    def add_new_tab(self, qurl=QUrl('')):
        if qurl == '':
            qurl = QUrl('http://www.ecosia.org')

        browser = QWebEngineView()
        browser.setUrl(qurl)
        browser.titleChanged.connect(lambda title, browser=browser: self.update_tab_title(browser, title))

        i = self.tabs.addTab(browser, browser.title())
        self.tabs.setCurrentIndex(i)

        # Update the tab count
        self.tab_count += 1

        # Update the URL bar
        self.update_urlbar(qurl, browser)


app = QApplication(sys.argv)
QApplication.setApplicationName("R-Browser")
window = Browser()
window.showMaximized()
app.exec_()
