"""
Генератор персональных вариантов заданий.

Формирует детерминированные уникальные входные данные для каждого студента
на основе его ФИО или никнейма, исключая списывание готовых ответов.
"""

import hashlib
import random
from typing import Any, Dict
from services.base import BaseService


class VariantGenerator(BaseService):
    """Генерирует индивидуальные числовые параметры и условия задач."""

    def __init__(self) -> None:
        super().__init__("variant_generator")

    def _get_seed_from_identifier(self, identifier: str) -> int:
        """Вычисляет числовой seed из строки ФИО через SHA-256."""
        normalized = identifier.strip().lower().encode("utf-8")
        hash_digest = hashlib.sha256(normalized).hexdigest()
        return int(hash_digest[:12], 16)

    def generate_variant(self, identifier: str, lesson_idx: int) -> Dict[str, Any]:
        """Генерирует параметры варианта для указанного урока."""
        seed = self._get_seed_from_identifier(identifier)
        rng = random.Random(seed + lesson_idx * 1000)
        self.log.debug(f"Генерация варианта: id={identifier}, seed={seed}")
        generators = {
            1: self._gen_git_basics,
            2: self._gen_git_branching,
            3: self._gen_conditions,
            4: self._gen_flowcharts,
            5: self._gen_arrays,
            6: self._gen_binary_search,
        }
        gen_func = generators.get(lesson_idx, self._gen_default)
        return gen_func(rng, identifier, seed)

    def _gen_git_basics(self, rng: random.Random, name: str, seed: int) -> Dict[str, Any]:
        """Генерирует уникальные параметры для 1-го урока Git."""
        suffix = rng.randint(100, 999)
        return {
            "name": name,
            "seed": seed,
            "repo_dir": f"project_{suffix}",
            "marker_text": f"Study Project by {name} (ID: {suffix})",
            "diff_marker": f"Feature line added: {rng.randint(1000, 9999)}",
        }

    def _gen_git_branching(self, rng: random.Random, name: str, seed: int) -> Dict[str, Any]:
        """Генерирует уникальные параметры для 2-го урока Git (ветвление)."""
        branches = ["feature-auth", "task-logic", "patch-core", "dev-v1"]
        return {
            "name": name,
            "seed": seed,
            "branch_name": f"{rng.choice(branches)}_{rng.randint(10, 99)}",
            "conflict_file": f"config_{rng.randint(1, 9)}.txt",
            "main_content": f"PORT={rng.randint(3000, 8000)}",
            "branch_content": f"PORT={rng.randint(8001, 9999)}",
        }

    def _gen_conditions(self, rng: random.Random, name: str, seed: int) -> Dict[str, Any]:
        """Генерирует персональные числа для условий и площадей фигур."""
        return {
            "name": name,
            "seed": seed,
            "leap_year_test": rng.choice([1600, 1900, 2000, 2024, 2100, 2400]),
            "rect_a": rng.randint(3, 15),
            "rect_b": rng.randint(4, 20),
            "circle_r": round(rng.uniform(2.5, 9.5), 1),
            "triangle_a": rng.randint(5, 12),
            "triangle_b": rng.randint(5, 12),
            "triangle_c": rng.randint(5, 12),
        }

    def _gen_flowcharts(self, rng: random.Random, name: str, seed: int) -> Dict[str, Any]:
        """Генерирует трассировочные значения для проверки блок-схем."""
        start_x = rng.randint(1, 10)
        multiplier = rng.randint(2, 4)
        return {
            "name": name,
            "seed": seed,
            "start_x": start_x,
            "multiplier": multiplier,
            "iterations": 3,
            "task_goal": "Вычислить значение x после прохода цикла из 3 шагов",
        }

    def _gen_arrays(self, rng: random.Random, name: str, seed: int) -> Dict[str, Any]:
        """Генерирует персональный массив чисел для сортировки и фильтрации."""
        sample_size = rng.randint(8, 12)
        raw_list = [rng.randint(-20, 50) for _ in range(sample_size)]
        return {
            "name": name,
            "seed": seed,
            "numbers": raw_list,
            "target_filter": "Удалить отрицательные и отсортировать по возрастанию",
        }

    def _gen_binary_search(self, rng: random.Random, name: str, seed: int) -> Dict[str, Any]:
        """Генерирует персональный диапазон и искомое для бинарного поиска."""
        lower = rng.randint(1, 50)
        upper = lower + rng.randint(80, 200)
        target = rng.randint(lower, upper)
        return {
            "name": name,
            "seed": seed,
            "lower_bound": lower,
            "upper_bound": upper,
            "target_x": target,
        }

    def _gen_default(self, rng: random.Random, name: str, seed: int) -> Dict[str, Any]:
        """Заглушка для дополнительных тем."""
        return {"name": name, "seed": seed, "param": rng.randint(1, 100)}
