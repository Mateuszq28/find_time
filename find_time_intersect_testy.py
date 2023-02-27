import numpy as np
from datetime import datetime, timedelta

print("start array")
a = np.array((1,3))
print("a", a)
b = np.array((2,5))
print("b", b)
inter = np.intersect1d(a,b)
print("np.concatenate(a,b)", np.concatenate((a,b)))
print("np.intersect1d", inter)


print("start arange")
a = np.arange(1,4)
print("a", a)
b = np.arange(2,6)
print("b", b)
inter = np.intersect1d(a,b)
print("np.concatenate(a,b)", np.concatenate((a,b)))
print("np.intersect1d", inter)


print("start array(range)")
a = np.array(range(1,4))
print("a", a)
b = np.array(range(2,6))
print("b", b)
inter = np.intersect1d(a,b)
print("np.concatenate(a,b)", np.concatenate((a,b)))
print("np.intersect1d", inter)


print("start linspace")
a = np.linspace(1,3, 3-1+1)
print("a", a)
b = np.linspace(2,5, 5-2+1)
print("b", b)
inter = np.intersect1d(a,b)
print("np.concatenate(a,b)", np.concatenate((a,b)))
print("np.intersect1d", inter)


def date2timestamp(date):
    return int(datetime.timestamp(date))

def timestamp2datetime(timestamp):
    return datetime.fromtimestamp(timestamp)

print("start array(range(datetime))")
a1 = date2timestamp(datetime.today())
a2 = date2timestamp(datetime.today() + timedelta(days=2))
a = np.array(range(a1, a2))
print("a", a)
b1 = date2timestamp(datetime.today() + timedelta(days=1))
b2 = date2timestamp(datetime.today() + timedelta(days=5))
b = np.array(range(b1, b2))
print("b", b)
inter = np.intersect1d(a,b)
print("np.concatenate(a,b)", np.concatenate((a,b)))
print("np.intersect1d", inter)
inter_datetime = np.array([timestamp2datetime(x) for x in inter])
print("np.intersect1d datetime", inter_datetime)