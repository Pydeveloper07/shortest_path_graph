from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, \
    QLabel, QLineEdit, QPushButton, QSpacerItem, QMessageBox
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from graph import Graph
from graph_complex import edges, vertex_list
from sound_recorder import record
from speech_to_text_converter import convert_speech_to_text
from text_to_speech_converter import convert_text_to_speech
from voice_player import play_audio_file
import time


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.width = 1000
        self.height = 800
        self.graph = None
        self.vertex_identifiers = [vertex[0] for vertex in vertex_list.values()]
        self.file = "graph-complex.png"
        self.shortest_path = None
        self.response_voice_path = None
        self.src_input = QLineEdit()
        self.dest_input = QLineEdit()
        self.result_label = QLabel()
        self.canvas_label = QLabel()
        self.canvas_label.setMinimumSize(978, 739)
        self.canvas_label.setMaximumSize(978, 739)
        self.vbox = QVBoxLayout()
        self.setStyleSheet("background: white")
        self.init_graph()
        self.init_ui()
        self.init_topbar()
        self.init_sub_bar()
        self.init_canvas()

    def init_graph(self):
        v_list = []
        for key in vertex_list.keys():
            v_list.append(vertex_list[key])
        self.graph = Graph(v_list)
        self.init_edges()

    def init_edges(self):
        for key in edges.keys():
            self.graph.add_edge(edges[key][0], edges[key][1], edges[key][2])

    def init_ui(self):
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        window_h = screen_rect.height()
        window_w = screen_rect.width()
        # self.setMaximumSize(self.width, self.height)
        self.setMinimumSize(self.width, self.height)
        self.setGeometry(int((window_w - self.width) / 2), int((window_h - self.height) / 2), self.width, self.height)
        self.setWindowTitle("Graph Window")
        self.setLayout(self.vbox)
        self.show()

    def init_topbar(self):
        self.hbox = QHBoxLayout()
        src_label = QLabel("Source:")
        src_label.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        self.src_input.setMaximumWidth(50)
        dest_label = QLabel("Destination:")
        dest_label.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        self.dest_input.setMaximumWidth(50)
        submit_btn = QPushButton("FIND PATH")
        submit_btn.setStyleSheet("background: green; color:white; padding: 5px 10px;")
        submit_btn.setIcon(QtGui.QIcon("search.png"))
        submit_btn.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        submit_btn.clicked.connect(self.find_shortest_path)
        record_btn = QPushButton("Record")
        record_btn.setStyleSheet(
            "background: #46eaf2; color:#000ead; padding: 5px 10px; margin-left:5px; margin-right: 5px;"
        )
        record_btn.setIcon(QtGui.QIcon("microphone.png"))
        record_btn.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        record_btn.clicked.connect(self.record)
        play_button = QPushButton("Play")
        play_button.setStyleSheet(
            "background: #46eaf2; color:#000ead; padding: 5px 10px; margin-left:5px; margin-right: 5px;"
        )
        # play_button.setIcon(QtGui.QIcon("microphone.png"))
        play_button.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        play_button.clicked.connect(self.play)
        left_spacer = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        right_spacer = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        tw_label = QLabel("Total weight: ")
        self.result_label.setMinimumWidth(30)

        self.hbox.addSpacerItem(left_spacer)
        self.hbox.addWidget(src_label)
        self.hbox.addWidget(self.src_input)
        self.hbox.addWidget(dest_label)
        self.hbox.addWidget(self.dest_input)
        self.hbox.addWidget(submit_btn)
        self.hbox.addWidget(record_btn)
        self.hbox.addWidget(play_button)
        self.hbox.addSpacerItem(right_spacer)
        self.hbox.addWidget(tw_label)
        self.hbox.addWidget(self.result_label)
        self.vbox.addLayout(self.hbox)

    def init_sub_bar(self):
        hbox = QHBoxLayout()

        rec_label = QLabel()
        rec_label.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        rec_label.setObjectName("recordIndicator")
        left_spacer = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        right_spacer = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        hbox.addSpacerItem(left_spacer)
        hbox.addWidget(rec_label)
        hbox.addSpacerItem(right_spacer)
        self.vbox.addLayout(hbox)

    def init_canvas(self):
        self.canvas_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        canvas = QtGui.QPixmap(self.file)
        self.canvas_label.setPixmap(canvas)
        vspacer = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.vbox.addSpacerItem(vspacer)
        self.vbox.addWidget(self.canvas_label, alignment=QtCore.Qt.AlignCenter)
        vspacer = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.vbox.addSpacerItem(vspacer)

    def find_shortest_path(self):
        source = self.src_input.text().upper().strip()
        destination = self.dest_input.text().upper().strip()
        result = self.__find_path(source, destination)
        if isinstance(result, list):
            self.shortest_path = result

    def __find_path(self, source, destination):
        if not source or not destination:
            if not source and not destination:
                self.show_error_msg("Please specify the SOURCE and DESTINATION!")
                return
            elif not source:
                self.show_error_msg("Please specify the SOURCE!")
                return
            else:
                self.show_error_msg("Please specify the DESTINATION!")
                return
        flag, result = self.graph.shortest_path(source, destination)
        if not flag:
            self.canvas_label.setPixmap(QtGui.QPixmap(self.file))
            self.show_error_msg(result)
        else:
            self.result_label.setText(str(result[-1]))
            self.canvas_label.setPixmap(QtGui.QPixmap(self.file))
            self.draw_shortest_path(result)

        return result

    def show_error_msg(self, msg):
        msgbox = QMessageBox(self)
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setText(msg)
        msgbox.setStandardButtons(QMessageBox.Ok)
        retval = msgbox.exec_()

    def draw_shortest_path(self, path):
        total_weight = path[-1]
        path = path[:-1]
        painter = QtGui.QPainter(self.canvas_label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor("#249c00"))
        painter.setPen(pen)
        point_list = []
        for x in path:
            point_list.append(QtCore.QPoint(
                self.graph.coordinate_of_vertices[x][0],
                self.graph.coordinate_of_vertices[x][1]
            ))
        polygon = QtGui.QPolygonF(point_list)
        painter.drawPolyline(polygon)
        time.sleep(0.5)
        self.update()
        painter.end()

    def set_recording_indicator_status(self, status_text):
        rec_indicator = self.findChild(QLabel, "recordIndicator")
        rec_indicator.setText(status_text)

    def record(self):
        try:
            self.set_recording_indicator_status("Processing your voice...")
            audio_path = record()
            result = convert_speech_to_text(audio_path)
            self.__process_result(result)
            self.set_recording_indicator_status("")
        except Exception:
            self.show_error_msg("Something went wrong.")

    def __process_result(self, result):
        try:
            result = [ch.upper() for ch in result.split()]
            inters = tuple(set(self.vertex_identifiers).intersection(set(result)))
            source, destination = tuple(sorted(inters, key=lambda x: result.index(x)))
            self.src_input.setText(source)
            self.dest_input.setText(destination)
            result = self.__find_path(source, destination)
            if isinstance(result, list):
                self.shortest_path = result
            else:
                self.show_error_msg(result)
            self.__prepare_voice_response()
        except Exception:
            self.show_error_msg("Something went wrong during processing voice.")

    def __prepare_voice_response(self):
        if self.shortest_path:
            text = self.__convert_path_to_speech_text()
        else:
            self.show_error_msg("Path not found.")
            return
        self.response_voice_path = convert_text_to_speech(text)

    def play(self):
        if self.response_voice_path:
            play_audio_file(self.response_voice_path)
        else:
            self.show_error_msg("No response found to play.")

    def __convert_path_to_speech_text(self):
        text = "Take the route: "
        path = self.shortest_path[:-1]
        path_to_text = ', '.join(path)
        text += path_to_text
        text += f" The cost is {self.shortest_path[-1]}"

        return text

