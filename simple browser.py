import sys
import os
from PyQt5.QtCore import QUrl, Qt, QSize, QSettings
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QToolBar, 
                             QLineEdit, QAction, QMenu, QInputDialog, QDialog, 
                             QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QStyle)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon
import traceback

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        layout = QVBoxLayout(self)

        # Search Engine
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Default Search Engine:"))
        self.search_engine_combo = QComboBox()
        self.search_engine_combo.addItems(["Google", "Bing", "DuckDuckGo"])
        search_layout.addWidget(self.search_engine_combo)
        layout.addLayout(search_layout)

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        layout.addWidget(save_button)

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Browser")
        self.setGeometry(100, 100, 1200, 800)
        
        self.settings = QSettings("YourCompany", "AdvancedBrowser")
        self.load_settings()
        
        # Define profiles at the beginning
        self.default_profile = QWebEngineProfile.defaultProfile()
        self.private_profile = QWebEngineProfile()

        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setMovable(True)  # Allow tab reordering
        self.setCentralWidget(self.tabs)

        # Create toolbar
        nav_toolbar = QToolBar()
        self.addToolBar(nav_toolbar)

        # Back button
        back_btn = QAction(self.style().standardIcon(QStyle.SP_ArrowBack), "Back", self)
        back_btn.setShortcut("Alt+Left")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        nav_toolbar.addAction(back_btn)

        # Forward button
        forward_btn = QAction(self.style().standardIcon(QStyle.SP_ArrowForward), "Forward", self)
        forward_btn.setShortcut("Alt+Right")
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        nav_toolbar.addAction(forward_btn)

        # Reload button
        reload_btn = QAction(self.style().standardIcon(QStyle.SP_BrowserReload), "Reload", self)
        reload_btn.setShortcut("Ctrl+R")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        nav_toolbar.addAction(reload_btn)

        # Home button
        home_btn = QAction(self.style().standardIcon(QStyle.SP_DirHomeIcon), "Home", self)
        home_btn.setShortcut("Alt+Home")
        home_btn.triggered.connect(self.navigate_home)
        nav_toolbar.addAction(home_btn)
        
        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_toolbar.addWidget(self.url_bar)

        # New tab button
        self.new_tab_btn = QAction(self.style().standardIcon(QStyle.SP_FileIcon), "New Tab", self)
        self.new_tab_btn.setShortcut("Ctrl+T")
        self.new_tab_btn.triggered.connect(self.add_new_tab)
        nav_toolbar.addAction(self.new_tab_btn)
        print("New Tab button added to toolbar")

        # Bookmarks menu
        bookmark_menu = QMenu(self)
        bookmark_menu.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.bookmark_action = self.menuBar().addMenu(bookmark_menu)

        add_bookmark_action = QAction(self.style().standardIcon(QStyle.SP_DialogSaveButton), "Add Bookmark", self)
        add_bookmark_action.setShortcut("Ctrl+D")
        add_bookmark_action.triggered.connect(self.add_bookmark)
        bookmark_menu.addAction(add_bookmark_action)

        self.bookmarks = {}

        # Add a search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search in page...")
        self.search_bar.returnPressed.connect(self.search_in_page)
        nav_toolbar.addWidget(self.search_bar)

        # Add a history menu
        history_menu = QMenu(self)
        history_menu.setIcon(self.style().standardIcon(QStyle.SP_FileDialogContentsView))
        self.history_action = self.menuBar().addMenu(history_menu)

        # Settings button
        settings_btn = QAction(self.style().standardIcon(QStyle.SP_FileDialogInfoView), "Settings", self)
        settings_btn.setShortcut("Ctrl+,")
        settings_btn.triggered.connect(self.open_settings)
        nav_toolbar.addAction(settings_btn)

        # Private browsing button
        self.private_browsing_btn = QAction(self.style().standardIcon(QStyle.SP_DriveNetIcon), "Private Browsing", self)
        self.private_browsing_btn.setCheckable(True)
        self.private_browsing_btn.triggered.connect(self.toggle_private_browsing)
        nav_toolbar.addAction(self.private_browsing_btn)

        # Add New Window button
        new_window_btn = QAction(self.style().standardIcon(QStyle.SP_FileDialogNewFolder), "New Window", self)
        new_window_btn.setShortcut("Ctrl+N")
        new_window_btn.triggered.connect(self.open_new_window)
        nav_toolbar.addAction(new_window_btn)

        # Add initial tab
        self.add_new_tab()

        self.search_engine = self.settings.value("search_engine", "Google")
        
        print("Browser initialized")
        print(f"Number of tabs: {self.tabs.count()}")
        print(f"Current search engine: {self.search_engine}")

    def add_new_tab(self, qurl=None, label="New Tab"):
        try:
            if qurl is None or not isinstance(qurl, QUrl):
                qurl = QUrl(self.get_home_page())  # Ensure qurl is always a valid QUrl object

            profile = self.private_profile if self.private_browsing_btn.isChecked() else self.default_profile
            page = QWebEnginePage(profile, self)

            browser = QWebEngineView(self)
            browser.setPage(page)
            browser.setUrl(qurl)  # Ensure qurl is valid and passed to setUrl()

            i = self.tabs.addTab(browser, label)
            self.tabs.setCurrentIndex(i)

            browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url(qurl, browser))
            browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

            settings = browser.page().settings()
            settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)

        except Exception as e:
            print(f"Error in add_new_tab: {str(e)}")
            traceback.print_exc()


    def get_home_page(self):
        print(f"Getting home page for search engine: {self.search_engine}")
        if self.search_engine == "Google":
            return "https://www.google.com"
        elif self.search_engine == "Bing":
            return "https://www.bing.com"
        elif self.search_engine == "DuckDuckGo":
            return "https://duckduckgo.com"
        else:
            print(f"Unknown search engine: {self.search_engine}. Defaulting to Google.")
            return "https://www.google.com"


    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.search_engine_combo.setCurrentText(self.search_engine)
        if dialog.exec_():
            new_search_engine = dialog.search_engine_combo.currentText()
            if new_search_engine != self.search_engine:
                self.search_engine = new_search_engine
                self.settings.setValue("search_engine", new_search_engine)
                print(f"Search engine changed to {new_search_engine}")
                self.update_current_tab()

    def update_current_tab(self):
        current_tab = self.current_tab()
        if current_tab:
            current_tab.setUrl(QUrl(self.get_home_page()))

    def navigate_home(self):
        self.current_tab().setUrl(QUrl(self.get_home_page()))

    def current_tab(self):
        return self.tabs.currentWidget()

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")
        
        if " " in self.url_bar.text() or "." not in self.url_bar.text():
            search_query = self.url_bar.text()
            if self.search_engine == "Google":
                q = QUrl(f"https://www.google.com/search?q={search_query}")
            elif self.search_engine == "Bing":
                q = QUrl(f"https://www.bing.com/search?q={search_query}")
            elif self.search_engine == "DuckDuckGo":
                q = QUrl(f"https://duckduckgo.com/?q={search_query}")

        self.current_tab().setUrl(q)

    def update_url(self, q, browser=None):
        if browser != self.current_tab():
            return
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

        # Add to history
        title = self.current_tab().page().title()
        history_action = QAction(QIcon(os.path.join('icons', 'bx-link.svg')), f"{title} - {q.toString()}", self)
        history_action.triggered.connect(lambda _, url=q: self.open_url(url))
        self.history_action.menu().addAction(history_action)

    def open_url(self, url):
        self.current_tab().setUrl(url)

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

    def search_in_page(self):
        self.current_tab().findText(self.search_bar.text())

    def load_settings(self):
        self.search_engine = self.settings.value("search_engine", "Google")

    def toggle_private_browsing(self):
        if self.private_browsing_btn.isChecked():
            self.setWindowTitle("Advanced Browser (Private Mode)")
            # Create a new profile for each private browsing session
            self.private_profile = QWebEngineProfile()
        else:
            self.setWindowTitle("Advanced Browser")
        
        # Reload the current page with the new profile
        current_url = self.current_tab().url()
        self.add_new_tab(current_url)
        self.close_tab(self.tabs.currentIndex() - 1)

    def open_new_window(self):
        new_window = Browser()
        new_window.show()

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