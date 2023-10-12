from typing import List, Tuple


# Работа с файлом ------------------------------------------------------
class File:
    def __init__(self, filename):
        self.filename = filename
        
    def read(self) -> List[str]:
        with open(self.filename, encoding="utf-8") as file:
            return file.readlines()
            
    def write(self, line: str) -> None:
        with open(self.filename, mode="a+") as file:
            file.write(line)
# ----------------------------------------------------------------------


# Вспомогательные функции ----------------------------------------------
def str_to_list_with_integers(string) -> List[int]:
    return list(map(int, string.strip().split()))


def get_student_str_and_result_list(string) -> Tuple[str, List[int]]:
    for i, char in enumerate(string):
        if char.isdigit():
            break
    return string[:i - 1], str_to_list_with_integers(string[i - 1:])


def calc_points_for_student(student_results, time_limits, max_points) -> int:
    points = 0
    for student_time, time_limit, max_point in zip(student_results, time_limits, max_points):
        if student_time > time_limit:
            points += max_point // 2
        elif 0 < student_time <= time_limit:
            points += max_point
    return points
    

def count_passed_tasks(student_results) -> int:
    return len([x for x in student_results if x > 0])
# ----------------------------------------------------------------------


def main() -> None:
    # Создаем файловые объекты ---------------------------------------------
    input_file = File("U1.txt")
    output_file = File("U1rez.txt")
    # ----------------------------------------------------------------------
    
    # Парсим данные из входного файла --------------------------------------
    _, time_limits, max_points, *students = input_file.read()

    time_limits = str_to_list_with_integers(time_limits)
    max_points = str_to_list_with_integers(max_points)
    students = dict([
        get_student_str_and_result_list(student)
        for student in students
    ])
    # ----------------------------------------------------------------------
    
    # Вычисления -----------------------------------------------------------
    students_result = {
        student_name: [
            count_passed_tasks(student_results), 
            sum(student_results),
            calc_points_for_student(student_results, time_limits, max_points)
            ]
        for student_name, student_results in students.items()
    }
    max_point_of_students = max(students_result.items(), key=lambda student: student[1][0])[1][2]
    
    students_result_max_point = [
        student
        for student in sorted(students_result.items(), key=lambda student: student[1][0], reverse=True)
        if student[1][2] == max_point_of_students
    ]
    # ----------------------------------------------------------------------
    
    # Записываем результат в выходной файл ---------------------------------
    output_file.write(f"{max_point_of_students}\n")
    
    for line in students_result_max_point:
        output_file.write(f"{line[0]} {line[1][0]} {line[1][1]}\n")
    # ----------------------------------------------------------------------
    
    
if __name__ == "__main__":
    main()
