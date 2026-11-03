"""
models.py
Object-Oriented Domain Models for Job Application Tracker.
Demonstrates:
- Inheritance (BaseRecord -> JobApplication)
- Polymorphism (summary representation)
- Encapsulation (validated properties, private members)
- Type safety and Enum enforcement
"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class JobType(str, Enum):
    """Enumeration of accepted job employment types."""
    INTERNSHIP = "Internship"
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"

    @classmethod
    def from_string(cls, value: str) -> "JobType":
        lookup = {
            "1": cls.INTERNSHIP,
            "internship": cls.INTERNSHIP,
            "2": cls.FULL_TIME,
            "full-time": cls.FULL_TIME,
            "full time": cls.FULL_TIME,
            "fulltime": cls.FULL_TIME,
            "3": cls.PART_TIME,
            "part-time": cls.PART_TIME,
            "part time": cls.PART_TIME,
            "4": cls.CONTRACT,
            "contract": cls.CONTRACT,
        }
        normalized = value.strip().lower()
        if normalized in lookup:
            return lookup[normalized]
        for member in cls:
            if member.value.lower() == normalized:
                return member
        return cls.FULL_TIME


class ApplicationStatus(str, Enum):
    """Enumeration of job application lifecycle stages."""
    APPLIED = "Applied"
    INTERVIEW_SCHEDULED = "Interview Scheduled"
    SELECTED = "Selected"
    REJECTED = "Rejected"
    PENDING = "Pending"

    @classmethod
    def from_string(cls, value: str) -> "ApplicationStatus":
        lookup = {
            "1": cls.APPLIED,
            "applied": cls.APPLIED,
            "2": cls.INTERVIEW_SCHEDULED,
            "interview": cls.INTERVIEW_SCHEDULED,
            "interview scheduled": cls.INTERVIEW_SCHEDULED,
            "3": cls.SELECTED,
            "selected": cls.SELECTED,
            "offer": cls.SELECTED,
            "4": cls.REJECTED,
            "rejected": cls.REJECTED,
            "5": cls.PENDING,
            "pending": cls.PENDING,
        }
        normalized = value.strip().lower()
        if normalized in lookup:
            return lookup[normalized]
        for member in cls:
            if member.value.lower() == normalized:
                return member
        return cls.APPLIED


class Priority(str, Enum):
    """
    Application Priority level (High, Medium, Low).
    Allows job seekers to prioritize dream companies or urgent deadlines.
    """
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

    @property
    def weight(self) -> int:
        """Numeric rank for sorting: High (3) > Medium (2) > Low (1)."""
        mapping = {"High": 3, "Medium": 2, "Low": 1}
        return mapping.get(self.value, 2)

    @classmethod
    def from_string(cls, value: str) -> "Priority":
        lookup = {
            "1": cls.HIGH,
            "high": cls.HIGH,
            "h": cls.HIGH,
            "2": cls.MEDIUM,
            "medium": cls.MEDIUM,
            "med": cls.MEDIUM,
            "m": cls.MEDIUM,
            "3": cls.LOW,
            "low": cls.LOW,
            "l": cls.LOW,
        }
        normalized = str(value).strip().lower()
        if normalized in lookup:
            return lookup[normalized]
        for member in cls:
            if member.value.lower() == normalized:
                return member
        return cls.MEDIUM


class BaseRecord(ABC):
    """
    Abstract Base Class for tracker entities.
    Enforces OOP design with common ID handling and polymorphic summary.
    """

    def __init__(self, record_id: Optional[int] = None, created_at: Optional[str] = None):
        self._id = record_id
        self._created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        if self._id is not None:
            raise ValueError("Record ID is immutable once assigned.")
        self._id = int(value)

    @property
    def created_at(self) -> str:
        return self._created_at

    @abstractmethod
    def summary(self) -> str:
        """Polymorphic summary string for CLI representations."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert record to dictionary for persistence/serialization."""
        pass


class JobApplication(BaseRecord):
    """
    Job Application Model with complete encapsulation and data validation.
    Includes Company, Role, Location, Date, Type, Status, Priority, Salary,
    Description, Link, Notes, and Interview details.
    """

    def __init__(
        self,
        company: str,
        role: str,
        application_date: str,
        location: str = "Remote",
        job_type: str = JobType.FULL_TIME.value,
        status: str = ApplicationStatus.APPLIED.value,
        priority: str = Priority.MEDIUM.value,
        salary_or_stipend: str = "Not Disclosed",
        job_description: str = "",
        link: str = "",
        notes: str = "",
        interview_date: Optional[str] = None,
        interview_rounds: int = 0,
        interview_notes: str = "",
        record_id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        super().__init__(record_id=record_id, created_at=created_at)

        # Encapsulated attributes with validated assignments
        self.company = company
        self.role = role
        self.location = location or "Remote"
        self.application_date = application_date
        self.job_type = job_type
        self.status = status
        self.priority = priority
        self.salary_or_stipend = salary_or_stipend or "Not Disclosed"
        self.job_description = job_description or ""
        self.link = link or ""
        self.notes = notes or ""
        self.interview_date = interview_date or "None"
        self.interview_rounds = int(interview_rounds or 0)
        self.interview_notes = interview_notes or ""
        self._updated_at = updated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Property: company
    @property
    def company(self) -> str:
        return self._company

    @company.setter
    def company(self, value: str) -> None:
        if not value or not str(value).strip():
            raise ValueError("Company name cannot be blank.")
        self._company = str(value).strip()

    # Property: role
    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, value: str) -> None:
        if not value or not str(value).strip():
            raise ValueError("Job role cannot be blank.")
        self._role = str(value).strip()

    # Property: application_date
    @property
    def application_date(self) -> str:
        return self._application_date

    @application_date.setter
    def application_date(self, value: str) -> None:
        cleaned = str(value).strip()
        if not cleaned:
            cleaned = datetime.now().strftime("%Y-%m-%d")
        self._application_date = cleaned

    # Property: job_type
    @property
    def job_type(self) -> str:
        return self._job_type.value

    @job_type.setter
    def job_type(self, value: Any) -> None:
        if isinstance(value, JobType):
            self._job_type = value
        else:
            self._job_type = JobType.from_string(str(value))

    # Property: status
    @property
    def status(self) -> str:
        return self._status.value

    @status.setter
    def status(self, value: Any) -> None:
        if isinstance(value, ApplicationStatus):
            self._status = value
        else:
            self._status = ApplicationStatus.from_string(str(value))

    # Property: priority (Low, Medium, High)
    @property
    def priority(self) -> str:
        return self._priority.value

    @priority.setter
    def priority(self, value: Any) -> None:
        if isinstance(value, Priority):
            self._priority = value
        else:
            self._priority = Priority.from_string(str(value))

    @property
    def priority_weight(self) -> int:
        """Returns numeric weight for sorting (High=3, Medium=2, Low=1)."""
        return self._priority.weight

    @property
    def updated_at(self) -> str:
        return self._updated_at

    def touch(self) -> None:
        """Updates the modified timestamp."""
        self._updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Polymorphic implementation
    def summary(self) -> str:
        app_id = f"#{self.id}" if self.id else "New"
        return f"[{app_id}] {self.company} - {self.role} | Priority: {self.priority} | Status: {self.status}"

    def to_dict(self) -> Dict[str, Any]:
        """Serializes model into dictionary mapping to database columns."""
        return {
            "id": self.id,
            "company": self.company,
            "role": self.role,
            "location": self.location,
            "application_date": self.application_date,
            "job_type": self.job_type,
            "status": self.status,
            "priority": self.priority,
            "salary_or_stipend": self.salary_or_stipend,
            "job_description": self.job_description,
            "link": self.link,
            "notes": self.notes,
            "interview_date": self.interview_date,
            "interview_rounds": self.interview_rounds,
            "interview_notes": self.interview_notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_row(cls, row: Any) -> "JobApplication":
        """
        Factory method to reconstruct a JobApplication object from a SQLite row or dictionary.
        """
        # Supports sqlite3.Row or dict
        data = dict(row) if hasattr(row, "keys") else row
        return cls(
            company=data.get("company", "Unknown"),
            role=data.get("role", "Unknown"),
            location=data.get("location", "Remote"),
            application_date=data.get("application_date", datetime.now().strftime("%Y-%m-%d")),
            job_type=data.get("job_type", JobType.FULL_TIME.value),
            status=data.get("status", ApplicationStatus.APPLIED.value),
            priority=data.get("priority", Priority.MEDIUM.value),
            salary_or_stipend=data.get("salary_or_stipend", "Not Disclosed"),
            job_description=data.get("job_description", ""),
            link=data.get("link", ""),
            notes=data.get("notes", ""),
            interview_date=data.get("interview_date"),
            interview_rounds=data.get("interview_rounds", 0),
            interview_notes=data.get("interview_notes", ""),
            record_id=data.get("id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
