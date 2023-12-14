import sys
import json
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

app = QApplication(sys.argv)
app.setApplicationName('My Cool Browser')

# Load bookmarks from the JSON file
def load_bookmarks():
    try:
        with open('database.json', 'r') as file:
            bookmarks_data = json.load(file)
            return bookmarks_data.get('bookmarks', [])
    except FileNotFoundError:
        return []

# Save bookmarks to the JSON file
def save_bookmarks(bookmarks):
    bookmarks_data = {'bookmarks': bookmarks}
    with open('database.json', 'w') as file:
        json.dump(bookmarks_data, file, indent=2)

# Add a bookmark
def add_bookmark(browser, bookmarks):
    bookmark_url = browser.url().toString()
    if bookmark_url not in bookmarks:
        bookmarks.append(bookmark_url)
        save_bookmarks(bookmarks)
        QMessageBox.information(None, 'Bookmark Added', f'Bookmark for {bookmark_url} added successfully.')

# Open a new tab when the "+" button is clicked
def open_new_tab():
    new_browser = QWebEngineView()
    new_browser.setUrl(QUrl('http://google.com'))
    index = tab_widget.addTab(new_browser, f"Tab {tab_widget.count() + 1}")
    tab_bar.setTabButton(index, QTabBar.RightSide, create_plus_button())
    tab_bar.setTabButton(index - 1, QTabBar.RightSide, create_close_button(index - 1))

# Create "+" button for new tab
def create_plus_button():
    plus_btn = QPushButton("+")
    plus_btn.clicked.connect(open_new_tab)
    return plus_btn

# Create "X" button to close the tab
def create_close_button(tab_index):
    close_btn = QPushButton("X")
    close_btn.clicked.connect(lambda: close_tab(tab_index))
    return close_btn

# Close the tab
def close_tab(tab_index):
    tab_widget.removeTab(tab_index)

# Main window setup
browser = QWebEngineView()
browser.setUrl(QUrl('http://google.com'))

# Tabs setup
tab_widget = QTabWidget()
tab_widget.addTab(browser, "Tab 1")

navbar = QToolBar()

back_btn = QAction('←')
back_btn.triggered.connect(browser.back)
navbar.addAction(back_btn)

forward_btn = QAction('→')
forward_btn.triggered.connect(browser.forward)
navbar.addAction(forward_btn)

reload_btn = QAction('↻')
reload_btn.triggered.connect(browser.reload)
navbar.addAction(reload_btn)

home_btn = QAction('Home')
home_btn.triggered.connect(lambda: browser.setUrl(QUrl('http://programming-hero.com')))
navbar.addAction(home_btn)

bookmark_btn = QAction('Bookmark')
bookmark_btn.triggered.connect(lambda: add_bookmark(browser, bookmarks))
navbar.addAction(bookmark_btn)

url_bar = QLineEdit()
url_bar.returnPressed.connect(lambda: browser.setUrl(QUrl(url_bar.text())))
navbar.addWidget(url_bar)

# Add "+" button for new tab
tab_bar = tab_widget.tabBar()
index = tab_widget.addTab(browser, "Tab 1")
tab_bar.setTabButton(index, QTabBar.RightSide, create_plus_button())

browser.urlChanged.connect(lambda q: url_bar.setText(q.toString()))

# Load bookmarks from the JSON file
bookmarks = load_bookmarks()

# Main window setup
main_window = QWidget()

# Set up main layout
main_layout = QVBoxLayout(main_window)
main_layout.addWidget(navbar)
main_layout.addWidget(tab_widget)

# Show the main window
main_window.showMaximized()

sys.exit(app.exec_())
