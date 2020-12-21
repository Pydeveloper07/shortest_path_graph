from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, \
    QLabel, QLineEdit, QPushButton, QSpacerItem, QMessageBox
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from main import Graph
from graph_complex import edges, vertex_list
import sys
import time

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.width = 1000
        self.height = 800
        self.graph = None
        self.file = "graph-complex.png"
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
        self.setGeometry(int((window_w-self.width)/2), int((window_h-self.height)/2), self.width, self.height)
        self.setWindowTitle("Graph Window")
        self.setLayout(self.vbox)
        self.show()

    def init_topbar(self):
        hbox = QHBoxLayout()
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
        left_spacer = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        right_spacer = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        tw_label = QLabel("Total weight: ")
        self.result_label.setMinimumWidth(30)

        hbox.addSpacerItem(left_spacer)
        hbox.addWidget(src_label)
        hbox.addWidget(self.src_input)
        hbox.addWidget(dest_label)
        hbox.addWidget(self.dest_input)
        hbox.addWidget(submit_btn)
        hbox.addSpacerItem(right_spacer)
        hbox.addWidget(tw_label)
        hbox.addWidget(self.result_label)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())