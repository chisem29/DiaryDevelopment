from getOptimLessons import getOptimLessonsData as GBLD

classTable = GBLD('result').set_index('Класс')

teacherTable = GBLD('teachersRes').set_index('Учитель')

classRoomsTable = GBLD('classRoom1').set_index('Кабинет')
