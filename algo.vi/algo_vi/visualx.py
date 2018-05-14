#coding=utf-8
# =================
# author: zhouxin
# start_date： 171112
# description: objs in this file contains varity of visualization process methods
# =================

from matplotlib import pyplot as plt
from matplotlib import animation
import abc
import pyaudio
from settings import COLOR_MAPPING, AUDIO_MAPPING, FINISHED
from makesound import play_tone
# plt.rcParams['animation.ffmpeg_path'] = "C:\Program Files\ImageMagick-7.0.7-Q16/ffmpeg.exe"
# plt.rcParams['animation.convert_path'] = r"C:\Program Files\ImageMagick-7.0.7-Q16\magick.exe"
# plt.rcParams['animation.ffmpeg_args'] = '-report'
# plt.rcParams['animation.bitrate'] = 2000

class Visual(object, metaclass=abc.ABCMeta):

    def __init__(self, *args, **kw):
        # basic matplotlib configuration
        self.fig, self.ax = plt.subplots()
        # self.fig = plt.figure()
        self.kw = kw
        self.audio = pyaudio.PyAudio()

        # fig set
        self._fig_conf()

        # axis set
        self._axis_conf()

        # basic animation config
        self.frames = kw.get('frames', 200)
        self.interval = kw.get('interval', 10)

    def _fig_conf(self):
        '''as the method name says'''
        facecolor = self.kw.get('facecolor', 'white')
        title = self.kw.get('title', '')
        self.fig.set_facecolor(facecolor)
        plt.title(title)

    def _axis_conf(self):
        '''set axis paras'''
        self.ax.get_yaxis().set_visible(False)
        self.ax.get_xaxis().set_visible(False)
        self.ax.set_frame_on(False)
        

class ViSort(Visual):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._data = kw.get('od', [])  # od --> ordereddict
        self._data.extend(FINISHED)
        self.frames = range(1, len(self._data))
        self.count = 0
        
    def _ini_animate(self):
        '''init func for animation'''
        data = self._data[0]
        length = len(data)

        height = data.keys()
        left = list(range(length))
        color = data.values()
        # self.ax.set_xticklabels([0]+list(data.keys()))
        self.bar = plt.bar(left, height, color=color)
        return self.bar

    def _animate(self, item):
        '''animation func'''
        data = self._data[item]
        f = None
        for patch, h, c in zip(self.bar, data.keys(), 
                               data.values()):
            b = r'#%02x%02x%02x' % tuple([int(i * 255) for i in patch.get_fc()[:3]])
            if b.lower() != c.lower() and c.lower() != COLOR_MAPPING['OUT1']:
                if h < len(AUDIO_MAPPING):
                    f = AUDIO_MAPPING[h]
                else:
                    f = h * 100
            patch.set_height(h)
            patch.set_color(c)
        if f:
            play_tone(self.stream, frequency=f)

        # self.ax.set_xticklabels([0]+list(data.keys()))
        return self.bar


        

    def show(self):
        # init sound stream
        self.stream = self.audio.open(format=pyaudio.paFloat32,
            channels=1, rate=44100, output=1)
        
        # interval = self.kw.get('interval', 100)
        # interval = interval // 1000
        '''show animation'''
        anis = animation.FuncAnimation(self.fig, 
                                        self._animate, 
                                        init_func=self._ini_animate,
                                        frames=self.frames, 
                                        interval=self.interval,
                                        repeat=False
                                        )
        # anis.save("a.gif", writer='imagemagick', fps=60, bitrate=-1)
        plt.show()

        self.stream.close()
        self.audio.terminate()
