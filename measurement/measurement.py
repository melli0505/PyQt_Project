import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from qtrangeslider import QRangeSlider
import measurement.screenshotclass as ssc
import measurement.worker as wk
from socket import *
import numpy as np

sig = []
time = []

class Triggers:
    rec_trig = 0  # 0 for not selected, 1 for select
    rec_mode = 0  # 0 for normal, 1 for ultra

    led_mode = 0  # 0 for on, 1 for off

    measurement_trig = 0  # 0 for not selected,1 for select

    db_scaling_trig = 0  # 0 for not selected, 1 for select
    db_scaling_mode = 0  # 0 for auto, 1 for smart, -1 for off

    sound_trig = 0  # 주파수 0 for not selected, 1 for select

    play_trig = 0  # -1 for not working, 0 for not selected, 1 for select
    play_mode = 0  # 0 for normal, 1 for 0.5, 2 for 0.25

    time_nv_trig = 0  # 0 for on, 1 for off, -1 for disabled


class MeasurementWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.measure_set = 0  # 측정 거리 설정 슬라이더 값
        self.db_set = 0  # dB 슬라이더 값
        self.sound_flag = 0  # 0 for sound btn off, 1 for on
        self.time_val = 0  # time_navigation slider 값
        self.time_st_flag = 0  # 0 for time_setting btn off, 1 for on
        self.video_flag = 0  # 0 for video_btn off, 1 for on
        self.frequency_flag = 0  # 0 for frequency_btn off, 1 for on
        self.recur_flag = 0  # frequency 버튼 순환 확인 flag
        self.max_freq_set = 30  # frequency slider max 설정 값
        self.min_freq_set = 0  # frequency slider min 설정 값

        self.i = 0  # socket recv 값 갱신 주기 조절용 변수

        # 그리드 레이아웃 생성
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        # 측정 시작 버튼
        self.rec_btn = QPushButton('', self)
        self.rec_btn.setMinimumHeight(65)
        self.rec_btn.setMaximumWidth(85)
        self.rec_btn.setIcon(QIcon('./icons/rec.png'))
        self.rec_btn.setIconSize(QSize(60, 60))
        self.rec_btn.setStyleSheet("background-color: #55B0BC;")
        self.rec_btn.clicked.connect(self.rec_start_event)

        # 화면 캡쳐 버튼
        self.capture_btn = QPushButton('', self)
        self.capture_btn.setMinimumHeight(65)
        self.capture_btn.setMaximumWidth(85)
        self.capture_btn.setIcon(QIcon('./icons/capture.png'))
        self.capture_btn.setIconSize(QSize(60, 60))
        self.capture_btn.setStyleSheet("background-color: #55B0BC;")
        self.capture_btn.clicked.connect(self.capture_event)

        # 타임 마커 표시 버튼
        self.time_marker_btn = QPushButton('', self)
        self.time_marker_btn.setMinimumHeight(65)
        self.time_marker_btn.setMaximumWidth(85)
        self.time_marker_btn.setIcon(QIcon('./icons/time-marker.png'))
        self.time_marker_btn.setIconSize(QSize(60, 60))
        self.time_marker_btn.setStyleSheet("background-color: #55B0BC;")

        # 파일 불러오기 버튼
        self.file_open_btn = QPushButton('', self)
        self.file_open_btn.setMinimumHeight(65)
        self.file_open_btn.setMaximumWidth(85)
        self.file_open_btn.setIcon(QIcon('./icons/file-open.png'))
        self.file_open_btn.setIconSize(QSize(60, 60))
        self.file_open_btn.setStyleSheet("background-color: #55B0BC;")
        self.file_open_btn.clicked.connect(self.fileOpen)

        # 파일 저장 버튼
        self.file_save_btn = QPushButton('', self)
        self.file_save_btn.setMinimumHeight(65)
        self.file_save_btn.setMaximumWidth(85)
        self.file_save_btn.setIcon(QIcon('./icons/file-save.png'))
        self.file_save_btn.setIconSize(QSize(60, 60))
        self.file_save_btn.setStyleSheet("background-color: #55B0BC;")

        # LED 조명 켜기/끄기 버튼
        self.led_btn = QPushButton('', self)
        self.led_btn.setMinimumHeight(65)
        self.led_btn.setMaximumWidth(85)
        self.led_btn.setIcon(QIcon('./icons/led.png'))
        self.led_btn.setIconSize(QSize(60, 60))
        self.led_btn.setStyleSheet("background-color: #55B0BC;")
        self.led_btn.clicked.connect(self.led_control)

        # 파일 재생 버튼
        self.play_btn = QPushButton('', self)
        self.play_btn.setMinimumHeight(65)
        self.play_btn.setMaximumWidth(85)
        self.play_btn.setIcon(QIcon('./icons/play.png'))
        self.play_btn.setIconSize(QSize(60, 60))
        self.play_btn.setStyleSheet("background-color: #55B0BC;")
        self.play_btn.clicked.connect(self.play_setting_event)

        # 측정창 나가기 버튼
        self.exit_btn = QPushButton('', self)
        self.exit_btn.setMinimumHeight(65)
        self.exit_btn.setMaximumWidth(85)
        self.exit_btn.setIcon(QIcon('./icons/exit.png'))
        self.exit_btn.setIconSize(QSize(60, 60))
        self.exit_btn.setStyleSheet("background-color: #55B0BC;")

        # 영상 변환 버튼
        self.video_btn = QPushButton('', self)
        self.video_btn.setMinimumHeight(65)
        self.video_btn.setMaximumWidth(85)
        self.video_btn.setIcon(QIcon('./icons/video.png'))
        self.video_btn.setIconSize(QSize(60, 60))
        self.video_btn.setStyleSheet("background-color: #55B0BC;")
        self.video_btn.clicked.connect(self.video_event)

        # dB 스케일링 버튼
        self.db_scaling_btn = QPushButton('', self)
        self.db_scaling_btn.setMinimumHeight(65)
        self.db_scaling_btn.setMaximumWidth(85)
        self.db_scaling_btn.setIcon(QIcon('./icons/db-scaling.png'))
        self.db_scaling_btn.setIconSize(QSize(60, 60))
        self.db_scaling_btn.setStyleSheet("background-color: #55B0BC;")
        self.db_scaling_btn.clicked.connect(self.db_scaling_event)

        # 타임 마커 이동 버튼
        self.time_marker_move_btn = QPushButton('', self)
        self.time_marker_move_btn.setMinimumHeight(65)
        self.time_marker_move_btn.setMaximumWidth(85)
        self.time_marker_move_btn.setIcon(QIcon('./icons/time-marker.png'))
        self.time_marker_move_btn.setIconSize(QSize(60, 60))
        self.time_marker_move_btn.setStyleSheet("background-color: #55B0BC;")

        # 사운드 설정 버튼
        self.sound_btn = QPushButton('', self)
        self.sound_btn.setMinimumHeight(65)
        self.sound_btn.setMaximumWidth(85)
        self.sound_btn.setIcon(QIcon('./icons/sound.png'))
        self.sound_btn.setIconSize(QSize(60, 60))
        self.sound_btn.setStyleSheet("background-color: #55B0BC;")
        self.sound_btn.clicked.connect(self.sound_control)

        # 측정 영상 저장 시간 설정 버튼
        self.time_setting_btn = QPushButton('', self)
        self.time_setting_btn.setMinimumHeight(65)
        self.time_setting_btn.setMaximumWidth(85)
        self.time_setting_btn.setIcon(QIcon('./icons/time-setting.png'))
        self.time_setting_btn.setIconSize(QSize(60, 60))
        self.time_setting_btn.setStyleSheet("background-color: #55B0BC;")
        self.time_setting_btn.clicked.connect(self.time_setting_event)

        # 타임 네비게이션 버튼
        self.time_navigation_btn = QPushButton('', self)
        self.time_navigation_btn.setMinimumHeight(65)
        self.time_navigation_btn.setMaximumWidth(85)
        self.time_navigation_btn.setIcon(QIcon('./icons/time-navigator.png'))
        self.time_navigation_btn.setIconSize(QSize(60, 60))
        self.time_navigation_btn.setStyleSheet("background-color: #55B0BC;")
        self.time_navigation_btn.clicked.connect(self.time_navigation_event)


        # graph plotting
        self.origin_Graph = pg.PlotWidget(title="original chart")
        self.fft_Graph = pg.PlotWidget(title="fft chart")

        self.origin_Graph.enableAutoRange(axis='x')
        self.origin_Graph.enableAutoRange(axis='y')
        self.x = []
        self.y = []

        self.fft_Graph.enableAutoRange(axis='x')
        self.fft_Graph.enableAutoRange(axis='y')
        self.fft_val = []

        self.origin_line = self.origin_Graph.plot(self.x, self.y)
        self.fft_line = self.fft_Graph.plot(self.fft_val)

        self.clientSocket = socket(AF_INET, SOCK_STREAM)

        # 그리드 레이아웃에 위젯 추가
        self.grid.addWidget(self.rec_btn, 0, 0)
        self.grid.addWidget(self.capture_btn, 1, 0)
        self.grid.addWidget(self.time_marker_btn, 2, 0)
        self.grid.addWidget(self.file_open_btn, 3, 0)
        self.grid.addWidget(self.file_save_btn, 4, 0)
        self.grid.addWidget(self.led_btn, 5, 0)
        self.grid.addWidget(self.play_btn, 6, 0)

        self.grid.addWidget(self.origin_Graph, 0, 1, 4, 6)
        self.grid.addWidget(self.fft_Graph, 4, 1, 3, 6)

        self.grid.addWidget(self.exit_btn, 0, 9)
        self.grid.addWidget(self.video_btn, 1, 9)
        self.grid.addWidget(self.db_scaling_btn, 2, 9)
        self.grid.addWidget(self.time_marker_move_btn, 3, 9)
        self.grid.addWidget(self.sound_btn, 4, 9)
        self.grid.addWidget(self.time_setting_btn, 5, 9)
        self.grid.addWidget(self.time_navigation_btn, 6, 9)

    # screenshot event
    def capture_event(self):
        self.screenshot = ssc.Screenshot()
        self.screenshot.show()
        self.screenshot.close()

    # normal mode 측정 설정 및 측정 방식 선택
    def rec_start_event(self):
        if Triggers.rec_trig == 0:  # 측정대기상태라면 위젯 추가
            Triggers.rec_trig += 1
            # ultra mode btn
            self.rec_ultra = QPushButton('', self)
            self.rec_ultra.setMinimumHeight(65)
            self.rec_ultra.setMaximumWidth(85)
            self.rec_ultra.setIcon(QIcon('./icons/rec.png'))
            self.rec_ultra.setIconSize(QSize(60, 60))
            self.rec_ultra.setStyleSheet("background-color: #55B0BC;")
            self.rec_ultra.clicked.connect(self.rec_ultra_event)

            self.grid.addWidget(self.rec_ultra, 0, 1)

        elif Triggers.rec_trig > 0:  # 모드 선택 상태라면
            self.reformat_btns()
            Triggers.rec_trig = 0
            Triggers.rec_num = 0

    # ultra mode 선택
    def rec_ultra_event(self):
        if Triggers.rec_trig > 0:
            self.reformat_btns()
            Triggers.rec_trig = 0
            Triggers.rec_num = 1

    # 측정 시작 후 버튼 변경
    def reformat_btns(self):
        # socket 설정
        ip = "127.0.0.1"
        port = 12345
        self.clientSocket.connect((ip, port))

        # 멀티스레드 시작
        self.th = wk.Worker(val=0, parent=self, client=self.clientSocket)
        self.th.thread_signal.connect(self.show_result)
        self.th.start()

        # 그리드에서 변경 버튼 삭제
        self.grid.removeWidget(self.rec_ultra)
        self.grid.removeWidget(self.rec_btn)
        self.grid.removeWidget(self.time_marker_move_btn)
        self.rec_ultra.deleteLater()

        self.rec_btn.deleteLater()
        self.time_marker_move_btn.deleteLater()
        self.rec_ultra = None

        Triggers.play_trig = -1
        Triggers.time_nv_trig = -1

        # 측정 거리 버튼
        self.measurement_distance = QPushButton('', self)
        self.measurement_distance.setMinimumHeight(65)
        self.measurement_distance.setMaximumWidth(85)
        self.measurement_distance.setIcon(QIcon('./icons/measure-distance.png'))
        self.measurement_distance.setIconSize(QSize(60, 60))
        self.measurement_distance.setStyleSheet("background-color: #55B0BC;")
        self.grid.addWidget(self.measurement_distance, 1, 9)
        self.measurement_distance.clicked.connect(self.measurement_event)

        # 측정 중지 버튼
        self.stop_btn = QPushButton('', self)
        self.stop_btn.setMinimumHeight(65)
        self.stop_btn.setMaximumWidth(85)
        self.stop_btn.setIcon(QIcon('./icons/stop.png'))
        self.stop_btn.setIconSize(QSize(60, 60))
        self.stop_btn.setStyleSheet("background-color: #55B0BC;")
        self.grid.addWidget(self.stop_btn, 0, 0)
        self.stop_btn.clicked.connect(self.stop_measure)

        # 주파수 버튼
        self.frequency_btn = QPushButton('', self)
        self.frequency_btn.setMinimumHeight(65)
        self.frequency_btn.setMaximumWidth(85)
        self.frequency_btn.setIcon(QIcon('./icons/frequency.png'))
        self.frequency_btn.setIconSize(QSize(60, 60))
        self.frequency_btn.setStyleSheet("background-color: #55B0BC;")
        self.grid.addWidget(self.frequency_btn, 3, 9)
        self.frequency_btn.clicked.connect(self.frequency_event)

        self.file_save_btn.setStyleSheet("background-color: #5E777A")
        self.play_btn.setStyleSheet("background-color: #5E777A")
        self.time_navigation_btn.setStyleSheet("background-color: #5E777A")


    # 측정 종료 후 복귀
    def stop_measure(self):
        # socket thread 비활성화
        self.th.terminate()
        self.th.working = False

        self.clientSocket.close()
        self.clientSocket = socket(AF_INET, SOCK_STREAM)

        # 측정 종료 후 변경되는 버튼 삭제
        self.grid.removeWidget(self.stop_btn)
        self.grid.removeWidget(self.frequency_btn)
        self.grid.removeWidget(self.measurement_distance)
        self.stop_btn.deleteLater()
        self.frequency_btn.deleteLater()
        self.measurement_distance.deleteLater()

        # 측정 대기 중 사용되는 버튼 복귀
        self.rec_btn = QPushButton('', self)
        self.rec_btn.setMinimumHeight(65)
        self.rec_btn.setMaximumWidth(85)
        self.rec_btn.setIcon(QIcon('./icons/rec.png'))
        self.rec_btn.setIconSize(QSize(60, 60))
        self.rec_btn.setStyleSheet("background-color: #55B0BC;")
        self.rec_btn.clicked.connect(self.rec_start_event)

        self.time_marker_move_btn = QPushButton('', self)
        self.time_marker_move_btn.setMinimumHeight(65)
        self.time_marker_move_btn.setMaximumWidth(85)
        self.time_marker_move_btn.setIcon(QIcon('./icons/time-marker.png'))
        self.time_marker_move_btn.setIconSize(QSize(60, 60))
        self.time_marker_move_btn.setStyleSheet("background-color: #55B0BC;")

        self.grid.addWidget(self.rec_btn, 0, 0)
        self.grid.addWidget(self.time_marker_move_btn, 3, 9)
        self.grid.addWidget(self.video_btn, 1, 9)

        Triggers.rec_trig = 0
        Triggers.rec_mode = 0
        Triggers.play_trig = 0
        Triggers.time_nv_trig = 0

        self.file_save_btn.setStyleSheet("background-color: #55B0BC")
        self.play_btn.setStyleSheet("background-color: #55B0BC")
        self.time_navigation_btn.setStyleSheet("background-color: #55B0BC")

    # tcp 통신을 통한 데이터 갱신
    def show_result(self, val):
        global time, sig
        sig.append(val[1])
        if self.i == 9:
            self.fft_val = abs(np.fft.fft(sig) / len(sig))
            # self.fft_val.extend(fft)
            self.i = 0

        self.i += 1

        self.x.append(val[0])
        self.y.append(val[1])

        self.origin_line.setData(self.x, self.y)
        self.fft_line.setData(self.fft_val)

    # 파일 재생 속도 설정
    def play_setting_event(self):
        if Triggers.play_trig == -1:
            return
        elif Triggers.play_trig == 0:
            Triggers.play_trig += 1

            # 0.5배속 재생 버튼
            self.play_05 = QPushButton('', self)
            self.play_05.setMinimumHeight(65)
            self.play_05.setMaximumWidth(85)
            self.play_05.setIcon(QIcon('./icons/play.png'))
            self.play_05.setIconSize(QSize(60, 60))
            self.play_05.setStyleSheet("background-color: #55B0BC;")
            self.play_05.clicked.connect(self.play05_setting_event)

            # 0.25배속 재생 버튼
            self.play_025 = QPushButton('', self)
            self.play_025.setMinimumHeight(65)
            self.play_025.setMaximumWidth(85)
            self.play_025.setIcon(QIcon('./icons/play.png'))
            self.play_025.setIconSize(QSize(60, 60))
            self.play_025.setStyleSheet("background-color: #55B0BC;")
            self.play_025.clicked.connect(self.play025_setting_event)

            self.grid.addWidget(self.play_05, 6, 1)
            self.grid.addWidget(self.play_025, 6, 2)

        elif Triggers.play_trig > 0:
            self.grid.removeWidget(self.play_025)
            self.grid.removeWidget(self.play_05)
            self.play_025.deleteLater()
            self.play_05.deleteLater()

            Triggers.play_trig = 0
            Triggers.play_mode = 0

    # 0.5배속 선택
    def play05_setting_event(self):
        if Triggers.play_trig > 0:
            self.grid.removeWidget(self.play_025)
            self.grid.removeWidget(self.play_05)
            self.play_025.deleteLater()
            self.play_05.deleteLater()

            Triggers.play_trig = 0
            Triggers.play_mode = 1
            print(Triggers.play_mode, 'play 0.5')

    # 0.25배속 선택
    def play025_setting_event(self):
        if Triggers.play_trig > 0:
            self.grid.removeWidget(self.play_025)
            self.grid.removeWidget(self.play_05)
            self.play_025.deleteLater()
            self.play_05.deleteLater()

            Triggers.play_trig = 0
            Triggers.play_mode = 2
            print(Triggers.play_mode, 'play 0.25')

    # led on/off
    def led_control(self):
        if Triggers.led_mode == 0:
            Triggers.led_mode = 1
            self.led_btn.setIcon(QIcon('icons/led.png'))
        else:
            Triggers.led_mode = 0
            self.led_btn.setIcon(QIcon('icons/led-off.png'))

    #버튼 중복 활성화 제어 함수
    def change_btn(self, flag):
        if flag != 'video_flag' and self.video_flag == 1:
            self.video_event()
        elif flag != 'sound_flag' and self.sound_flag == 1:
            self.sound_control()
        elif flag != 'measurement_trig' and Triggers.measurement_trig > 0:
            self.measurement_event()
        elif flag != 'db_scaling_trig' and Triggers.db_scaling_trig > 0:
            self.db_scaling_event()
        elif flag != 'frequency_flag' and self.frequency_flag == 1:
            self.frequency_event()
        elif flag != 'time_st_flag' and self.time_st_flag == 1:
            self.time_setting_event()
        elif flag != 'time_nv_trig' and Triggers.time_nv_trig > 0:
            self.time_navigation_event()

    # 동영상 편집 이벤트
    def video_event(self):
        self.change_btn('video_flag')

        if self.video_flag == 0: # on
            self.video_flag = 1

            self.video_sp_btn = QPushButton('', self)  # video start point setting button
            self.video_sp_btn.setMinimumHeight(65)
            self.video_sp_btn.setMaximumWidth(85)
            self.video_sp_btn.setIcon(QIcon('./icons/video-editing.png'))
            self.video_sp_btn.setIconSize(QSize(60, 60))
            self.video_sp_btn.setStyleSheet("background-color: #55B0BC;")
            self.grid.addWidget(self.video_sp_btn, 1, 8)

            self.video_ep_btn = QPushButton('', self)  # video end point setting button
            self.video_ep_btn.setMinimumHeight(65)
            self.video_ep_btn.setMaximumWidth(85)
            self.video_ep_btn.setIcon(QIcon('./icons/video-editing.png'))
            self.video_ep_btn.setIconSize(QSize(60, 60))
            self.video_ep_btn.setStyleSheet("background-color: #55B0BC;")
            self.grid.addWidget(self.video_ep_btn, 2, 8)

            self.video_rs_btn = QPushButton('', self)  # video remove setting button
            self.video_rs_btn.setMinimumHeight(65)
            self.video_rs_btn.setMaximumWidth(85)
            self.video_rs_btn.setIcon(QIcon('./icons/video-editing.png'))
            self.video_rs_btn.setIconSize(QSize(60, 60))
            self.video_rs_btn.setStyleSheet("background-color: #55B0BC;")
            self.grid.addWidget(self.video_rs_btn, 3, 8)

            self.video_conv_btn = QPushButton('', self)  # video conversion button
            self.video_conv_btn.setMinimumHeight(65)
            self.video_conv_btn.setMaximumWidth(85)
            self.video_conv_btn.setIcon(QIcon('./icons/video_conversion.png'))
            self.video_conv_btn.setIconSize(QSize(60, 60))
            self.video_conv_btn.setStyleSheet("background-color: #55B0BC;")
            self.grid.addWidget(self.video_conv_btn, 4, 8)
        else:
            self.video_flag = 0  # off

            self.grid.removeWidget(self.video_sp_btn)
            self.video_sp_btn.deleteLater()
            self.video_sp_btn = None

            self.grid.removeWidget(self.video_ep_btn)
            self.video_ep_btn.deleteLater()
            self.video_ep_btn = None

            self.grid.removeWidget(self.video_rs_btn)
            self.video_rs_btn.deleteLater()
            self.video_rs_btn = None

            self.grid.removeWidget(self.video_conv_btn)
            self.video_conv_btn.deleteLater()
            self.video_conv_btn = None

    # 측정 거리 설정 이벤트
    def measurement_event(self):
        self.change_btn('measurement_trig')
        if Triggers.measurement_trig == 0:  # 슬라이더 열기
            Triggers.measurement_trig += 1
            self.measure_lbl = QLabel('측정거리\n' + str(self.measure_set) + 'cm', self)
            self.grid.addWidget(self.measure_lbl, 0, 8)
            self.measure_lbl.setAlignment(Qt.AlignCenter)

            self.measure_slider = QSlider(Qt.Vertical, self)
            self.measure_slider.setRange(0, 350)
            self.measure_slider.setSingleStep(2)
            self.measure_slider.setStyleSheet("margin-left: 3.5em; margin-bottom: 30px")
            self.grid.addWidget(self.measure_slider, 2, 8, 5, 1)
            self.measure_slider.valueChanged.connect(self.measure_slider_value_changed)

        elif Triggers.measurement_trig > 0:  # 슬라이더 닫기
            Triggers.measurement_trig = 0
            self.grid.removeWidget(self.measure_lbl)
            self.measure_lbl.deleteLater()
            self.measure_lbl = None

            self.grid.removeWidget(self.measure_slider)
            self.measure_slider.deleteLater()
            self.measure_slider = None

    # 측정 거리 설정 슬라이더 값 변경 시 호출되는 함수
    def measure_slider_value_changed(self):
        self.measure_set = self.measure_slider.value()
        self.measure_lbl.setText('측정거리\n' + str(self.measure_set) + 'cm')

    # dB 스케일링 이벤트
    def db_scaling_event(self):
        self.change_btn('db_scaling_trig')

        if Triggers.db_scaling_trig == 0: # 슬라이더 열기
            Triggers.db_scaling_trig += 1
            self.db_set = 0
            self.db_scaling_mode = 0 # Auto
            self.auto_mode = QPushButton('Auto',self)
            self.grid.addWidget(self.auto_mode, 0, 8)
            self.auto_mode.clicked.connect(self.db_mode_change_smart)

            self.dynamic_lbl = QLabel('Dynamic\n' + str(self.db_set), self)
            self.grid.addWidget(self.dynamic_lbl, 1, 8)
            self.dynamic_lbl.setAlignment(Qt.AlignCenter)

            self.db_slider = QSlider(Qt.Vertical,self)
            self.db_slider.setRange(0.5, 50)
            self.db_slider.setSingleStep(2)
            self.db_slider.setStyleSheet("margin-left: 5em; ")
            self.grid.addWidget(self.db_slider, 3, 8, 4, 1)
            self.db_slider.valueChanged.connect(self.db_slider_value_changed)

        elif Triggers.db_scaling_trig > 0:  # 슬라이더 닫기
            Triggers.db_scaling_trig = 0
            self.grid.removeWidget(self.auto_mode)
            self.auto_mode.deleteLater()
            self.auto_mode = None

            self.grid.removeWidget(self.dynamic_lbl)
            self.dynamic_lbl.deleteLater()
            self.dynamic_lbl = None

            self.grid.removeWidget(self.db_slider)
            self.db_slider.deleteLater()
            self.db_slider = None

    # dB 모드 변경(Auto to Smart)
    def db_mode_change_smart(self):
        self.db_scaling_mode += 1  # Smart
        self.grid.removeWidget(self.auto_mode)
        self.auto_mode.deleteLater()
        self.auto_mode = None

        self.grid.removeWidget(self.dynamic_lbl)
        self.dynamic_lbl.deleteLater()
        self.dynamic_lbl = None

        self.smart_mode = QPushButton('Smart', self)
        self.grid.addWidget(self.smart_mode, 0, 8)
        self.smart_mode.clicked.connect(self.db_mode_change_off)

        self.crest_lbl = QLabel('Crest\n' + str(self.db_set), self)
        self.grid.addWidget(self.crest_lbl, 1, 8)
        self.crest_lbl.setAlignment(Qt.AlignCenter)

    # dB 모드 변경(Smart to Off)
    def db_mode_change_off(self):
        self.db_scaling_mode += 1  # Off
        self.grid.removeWidget(self.smart_mode)
        self.smart_mode.deleteLater()
        self.smart_mode = None

        self.grid.removeWidget(self.crest_lbl)
        self.crest_lbl.deleteLater()
        self.crest_lbl = None

        self.off_mode = QPushButton('Off', self)
        self.grid.addWidget(self.off_mode, 0, 8)
        self.off_mode.clicked.connect(self.db_mode_change_exit)

        self.most_db_lbl = QLabel('최고 dB\n' + str(self.db_set), self)
        self.grid.addWidget(self.most_db_lbl, 1, 8)
        self.most_db_lbl.setAlignment(Qt.AlignCenter)

    # dB 모드 변경(Off to Exit)
    def db_mode_change_exit(self):
        Triggers.db_scaling_trig = 0
        self.grid.removeWidget(self.off_mode)
        self.off_mode.deleteLater()
        self.off_mode = None

        self.grid.removeWidget(self.most_db_lbl)
        self.most_db_lbl.deleteLater()
        self.most_db_lbl = None

        self.grid.removeWidget(self.db_slider)
        self.db_slider.deleteLater()
        self.db_slider = None

    # dB 슬라이더 값 변경 시 호출되는 함수
    def db_slider_value_changed(self):
        self.db_set = 0
        self.db_set = self.db_slider.value()
        if self.db_scaling_mode == 0:
            self.dynamic_lbl.setText('Dynamic\n' + str(self.db_set))
        elif self.db_scaling_mode == 1:
            self.crest_lbl.setText('Crest\n' + str(self.db_set))
        elif self.db_scaling_mode == 2:
            self.most_db_lbl.setText('최고 dB\n' + str(self.db_set))

    # 주파수 설정 이벤트
    def frequency_event(self):
        self.change_btn('frequency_flag')

        if self.frequency_flag == 0:  # init or recur
            self.frequency_flag = 1  # on

            if self.recur_flag == 1: # 버튼 순환으로 다시 '사용자지정'모드가 된 경우
                self.grid.removeWidget(self.frequency_mode)
                self.frequency_mode.deleteLater()
                self.frequency_mode = None
                self.grid.removeWidget(self.octave_lbl)
                self.octave_lbl.deleteLater()
                self.octave_lbl = None

            self.frequency_mode = QPushButton("사용자지정")
            self.grid.addWidget(self.frequency_mode, 0, 8)
            self.frequency_mode.clicked.connect(self.frequency_octave)
            self.frequency_mode.setMaximumWidth(90)

            self.max_freq_lbl = QLabel('최대 Freq \n' + str(self.max_freq_set), self)
            self.grid.addWidget(self.max_freq_lbl, 1, 8)
            self.max_freq_lbl.setAlignment(Qt.AlignCenter)

            self.min_freq_lbl = QLabel('최소 Freq \n' + str(self.min_freq_set), self)
            self.grid.addWidget(self.min_freq_lbl, 2, 8)
            self.min_freq_lbl.setAlignment(Qt.AlignCenter)

            self.frequency_slider = QRangeSlider()
            self.frequency_slider.setRange(0, 60)
            self.frequency_slider.setSingleStep(2)
            self.frequency_slider.valueChanged.connect(self.frequency_slider_value_changed)
            self.frequency_slider.setStyleSheet("margin-left: 5em; ")
            self.grid.addWidget(self.frequency_slider, 3, 8, 4, 2)

        else:  #버튼 off
            self.frequency_flag = 0  # off
            self.recur_flag = 0

            text = self.frequency_mode.text()
            self.grid.removeWidget(self.frequency_mode)
            self.frequency_mode.deleteLater()
            self.frequency_mode = None

            if (text == '사용자지정'):
                self.grid.removeWidget(self.max_freq_lbl)
                self.max_freq_lbl.deleteLater()
                self.max_freq_lbl = None

                self.grid.removeWidget(self.min_freq_lbl)
                self.min_freq_lbl.deleteLater()
                self.min_freq_lbl = None

                self.grid.removeWidget(self.frequency_slider)
                self.frequency_slider.deleteLater()
                self.frequency_slider = None
            else:
                self.grid.removeWidget(self.octave_lbl)
                self.octave_lbl.deleteLater()
                self.octave_lbl = None

    # 주파수 설정 이벤트 (Octave 모드)
    def frequency_octave(self):
        self.grid.removeWidget(self.frequency_mode)
        self.frequency_mode.deleteLater()
        self.frequency_mode = None

        self.grid.removeWidget(self.max_freq_lbl)
        self.max_freq_lbl.deleteLater()
        self.max_freq_lbl = None

        self.grid.removeWidget(self.min_freq_lbl)
        self.min_freq_lbl.deleteLater()
        self.min_freq_lbl = None

        self.grid.removeWidget(self.frequency_slider)
        self.frequency_slider.deleteLater()
        self.frequency_slider = None

        self.frequency_mode = QPushButton("Octave")
        self.grid.addWidget(self.frequency_mode, 0, 8)
        self.frequency_mode.clicked.connect(self.frequency_3rd_octave)
        self.frequency_mode.setMaximumWidth(90)

        self.octave_lbl = QComboBox(self)
        self.octave_lbl.addItem('250Hz')
        self.octave_lbl.addItem('500Hz')
        self.octave_lbl.addItem('1000Hz')
        self.octave_lbl.addItem('2000Hz')
        self.octave_lbl.addItem('4000Hz')
        self.octave_lbl.addItem('8000Hz')
        self.octave_lbl.addItem('16000Hz')
        self.grid.addWidget(self.octave_lbl, 1, 8)

    # 주파수 설정 이벤트(3rd Octave 모드)
    def frequency_3rd_octave(self):
        self.grid.removeWidget(self.frequency_mode)
        self.frequency_mode.deleteLater()
        self.frequency_mode = None

        self.grid.removeWidget(self.octave_lbl)
        self.octave_lbl.deleteLater()
        self.octave_lbl = None

        self.recur_flag = 1

        self.frequency_mode = QPushButton("3rd Oct")
        self.grid.addWidget(self.frequency_mode, 0, 8)
        self.frequency_mode.clicked.connect(self.frequency_event)
        self.frequency_mode.setMaximumWidth(90)

        self.octave_lbl = QComboBox(self)
        self.octave_lbl.addItem('250Hz')
        self.octave_lbl.addItem('315Hz')
        self.octave_lbl.addItem('400Hz')
        self.octave_lbl.addItem('500Hz')
        self.octave_lbl.addItem('630Hz')
        self.octave_lbl.addItem('800Hz')
        self.octave_lbl.addItem('1000Hz')
        self.octave_lbl.addItem('1250Hz')
        self.octave_lbl.addItem('1600Hz')
        self.octave_lbl.addItem('2000Hz')
        self.octave_lbl.addItem('2500Hz')
        self.octave_lbl.addItem('3150Hz')
        self.octave_lbl.addItem('4000Hz')
        self.octave_lbl.addItem('5000Hz')
        self.octave_lbl.addItem('6300Hz')
        self.octave_lbl.addItem('8000Hz')
        self.octave_lbl.addItem('10000Hz')
        self.octave_lbl.addItem('12500Hz')
        self.octave_lbl.addItem('16000Hz')
        self.octave_lbl.addItem('20000Hz')

        self.grid.addWidget(self.octave_lbl, 1, 8)

    # 사운드 설정 On/Off
    def sound_control(self):
        self.change_btn('sound_flag')

        if self.sound_flag == 0:  # init or sound off -> sound on
            self.sound_flag = 1  # on
            self.sound_btn.setIcon(QIcon('icons/sound.png'))

            self.no_signal_btn = QPushButton('', self)
            self.no_signal_btn.setMinimumHeight(65)
            self.no_signal_btn.setMaximumWidth(85)
            self.no_signal_btn.setIcon(QIcon('./icons/no-signal.png'))
            self.no_signal_btn.setIconSize(QSize(60, 60))
            self.no_signal_btn.setStyleSheet("background-color: #55B0BC;")
            self.grid.addWidget(self.no_signal_btn, 0, 8)
            self.no_signal_btn.clicked.connect(self.sound_event)

            self.sound_slider = QSlider(Qt.Vertical,self)
            self.sound_slider.setRange(0, 50)
            self.sound_slider.setSingleStep(2)
            self.sound_slider.setStyleSheet("margin-left: 3.5em; margin-bottom: 30px")
            self.grid.addWidget(self.sound_slider, 1, 8, 6, 1)

        else:  # sound on -> sound off
            self.sound_flag = 0  # off
            self.sound_btn.setIcon(QIcon('icons/sound-off.png'))
            self.grid.removeWidget(self.no_signal_btn)
            self.no_signal_btn.deleteLater()
            self.no_signal_btn = None

            self.grid.removeWidget(self.sound_slider)
            self.sound_slider.deleteLater()
            self.sound_slider = None

    # 사운드 On일 때 호출되는 함수
    def sound_event(self):
        if Triggers.sound_trig == 0:  # 전영역 주파수
            Triggers.sound_trig += 1
            self.no_signal_btn.setIcon(QIcon('icons/no-signal.png'))

        elif Triggers.sound_trig > 0:  # 선택 영역 주파수
            Triggers.sound_trig = 0
            self.no_signal_btn.setIcon(QIcon('icons/signal.png'))

    # time setting 이벤트(측정 영상 저장 시간 설정)
    def time_setting_event(self):
        self.change_btn('time_st_flag')
        if self.time_st_flag == 0: # init or time_setting on
            self.time_st_flag = 1 # on

            self.saved_lbl = QLabel('저장시간', self)
            self.grid.addWidget(self.saved_lbl, 0, 8)

            self.time_set = QComboBox(self)
            self.time_set.addItem('10 초')
            self.time_set.addItem('30 초')
            self.time_set.addItem('60 초')
            self.grid.addWidget(self.time_set, 1, 8)

        else:  # time_setting off
            self.time_st_flag = 0  # off
            # print(self.time_set.currentText())

            self.grid.removeWidget(self.saved_lbl)
            self.saved_lbl.deleteLater()
            self.saved_lbl = None

            self.grid.removeWidget(self.time_set)
            self.time_set.deleteLater()
            self.time_set = None

    # time navigation 이벤트(음향 이미지 정밀 분석)
    def time_navigation_event(self):
        if Triggers.time_nv_trig == -1:  # record 중일 때 비활성화
            return
        elif Triggers.time_nv_trig == 0:  # init or on
            self.change_btn('time_nv_trig')

            Triggers.time_nv_trig += 1

            self.time_lbl = QLabel('0')
            self.grid.addWidget(self.time_lbl, 0, 8)
            self.time_lbl.setStyleSheet("margin-left: 2em;")

            self.time_up_btn = QPushButton('', self)
            self.time_up_btn.setMinimumHeight(65)
            self.time_up_btn.setMaximumWidth(85)
            self.time_up_btn.setIcon(QIcon('./icons/up-arrow.png'))
            self.time_up_btn.setIconSize(QSize(60, 60))
            self.time_up_btn.setStyleSheet("background-color: #55B0BC;")
            self.time_up_btn.clicked.connect(self.time_up_event)
            self.grid.addWidget(self.time_up_btn, 1, 8)

            self.slider = QSlider(Qt.Vertical, self)
            self.slider.setRange(0, 50)
            self.slider.setSingleStep(2)
            self.slider.valueChanged.connect(self.slider_value_changed)
            self.slider.setStyleSheet("margin-left: 4em; margin-bottom: 30px")
            self.grid.addWidget(self.slider, 2, 8, 4, 2)

            self.time_down_btn = QPushButton('', self)
            self.time_down_btn.setMinimumHeight(65)
            self.time_down_btn.setMaximumWidth(85)
            self.time_down_btn.setIcon(QIcon('./icons/down-arrow.png'))
            self.time_down_btn.setIconSize(QSize(60, 60))
            self.time_down_btn.setStyleSheet("background-color: #55B0BC;")
            self.time_down_btn.clicked.connect(self.time_down_event)
            self.grid.addWidget(self.time_down_btn, 6, 8)

        elif Triggers.time_nv_trig > 0:
            self.grid.removeWidget(self.time_lbl)
            self.time_lbl.deleteLater()
            self.time_lbl = None

            self.grid.removeWidget(self.time_up_btn)
            self.grid.removeWidget(self.time_down_btn)
            self.time_up_btn.deleteLater()
            self.time_down_btn.deleteLater()
            self.time_up_btn = None
            self.time_down_btn = None

            self.grid.removeWidget(self.slider)
            self.slider.deleteLater()
            self.slider = None

            Triggers.time_nv_trig = 0

    # time_navigation_arrow_btn_event
    def time_up_event(self):
        self.now_time = self.slider.value()
        self.slider.setValue(self.now_time + 1)

    def time_down_event(self):
        self.now_time = self.slider.value()
        self.slider.setValue(self.now_time - 1)

    # time_navigation_slider_event
    def slider_value_changed(self):
        self.time_val = self.slider.value()
        self.time_lbl.setText(str(self.time_val))

    # frequency_slider_event
    def frequency_slider_value_changed(self):
        self.freq_val = self.frequency_slider.value()
        self.max_freq_set = self.freq_val[1]
        self.min_freq_set = self.freq_val[0]
        self.max_freq_lbl.setText('최대 Freq \n' + str(self.max_freq_set))
        self.min_freq_lbl.setText('최소 Freq \n' + str(self.min_freq_set))

    # file open event
    def fileOpen(self):
        fileName = QFileDialog.getOpenFileName(self, self.tr("Open Data Files"), './', self.tr(
            "Data Files (*.csv *.xls *.xlsx *.tdms);; Images (*.png *.xpm *.jpg *.gif);; All Files(*.*)"))
        print("load file : ", fileName[0])
        return fileName


class MeasurementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 측정창 종료 버튼
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')  # 단축키
        exitAction.setStatusTip('Exit application')  # 상태팁
        exitAction.triggered.connect(qApp.quit)  # 어플리케이션 종료

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        Exit = menubar.addMenu('&File')
        Exit.addAction(exitAction)

        filemenu = menubar.addMenu('&Edit')
        filemenu.addAction(exitAction)

        wg = MeasurementWidget()
        self.setCentralWidget(wg)

        self.setWindowTitle('Sound Cam')
        self.resize(720, 480)
        self.show()
