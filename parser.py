import bs4.element
import requests
import re
import json

import sqlite3

from bs4 import BeautifulSoup


def parse_staff():
    next_link = "https://ssau.ru/staff"
    conn = sqlite3.connect('database.sqlite3')
    while next_link:
        r = requests.get(next_link)
        staff_list = re.findall(r"https://ssau\.ru/staff/[0-9A-Za-z\-]+\">\n[А-Я][а-я]+ [А-Я][а-я]+ [А-Я][а-я]+\n", r.text)
        for staff_str in staff_list:
            full_name = re.findall(r"[А-Я][а-я]+ [А-Я][а-я]+ [А-Я][а-я]+", staff_str)
            link = re.findall(r"https://ssau\.ru/staff/[0-9A-Za-z\-]+", staff_str)
            id = re.findall("\d+", link[0])[0]
            try:
                conn.execute(f"INSERT INTO teachers VALUES (?, ?)", (id, full_name[0]))
            except(sqlite3.IntegrityError):
                print(full_name[0])
                pass
        next_page_exists = re.findall(r"href=\"https:\/\/ssau\.ru\/staff\?page=[0-9]+&amp;letter=0\">Вперёд", r.text)
        if len(next_page_exists):
            next_link = re.findall(r"https://ssau.ru/staff\?page=\d+", next_page_exists[0])[0]
        else:
            conn.commit()
            conn.close()
            return


def parse_groups():
    domain = 'https://ssau.ru'
    link = '/rasp'
    r = requests.get(domain + link)
    page = BeautifulSoup(r.text, 'html.parser')
    links = page.findAll('div', class_="faculties__item")
    faculty_links = []
    links_to_parse_groups = []
    for link in links:
        faculty_links.append(link.a['href'])
    for faculty in faculty_links:
        faculty_request = requests.get(domain + faculty)
        parsed_faculty_request = BeautifulSoup(faculty_request.text, 'html.parser')
        years = parsed_faculty_request.findAll('div', class_="nav-course__item")
        for year in years:
            links_to_parse_groups.append(year.a['href'])
    result = []
    for elem in links_to_parse_groups:
        r = requests.get(domain + elem)
        page = BeautifulSoup(r.text, 'html.parser')
        groups = page.findAll('a', class_='btn-text group-catalog__group')
        for group in groups:
            result.append((group.text, group['href']))
    return result


def get_timetable(category: str, id: int, week: int, yearId=9):
    if not week:
        week = 16
    link = "https://cabinet.ssau.ru/api/timetable/get-timetable?yearId="+str(yearId)+"&week="+str(week)+"&userType=student&groupId="+str(id)
    if category == "staff":
        link = "https://cabinet.ssau.ru/api/timetable/get-timetable?yearId="+str(yearId)+"&week="+str(week)+"&userType=student&staffId="+str(id)
    r = requests.get(link, cookies={"laravel_session": ""})
    lessons = json.loads(r.text)['lessons']
    result = []
    for lesson in lessons:
        type = lesson['type']['name']
        teacher = lesson['teachers'][0]
        teacher_id = teacher['id']
        teacher_name = teacher['name']
        day = lesson['weekday']['name']
        time = lesson['time']['name']
        discipline = lesson['discipline']['name']
        weeks = [elem['week'] for elem in lesson['weeks']]
        result.append({'discipline': discipline, 'type': type, 'teacher': [teacher_id, teacher_name],
                       'day': day, time: 'time', 'weeks': weeks})
    return result


def parse_timetable(category: str, id: int, week: int, day: int):
    domain = "https://ssau.ru"
    if category == "group":
        link = "/rasp?groupId=" + str(id)
    else:
        link = "/rasp?staffId=" + str(id)
    if week:
        link += "&selectedWeek=" + str(week)
    if day:
        link += "&selectedWeekday=" + str(day)
    else:
        link += "&selectedWeekday=1"

    r = requests.get(domain + link)
    schedule = BeautifulSoup(r.text, 'html.parser')
    times = []
    for time_item in schedule.findAll('div', class_="schedule__time"):
        times.append([elem.text.strip() for elem in time_item.children])

    header = []
    lessons = []
    info = {}
    for object_name in schedule.findAll('h2', class_='info-block__title'):
        info['object_name'] = object_name.text.strip()
    info['object_info'] = []
    for object_infos in schedule.findAll('div', class_='info-block__description'):
        for object_info in object_infos.children:
            info['object_info'].append(object_info.text.strip())
    for schedule_item in schedule.findAll('div', class_="schedule__item"):
        if "schedule__head" in schedule_item.attrs['class']:
            header.append([header_elem.text.strip() for header_elem in schedule_item.children])
            continue
        else:
            lesson_attrs = [elem for elem in schedule_item.children]
            groups = []
            lesson = {}
            if len(lesson_attrs) != 0:
                for elem in lesson_attrs[0].children:
                    if type(elem) == bs4.NavigableString:
                        continue
                    if 'schedule__discipline' in elem.attrs['class']:
                        lesson['subject'] = elem.text.strip()
                        continue
                    if 'schedule__teacher' in elem.attrs['class']:
                        lesson['teacher_name'] = elem.text.strip()
                        lesson['teacher_link'] = ""
                        if elem.a:
                            teaher_link = elem.a['href']
                            teacher_id = re.findall(r'\d+', teaher_link)[0]
                            lesson['teacher_link'] = teacher_id
                        continue
                    if 'schedule__groups' in elem.attrs['class']:
                        for group in elem.children:
                            if type(group) == bs4.element.Tag:
                                group_name = group.text.strip()
                                group_id = ""
                                if 'href' in group.attrs:
                                    group_link = group.attrs['href']
                                    group_id = re.findall(r'\d+', group_link)[0]
                                groups.append({'group_name': group_name, 'group_link': group_id})
                        continue
                    if 'schedule__group' in elem.attrs['class']:
                        if type(elem) == bs4.element.Tag:
                            group_name = elem.text
                            group_id = ''
                            if 'href' in elem.attrs:
                                group_link = elem.attrs['href']
                                group_id = re.findall(r'\d+', group_link)[0]
                            groups.append({'group_name': group_name, 'group_link': group_id})
                        continue
                    if 'schedule__place' in elem.attrs['class']:
                        lesson['place'] = elem.text.strip()

                lesson['groups'] = groups
                lessons.append(lesson)
            else:
                lessons.append({})
    result = {}
    result['info'] = info
    result['times'] = times
    result['header'] = header
    result['lessons'] = lessons
    return result


def insert_groups_into_sqlite(groups: list):
    conn = sqlite3.connect('database.sqlite3')
    for group in groups:
        name = re.findall('\d{4}-\d{6}[DZV]', group[0])[0]
        id = re.findall('\d+', group[1])[0]
        try:
            conn.execute(f"INSERT INTO groups VALUES (?, ?)", (id, name))
        except sqlite3.IntegrityError:
            print(name)
            pass
    conn.commit()
    conn.close()


def get_current_week():
    r = requests.get("https://ssau.ru/rasp?groupId=531873998")
    page = BeautifulSoup(r.text, 'html.parser')
    week_arr = page.findAll('span', class_="h3-text week-nav-current_week")
    if len(week_arr):
        week = week_arr[0].text
        week_number = int(re.findall(r'\d+', week)[0])
        return week_number
    else:
        return None
