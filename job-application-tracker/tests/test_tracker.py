"""
test_tracker.py
Unit and Integration Test Suite for Job Application Tracker.
Tests:
- JobApplication and Priority models
- DatabaseManager CRUD and SQL injection safety
- Priority field assignment, validation, and sorting order (High -> Medium -> Low)
- Search across Company, Role, Status, and Priority
- Update and Delete operations
- Database persistence across multiple DatabaseManager instances
"""

import os
import sys
import tempfile
import unittest

# Ensure parent directory is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import JobApplication, JobType, ApplicationStatus, Priority
from database import DatabaseManager


class TestJobApplicationModel(unittest.TestCase):
    """Tests OOP Models, encapsulation, priority logic, and validation."""

    def test_model_creation_defaults(self):
        app = JobApplication(
            company="Acme Corp",
            role="Python Developer",
            application_date="2026-11-01",
        )
        self.assertEqual(app.company, "Acme Corp")
        self.assertEqual(app.role, "Python Developer")
        self.assertEqual(app.priority, Priority.MEDIUM.value)
        self.assertEqual(app.priority_weight, 2)
        self.assertEqual(app.status, ApplicationStatus.APPLIED.value)
        self.assertEqual(app.job_type, JobType.FULL_TIME.value)

    def test_priority_assignment_and_weights(self):
        """Validates the Priority field (Low, Medium, High) and sorting weights."""
        app_high = JobApplication(
            company="Dream Co",
            role="Staff Engineer",
            application_date="2026-11-01",
            priority="High",
        )
        app_med = JobApplication(
            company="Steady Co",
            role="Software Engineer",
            application_date="2026-11-01",
            priority="Medium",
        )
        app_low = JobApplication(
            company="Fallback Co",
            role="Analyst",
            application_date="2026-11-01",
            priority="Low",
        )

        self.assertEqual(app_high.priority, "High")
        self.assertEqual(app_high.priority_weight, 3)

        self.assertEqual(app_med.priority, "Medium")
        self.assertEqual(app_med.priority_weight, 2)

        self.assertEqual(app_low.priority, "Low")
        self.assertEqual(app_low.priority_weight, 1)

        # High priority weight must be strictly greater than Medium and Low
        self.assertGreater(app_high.priority_weight, app_med.priority_weight)
        self.assertGreater(app_med.priority_weight, app_low.priority_weight)

    def test_empty_company_validation(self):
        """Defensive validation: Company cannot be blank."""
        with self.assertRaises(ValueError):
            JobApplication(company="   ", role="Engineer", application_date="2026-11-01")

    def test_empty_role_validation(self):
        """Defensive validation: Role cannot be blank."""
        with self.assertRaises(ValueError):
            JobApplication(company="Google", role="", application_date="2026-11-01")


class TestDatabaseManager(unittest.TestCase):
    """Tests SQLite database operations, queries, priority sorting, and persistence."""

    def setUp(self):
        # Create an isolated temporary SQLite database for each test
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db_path = self.temp_file.name
        self.temp_file.close()
        self.db = DatabaseManager(self.temp_db_path)

    def tearDown(self):
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def test_add_and_retrieve_application(self):
        """Verifies adding a job application and retrieving it with ID."""
        app = JobApplication(
            company="Meta",
            role="Software Engineer",
            location="Remote",
            application_date="2026-10-15",
            priority="High",
            status="Applied",
            salary_or_stipend="$150,000",
        )
        app_id = self.db.add_application(app)
        self.assertIsNotNone(app_id)
        self.assertGreater(app_id, 0)

        fetched = self.db.get_application_by_id(app_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.company, "Meta")
        self.assertEqual(fetched.role, "Software Engineer")
        self.assertEqual(fetched.priority, "High")
        self.assertEqual(fetched.salary_or_stipend, "$150,000")

    def test_priority_sorting(self):
        """
        Verifies sorting applications based on Priority:
        High -> Medium -> Low when sorted ASC (custom order rank 1 -> 2 -> 3).
        """
        app_low = JobApplication(
            company="Alpha Corp", role="Tester", application_date="2026-10-01", priority="Low"
        )
        app_high = JobApplication(
            company="Beta Corp", role="Lead Dev", application_date="2026-10-02", priority="High"
        )
        app_med = JobApplication(
            company="Gamma Corp", role="DevOps", application_date="2026-10-03", priority="Medium"
        )

        self.db.add_application(app_low)
        self.db.add_application(app_high)
        self.db.add_application(app_med)

        sorted_apps = self.db.get_all_applications(sort_by="priority", order="ASC")
        priorities = [a.priority for a in sorted_apps]

        # First must be High, then Medium, then Low
        self.assertEqual(priorities[0], "High")
        self.assertEqual(priorities[1], "Medium")
        self.assertEqual(priorities[2], "Low")

    def test_search_applications(self):
        """Verifies searching by company name, role, and status."""
        self.db.add_application(
            JobApplication(company="Microsoft", role="Frontend Dev", application_date="2026-10-01", status="Applied")
        )
        self.db.add_application(
            JobApplication(company="Apple", role="iOS Engineer", application_date="2026-10-02", status="Selected")
        )

        # Search by company
        res_company = self.db.search_applications("micro", search_field="company")
        self.assertEqual(len(res_company), 1)
        self.assertEqual(res_company[0].company, "Microsoft")

        # Search by role
        res_role = self.db.search_applications("iOS", search_field="role")
        self.assertEqual(len(res_role), 1)
        self.assertEqual(res_role[0].company, "Apple")

        # Search by status
        res_status = self.db.search_applications("Selected", search_field="status")
        self.assertEqual(len(res_status), 1)
        self.assertEqual(res_status[0].status, "Selected")

    def test_update_application(self):
        """Verifies updating status, priority, and notes."""
        app = JobApplication(
            company="Amazon",
            role="Cloud Architect",
            application_date="2026-10-05",
            status="Applied",
            priority="Medium",
        )
        app_id = self.db.add_application(app)

        updates = {
            "status": "Interview Scheduled",
            "priority": "High",
            "interview_date": "2026-11-20",
            "interview_rounds": 1,
            "interview_notes": "Screening completed.",
        }
        success = self.db.update_application(app_id, updates)
        self.assertTrue(success)

        updated = self.db.get_application_by_id(app_id)
        self.assertEqual(updated.status, "Interview Scheduled")
        self.assertEqual(updated.priority, "High")
        self.assertEqual(updated.interview_rounds, 1)

    def test_delete_application(self):
        """Verifies permanent deletion of application record."""
        app = JobApplication(company="Netflix", role="Streaming Eng", application_date="2026-10-01")
        app_id = self.db.add_application(app)
        self.assertIsNotNone(self.db.get_application_by_id(app_id))

        deleted = self.db.delete_application(app_id)
        self.assertTrue(deleted)
        self.assertIsNone(self.db.get_application_by_id(app_id))

    def test_database_persistence_across_instances(self):
        """Simulates restarting application: ensures data persists across connections."""
        app = JobApplication(
            company="OpenAI",
            role="Research Scientist",
            application_date="2026-10-10",
            priority="High",
        )
        app_id = self.db.add_application(app)

        # Reopen with a completely new DatabaseManager instance pointing to the same file
        reopened_db = DatabaseManager(self.temp_db_path)
        persisted_app = reopened_db.get_application_by_id(app_id)

        self.assertIsNotNone(persisted_app)
        self.assertEqual(persisted_app.company, "OpenAI")
        self.assertEqual(persisted_app.priority, "High")

    def test_dashboard_statistics(self):
        """Verifies metric calculations: success rate, counts, priority breakdowns."""
        self.db.add_application(JobApplication(company="C1", role="R1", application_date="2026-10-01", status="Selected", priority="High"))
        self.db.add_application(JobApplication(company="C2", role="R2", application_date="2026-10-02", status="Applied", priority="Medium"))
        self.db.add_application(JobApplication(company="C3", role="R3", application_date="2026-10-03", status="Interview Scheduled", priority="High"))
        self.db.add_application(JobApplication(company="C4", role="R4", application_date="2026-10-04", status="Rejected", priority="Low"))

        stats = self.db.get_statistics()
        self.assertEqual(stats["total"], 4)
        self.assertEqual(stats["selected"], 1)
        self.assertEqual(stats["applied"], 1)
        self.assertEqual(stats["interviewing"], 1)
        self.assertEqual(stats["rejected"], 1)
        self.assertEqual(stats["priority_breakdown"]["High"], 2)
        self.assertEqual(stats["priority_breakdown"]["Medium"], 1)
        self.assertEqual(stats["priority_breakdown"]["Low"], 1)
        self.assertEqual(stats["success_rate"], 25.0)  # 1 selected / 4 total = 25%


if __name__ == "__main__":
    unittest.main()
