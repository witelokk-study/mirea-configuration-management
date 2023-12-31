import json
import unittest
from cfglang.converter import Converter


class TestConvertToJson(unittest.TestCase):
    def setUp(self) -> None:
        self._converter = Converter()

    def test_convert_1(self):
        cfglang = """ (ship (registry 1701)
       (x        42)
       (y        13))
"""

        self.assertEqual(
            json.loads('{"ship": {"registry": 1701, "x": 42, "y": 13}}'),
            json.loads(self._converter.convert(cfglang))
        )

    def test_convert_2(self):
        cfglang = """ (users
   ((uid 1)   (name "root") (gid 1))
   ((uid 108) (name "matt") (gid 108))
   ((uid 109) (name "ralf") (gid 109)))
"""

        self.assertEqual(
            json.loads('{"users": [{"uid":1,"name":"root","gid":1}, {"uid":108,"name":"matt","gid":108}, {"uid":109,"name":"ralf","gid":109}]}'),
            json.loads(self._converter.convert(cfglang))
        )

    def test_convert_3(self):
        cfglang = '''(
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
'''
        expected = '''{
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
'''

        self.assertEqual(
            json.loads(expected),
            json.loads(self._converter.convert(cfglang))
        )