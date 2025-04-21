from pathlib import Path
import itertools

def check_file_exist(filepath: Path):
    if filepath.exists():
        return True
    else:
        print(f"Файла '{filepath}' не существует! Пропуск")
        return False

def combine_dicts(dictionaries_to_combine: list[dict[str, list]]) -> dict:
    """## Объединение словарей
    ### Объединяет словари с одинаковыми ключами и одинаковыми одинаковым типом значений

    ### Args:
        `dictionaries_to_combine` (list[dict[str, list]]): Список словарей

    ### Returns:
        `dict`: Объединенный словарь с расширенным списком значений одного уровня
    """
    combined_logs = {}
    for k in dictionaries_to_combine[0]:
        combined_logs[k] = list(itertools.chain(*[d[k] for d in dictionaries_to_combine]))
    return combined_logs