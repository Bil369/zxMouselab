# zxMouselab

![build](https://img.shields.io/badge/build-passing-success)
![build](https://img.shields.io/badge/python-v3.7-ff68b4)
![build](https://img.shields.io/badge/psychopy-2020.2.4.post1-orange)
![build](https://img.shields.io/badge/license-GPL-blue)

本仓库是使用Psychopy实现的类似Mouselab的决策过程追踪工具zxMouselab，可以用于完成信息板(Information Display Board, IDB)实验。

![示例](example1.png)

支持评价量表：
![评价量表](example2.png)

由于本人水平有限，该工具的实现还有诸多不够完善的地方，可以在Issues中提出，我也会继续改进。 

:yellow_heart: :blue_heart: :purple_heart: :heart: :green_heart: I'm not majoring in psychology. I'm majoring in computer science and technology. This repository is written for my sister :girl: , who is majoring in psychology.

## 目录

- [zxMouselab](#zxMouselab)
  - [目录](#%e7%9b%ae%e5%bd%95)
  - [特性](#特性)
  - [安装](#%e5%ae%89%e8%a3%85)
  - [使用](#%e4%bd%bf%e7%94%a8)
    - [设置信息板](#设置信息板)
    - [运行](#运行)
    - [结果](#结果)
  - [License](#license)

## 安装

需要安装以下依赖：
- Python >= 3.7
- PsychoPy >= 2020.2.4.post1

## 使用

### 设置信息板
tests目录下存放不同的信息板，一个信息板一个文件。注意所有存放在tests目录下的文件都会被受试者使用。

每个文件的格式为：
![test_example](test_example.png)

信息板支持最多6个属性，24个选项，如果选项数多余6个，请开启大选择集支持：

编辑Mouselab.py文件开始处：
```python
####################################################
big_support = True  # 大选择集：True 小选择集：False
####################################################
```

### 运行

在PsychoPy中或在Python环境中（确保安装了PsychoPy依赖）运行zxMouselab.py即可。

### 结果

输出结果位于results文件夹下：
- sub_id_detail.csv记录了被试者所有查看记录和对应时间(s)
- sub_id_sum.csv记录了被试者的最终选择结果、决策时间(s)以及查看每个格子的总时间(s)
- sub_id_rating.txt记录了被试者的所有评分记录、决策时间(s)、选择评分对应的时间点

支持计算搜索深度(DS)与搜索模式(PS)：   

运行ds_ps_calculation.py，会对results下的所有被试者记录进行计算，搜索深度保存为ds_results.csv，搜索模式保存为ps_results.csv

## License
[GPL](https://github.com/Bil369/zxMouselab/blob/master/LICENSE) &copy; [Bil369](https://github.com/Bil369)