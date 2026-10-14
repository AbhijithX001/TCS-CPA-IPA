"""
Idempotent seed command: python manage.py seed_cpa
Populates all Subjects, StudyDays, Tasks, CodingPractice records, and starter MistakeLogs.
Running multiple times is safe — existing records are matched and updated, not duplicated.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from tracker.models import Subject, StudyDay, Task, CodingPractice, MistakeLog
import datetime


class Command(BaseCommand):
    help = 'Seeds the TCS CPA/IPA Exam Preparation Tracker database with syllabus and study plan.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('=== TCS CPA/IPA Tracker Seed ==='))

        # ------------------------------------------------------------------ #
        # 1. SUBJECTS                                                          #
        # ------------------------------------------------------------------ #
        subjects_data = [
            # MCQ Section
            {
                'code': 'BS_MCQ',
                'name': 'Business Skills',
                'section_type': Subject.SECTION_MCQ,
                'marks': 25,
                'questions_count': 25,
                'time_info': '25 Qs · 25 Marks · ~30 mins',
            },
            {
                'code': 'JAVA_MCQ',
                'name': 'Java MCQs',
                'section_type': Subject.SECTION_MCQ,
                'marks': 10,
                'questions_count': 10,
                'time_info': '10 Qs · 10 Marks · ~12 mins',
            },
            {
                'code': 'UI_MCQ',
                'name': 'UI (HTML, CSS, JS)',
                'section_type': Subject.SECTION_MCQ,
                'marks': 5,
                'questions_count': 5,
                'time_info': '5 Qs · 5 Marks · ~5 mins',
            },
            {
                'code': 'UNIX_MCQ',
                'name': 'Unix Commands & OS',
                'section_type': Subject.SECTION_MCQ,
                'marks': 5,
                'questions_count': 5,
                'time_info': '5 Qs · 5 Marks · ~5 mins',
            },
            {
                'code': 'SQL_MCQ',
                'name': 'SQL Queries & RDBMS',
                'section_type': Subject.SECTION_MCQ,
                'marks': 5,
                'questions_count': 5,
                'time_info': '5 Qs · 5 Marks · ~5 mins',
            },
            # Coding Section
            {
                'code': 'JAVA_15',
                'name': 'Java Coding Problem 1 (15 Marks)',
                'section_type': Subject.SECTION_CODING,
                'marks': 15,
                'questions_count': 1,
                'time_info': '1 Q · 15 Marks · ~20 mins target',
            },
            {
                'code': 'JAVA_35',
                'name': 'Java Coding Problem 2 (35 Marks)',
                'section_type': Subject.SECTION_CODING,
                'marks': 35,
                'questions_count': 1,
                'time_info': '1 Q · 35 Marks · ~50 mins target',
            },
        ]

        subject_map = {}
        for sd in subjects_data:
            obj, created = Subject.objects.update_or_create(
                code=sd['code'],
                defaults={k: v for k, v in sd.items() if k != 'code'},
            )
            subject_map[sd['code']] = obj
            verb = 'Created' if created else 'Updated'
            self.stdout.write(f'  {verb} Subject: {obj}')

        # ------------------------------------------------------------------ #
        # 2. STUDY DAYS + TASKS                                                #
        # ------------------------------------------------------------------ #
        days_data = [
            {
                'date': datetime.date(2026, 10, 13),
                'title': 'Day 1 — Java Fundamentals and MCQs',
                'focus_summary': (
                    'Build a solid Java foundation: strings, arrays, loops, OOP basics. '
                    'Warm up with LeetCode 15-mark style problems. Revise Java MCQ topics.'
                ),
                'tasks': [
                    {
                        'subject': 'JAVA_MCQ',
                        'title': 'Revise Java strings, arrays, loops, methods, and basic OOP',
                        'resource_url': None,
                        'resource_label': '',
                        'order': 1,
                    },
                    {
                        'subject': 'JAVA_15',
                        'title': 'Solve Valid Palindrome',
                        'resource_url': 'https://leetcode.com/problems/valid-palindrome/',
                        'resource_label': 'LeetCode #125',
                        'order': 2,
                    },
                    {
                        'subject': 'JAVA_15',
                        'title': 'Solve Second Largest in Array',
                        'resource_url': 'https://www.geeksforgeeks.org/problems/second-largest3735/1',
                        'resource_label': 'GFG Problem',
                        'order': 3,
                    },
                    {
                        'subject': 'JAVA_15',
                        'title': 'Solve First Unique Character in a String',
                        'resource_url': 'https://leetcode.com/problems/first-unique-character-in-a-string/',
                        'resource_label': 'LeetCode #387',
                        'order': 4,
                    },
                    {
                        'subject': 'JAVA_MCQ',
                        'title': 'Practise 15 Java MCQs on strings, arrays, loops, constructors, and output prediction',
                        'resource_url': None,
                        'resource_label': '',
                        'order': 5,
                    },
                ],
            },
            {
                'date': datetime.date(2026, 10, 14),
                'title': 'Day 2 — Java Coding and Advanced Practice',
                'focus_summary': (
                    'Deep dive into Java OOP: classes, constructors, ArrayList. '
                    'Tackle 35-mark style class-based problems and more 15-mark warm-ups. '
                    'Revise OOP, inheritance, exceptions, and collections MCQs.'
                ),
                'tasks': [
                    {
                        'subject': 'JAVA_35',
                        'title': 'Revise classes, objects, constructors, getters/setters, static methods, and ArrayList',
                        'resource_url': None,
                        'resource_label': '',
                        'order': 1,
                    },
                    {
                        'subject': 'JAVA_35',
                        'title': 'Study the 35-Mark Complete Preparation Guide',
                        'resource_url': 'https://github.com/apoorv-jn24/TCS-IPA-PREPARATION/blob/main/06-Java-Coding/JAVA-35-MARKS-COMPLETE-GUIDE.md',
                        'resource_label': 'GitHub Guide',
                        'order': 2,
                    },
                    {
                        'subject': 'JAVA_35',
                        'title': 'Solve Class-Based Problem #1 involving objects, filtering, counting, and sorting',
                        'resource_url': 'https://github.com/apoorv-jn24/TCS-IPA-PREPARATION/blob/main/06-Java-Coding/JAVA-35-MARKS-COMPLETE-GUIDE.md',
                        'resource_label': 'GitHub 35M Guide',
                        'order': 3,
                    },
                    {
                        'subject': 'JAVA_35',
                        'title': 'Solve Class-Based Problem #2 involving objects, filtering, counting, and sorting',
                        'resource_url': 'https://github.com/apoorv-jn24/TCS-IPA-PREPARATION/blob/main/06-Java-Coding/JAVA-35-MARKS-COMPLETE-GUIDE.md',
                        'resource_label': 'GitHub 35M Guide',
                        'order': 4,
                    },
                    {
                        'subject': 'JAVA_15',
                        'title': 'Solve 15-Mark-Style Problem #1',
                        'resource_url': 'https://github.com/prince-kumar-singh/tcs-ipa-resources/tree/main/Important-Java-Program--IPA-15Marks-master',
                        'resource_label': 'GitHub 15M Repo',
                        'order': 5,
                    },
                    {
                        'subject': 'JAVA_15',
                        'title': 'Solve 15-Mark-Style Problem #2',
                        'resource_url': 'https://github.com/prince-kumar-singh/tcs-ipa-resources/tree/main/Important-Java-Program--IPA-15Marks-master',
                        'resource_label': 'GitHub 15M Repo',
                        'order': 6,
                    },
                    {
                        'subject': 'JAVA_MCQ',
                        'title': 'Practise 20 Java MCQs on OOP, inheritance, overloading, overriding, exceptions, and collections',
                        'resource_url': None,
                        'resource_label': '',
                        'order': 7,
                    },
                ],
            },
            {
                'date': datetime.date(2026, 10, 15),
                'title': 'Day 3 — All Other Sections and Final Mock',
                'focus_summary': (
                    'Cover BS, UI, Unix, SQL MCQs. Complete a full timed 70-minute coding mock. '
                    'Identify and fix weak areas before exam day.'
                ),
                'tasks': [
                    {
                        'subject': 'BS_MCQ',
                        'title': 'Practise 25 MCQs on communication, workplace ethics, professional conduct, and KYT (Know Your TCS)',
                        'resource_url': None,
                        'resource_label': '',
                        'order': 1,
                    },
                    {
                        'subject': 'UI_MCQ',
                        'title': 'Practise 5 MCQs on HTML, CSS, JavaScript, and related syllabus topics',
                        'resource_url': None,
                        'resource_label': '',
                        'order': 2,
                    },
                    {
                        'subject': 'UNIX_MCQ',
                        'title': 'Practise 5 MCQs on commands, file permissions, processes, and pipes',
                        'resource_url': None,
                        'resource_label': '',
                        'order': 3,
                    },
                    {
                        'subject': 'SQL_MCQ',
                        'title': 'Practise 5 MCQs on joins, aggregate functions, GROUP BY, HAVING, and subqueries',
                        'resource_url': None,
                        'resource_label': '',
                        'order': 4,
                    },
                    {
                        'subject': 'JAVA_35',
                        'title': 'Complete a timed mock consisting of one 15-mark and one 35-mark problem in 70 minutes',
                        'resource_url': None,
                        'resource_label': '',
                        'order': 5,
                    },
                    {
                        'subject': 'JAVA_15',
                        'title': 'Review coding errors and repeat the weakest problem without notes',
                        'resource_url': None,
                        'resource_label': '',
                        'order': 6,
                    },
                ],
            },
            {
                'date': datetime.date(2026, 10, 16),
                'title': 'Day 4 — Exam Day 🎯',
                'focus_summary': (
                    'Light revision only. No new topics. Check gear: laptop, camera, internet. '
                    'Stay calm, trust the preparation, read questions carefully before coding.'
                ),
                'tasks': [
                    {
                        'subject': 'JAVA_35',
                        'title': 'Revise Java syntax, OOP, and coding mistakes',
                        'resource_url': None,
                        'resource_label': '',
                        'order': 1,
                    },
                    {
                        'subject': 'BS_MCQ',
                        'title': 'Review key concepts from UI, Unix, SQL, and Business Skills',
                        'resource_url': None,
                        'resource_label': '',
                        'order': 2,
                    },
                    {
                        'subject': 'UNIX_MCQ',
                        'title': 'Check the assessment launcher, camera, and internet connection',
                        'resource_url': None,
                        'resource_label': '',
                        'order': 3,
                    },
                ],
            },
        ]

        day_map = {}
        for dd in days_data:
            day_obj, day_created = StudyDay.objects.update_or_create(
                date=dd['date'],
                defaults={
                    'title': dd['title'],
                    'focus_summary': dd['focus_summary'],
                },
            )
            day_map[dd['date']] = day_obj
            verb = 'Created' if day_created else 'Updated'
            self.stdout.write(f'  {verb} StudyDay: {day_obj}')

            for t in dd['tasks']:
                subject_obj = subject_map[t['subject']]
                task_obj, t_created = Task.objects.get_or_create(
                    day=day_obj,
                    subject=subject_obj,
                    title=t['title'],
                    defaults={
                        'resource_url': t.get('resource_url'),
                        'resource_label': t.get('resource_label', ''),
                        'order': t.get('order', 0),
                    },
                )
                verb2 = 'Created' if t_created else 'Exists'
                self.stdout.write(f'    {verb2} Task: {task_obj}')

        # ------------------------------------------------------------------ #
        # 3. CODING PRACTICE RECORDS                                           #
        # ------------------------------------------------------------------ #
        coding_data = [
            {
                'title': 'Valid Palindrome',
                'category': CodingPractice.CAT_15,
                'url': 'https://leetcode.com/problems/valid-palindrome/',
                'day_date': datetime.date(2026, 10, 13),
                'key_edge_cases': (
                    'Use two-pointer approach on cleaned string. '
                    'Edge case: empty string after removing non-alphanumeric chars returns true. '
                    'Character.isLetterOrDigit() + Character.toLowerCase() in Java.'
                ),
            },
            {
                'title': 'Second Largest in Array',
                'category': CodingPractice.CAT_15,
                'url': 'https://www.geeksforgeeks.org/problems/second-largest3735/1',
                'day_date': datetime.date(2026, 10, 13),
                'key_edge_cases': (
                    'Handle arrays with all identical elements (return -1). '
                    'Single element array edge case. '
                    'Avoid using sort — O(n) single pass with two variables.'
                ),
            },
            {
                'title': 'First Unique Character in a String',
                'category': CodingPractice.CAT_15,
                'url': 'https://leetcode.com/problems/first-unique-character-in-a-string/',
                'day_date': datetime.date(2026, 10, 13),
                'key_edge_cases': (
                    'Use int[26] frequency array for O(n). '
                    'Second pass finds first char with freq == 1. '
                    'Return -1 if none found. All lowercase letters assumed.'
                ),
            },
            {
                'title': '15-Mark-Style Problem #1 (TCS IPA Pattern)',
                'category': CodingPractice.CAT_15,
                'url': 'https://github.com/prince-kumar-singh/tcs-ipa-resources/tree/main/Important-Java-Program--IPA-15Marks-master',
                'day_date': datetime.date(2026, 10, 14),
                'key_edge_cases': (
                    'Scanner.nextLine() buffer flush trap after nextInt(). '
                    'Always call sc.nextLine() to consume the leftover newline before reading strings. '
                    'Use equalsIgnoreCase() for case-insensitive string comparison.'
                ),
            },
            {
                'title': '15-Mark-Style Problem #2 (TCS IPA Pattern)',
                'category': CodingPractice.CAT_15,
                'url': 'https://github.com/prince-kumar-singh/tcs-ipa-resources/tree/main/Important-Java-Program--IPA-15Marks-master',
                'day_date': datetime.date(2026, 10, 14),
                'key_edge_cases': (
                    'Check for null/empty arrays before looping. '
                    'Watch for ArrayIndexOutOfBoundsException on boundary values. '
                    'Integer.parseInt() throws NumberFormatException — wrap in try-catch if parsing user input.'
                ),
            },
            {
                'title': 'Class-Based OOP Problem #1 (Objects, Filtering, Counting, Sorting)',
                'category': CodingPractice.CAT_35,
                'url': 'https://github.com/apoorv-jn24/TCS-IPA-PREPARATION/blob/main/06-Java-Coding/JAVA-35-MARKS-COMPLETE-GUIDE.md',
                'day_date': datetime.date(2026, 10, 14),
                'key_edge_cases': (
                    'Define class with private fields + public getters/setters. '
                    'Use ArrayList<YourClass> to store objects. '
                    'Collections.sort() with Comparator lambda for sorting. '
                    'Stream().filter() or manual loop for filtering. '
                    'toString() override for clean output.'
                ),
            },
            {
                'title': 'Class-Based OOP Problem #2 (Objects, Filtering, Counting, Sorting)',
                'category': CodingPractice.CAT_35,
                'url': 'https://github.com/apoorv-jn24/TCS-IPA-PREPARATION/blob/main/06-Java-Coding/JAVA-35-MARKS-COMPLETE-GUIDE.md',
                'day_date': datetime.date(2026, 10, 14),
                'key_edge_cases': (
                    'Static counter variable for counting instances. '
                    'Parameterized constructor sets all fields. '
                    'Avoid NullPointerException when checking String fields. '
                    'Use Comparator.comparing() for multi-field sorting.'
                ),
            },
            {
                'title': '70-Minute Timed Mock (15M + 35M Combined)',
                'category': CodingPractice.CAT_FUNDAMENTALS,
                'url': 'https://github.com/apoorv-jn24/TCS-IPA-PREPARATION/blob/main/06-Java-Coding/JAVA-35-MARKS-COMPLETE-GUIDE.md',
                'day_date': datetime.date(2026, 10, 15),
                'key_edge_cases': (
                    'Budget: 20 mins for 15M + 50 mins for 35M. '
                    'Read the full problem before writing any code. '
                    'Test with given sample input first. '
                    'Leave 5 mins buffer for compilation and edge case testing.'
                ),
            },
        ]

        for cd in coding_data:
            day_obj = day_map.get(cd['day_date'])
            cp_obj, c_created = CodingPractice.objects.get_or_create(
                title=cd['title'],
                defaults={
                    'category': cd['category'],
                    'url': cd['url'],
                    'day': day_obj,
                    'key_edge_cases': cd['key_edge_cases'],
                },
            )
            verb = 'Created' if c_created else 'Exists'
            self.stdout.write(f'  {verb} CodingPractice: {cp_obj}')

        # ------------------------------------------------------------------ #
        # 4. STARTER MISTAKE LOGS                                              #
        # ------------------------------------------------------------------ #
        mistakes_data = [
            {
                'subject_code': 'JAVA_35',
                'topic_or_question': 'Scanner newline buffer trap in 35-mark problems',
                'what_went_wrong': (
                    'Called sc.nextInt() or sc.nextDouble() to read a number, then immediately called '
                    'sc.nextLine() to read a string — got an empty string instead of the actual input.'
                ),
                'correct_concept_or_fix': (
                    'After any sc.nextInt() / sc.nextDouble() / sc.nextLong(), always insert a dummy '
                    'sc.nextLine() call to consume the leftover newline character in the buffer BEFORE '
                    'calling sc.nextLine() for actual string input. '
                    'Example: int n = sc.nextInt(); sc.nextLine(); // flush\\nString s = sc.nextLine();'
                ),
            },
            {
                'subject_code': 'SQL_MCQ',
                'topic_or_question': 'WHERE vs HAVING with aggregate functions',
                'what_went_wrong': (
                    'Used WHERE clause to filter on COUNT() / SUM() / AVG() result — '
                    'got a SQL error because WHERE executes before GROUP BY and cannot reference aggregates.'
                ),
                'correct_concept_or_fix': (
                    'WHERE filters individual rows BEFORE grouping. '
                    'HAVING filters groups AFTER GROUP BY and CAN reference aggregate functions. '
                    'Rule: "If you need COUNT/SUM/AVG in the condition, use HAVING, not WHERE." '
                    'Example: SELECT dept, COUNT(*) FROM emp GROUP BY dept HAVING COUNT(*) > 5;'
                ),
            },
        ]

        for md in mistakes_data:
            subject_obj = subject_map[md['subject_code']]
            m_obj, m_created = MistakeLog.objects.get_or_create(
                subject=subject_obj,
                topic_or_question=md['topic_or_question'],
                defaults={
                    'what_went_wrong': md['what_went_wrong'],
                    'correct_concept_or_fix': md['correct_concept_or_fix'],
                },
            )
            verb = 'Created' if m_created else 'Exists'
            self.stdout.write(f'  {verb} MistakeLog: {m_obj}')

        # ------------------------------------------------------------------ #
        # Done                                                                 #
        # ------------------------------------------------------------------ #
        self.stdout.write(self.style.SUCCESS('\n✅ Seed complete! All records created/verified.'))
        self.stdout.write(self.style.SUCCESS(
            f'  Subjects: {Subject.objects.count()} | '
            f'StudyDays: {StudyDay.objects.count()} | '
            f'Tasks: {Task.objects.count()} | '
            f'CodingPractices: {CodingPractice.objects.count()} | '
            f'MistakeLogs: {MistakeLog.objects.count()}'
        ))
