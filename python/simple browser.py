import sys
import os
from PyQt5.QtCore import QUrl, Qt, QSize
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QToolBar, 
                             QLineEdit, QAction, QMenu, QInputDialog)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Terminal Browser")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # Create toolbar
        nav_toolbar = QToolBar()
        self.addToolBar(nav_toolbar)

        # Back button
        back_btn = QAction(QIcon(os.path.join('icons', 'bx-left-arrow-alt.svg')), "", self)
        back_btn.setToolTip("Back")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        nav_toolbar.addAction(back_btn)

        # Forward button
        forward_btn = QAction(QIcon(os.path.join('icons', 'bx-right-arrow-alt.svg')), "", self)
        forward_btn.setToolTip("Forward")
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        nav_toolbar.addAction(forward_btn)

        # Reload button
        reload_btn = QAction(QIcon(os.path.join('icons', 'bx-refresh.svg')), "", self)
        reload_btn.setToolTip("Reload")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        nav_toolbar.addAction(reload_btn)

        # Home button
        home_btn = QAction(QIcon(os.path.join('icons', 'bx-home.svg')), "", self)
        home_btn.setToolTip("Home")
        home_btn.triggered.connect(self.navigate_home)
        nav_toolbar.addAction(home_btn)
        
        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_toolbar.addWidget(self.url_bar)

        # New tab button
        new_tab_btn = QAction(QIcon(os.path.join('icons', 'bx-plus.svg')), "", self)
        new_tab_btn.setToolTip("New Tab")
        new_tab_btn.triggered.connect(self.add_new_tab)
        nav_toolbar.addAction(new_tab_btn)

        # Bookmarks menu
        bookmark_menu = QMenu(self)
        bookmark_menu.setIcon(QIcon(os.path.join('icons', 'bx-bookmark.svg')))
        self.bookmark_action = self.menuBar().addMenu(bookmark_menu)

        add_bookmark_action = QAction(QIcon(os.path.join('icons', 'bx-bookmark.svg')), "Add Bookmark", self)
        add_bookmark_action.triggered.connect(self.add_bookmark)
        bookmark_menu.addAction(add_bookmark_action)

        self.bookmarks = {}

        # Add initial tab
        self.add_new_tab()

    def add_new_tab(self, qurl=None):
        if qurl is None:
            qurl = QUrl("https://www.google.com")
        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, QIcon(os.path.join('icons', 'bx-window.svg')), "New Tab")
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: 
                                     self.tabs.setTabText(i, browser.page().title()))

    def current_tab(self):
        return self.tabs.currentWidget()

    def navigate_home(self):
        self.current_tab().setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")
        
        if " " in self.url_bar.text() or "." not in self.url_bar.text():
            q = QUrl(f"https://www.google.com/search?q={self.url_bar.text()}")

        self.current_tab().setUrl(q)

    def update_url(self, q, browser=None):
        if browser != self.current_tab():
            return
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def close_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def add_bookmark(self):
        url = self.current_tab().url().toString()
        title, ok = QInputDialog.getText(self, "Add Bookmark", "Enter bookmark name:")
        if ok and title:
            self.bookmarks[title] = url
            bookmark_action = QAction(QIcon(os.path.join('icons', 'bx-bookmark.svg')), title, self)
            bookmark_action.triggered.connect(lambda _, url=url: self.open_bookmark(url))
            self.bookmark_action.menu().addAction(bookmark_action)

    def open_bookmark(self, url):
        self.current_tab().setUrl(QUrl(url))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set icon size for the application
    app.setStyleSheet("""
        QToolBar { icon-size: 20px; }
        QMenu { icon-size: 16px; }
    """)
    
    browser = Browser()
    app.setWindowIcon(QIcon(os.path.join('icons', 'bx-terminal.svg')))
    browser.show()
    sys.exit(app.exec_())