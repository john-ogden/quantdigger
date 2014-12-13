# -*- coding: utf8 -*-
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.widgets import Cursor
from matplotlib.widgets import MultiCursor
import matplotlib.pyplot as plt


class TechnicWidget(FigureCanvasQTAgg):
    def __init__(self, parent=None, *args):
        self.fig = plt.figure()
        self.cross_cursor = None
        self.v_cursor = None
        self.add_subplot(*args)
        self.connect()
        for ax in self.axes:
            ax.format_coord = self.format_coord 
        super(TechnicWidget, self).__init__(self.fig)
        self.setParent(parent)


    def connect(self):
        """
        matplotlib信号连接。
        """
        self.cidpress = self.fig.canvas.mpl_connect( "button_press_event", self.on_press)
        self.cidrelease = self.fig.canvas.mpl_connect( "button_release_event", self.on_release)
        self.cidmotion = self.fig.canvas.mpl_connect( "motion_notify_event", self.on_motion)

        self.fig.canvas.mpl_connect('axes_enter_event', self.enter_axes)
        self.fig.canvas.mpl_connect('axes_leave_event', self.leave_axes)

    def disconnect(self):
        self.fig.canvas.mpl_disconnect(self.cidmotion)
        self.fig.canvas.mpl_disconnect(self.cidrelease)
        self.fig.canvas.mpl_disconnect(self.cidpress)


    def on_press(self, event):
        pass

    def on_release(self, event):
        pass

    def on_motion(self, event):
        pass


    def enter_axes(self, event):
        #event.inaxes.patch.set_facecolor('yellow')
        # 只有当前axes会闪烁。
        axes = [ax for ax in self.fig.axes if ax is not event.inaxes]
        self.v_cursor = MultiCursor(event.canvas, axes, color='r', lw=2, horizOn=False, vertOn=True)
        self.cross_cursor = Cursor(event.inaxes, useblit=True, color='red', linewidth=2, vertOn=True, horizOn=True)
        event.canvas.draw()

    def leave_axes(self, event):
        del self.v_cursor
        del self.cross_cursor
        #event.inaxes.patch.set_facecolor('white')
        #event.canvas.draw()

    def add_subplot(self, *args):
        num_axes = sum(args)
        for i, ratio in enumerate(args):
            if i > 0:
                plt.subplot2grid((num_axes, 1), (sum(args[:i]), 0),
                                 rowspan = ratio, sharex = self.fig.axes[0])
            else:
                plt.subplot2grid((num_axes, 1), (sum(args[:i]), 0), rowspan = ratio)

        #for ax in self.fig.axes:
            #ax.set_xticklabels([])

    def subplots_adjust(self, left, bottom, right, top, wspace=None, hspace=None):
        plt.subplots_adjust(left, bottom, right, top, wspace, hspace)

    @property
    def axes(self):
        return self.fig.axes

    def format_coord(self, x, y):
        """ 状态栏信息显示 """
        return "x=%.2f, y=%.2f" % (x, y)

    def draw_axes(self, ith, func):
        """传递绘图函数，画第ith个图。
        
        Args:
            ith (number): 待绘axes的编号。
            func (function): 绘图函数。
        """
        try:
            axes = self.axes[ith]
        except IndexError as e:
            print(e)
        else:
            func(axes)