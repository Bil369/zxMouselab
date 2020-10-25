import os
import random

from psychopy import clock, event, gui
from psychopy.visual import ImageStim, RatingScale, Rect, TextStim, Window

####################################################
big_support = True  # 大选择集：True 小选择集：False
####################################################

class Button():
    START, END = range(2)
    def __init__(self, win, pos, width, height, name, text='选择'):
        self.name = name
        self.rect = Rect(win, height=height, width=width, units='norm', pos=pos)
        self.mouse = event.Mouse(win=win)
        self.caption = TextStim(win, text=text, height=height - 0.01 , pos=pos, units='norm', color=(0, 0, 0), colorSpace='rgb255')
        self.state = self.START
        
    def draw(self):
        x, y = self.mouse.getPos()
        if self.rect.contains(x, y, units='norm'):
            self.rect.setLineColor(color=(0, 0, 204), colorSpace='rgb255')
            self.caption.setColor(color=(0, 0, 204), colorSpace='rgb255')
        else:
            self.rect.setLineColor(color=(0, 0, 0), colorSpace='rgb255')
            self.caption.setColor(color=(0, 0, 0), colorSpace='rgb255')
        self.rect.draw()
        self.caption.draw()
    
    def process(self):
        x, y = self.mouse.getPos()
        if self.rect.contains(x, y, units='norm') and self.mouse.getPressed()[0] == 1:
            self.state = self.END


class SimpleCover():
    '''
        This class is a simplified version of class Cover for the practice mode.
    '''
    COVER, SHOW = range(2)
    def __init__(self, win, pos, name, width=0.15, height=0.1, color=(178, 178, 178)):
        self.rect = Rect(win, height=height, width=width, units='norm', pos=pos)
        self.rect.setFillColor(color=color, colorSpace='rgb255')
        self.rect.setLineColor(color=color, colorSpace='rgb255')
        self.mouse = event.Mouse(win=win)
        self.state = self.COVER
        
    def draw(self):
        if self.state == self.COVER:
            self.rect.draw()
        elif self.state == self.SHOW:
            pass
    
    def process(self):
        x, y = self.mouse.getPos()
        # if need to click to see the information, uncomment the following line and comment the line after the following line
        if self.rect.contains(x, y, units='norm') and self.mouse.getPressed()[0] == 1:
        # if self.rect.contains(x, y, units='norm'):
            self.state = self.SHOW
        elif not self.rect.contains(x, y, units='norm'):
            self.state = self.COVER


class Cover():
    COVER, SHOW = range(2)
    def __init__(self, win, pos, name, detail_file, sub_id, test_id, width=0.15, height=0.1, color=(178, 178, 178)):
        self.name = name
        self.rect = Rect(win, height=height, width=width, units='norm', pos=pos)
        self.rect.setFillColor(color=color, colorSpace='rgb255')
        self.rect.setLineColor(color=color, colorSpace='rgb255')
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
        elif self.state == self.SHOW:
            pass
    
    def process(self):
        x, y = self.mouse.getPos()
        # if need to click to see the information, uncomment the following line and comment the line after the following line
        if self.rect.contains(x, y, units='norm') and self.mouse.getPressed()[0] == 1:
        # if self.rect.contains(x, y, units='norm'):
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
        

class Trial():
    def __init__(self, win, test_file, sum_file, detail_file, sub_id, big_support=False):
        self.win = win
        self.test_file = test_file
        self.sum_file = sum_file
        self.detail_file = detail_file
        self.sub_id = sub_id
        self.test_id = self.test_file.split('.')[0]
        self.big_support = big_support
        self.clk = clock.Clock()
        self.start_time = 0
        self.first_look = True

        # 处理文件输入
        file_handle = open(os.path.join('tests', test_file), 'r', encoding='utf-8')
        self.attributes_num = int(file_handle.readline())
        self.attributes_name = file_handle.readline().rstrip('\n').split(',')
        self.choices_num = int(file_handle.readline())
        self.choices = []
        for i in range(self.choices_num):
            choice = {}
            choice['choice_name'] = file_handle.readline().rstrip('\n')
            choice['attributes'] = []
            for j in range(self.attributes_num):
                attribute_content = file_handle.readline().rstrip('\n')
                choice['attributes'].append(attribute_content)
            self.choices.append(choice)
        file_handle.close()

        # 小选择集随机取6个
        if not big_support:
            self.choices_num = 6
            random.shuffle(self.choices)
            self.choices = self.choices[:6]

        # 选项顺序随机打乱
        random.shuffle(self.choices)

        # 写入表头
        sum_write = ['sub_id', 'test_id', 'choice', 'decision_time']
        for i in self.choices:
            for j in self.attributes_name:
                sum_write.append(i['choice_name'] + '_' + j)
        sum_file.write(','.join(sum_write))
        sum_file.write('\n')

        detail_write = ('sub_id', 'test_id', 'action', 'time')
        detail_file.write(','.join(detail_write))
        detail_file.write('\n')

        '''
            if big_support:
                x轴(-0.8, 0.9)，-0.95留给属性
                y轴(-0.9, 0.9)，0.9留给选项标签
            else:
                x轴(-0.7, 0.8)，-0.85留给属性
                y轴(-0.5, 0.5)，0.5留给选项标签
        '''

        # 生成labels
        self.labels = []
        for i in range(self.choices_num):
            if self.big_support:
                self.labels.append(TextStim(win, text=self.choices[i]['choice_name'], height=0.04, 
                                            pos=(1.7 / (min(12, self.choices_num) - 1) * (i % 12) - 0.8, 0.9 - 0.12 * (i // 12 * 8)), 
                                            color=(0, 0, 0), colorSpace='rgb255', name='label'+self.choices[i]['choice_name']))
            else:
                self.labels.append(TextStim(win, text=self.choices[i]['choice_name'], height=0.04, 
                                            pos=(1.5 / (min(6, self.choices_num) - 1) * (i % 6) - 0.7, 0.5), 
                                            color=(0, 0, 0), colorSpace='rgb255', name='label'+self.choices[i]['choice_name']))

        # 生成hints
        self.hints = []
        for i in range(self.attributes_num):
            if big_support:
                self.hints.append(TextStim(win, text=self.attributes_name[i], height=0.04, pos=(-0.95, 0.9 - 0.12 * (i+1)), units='norm', 
                                            color=(0, 0, 0), colorSpace='rgb255', name='text'+self.attributes_name[i]))
                self.hints.append(TextStim(win, text=self.attributes_name[i], height=0.04, pos=(-0.95, 0.9 - 0.12 * (i+1+7+1)), units='norm', 
                                            color=(0, 0, 0), colorSpace='rgb255', name='text'+self.attributes_name[i]))
            else:
                self.hints.append(TextStim(win, text=self.attributes_name[i], height=0.04, pos=(-0.85, 0.5 - 0.12 * (i+1)), units='norm', 
                                            color=(0, 0, 0), colorSpace='rgb255', name='text'+self.attributes_name[i]))

        # 生成texts和covers
        self.texts = {}
        self.covers = {}
        for i in range(self.choices_num):
            choice_name = self.choices[i]['choice_name']
            for j in range(self.attributes_num):
                attribute_name = self.attributes_name[j]
                attribute_content = self.choices[i]['attributes'][j]
                if self.big_support:
                    self.texts[choice_name+'_'+attribute_name] = TextStim(win, text=attribute_content, height=0.04, 
                                                                    pos=(1.7 / (min(12, self.choices_num) - 1) * (i % 12) - 0.8, 0.9 - 0.12 * (i // 12 * 8 + j + 1)),
                                                                    units='norm', color=(0, 0, 0), colorSpace='rgb255', name='text'+choice_name+attribute_name)
                    self.covers[choice_name+'_'+attribute_name] = Cover(win, pos=(1.7 / (min(12, self.choices_num) - 1) * (i % 12) - 0.8, 0.9 - 0.12 * (i // 12 * 8 + j + 1)), 
                                                                    name=choice_name+'_'+attribute_name, detail_file=self.detail_file, width=0.12, height=0.08,
                                                                    sub_id=self.sub_id, test_id=self.test_id)
                else:
                    self.texts[choice_name+'_'+attribute_name] = TextStim(win, text=attribute_content, height=0.04, 
                                                                    pos=(1.5 / (min(6, self.choices_num) - 1) * (i % 6) - 0.7, 0.5 - 0.12 * (j+1)),
                                                                    units='norm', color=(0, 0, 0), colorSpace='rgb255', name='text'+choice_name+attribute_name)
                    self.covers[choice_name+'_'+attribute_name] = Cover(win, pos=(1.5 / (min(6, self.choices_num) - 1) * (i % 6) - 0.7, 0.5 - 0.12 * (j+1)), 
                                                                    name=choice_name+'_'+attribute_name, detail_file=self.detail_file, width=0.12, height=0.08,
                                                                    sub_id=self.sub_id, test_id=self.test_id)


        self.buttons = []
        for i in range(self.choices_num):
            if self.big_support:
                self.buttons.append(Button(win, pos=(1.7 / (min(12, self.choices_num) - 1) * (i % 12) - 0.8, 0.9 - 0.12 * (i // 12 * 8 + self.attributes_num + 1)), 
                                            height=0.05, width=0.1, name=self.choices[i]['choice_name']))
            else:
                self.buttons.append(Button(win, pos=(1.5 / (min(6, self.choices_num) - 1) * (i % 6) - 0.7, 0.5 - 0.12 * (self.attributes_num+1)), 
                                            height=0.05, width=0.1, name=self.choices[i]['choice_name']))
        
    def run(self):
        done = False
        self.result = ''
        while not done:
            if self.first_look:
                self.start_time = self.clk.getTime()
                self.first_look = False
            # ensure that texts draw before covers otherwise they can't be coverd.
            for t in self.texts.values():
                t.draw()
            for b in self.buttons:
                b.process()
                b.draw()
                if b.state == b.END:
                    self.result = b.name
                    done = True
            for c in self.covers.values():
                c.process()
                c.draw()
            for h in self.hints:
                h.draw()
            for l in self.labels:
                l.draw()
            self.win.flip()
        
    def save(self):
        self.sum_file.write(str(self.sub_id) + ',')
        self.sum_file.write(str(self.test_id) + ',')
        self.sum_file.write(str(self.result) + ',')
        self.sum_file.write(str(self.clk.getTime() - self.start_time) + ',')
        sum_write = []
        for i in self.choices:
            for j in self.attributes_name:
                sum_write.append(str(self.covers[i['choice_name'] + '_' + j].time))
        self.sum_file.write(','.join(sum_write))
        self.sum_file.write('\n')


class Rating():
    def __init__(self, win, description, labels, rating_file):
        self.win = win
        self.rating_file = rating_file
        self.description = TextStim(win, text=description, height=0.05, pos=(0, 0.5), units='norm', color=(0, 0, 0), colorSpace='rgb255')
        if len(labels) == 7:
            self.rating_scale = RatingScale(win, scale=None, labels=labels, tickMarks=[1, 2, 3, 4, 5, 6, 7], pos=(0, 0), 
                                            stretch=3, textSize=0.8, textColor='Black', lineColor='Black', showValue=False, showAccept=False)
        else:
            self.rating_scale = RatingScale(win, scale=None, labels=labels, pos=(0, 0), stretch=3, textSize=0.8, textColor='Black', 
                                            lineColor='Black', showValue=False, showAccept=False)
        self.button = Button(win, (0, -0.5), width=0.1, height=0.05, name='button_rating', text='确认')

    def run(self):
        while self.button.state != self.button.END:
            self.description.draw()
            self.rating_scale.draw()
            self.button.process()
            self.button.draw()
            self.win.flip()

    def save(self):
        self.rating_file.write('Rating: ' + str(self.rating_scale.getRating()) + '\n')
        self.rating_file.write('Decision Time: ' + str(self.rating_scale.getRT()) + '\n')
        choice_history = self.rating_scale.getHistory()
        self.rating_file.write('Choice History:\n(choice\ttime)\n')
        for i in choice_history:
            self.rating_file.write(str(i[0]) + '\t' + str(i[1]) + '\n')
        self.rating_file.write('\n')


class ShowAndConfirm():
    def __init__(self, win, image, button_text):
        self.win = win
        self.show = ImageStim(win, image=image, units='norm')
        self.confirm_button = Button(win, (0, -0.5), width=0.1, height=0.05, name='confirm_button', text=button_text)

    def run(self):
        while self.confirm_button.state != self.confirm_button.END:
            self.show.draw()
            self.confirm_button.process()
            self.confirm_button.draw()
            self.win.flip()


def get_sub_id():
    '''
    返回被试者id: int
    '''
    my_Dlg = gui.Dlg(title='受试者信息')
    my_Dlg.addField(label='被试者ID:')
    my_Dlg.show()

    if my_Dlg.OK:
        sub_id = int(my_Dlg.data[0])
    else:
        exit(0)
        
    return sub_id
    

sub_id = get_sub_id()
scr_width = 1920
scr_height = 1080
sum_file = open(os.path.join('results', str(sub_id) + '_sum' + '.csv'), 'w')
detail_file = open(os.path.join('results', str(sub_id) + '_detail' + '.csv'), 'w')
rating_file = open(os.path.join('results', str(sub_id) + '_rating' + '.txt'), 'w')
win = Window(size=(scr_width, scr_height), units='norm', fullscr=True, color=(255, 255, 255), colorSpace='rgb255')

# introduction 1
intro1 = ShowAndConfirm(win, 'imgs/intro1.png', '确认')
intro1.run()

# introduction 2
intro2 = ShowAndConfirm(win, 'imgs/intro2.png', '确认')
intro2.run()

# practice
practice_title = TextStim(win, text='练习', height=0.1, pos=(0, 0.5), units='norm', color=(0, 0, 0), colorSpace='rgb255')
practice = ImageStim(win, image='imgs/practice.png', pos=(0, 0.2), units='norm')
practice_hint = TextStim(win, text='价格', height=0.05, pos=(-0.15, 0), units='norm', color=(0, 0, 0), colorSpace='rgb255')
practice_text = TextStim(win, text='￥9999', height=0.05, pos=(0, 0), units='norm', color=(0, 0, 0), colorSpace='rgb255')
practice_cover = SimpleCover(win, pos=(0, 0), name='价格')
button_practice = Button(win, (0, -0.5), width=0.1, height=0.05, name='button_practice', text='正式开始')
while button_practice.state != button_practice.END:
    practice_title.draw()
    practice.draw()
    practice_hint.draw()
    practice_text.draw()
    practice_cover.process()
    practice_cover.draw()
    button_practice.process()
    button_practice.draw()
    win.flip()

# tests
tests = sorted(os.listdir('tests'))
for test_file in tests:
    trial = Trial(win=win, test_file=test_file, sum_file=sum_file, detail_file=detail_file, sub_id=sub_id, big_support=big_support)
    trial.run()
    trial.save()

# thanks
thanks = ShowAndConfirm(win, 'imgs/thanks.png', '确认')
thanks.run()

# rating1
rating1 = Rating(win=win, description='对于最后的选择，您是否感到满意？', 
                labels=('1\n非常不满意', '2\n不满意', '3\n有点不满意', '4\n一般', '5\n有点满意', '6\n满意', '7\n非常满意'), 
                rating_file=rating_file)
rating1.run()
rating1.save()

# rating2
rating2 = Rating(win=win, description='对于最后的选择，您是否感到后悔？', 
                labels=('1\n非常不后悔', '2\n不后悔', '3\n有点不后悔', '4\n一般', '5\n有点后悔', '6\n后悔', '7\n非常后悔'), 
                rating_file=rating_file)
rating2.run()
rating2.save()

# rating3
rating3 = Rating(win=win, description='您刚选购的相机是您认为最好的选择吗，对此您的自信程度如何？', 
                labels=('1\n非常没信心', '2\n没信心', '3\n有点没信心', '4\n一般', '5\n有点信心', '6\n有信心', '7\n非常有信心'), 
                rating_file=rating_file)
rating3.run()
rating3.save()

# rating4
rating4 = Rating(win=win, description='您完成该决策任务的努力程度是多少？', 
                labels=('1\n非常轻松', '4\n中度努力', '7\n非常努力'), 
                rating_file=rating_file)
rating4.run()
rating4.save()

# rating5
rating5 = Rating(win=win, description='您认为这次选购相机的选择难度如何', 
                labels=('1\n非常简单', '2\n比较简单', '3\n有点简单', '4\n一般', '5\n有点难', '6\n比较难', '7\n非常难'), 
                rating_file=rating_file)
rating5.run()
rating5.save()

# rating6
rating6 = Rating(win=win, description='您认为提供给您的选项数量__________', 
                labels=('1\n非常少', '2\n比较少', '3\n有点少', '4\n一般', '5\n有点多', '6\n比较多', '7\n非常多'), 
                rating_file=rating_file)
rating6.run()
rating6.save()

# rating7
rating7 = Rating(win=win, description='假设提供给您一个“暂不选择”的选项，您选择“暂不选择”的倾向是多少？ ', 
                labels=('1\n非常少', '2\n比较少', '3\n有点少', '4\n一般', '5\n有点多', '6\n比较多', '7\n非常多'), 
                rating_file=rating_file)
rating7.run()
rating7.save()

# ending
ending = ShowAndConfirm(win, 'imgs/ending.png', '退出')
ending.run()

sum_file.close()
detail_file.close()
rating_file.close()
win.close()