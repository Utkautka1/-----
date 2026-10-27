"""
Главный запускаемый файл обучающего тренажёра (CLI).

Зачем существует этот модуль:
Предоставляет студентам понятный интерфейс для запуска тестов,
получения подсказок, генерации персональных заданий и прохождения квизов.

Как запустить:
    python tutor.py list                 # Показать список тем
    python tutor.py test 3               # Проверить решение урока 3
    python tutor.py test 3 --level base  # Проверить уровень для новичков
    python tutor.py hint 3 1             # Показать подсказку №1 к уроку 3
    python tutor.py variant "Иванов Иван" 3
    python tutor.py quiz 3               # Запустить квиз по уроку 3
"""

import sys
from typing import List

from config import COLORS
from core.models import DifficultyLevel, Lesson
from services.hint_service import HintService
from services.lesson_service import LessonService
from services.quiz_service import QuizService
from services.test_runner import TestRunner
from services.variant_generator import VariantGenerator


# Инициализируем сервисы системы
lesson_service = LessonService()
test_runner = TestRunner()
hint_service = HintService()
quiz_service = QuizService()
variant_generator = VariantGenerator()


def show_help() -> None:
    """Выводит справку по доступным командам тренажёра."""
    print()
    print(f"{COLORS.BOLD}Использование тренажёра:{COLORS.RESET}")
    print("  python tutor.py list                 — Список всех тем")
    print("  python tutor.py test <номер>         — Проверить решение")
    print("  python tutor.py test <номер> --level base|standard|advanced")
    print("  python tutor.py hint <номер> <шаг>   — Подсказка (шаги 1, 2, 3)")
    print("  python tutor.py variant <ФИО>        — Персональный вариант")
    print("  python tutor.py quiz <номер>         — Проверочный квиз")
    print()


def show_lesson_card(lesson: Lesson) -> None:
    """Выводит карточку одного урока в консоль."""
    num = f"{lesson.index:02d}"
    print(f" {COLORS.CYAN}[{num}]{COLORS.RESET} {COLORS.BOLD}{lesson.title}{COLORS.RESET}")
    print(f"      Папка: lessons/{lesson.path.name}")
    print(f"      Уровни сложности:")
    print(f"        • {COLORS.GREEN}base{COLORS.RESET}     — с нуля, пошаговые подсказки")
    print(f"        • {COLORS.YELLOW}standard{COLORS.RESET} — практическая работа кафедры")
    print(f"        • {COLORS.RED}advanced{COLORS.RESET} — повышенная сложность, профи")
    print()


def cmd_list() -> None:
    """Отображает список всех доступных уроков 1 курса."""
    all_lessons = lesson_service.get_all_lessons()

    print()
    print(f"{COLORS.BOLD}📚 ОБУЧАЮЩИЕ УРОКИ И ПРАКТИКИ (1 КУРС):{COLORS.RESET}")
    print("=" * 60)
    print()

    for item in all_lessons:
        show_lesson_card(item)

    print("=" * 60)
    print(f"{COLORS.DIM}Для начала выберите урок, например: python tutor.py test 1{COLORS.RESET}")
    print()


def parse_difficulty(args: List[str]) -> DifficultyLevel:
    """Определяет уровень сложности из переданных аргументов командной строки."""
    if "--level" in args:
        idx = args.index("--level")
        if idx + 1 < len(args):
            user_choice = args[idx + 1].lower()
            if user_choice == "base":
                return DifficultyLevel.BASE
            if user_choice == "advanced":
                return DifficultyLevel.ADVANCED
    return DifficultyLevel.STANDARD


def cmd_test(args: List[str]) -> None:
    """Запускает автопроверку решения студента."""
    if not args or not args[0].isdigit():
        print(f"{COLORS.RED}Ошибка: укажите номер урока. Пример: python tutor.py test 3{COLORS.RESET}")
        return

    lesson_num = int(args[0])
    lesson = lesson_service.get_lesson_by_index(lesson_num)
    if not lesson:
        print(f"{COLORS.RED}Ошибка: урок №{lesson_num} не найден.{COLORS.RESET}")
        return

    level = parse_difficulty(args)
    print()
    print(f"{COLORS.BOLD}🚀 Проверка урока №{lesson_num}:{COLORS.RESET} {lesson.title}")
    print(f"   Уровень сложности: {COLORS.CYAN}{level.value}{COLORS.RESET}")
    print("-" * 60)

    result = test_runner.run_tests(lesson, level)
    display_test_result(result, lesson_num)


def display_test_result(result, lesson_num: int) -> None:
    """Печатает вердикт тестирования с рекомендациями."""
    if result.success:
        print(f"{COLORS.GREEN}✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!{COLORS.RESET}")
        print(f"   Результат: {result.passed_tests} из {result.total_tests} тестов.")
        print(f"   {result.message}")
        print()
    else:
        print(f"{COLORS.RED}❌ ОБНАРУЖЕНЫ ОШИБКИ В РЕШЕНИИ{COLORS.RESET}")
        print(f"   Пройдено: {result.passed_tests} из {result.total_tests} тестов.")
        print(f"   Подробности: {result.message}")
        print()
        print(f"{COLORS.YELLOW}💡 Подсказка: запустите 'python tutor.py hint {lesson_num} 1'{COLORS.RESET}")
        print()


def cmd_hint(args: List[str]) -> None:
    """Выводит ступенчатую подсказку к уроку."""
    if not args or not args[0].isdigit():
        print(f"{COLORS.RED}Ошибка: укажите номер урока. Пример: python tutor.py hint 3 1{COLORS.RESET}")
        return

    lesson_num = int(args[0])
    lesson = lesson_service.get_lesson_by_index(lesson_num)
    if not lesson:
        print(f"{COLORS.RED}Ошибка: урок №{lesson_num} не найден.{COLORS.RESET}")
        return

    step = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
    hints_file = lesson_service.get_hints_file(lesson)
    hints = hint_service.load_hints(hints_file)
    hint = hint_service.get_hint_by_level(hints, step)

    if not hint:
        print(f"{COLORS.YELLOW}Подсказка уровня {step} отсутствует. Доступны уровни: 1, 2, 3.{COLORS.RESET}")
        return

    print()
    print(hint_service.format_hint(hint))
    print()


def cmd_variant(args: List[str]) -> None:
    """Генерирует уникальный вариант задания по ФИО студента."""
    if not args:
        print(f"{COLORS.RED}Ошибка: укажите имя. Пример: python tutor.py variant 'Иванов Иван' 3{COLORS.RESET}")
        return

    student_name = args[0]
    lesson_num = int(args[1]) if len(args) > 1 and args[1].isdigit() else 3
    data = variant_generator.generate_variant(student_name, lesson_num)

    print()
    print(f"{COLORS.BOLD}🎯 Персональный вариант для:{COLORS.RESET} {COLORS.CYAN}{student_name}{COLORS.RESET}")
    print(f"   Урок №{lesson_num} (Идентификатор: {data.get('seed')})")
    print("=" * 60)
    for key, value in data.items():
        if key not in ("name", "seed"):
            print(f"   • {COLORS.BOLD}{key}{COLORS.RESET}: {value}")
    print("=" * 60)
    print()


def cmd_quiz(args: List[str]) -> None:
    """Запускает интерактивный опрос на закрепление материала."""
    if not args or not args[0].isdigit():
        print(f"{COLORS.RED}Ошибка: укажите номер урока. Пример: python tutor.py quiz 6{COLORS.RESET}")
        return

    lesson_num = int(args[0])
    lesson = lesson_service.get_lesson_by_index(lesson_num)
    if not lesson:
        print(f"{COLORS.RED}Ошибка: урок №{lesson_num} не найден.{COLORS.RESET}")
        return

    quiz_file = lesson_service.get_quiz_file(lesson)
    questions = quiz_service.load_quiz(quiz_file)
    if not questions:
        print(f"{COLORS.YELLOW}Квиз для этого урока пока готовится.{COLORS.RESET}")
        return

    print()
    print(f"{COLORS.BOLD}🧠 ПРОВЕРОЧНЫЙ КВИЗ: {lesson.title}{COLORS.RESET}")
    score = 0
    for i, q in enumerate(questions, start=1):
        if quiz_service.ask_question(i, q):
            score += 1

    print()
    print(f"{COLORS.BOLD}Итог квиза: {score} из {len(questions)} правильных ответов!{COLORS.RESET}")
    print()


def main() -> None:
    """Главная функция-диспетчер аргументов командной строки."""
    if len(sys.argv) < 2:
        cmd_list()
        return

    command = sys.argv[1].lower()
    command_args = sys.argv[2:]

    if command == "list":
        cmd_list()
    elif command == "test":
        cmd_test(command_args)
    elif command == "hint":
        cmd_hint(command_args)
    elif command == "variant":
        cmd_variant(command_args)
    elif command == "quiz":
        cmd_quiz(command_args)
    elif command in ("--help", "-h", "help"):
        show_help()
    else:
        print(f"{COLORS.RED}Неизвестная команда '{command}'.{COLORS.RESET}")
        show_help()


if __name__ == "__main__":
    main()
