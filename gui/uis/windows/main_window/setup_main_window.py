

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import threading

from database.personDaoImpl import PersonDaoImpl
from database.Person import Person
from . functions_main_window import *
# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *
# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings
# IMPORT THEME COLORS
# ///////////////////////////////////////////////////////////////
from gui.core.json_themes import Themes
# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *
# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from . ui_main import *
# MAIN FUNCTIONS
# ///////////////////////////////////////////////////////////////
from . functions_main_window import *
from concurrent.futures import ThreadPoolExecutor
# PY WINDOW
# ///////////////////////////////////////////////////////////////
pool = ThreadPoolExecutor(max_workers=1)
class SetupMainWindow:
    def __init__(self):
        super().__init__()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)
        self.files = [str]

    # ADD LEFT MENUS
    # ///////////////////////////////////////////////////////////////
    add_left_menus = [
        {
            "btn_icon" : "icon_home.svg",
            "btn_id" : "btn_home",
            "btn_text" : "Home",
            "btn_tooltip" : "Home page",
            "show_top" : True,
            "is_active" : True
        },

        {
            "btn_icon" : "no_icon.svg",
            "btn_id" : "btn_pictures",
            "btn_text" : "show pictures",
            "btn_tooltip" : "show pictures",
            "show_top" : True,
            "is_active" : False
        },
        {
            "btn_icon": "icon_add_user.svg",
            "btn_id": "btn_add_person",
            "btn_text": "Add Person",
            "btn_tooltip": "Add person",
            "show_top": True,
            "is_active": False
        },
    ]

    # SETUP CUSTOM BTNs OF CUSTOM WIDGETS
    # Get sender() function when btn is clicked
    # ///////////////////////////////////////////////////////////////
    def setup_btns(self):
        if self.ui.title_bar.sender() != None:
            return self.ui.title_bar.sender()
        elif self.ui.left_menu.sender() != None:
            return self.ui.left_menu.sender()
        elif self.ui.load_pages.row_3_layout.sender() != None:
            return self.ui.load_pages.row_3_layout.sender()

    # SETUP MAIN WINDOW WITH CUSTOM PARAMETERS
    # ///////////////////////////////////////////////////////////////
    def setup_gui(self,sfr):
        # APP TITLE
        # ///////////////////////////////////////////////////////////////
        self.setWindowTitle(self.settings["app_name"])
        
        # REMOVE TITLE BAR
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

        # ADD GRIPS
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)

        # LEFT MENUS / GET SIGNALS WHEN LEFT MENU BTN IS CLICKED / RELEASED
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.left_menu.add_menus(SetupMainWindow.add_left_menus)

        # SET SIGNALS
        self.ui.left_menu.clicked.connect(self.btn_clicked)
        self.ui.left_menu.released.connect(self.btn_released)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items

        # page 3 - database
        # ///////////////////////////////////////////////////////////////
        # PY LINE EDIT
        self.line_fisrt_name = PyLineEdit (
            text="",
            place_holder_text="First name",
            radius=8,
            border_size=3,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.line_fisrt_name.setMinimumHeight (40)

        self.line_last_name = PyLineEdit (
            text="",
            place_holder_text="Last name",
            radius=8,
            border_size=3,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.line_last_name.setMinimumHeight (40)

        self.line_id = PyLineEdit (
            text="",
            place_holder_text="id",
            radius=8,
            border_size=3,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.line_id.setMinimumHeight (40)

        self.line_email = PyLineEdit (
            text="",
            place_holder_text="Email",
            radius=8,
            border_size=3,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.line_email.setMinimumHeight (40)

        self.line_phone_number = PyLineEdit (
            text="",
            place_holder_text="Phone number",
            radius=8,
            border_size=3,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.line_phone_number.setMinimumHeight (40)
        self.line_phone_number.setMaximumWidth (637)

        def dialog():
            self.files, check = QFileDialog.getOpenFileNames(None, "Open files",
                                                       "images", "Image files (*.jpg *.jpeg, *png)")

        # PUSH BUTTON 1
        self.button_choose_images = PyPushButton (
            text="Choose images",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.button_choose_images.setMinimumHeight (40)
        self.button_choose_images.clicked.connect(dialog)

        # Add Person BUTTON
        self.button_add_person = PyIconButton (
            icon_path=Functions.set_svg_icon ("icon_add_user.svg"),
            parent=self,
            app_parent=self.ui.central_widget,
            tooltip_text="add person",
            width=40,
            height=40,
            radius=8,
            dark_one=self.themes["app_color"]["dark_one"],
            icon_color=self.themes["app_color"]["icon_color"],
            icon_color_hover=self.themes["app_color"]["icon_hover"],
            icon_color_pressed=self.themes["app_color"]["white"],
            icon_color_active=self.themes["app_color"]["icon_active"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["context_color"],
        )

        # TODO: must validate inputs
        def add_to_db():
            dao = PersonDaoImpl(sfr)
            dao.add_person(Person([self.line_id.text(),self.line_fisrt_name.text(),
                                  self.line_last_name.text(), self.line_email.text(),self.line_phone_number.text()]),
                                  self.files)

        self.button_add_person.clicked.connect(add_to_db)
        # ADD WIDGETS
        self.ui.load_pages.row_1_layout.addWidget(self.line_fisrt_name)
        self.ui.load_pages.row_1_layout.addWidget(self.line_last_name)
        self.ui.load_pages.row_2_layout.addWidget(self.line_id)
        self.ui.load_pages.row_2_layout.addWidget(self.line_email)
        self.ui.load_pages.row_3_layout.addWidget(self.line_phone_number)
        self.ui.load_pages.row_3_layout.addWidget(self.button_choose_images)
        self.ui.load_pages.row_3_layout.addWidget(self.button_add_person)

    # RESIZE GRIPS AND CHANGE POSITION
    # Resize or change position when window is resized
    # ///////////////////////////////////////////////////////////////
    def resize_grips(self):
        if self.settings["custom_title_bar"]:
            self.left_grip.setGeometry(5, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
            self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
            self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
            self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)