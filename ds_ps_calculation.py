import csv
import os

# calculate total choices in each test
test_choices_num = {}
tests = sorted(os.listdir('tests'))
for test_file in tests:
    file_handle = open(os.path.join('tests', test_file), 'r', encoding='utf-8')
    attributes_num = int(file_handle.readline())
    attributes_name = file_handle.readline().rstrip('\n').split(',')
    choices_num = int(file_handle.readline())
    test_choices_num[test_file.split('.')[0]] = choices_num * attributes_num
    file_handle.close()

# calculate DS and PS for each sub_id in each test
ds_result_handle = open('ds_results.csv', 'w+')
ds_result_handle.write(','.join(('sub_id', 'test_id', 'DS')))
ds_result_handle.write('\n')

ps_result_handle = open('ps_results.csv', 'w+')
ps_result_handle.write(','.join(('sub_id', 'test_id', 'PS')))
ps_result_handle.write('\n')

detail_files = sorted(os.listdir('results'))
for detail_file in detail_files:
    if detail_file.endswith('detail.csv'):
        sub_id = detail_file.split('_')[0]
        detail_file_handle = open(os.path.join('results', detail_file))
        detail_file_reader = csv.reader(detail_file_handle)
        search_seq = list(detail_file_reader)
        
        # calculate DS
        search_list = {}
        for i in range(len(search_seq)):
            if i == 0:
                continue
            test_id = search_seq[i][1]
            search_list.setdefault(test_id, [])
            if search_seq[i][2] not in search_list[test_id]:
                search_list[test_id].append(search_seq[i][2])
        for i in search_list.keys():
            ds = len(search_list[i]) / test_choices_num[i]
            ds_result_handle.write(','.join((str(sub_id), str(i), str(ds))))
            ds_result_handle.write('\n')
        
        # calculate PS
        between_dim = {}
        inner_dim = {}
        for i in range(len(search_seq)):
            if i == 0 or i == 1:
                continue
                
            test_id = search_seq[i][1]
            between_dim.setdefault(test_id, 0)
            inner_dim.setdefault(test_id, 0)

            choice_name_now, attributes_name_now = search_seq[i][2].split('_')
            choice_name_pre, attributes_name_pre = search_seq[i-1][2].split('_')
            
            if attributes_name_now != attributes_name_pre and choice_name_now == choice_name_pre:
                between_dim[test_id] += 1
            if attributes_name_now == attributes_name_pre and choice_name_now != choice_name_pre:
                inner_dim[test_id] += 1
        for i in between_dim.keys():
            ps = (between_dim[i] - inner_dim[i]) / (between_dim[i] + inner_dim[i])
            ps_result_handle.write(','.join((str(sub_id), str(i), str(ps))))
            ps_result_handle.write('\n')

        detail_file_handle.close()
    
ds_result_handle.close()
ps_result_handle.close()