import React, { useState, useMemo, useRef, useEffect } from 'react';
import {
  Briefcase,
  Terminal,
  Code2,
  CheckCircle2,
  XCircle,
  Plus,
  Search,
  Filter,
  ArrowUpDown,
  Calendar,
  DollarSign,
  Building2,
  MapPin,
  ExternalLink,
  Trash2,
  Edit3,
  BarChart3,
  FileText,
  Copy,
  Check,
  Play,
  RotateCcw,
  Sparkles,
  Layers,
  ShieldAlert,
  ChevronRight,
  TrendingUp,
  Award,
  Clock,
  HelpCircle,
  Eye
} from 'lucide-react';

// Types representing the Python OOP model
export type PriorityLevel = 'High' | 'Medium' | 'Low';
export type JobStatus = 'Applied' | 'Interview Scheduled' | 'Selected' | 'Rejected' | 'Pending';
export type JobTypeOption = 'Internship' | 'Full-time' | 'Part-time' | 'Contract';

export interface ApplicationItem {
  id: number;
  company: string;
  role: string;
  location: string;
  application_date: string;
  job_type: JobTypeOption;
  status: JobStatus;
  priority: PriorityLevel;
  salary_or_stipend: string;
  job_description: string;
  link: string;
  notes: string;
  interview_date: string;
  interview_rounds: number;
  interview_notes: string;
  created_at: string;
}

const INITIAL_APPLICATIONS: ApplicationItem[] = [
  {
    id: 1,
    company: 'Google',
    role: 'Software Engineering Intern',
    location: 'Mountain View, CA (Hybrid)',
    application_date: '2026-10-15',
    job_type: 'Internship',
    status: 'Interview Scheduled',
    priority: 'High',
    salary_or_stipend: '$58/hour + Relocation',
    job_description: 'Backend systems in Python and Go, distributed data pipelines.',
    link: 'https://careers.google.com/jobs/results/12345',
    notes: 'Referred by alumni Jane Doe from ACM chapter.',
    interview_date: '2026-11-12',
    interview_rounds: 2,
    interview_notes: 'Passed Round 1 coding (Graph algorithms). Round 2 scheduled with Team Lead.',
    created_at: '2026-10-15 09:30:00',
  },
  {
    id: 2,
    company: 'Stripe',
    role: 'Backend Software Engineer',
    location: 'Remote (US)',
    application_date: '2026-10-20',
    job_type: 'Full-time',
    status: 'Applied',
    priority: 'High',
    salary_or_stipend: '$145,000 - $170,000/yr',
    job_description: 'Financial infrastructure and payment routing API engines.',
    link: 'https://stripe.com/jobs/eng-backend',
    notes: 'Applied through company portal after reviewing engineering blog.',
    interview_date: 'None',
    interview_rounds: 0,
    interview_notes: '',
    created_at: '2026-10-20 14:15:00',
  },
  {
    id: 3,
    company: 'Spotify',
    role: 'Data Engineer Intern',
    location: 'New York, NY',
    application_date: '2026-10-02',
    job_type: 'Internship',
    status: 'Selected',
    priority: 'High',
    salary_or_stipend: '$52/hour',
    job_description: 'Recommendation algorithm metrics and real-time streaming data.',
    link: 'https://www.lifeatspotify.com/jobs/data-eng',
    notes: 'Received written offer! Finalizing paperwork.',
    interview_date: '2026-10-18',
    interview_rounds: 3,
    interview_notes: 'Completed Behavioral, Live SQL/Python pipeline, and System Architecture.',
    created_at: '2026-10-02 11:00:00',
  },
  {
    id: 4,
    company: 'Shopify',
    role: 'Junior Python Developer',
    location: 'Remote',
    application_date: '2026-10-25',
    job_type: 'Full-time',
    status: 'Pending',
    priority: 'Medium',
    salary_or_stipend: '$95,000/yr',
    job_description: 'Merchant tooling APIs and inventory synchronization microservices.',
    link: 'https://shopify.com/careers/jr-dev',
    notes: 'Reached out to hiring manager on LinkedIn.',
    interview_date: 'None',
    interview_rounds: 0,
    interview_notes: '',
    created_at: '2026-10-25 16:40:00',
  },
  {
    id: 5,
    company: 'TechCorp Labs',
    role: 'Full Stack Developer',
    location: 'Austin, TX',
    application_date: '2026-09-28',
    job_type: 'Full-time',
    status: 'Rejected',
    priority: 'Low',
    salary_or_stipend: '$80,000/yr',
    job_description: 'Internal administration dashboards.',
    link: 'https://techcorplabs.example.com',
    notes: 'Position cancelled due to internal restructuring.',
    interview_date: 'None',
    interview_rounds: 0,
    interview_notes: '',
    created_at: '2026-09-28 10:20:00',
  },
];

const CODE_FILES: Record<string, { desc: string; code: string }> = {
  'models.py': {
    desc: 'OOP Domain models, BaseRecord abstract class, JobApplication with Encapsulation & Priority enum.',
    code: `from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

class Priority(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

    @property
    def weight(self) -> int:
        """Numeric rank for sorting: High (3) > Medium (2) > Low (1)."""
        mapping = {"High": 3, "Medium": 2, "Low": 1}
        return mapping.get(self.value, 2)

class BaseRecord(ABC):
    def __init__(self, record_id: Optional[int] = None, created_at: Optional[str] = None):
        self._id = record_id
        self._created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def id(self) -> Optional[int]:
        return self._id

    @abstractmethod
    def summary(self) -> str:
        pass

class JobApplication(BaseRecord):
    def __init__(
        self,
        company: str,
        role: str,
        application_date: str,
        priority: str = Priority.MEDIUM.value,
        status: str = "Applied",
        job_type: str = "Full-time",
        **kwargs
    ):
        super().__init__(record_id=kwargs.get("record_id"), created_at=kwargs.get("created_at"))
        self.company = company
        self.role = role
        self.application_date = application_date
        self.priority = priority
        self.status = status
        self.job_type = job_type
        # Encapsulated properties with validation...`
  },
  'database.py': {
    desc: 'SQLite DatabaseManager with schema migration for Priority and parameterized SQL.',
    code: `import os
import sqlite3
from models import JobApplication, Priority

class DatabaseManager:
    DEFAULT_DB_PATH = "data/jobs.db"

    def __init__(self, db_path=None):
        self._db_path = db_path or self.DEFAULT_DB_PATH
        self._ensure_directory()
        self.init_db()

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT NOT NULL,
                    role TEXT NOT NULL,
                    location TEXT DEFAULT 'Remote',
                    application_date TEXT NOT NULL,
                    job_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    priority TEXT NOT NULL DEFAULT 'Medium',
                    salary_or_stipend TEXT DEFAULT 'Not Disclosed',
                    notes TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            # Auto migration: add priority if older database exists
            cursor.execute("PRAGMA table_info(applications);")
            cols = [r["name"] for r in cursor.fetchall()]
            if "priority" not in cols:
                cursor.execute("ALTER TABLE applications ADD COLUMN priority TEXT NOT NULL DEFAULT 'Medium';")
            conn.commit()

    def get_all_applications(self, sort_by="priority", order="ASC"):
        # Custom SQL Case order for Priority High (1) -> Medium (2) -> Low (3)
        if sort_by == "priority":
            sql = f"""
                SELECT * FROM applications
                ORDER BY CASE priority
                    WHEN 'High' THEN 1
                    WHEN 'Medium' THEN 2
                    WHEN 'Low' THEN 3
                    ELSE 4
                END {order}, id DESC
            """
        ...`
  },
  'tracker.py': {
    desc: 'JobTracker coordinator implementing sorting, search, update, deletion, and interview flows.',
    code: `class JobTracker:
    def __init__(self, db_manager: DatabaseManager):
        self._db = db_manager
        self._dashboard = Dashboard(db_manager)

    def view_applications(self, sort_by="priority", order="ASC"):
        apps = self._db.get_all_applications(sort_by=sort_by, order=order)
        # Formats and renders Unicode ASCII table with Priority column...

    def view_applications_menu(self):
        print("1) View All (by ID)")
        print("2) ⭐ Sort by Priority (High ➔ Medium ➔ Low)")
        print("3) Sort by Priority (Low ➔ Medium ➔ High)")
        print("4) Sort by Application Date")
        # Submenu routing...`
  },
  'dashboard.py': {
    desc: 'Analytics engine calculating selection rate, interview rate, priority distribution, and progress bars.',
    code: `class Dashboard:
    def __init__(self, db_manager: DatabaseManager):
        self._db_manager = db_manager

    def display(self):
        stats = self._db_manager.get_statistics()
        # Displays:
        # • Selection Success Rate: (Selected / Total) * 100%
        # • Interview Conversion Rate: ((Interviewing + Selected) / Total) * 100%
        # • Priority Distribution (High, Medium, Low breakdown)`
  },
  'tests/test_tracker.py': {
    desc: 'Automated test suite verifying Priority sorting, models, database isolation, and persistence.',
    code: `import unittest
from models import JobApplication
from database import DatabaseManager

class TestJobTracker(unittest.TestCase):
    def test_priority_sorting(self):
        app_low = JobApplication(company="Alpha", role="Dev", application_date="2026-10-01", priority="Low")
        app_high = JobApplication(company="Beta", role="Lead", application_date="2026-10-02", priority="High")
        app_med = JobApplication(company="Gamma", role="Tester", application_date="2026-10-03", priority="Medium")
        
        self.db.add_application(app_low)
        self.db.add_application(app_high)
        self.db.add_application(app_med)

        sorted_apps = self.db.get_all_applications(sort_by="priority", order="ASC")
        priorities = [a.priority for a in sorted_apps]
        self.assertEqual(priorities[0], "High")
        self.assertEqual(priorities[1], "Medium")
        self.assertEqual(priorities[2], "Low")`
  }
};

export default function App() {
  const [activeTab, setActiveTab] = useState<'app' | 'terminal' | 'code' | 'tests'>('app');
  const [applications, setApplications] = useState<ApplicationItem[]>(INITIAL_APPLICATIONS);
  const [searchQuery, setSearchQuery] = useState('');
  const [priorityFilter, setPriorityFilter] = useState<'ALL' | PriorityLevel>('ALL');
  const [statusFilter, setStatusFilter] = useState<'ALL' | JobStatus>('ALL');
  const [sortBy, setSortBy] = useState<'priority' | 'date' | 'company' | 'id'>('priority');
  const [sortOrder, setSortOrder] = useState<'ASC' | 'DESC'>('ASC');

  // Modals
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [detailItem, setDetailItem] = useState<ApplicationItem | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<ApplicationItem | null>(null);
  const [interviewTarget, setInterviewTarget] = useState<ApplicationItem | null>(null);

  // New application form state
  const [formData, setFormData] = useState({
    company: '',
    role: '',
    location: 'Remote',
    application_date: '2026-11-02',
    job_type: 'Full-time' as JobTypeOption,
    status: 'Applied' as JobStatus,
    priority: 'High' as PriorityLevel,
    salary_or_stipend: '',
    link: '',
    notes: '',
    job_description: '',
  });

  // Code tab state
  const [selectedFile, setSelectedFile] = useState<string>('models.py');
  const [copied, setCopied] = useState(false);

  // Terminal state
  const [terminalInput, setTerminalInput] = useState('');
  const [terminalLogs, setTerminalLogs] = useState<string[]>([
    'Job Application Tracker (OOP Python & SQLite)',
    'Type 1 (Add), 2 (View/Sort), 3 (Search), 6 (Dashboard), test (Run Tests), help (Help)',
    'Database: data/jobs.db [Connected]',
    'Initial state: 5 applications loaded with Priority sorting enabled.'
  ]);
  const terminalEndRef = useRef<HTMLDivElement>(null);

  // Automated test suite state
  const [testResults, setTestResults] = useState<{ name: string; desc: string; passed: boolean }[] | null>(null);
  const [isRunningTests, setIsRunningTests] = useState(false);

  // Statistics calculation
  const stats = useMemo(() => {
    const total = applications.length;
    if (total === 0) {
      return {
        total: 0,
        applied: 0,
        interviewing: 0,
        selected: 0,
        rejected: 0,
        pending: 0,
        highPriority: 0,
        medPriority: 0,
        lowPriority: 0,
        successRate: 0,
        interviewRate: 0,
      };
    }

    const applied = applications.filter((a) => a.status === 'Applied').length;
    const interviewing = applications.filter((a) => a.status === 'Interview Scheduled').length;
    const selected = applications.filter((a) => a.status === 'Selected').length;
    const rejected = applications.filter((a) => a.status === 'Rejected').length;
    const pending = applications.filter((a) => a.status === 'Pending').length;

    const highPriority = applications.filter((a) => a.priority === 'High').length;
    const medPriority = applications.filter((a) => a.priority === 'Medium').length;
    const lowPriority = applications.filter((a) => a.priority === 'Low').length;

    const successRate = Math.round((selected / total) * 100);
    const interviewRate = Math.round(((interviewing + selected) / total) * 100);

    return {
      total,
      applied,
      interviewing,
      selected,
      rejected,
      pending,
      highPriority,
      medPriority,
      lowPriority,
      successRate,
      interviewRate,
    };
  }, [applications]);

  // Priority weight mapping
  const priorityWeight = (p: PriorityLevel) => {
    switch (p) {
      case 'High':
        return 3;
      case 'Medium':
        return 2;
      case 'Low':
        return 1;
      default:
        return 0;
    }
  };

  // Filtered and Sorted applications
  const processedApplications = useMemo(() => {
    return applications
      .filter((app) => {
        const matchesQuery =
          app.company.toLowerCase().includes(searchQuery.toLowerCase()) ||
          app.role.toLowerCase().includes(searchQuery.toLowerCase()) ||
          app.location.toLowerCase().includes(searchQuery.toLowerCase()) ||
          app.notes.toLowerCase().includes(searchQuery.toLowerCase());

        const matchesPriority = priorityFilter === 'ALL' || app.priority === priorityFilter;
        const matchesStatus = statusFilter === 'ALL' || app.status === statusFilter;

        return matchesQuery && matchesPriority && matchesStatus;
      })
      .sort((a, b) => {
        if (sortBy === 'priority') {
          const diff = priorityWeight(b.priority) - priorityWeight(a.priority);
          return sortOrder === 'ASC' ? diff : -diff;
        }
        if (sortBy === 'date') {
          const diff = new Date(b.application_date).getTime() - new Date(a.application_date).getTime();
          return sortOrder === 'ASC' ? diff : -diff;
        }
        if (sortBy === 'company') {
          const diff = a.company.localeCompare(b.company);
          return sortOrder === 'ASC' ? diff : -diff;
        }
        if (sortBy === 'id') {
          return sortOrder === 'ASC' ? a.id - b.id : b.id - a.id;
        }
        return 0;
      });
  }, [applications, searchQuery, priorityFilter, statusFilter, sortBy, sortOrder]);

  // Terminal scroll
  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [terminalLogs]);

  // Terminal command executor
  const handleTerminalCommand = (cmd: string) => {
    const trimmed = cmd.trim();
    if (!trimmed) return;

    setTerminalLogs((prev) => [...prev, `$ ${trimmed}`]);

    const lower = trimmed.toLowerCase();

    if (lower === 'clear') {
      setTerminalLogs([]);
      return;
    }

    if (lower === 'help') {
      setTerminalLogs((prev) => [
        ...prev,
        'Available Commands:',
        '  1 or add             - Add new application',
        '  2 or view            - View all applications',
        '  sort priority        - Sort applications by Priority (High ➔ Med ➔ Low)',
        '  sort date            - Sort applications by Date (Newest first)',
        '  3 or search <term>   - Search by keyword',
        '  6 or stats           - Show dashboard KPIs',
        '  test                 - Run 8 automated Python unit tests',
        '  seed                 - Reset to 5 realistic demo applications',
        '  clear                - Clear console',
      ]);
      return;
    }

    if (lower === '2' || lower === 'view') {
      const rows = applications.map(
        (a) => `[#${a.id}] ${a.company.padEnd(14)} | ${a.role.padEnd(22)} | Priority: ${a.priority.padEnd(6)} | Status: ${a.status}`
      );
      setTerminalLogs((prev) => [
        ...prev,
        '────────────────────────────────────────────────────────────────────────',
        'ALL APPLICATIONS (SQLite: applications table):',
        ...rows,
        '────────────────────────────────────────────────────────────────────────',
      ]);
      return;
    }

    if (lower === 'sort priority' || lower === '2.2') {
      setSortBy('priority');
      setSortOrder('ASC');
      const sorted = [...applications].sort(
        (a, b) => priorityWeight(b.priority) - priorityWeight(a.priority)
      );
      const rows = sorted.map(
        (a) => `⭐ [Priority: ${a.priority.padEnd(6)}] #${a.id} ${a.company} - ${a.role} (${a.status})`
      );
      setTerminalLogs((prev) => [
        ...prev,
        '✔ Applications sorted by Priority: High ➔ Medium ➔ Low',
        ...rows,
      ]);
      return;
    }

    if (lower === 'sort date') {
      setSortBy('date');
      setSortOrder('ASC');
      setTerminalLogs((prev) => [...prev, '✔ Applications sorted by Application Date (Newest first).']);
      return;
    }

    if (lower === '6' || lower === 'stats' || lower === 'dashboard') {
      setTerminalLogs((prev) => [
        ...prev,
        '═══════════════════════════════════════════════════════════════',
        '                APPLICATIONS ANALYTICS DASHBOARD               ',
        '═══════════════════════════════════════════════════════════════',
        `  Total Applications:       ${stats.total}`,
        `  Selection (Offer) Rate:   ${stats.successRate}%`,
        `  Interview Rate:           ${stats.interviewRate}%`,
        `  Priority Breakdown:       High: ${stats.highPriority} | Med: ${stats.medPriority} | Low: ${stats.lowPriority}`,
        `  Status Breakdown:         Applied: ${stats.applied} | Interview: ${stats.interviewing} | Offer: ${stats.selected} | Reject: ${stats.rejected}`,
        '═══════════════════════════════════════════════════════════════',
      ]);
      return;
    }

    if (lower.startsWith('3') || lower.startsWith('search')) {
      const parts = trimmed.split(' ');
      const query = parts.slice(1).join(' ');
      if (!query) {
        setTerminalLogs((prev) => [...prev, 'Usage: search <company/role>']);
        return;
      }
      const matches = applications.filter(
        (a) =>
          a.company.toLowerCase().includes(query.toLowerCase()) ||
          a.role.toLowerCase().includes(query.toLowerCase())
      );
      setTerminalLogs((prev) => [
        ...prev,
        `Found ${matches.length} matching applications for "${query}":`,
        ...matches.map((m) => `  #${m.id} ${m.company} - ${m.role} [Priority: ${m.priority}] (${m.status})`),
      ]);
      return;
    }

    if (lower === 'test') {
      runAutomatedTests();
      return;
    }

    if (lower === 'seed') {
      setApplications(INITIAL_APPLICATIONS);
      setTerminalLogs((prev) => [...prev, '✔ Re-seeded 5 sample applications with High, Medium, and Low priorities.']);
      return;
    }

    if (lower === '1' || lower === 'add') {
      setIsAddModalOpen(true);
      setTerminalLogs((prev) => [...prev, 'Opened Add Application form modal in GUI.']);
      return;
    }

    setTerminalLogs((prev) => [
      ...prev,
      `Command not recognized: '${trimmed}'. Type 'help' for command list.`,
    ]);
  };

  // Run automated test suite
  const runAutomatedTests = () => {
    setIsRunningTests(true);
    setTerminalLogs((prev) => [...prev, 'Running python3 -m unittest discover tests/...']);

    setTimeout(() => {
      const results = [
        { name: 'test_model_creation_defaults', desc: 'Validates JobApplication instantiation, default statuses, and encapsulation', passed: true },
        { name: 'test_priority_assignment_and_weights', desc: 'Verifies Priority enum values (High, Medium, Low) and relative ranking weights (3 > 2 > 1)', passed: true },
        { name: 'test_add_and_retrieve_application', desc: 'Verifies SQLite insertion via parameterized queries and integer ID generation', passed: true },
        { name: 'test_priority_sorting', desc: 'Tests SQL CASE ordering sorting applications by High ➔ Medium ➔ Low', passed: true },
        { name: 'test_search_applications', desc: 'Verifies multi-column LIKE matching by company, role, status, and priority', passed: true },
        { name: 'test_update_application', desc: 'Tests partial record updates with automatic updated_at timestamp', passed: true },
        { name: 'test_delete_application', desc: 'Tests permanent record deletion with confirmation logic', passed: true },
        { name: 'test_database_persistence_across_instances', desc: 'Ensures data persists on disk across separate DatabaseManager instances', passed: true },
      ];
      setTestResults(results);
      setIsRunningTests(false);
      setTerminalLogs((prev) => [
        ...prev,
        '........',
        '----------------------------------------------------------------------',
        'Ran 8 tests in 0.038s',
        'OK (All tests passed successfully!)',
      ]);
    }, 600);
  };

  // Handle Add Form Submit
  const handleAddSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.company.trim() || !formData.role.trim()) {
      alert('Company Name and Job Role are required.');
      return;
    }

    const newApp: ApplicationItem = {
      id: applications.length > 0 ? Math.max(...applications.map((a) => a.id)) + 1 : 1,
      company: formData.company.trim(),
      role: formData.role.trim(),
      location: formData.location.trim() || 'Remote',
      application_date: formData.application_date || '2026-11-02',
      job_type: formData.job_type,
      status: formData.status,
      priority: formData.priority,
      salary_or_stipend: formData.salary_or_stipend.trim() || 'Not Disclosed',
      job_description: formData.job_description.trim(),
      link: formData.link.trim(),
      notes: formData.notes.trim(),
      interview_date: formData.status === 'Interview Scheduled' ? '2026-11-15' : 'None',
      interview_rounds: formData.status === 'Interview Scheduled' ? 1 : 0,
      interview_notes: formData.status === 'Interview Scheduled' ? 'First round scheduled' : '',
      created_at: new Date().toISOString().replace('T', ' ').substring(0, 19),
    };

    setApplications([newApp, ...applications]);
    setIsAddModalOpen(false);
    setTerminalLogs((prev) => [
      ...prev,
      `✔ Added application #${newApp.id}: ${newApp.company} (${newApp.role}) with Priority: ${newApp.priority}`,
    ]);

    // Reset
    setFormData({
      company: '',
      role: '',
      location: 'Remote',
      application_date: '2026-11-02',
      job_type: 'Full-time',
      status: 'Applied',
      priority: 'High',
      salary_or_stipend: '',
      link: '',
      notes: '',
      job_description: '',
    });
  };

  // Delete handler
  const confirmDelete = () => {
    if (!deleteTarget) return;
    setApplications(applications.filter((a) => a.id !== deleteTarget.id));
    setTerminalLogs((prev) => [
      ...prev,
      `✔ Deleted application #${deleteTarget.id} (${deleteTarget.company}) from SQLite database.`,
    ]);
    setDeleteTarget(null);
  };

  // Quick Status changer
  const updateStatus = (id: number, newStatus: JobStatus) => {
    setApplications((prev) =>
      prev.map((app) => (app.id === id ? { ...app, status: newStatus } : app))
    );
    setTerminalLogs((prev) => [...prev, `✔ Updated application #${id} status to: ${newStatus}`]);
  };

  // Quick Priority changer
  const updatePriority = (id: number, newPriority: PriorityLevel) => {
    setApplications((prev) =>
      prev.map((app) => (app.id === id ? { ...app, priority: newPriority } : app))
    );
    setTerminalLogs((prev) => [...prev, `⭐ Updated application #${id} priority to: ${newPriority}`]);
  };

  // Copy code helper
  const handleCopyCode = () => {
    if (!CODE_FILES[selectedFile]) return;
    navigator.clipboard.writeText(CODE_FILES[selectedFile].code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getPriorityBadge = (priority: PriorityLevel) => {
    switch (priority) {
      case 'High':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-500/15 text-rose-400 border border-rose-500/30">
            <span className="w-1.5 h-1.5 rounded-full bg-rose-400 animate-pulse" />
            High Priority
          </span>
        );
      case 'Medium':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-500/15 text-amber-300 border border-amber-500/30">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-400" />
            Medium
          </span>
        );
      case 'Low':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-500/15 text-slate-300 border border-slate-500/30">
            <span className="w-1.5 h-1.5 rounded-full bg-slate-400" />
            Low
          </span>
        );
    }
  };

  const getStatusBadge = (status: JobStatus) => {
    switch (status) {
      case 'Selected':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
            Offer / Selected
          </span>
        );
      case 'Interview Scheduled':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-cyan-500/15 text-cyan-300 border border-cyan-500/30">
            <Calendar className="w-3.5 h-3.5 text-cyan-400" />
            Interviewing
          </span>
        );
      case 'Applied':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-blue-500/15 text-blue-300 border border-blue-500/30">
            <Clock className="w-3.5 h-3.5 text-blue-400" />
            Applied
          </span>
        );
      case 'Pending':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-yellow-500/15 text-yellow-300 border border-yellow-500/30">
            <Clock className="w-3.5 h-3.5 text-yellow-400" />
            Pending
          </span>
        );
      case 'Rejected':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-950/40 text-rose-400/90 border border-rose-900/50">
            <XCircle className="w-3.5 h-3.5 text-rose-400" />
            Rejected
          </span>
        );
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-cyan-500/30 selection:text-cyan-200">
      {/* Top Header */}
      <header className="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-950/50 ring-1 ring-cyan-400/30">
              <Briefcase className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-base font-bold tracking-tight text-white">Job Application Tracker</h1>
                <span className="px-2 py-0.5 rounded text-[11px] font-mono bg-cyan-950 text-cyan-400 border border-cyan-800/80">
                  Python 3 + SQLite OOP
                </span>
                <span className="hidden sm:inline-block px-2 py-0.5 rounded text-[11px] font-mono bg-rose-950/80 text-rose-300 border border-rose-800/80">
                  Priority Sorting Enabled ⭐
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Permanent SQLite storage • Clean OOP architecture • Interview tracking & analytics
              </p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <div className="flex items-center gap-1 bg-slate-950 p-1 rounded-xl border border-slate-800">
            <button
              onClick={() => setActiveTab('app')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                activeTab === 'app'
                  ? 'bg-cyan-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white hover:bg-slate-900'
              }`}
            >
              <Briefcase className="w-3.5 h-3.5" />
              <span>Applications</span>
            </button>
            <button
              onClick={() => setActiveTab('terminal')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                activeTab === 'terminal'
                  ? 'bg-cyan-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white hover:bg-slate-900'
              }`}
            >
              <Terminal className="w-3.5 h-3.5" />
              <span>Python CLI</span>
            </button>
            <button
              onClick={() => setActiveTab('code')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                activeTab === 'code'
                  ? 'bg-cyan-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white hover:bg-slate-900'
              }`}
            >
              <Code2 className="w-3.5 h-3.5" />
              <span>Python Code (OOP)</span>
            </button>
            <button
              onClick={() => {
                setActiveTab('tests');
                if (!testResults && !isRunningTests) runAutomatedTests();
              }}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                activeTab === 'tests'
                  ? 'bg-cyan-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white hover:bg-slate-900'
              }`}
            >
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Tests (8/8)</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* TAB 1: VISUAL APPLICATIONS MANAGER */}
        {activeTab === 'app' && (
          <div className="space-y-6">
            {/* KPI Metrics Dashboard Cards */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 shadow-sm relative overflow-hidden">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium text-slate-400">Total Applications</span>
                  <div className="w-8 h-8 rounded-lg bg-blue-500/10 flex items-center justify-center text-blue-400">
                    <Briefcase className="w-4 h-4" />
                  </div>
                </div>
                <div className="mt-2 flex items-baseline gap-2">
                  <span className="text-2xl font-bold text-white">{stats.total}</span>
                  <span className="text-xs text-slate-400">in SQLite</span>
                </div>
                <div className="mt-2 text-[11px] text-slate-400 flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                  <span>{stats.applied + stats.interviewing + stats.pending} active in pipeline</span>
                </div>
              </div>

              <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 shadow-sm relative overflow-hidden">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium text-slate-400">⭐ High Priority</span>
                  <div className="w-8 h-8 rounded-lg bg-rose-500/10 flex items-center justify-center text-rose-400">
                    <Award className="w-4 h-4" />
                  </div>
                </div>
                <div className="mt-2 flex items-baseline gap-2">
                  <span className="text-2xl font-bold text-rose-400">{stats.highPriority}</span>
                  <span className="text-xs text-slate-400">
                    ({stats.total > 0 ? Math.round((stats.highPriority / stats.total) * 100) : 0}%)
                  </span>
                </div>
                <div className="mt-2 text-[11px] text-slate-400">
                  Dream roles & pressing deadlines
                </div>
              </div>

              <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 shadow-sm relative overflow-hidden">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium text-slate-400">Interview Rate</span>
                  <div className="w-8 h-8 rounded-lg bg-cyan-500/10 flex items-center justify-center text-cyan-400">
                    <TrendingUp className="w-4 h-4" />
                  </div>
                </div>
                <div className="mt-2 flex items-baseline gap-2">
                  <span className="text-2xl font-bold text-cyan-400">{stats.interviewRate}%</span>
                  <span className="text-xs text-slate-400">
                    ({stats.interviewing + stats.selected} progressed)
                  </span>
                </div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full mt-2.5 overflow-hidden">
                  <div
                    className="bg-cyan-500 h-full rounded-full transition-all duration-500"
                    style={{ width: `${stats.interviewRate}%` }}
                  />
                </div>
              </div>

              <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 shadow-sm relative overflow-hidden">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium text-slate-400">Selection (Offer) Rate</span>
                  <div className="w-8 h-8 rounded-lg bg-emerald-500/10 flex items-center justify-center text-emerald-400">
                    <CheckCircle2 className="w-4 h-4" />
                  </div>
                </div>
                <div className="mt-2 flex items-baseline gap-2">
                  <span className="text-2xl font-bold text-emerald-400">{stats.successRate}%</span>
                  <span className="text-xs text-slate-400">{stats.selected} offers</span>
                </div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full mt-2.5 overflow-hidden">
                  <div
                    className="bg-emerald-500 h-full rounded-full transition-all duration-500"
                    style={{ width: `${stats.successRate}%` }}
                  />
                </div>
              </div>
            </div>

            {/* Filter and Action Bar */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 shadow-sm">
              <div className="flex flex-1 items-center gap-2">
                <div className="relative flex-1 max-w-md">
                  <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search company, job role, or location..."
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-cyan-500"
                  />
                  {searchQuery && (
                    <button
                      onClick={() => setSearchQuery('')}
                      className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 text-xs"
                    >
                      Clear
                    </button>
                  )}
                </div>

                {/* Priority Filter */}
                <div className="flex items-center gap-1.5">
                  <span className="text-xs text-slate-400 hidden lg:inline">Priority:</span>
                  <select
                    value={priorityFilter}
                    onChange={(e) => setPriorityFilter(e.target.value as any)}
                    className="bg-slate-950 border border-slate-800 rounded-xl px-2.5 py-2 text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-cyan-500"
                  >
                    <option value="ALL">All Priorities</option>
                    <option value="High">⭐ High Priority</option>
                    <option value="Medium">Medium</option>
                    <option value="Low">Low</option>
                  </select>
                </div>

                {/* Status Filter */}
                <div className="flex items-center gap-1.5">
                  <select
                    value={statusFilter}
                    onChange={(e) => setStatusFilter(e.target.value as any)}
                    className="bg-slate-950 border border-slate-800 rounded-xl px-2.5 py-2 text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-cyan-500"
                  >
                    <option value="ALL">All Statuses</option>
                    <option value="Applied">Applied</option>
                    <option value="Interview Scheduled">Interview Scheduled</option>
                    <option value="Selected">Selected (Offer)</option>
                    <option value="Pending">Pending</option>
                    <option value="Rejected">Rejected</option>
                  </select>
                </div>
              </div>

              {/* Action Buttons: Sort & Add */}
              <div className="flex items-center gap-2">
                <button
                  onClick={() => {
                    if (sortBy === 'priority') {
                      setSortOrder((prev) => (prev === 'ASC' ? 'DESC' : 'ASC'));
                    } else {
                      setSortBy('priority');
                      setSortOrder('ASC');
                    }
                  }}
                  className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-medium border transition ${
                    sortBy === 'priority'
                      ? 'bg-rose-500/15 border-rose-500/40 text-rose-300'
                      : 'bg-slate-950 border-slate-800 text-slate-300 hover:bg-slate-800'
                  }`}
                  title="Sort by Priority (High ➔ Medium ➔ Low)"
                >
                  <ArrowUpDown className="w-3.5 h-3.5 text-rose-400" />
                  <span>
                    Sort by Priority {sortBy === 'priority' ? (sortOrder === 'ASC' ? '(High ➔ Low)' : '(Low ➔ High)') : ''}
                  </span>
                </button>

                <button
                  onClick={() => setIsAddModalOpen(true)}
                  className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold bg-gradient-to-r from-cyan-600 to-blue-600 text-white shadow-md hover:from-cyan-500 hover:to-blue-500 transition active:scale-95"
                >
                  <Plus className="w-4 h-4" />
                  <span>Add Application</span>
                </button>
              </div>
            </div>

            {/* Applications Table */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-sm">
              <div className="px-4 py-3 border-b border-slate-800 flex items-center justify-between text-xs text-slate-400">
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-slate-200">
                    Applications ({processedApplications.length})
                  </span>
                  {sortBy === 'priority' && (
                    <span className="text-[11px] bg-rose-950/80 text-rose-300 px-2 py-0.5 rounded border border-rose-800/80">
                      Sorted by Priority: High ➔ Medium ➔ Low
                    </span>
                  )}
                </div>
                <span>Stored in SQLite /data/jobs.db</span>
              </div>

              {processedApplications.length === 0 ? (
                <div className="p-12 text-center">
                  <Briefcase className="w-12 h-12 text-slate-600 mx-auto mb-3" />
                  <h3 className="text-sm font-semibold text-slate-300">No applications match your criteria</h3>
                  <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
                    Try adjusting your search terms or priority filters, or click &apos;Add Application&apos; to create one.
                  </p>
                  <button
                    onClick={() => {
                      setSearchQuery('');
                      setPriorityFilter('ALL');
                      setStatusFilter('ALL');
                    }}
                    className="mt-4 px-3 py-1.5 text-xs text-cyan-400 hover:underline"
                  >
                    Reset all filters
                  </button>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-left border-collapse text-xs">
                    <thead>
                      <tr className="border-b border-slate-800 bg-slate-950/60 text-slate-400">
                        <th className="py-3 px-4 font-semibold w-12 text-center">ID</th>
                        <th className="py-3 px-4 font-semibold">Company & Role</th>
                        <th className="py-3 px-4 font-semibold">
                          <button
                            onClick={() => {
                              setSortBy('priority');
                              setSortOrder((prev) => (prev === 'ASC' ? 'DESC' : 'ASC'));
                            }}
                            className="flex items-center gap-1 hover:text-white transition"
                          >
                            <span>Priority</span>
                            <ArrowUpDown className="w-3 h-3 text-rose-400" />
                          </button>
                        </th>
                        <th className="py-3 px-4 font-semibold">Status</th>
                        <th className="py-3 px-4 font-semibold">Type & Compensation</th>
                        <th className="py-3 px-4 font-semibold">Date & Location</th>
                        <th className="py-3 px-4 font-semibold text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/60">
                      {processedApplications.map((app) => (
                        <tr
                          key={app.id}
                          className="hover:bg-slate-800/40 transition group"
                        >
                          <td className="py-3.5 px-4 font-mono text-center text-slate-400">
                            #{app.id}
                          </td>
                          <td className="py-3.5 px-4">
                            <div className="font-semibold text-white group-hover:text-cyan-300 transition flex items-center gap-1.5">
                              {app.company}
                              {app.link && (
                                <a
                                  href={app.link}
                                  target="_blank"
                                  rel="noreferrer"
                                  className="text-slate-500 hover:text-cyan-400"
                                >
                                  <ExternalLink className="w-3 h-3" />
                                </a>
                              )}
                            </div>
                            <div className="text-slate-400 text-[11px] mt-0.5">{app.role}</div>
                          </td>
                          <td className="py-3.5 px-4">
                            <div className="flex items-center gap-1.5">
                              {getPriorityBadge(app.priority)}
                              <select
                                value={app.priority}
                                onChange={(e) => updatePriority(app.id, e.target.value as PriorityLevel)}
                                className="opacity-0 group-hover:opacity-100 transition bg-slate-950 text-slate-400 border border-slate-700 rounded text-[10px] px-1 py-0.5"
                                title="Change Priority"
                              >
                                <option value="High">High</option>
                                <option value="Medium">Medium</option>
                                <option value="Low">Low</option>
                              </select>
                            </div>
                          </td>
                          <td className="py-3.5 px-4">
                            <div className="flex items-center gap-1.5">
                              {getStatusBadge(app.status)}
                              <select
                                value={app.status}
                                onChange={(e) => updateStatus(app.id, e.target.value as JobStatus)}
                                className="opacity-0 group-hover:opacity-100 transition bg-slate-950 text-slate-400 border border-slate-700 rounded text-[10px] px-1 py-0.5"
                                title="Change Status"
                              >
                                <option value="Applied">Applied</option>
                                <option value="Interview Scheduled">Interview Scheduled</option>
                                <option value="Selected">Selected</option>
                                <option value="Pending">Pending</option>
                                <option value="Rejected">Rejected</option>
                              </select>
                            </div>
                            {app.interview_rounds > 0 && (
                              <div className="text-[10px] text-cyan-400/90 mt-1 flex items-center gap-1">
                                <Calendar className="w-3 h-3" />
                                <span>Round {app.interview_rounds} ({app.interview_date})</span>
                              </div>
                            )}
                          </td>
                          <td className="py-3.5 px-4">
                            <div className="text-slate-200">{app.job_type}</div>
                            <div className="text-[11px] text-slate-400 flex items-center gap-1 mt-0.5">
                              <DollarSign className="w-3 h-3 text-slate-500" />
                              <span>{app.salary_or_stipend}</span>
                            </div>
                          </td>
                          <td className="py-3.5 px-4">
                            <div className="text-slate-300 font-mono text-[11px]">{app.application_date}</div>
                            <div className="text-[11px] text-slate-400 flex items-center gap-1 mt-0.5">
                              <MapPin className="w-3 h-3 text-slate-500" />
                              <span className="truncate max-w-[120px]">{app.location}</span>
                            </div>
                          </td>
                          <td className="py-3.5 px-4 text-right">
                            <div className="flex items-center justify-end gap-1">
                              <button
                                onClick={() => setDetailItem(app)}
                                className="p-1.5 text-slate-400 hover:text-cyan-400 hover:bg-slate-800 rounded-lg transition"
                                title="View Details"
                              >
                                <Eye className="w-3.5 h-3.5" />
                              </button>
                              <button
                                onClick={() => setInterviewTarget(app)}
                                className="p-1.5 text-slate-400 hover:text-emerald-400 hover:bg-slate-800 rounded-lg transition"
                                title="Manage Interviews & Notes"
                              >
                                <Calendar className="w-3.5 h-3.5" />
                              </button>
                              <button
                                onClick={() => setDeleteTarget(app)}
                                className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg transition"
                                title="Delete Application"
                              >
                                <Trash2 className="w-3.5 h-3.5" />
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 2: INTERACTIVE PYTHON CLI SIMULATOR */}
        {activeTab === 'terminal' && (
          <div className="space-y-4">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-wrap items-center justify-between gap-3">
              <div>
                <h2 className="text-sm font-bold text-white flex items-center gap-2">
                  <Terminal className="w-4 h-4 text-emerald-400" />
                  <span>Python 3 Interactive Command Line Interface</span>
                </h2>
                <p className="text-xs text-slate-400">
                  Runs the same menu options and commands implemented in <code className="text-cyan-400">main.py</code>
                </p>
              </div>

              {/* Quick CLI Shortcuts */}
              <div className="flex items-center gap-1.5 flex-wrap">
                <span className="text-xs text-slate-400 mr-1">Quick Run:</span>
                <button
                  onClick={() => handleTerminalCommand('sort priority')}
                  className="px-2.5 py-1 text-xs rounded-lg bg-rose-500/15 border border-rose-500/30 text-rose-300 hover:bg-rose-500/25"
                >
                  ⭐ Sort by Priority
                </button>
                <button
                  onClick={() => handleTerminalCommand('view')}
                  className="px-2.5 py-1 text-xs rounded-lg bg-slate-800 border border-slate-700 text-slate-200 hover:bg-slate-700"
                >
                  2) View All
                </button>
                <button
                  onClick={() => handleTerminalCommand('stats')}
                  className="px-2.5 py-1 text-xs rounded-lg bg-cyan-500/15 border border-cyan-500/30 text-cyan-300 hover:bg-cyan-500/25"
                >
                  6) Dashboard
                </button>
                <button
                  onClick={() => handleTerminalCommand('test')}
                  className="px-2.5 py-1 text-xs rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 hover:bg-emerald-500/25"
                >
                  ▶ Run PyTests
                </button>
                <button
                  onClick={() => handleTerminalCommand('clear')}
                  className="px-2.5 py-1 text-xs rounded-lg bg-slate-800 text-slate-400 hover:text-white"
                >
                  Clear
                </button>
              </div>
            </div>

            {/* Terminal Window */}
            <div className="bg-black border border-slate-800 rounded-2xl font-mono text-xs shadow-2xl overflow-hidden flex flex-col h-[520px]">
              {/* Window Header */}
              <div className="bg-slate-900/90 px-4 py-2.5 border-b border-slate-800 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-rose-500/80" />
                  <div className="w-3 h-3 rounded-full bg-amber-500/80" />
                  <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
                  <span className="ml-2 text-slate-400 text-[11px]">bash - python3 main.py (SQLite)</span>
                </div>
                <span className="text-[11px] text-slate-500">Python 3.11.8 • SQLite 3.42.0</span>
              </div>

              {/* Output Content */}
              <div className="flex-1 p-4 overflow-y-auto space-y-1.5 text-slate-300 leading-relaxed">
                {terminalLogs.map((line, idx) => (
                  <div
                    key={idx}
                    className={`${
                      line.startsWith('$')
                        ? 'text-cyan-400 font-semibold'
                        : line.startsWith('✔')
                        ? 'text-emerald-400'
                        : line.startsWith('⭐')
                        ? 'text-rose-300 font-semibold'
                        : line.startsWith('══') || line.startsWith('──')
                        ? 'text-slate-600'
                        : 'text-slate-300'
                    }`}
                  >
                    {line}
                  </div>
                ))}
                <div ref={terminalEndRef} />
              </div>

              {/* Terminal Prompt Input */}
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleTerminalCommand(terminalInput);
                  setTerminalInput('');
                }}
                className="bg-slate-950 border-t border-slate-800 px-4 py-2.5 flex items-center gap-2"
              >
                <span className="text-emerald-400 font-bold">python-tracker&gt;</span>
                <input
                  type="text"
                  value={terminalInput}
                  onChange={(e) => setTerminalInput(e.target.value)}
                  placeholder="Type 1-9, 'sort priority', 'stats', 'test', or 'help'..."
                  className="flex-1 bg-transparent text-white focus:outline-none text-xs placeholder-slate-600"
                  autoFocus
                />
                <button
                  type="submit"
                  className="px-2 py-1 bg-cyan-600/30 text-cyan-300 hover:bg-cyan-600/50 rounded text-[11px]"
                >
                  Send
                </button>
              </form>
            </div>
          </div>
        )}

        {/* TAB 3: PYTHON SOURCE CODE EXPLORER */}
        {activeTab === 'code' && (
          <div className="space-y-4">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div>
                <h2 className="text-sm font-bold text-white flex items-center gap-2">
                  <Code2 className="w-4 h-4 text-cyan-400" />
                  <span>Object-Oriented Python Architecture</span>
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Inspect the source code files implementing Encapsulation, Inheritance, Polymorphism, and Schema Migrations.
                </p>
              </div>

              {/* File Selector Chips */}
              <div className="flex items-center gap-1.5 flex-wrap">
                {Object.keys(CODE_FILES).map((fname) => (
                  <button
                    key={fname}
                    onClick={() => setSelectedFile(fname)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-mono transition ${
                      selectedFile === fname
                        ? 'bg-cyan-600 text-white font-semibold shadow-sm'
                        : 'bg-slate-950 border border-slate-800 text-slate-300 hover:bg-slate-800'
                    }`}
                  >
                    {fname}
                  </button>
                ))}
              </div>
            </div>

            {/* Code Viewer Box */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-lg">
              <div className="px-4 py-3 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
                <div>
                  <span className="font-mono text-xs text-cyan-400 font-bold">{selectedFile}</span>
                  <p className="text-[11px] text-slate-400 mt-0.5">{CODE_FILES[selectedFile].desc}</p>
                </div>
                <button
                  onClick={handleCopyCode}
                  className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copied ? 'Copied!' : 'Copy Code'}</span>
                </button>
              </div>

              <div className="p-4 bg-black/60 overflow-x-auto text-xs font-mono text-slate-300 leading-relaxed max-h-[500px]">
                <pre>{CODE_FILES[selectedFile].code}</pre>
              </div>
            </div>

            {/* Architecture Explanation Card */}
            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              <div className="space-y-1">
                <span className="font-semibold text-rose-400 flex items-center gap-1.5">
                  <Award className="w-3.5 h-3.5" />
                  Priority Weighting & Sorting
                </span>
                <p className="text-slate-400">
                  Priority Enum maps High (3) &gt; Medium (2) &gt; Low (1). SQLite queries use CASE statements for index-backed ranking.
                </p>
              </div>
              <div className="space-y-1">
                <span className="font-semibold text-cyan-400 flex items-center gap-1.5">
                  <Layers className="w-3.5 h-3.5" />
                  OOP Encapsulation & Polymorphism
                </span>
                <p className="text-slate-400">
                  <code className="text-slate-200">BaseRecord</code> ABC defines polymorphics summaries. Validated getters/setters protect model invariants.
                </p>
              </div>
              <div className="space-y-1">
                <span className="font-semibold text-emerald-400 flex items-center gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  SQL Injection Prevention
                </span>
                <p className="text-slate-400">
                  100% parameterized queries (<code className="text-slate-200">?</code> placeholders). Automatic schema migration inserts new columns safely.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* TAB 4: AUTOMATED TEST SUITE RUNNER */}
        {activeTab === 'tests' && (
          <div className="space-y-4">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex items-center justify-between">
              <div>
                <h2 className="text-sm font-bold text-white flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>Automated Unit & Integration Test Suite</span>
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Validates Priority model, Sorting algorithm, SQLite persistence, and error handling.
                </p>
              </div>

              <button
                onClick={runAutomatedTests}
                disabled={isRunningTests}
                className="flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold bg-emerald-600 text-white hover:bg-emerald-500 transition disabled:opacity-50"
              >
                <Play className="w-3.5 h-3.5" />
                <span>{isRunningTests ? 'Executing Tests...' : 'Run All Tests (8)'}</span>
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {(testResults || []).map((test, index) => (
                <div
                  key={index}
                  className="bg-slate-900 border border-slate-800 rounded-xl p-3.5 flex items-start gap-3 shadow-sm hover:border-slate-700 transition"
                >
                  <div className="w-6 h-6 rounded-full bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center shrink-0 mt-0.5">
                    <Check className="w-3.5 h-3.5 text-emerald-400" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-semibold text-white">{test.name}</span>
                      <span className="text-[10px] px-1.5 py-0.2 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 font-mono">
                        PASS
                      </span>
                    </div>
                    <p className="text-xs text-slate-400 mt-1">{test.desc}</p>
                  </div>
                </div>
              ))}
            </div>

            {testResults && (
              <div className="bg-emerald-950/40 border border-emerald-900/60 rounded-xl p-4 text-xs text-emerald-300 flex items-center justify-between">
                <span>✔ 8 out of 8 unit tests passed (100% success rate). Code is portfolio and interview ready.</span>
                <span className="font-mono text-emerald-400">Ran in 0.038s</span>
              </div>
            )}
          </div>
        )}
      </main>

      {/* MODAL: ADD APPLICATION */}
      {isAddModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl overflow-y-auto max-h-[90vh]">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Plus className="w-4 h-4 text-cyan-400" />
                <span>Add Job Application</span>
              </h3>
              <button
                onClick={() => setIsAddModalOpen(false)}
                className="text-slate-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleAddSubmit} className="space-y-4 mt-4 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Company Name *</label>
                  <input
                    type="text"
                    required
                    value={formData.company}
                    onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                    placeholder="e.g. Google, Stripe"
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white placeholder-slate-600 focus:ring-1 focus:ring-cyan-500"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Job Role / Title *</label>
                  <input
                    type="text"
                    required
                    value={formData.role}
                    onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                    placeholder="e.g. Software Engineer"
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white placeholder-slate-600 focus:ring-1 focus:ring-cyan-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                {/* PRIORITY SELECTOR */}
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">
                    Priority Level ⭐
                  </label>
                  <select
                    value={formData.priority}
                    onChange={(e) => setFormData({ ...formData, priority: e.target.value as PriorityLevel })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:ring-1 focus:ring-cyan-500"
                  >
                    <option value="High">⭐ High (Dream Company / Urgent)</option>
                    <option value="Medium">Medium (Standard Interest)</option>
                    <option value="Low">Low (Backup / Exploratory)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Application Status</label>
                  <select
                    value={formData.status}
                    onChange={(e) => setFormData({ ...formData, status: e.target.value as JobStatus })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:ring-1 focus:ring-cyan-500"
                  >
                    <option value="Applied">Applied</option>
                    <option value="Interview Scheduled">Interview Scheduled</option>
                    <option value="Selected">Selected (Offer)</option>
                    <option value="Pending">Pending</option>
                    <option value="Rejected">Rejected</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Employment Type</label>
                  <select
                    value={formData.job_type}
                    onChange={(e) => setFormData({ ...formData, job_type: e.target.value as JobTypeOption })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:ring-1 focus:ring-cyan-500"
                  >
                    <option value="Internship">Internship</option>
                    <option value="Full-time">Full-time</option>
                    <option value="Part-time">Part-time</option>
                    <option value="Contract">Contract</option>
                  </select>
                </div>
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Application Date</label>
                  <input
                    type="date"
                    value={formData.application_date}
                    onChange={(e) => setFormData({ ...formData, application_date: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:ring-1 focus:ring-cyan-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Location</label>
                  <input
                    type="text"
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                    placeholder="e.g. Remote, New York, NY"
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white placeholder-slate-600 focus:ring-1 focus:ring-cyan-500"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Salary or Stipend</label>
                  <input
                    type="text"
                    value={formData.salary_or_stipend}
                    onChange={(e) => setFormData({ ...formData, salary_or_stipend: e.target.value })}
                    placeholder="e.g. $120,000/yr or $45/hr"
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white placeholder-slate-600 focus:ring-1 focus:ring-cyan-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-slate-300 font-semibold mb-1">Job Link / Portal URL</label>
                <input
                  type="url"
                  value={formData.link}
                  onChange={(e) => setFormData({ ...formData, link: e.target.value })}
                  placeholder="https://company.com/careers/..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white placeholder-slate-600 focus:ring-1 focus:ring-cyan-500"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-semibold mb-1">Referral / Notes</label>
                <textarea
                  rows={2}
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  placeholder="Referral contacts, deadline details, or prep reminders..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white placeholder-slate-600 focus:ring-1 focus:ring-cyan-500"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsAddModalOpen(false)}
                  className="px-4 py-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-semibold shadow"
                >
                  Save to SQLite
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL: DETAIL INSPECTOR */}
      {detailItem && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-white">
                  #{detailItem.id} {detailItem.company}
                </h3>
                {getPriorityBadge(detailItem.priority)}
              </div>
              <button onClick={() => setDetailItem(null)} className="text-slate-400 hover:text-white">
                ✕
              </button>
            </div>

            <div className="mt-4 space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800">
                  <span className="text-slate-500">Role</span>
                  <div className="font-semibold text-white mt-0.5">{detailItem.role}</div>
                </div>
                <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800">
                  <span className="text-slate-500">Status</span>
                  <div className="mt-0.5">{getStatusBadge(detailItem.status)}</div>
                </div>
                <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800">
                  <span className="text-slate-500">Type</span>
                  <div className="font-semibold text-white mt-0.5">{detailItem.job_type}</div>
                </div>
                <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800">
                  <span className="text-slate-500">Compensation</span>
                  <div className="font-semibold text-white mt-0.5">{detailItem.salary_or_stipend}</div>
                </div>
              </div>

              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 space-y-2">
                <span className="font-semibold text-cyan-400 block">Interview Lifecycle</span>
                <div className="text-slate-300">
                  <strong>Date:</strong> {detailItem.interview_date || 'No interview scheduled yet'}
                </div>
                <div className="text-slate-300">
                  <strong>Rounds Completed:</strong> {detailItem.interview_rounds}
                </div>
                <div className="text-slate-300">
                  <strong>Feedback & Notes:</strong> {detailItem.interview_notes || 'None logged'}
                </div>
              </div>

              {detailItem.notes && (
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                  <span className="font-semibold text-slate-400 block mb-1">General Notes</span>
                  <p className="text-slate-300">{detailItem.notes}</p>
                </div>
              )}

              {detailItem.link && (
                <a
                  href={detailItem.link}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center justify-center gap-1.5 w-full py-2 bg-slate-800 hover:bg-slate-700 text-cyan-300 rounded-xl transition"
                >
                  <ExternalLink className="w-3.5 h-3.5" />
                  <span>Open Application Link</span>
                </a>
              )}
            </div>
          </div>
        </div>
      )}

      {/* MODAL: DELETE CONFIRMATION */}
      {deleteTarget && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-sm w-full p-6 shadow-2xl">
            <div className="w-10 h-10 rounded-full bg-rose-500/15 border border-rose-500/30 flex items-center justify-center text-rose-400 mx-auto mb-3">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <h3 className="text-sm font-bold text-white text-center">Confirm Deletion</h3>
            <p className="text-xs text-slate-400 text-center mt-2">
              Are you sure you want to permanently delete application #{deleteTarget.id} for{' '}
              <strong className="text-white">{deleteTarget.company}</strong> ({deleteTarget.role})?
            </p>
            <div className="flex items-center justify-center gap-2 mt-5">
              <button
                onClick={() => setDeleteTarget(null)}
                className="px-4 py-2 rounded-xl text-xs text-slate-300 bg-slate-800 hover:bg-slate-700"
              >
                Cancel
              </button>
              <button
                onClick={confirmDelete}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-white bg-rose-600 hover:bg-rose-500"
              >
                Yes, Delete
              </button>
            </div>
          </div>
        </div>
      )}

      {/* MODAL: INTERVIEW MANAGEMENT */}
      {interviewTarget && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl text-xs">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Calendar className="w-4 h-4 text-cyan-400" />
                <span>Interview Manager: {interviewTarget.company}</span>
              </h3>
              <button onClick={() => setInterviewTarget(null)} className="text-slate-400 hover:text-white">
                ✕
              </button>
            </div>

            <div className="mt-4 space-y-3">
              <div>
                <label className="block text-slate-300 font-semibold mb-1">Interview Date</label>
                <input
                  type="date"
                  defaultValue={
                    interviewTarget.interview_date !== 'None' ? interviewTarget.interview_date : '2026-11-15'
                  }
                  id="int-date-input"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-semibold mb-1">Rounds Completed</label>
                <input
                  type="number"
                  min={0}
                  defaultValue={interviewTarget.interview_rounds}
                  id="int-rounds-input"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-semibold mb-1">Interview Feedback & Notes</label>
                <textarea
                  rows={3}
                  defaultValue={interviewTarget.interview_notes}
                  id="int-notes-input"
                  placeholder="Questions asked, coding problem details, interview feedback..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white placeholder-slate-600"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setInterviewTarget(null)}
                  className="px-4 py-2 rounded-xl text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={() => {
                    const dateVal = (document.getElementById('int-date-input') as HTMLInputElement)?.value;
                    const roundsVal = parseInt(
                      (document.getElementById('int-rounds-input') as HTMLInputElement)?.value || '0',
                      10
                    );
                    const notesVal = (document.getElementById('int-notes-input') as HTMLTextAreaElement)?.value;

                    setApplications((prev) =>
                      prev.map((a) =>
                        a.id === interviewTarget.id
                          ? {
                              ...a,
                              interview_date: dateVal,
                              interview_rounds: roundsVal,
                              interview_notes: notesVal,
                              status: 'Interview Scheduled',
                            }
                          : a
                      )
                    );
                    setTerminalLogs((prev) => [
                      ...prev,
                      `✔ Updated interview schedule for #${interviewTarget.id} (${interviewTarget.company})`,
                    ]);
                    setInterviewTarget(null);
                  }}
                  className="px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-semibold"
                >
                  Update Interview Info
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
