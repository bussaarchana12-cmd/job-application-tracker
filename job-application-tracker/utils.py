"""
utils.py
CLI presentation, table formatting, input validation, and color utilities.
Built using standard library modules for maximum portability.
"""

import os
import re
import sys
from datetime import datetime
from typing import List, Optional, Tuple


class Colors:
    """ANSI color escape codes with automatic fallback."""
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    # Disable colors if terminal is non-interactive or Windows without VT100
    @classmethod
    def disable(cls):
        cls.HEADER = ""
        cls.BLUE = ""
        cls.CYAN = ""
        cls.GREEN = ""
        cls.YELLOW = ""
        cls.RED = ""
        cls.MAGENTA = ""
        cls.BOLD = ""
        cls.UNDERLINE = ""
        cls.DIM = ""
        cls.RESET = ""


# Auto-check terminal support
if not sys.stdout.isatty() or os.name == "nt" and "WT_SESSION" not in os.environ:
    # Keep light formatting or enable if modern terminal
    pass


def clear_screen() -> None:
    """Clears the terminal screen smoothly."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner(subtitle: str = "Student & Job Seeker Portfolio Edition") -> None:
    """Displays a modern ASCII banner for the CLI."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════════╗
║                   JOB APPLICATION TRACKER (OOP)                       ║
║        {subtitle.center(59)}      ║
╚═══════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


def print_section(title: str) -> None:
    """Prints a styled section header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}▶ {title.upper()}{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * (len(title) + 4)}{Colors.RESET}")


def format_table(headers: List[str], rows: List[List[str]], alignments: Optional[List[str]] = None) -> str:
    """
    Renders a clean, Unicode box-drawing table.
    Works independently without external packages.
    """
    if not headers:
        return ""

    num_cols = len(headers)
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in str_rows:
        for idx in range(min(num_cols, len(row))):
            col_widths[idx] = max(col_widths[idx], len(row[idx]))

    # Padding
    pad = 1
    total_widths = [w + (pad * 2) for w in col_widths]

    # Border elements
    top = "┌" + "┬".join("─" * w for w in total_widths) + "┐"
    header_sep = "├" + "┼".join("─" * w for w in total_widths) + "┤"
    bottom = "└" + "┴".join("─" * w for w in total_widths) + "┘"

    # Format header
    header_line = "│"
    for i, h in enumerate(headers):
        align = alignments[i] if alignments and i < len(alignments) else "<"
        cell = f" {h} ".center(total_widths[i]) if align == "^" else f" {h} ".ljust(total_widths[i])
        header_line += f"{Colors.BOLD}{cell}{Colors.RESET}│"

    # Format rows
    data_lines = []
    for row in str_rows:
        line = "│"
        for i in range(num_cols):
            val = row[i] if i < len(row) else ""
            align = alignments[i] if alignments and i < len(alignments) else "<"
            if align == ">":
                cell = f" {val} ".rjust(total_widths[i])
            elif align == "^":
                cell = f" {val} ".center(total_widths[i])
            else:
                cell = f" {val} ".ljust(total_widths[i])

            # Apply subtle coloring for Status and Priority
            if val in ("High",):
                cell_colored = f"{Colors.RED}{Colors.BOLD}{cell}{Colors.RESET}"
            elif val in ("Medium",):
                cell_colored = f"{Colors.YELLOW}{cell}{Colors.RESET}"
            elif val in ("Low",):
                cell_colored = f"{Colors.DIM}{cell}{Colors.RESET}"
            elif val in ("Selected",):
                cell_colored = f"{Colors.GREEN}{Colors.BOLD}{cell}{Colors.RESET}"
            elif val in ("Interview Scheduled",):
                cell_colored = f"{Colors.CYAN}{Colors.BOLD}{cell}{Colors.RESET}"
            elif val in ("Rejected",):
                cell_colored = f"{Colors.RED}{cell}{Colors.RESET}"
            else:
                cell_colored = cell

            line += cell_colored + "│"
        data_lines.append(line)

    return "\n".join([top, header_line, header_sep] + data_lines + [bottom])


def prompt_non_empty(label: str, default: Optional[str] = None) -> str:
    """Prompts the user for a required string, re-prompting if blank."""
    default_hint = f" [{default}]" if default else ""
    while True:
        try:
            val = input(f"{Colors.BOLD}{label}{default_hint}:{Colors.RESET} ").strip()
            if not val and default is not None:
                return default
            if val:
                return val
            print(f"  {Colors.RED}✖ Error: This field cannot be empty. Please enter a value.{Colors.RESET}")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            raise


def prompt_date(label: str = "Application Date (YYYY-MM-DD)", default: str = "today") -> str:
    """Validates date format YYYY-MM-DD or defaults to current date."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    default_val = today_str if default == "today" else default

    while True:
        val = input(f"{Colors.BOLD}{label} [{default_val}]:{Colors.RESET} ").strip()
        if not val:
            return default_val
        if val.lower() == "today":
            return today_str

        # Match YYYY-MM-DD
        if re.match(r"^\d{4}-\d{2}-\d{2}$", val):
            try:
                datetime.strptime(val, "%Y-%m-%d")
                return val
            except ValueError:
                print(f"  {Colors.RED}✖ Invalid calendar date. Use YYYY-MM-DD (e.g. 2026-11-02).{Colors.RESET}")
        else:
            print(f"  {Colors.RED}✖ Format must be YYYY-MM-DD. (Or press Enter for today: {today_str}){Colors.RESET}")


def prompt_priority(default: str = "Medium") -> str:
    """Interactive priority picker (High, Medium, Low)."""
    print(f"\n{Colors.BOLD}Select Priority Level:{Colors.RESET}")
    print(f"  {Colors.RED}1) High{Colors.RESET}   (Top dream companies, pressing deadlines)")
    print(f"  {Colors.YELLOW}2) Medium{Colors.RESET} (Standard strong interest)")
    print(f"  {Colors.DIM}3) Low{Colors.RESET}    (Backup applications, exploratory)")

    choice_map = {"1": "High", "2": "Medium", "3": "Low", "high": "High", "medium": "Medium", "low": "Low"}
    while True:
        choice = input(f"{Colors.BOLD}Enter choice (1-3) [{default}]:{Colors.RESET} ").strip()
        if not choice:
            return default
        if choice in choice_map:
            return choice_map[choice]
        print(f"  {Colors.RED}✖ Please select 1 (High), 2 (Medium), or 3 (Low).{Colors.RESET}")


def prompt_job_type(default: str = "Full-time") -> str:
    """Interactive job type picker."""
    print(f"\n{Colors.BOLD}Select Job Type:{Colors.RESET}")
    print("  1) Internship")
    print("  2) Full-time")
    print("  3) Part-time")
    print("  4) Contract")

    mapping = {"1": "Internship", "2": "Full-time", "3": "Part-time", "4": "Contract"}
    while True:
        choice = input(f"{Colors.BOLD}Enter choice (1-4) [{default}]:{Colors.RESET} ").strip()
        if not choice:
            return default
        if choice in mapping:
            return mapping[choice]
        print(f"  {Colors.RED}✖ Invalid selection. Pick a number between 1 and 4.{Colors.RESET}")


def prompt_status(default: str = "Applied") -> str:
    """Interactive status selector."""
    print(f"\n{Colors.BOLD}Select Application Status:{Colors.RESET}")
    print("  1) Applied")
    print(f"  {Colors.CYAN}2) Interview Scheduled{Colors.RESET}")
    print(f"  {Colors.GREEN}3) Selected (Offer){Colors.RESET}")
    print(f"  {Colors.RED}4) Rejected{Colors.RESET}")
    print(f"  {Colors.YELLOW}5) Pending{Colors.RESET}")

    mapping = {
        "1": "Applied",
        "2": "Interview Scheduled",
        "3": "Selected",
        "4": "Rejected",
        "5": "Pending",
    }
    while True:
        choice = input(f"{Colors.BOLD}Enter choice (1-5) [{default}]:{Colors.RESET} ").strip()
        if not choice:
            return default
        if choice in mapping:
            return mapping[choice]
        print(f"  {Colors.RED}✖ Invalid selection. Pick a number between 1 and 5.{Colors.RESET}")


def prompt_confirmation(message: str, default_no: bool = True) -> bool:
    """Asks for confirmation (yes/no) before executing destructive operations."""
    hint = " [y/N]" if default_no else " [Y/n]"
    while True:
        resp = input(f"{Colors.YELLOW}{Colors.BOLD}⚠ {message}{hint}:{Colors.RESET} ").strip().lower()
        if not resp:
            return not default_no
        if resp in ("y", "yes"):
            return True
        if resp in ("n", "no"):
            return False
        print(f"  {Colors.RED}✖ Please answer 'yes' (y) or 'no' (n).{Colors.RESET}")


def render_progress_bar(percentage: float, width: int = 24) -> str:
    """Renders a visual ASCII progress bar."""
    filled_len = int(round(width * percentage / 100))
    bar = "█" * filled_len + "░" * (width - filled_len)
    return f"[{bar}] {percentage:.1f}%"
