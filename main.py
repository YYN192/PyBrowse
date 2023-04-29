import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

class BrowserTab(QWebEngineView):
    def __init__(self, url):
        super().__init__()
        self.load(QUrl(url))


class MainWindow(QMainWindow):
    def __init__(self):



        super().__init__()
        self.setWindowTitle('PyBrowse')

        # Set window iconlik
        self.setWindowIcon(QIcon('icon.png'))

        # Create taskbar icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('icon.png'))
        self.tray_icon.setVisible(True)

        # Set window icon again
        self.setWindowIcon(QIcon('icon.png'))
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.add_tab("https://www.duckduckgo.com")
        self.setCentralWidget(self.tab_widget)
        # Navigation bar
        navbar = QToolBar()
        self.addToolBar(navbar)
        # Set font size and icon size
        font = navbar.font()
        font.setPointSize(14)
        navbar.setFont(font)
        navbar.setIconSize(QSize(32, 32))
        back_btn = QAction('←', self)
        back_btn.triggered.connect(self.active_browser().back)
        navbar.addAction(back_btn)
        forward_btn = QAction('→', self)
        forward_btn.triggered.connect(self.active_browser().forward)
        navbar.addAction(forward_btn)
        reload_btn = QAction('↻', self)
        reload_btn.triggered.connect(self.active_browser().reload)
        navbar.addAction(reload_btn)
        home_btn = QAction('⌂', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)
        zoom_in_btn = QAction('+', self)
        zoom_in_btn.triggered.connect(self.zoom_in)
        navbar.addAction(zoom_in_btn)
        zoom_out_btn = QAction('-', self)
        zoom_out_btn.triggered.connect(self.zoom_out)
        navbar.addAction(zoom_out_btn)
        # Add keyboard shortcuts
        new_tab_shortcut = QShortcut(QKeySequence('Ctrl+T'), self)
        new_tab_shortcut.activated.connect(self.add_new_tab)
        close_tab_shortcut = QShortcut(QKeySequence('Ctrl+W'), self)
        close_tab_shortcut.activated.connect(self.close_current_tab)
        # Add "+" button to tab bar
        self.add_tab_button = QToolButton(self)
        self.add_tab_button.setText('+')
        self.add_tab_button.setAutoRaise(True)
        self.add_tab_button.clicked.connect(self.add_new_tab)
        self.tab_widget.setCornerWidget(self.add_tab_button)
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)
        self.active_browser().urlChanged.connect(self.update_url)
        self.showMaximized()
    def add_tab(self, url):
        new_tab = BrowserTab(url)
        index = self.tab_widget.addTab(new_tab, "New Tab")
        self.tab_widget.setCurrentIndex(index)
    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)
    def active_browser(self):
        return self.tab_widget.currentWidget()
    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith('http'):
            url = 'http://' + url
        self.active_browser().load(QUrl(url))
    def navigate_home(self):
        self.active_browser().load(QUrl("https://www.duckduckgo.com"))
    def update_url(self, q):
        self.url_bar.setText(q.toString())
    def zoom_in(self):
        self.active_browser().setZoomFactor(
            self.active_browser().zoomFactor() + 0.1)
    def zoom_out(self):
        self.active_browser().setZoomFactor(
            self.active_browser().zoomFactor() - 0.1)
    def add_new_tab(self):
        # Add a new tab with a default URL
        self.add_tab('https://www.duckduckgo.com')
    def close_current_tab(self):
        # Close the current tab
        current_index = self.tab_widget.currentIndex()
        self.tab_widget.removeTab(current_index)
    def add_new_tab(self):
        # Add a new tab with a default URL
        self.add_tab('https://www.duckduckgo.com')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
