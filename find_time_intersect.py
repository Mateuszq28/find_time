from datetime import datetime
import os


def text2date_scope(person_time_text):
    date_list = []
    person_time_list = person_time_text.split("\n")
    for l in person_time_list:
        time_in = l[0:14]
        time_out = l[0:9] + l[15:20]
        date_time_obj_in = datetime.strptime(time_in, '%d.%m.%y %H:%M')
        date_time_obj_out = datetime.strptime(time_out, '%d.%m.%y %H:%M')
        # to samo inaczej
        # time_in = l[0:7] + "20" + l[7:9] + l[9:14]
        # time_out = l[0:7] + "20" + l[7:9] + l[15:20]
        # date_time_obj_in = datetime.strptime(time_in, '%d.%m.%Y %H:%M')
        # date_time_obj_out = datetime.strptime(time_out, '%d.%m.%Y %H:%M')
        date_list.append([date_time_obj_in, date_time_obj_out])
    return sorted(date_list)        


def person_time_list2person_scope_list(person_time_list):
    person_scope_list = []
    for p in person_time_list:
        p_scope = text2date_scope(p)
        person_scope_list.append(p_scope)
    return person_scope_list


def date2timestamp(date):
    return int(datetime.timestamp(date))


def timestamp2datetime(timestamp):
    return datetime.fromtimestamp(timestamp)


def person_scope_list2person_set_list(person_scope_list):
    person_set_list = []
    for p in person_scope_list:
        one_preson_date_set = []
        for d in p:
            date1 = date2timestamp(d[0])
            date2 = date2timestamp(d[1])
            drange = range(date1, date2+60, 60)
            one_preson_date_set += drange
        person_set_list.append(one_preson_date_set)
    return person_set_list


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def intersection2(lst1, lst2):
    return list(set(lst1) & set(lst2))


def one_list2date_scope_list(one_list):
    l = len(one_list)
    start_idx = 0
    end_idx = 0
    date_scope_list = []
    for i in range(1,l):
        one_list.sort()
        if one_list[i] - one_list[i-1] > 60:
            end_idx = i-1
            date1 = timestamp2datetime(one_list[start_idx])
            date2 = timestamp2datetime(one_list[end_idx])
            date_scope_list.append([date1, date2])
            start_idx = i
            end_idx = i
    end_idx = l-1
    date1 = timestamp2datetime(one_list[start_idx])
    date2 = timestamp2datetime(one_list[end_idx])
    date_scope_list.append([date1, date2])
    return date_scope_list


# na wejściu lista czasów wszystkich osób
def find_common_time(person_time_list):
    if len(person_time_list) == 0:
        return []
    elif len(person_time_list) == 1:
        return text2date_scope(person_time_list[0])
    else:
        person_scope_list = person_time_list2person_scope_list(person_time_list)
        person_set_list = person_scope_list2person_set_list(person_scope_list)
        common = person_set_list[0]
        for p in person_set_list[1:]:
            common = intersection2(common, p)
        date_scope_list = one_list2date_scope_list(common)
        return date_scope_list
        

def scope2text(common):
    text = ""
    for c in common:
        text += c[0].strftime("%d.%m.%y %H:%M")
        text += c[1].strftime("-%H:%M\n")
    return text


def delete_prefix(person_time_list_with_prefix_line):
    new_list = []
    for person_string in person_time_list_with_prefix_line:
        person_lines = person_string.split("\n")
        new_list.append("\n".join(person_lines[1:]))
    return new_list


def main():
    # main
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, "dates.txt")
    with open(path, 'r') as f:
        date_text = f.read()

    person_time_list_with_prefix_line = date_text.split("\n\n")
    person_time_list = delete_prefix(person_time_list_with_prefix_line)
    common = sorted(find_common_time(person_time_list))
    common_text = scope2text(common)
    print(common_text)
    path = os.path.join(dirname, "result.txt")
    with open(path, 'w') as f:
        f.write(common_text)

main()