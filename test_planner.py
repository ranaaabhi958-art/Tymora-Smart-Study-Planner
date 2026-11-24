import unittest
from datetime import date, timedelta
from planner import generate_schedule, validate_inputs, validate_schedule

class PlannerTests(unittest.TestCase):
    def setUp(self):
        today = date.today()
        self.subjects = [
            {"name":"Algorithms","exam_date":today+timedelta(days=3),"difficulty":"Hard","preparation":"Weak"},
            {"name":"Networks","exam_date":today+timedelta(days=7),"difficulty":"Medium","preparation":"Good"},
        ]

    def test_valid_inputs(self):
        self.assertEqual(validate_inputs(self.subjects, 4, 50), [])

    def test_empty_subjects_rejected(self):
        self.assertTrue(validate_inputs([], 4, 50))

    def test_daily_limit_respected(self):
        schedule = generate_schedule(self.subjects, 4, 50)
        self.assertEqual(validate_schedule(schedule, 4), [])

    def test_no_sessions_after_exam(self):
        schedule = generate_schedule(self.subjects, 4, 50)
        for item in schedule:
            self.assertLessEqual(date.fromisoformat(item["Date"]), date.fromisoformat(item["Exam date"]))

    def test_positive_durations(self):
        schedule = generate_schedule(self.subjects, 3, 45)
        self.assertTrue(all(x["Duration (minutes)"] > 0 for x in schedule))

if __name__ == "__main__":
    unittest.main()
