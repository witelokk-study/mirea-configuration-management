# Задание
Реализовать синтаксический разбор придуманного вами конфигурационного языка, основанного на S-выражениях (в которых у нас есть только скобки, пробелы и значения различных типов) для представления информации о студентах и группах (см. задачу 1 из практики 3).

Формат должен быть основан на грамматике, приведенной ниже. Детали формата на основе S-выражений необходимо продумать самостоятельно и обязательно описать их в БНФ. Формат должен поддерживать комментарии, типы данных: число, имя, строка.
Разбор реализовать средствами типа Lex/Yacc на выбранном ЯП (SLY в Python, Flex/Bison в C/C++, ANTLR в Java, ...).
После разбора результат преобразовать в JSON-представление. Пример из ПР 3.1 у вас должен получиться на выходе таким же и это надо показать в решении.
Программа должна иметь интерфейс командной строки: входным аргументом является имя конфигурационного файла, а результатом выполнения является вывод на экран (stdout) результата трансляции в JSON.
Дополнительный плюс за поддержку принципа DRY (то есть в язык можно добавить переменные, функции и так далее).

Базовая грамматика, которую необходимо реализовать и расширить для своих нужд (комментарии, представление data...):

```
<program> ::= <s-exp-list> 
<s-exp> ::= <data> |  '(' <s-exp-list> ')'
<s-exp-list> ::= <sexp> <s-exp-list> |
```

Конфликты shift/reduce, которые выдает Yacc-подобный инструмент, недопустимы. Они возникают, если у вас неоднозначная грамматика, то есть одному предложению языка могут соответствовать несколько вариантов разбора. В этом случае нужно поправить грамматику.

## Грамматика
Граматика получившегося языка

```
<program> ::= <s-exp-list> 
<s-exp> ::= <data> |  '(' <s-exp-list> ')' <comment>
<s-exp-list> ::= <s-exp> <s-exp-list> |
<comment> = '#' <любые символы>
<data> = <ID> | <STRING> | <INT> | <FLOAT> <BOOL>
```

## Пример работы
Входной файл:
```
(
  (groups
    "ИКБО-1-20"
    "ИКБО-2-20"
    "ИКБО-3-20"
    "ИКБО-4-20"
    "ИКБО-5-20"
    "ИКБО-6-20"
    "ИКБО-7-20"
    "ИКБО-8-20"
    "ИКБО-9-20"
    "ИКБО-10-20"
    "ИКБО-11-20"
    "ИКБО-12-20"
    "ИКБО-13-20"
    "ИКБО-14-20"
    "ИКБО-15-20"
    "ИКБО-16-20"
    "ИКБО-17-20"
    "ИКБО-18-20"
    "ИКБО-19-20"
    "ИКБО-20-20"
    "ИКБО-21-20"
    "ИКБО-22-20"
    "ИКБО-23-20"
    "ИКБО-24-20"
  )
  (students
    (
      (age 19)
      (group "ИКБО-4-20")
      (name "Иванов И.И.")
    )
    (
      (age 18)
      (group "ИКБО-5-20")
      (name "Петров П.П.")
    )
    (
      (age 18)
      (group "ИКБО-5-20")
      (name "Сидоров С.С.")
    )
  )
  (subject "Конфигурационное управление")
)
```

Вывод программы:
```json
{
    "groups": [
        "ИКБО-1-20",
        "ИКБО-2-20",
        "ИКБО-3-20",
        "ИКБО-4-20",
        "ИКБО-5-20",
        "ИКБО-6-20",
        "ИКБО-7-20",
        "ИКБО-8-20",
        "ИКБО-9-20",
        "ИКБО-10-20",
        "ИКБО-11-20",
        "ИКБО-12-20",
        "ИКБО-13-20",
        "ИКБО-14-20",
        "ИКБО-15-20",
        "ИКБО-16-20",
        "ИКБО-17-20",
        "ИКБО-18-20",
        "ИКБО-19-20",
        "ИКБО-20-20",
        "ИКБО-21-20",
        "ИКБО-22-20",
        "ИКБО-23-20",
        "ИКБО-24-20"
    ],
    "students": [
        {
            "age": 19,
            "group": "ИКБО-4-20",
            "name": "Иванов И.И."
        },
        {
            "age": 18,
            "group": "ИКБО-5-20",
            "name": "Петров П.П."
        },
        {
            "age": 18,
            "group": "ИКБО-5-20",
            "name": "Сидоров С.С."
        }
    ],
    "subject": "Конфигурационное управление"
}
```

## Исходный код
% Код файла cfglang/cfglang/__main__.py
```python ./cfglang/cfglang/__main__.py
```

% Код файла cfglang/cfglang/converter.py
```python ./cfglang/cfglang/converter.py
```

% Код файла cfglang/cfglang/lang_lexer.py
```python ./cfglang/cfglang/lang_lexer.py
```

% Код файла cfglang/cfglang/lang_parser.py
```python ./cfglang/cfglang/lang_parser.py
```

% Код файла cfglang/pyproject.toml
```toml ./cfglang/pyproject.toml
```