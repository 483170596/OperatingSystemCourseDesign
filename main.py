import sys
import random

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget

from window import Ui_Window


# 进程类
class Progress:
    def __init__(self, pid, arrival_time, sum_time, cpu, io):
        self.id = pid  # 编号
        self.arrival_time = arrival_time  # 到达时间
        self.sum_time = sum_time  # 总时间
        self.cpu = cpu  # cpu请求列表
        self.io = io  # io请求列表
        self.complete = 0  # 已完成部分
        self.start_time = None  # 开始时间
        self.finish_time = None  # 完成时间


# 界面+逻辑
class MyWindow(QWidget, Ui_Window):
    def __init__(self, progress_list):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("模拟进程调度")

        # TODO 当前时间
        self.current_time = 0

        # TODO 当前cpu进程
        self.current_cpu_progress = None

        # TODO 当前io进程
        self.current_io_progress = None

        # TODO FCFS总时间
        self.sum_FCFS_time = 0

        # TODO RR总时间
        self.sum_RR_time = 0

        # TODO 运行标志
        self.run_flag = False

        # TODO 计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_func)

        # TODO 进程列表
        self.progress1 = progress_list[0]
        self.progress2 = progress_list[1]
        self.progress3 = progress_list[2]
        self.progress4 = progress_list[3]
        if self.FCFS_button.isChecked():
            self.progress1.io = []
            self.progress1.cpu = [{"start": 0, "end": self.progress1.sum_time}]
            self.progress2.io = []
            self.progress2.cpu = [{"start": 0, "end": self.progress2.sum_time}]
            self.progress3.io = []
            self.progress3.cpu = [{"start": 0, "end": self.progress3.sum_time}]
            self.progress4.io = []
            self.progress4.cpu = [{"start": 0, "end": self.progress4.sum_time}]
        if self.progress_num_box.value() == 2:
            self.progress_order_list = [self.progress1, self.progress2]
        if self.progress_num_box.value() == 3:
            self.progress_order_list = [self.progress1, self.progress2, self.progress3]
        if self.progress_num_box.value() == 4:
            self.progress_order_list = [self.progress1, self.progress2, self.progress3, self.progress4]
        self.progress_order_list.sort(key=lambda x: x.arrival_time)

        # TODO 就绪队列
        self.ready_queue = []

        # TODO 等待队列
        self.wait_queue = []

        self.sum_turnaround_time = 0
        self.sum_response_time = 0

        # 初始状态下隐藏5个widget
        self.progress1_widget.hide()
        self.progress2_widget.hide()
        self.progress3_widget.hide()
        self.progress4_widget.hide()
        self.result_widget.hide()

        # 绑定create_progress函数，按下创建进程，显示进程widget，并锁定几个条件设置按钮，使能几个功能按钮
        self.create_progress_button.clicked.connect(self.create_progress)

        # 绑定start函数
        self.start_button.clicked.connect(self.start)

        # 绑定re_start函数，按下重新开始，隐藏进程widget，并使能几个条件设置按钮，锁定几个功能按钮
        self.re_start_button.clicked.connect(self.re_start)

        # 绑定stop_continue函数
        self.stop_continue_button.clicked.connect(self.stop_continue)

        # 绑定exit函数
        self.exit_button.clicked.connect(self.exit)

    # TODO FCFS
    def FCFS(self):
        # print(self.current_cpu_progress == self.progress1)
        # print(self.current_cpu_progress)
        # print(self.progress1)
        # print(self.current_cpu_progress.id, self.current_cpu_progress.sum_time, self.current_cpu_progress.complete)
        # print(self.progress1.id, self.progress1.sum_time, self.progress1.complete)

        self.current_cpu_progress.complete += 1
        if self.current_cpu_progress.id == 1:
            self.progress1_bar.setValue(
                int(self.progress1.complete / self.progress1.sum_time * 100))
            self.progress1_state_label.setText("运行")
            if self.progress1.complete == self.progress1.sum_time:
                self.progress1_state_label.setText("完成")
                self.progress1.finish_time = self.current_time
                self.sum_response_time += (self.progress1.start_time - self.progress1.arrival_time)
                self.sum_turnaround_time += (self.progress1.finish_time - self.progress1.arrival_time)
        if self.current_cpu_progress.id == 2:
            self.progress2_bar.setValue(
                int(self.progress2.complete / self.progress2.sum_time * 100))
            self.progress2_state_label.setText("运行")
            if self.progress2.complete == self.progress2.sum_time:
                self.progress2_state_label.setText("完成")
                self.progress2.finish_time = self.current_time
                self.sum_response_time += (self.progress2.start_time - self.progress2.arrival_time)
                self.sum_turnaround_time += (self.progress2.finish_time - self.progress2.arrival_time)
        if self.current_cpu_progress.id == 3:
            self.progress3_bar.setValue(
                int(self.progress3.complete / self.progress3.sum_time * 100))
            self.progress3_state_label.setText("运行")
            if self.progress3.complete == self.progress3.sum_time:
                self.progress3_state_label.setText("完成")
                self.progress3.finish_time = self.current_time
                self.sum_response_time += (self.progress3.start_time - self.progress3.arrival_time)
                self.sum_turnaround_time += (self.progress3.finish_time - self.progress3.arrival_time)
        if self.current_cpu_progress.id == 4:
            self.progress4_bar.setValue(
                int(self.progress4.complete / self.progress4.sum_time * 100))
            self.progress4_state_label.setText("运行")
            if self.progress4.complete == self.progress4.sum_time:
                self.progress4_state_label.setText("完成")
                self.progress4.finish_time = self.current_time
                self.sum_response_time += (self.progress4.start_time - self.progress4.arrival_time)
                self.sum_turnaround_time += (self.progress4.finish_time - self.progress4.arrival_time)

        # 如果当前进程执行完
        if self.current_cpu_progress.complete == self.current_cpu_progress.sum_time:
            # 就绪队列有进程，排第一的进程就可以运行
            if len(self.ready_queue) != 0:
                self.current_cpu_progress = self.ready_queue.pop(0)
                self.current_cpu_progress.start_time = self.current_time
            else:
                # 没有就结束
                self.cpu_state_label.setText("空闲")
                self.cpu_state_button.setStyleSheet("""
                QPushButton {
    border: 1px solid black; /* 设置黑色边框，可以根据需要调整边框宽度 */
    background-color: white; /* 设置背景颜色为白色 */
    border-radius: 10px; /* 设置按钮的边界半径为按钮宽度和高度的一半，以使其呈现为圆形 */
    width: 20px; /* 设置按钮的宽度 */
    height: 20px; /* 设置按钮的高度 */
}""")
                self.timer.stop()
                self.stop_continue_button.setEnabled(False)
                self.response_time_label.setText(f"{self.sum_response_time / self.progress_num_box.value():.2f}")
                self.turnaround_time_label.setText(f"{self.sum_turnaround_time / self.progress_num_box.value():.2f}")
                self.cpu_efficiency_label.setText("100%")
                return

        if self.current_cpu_progress != self.progress1 and self.progress1.complete == 0 and self.progress1.arrival_time == self.current_time:
            self.ready_queue.append(self.progress1)
            self.progress1_state_label.setText("就绪")
        if self.current_cpu_progress != self.progress2 and self.progress2.complete == 0 and self.progress2.arrival_time == self.current_time:
            self.ready_queue.append(self.progress2)
            self.progress2_state_label.setText("就绪")
        if self.current_cpu_progress != self.progress3 and self.progress3.complete == 0 and self.progress3.arrival_time == self.current_time and (
                self.progress_num_box.value() == 3 or self.progress_num_box.value() == 4):
            self.ready_queue.append(self.progress3)
            self.progress3_state_label.setText("就绪")
        if self.current_cpu_progress != self.progress4 and self.progress4.complete == 0 and self.progress4.arrival_time == self.current_time and self.progress_num_box.value() == 4:
            self.ready_queue.append(self.progress4)
            self.progress4_state_label.setText("就绪")

        self.cpu_state_label.setText(f"运行：进程{self.current_cpu_progress.id}")
        self.cpu_state_button.setStyleSheet("""
        QPushButton {
    border: 1px solid black; /* 设置黑色边框，可以根据需要调整边框宽度 */
    background-color: red; /* 设置背景颜色为红色 */
    border-radius: 10px; /* 设置按钮的边界半径为按钮宽度和高度的一半，以使其呈现为圆形 */
    width: 20px; /* 设置按钮的宽度 */
    height: 20px; /* 设置按钮的高度 */
}""")

        if len(self.ready_queue) == 0:
            self.ready_queue_label.setText("空")
        else:
            read_queue_label_text = ""
            for ready_progress in self.ready_queue:
                read_queue_label_text += str(ready_progress.id)
            self.ready_queue_label.setText(read_queue_label_text)

    # TODO RR
    def RR(self):
        pass

    # TODO
    def update_func(self):
        if self.current_time == 0:
            self.current_cpu_progress = self.ready_queue.pop(0)
            self.current_cpu_progress.start_time = 0
        self.current_time += 1
        if self.FCFS_button.isChecked():
            self.FCFS()
        if self.RR_button.isChecked():
            self.RR()

    # 绑定create_progress_button，按下创建进程，显示进程widget
    def create_progress(self):
        self.sum_turnaround_time = 0
        self.sum_response_time = 0
        for progress in self.progress_order_list:
            if progress.arrival_time == 0 and progress.cpu[0]["start"] == 0:
                if progress.id == 1:
                    self.progress1_state_label.setText("就绪")
                if progress.id == 2:
                    self.progress2_state_label.setText("就绪")
                if progress.id == 3:
                    self.progress3_state_label.setText("就绪")
                if progress.id == 4:
                    self.progress4_state_label.setText("就绪")
                self.ready_queue.append(progress)
        for progress in self.progress_order_list:
            if len(progress.io) != 0:
                if progress.arrival_time == 0 and progress.io[0]["start"] == 0:
                    self.wait_queue.append(progress)
        # 锁定
        self.progress_num_box.setEnabled(False)
        self.FCFS_button.setEnabled(False)
        self.RR_button.setEnabled(False)
        self.time_slicing_box.setEnabled(False)
        self.create_progress_button.setEnabled(False)
        # 使能
        self.start_button.setEnabled(True)
        self.re_start_button.setEnabled(True)
        # 显示
        if len(self.ready_queue) == 0:
            self.ready_queue_label.setText("空")
        else:
            read_queue_label_text = ""
            for ready_progress in self.ready_queue:
                read_queue_label_text += str(ready_progress.id)
            self.ready_queue_label.setText(read_queue_label_text)

        if len(self.wait_queue) == 0:
            self.wait_queue_label.setText("空")
        else:
            wait_queue_label_text = ""
            for wait_progress in self.wait_queue:
                wait_queue_label_text += str(wait_progress.id)
            self.ready_queue_label.setText(wait_queue_label_text)

        unit_time_length = 450 / max([progress.sum_time for progress in self.progress_order_list])
        self.progress1_bar.setMaximumWidth(int(unit_time_length * self.progress1.sum_time))
        self.progress2_bar.setMaximumWidth(int(unit_time_length * self.progress2.sum_time))
        self.progress1_widget.show()
        self.progress2_widget.show()
        self.progress1_bar.setStyleSheet(self.get_progressbar_stylesheet(self.progress1))
        self.progress2_bar.setStyleSheet(self.get_progressbar_stylesheet(self.progress2))
        if self.progress_num_box.value() == 3:
            self.progress3_bar.setStyleSheet(self.get_progressbar_stylesheet(self.progress3))
            self.progress3_widget.show()
            self.progress3_bar.setMaximumWidth(int(unit_time_length * self.progress3.sum_time))
        if self.progress_num_box.value() == 4:
            self.progress3_bar.setStyleSheet(self.get_progressbar_stylesheet(self.progress3))
            self.progress4_bar.setStyleSheet(self.get_progressbar_stylesheet(self.progress4))
            self.progress3_widget.show()
            self.progress4_widget.show()
            self.progress3_bar.setMaximumWidth(int(unit_time_length * self.progress3.sum_time))
            self.progress4_bar.setMaximumWidth(int(unit_time_length * self.progress4.sum_time))
        self.result_widget.show()
        self.progress1_arrival_time_label.setText(f"{self.progress1.arrival_time}")
        self.progress2_arrival_time_label.setText(f"{self.progress2.arrival_time}")
        self.progress3_arrival_time_label.setText(f"{self.progress3.arrival_time}")
        self.progress4_arrival_time_label.setText(f"{self.progress4.arrival_time}")

    # TODO 开始运行
    def start(self):
        self.run_flag = True
        self.start_button.setEnabled(False)
        self.stop_continue_button.setEnabled(True)
        self.timer.start(100)

    # 重新开始
    def re_start(self):
        self.ready_queue.clear()
        self.timer.stop()
        self.current_time = 0
        self.run_flag = False
        self.stop_continue_button.setText("暂停")
        self.progress1.complete = 0
        self.progress2.complete = 0
        self.progress3.complete = 0
        self.progress4.complete = 0
        # 隐藏5个widget
        self.progress1_widget.hide()
        self.progress2_widget.hide()
        self.progress3_widget.hide()
        self.progress4_widget.hide()
        self.result_widget.hide()

        self.progress_num_box.setEnabled(True)
        self.FCFS_button.setEnabled(True)
        self.RR_button.setEnabled(True)
        self.time_slicing_box.setEnabled(True)
        self.create_progress_button.setEnabled(True)
        self.start_button.setEnabled(True)

        self.start_button.setEnabled(False)
        self.re_start_button.setEnabled(False)
        self.stop_continue_button.setEnabled(False)

        self.cpu_state_button.setStyleSheet("""
            QPushButton {
                border: 1px solid black; /* 设置黑色边框，可以根据需要调整边框宽度 */
                background-color: white; /* 设置背景颜色为白色 */
                border-radius: 10px; /* 设置按钮的边界半径为按钮宽度和高度的一半，以使其呈现为圆形 */
                width: 20px; /* 设置按钮的宽度 */
                height: 20px; /* 设置按钮的高度 */
                }
        """)
        self.io_state_button.setStyleSheet("""
            QPushButton {
                border: 1px solid black; /* 设置黑色边框，可以根据需要调整边框宽度 */
                background-color: white; /* 设置背景颜色为白色 */
                border-radius: 10px; /* 设置按钮的边界半径为按钮宽度和高度的一半，以使其呈现为圆形 */
                width: 20px; /* 设置按钮的宽度 */
                height: 20px; /* 设置按钮的高度 */
            }
        """)
        self.cpu_state_label.setText("空闲")
        self.io_state_label.setText("空闲")

        self.ready_queue_label.setText("空")
        self.wait_queue_label.setText("空")

        self.progress1_bar.setValue(0)
        self.progress2_bar.setValue(0)
        self.progress3_bar.setValue(0)
        self.progress4_bar.setValue(0)
        self.progress1_state_label.setText("-")
        self.progress2_state_label.setText("-")
        self.progress3_state_label.setText("-")
        self.progress4_state_label.setText("-")

        self.turnaround_time_label.setText("-")
        self.response_time_label.setText("-")
        self.cpu_efficiency_label.setText("-")

        self.progress1_arrival_time_label.setText("-")
        self.progress2_arrival_time_label.setText("-")
        self.progress3_arrival_time_label.setText("-")
        self.progress4_arrival_time_label.setText("-")

    # TODO 暂停继续
    def stop_continue(self):
        if self.run_flag:
            self.run_flag = not self.run_flag
            self.timer.stop()
            self.stop_continue_button.setText("继续")
        else:
            self.stop_continue_button.setText("暂停")
            self.start()

    # 退出
    @staticmethod
    def exit():
        exit(0)

    # 获取progress_bar的stylesheet
    @staticmethod
    def get_progressbar_stylesheet(progress):
        if len(progress.cpu) == 1 and len(progress.io) == 0:
            return f"""
                QProgressBar {{
                    text-align: left; /* 设置文本左对齐 */
                    border: 1px solid black; /* 设置黑色边框，可以根据需要调整边框宽度 */
                    background-color: red;
                }}

                QProgressBar::chunk {{
                    background-color: blue; /* 设置进度条颜色为蓝色 */
                }}

                QProgressBar::text {{
                    position: relative; /* 使文本垂直居中 */
                    top: 50%; /* 使文本垂直居中 */
                    transform: translateY(-50%); /* 使文本垂直居中 */
                }}
            """
        if len(progress.cpu) + len(progress.io) == 2:
            if progress.cpu[0]["start"] == 0:
                return f"""
                    QProgressBar {{
                        text-align: left; /* 设置文本左对齐 */
                        border: 1px solid black; /* 设置黑色边框，可以根据需要调整边框宽度 */
                        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 255), stop:{progress.cpu[0]["end"] / progress.sum_time :.2f} rgba(255, 0, 0, 255), stop:{progress.io[0]["start"] / progress.sum_time} rgba(0, 255, 0, 255), stop:1 rgba(0, 255, 0, 255))
                    }}

                    QProgressBar::chunk {{
                        background-color: blue; /* 设置进度条颜色为蓝色 */
                    }}

                    QProgressBar::text {{
                        position: relative; /* 使文本垂直居中 */
                        top: 50%; /* 使文本垂直居中 */
                        transform: translateY(-50%); /* 使文本垂直居中 */
                    }}
                """
            if progress.io[0]["start"] == 0:
                return f"""
                    QProgressBar {{
                        text-align: left; /* 设置文本左对齐 */
                        border: 1px solid black; /* 设置黑色边框，可以根据需要调整边框宽度 */
                        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 255, 0, 255), stop:{progress.io[0]["end"] / progress.sum_time} rgba(0, 255, 0, 255), stop:{progress.cpu[0]["start"] / progress.sum_time} rgba(255, 0, 0, 255), stop:1 rgba(255, 0, 0, 255))
                    }}

                    QProgressBar::chunk {{
                        background-color: blue; /* 设置进度条颜色为蓝色 */
                    }}

                    QProgressBar::text {{
                        position: relative; /* 使文本垂直居中 */
                        top: 50%; /* 使文本垂直居中 */
                        transform: translateY(-50%); /* 使文本垂直居中 */
                    }}
                """
        if len(progress.cpu) + len(progress.io) == 3:
            if progress.cpu[0]["start"] == 0:
                return f"""
                        QProgressBar {{
                            text-align: left; /* 设置文本左对齐 */
                            border: 1px solid black; /* 设置黑色边框，可以根据需要调整边框宽度 */
                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 255), stop:{progress.cpu[0]["end"] / progress.sum_time} rgba(255, 0, 0, 255), stop:{progress.io[0]["start"] / progress.sum_time} rgba(0, 255, 0, 255), stop:{progress.io[0]["end"] / progress.sum_time} rgba(0, 255, 0, 255),stop:{progress.cpu[1]["start"] / progress.sum_time} rgba(255, 0, 0, 255),stop:1 rgba(255, 0, 0, 255))
                        }}

                        QProgressBar::chunk {{
                            background-color: blue; /* 设置进度条颜色为蓝色 */
                        }}

                        QProgressBar::text {{
                            position: relative; /* 使文本垂直居中 */
                            top: 50%; /* 使文本垂直居中 */
                            transform: translateY(-50%); /* 使文本垂直居中 */
                        }}
                    """
            if progress.io[0]["start"] == 0:
                return f"""
                    QProgressBar {{
                        text-align: left; /* 设置文本左对齐 */
                        border: 1px solid black; /* 设置黑色边框，可以根据需要调整边框宽度 */
                        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 255, 0, 255), stop:{progress.io[0]["end"] / progress.sum_time} rgba(0, 255, 0, 255), stop:{progress.cpu[0]["start"] / progress.sum_time} rgba(255, 0, 0, 255), stop:{progress.cpu[0]["end"] / progress.sum_time} rgba(255, 0, 0, 255),stop:{progress.io[1]["start"] / progress.sum_time} rgba(0, 255, 0, 255),stop:1 rgba(0, 255, 0, 255))
                    }}

                    QProgressBar::chunk {{
                        background-color: blue; /* 设置进度条颜色为蓝色 */
                    }}

                    QProgressBar::text {{
                        position: relative; /* 使文本垂直居中 */
                        top: 50%; /* 使文本垂直居中 */
                        transform: translateY(-50%); /* 使文本垂直居中 */
                    }}
                """


if __name__ == '__main__':
    app = QApplication(sys.argv)

    p1_sum_time = random.randint(9, 15)

    p2_arrival_time = random.randint(0, 8)
    p2_sum_time = random.randint(9, 15)

    p3_arrival_time = random.randint(0, 8)
    p3_sum_time = random.randint(9, 15)

    p4_arrival_time = random.randint(0, 8)
    p4_sum_time = random.randint(9, 15)

    p1 = Progress(1, 0, p1_sum_time * 10, [{"start": 0, "end": 80}], [{"start": 81, "end": p1_sum_time * 10}])
    p2 = Progress(2, p2_arrival_time * 10, p2_sum_time * 10,
                  [{"start": 0, "end": 40}, {"start": 61, "end": p2_sum_time * 10}],
                  [{"start": 41, "end": 60}])
    p3 = Progress(3, p3_arrival_time * 10, p3_sum_time * 10, [{"start": 21, "end": 80}],
                  [{"start": 0, "end": 20}, {"start": 81, "end": p3_sum_time * 10}])
    p4 = Progress(4, p4_arrival_time * 10, p4_sum_time * 10, [{"start": 31, "end": p4_sum_time * 10}],
                  [{"start": 0, "end": 30}])

    ui = MyWindow([p1, p2, p3, p4])
    ui.show()
    sys.exit(app.exec())
