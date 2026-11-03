"""
dashboard.py
Dashboard class responsible for computing metrics, analytics, and visual reports.
Demonstrates:
- Statistical aggregation and KPI calculations
- Clean report generation and ASCII visualization
- Object-Oriented aggregation pattern
"""

from typing import Dict, Any
from database import DatabaseManager
from utils import Colors, format_table, render_progress_bar


class Dashboard:
    """
    Renders analytics, KPIs, funnel statistics, and priority distributions.
    """

    def __init__(self, db_manager: DatabaseManager):
        self._db_manager = db_manager

    def get_data(self) -> Dict[str, Any]:
        """Fetches up-to-date metrics from the DatabaseManager."""
        return self._db_manager.get_statistics()

    def display(self) -> None:
        """
        Prints the comprehensive job search analytics dashboard.
        """
        stats = self.get_data()
        total = stats["total"]

        print(f"\n{Colors.BOLD}{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}║                    APPLICATIONS ANALYTICS DASHBOARD                   ║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════╝{Colors.RESET}")

        if total == 0:
            print(f"\n  {Colors.YELLOW}ℹ No applications recorded yet. Start by adding a job application!{Colors.RESET}\n")
            return

        # Top KPI Cards
        print(f"\n{Colors.BOLD}── 📊 KEY PERFORMANCE INDICATORS ────────────────────────────────────────{Colors.RESET}")
        print(f"  • Total Applications Submitted:  {Colors.BOLD}{total}{Colors.RESET}")
        print(f"  • Active in Pipeline:            {Colors.BOLD}{stats['applied'] + stats['interviewing'] + stats['pending']}{Colors.RESET}")
        print(f"  • Interview Conversion Rate:     {Colors.CYAN}{render_progress_bar(stats['interview_rate'])}{Colors.RESET}")
        print(f"  • Final Selection (Offer) Rate:  {Colors.GREEN}{render_progress_bar(stats['success_rate'])}{Colors.RESET}")

        # Status Funnel Table
        print(f"\n{Colors.BOLD}── 📈 PIPELINE STATUS BREAKDOWN ────────────────────────────────────────{Colors.RESET}")
        status_headers = ["Status Stage", "Count", "Percentage", "Funnel Visual"]
        status_rows = []

        stages = [
            ("Applied", stats["applied"], Colors.BLUE),
            ("Interview Scheduled", stats["interviewing"], Colors.CYAN),
            ("Selected (Offer)", stats["selected"], Colors.GREEN),
            ("Pending", stats["pending"], Colors.YELLOW),
            ("Rejected", stats["rejected"], Colors.RED),
        ]

        for label, count, color in stages:
            pct = (count / total * 100.0) if total > 0 else 0.0
            mini_bar = "█" * int(round(pct / 5)) + "░" * (20 - int(round(pct / 5)))
            status_rows.append([
                label,
                str(count),
                f"{pct:.1f}%",
                f"[{mini_bar}]",
            ])

        print(format_table(status_headers, status_rows, alignments=["<", ">", ">", "<"]))

        # Priority Breakdown Table
        print(f"\n{Colors.BOLD}── ⭐ PRIORITY DISTRIBUTION ─────────────────────────────────────────────{Colors.RESET}")
        p_stats = stats["priority_breakdown"]
        priority_headers = ["Priority Level", "Count", "Share of Total", "Focus Recommendation"]
        priority_rows = [
            [
                "High",
                str(p_stats["High"]),
                f"{(p_stats['High'] / total * 100.0):.1f}%",
                "Top target! Follow up weekly and prepare custom interview stories.",
            ],
            [
                "Medium",
                str(p_stats["Medium"]),
                f"{(p_stats['Medium'] / total * 100.0):.1f}%",
                "Core applications. Maintain standard networking cadence.",
            ],
            [
                "Low",
                str(p_stats["Low"]),
                f"{(p_stats['Low'] / total * 100.0):.1f}%",
                "Backup options. Re-evaluate if priority shifts.",
            ],
        ]
        print(format_table(priority_headers, priority_rows, alignments=["<", ">", ">", "<"]))

        # Job Type Breakdown
        job_types = stats.get("job_type_breakdown", {})
        if job_types:
            print(f"\n{Colors.BOLD}── 💼 EMPLOYMENT TYPE DISTRIBUTION ─────────────────────────────────────{Colors.RESET}")
            jt_headers = ["Job Type", "Applications", "Share"]
            jt_rows = [
                [jt, str(cnt), f"{(cnt / total * 100.0):.1f}%"]
                for jt, cnt in job_types.items()
            ]
            print(format_table(jt_headers, jt_rows, alignments=["<", ">", ">"]))

        print(f"\n{Colors.DIM}Last updated: Real-time query against SQLite database.{Colors.RESET}\n")
