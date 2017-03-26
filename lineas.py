# -*- coding: utf-8 -*-
# python 2.7, python3.5
import csv

reader = list(csv.reader(open('data/moviedaily.csv', 'r'), delimiter='\t'))

def accumulated_views(reader, title, days):
    accumulated_views = {}
    accumulated_views[0] = 0
    count = 0
    for line in reader:
        if count == 0:
            count = count + 1
            continue
        if line[1] == title and count <= days:
            if(count == 1):
                accumulated_views[count] = int(line[3])
            else:
                day = int(line[2])
                accumulated_views[day] = accumulated_views[day - 1] + int(line[3])
            count = count + 1

    return accumulated_views

ABM_acc_views = accumulated_views(reader, 'A Beautiful Mind', 70)
BAT_acc_views = accumulated_views(reader, 'Batman', 70)
GLAD_acc_views = accumulated_views(reader, 'Gladiator', 70)
TNC_acc_views = accumulated_views(reader, 'Titanic', 70)

# TESTING
# for k,v in ABM_acc_views.items():
#     print(k,v)

# # PREPROCESSING
count = 0

ABM_DAILY_PER_THEATER = {}
BAT_DAILY_PER_THEATER = {}
GLAD_DAILY_PER_THEATER = {}
TNC_DAILY_PER_THEATER = {}

for line in reader:
    if count == 0:
        count = count + 1
        continue
    if line[1] == 'A Beautiful Mind' and int(line[2]) <= 70:
        day = int(line[2])
        ABM_DAILY_PER_THEATER[day] = line[3]
    elif line[1] == 'Batman' and int(line[2]) <= 70:
        day = int(line[2])
        BAT_DAILY_PER_THEATER[day] = line[3]
    elif line[1] == 'Gladiator' and int(line[2]) <= 70:
        day = int(line[2])
        GLAD_DAILY_PER_THEATER[day] = line[3]
    elif line[1] == 'Titanic' and int(line[2]) <= 70:
        day = int(line[2])
        TNC_DAILY_PER_THEATER[day] = line[3]
    count = count + 1


# # MATPLOTLIB
import matplotlib.pyplot as plt

# # DAILY_PER_THEATER
# plt.plot(list(ABM_DAILY_PER_THEATER.keys()), list(ABM_DAILY_PER_THEATER.values()), label=u'Facturación diarias de "A Beautiful Mind"')
# plt.plot(list(BAT_DAILY_PER_THEATER.keys()), list(BAT_DAILY_PER_THEATER.values()), label=u'Facturación diarias de "Batman')
# plt.plot(list(GLAD_DAILY_PER_THEATER.keys()), list(GLAD_DAILY_PER_THEATER.values()), label=u'Facturación diarias de "Gladiator"')
# plt.plot(list(TNC_DAILY_PER_THEATER.keys()), list(TNC_DAILY_PER_THEATER.values()), label=u'Facturación diarias de "Titanic"')
# plt.xlabel('days')
# plt.ylabel('Daily per theater receipts($)')
# plt.legend(loc=1)
# plt.show()

# # ACCUMULATED_DAILY
plt.plot(list(TNC_acc_views.keys()), list(TNC_acc_views.values()), label=u'Facturación de "Titanic" en primeras 10 semanas')
plt.plot(list(BAT_acc_views.keys()), list(BAT_acc_views.values()), label=u'Facturación de "Batman" en primeras 10 semanas')
plt.plot(list(ABM_acc_views.keys()), list(ABM_acc_views.values()), label=u'Facturación de "A Beautiful Mind" en primeras 10 semanas')
plt.plot(list(GLAD_acc_views.keys()), list(GLAD_acc_views.values()), label=u'Facturación de "Gladiator" en primeras 10 semanas')
plt.xlabel('days')
plt.ylabel('Accumulated receipts($)')

plt.legend(loc=2)
plt.show()

# # # PIE GRAPHIC
# data = [ABM_acc_views[70], BAT_acc_views[70], GLAD_acc_views[70], TNC_acc_views[70]]
# plt.pie(data, labels=('A Beautiful Mind', 'Batman', 'Gladiator', 'Titanic'))
# plt.show()
