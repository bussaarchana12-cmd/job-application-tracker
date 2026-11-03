"""
tracker.py
JobTracker coordinator class implementing business logic and user operations.
Demonstrates:
- Object-Oriented design and loose coupling with DatabaseManager
- Priority-based listing and sorting (High -> Medium -> Low)
- Interview tracking and notes management
- Input validation and defensive error handling
"""

from typing import Optional, List
from database import DatabaseManager
from dashboard import Dashboard
from models import JobApplication, Priority, ApplicationStatus, JobType
from utils import (
    Colors,
    format_table,
    prompt_non_empty,
    prompt_date,
    prompt_priority,
    prompt_job_type,
    prompt_status,
    prompt_confirmation,
    print_section,
)


class JobTracker:
    """
    Main business coordinator for managing applications, interviews,
    searching, filtering, sorting, and reporting.
    """

    def __init__(self, db_manager: DatabaseManager):
        self._db = db_manager
        self._dashboard = Dashboard(db_manager)

    @property
    def db(self) -> DatabaseManager:
        return self._db

    @property
    def dashboard(self) -> Dashboard:
        return self._dashboard

    # ─────────────────────────────────────────────────────────────
    # FEATURE 1: ADD JOB APPLICATION
    # ─────────────────────────────────────────────────────────────
    def add_application(self) -> Optional[JobApplication]:
        """Collects application fields from the user, validates, and stores in SQLite."""
        print_section("Add New Job Application")
        print(f"{Colors.DIM}Enter application details below. Press Enter to accept defaults.{Colors.RESET}\n")

        try:
            company = prompt_non_empty("Company Name")
            role = prompt_non_empty("Job Role / Position Title")
            location = input(f"{Colors.BOLD}Job Location (e.g. Remote, New York, NY) [Remote]:{Colors.RESET} ").strip() or "Remote"
            app_date = prompt_date("Application Date (YYYY-MM-DD)")
            job_type = prompt_job_type()
            priority = prompt_priority(default="Medium")
            status = prompt_status(default="Applied")
            salary = input(f"{Colors.BOLD}Salary or Stipend (e.g. $95,000/yr or $35/hr) [Not Disclosed]:{Colors.RESET} ").strip() or "Not Disclosed"
            link = input(f"{Colors.BOLD}Application URL / Company Website [None]:{Colors.RESET} ").strip()
            notes = input(f"{Colors.BOLD}Initial Notes / Referral info [None]:{Colors.RESET} ").strip()
            desc = input(f"{Colors.BOLD}Short Job Description or Tech Stack [Optional]:{Colors.RESET} ").strip()

            # If status is set to Interview Scheduled, capture interview info immediately
            interview_date = None
            interview_rounds = 0
            interview_notes = ""
            if status == ApplicationStatus.INTERVIEW_SCHEDULED.value:
                interview_date = prompt_date("Scheduled Interview Date")
                interview_rounds = 1
                interview_notes = input(f"{Colors.BOLD}Round details (e.g. Technical Screening with Engineering Manager):{Colors.RESET} ").strip()

            # Construct OOP Model
            application = JobApplication(
                company=company,
                role=role,
                location=location,
                application_date=app_date,
                job_type=job_type,
                status=status,
                priority=priority,
                salary_or_stipend=salary,
                job_description=desc,
                link=link,
                notes=notes,
                interview_date=interview_date,
                interview_rounds=interview_rounds,
                interview_notes=interview_notes,
            )

            # Persist to SQLite
            new_id = self._db.add_application(application)
            print(f"\n{Colors.GREEN}{Colors.BOLD}✔ Successfully added application #{new_id} for {company} ({role})!{Colors.RESET}")
            print(f"  Priority set to: {Colors.BOLD}{priority}{Colors.RESET} | Status: {Colors.BOLD}{status}{Colors.RESET}\n")
            return application

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Action aborted by user.{Colors.RESET}")
            return None

    # ─────────────────────────────────────────────────────────────
    # FEATURE 2: VIEW APPLICATIONS WITH PRIORITY SORTING
    # ─────────────────────────────────────────────────────────────
    def view_applications(self, sort_by: str = "id", order: str = "ASC") -> None:
        """
        Displays all applications in a clean table with configurable sorting.
        Supports sorting by Priority (High -> Medium -> Low), Date, Company, Status, or ID.
        """
        apps = self._db.get_all_applications(sort_by=sort_by, order=order)
        if not apps:
            print(f"\n  {Colors.YELLOW}No job applications found in the database.{Colors.RESET}\n")
            return

        headers = ["ID", "Company", "Job Role", "Type", "Priority", "Status", "Date", "Location"]
        rows = []
        for app in apps:
            rows.append([
                str(app.id),
                app.company,
                app.role,
                app.job_type,
                app.priority,
                app.status,
                app.application_date,
                app.location,
            ])

        sort_label = f"Sorted by: {sort_by.upper()} ({order.upper()})"
        if sort_by == "priority":
            sort_label += " [High ➔ Medium ➔ Low]"

        print_section(f"All Job Applications ({len(apps)} Total) — {sort_label}")
        print(format_table(headers, rows, alignments=["^", "<", "<", "^", "^", "<", "^", "<"]))
        print(f"{Colors.DIM}Use option 'View Individual Application Details' to see full notes and interview logs.{Colors.RESET}\n")

    def view_applications_menu(self) -> None:
        """Interactive viewing submenu providing multiple sorting strategies."""
        while True:
            print(f"\n{Colors.BOLD}{Colors.CYAN}--- View & Sort Applications ---{Colors.RESET}")
            print(f"  1) View All (Default order: by ID)")
            print(f"  {Colors.BOLD}2) ⭐ Sort by Priority (High ➔ Medium ➔ Low){Colors.RESET}")
            print(f"  3) Sort by Priority (Low ➔ Medium ➔ High)")
            print(f"  4) Sort by Application Date (Newest first)")
            print(f"  5) Sort by Company Name (A-Z)")
            print(f"  6) Sort by Status")
            print(f"  7) Inspect Individual Application Details (by ID)")
            print(f"  8) Back to Main Menu")

            choice = input(f"{Colors.BOLD}Select an option (1-8):{Colors.RESET} ").strip()
            if choice == "1":
                self.view_applications(sort_by="id", order="ASC")
            elif choice == "2":
                self.view_applications(sort_by="priority", order="ASC")
            elif choice == "3":
                self.view_applications(sort_by="priority", order="DESC")
            elif choice == "4":
                self.view_applications(sort_by="date", order="DESC")
            elif choice == "5":
                self.view_applications(sort_by="company", order="ASC")
            elif choice == "6":
                self.view_applications(sort_by="status", order="ASC")
            elif choice == "7":
                self.view_single_application_detail()
            elif choice in ("8", "q", "exit", "b"):
                break
            else:
                print(f"  {Colors.RED}✖ Invalid option. Please select 1 through 8.{Colors.RESET}")

    def view_single_application_detail(self) -> None:
        """Displays full comprehensive profile of a single application."""
        app_id_str = input(f"{Colors.BOLD}Enter Application ID to inspect:{Colors.RESET} ").strip()
        if not app_id_str.isdigit():
            print(f"  {Colors.RED}✖ Error: Application ID must be an integer.{Colors.RESET}")
            return

        app = self._db.get_application_by_id(int(app_id_str))
        if not app:
            print(f"  {Colors.RED}✖ No application found with ID #{app_id_str}.{Colors.RESET}")
            return

        print(f"\n{Colors.BOLD}{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}║ APPLICATION PROFILE: #{app.id} - {app.company.upper()} {Colors.RESET}".ljust(72) + f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════╝{Colors.RESET}")
        print(f"  • Company:              {Colors.BOLD}{app.company}{Colors.RESET}")
        print(f"  • Job Role / Title:     {Colors.BOLD}{app.role}{Colors.RESET}")
        print(f"  • Employment Type:      {app.job_type}")
        print(f"  • Location:             {app.location}")
        print(f"  • Priority:             {Colors.BOLD}{app.priority}{Colors.RESET}")
        print(f"  • Current Status:       {Colors.BOLD}{app.status}{Colors.RESET}")
        print(f"  • Application Date:     {app.application_date}")
        print(f"  • Compensation:         {app.salary_or_stipend}")
        print(f"  • Application Link:     {app.link or 'N/A'}")
        print(f"  • Job Description:      {app.job_description or 'N/A'}")
        print(f"  • General Notes:        {app.notes or 'N/A'}")
        print(f"\n{Colors.BOLD}── INTERVIEW TRACKING ──────────────────────────────────────────────────{Colors.RESET}")
        print(f"  • Scheduled Date:       {app.interview_date or 'No interview scheduled yet'}")
        print(f"  • Rounds Completed:     {app.interview_rounds}")
        print(f"  • Interview Feedback:   {app.interview_notes or 'No feedback notes recorded yet'}")
        print(f"\n{Colors.DIM}Record Created: {app.created_at} | Last Modified: {app.updated_at}{Colors.RESET}\n")

    # ─────────────────────────────────────────────────────────────
    # FEATURE 3: SEARCH APPLICATIONS
    # ─────────────────────────────────────────────────────────────
    def search_applications_menu(self) -> None:
        """Interactive search menu by company, role, status, or priority."""
        print_section("Search Job Applications")
        print("  1) Search by Company Name")
        print("  2) Search by Job Role")
        print("  3) Search by Status")
        print(f"  4) Search by Priority (High / Medium / Low)")
        print("  5) Search Across All Fields")

        choice = input(f"{Colors.BOLD}Select search method (1-5):{Colors.RESET} ").strip()
        field_map = {
            "1": "company",
            "2": "role",
            "3": "status",
            "4": "priority",
            "5": "all",
        }
        search_field = field_map.get(choice, "all")
        query = prompt_non_empty(f"Enter search query for '{search_field}'")

        results = self._db.search_applications(query, search_field=search_field)
        if not results:
            print(f"\n  {Colors.YELLOW}No applications matched '{query}'.{Colors.RESET}\n")
            return

        headers = ["ID", "Company", "Job Role", "Priority", "Status", "Date", "Location"]
        rows = [
            [str(a.id), a.company, a.role, a.priority, a.status, a.application_date, a.location]
            for a in results
        ]

        print(f"\n{Colors.GREEN}✔ Found {len(results)} matching application(s):{Colors.RESET}")
        print(format_table(headers, rows, alignments=["^", "<", "<", "^", "<", "^", "<"]))
        print()

    # ─────────────────────────────────────────────────────────────
    # FEATURE 4: UPDATE APPLICATIONS
    # ─────────────────────────────────────────────────────────────
    def update_application_menu(self) -> None:
        """Updates company details, status, priority, or notes."""
        print_section("Update Job Application")
        app_id_str = input(f"{Colors.BOLD}Enter Application ID to update:{Colors.RESET} ").strip()
        if not app_id_str.isdigit():
            print(f"  {Colors.RED}✖ Error: Application ID must be an integer.{Colors.RESET}")
            return

        app = self._db.get_application_by_id(int(app_id_str))
        if not app:
            print(f"  {Colors.RED}✖ No application found with ID #{app_id_str}.{Colors.RESET}")
            return

        print(f"\nSelected: {Colors.BOLD}#{app.id} {app.company} ({app.role}){Colors.RESET}")
        print(f"Current Status: {app.status} | Priority: {app.priority} | Salary: {app.salary_or_stipend}")

        print(f"\n{Colors.BOLD}What would you like to update?{Colors.RESET}")
        print("  1) Application Status (Applied / Interview / Selected / Rejected / Pending)")
        print(f"  2) ⭐ Priority Level (High / Medium / Low)")
        print("  3) Company Name")
        print("  4) Job Role")
        print("  5) Location")
        print("  6) Salary or Stipend")
        print("  7) Notes / Links")
        print("  8) All Primary Fields")
        print("  9) Cancel")

        field_choice = input(f"{Colors.BOLD}Enter choice (1-9):{Colors.RESET} ").strip()
        updates = {}

        if field_choice == "1":
            new_status = prompt_status(default=app.status)
            updates["status"] = new_status
            if new_status == ApplicationStatus.INTERVIEW_SCHEDULED.value and app.interview_date in ("None", None, ""):
                updates["interview_date"] = prompt_date("Schedule Interview Date")
        elif field_choice == "2":
            new_priority = prompt_priority(default=app.priority)
            updates["priority"] = new_priority
        elif field_choice == "3":
            updates["company"] = prompt_non_empty("New Company Name", default=app.company)
        elif field_choice == "4":
            updates["role"] = prompt_non_empty("New Job Role", default=app.role)
        elif field_choice == "5":
            updates["location"] = input(f"New Location [{app.location}]: ").strip() or app.location
        elif field_choice == "6":
            updates["salary_or_stipend"] = input(f"New Salary/Stipend [{app.salary_or_stipend}]: ").strip() or app.salary_or_stipend
        elif field_choice == "7":
            updates["notes"] = input(f"New Notes [{app.notes}]: ").strip() or app.notes
            updates["link"] = input(f"New Link [{app.link}]: ").strip() or app.link
        elif field_choice == "8":
            updates["company"] = prompt_non_empty("Company Name", default=app.company)
            updates["role"] = prompt_non_empty("Job Role", default=app.role)
            updates["location"] = input(f"Location [{app.location}]: ").strip() or app.location
            updates["priority"] = prompt_priority(default=app.priority)
            updates["status"] = prompt_status(default=app.status)
            updates["salary_or_stipend"] = input(f"Salary [{app.salary_or_stipend}]: ").strip() or app.salary_or_stipend
            updates["notes"] = input(f"Notes [{app.notes}]: ").strip() or app.notes
        elif field_choice == "9":
            print("Update cancelled.")
            return
        else:
            print(f"  {Colors.RED}✖ Invalid selection.{Colors.RESET}")
            return

        if updates:
            success = self._db.update_application(app.id, updates)
            if success:
                print(f"\n{Colors.GREEN}{Colors.BOLD}✔ Application #{app.id} updated successfully!{Colors.RESET}\n")
            else:
                print(f"\n{Colors.RED}✖ Failed to update application record.{Colors.RESET}\n")

    # ─────────────────────────────────────────────────────────────
    # FEATURE 5: DELETE APPLICATION
    # ─────────────────────────────────────────────────────────────
    def delete_application_flow(self) -> None:
        """Deletes an application by ID after explicit user confirmation."""
        print_section("Delete Job Application")
        app_id_str = input(f"{Colors.BOLD}Enter Application ID to delete:{Colors.RESET} ").strip()
        if not app_id_str.isdigit():
            print(f"  {Colors.RED}✖ Error: Application ID must be an integer.{Colors.RESET}")
            return

        app_id = int(app_id_str)
        app = self._db.get_application_by_id(app_id)
        if not app:
            print(f"  {Colors.RED}✖ No application found with ID #{app_id}.{Colors.RESET}")
            return

        print(f"\nTarget Record: {Colors.BOLD}#{app.id} - {app.company} ({app.role}){Colors.RESET}")
        print(f"Applied on: {app.application_date} | Status: {app.status} | Priority: {app.priority}")

        confirmed = prompt_confirmation(
            f"Are you sure you want to permanently delete application #{app.id}?",
            default_no=True,
        )

        if confirmed:
            success = self._db.delete_application(app_id)
            if success:
                print(f"\n{Colors.GREEN}{Colors.BOLD}✔ Application #{app_id} has been permanently deleted.{Colors.RESET}\n")
            else:
                print(f"\n{Colors.RED}✖ Could not delete record.{Colors.RESET}\n")
        else:
            print(f"\n{Colors.YELLOW}Deletion cancelled. No changes made.{Colors.RESET}\n")

    # ─────────────────────────────────────────────────────────────
    # FEATURE 7: INTERVIEW MANAGEMENT
    # ─────────────────────────────────────────────────────────────
    def manage_interview_flow(self) -> None:
        """Stores interview dates, rounds, feedback notes, and questions."""
        print_section("Interview Management")
        app_id_str = input(f"{Colors.BOLD}Enter Application ID to manage interview:{Colors.RESET} ").strip()
        if not app_id_str.isdigit():
            print(f"  {Colors.RED}✖ Error: Application ID must be an integer.{Colors.RESET}")
            return

        app = self._db.get_application_by_id(int(app_id_str))
        if not app:
            print(f"  {Colors.RED}✖ No application found with ID #{app_id_str}.{Colors.RESET}")
            return

        print(f"\nTarget: {Colors.BOLD}#{app.id} {app.company} - {app.role}{Colors.RESET}")
        print(f"Current Interview Date:  {app.interview_date}")
        print(f"Rounds Completed So Far: {app.interview_rounds}")
        print(f"Existing Interview Notes: {app.interview_notes or 'None'}")

        print(f"\n{Colors.BOLD}Options:{Colors.RESET}")
        print("  1) Schedule / Reschedule Interview Date")
        print("  2) Increment Round & Log Interview Feedback")
        print("  3) Mark as Selected (Job Offer Received)")
        print("  4) Mark as Rejected")
        print("  5) Return to Main Menu")

        opt = input(f"{Colors.BOLD}Enter choice (1-5):{Colors.RESET} ").strip()
        updates = {}

        if opt == "1":
            date_val = prompt_date("New Interview Date (YYYY-MM-DD)")
            updates["interview_date"] = date_val
            updates["status"] = ApplicationStatus.INTERVIEW_SCHEDULED.value
        elif opt == "2":
            new_rounds = app.interview_rounds + 1
            print(f"\nLogging Round #{new_rounds}...")
            round_type = input("Round Type (e.g. Phone Screen, Coding, System Design, Behavioral): ").strip()
            notes = input("Key questions asked, feedback, or prep takeaways: ").strip()
            appended_notes = f"Round {new_rounds} ({round_type}): {notes}"
            if app.interview_notes:
                appended_notes = f"{app.interview_notes} | {appended_notes}"
            updates["interview_rounds"] = new_rounds
            updates["interview_notes"] = appended_notes
            updates["status"] = ApplicationStatus.INTERVIEW_SCHEDULED.value
        elif opt == "3":
            updates["status"] = ApplicationStatus.SELECTED.value
            offer_note = input("Offer details or congrats note: ").strip()
            if offer_note:
                updates["notes"] = f"{app.notes} [OFFER: {offer_note}]"
        elif opt == "4":
            updates["status"] = ApplicationStatus.REJECTED.value
            feedback = input("Feedback received (if any): ").strip()
            if feedback:
                updates["interview_notes"] = f"{app.interview_notes} [REJECTION FEEDBACK: {feedback}]"
        elif opt == "5":
            return
        else:
            print(f"  {Colors.RED}✖ Invalid selection.{Colors.RESET}")
            return

        if updates:
            self._db.update_application(app.id, updates)
            print(f"\n{Colors.GREEN}{Colors.BOLD}✔ Interview record updated for #{app.id} {app.company}!{Colors.RESET}\n")

    # ─────────────────────────────────────────────────────────────
    # FEATURE 6: DASHBOARD DISPLAY
    # ─────────────────────────────────────────────────────────────
    def show_dashboard(self) -> None:
        """Renders analytics dashboard."""
        self._dashboard.display()
