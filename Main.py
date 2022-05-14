# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from gui.uis.windows.main_window.functions_main_window import *
import os
import sys
import cv2
import numpy as np
from threads.VideoThread import VideoThread
from threads.PicturesThread import PicturesThread
from picBox import *
from queue import Queue
import threading
from datetime import datetime

persons_dict = {}

threadLock = threading.Lock()

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# ///////////////////////////////////////////////////////////////
# MAIN WINDOW
from gui.uis.windows.main_window import *

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "96"


# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
def check_data(name):
    if name == "Unknown":
        return 1
    now = datetime.now()
    if name not in persons_dict:
        persons_dict[name] = now.strftime("%Y%m%d%H%M%S")
        return 2
    if name in persons_dict:
        print((datetime.strptime(persons_dict[name], "%Y%m%d%H%M%S") - now).total_seconds())
        if (now - datetime.strptime(persons_dict[name], "%Y%m%d%H%M%S")).total_seconds() > 60:
            persons_dict[name] = now.strftime("%Y%m%d%H%M%S")
            return 3
    return 4


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True  # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)

        ###########################################################
        q = Queue()
        # create the video capture thread
        self.thread = VideoThread(q, threadLock)
        self.thread1 = PicturesThread(q, threadLock)

        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread1.page_pixmap_signal.connect(self.add_image_to_page)
        ###########################################################
        self.dao = PersonDaoImpl()
        # ///////////////////////////////////////////////////////////////
        self.i = 0
        self.j = -1

        # ///////////////////////////////////////////////////////////////

        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()
        self.start()

    # VIDEO THREAD HANDLING
    # ///////////////////////////////////////////////////////////////
    def start(self):
        self.thread.start()
        self.thread1.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @Slot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.load_pages.stream.setPixmap(qt_img)

    @Slot(np.ndarray, str)
    def add_image_to_page(self, cv_img, name):
        """Updates the image_label with a new opencv image"""
        check = check_data(name)
        if check == 2 or check == 3:
            qt_img = self.convert_cv_qt(cv_img)
            object = QLabel()
            box = picBox()
            # scaling the image
            qt_img = qt_img.scaled(300, 300, Qt.KeepAspectRatio)
            box.setImage(qt_img)
            box.set_data(name, self.dao)
            object.setPixmap(qt_img)
            self.ui.load_pages.gridLayout_2.addWidget(box, *self.getPos())
            self.ui.load_pages.right_pic_layout.addWidget(object)

    def getPos(self):
        self.j += 1
        if self.j % 3 == 0:
            self.i += 1

        return (self.i, self.j % 3)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(self.ui.load_pages.stream.width(), self.ui.load_pages.stream.height(),
                                        Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    # END OF THE VIDEO THREAD SECTION
    # ///////////////////////////////////////////////////////////////

    # LEFT MENU BTN IS CLICKED
    # Run function when btn is clicked
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_clicked(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # Remove Selection If Clicked By "btn_close_left_column"
        if btn.objectName() != "btn_settings":
            self.ui.left_menu.deselect_all_tab()

        # Get Title Bar Btn And Reset Active
        top_settings = MainFunctions.get_title_bar_btn(self, "btn_top_settings")
        top_settings.set_active(False)

        # LEFT MENU
        # ///////////////////////////////////////////////////////////////

        # HOME BTN
        if btn.objectName() == "btn_home":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 1
            MainFunctions.set_page(self, self.ui.load_pages.page_1)


        if btn.objectName () == "btn_pictures":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 3
            MainFunctions.set_page(self, self.ui.load_pages.page_2)

        # SETTINGS LEFT
        if btn.objectName () == "btn_settings" or btn.objectName () == "btn_close_left_column":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible (self):
                # Show / Hide
                MainFunctions.toggle_left_column (self)
                self.ui.left_menu.select_only_one_tab (btn.objectName ())
            else:
                if btn.objectName () == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab ()
                    # Show / Hide
                    MainFunctions.toggle_left_column (self)
                self.ui.left_menu.select_only_one_tab (btn.objectName ())

            # Change Left Column Menu
            if btn.objectName () != "btn_close_left_column":
                MainFunctions.set_left_column_menu (
                    self,
                    menu=self.ui.left_column.menus.menu_1,
                    title="Settings Left Column",
                    icon_path=Functions.set_svg_icon ("icon_settings.svg")
                )

        # TITLE BAR MENU
        # ///////////////////////////////////////////////////////////////

        # SETTINGS TITLE BAR
        if btn.objectName() == "btn_top_settings":
            # Toogle Active
            if not MainFunctions.right_column_is_visible(self):
                btn.set_active(True)

                # Show / Hide
                MainFunctions.toggle_right_column(self)
            else:
                btn.set_active(False)

                # Show / Hide
                MainFunctions.toggle_right_column(self)

            # Get Left Menu Btn
            top_settings = MainFunctions.get_left_menu_btn(self, "btn_settings")
            top_settings.set_active_tab(False)

            # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        print(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()


# SETTINGS WHEN TO START
# Set the initial class and also additional parameters of the "QApplication" class
# ///////////////////////////////////////////////////////////////
if __name__ == "__main__":
    # APPLICATION
    # ///////////////////////////////////////////////////////////////
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()

    # EXEC APP
    # ///////////////////////////////////////////////////////////////
    sys.exit(app.exec())