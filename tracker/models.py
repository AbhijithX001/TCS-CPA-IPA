"""
Models for TCS CPA/IPA Exam Preparation Tracker.
"""
from django.db import models


class Subject(models.Model):
    SECTION_MCQ = 'MCQ'
    SECTION_CODING = 'CODING'
    SECTION_CHOICES = [
        (SECTION_MCQ, 'MCQ Section (50 Marks / 50 Mins)'),
        (SECTION_CODING, 'Coding Section (50 Marks / 70 Mins)'),
    ]

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=120)
    section_type = models.CharField(max_length=10, choices=SECTION_CHOICES)
    marks = models.PositiveIntegerField()
    questions_count = models.PositiveIntegerField()
    time_info = models.CharField(max_length=80)

    class Meta:
        ordering = ['section_type', 'code']

    def __str__(self):
        return f"[{self.code}] {self.name}"

    @property
    def total_tasks(self):
        return self.tasks.count()

    @property
    def completed_tasks(self):
        return self.tasks.filter(is_completed=True).count()

    @property
    def progress_pct(self):
        total = self.total_tasks
        if total == 0:
            return 0
        return round((self.completed_tasks / total) * 100)


class StudyDay(models.Model):
    date = models.DateField(unique=True)
    title = models.CharField(max_length=200)
    focus_summary = models.TextField()

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.date} – {self.title}"

    @property
    def total_tasks(self):
        return self.tasks.count()

    @property
    def completed_tasks(self):
        return self.tasks.filter(is_completed=True).count()

    @property
    def progress_pct(self):
        total = self.total_tasks
        if total == 0:
            return 0
        return round((self.completed_tasks / total) * 100)


class Task(models.Model):
    day = models.ForeignKey(StudyDay, on_delete=models.CASCADE, related_name='tasks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=300)
    resource_url = models.URLField(blank=True, null=True)
    resource_label = models.CharField(max_length=100, blank=True)
    is_completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        status = '✓' if self.is_completed else '○'
        return f"{status} [{self.subject.code}] {self.title}"


class CodingPractice(models.Model):
    CAT_FUNDAMENTALS = 'FUNDAMENTALS'
    CAT_15 = '15_MARK'
    CAT_35 = '35_MARK'
    CAT_CHOICES = [
        (CAT_FUNDAMENTALS, 'Fundamentals / Warm-up'),
        (CAT_15, '15-Mark Problem'),
        (CAT_35, '35-Mark OOP Problem'),
    ]

    STATUS_PENDING = 'PENDING'
    STATUS_SOLVED = 'SOLVED'
    STATUS_REVISION = 'NEEDS_REVISION'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_SOLVED, 'Solved Optimal'),
        (STATUS_REVISION, 'Needs Revision'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CAT_CHOICES)
    url = models.URLField()
    day = models.ForeignKey(StudyDay, on_delete=models.SET_NULL, null=True, blank=True, related_name='coding_practices')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    time_taken_mins = models.PositiveIntegerField(null=True, blank=True)
    key_edge_cases = models.TextField(blank=True)

    class Meta:
        ordering = ['category', 'title']

    def __str__(self):
        return f"[{self.category}] {self.title} — {self.status}"


class MistakeLog(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='mistakes')
    topic_or_question = models.CharField(max_length=300)
    what_went_wrong = models.TextField()
    correct_concept_or_fix = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        status = '✓ Resolved' if self.is_resolved else '⚠ Open'
        return f"[{self.subject.code}] {self.topic_or_question} ({status})"
