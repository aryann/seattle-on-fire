import datetime
import unittest

import query_planner


class TestCreatePlan(unittest.TestCase):

    def test_start_resolution_checking(self):
        with self.assertRaises(ValueError):
            query_planner.create_plan(
                start=datetime.datetime(year=2017, month=1, day=15, hour=5, minute=55),
                end=datetime.datetime(year=2017, month=3, day=15))

    def test_end_resolution_checking(self):
        with self.assertRaises(ValueError):
            query_planner.create_plan(
                start=datetime.datetime(year=2017, month=1, day=15, hour=5),
                end=datetime.datetime(year=2017, month=3, day=15, minute=10))

    def test_single_day_range(self):
        plan = query_planner.create_plan(
            start=datetime.datetime(year=2017, month=1, day=15, hour=5),
            end=datetime.datetime(year=2017, month=1, day=15, hour=11))
        self.assertEqual(plan, [
            query_planner.Key(
                datetime.datetime(year=2017, month=1, day=15, hour=5),
                duration='1h'),
            query_planner.Key(
                datetime.datetime(year=2017, month=1, day=15, hour=6),
                duration='1h'),
            query_planner.Key(
                datetime.datetime(year=2017, month=1, day=15, hour=7),
                duration='1h'),
            query_planner.Key(
                datetime.datetime(year=2017, month=1, day=15, hour=8),
                duration='1h'),
            query_planner.Key(
                datetime.datetime(year=2017, month=1, day=15, hour=9),
                duration='1h'),
            query_planner.Key(
                datetime.datetime(year=2017, month=1, day=15, hour=10),
                duration='1h'),
        ])

    def test_multiple_day_range(self):
        plan = query_planner.create_plan(
            start=datetime.datetime(year=2017, month=1, day=15, hour=23),
            end=datetime.datetime(year=2017, month=1, day=18, hour=2))
        self.assertEqual(plan, [
            query_planner.Key(
                datetime.datetime(year=2017, month=1, day=15, hour=23),
                duration='1h'),
            query_planner.Key(
                datetime.datetime(year=2017, month=1, day=16),
                duration='1d'),
            query_planner.Key(
                datetime.datetime(year=2017, month=1, day=17),
                duration='1d'),
            query_planner.Key(
                datetime.datetime(year=2017, month=1, day=18, hour=0),
                duration='1h'),
            query_planner.Key(
                datetime.datetime(year=2017, month=1, day=18, hour=1),
                duration='1h'),
        ])

    def test_multiple_week_range(self):
        plan = query_planner.create_plan(
            start=datetime.datetime(year=2017, month=1, day=15, hour=23),
            end=datetime.datetime(year=2017, month=3, day=18, hour=2))
        self.assertEqual(plan, [
            query_planner.Key(
                datetime.datetime(year=2017, month=1, day=15, hour=23),
                duration='1h'),
            query_planner.Key(
                datetime.datetime(year=2017, month=1, day=16),
                duration='1w'),
            query_planner.Key(
                datetime.datetime(year=2017, month=1, day=23),
                duration='1w'),
            query_planner.Key(
                datetime.datetime(year=2017, month=1, day=30),
                duration='1w'),
            query_planner.Key(
                datetime.datetime(year=2017, month=2, day=6),
                duration='1w'),
            query_planner.Key(
                datetime.datetime(year=2017, month=2, day=13),
                duration='1w'),
            query_planner.Key(
                datetime.datetime(year=2017, month=2, day=20),
                duration='1w'),
            query_planner.Key(
                datetime.datetime(year=2017, month=2, day=27),
                duration='1w'),
            query_planner.Key(
                datetime.datetime(year=2017, month=3, day=6),
                duration='1w'),
            query_planner.Key(
                datetime.datetime(year=2017, month=3, day=13),
                duration='1d'),
            query_planner.Key(
                datetime.datetime(year=2017, month=3, day=14),
                duration='1d'),
            query_planner.Key(
                datetime.datetime(year=2017, month=3, day=15),
                duration='1d'),
            query_planner.Key(
                datetime.datetime(year=2017, month=3, day=16),
                duration='1d'),
            query_planner.Key(
                datetime.datetime(year=2017, month=3, day=17),
                duration='1d'),
            query_planner.Key(
                datetime.datetime(year=2017, month=3, day=18, hour=0),
                duration='1h'),
            query_planner.Key(
                datetime.datetime(year=2017, month=3, day=18, hour=1),
                duration='1h'),
        ])


if __name__ == '__main__':
    unittest.main()
