import sys
import pyqtgraph as pg
import FinanceDataReader as fdr
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt


class Triggers:
    rec_trig = 0  # 0 for not selected, 1 for select
    rec_mode = 0  # 0 for normal, 1 for ultra

    led_mode = 0  # 0 for on, 1 for off

    measurement_trig = 0  # 0 for not selected, 1 for select

    db_scaling_trig = 0  # 0 for not selected, 1 for select
    db_scaling_mode = 0  # 0 for auto, 1 for smart, -1 for off

    sound_trig = 0  # 주파수 0 for not selected, 1 for select


class MeasurementWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.led_flag = 0
        self.sound_flag = 0

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.rec_btn = QPushButton('', self)
        self.rec_btn.setMinimumHeight(65)
        self.rec_btn.setMaximumWidth(85)
        self.rec_btn.setIcon(QIcon('./icons/rec.png'))
        self.rec_btn.setIconSize(QSize(60, 60))
        self.rec_btn.setStyleSheet("background-color: #55B0BC;")
        self.rec_btn.clicked.connect(self.rec_start_event)

        self.capture_btn = QPushButton('', self)
        self.capture_btn.setMinimumHeight(65)
        self.capture_btn.setMaximumWidth(85)
        self.capture_btn.setIcon(QIcon('./icons/capture.png'))
        self.capture_btn.setIconSize(QSize(60, 60))
        self.capture_btn.setStyleSheet("background-color: #55B0BC;")

        self.time_marker_btn = QPushButton('', self)
        self.time_marker_btn.setMinimumHeight(65)
        self.time_marker_btn.setMaximumWidth(85)
        self.time_marker_btn.setIcon(QIcon('./icons/time-marker.png'))
        self.time_marker_btn.setIconSize(QSize(60, 60))
        self.time_marker_btn.setStyleSheet("background-color: #55B0BC;")

        self.file_open_btn = QPushButton('', self)
        self.file_open_btn.setMinimumHeight(65)
        self.file_open_btn.setMaximumWidth(85)
        self.file_open_btn.setIcon(QIcon('./icons/file-open.png'))
        self.file_open_btn.setIconSize(QSize(60, 60))
        self.file_open_btn.setStyleSheet("background-color: #55B0BC;")

        self.file_save_btn = QPushButton('', self)
        self.file_save_btn.setMinimumHeight(65)
        self.file_save_btn.setMaximumWidth(85)
        self.file_save_btn.setIcon(QIcon('./icons/file-save.png'))
        self.file_save_btn.setIconSize(QSize(60, 60))
        self.file_save_btn.setStyleSheet("background-color: #55B0BC;")

        self.led_btn = QPushButton('', self)
        self.led_btn.setMinimumHeight(65)
        self.led_btn.setMaximumWidth(85)
        self.led_btn.setIcon(QIcon('./icons/led.png'))
        self.led_btn.setIconSize(QSize(60, 60))
        self.led_btn.setStyleSheet("background-color: #55B0BC;")
        self.led_btn.clicked.connect(self.led_control)

        self.play_btn = QPushButton('', self)
        self.play_btn.setMinimumHeight(65)
        self.play_btn.setMaximumWidth(85)
        self.play_btn.setIcon(QIcon('./icons/play.png'))
        self.play_btn.setIconSize(QSize(60, 60))
        self.play_btn.setStyleSheet("background-color: #55B0BC;")

        self.exit_btn = QPushButton('', self)
        self.exit_btn.setMinimumHeight(65)
        self.exit_btn.setMaximumWidth(85)
        self.exit_btn.setIcon(QIcon('./icons/exit.png'))
        self.exit_btn.setIconSize(QSize(60, 60))
        self.exit_btn.setStyleSheet("background-color: #55B0BC;")

        self.video_btn = QPushButton('', self)
        self.video_btn.setMinimumHeight(65)
        self.video_btn.setMaximumWidth(85)
        self.video_btn.setIcon(QIcon('./icons/video.png'))
        self.video_btn.setIconSize(QSize(60, 60))
        self.video_btn.setStyleSheet("background-color: #55B0BC;")

        self.db_scaling_btn = QPushButton('', self)
        self.db_scaling_btn.setMinimumHeight(65)
        self.db_scaling_btn.setMaximumWidth(85)
        self.db_scaling_btn.setIcon(QIcon('./icons/db-scaling.png'))
        self.db_scaling_btn.setIconSize(QSize(60, 60))
        self.db_scaling_btn.setStyleSheet("background-color: #55B0BC;")
        self.db_scaling_btn.clicked.connect(self.db_scaling_event)

        self.time_marker_move_btn = QPushButton('', self)
        self.time_marker_move_btn.setMinimumHeight(65)
        self.time_marker_move_btn.setMaximumWidth(85)
        self.time_marker_move_btn.setIcon(QIcon('./icons/time-marker.png'))
        self.time_marker_move_btn.setIconSize(QSize(60, 60))
        self.time_marker_move_btn.setStyleSheet("background-color: #55B0BC;")

        self.sound_btn = QPushButton('', self)
        self.sound_btn.setMinimumHeight(65)
        self.sound_btn.setMaximumWidth(85)
        self.sound_btn.setIcon(QIcon('./icons/sound.png'))
        self.sound_btn.setIconSize(QSize(60, 60))
        self.sound_btn.setStyleSheet("background-color: #55B0BC;")
        self.sound_btn.clicked.connect(self.sound_control)

        self.time_setting_btn = QPushButton('', self)
        self.time_setting_btn.setMinimumHeight(65)
        self.time_setting_btn.setMaximumWidth(85)
        self.time_setting_btn.setIcon(QIcon('./icons/time-setting.png'))
        self.time_setting_btn.setIconSize(QSize(60, 60))
        self.time_setting_btn.setStyleSheet("background-color: #55B0BC;")

        self.time_navigation_btn = QPushButton('', self)
        self.time_navigation_btn.setMinimumHeight(65)
        self.time_navigation_btn.setMaximumWidth(85)
        self.time_navigation_btn.setIcon(QIcon('./icons/time-navigator.png'))
        self.time_navigation_btn.setIconSize(QSize(60, 60))
        self.time_navigation_btn.setStyleSheet("background-color: #55B0BC;")

        lbl_video = QLabel('Video')
        lbl_video.setMaximumWidth(1000)

        # lbl_graph1 = QLabel('Graph1')
        lbl_graph1 = pg.PlotWidget(axisItems={'bottom': pg.DateAxisItem()})
        df = fdr.DataReader("005930")
        unix_ts = [x.timestamp() for x in df.index]
        lbl_graph1.plot(x=unix_ts, y=df['Close'])
        lbl_graph1.setMaximumWidth(1000)

        # lbl_graph2 = QLabel('Graph2')
        lbl_graph2 = pg.PlotWidget(title="line chart")
        x = [1, 2, 3]
        y = [4, 5, 6]
        lbl_graph2.plot(x, y)
        lbl_graph2.setMaximumWidth(250)

        lbl_bar1 = QLabel('Bar1')
        lbl_bar1.setMaximumWidth(50)

        lbl_bar2 = QLabel('Bar2')
        lbl_bar2.setMaximumWidth(50)

        lbl_setting = QLabel('')
        lbl_setting.setMaximumWidth(100)

        lbl_video.setStyleSheet("border-style: solid;"
                                "border-width: 1px;")
        lbl_graph1.setStyleSheet("border-style: solid;"
                                 "border-width: 1px;")
        lbl_graph2.setStyleSheet("border-style: solid;"
                                 "border-width: 1px;")
        lbl_bar1.setStyleSheet("border-style: solid;"
                               "border-width: 1px;")
        lbl_bar2.setStyleSheet("border-style: solid;"
                               "border-width: 1px;")
        lbl_setting.setStyleSheet("border-style: solid;"
                                  "border-width: 1px;")

        self.grid.addWidget(self.rec_btn, 0, 0)
        self.grid.addWidget(self.capture_btn, 1, 0)
        self.grid.addWidget(self.time_marker_btn, 2, 0)
        self.grid.addWidget(self.file_open_btn, 3, 0)
        self.grid.addWidget(self.file_save_btn, 4, 0)
        self.grid.addWidget(self.led_btn, 5, 0)
        self.grid.addWidget(self.play_btn, 6, 0)

        self.grid.addWidget(lbl_video, 0, 1, 4, 5)
        self.grid.addWidget(lbl_graph1, 4, 1, 2, 5)

        self.grid.addWidget(lbl_bar1, 0, 6, 4, 1)
        self.grid.addWidget(lbl_bar2, 4, 6, 2, 1)

        self.grid.addWidget(lbl_graph2, 4, 7, 2, 1)

        self.grid.addWidget(lbl_setting, 0, 8, 7, 1)

        self.grid.addWidget(self.exit_btn, 0, 9)
        self.grid.addWidget(self.video_btn, 1, 9)
        self.grid.addWidget(self.db_scaling_btn, 2, 9)
        self.grid.addWidget(self.time_marker_move_btn, 3, 9)
        self.grid.addWidget(self.sound_btn, 4, 9)
        self.grid.addWidget(self.time_setting_btn, 5, 9)
        self.grid.addWidget(self.time_navigation_btn, 6, 9)

    def rec_start_event(self):
        if Triggers.rec_trig == 0:  # 대기상태라면 위젯 추가
            Triggers.rec_trig += 1
            self.rec_ultra = QPushButton('', self)
            self.rec_ultra.setMinimumHeight(65)
            self.rec_ultra.setMaximumWidth(85)
            self.rec_ultra.setIcon(QIcon('./icons/rec.png'))
            self.rec_ultra.setIconSize(QSize(60, 60))
            self.rec_ultra.setStyleSheet("background-color: #55B0BC;")
            self.rec_ultra.clicked.connect(self.rec_ultra_event)

            self.video_btn.deleteLater()

            self.measurement_distance = QPushButton('', self)
            self.measurement_distance.setMinimumHeight(65)
            self.measurement_distance.setMaximumWidth(85)
            self.measurement_distance.setIcon(QIcon('./icons/measure-distance.png'))
            self.measurement_distance.setIconSize(QSize(60, 60))
            self.measurement_distance.setStyleSheet("background-color: #55B0BC;")
            self.measurement_distance.clicked.connect(self.measurement_event)

            self.grid.addWidget(self.rec_ultra, 0, 1)
            self.grid.addWidget(self.measurement_distance, 1, 9)



        elif Triggers.rec_trig > 0:  # 모드 선택 상태라면
            self.grid.removeWidget(self.rec_ultra)
            self.grid.removeWidget(self.rec_btn)
            self.rec_ultra.deleteLater()
            self.rec_btn.deleteLater()
            self.rec_ultra = None

            self.stop_btn = QPushButton('', self)
            self.stop_btn.setMinimumHeight(65)
            self.stop_btn.setMaximumWidth(85)
            self.stop_btn.setIcon(QIcon('./icons/stop.png'))
            self.stop_btn.setIconSize(QSize(60, 60))
            self.stop_btn.setStyleSheet("background-color: #55B0BC;")
            self.grid.addWidget(self.stop_btn, 0, 0)

            Triggers.rec_trig = 0
            Triggers.rec_num = 0

            # print(Triggers.rec_num, "normal mode")

    def rec_ultra_event(self):
        if Triggers.rec_trig > 0:
            self.grid.removeWidget(self.rec_ultra)
            self.rec_ultra.deleteLater()
            self.rec_ultra = None
            Triggers.rec_trig = 0
            Triggers.rec_num = 1

            # print(Triggers.rec_num, "ultra mode")

    def led_control(self):
        if self.led_flag == 0:
            Triggers.led_flag = 1
            self.led_btn.setIcon(QIcon('icons/led.png'))
        else:
            Triggers.led_flag = 0
            self.led_btn.setIcon(QIcon('icons/led-off.png'))

    def measurement_event(self):
        # cur_measure_value = 0
        if Triggers.measurement_trig == 0:  # 슬라이더 열기
            Triggers.measurement_trig += 1
            self.measure_lbl = QLabel('측정거리', self)
            self.grid.addWidget(self.measure_lbl, 0, 8)

            self.measure_slider = QSlider(Qt.Vertical, self)
            self.measure_slider.setRange(0, 50)
            self.measure_slider.setSingleStep(2)
            self.grid.addWidget(self.measure_slider, 2, 8, 5, 1)
            # self.measure_slider.setValue(cur_measure_value)
            # self.measure_slider.valueChanged[int].connect(self.valuechange)
            # print(cur_measure_value)

        elif Triggers.measurement_trig > 0:  # 슬라이더 닫기
            Triggers.measurement_trig = 0
            self.grid.removeWidget(self.measure_lbl)
            self.measure_lbl.deleteLater()
            self.measure_lbl = None

            self.grid.removeWidget(self.measure_slider)
            self.measure_slider.deleteLater()
            self.measure_slider = None

    def valuechange(self, value):
        self.__init__(value)

    def db_scaling_event(self):
        if Triggers.db_scaling_trig == 0: # 슬라이더 열기
            Triggers.db_scaling_trig += 1
            self.mode_lbl = QLabel('Auto', self)
            self.db_mode = QComboBox(self)
            self.db_mode.addItem('Auto')
            self.db_mode.addItem('Smart')
            self.db_mode.addItem('Off')
            self.db_mode.activated[str].connect(self.db_mode_change_event)
            self.grid.addWidget(self.db_mode, 0, 8)

            self.dynamic_lbl = QLabel('Dynamic', self)
            self.grid.addWidget(self.dynamic_lbl, 1, 8)

            self.slider = QSlider(Qt.Vertical, self)
            self.slider.setRange(0.5, 50)
            self.slider.setSingleStep(2)
            self.grid.addWidget(self.slider, 3, 8, 4, 1)

        elif Triggers.db_scaling_trig > 0: # 슬라이더 닫기
            Triggers.db_scaling_trig = 0
            self.grid.removeWidget(self.db_mode)
            self.db_mode.deleteLater()
            self.db_mode = None

            self.grid.removeWidget(self.dynamic_lbl)
            self.dynamic_lbl.deleteLater()
            self.dynamic_lbl = None

            self.grid.removeWidget(self.slider)
            self.slider.deleteLater()
            self.slider = None


    def db_mode_change_event(self, text):
        if Triggers.db_scaling_mode < 0:
            self.grid.removeWidget(self.db_mode)
            self.db_mode.deleteLater()
            self.db_mode = None
            self.grid.addWidget(self.db_mode, 0, 8)

        self.mode_lbl.setText(text)
        self.mode_lbl.adjustSize()

        if text == 'Smart':
            Triggers.db_scaling_mode = 1
            self.crest_lbl = QLabel('Crest', self)
            self.grid.addWidget(self.crest_lbl, 2, 8)

        elif text == 'Off':
            Triggers.db_scaling_mode = 2
            self.crest_lbl = QLabel('최고 dB', self)
            self.grid.addWidget(self.crest_lbl, 2, 8)
        else:
            Triggers.db_scaling_mode = 0
            pass

    def sound_control(self):
        if self.sound_flag == 0: # init or sound off -> sound on
            self.sound_flag = 1 # on
            self.sound_btn.setIcon(QIcon('icons/sound.png'))

            self.no_signal_btn = QPushButton('', self)
            self.no_signal_btn.setMinimumHeight(65)
            self.no_signal_btn.setMaximumWidth(85)
            self.no_signal_btn.setIcon(QIcon('./icons/no-signal.png'))
            self.no_signal_btn.setIconSize(QSize(60, 60))
            self.no_signal_btn.setStyleSheet("background-color: #55B0BC;")
            self.grid.addWidget(self.no_signal_btn, 0, 8)
            self.no_signal_btn.clicked.connect(self.sound_event)

            self.slider = QSlider(Qt.Vertical, self)
            self.slider.setRange(0, 50)
            self.slider.setSingleStep(2)
            self.grid.addWidget(self.slider, 1, 8, 6, 1)

        else: # sound on -> sound off
            self.sound_flag = 0 # off
            self.sound_btn.setIcon(QIcon('icons/sound-off.png'))
            self.grid.removeWidget(self.no_signal_btn)
            self.no_signal_btn.deleteLater()
            self.no_signal_btn = None

            self.grid.removeWidget(self.slider)
            self.slider.deleteLater()
            self.slider = None

    def sound_event(self):
        if Triggers.sound_trig == 0:  # 전영역 주파수
            Triggers.sound_trig += 1
            self.no_signal_btn.setIcon(QIcon('icons/no-signal.png'))

        elif Triggers.sound_trig > 0:  # 선택 영역 주파수
            Triggers.sound_trig = 0
            self.no_signal_btn.setIcon(QIcon('icons/signal.png'))



        # if pre_mode == 'None':
        #     pass
        #
        # elif pre_mode == 'Smart':
        #     self.grid.removeWidget(self.crest_lbl)
        #     self.crest_lbl.deleteLater()
        #     self.crest_lbl = None
        #
        # elif pre_mode == 'Off':
        #     self.grid.removeWidget(self.high_db_lbl)
        #     self.high_db_lbl.deleteLater()
        #     self.high_db_lbl = None



class MeasurementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')  # 단축키
        exitAction.setStatusTip('Exit application')  # 상태팁
        exitAction.triggered.connect(qApp.quit)  # 어플리케이션 종료

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)

        filemenu = menubar.addMenu('&Edit')
        filemenu.addAction(exitAction)

        wg = MeasurementWidget()
        self.setCentralWidget(wg)

        self.setWindowTitle('Sound Cam')
        self.resize(720, 480)
        self.show()


# if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    ex = MeasurementWidget()
#    ex2 = MyMainWindow()
#    sys.exit(app.exec_())
