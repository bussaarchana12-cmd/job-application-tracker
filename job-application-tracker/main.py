#!/usr/bin/env python3
"""
main.py
Main entry point for the Job Application Tracker CLI application.
Demonstrates:
- Clean modular application entry
- Intuitive numbered command menu
- Graceful shutdown and interrupt handling
- Initial seed data option for fast portfolio demonstrations
"""

import sys
import os
from database import DatabaseManager
from tracker import JobTracker
from models import JobApplication, JobType, ApplicationStatus, Priority
from utils import Colors, print_banner, clear_screen


def seed_sample_data(db: DatabaseManager) -> None:
    """Seeds realistic demonstration data with varied priorities and statuses."""
    samples = [
        JobApplication(
            company="Google",
            role="Software Engineering Intern",
            location="Mountain View, CA (Hybrid)",
            application_date="2026-10-15",
            job_type=JobType.INTERNSHIP.value,
            status=ApplicationStatus.INTERVIEW_SCHEDULED.value,
            priority=Priority.HIGH.value,
            salary_or_stipend="$58/hour + Relocation",
            job_description="Backend systems in Python and Go, distributed data pipelines.",
            link="https://careers.google.com/jobs/results/12345",
            notes="Referred by alumni Jane Doe from ACM chapter.",
            interview_date="2026-11-12",
            interview_rounds=2,
            interview_notes="Passed Round 1 coding (Graph algorithms). Round 2 scheduled with Team Lead.",
        ),
        JobApplication(
            company="Stripe",
            role="Backend Software Engineer",
            location="Remote (US)",
            application_date="2026-10-20",
            job_type=JobType.FULL_TIME.value,
            status=ApplicationStatus.APPLIED.value,
            priority=Priority.HIGH.value,
            salary_or_stipend="$145,000 - $170,000/yr",
            job_description="Financial infrastructure and payment routing API engines.",
            link="https://stripe.com/jobs/eng-backend",
            notes="Applied through company portal after reviewing engineering blog.",
        ),
        JobApplication(
            company="Spotify",
            role="Data Engineer Intern",
            location="New York, NY",
            application_date="2026-10-02",
            job_type=JobType.INTERNSHIP.value,
            status=ApplicationStatus.SELECTED.value,
            priority=Priority.HIGH.value,
            salary_or_stipend="$52/hour",
            job_description="Recommendation algorithm metrics and real-time streaming data.",
            link="https://www.lifeatspotify.com/jobs/data-eng",
            notes="Received written offer on 2026-10-28! Deadline to respond is 2026-11-20.",
            interview_date="2026-10-18",
            interview_rounds=3,
            interview_notes="Completed Behavioral, Live SQL/Python pipeline, and System Architecture.",
        ),
        JobApplication(
            company="Shopify",
            role="Junior Python Developer",
            location="Remote",
            application_date="2026-10-25",
            job_type=JobType.FULL_TIME.value,
            status=ApplicationStatus.PENDING.value,
            priority=Priority.MEDIUM.value,
            salary_or_stipend="$95,000/yr",
            job_description="Merchant tooling APIs and inventory synchronization microservices.",
            link="https://shopify.com/careers/jr-dev",
            notes="Reached out to hiring manager on LinkedIn.",
        ),
        JobApplication(
            company="TechCorp Labs",
            role="Full Stack Developer",
            location="Austin, TX",
            application_date="2026-09-28",
            job_type=JobType.FULL_TIME.value,
            status=ApplicationStatus.REJECTED.value,
            priority=Priority.LOW.value,
            salary_or_stipend="$80,000/yr",
            job_description="Internal administration dashboards.",
            link="https://techcorplabs.example.com",
            notes="Position cancelled due to internal restructuring.",
        ),
    ]

    for item in samples:
        db.add_application(item)


def main():
    """Main program execution loop."""
    # Ensure current directory is in Python path for local imports
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    # Initialize Database & Tracker
    db_manager = DatabaseManager()
    tracker = JobTracker(db_manager)

    # Auto-seed if running fresh for instant demonstration
    all_apps = db_manager.get_all_applications()
    if len(all_apps) == 0:
        seed_sample_data(db_manager)

    while True:
        try:
            print_banner("OOP Python & SQLite CLI")
            print(f"{Colors.BOLD}Main Navigation Menu:{Colors.RESET}")
            print(f"  {Colors.BOLD}1){Colors.RESET} Add Job Application")
            print(f"  {Colors.BOLD}2){Colors.RESET} View Applications (with {Colors.YELLOW}Priority Sorting{Colors.RESET})")
            print(f"  {Colors.BOLD}3){Colors.RESET} Search Applications (Company, Role, Status, Priority)")
            print(f"  {Colors.BOLD}4){Colors.RESET} Update Application")
            print(f"  {Colors.BOLD}5){Colors.RESET} Delete Application (with confirmation)")
            print(f"  {Colors.BOLD}6){Colors.RESET} 📊 Dashboard & Analytics")
            print(f"  {Colors.BOLD}7){Colors.RESET} 🎙️ Interview Management")
            print(f"  {Colors.BOLD}8){Colors.RESET} 🔄 Seed Demo Applications")
            print(f"  {Colors.BOLD}9){Colors.RESET} 🚪 Exit Application")
            print(f"{Colors.DIM}─────────────────────────────────────────────────────────────────────────{Colors.RESET}")

            choice = input(f"{Colors.BOLD}Select an option (1-9):{Colors.RESET} ").strip()

            if choice == "1":
                tracker.add_application()
                input(f"\n{Colors.DIM}Press Enter to return to menu...{Colors.RESET}")
            elif choice == "2":
                tracker.view_applications_menu()
            elif choice == "3":
                tracker.search_applications_menu()
                input(f"\n{Colors.DIM}Press Enter to return to menu...{Colors.RESET}")
            elif choice == "4":
                tracker.update_application_menu()
                input(f"\n{Colors.DIM}Press Enter to return to menu...{Colors.RESET}")
            elif choice == "5":
                tracker.delete_application_flow()
                input(f"\n{Colors.DIM}Press Enter to return to menu...{Colors.RESET}")
            elif choice == "6":
                tracker.show_dashboard()
                input(f"\n{Colors.DIM}Press Enter to return to menu...{Colors.RESET}")
            elif choice == "7":
                tracker.manage_interview_flow()
                input(f"\n{Colors.DIM}Press Enter to return to menu...{Colors.RESET}")
            elif choice == "8":
                seed_sample_data(db_manager)
                print(f"\n{Colors.GREEN}{Colors.BOLD}✔ Added sample applications for testing.{Colors.RESET}")
                input(f"\n{Colors.DIM}Press Enter to return to menu...{Colors.RESET}")
            elif choice in ("9", "exit", "quit", "q"):
                print(f"\n{Colors.CYAN}{Colors.BOLD}Thank you for using Job Application Tracker. Good luck with your applications!{Colors.RESET}\n")
                sys.exit(0)
            else:
                print(f"\n{Colors.RED}✖ Invalid choice '{choice}'. Please enter a number between 1 and 9.{Colors.RESET}\n")

        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Session interrupted. Exiting safely...{Colors.RESET}")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Colors.RED}✖ Unexpected Error: {e}{Colors.RESET}")
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")


if __name__ == "__main__":
    main()
