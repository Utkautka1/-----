"""
Главный запускаемый файл обучающего тренажёра (CLI и Интерактивное меню).

Зачем существует этот модуль:
Предоставляет студентам удобный интерфейс:
  1. Интерактивное меню (можно просто запускать python tutor.py и жать 1, 2, 3...)
  2. Быстрые команды CLI (python tutor.py test 3, python tutor.py hint 3 1...)
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


def show_lesson_card(lesson: Lesson) -> None:
    """Выводит карточку одного урока в консоль."""
    num = f"{lesson.index:02d}"
    print(f" {COLORS.CYAN}[{num}]{COLORS.RESET} {COLORS.BOLD}{lesson.title}{COLORS.RESET}")
    print(f"      Папка: lessons/{lesson.path.name}")
    print(f"      Уровни: {COLORS.GREEN}base{COLORS.RESET} (с нуля), {COLORS.YELLOW}standard{COLORS.RESET} (норма), {COLORS.RED}advanced{COLORS.RESET} (профи)")


def cmd_list() -> None:
    """Отображает список всех доступных уроков 1 курса."""
    print()
    print(f"{COLORS.BOLD}📚 ОБУЧАЮЩИЕ УРОКИ И ПРАКТИКИ (1 КУРС):{COLORS.RESET}")
    print("=" * 62)
    for item in lesson_service.get_all_lessons():
        show_lesson_card(item)
    print("=" * 62)
    print()


def parse_difficulty(args: List[str]) -> DifficultyLevel:
    """Определяет уровень сложности из переданных аргументов командной строки."""
    if "--level" in args:
        idx = args.index("--level")
        if idx + 1 < len(args):
            choice = args[idx + 1].lower()
            if choice == "base":
                return DifficultyLevel.BASE
            if choice == "advanced":
                return DifficultyLevel.ADVANCED
    return DifficultyLevel.STANDARD


def cmd_test(args: List[str]) -> None:
    """Запускает автопроверку решения студента."""
    if not args or not args[0].isdigit():
        print(f"{COLORS.RED}Укажите номер урока. Пример: python tutor.py test 3{COLORS.RESET}")
        return

    lesson_num = int(args[0])
    lesson = lesson_service.get_lesson_by_index(lesson_num)
    if not lesson:
        print(f"{COLORS.RED}Урок №{lesson_num} не найден.{COLORS.RESET}")
        return

    level = parse_difficulty(args)
    print(f"\n{COLORS.BOLD}🚀 Проверка урока №{lesson_num}:{COLORS.RESET} {lesson.title} [{level.value}]")
    print("-" * 62)
    result = test_runner.run_tests(lesson, level)
    display_test_result(result, lesson_num)


def display_test_result(result, lesson_num: int) -> None:
    """Печатает вердикт тестирования с рекомендациями."""
    if result.success:
        print(f"{COLORS.GREEN}✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!{COLORS.RESET}")
        print(f"   Результат: {result.passed_tests} из {result.total_tests} тестов.")
        print(f"   {result.message}\n")
    else:
        print(f"{COLORS.RED}❌ ОБНАРУЖЕНЫ ОШИБКИ В РЕШЕНИИ{COLORS.RESET}")
        print(f"   Пройдено: {result.passed_tests} из {result.total_tests} тестов.")
        print(f"   Подробности: {result.message}\n")
        print(f"{COLORS.YELLOW}💡 Подсказка: 'python tutor.py hint {lesson_num} 1'{COLORS.RESET}\n")


def cmd_hint(args: List[str]) -> None:
    """Выводит ступенчатую подсказку к уроку."""
    if not args or not args[0].isdigit():
        print(f"{COLORS.RED}Укажите номер урока. Пример: python tutor.py hint 3 1{COLORS.RESET}")
        return

    lesson_num = int(args[0])
    lesson = lesson_service.get_lesson_by_index(lesson_num)
    if not lesson:
        print(f"{COLORS.RED}Урок №{lesson_num} не найден.{COLORS.RESET}")
        return

    step = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
    hints = hint_service.load_hints(lesson_service.get_hints_file(lesson))
    hint = hint_service.get_hint_by_level(hints, step)
    if not hint:
        print(f"{COLORS.YELLOW}Подсказка уровня {step} отсутствует. Доступны: 1, 2, 3.{COLORS.RESET}")
        return
    print(f"\n{hint_service.format_hint(hint)}\n")


def cmd_variant(args: List[str]) -> None:
    """Генерирует уникальный вариант задания по ФИО студента."""
    if not args:
        print(f"{COLORS.RED}Укажите имя. Пример: python tutor.py variant 'Иванов Иван' 3{COLORS.RESET}")
        return

    student_name = args[0]
    lesson_num = int(args[1]) if len(args) > 1 and args[1].isdigit() else 3
    data = variant_generator.generate_variant(student_name, lesson_num)

    print(f"\n{COLORS.BOLD}🎯 Персональный вариант для:{COLORS.RESET} {COLORS.CYAN}{student_name}{COLORS.RESET}")
    print(f"   Урок №{lesson_num} (Идентификатор: {data.get('seed')})")
    print("=" * 62)
    for key, value in data.items():
        if key not in ("name", "seed"):
            print(f"   • {COLORS.BOLD}{key}{COLORS.RESET}: {value}")
    print("=" * 62 + "\n")


def cmd_quiz(args: List[str]) -> None:
    """Запускает интерактивный опрос на закрепление материала."""
    if not args or not args[0].isdigit():
        print(f"{COLORS.RED}Укажите номер урока. Пример: python tutor.py quiz 6{COLORS.RESET}")
        return

    lesson_num = int(args[0])
    lesson = lesson_service.get_lesson_by_index(lesson_num)
    if not lesson:
        print(f"{COLORS.RED}Урок №{lesson_num} не найден.{COLORS.RESET}")
        return

    questions = quiz_service.load_quiz(lesson_service.get_quiz_file(lesson))
    if not questions:
        print(f"{COLORS.YELLOW}Квиз для этого урока пока готовится.{COLORS.RESET}")
        return

    print(f"\n{COLORS.BOLD}🧠 ПРОВЕРОЧНЫЙ КВИЗ: {lesson.title}{COLORS.RESET}")
    score = sum(quiz_service.ask_question(i, q) for i, q in enumerate(questions, 1))
    print(f"\n{COLORS.BOLD}Итог квиза: {score} из {len(questions)} правильных ответов!{COLORS.RESET}\n")


def interactive_menu() -> None:
    """Интерактивное меню: позволяет выбирать уроки и действия простым вводом цифр."""
    while True:
        cmd_list()
        user_input = input(f"{COLORS.CYAN}Введите номер урока (1-6) или 'q' для выхода: {COLORS.RESET}").strip()
        if user_input.lower() in ("q", "quit", "exit", "выход"):
            print("До встречи! Успешной практики!")
            break
        if user_input.isdigit() and 1 <= int(user_input) <= 6:
            lesson_action_menu(int(user_input))
        else:
            print(f"{COLORS.RED}Пожалуйста, введите цифру от 1 до 6.{COLORS.RESET}\n")


def lesson_action_menu(lesson_num: int) -> None:
    """Подменю действий внутри выбранного урока."""
    lesson = lesson_service.get_lesson_by_index(lesson_num)
    if not lesson:
        return
    while True:
        print(f"\n{COLORS.BOLD}Меню урока [{lesson_num:02d}]: {lesson.title}{COLORS.RESET}")
        print("  [1] Проверить уровень: 🟢 С нуля (base)")
        print("  [2] Проверить уровень: 🟡 Стандарт (standard)")
        print("  [3] Проверить уровень: 🔴 Профи (advanced)")
        print("  [4] Показать подсказку (Шаг 1: Идея)")
        print("  [5] Показать подсказку (Шаг 2: Алгоритм)")
        print("  [6] Показать подсказку (Шаг 3: Код и разбор)")
        print("  [7] Пройти проверочный квиз")
        print("  [8] Получить персональный вариант")
        print("  [0] ⬅ Назад ко всем урокам")

        choice = input(f"{COLORS.CYAN}Выберите действие (0-8): {COLORS.RESET}").strip()
        if choice == "0":
            break
        execute_menu_action(lesson_num, choice)


def execute_menu_action(num: int, choice: str) -> None:
    """Выполняет выбранное действие из подменю урока."""
    if choice == "1":
        cmd_test([str(num), "--level", "base"])
    elif choice == "2":
        cmd_test([str(num), "--level", "standard"])
    elif choice == "3":
        cmd_test([str(num), "--level", "advanced"])
    elif choice in ("4", "5", "6"):
        step = int(choice) - 3
        cmd_hint([str(num), str(step)])
    elif choice == "7":
        cmd_quiz([str(num)])
    elif choice == "8":
        name = input("Введите ваше имя/ФИО: ").strip() or "Студент"
        cmd_variant([name, str(num)])


def main() -> None:
    """Точка входа: запускает интерактивный режим либо команду CLI."""
    if len(sys.argv) < 2:
        interactive_menu()
        return

    cmd = sys.argv[1].lower()
    args = sys.argv[2:]
    actions = {
        "list": lambda: cmd_list(),
        "test": lambda: cmd_test(args),
        "hint": lambda: cmd_hint(args),
        "variant": lambda: cmd_variant(args),
        "quiz": lambda: cmd_quiz(args),
    }
    handler = actions.get(cmd)
    if handler:
        handler()
    else:
        interactive_menu()


if __name__ == "__main__":
    main()
