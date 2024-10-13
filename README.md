# Advanced Browser

Advanced Browser is a custom web browser application built using Python and PyQt5. It provides a variety of features, including tabbed browsing, a customizable search engine, private browsing, and bookmark management. This project demonstrates the integration of PyQt5's `QWebEngineView` for rendering web pages and several useful tools to improve the user experience.

## Features

- **Tabbed Browsing**: Easily open multiple tabs and reorder them.
- **Private Browsing**: Toggle private mode to avoid storing history and cookies.
- **Customizable Search Engine**: Choose between Google, Bing, and DuckDuckGo as the default search engine.
- **Bookmark Management**: Add, view, and navigate bookmarks for quick access to favorite sites.
- **History**: View and revisit browsing history directly from the browser.
- **Search in Page**: Search text within the current web page.
- **Keyboard Shortcuts**:
  - `Ctrl+T`: Open a new tab.
  - `Ctrl+R`: Reload the current tab.
  - `Ctrl+D`: Add a bookmark.
  - `Ctrl+N`: Open a new browser window.
  - `Ctrl+,`: Open settings.

## Installation

### Prerequisites
- Python 3.x
- PyQt5: Install via pip using the following command:
  ```bash
  pip install PyQt5 PyQtWebEngine
  ```

### Running the Project
To run the browser, navigate to the project directory and execute the following command:
```bash
python simple_browser.py
```

## Customization

You can modify the default search engine by navigating to **Settings** and selecting one of the available options: Google, Bing, or DuckDuckGo.

## Usage

- **Navigating the Web**: Enter a URL in the address bar or search for a term, and the browser will load the corresponding page or search result.
- **Adding Bookmarks**: Press `Ctrl+D` to add the current page to bookmarks, which can be accessed from the bookmarks menu.
- **Private Browsing**: Enable private browsing to browse without leaving history or storing cookies.

## Known Issues

- The browser doesn't support advanced security features like HTTPS certificate validation.
- Limited support for browser extensions or advanced developer tools.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your improvements or suggestions.

## License

This project is licensed under the MIT License.

---

Feel free to modify this to match any specific requirements you have for your project!
