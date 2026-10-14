# TCS-CPA-IPA

TCS CPA/IPA Exam Preparation Tracker web application built with Django, Tailwind CSS, WhiteNoise, and Gunicorn.

## Features
- **Daily Study Plan**: Interactive checklist for the 4-day sprint leading up to the 16 Oct 2026 exam.
- **Java Coding Practice Hub**: Track 15-mark and 35-mark OOP problems, time taken, and key edge cases.
- **Syllabus & Weightage**: Track progress across all MCQ modules (Business Skills, Java, UI, Unix, SQL).
- **Mistake & Revision Notebook**: Record traps and mistakes from mock tests to avoid repeating them.
- **Mock Exam Timer**: Built-in 70-min coding and 50-min MCQ timers.

## Setup & Running Locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
