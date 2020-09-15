import os
from psychopy import gui, event, clock
from psychopy.visual import Window, TextStim, Rect, RatingScale

class Button(object):
    START, END = range(2)
    def __init__(self, win, pos, width, height, name):
        self.name = name
        self.rect = Rect(win, height=height, width=width, units='norm', pos=pos)
        self.mouse = event.Mouse(win=win)
        self.caption = TextStim(win, text='选择', height=height - 0.01 , pos=pos, units='norm', color=(0, 0, 0), colorSpace='rgb255')
        self.state = self.START
        
    def draw(self):
        x, y = self.mouse.getPos()
        if self.rect.contains(x, y, units='norm'):
            self.rect.setLineColor(color=(0, 0, 0), colorSpace='rgb255')
            self.caption.setColor(color=(0, 0, 0), colorSpace='rgb255')
        else:
            self.rect.setLineColor(color=(255, 255, 255), colorSpace='rgb255')
            self.caption.setColor(color=(255, 255, 255), colorSpace='rgb255')
        self.rect.draw()
        self.caption.draw()
    
    def process(self):
        x, y = self.mouse.getPos()
        if self.rect.contains(x, y, units='norm') and self.mouse.getPressed()[0] == 1:
            self.state = self.END


class Cover(object):
    COVER, SHOW = range(2)
    def __init__(self, win, pos, name, detail_file, sub_id, test_id, width=0.25, height=0.1, color=(96, 96, 96)):
        self.name = name
        self.rect = Rect(win, height=height, width=width, units='norm', pos=pos)
        self.rect.setFillColor(color=color, colorSpace='rgb255')
        self.rect.setLineColor(color=color, colorSpace='rgb255')
        self.caption = TextStim(win, text=name, height=height - 0.05 , pos=pos, units='norm', color=(0, 0, 0), colorSpace='rgb255')
        self.mouse = event.Mouse(win=win)
        self.state = self.COVER
        self.time = 0
        self.single_time = 0
        self.last_state = self.COVER
        self.last_time = 0
        self.clk = clock.Clock()

        self.detail_file = detail_file
        self.sub_id = sub_id
        self.test_id = test_id
        
    def draw(self):
        if self.state == self.COVER:
            self.rect.draw()
            self.caption.draw()
        elif self.state == self.SHOW:
            pass
    
    def process(self):
        x, y = self.mouse.getPos()
        # click to see the information, uncomment the following line and comment the line after the following line
        # if self.rect.contains(x, y, units='norm') and self.mouse.getPressed()[0] == 1:
        if self.rect.contains(x, y, units='norm'):
            self.state = self.SHOW
        elif not self.rect.contains(x, y, units='norm'):
            self.state = self.COVER
        if self.last_state == self.SHOW:
            this_time = self.clk.getTime() - self.last_time
            self.time += this_time
            self.single_time += this_time
            # time记录累加时间，single_time记录单次时间
            if self.state == self.COVER:
                self.detail_file.write(','.join((str(self.sub_id), str(self.test_id), str(self.name), str(self.single_time))))
                self.detail_file.write('\n')
                self.single_time = 0
        self.last_time = self.clk.getTime()
        self.last_state = self.state
        

class Trial(object):
    def __init__(self, win, test_file, sum_file, detail_file, sub_id):
        self.win = win
        self.test_file = test_file
        self.sum_file = sum_file
        self.detail_file = detail_file
        self.sub_id = sub_id
        self.test_id = self.test_file.split('.')[0]

        # 处理文件输入
        file_handle = open(os.path.join('tests', test_file), 'r', encoding='utf-8')
        self.description = TextStim(win, text=file_handle.readline(), height=0.05, pos=(0, 0.9), units='norm', color=(0, 0, 0), colorSpace='rgb255')
        self.opt_num = int(file_handle.readline())
        self.opts = []
        for i in range(self.opt_num):
            choices = {}
            choices['choices_name'] = file_handle.readline().rstrip('\n')
            choices['choices_num'] = int(file_handle.readline())
            for j in range(choices['choices_num']):
                line = file_handle.readline()
                choices[line.split(' ')[0]] = line.split(' ')[1].rstrip('\n')
            self.opts.append(choices)
        file_handle.close()

        # 写入表头
        self.keys = []
        sum_write = ['sub_id', 'test_id', 'choice']
        for i in self.opts:
            for j in i.keys():
                if j != 'choices_name' and j != 'choices_num':
                    self.keys.append(j)
                    sum_write.append(j)
        sum_file.write(','.join(sum_write))
        sum_file.write('\n')

        detail_write = ('sub_id', 'test_id', 'action', 'time')
        detail_file.write(','.join(detail_write))
        detail_file.write('\n')

        # 生成texts和covers
        self.texts = {}
        self.covers = {}
        k = 0
        for opt in self.opts:
            p = 0
            for i in opt.keys():
                if i != 'choices_name' and i != 'choices_num':
                    '''
                        x轴(-0.8, 0.8)，一行最多6个，min(6, self.opt_num) - 1得到分割的数目
                        y轴(-0.8, 0.8)，一列最多12个，k // 6 * 7用于超过6个选项时将选项偏移到第二行，7是考虑了选择按钮
                    '''
                    self.texts[i] = TextStim(win, text=opt[i], height=0.05, pos=(1.6 / (min(6, self.opt_num) - 1) * (k % 6) - 0.8, 0.8 - 0.13 * (k // 6 * 7 + p)), 
                                                units='norm', color=(0, 0, 0), colorSpace='rgb255', name='text'+i)
                    self.covers[i] = Cover(win, pos=(1.6 / (min(6, self.opt_num) - 1) * (k % 6) - 0.8, 0.8 - 0.13 * (k // 6 * 7 + p)), name=i, 
                                                detail_file=self.detail_file, sub_id=self.sub_id, test_id=self.test_id)
                    p += 1
            k += 1

        self.buttons = []
        k = 0
        for i in self.opts:
            self.buttons.append(Button(win, pos=(1.6 / (min(6, self.opt_num) - 1) * (k % 6) - 0.8, 0.8 - 0.13 * (len(i.keys()) - 2 + k // 6 * 7)), 
                                        height=0.05, width=0.1, name=i['choices_name']))
            k += 1
        
    def run(self):
        done = False
        self.result = ''
        while not done:
            self.description.draw()
            for a in self.texts.values():
                a.draw()
            for b in self.buttons:
                b.process()
                b.draw()
                if b.state == b.END:
                    self.choice = b.name
                    done = True
            for c in self.covers.values():
                c.process()
                c.draw()
            self.win.flip()
        
    def save(self):
        self.sum_file.write(str(self.sub_id) + ',')
        self.sum_file.write(str(self.test_file.split('.')[0]) + ',')
        self.sum_file.write(str(self.choice) + ',')
        sum_write = []
        for i in self.keys:
            sum_write.append(str(self.covers[i].time))
        self.sum_file.write(','.join(sum_write))
        self.sum_file.write('\n')


class Rating(object):
    def __init__(self, win, description, scale_text, acceptPreText, rating_file):
        self.win = win
        self.description = description
        self.scale_text = scale_text
        self.acceptPreText = acceptPreText
        self.rating_file = rating_file

        self.rating_text = TextStim(win, text=description, height=0.1, pos=(0, 0.5), units='norm', color=(0, 0, 0), colorSpace='rgb255')
        self.ratingScale = RatingScale(win, scale=scale_text, acceptPreText=acceptPreText, pos=(0, -0.3))

    def run(self):
        while self.ratingScale.noResponse:
            self.rating_text.draw()
            self.ratingScale.draw()
            self.win.flip()

    def save(self):
        self.rating_file.write('Rating: ' + str(self.ratingScale.getRating()) + '\n')
        self.rating_file.write('Decision Time: ' + str(self.ratingScale.getRT()) + '\n')
        choiceHistory = self.ratingScale.getHistory()
        self.rating_file.write('Choice History:\n(choice\ttime)\n')
        for i in choiceHistory:
            self.rating_file.write(str(i[0]) + '\t' + str(i[1]) + '\n')


def getSubjectID():
    """
    返回被试者id(int)
    """
    myDlg = gui.Dlg(title='受试者信息')
    myDlg.addField(label='被试者ID:')
    myDlg.addField('屏幕宽度:', initial='1920')
    myDlg.addField('屏幕高度:', initial='1080')
    myDlg.show()

    if myDlg.OK:
        thisInfo = myDlg.data
    else:
        exit(0)
        
    return (int(thisInfo[0]), int(thisInfo[1]), int(thisInfo[2]))
    

sub_id, scr_width, scr_height = getSubjectID()
sum_file = open(os.path.join('results', str(sub_id) + '_sum' + '.csv'), 'w')
detail_file = open(os.path.join('results', str(sub_id) + '_detail' + '.csv'), 'w')
rating_file = open(os.path.join('results', str(sub_id) + '_rating' + '.txt'), 'w')
win = Window(size=(scr_width, scr_height), units='norm', fullscr=True)

# tests
tests = sorted(os.listdir('tests'))
for test_file in tests:
    trial = Trial(win=win, test_file=test_file, sum_file=sum_file, detail_file=detail_file, sub_id=sub_id)
    trial.run()
    trial.save()

# 评分
rating = Rating(win=win, description='请对决策的自信度进行评价\n(选择后请点击标尺下方数字按钮)', 
                        scale_text='1=非常不自信..........7=非常自信', 
                        acceptPreText='请在标尺上点击', 
                        rating_file=rating_file)
rating.run()
rating.save()

sum_file.close()
detail_file.close()
rating_file.close()
win.close()