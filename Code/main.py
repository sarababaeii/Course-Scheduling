from file_manager import FileManager
from day import Day
from course import Course
from lecturer import Lecturer
from faculty import Faculty
from period import Period
from gams import *
from os import *


BASE_DIR = path.abspath('')
ws = GamsWorkspace(working_directory=BASE_DIR, system_directory='/Library/Frameworks/GAMS.framework/Resources')


def set_input_data(courses, lecturers, periods, faculty, groups):
    db = ws.add_database()

    c_python = [str(course.num) for course in courses]
    c = db.add_set("c", 1)
    for cp in c_python:
        c.add_record(cp)

    l_python = [str(lecturer.num) for lecturer in lecturers]
    l = db.add_set("l", 1)
    for lp in l_python:
        l.add_record(lp)

    d_python = [str(i) for i in range(1, 6)]
    d = db.add_set("d", 1)
    for dp in d_python:
        d.add_record(dp)

    last_d_python = 5
    last_d = db.add_set("last_d", 1)
    last_d.add_record(str(last_d_python))

    h_python = [str(period.num) for period in periods]
    h = db.add_set("h", 1)
    for hp in h_python:
        h.add_record(hp)

    j_python = [str(i) for i in range(1, faculty.groups + 1)]
    j = db.add_set("j", 1)
    for jp in j_python:
        j.add_record(jp)

#    print("c:", c_python)
#    print("l:", l_python)
#    print("d:", d_python)
#    print("h:", h_python)
#    print("j:", j_python)

    k_python = faculty.classes
#    print("k:", k_python)
    k = db.add_parameter("k", 0)
    k.add_record().value = k_python

    n_python = {}
    for course in courses:
        n_python[str(course.num)] = course.get_class_num()
#    print("n:", n_python)
    n = db.add_parameter_dc("n", [c])
    for cp in c_python:
        n.add_record(cp).value = n_python[cp]

    u_python = {}
    for course in courses:
        u_python[str(course.num)] = int(course.is_3_units())
#    print("u:", u_python)
    u = db.add_parameter_dc("u", [c])
    for cp in c_python:
        u.add_record(cp).value = u_python[cp]

    s_python = {}
    for record in groups:
        s_python[record[1], record[2]] = 1
#    print("s:", s_python)
    s = db.add_parameter_dc("s", [j, c])
    for jp in j_python:
        for cp in c_python:
            if (jp, cp) in s_python:
                s.add_record((jp, cp)).value = s_python[(jp, cp)]

    a_python = {}
    for course in courses:
        a_python[str(course.num), str(course.lecturer_num)] = 1
#    print("a:", a_python)
    a = db.add_parameter_dc("a", [c, l])
    for cp in c_python:
        for lp in l_python:
            if (cp, lp) in a_python:
                a.add_record((cp, lp)).value = a_python[(cp, lp)]

    b_python = {}
    for lecturer in lecturers:
        for date in lecturer.availabe_dates:
            b_python[str(lecturer.num), str(date.day.value), str(date.period_num)] = 1
#    print("b:", b_python)
    b = db.add_parameter_dc("b", [l, d, h])
    for lp in l_python:
        for dp in d_python:
            for hp in h_python:
                if (lp, dp, hp) in b_python:
                    b.add_record((lp, dp, hp)).value = b_python[(lp, dp, hp)]

    f_python = {"3": 1, "8": 1}
#    print("f:", f_python)
    f = db.add_parameter_dc("f", [h])
    for hp in h_python:
        if (hp) in f_python:
            f.add_record(hp).value = f_python[hp]

    g_python = {}
    for period in periods:
        val = 0
        if period.is_2_hours() == False:
            val = 1
        g_python[str(period.num)] = val
#    print("g:", g_python)
    g = db.add_parameter_dc("g", [h])
    for hp in h_python:
        g.add_record(hp).value = g_python[hp]

    t_python = {}
    for p1 in periods:
        for p2 in periods:
            if p1.has_intersec_with(p2):
                t_python[str(p1.num), str(p2.num)] = 1
#    print("t:", t_python)
    t = db.add_parameter_dc("t", [h, h])
    for hp in h_python:
        for hp1 in h_python:
            if hp != hp1:
                if (hp, hp1) in t_python:
                    t.add_record((hp, hp1)).value = t_python[(hp, hp1)]

    M_python = len(d_python) * len(h_python)
#    print("M:", M_python)
    M = db.add_parameter("M", 0)
    M.add_record().value = M_python

    return db


def run_model():
    opt = ws.add_options()
    opt.defines["gdxincname"] = db.name
    m = ws.add_job_from_file("CourseTimetabling02.gms")
    m.run(opt, databases=db)
    return m


def show_output_data(m):
    var_z1 = [rec.level for rec in m.out_db["z1"]]
    print("z1: ", int(var_z1[0]), "\n")

    var_z2 = [rec.level for rec in m.out_db["z2"]]
    print("z2: ", int(var_z2[0]), "\n")

    var_z3 = [rec.level for rec in m.out_db["z3"]]
    print("z3: ", int(var_z3[0]), "\n")
    
    results = []
    for rec in m.out_db["delta"]:
        if int(rec.level) != 0:
            results.append((rec.key(0), rec.key(1), rec.key(2)))

    return results


def set_courses_dates(results, courses):
    for result in results:
        index = Course.get_index_of_num(int(result[0]), courses)
        day = Day.get_day_with_value(int(result[1]))
        courses[index].insert_date(day, result[2])

def show_results(courses, periods):
    print("Weekly Schedule:")
    for course in courses:
        print(course.num, end=": ")
        for date in course.scheduled_dates:
            day = date.day.get_string()
            period_index = Period.get_index_of_num(int(date.period_num), periods)
            print(day, periods[period_index].get_string(), end=",    ")
        print()


dataset = input("Dataset Name:")

periods = []
periods.append(Period(1, 8, 10))
periods.append(Period(2, 10, 12))
periods.append(Period(3, 13, 15))
periods.append(Period(4, 15, 17))
periods.append(Period(5, 7.45, 9.15))
periods.append(Period(6, 9.15, 10.45))
periods.append(Period(7, 10.45, 12.15))
periods.append(Period(8, 13.30, 15))
periods.append(Period(9, 15, 16.30))

courses = Course.create_courses(dataset + "/Sheet 1.csv")
lecturers = Lecturer.create_lecturers(dataset + "/Sheet 2.csv")
Course.set_lecturers(dataset + "/Sheet 3.csv", courses)
faculty = Faculty.create_faculty(dataset + "/Sheet 5.csv")
groups = FileManager.read_from_csv(dataset + "/Sheet 4.csv")

db = set_input_data(courses, lecturers, periods, faculty, groups)
m = run_model()
results = show_output_data(m)
set_courses_dates(results, courses)

show_results(courses, periods)
