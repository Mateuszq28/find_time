from datetime import datetime
import os


def text2date_scope(person_time_text):
    date_list = []
    person_time_list = person_time_text.split("\n")
    for l in person_time_list:
        time_in = l[0:16]
        time_out = l[0:11] + l[17:22]
        date_time_obj_in = datetime.strptime(time_in, '%d.%m.%Y %H:%M')
        date_time_obj_out = datetime.strptime(time_out, '%d.%m.%Y %H:%M')
        date_list.append([date_time_obj_in, date_time_obj_out])
    return sorted(date_list)


# n - pojedynczy rekord z common (z wszystkich wspólnych przedziałów)
# n - pojedynczy rekord przedziału jednej osoby
# zwraca wspólny przedział lub None
def n_in_common_day(com_day, n):
    n1 = com_day
    n2 = n
    if n1[1].time() < n2[0].time():
        # pierwszy przed drugim, nie nakładają się
        return None
    if n2[1].time() < n1[0].time():
        # drugi przed pierwszym, nie nakładają się
        return None
    if n1[0].time() == n2[0].time() and n1[1].time() == n2[1].time():
        # przedziały równe
        return n1
    if n1[0].time() < n2[0].time() and n1[1].time() > n2[0].time() and n1[1].time() < n2[1].time():
        # drugi przed pierwszym, nakładają się
        return [n2[0], n1[1]]
    if n2[0].time() < n1[0].time() and n2[1].time() > n1[0].time() and n2[1].time() < n1[1].time():
        # pierwszy przed drugim, nakładają się
        return [n1[0], n2[1]]
    if n1[0].time() > n2[0].time() and n1[1].time() < n2[1].time():
        # pierwszy zawiera się w drugim
        return n1
    if n2[0].time() > n1[0].time() and n2[1].time() < n1[1].time():
        # drugi zawiera się w pierwszym
        return n2


# n - pojedynczy rekord przedziału jednej osoby
# common - wszystkie wspólnie odselekcjonowane bramką AND przedziały (rekordy)
# zwraca nowe common
def n_in_common(n, common):
    if n < common[0] or n > common[-1]:
        return []
    else:
        # odsiewamy rekordy, patrząc tylko na te z tymi samymi dniami
        day1 = n[0].date()
        common_days = [c for c in common if c[0].date() == day1]
        if len(common_days) < 1:
            return []
        else:
            new_common_days = []
            for com_day in common_days:
                n_cut = n_in_common_day(com_day, n)
                if n_cut is not None:
                    new_common_days.append(n_cut)
            return new_common_days
                

# na wejściu lista czasów wszystkich osób
def find_common_time(person_time_list):
    if len(person_time_list) == 0:
        return ""
    elif len(person_time_list) == 1:
        return person_time_list[0]
    else:
        common = text2date_scope(person_time_list[0])
        for p in person_time_list[1:]:
            new_scope = text2date_scope(p)
            new_common = []
            for n in new_scope:
                n_cut = n_in_common(n, common)
                if len(n_cut) > 0:
                    for n_c in n_cut:
                        new_common.append(n_c)
            # podmnieniamy, bo bramka AND
            # common.clear()
            common = new_common
    return common
        

def scope2text(common):
    text = ""
    for c in common:
        text += c[0].strftime("%d.%m.%y %H:%M")
        text += c[1].strftime("-%H:%M\n")
    return text


def main():
    # main
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, "dates.txt")
    with open(path, 'r') as f:
        date_text = f.read()

    person_time_list = date_text.split("\n\n")
    common = find_common_time(person_time_list)
    common_text = scope2text(common)
    print(common_text)
    path = os.path.join(dirname, "result.txt")
    with open(path, 'w') as f:
        f.write(common_text)


main()