"""
Views for TCS CPA/IPA Exam Preparation Tracker.
All AJAX endpoints return JSON; the dashboard view returns HTML.
"""
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Subject, StudyDay, Task, CodingPractice, MistakeLog


# ---------------------------------------------------------------------------
# Helper: compute overall stats
# ---------------------------------------------------------------------------
def _compute_stats():
    all_tasks = Task.objects.all()
    total = all_tasks.count()
    completed = all_tasks.filter(is_completed=True).count()
    pct = round((completed / total) * 100) if total else 0
    return {'total': total, 'completed': completed, 'pending': total - completed, 'pct': pct}


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
def dashboard(request):
    study_days = StudyDay.objects.prefetch_related(
        'tasks__subject', 'coding_practices'
    ).all()

    subjects = Subject.objects.prefetch_related('tasks').all()

    coding_practices = CodingPractice.objects.select_related('day').all()
    mistakes = MistakeLog.objects.select_related('subject').all()

    stats = _compute_stats()

    mcq_subjects = subjects.filter(section_type=Subject.SECTION_MCQ)
    coding_subjects = subjects.filter(section_type=Subject.SECTION_CODING)

    context = {
        'study_days': study_days,
        'subjects': subjects,
        'mcq_subjects': mcq_subjects,
        'coding_subjects': coding_subjects,
        'coding_practices': coding_practices,
        'mistakes': mistakes,
        'stats': stats,
        'all_subjects': subjects,  # for forms
    }
    return render(request, 'tracker/dashboard.html', context)


# ---------------------------------------------------------------------------
# AJAX: Toggle Task Completion
# ---------------------------------------------------------------------------
@require_POST
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_completed = not task.is_completed
    task.save()

    # Recompute stats for the day, subject, and overall
    day = task.day
    subject = task.subject
    overall = _compute_stats()

    return JsonResponse({
        'success': True,
        'task_id': task.id,
        'is_completed': task.is_completed,
        'day_id': day.id,
        'day_completed': day.completed_tasks,
        'day_total': day.total_tasks,
        'day_pct': day.progress_pct,
        'subject_id': subject.id,
        'subject_code': subject.code,
        'subject_completed': subject.completed_tasks,
        'subject_total': subject.total_tasks,
        'subject_pct': subject.progress_pct,
        'overall_pct': overall['pct'],
        'overall_completed': overall['completed'],
        'overall_total': overall['total'],
        'overall_pending': overall['pending'],
    })


# ---------------------------------------------------------------------------
# AJAX: Save Task Note
# ---------------------------------------------------------------------------
@require_POST
def save_task_note(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    try:
        data = json.loads(request.body)
        task.notes = data.get('notes', '').strip()
    except json.JSONDecodeError:
        task.notes = request.POST.get('notes', '').strip()
    task.save()
    return JsonResponse({'success': True, 'task_id': task.id, 'notes': task.notes})


# ---------------------------------------------------------------------------
# AJAX: Add Custom Task
# ---------------------------------------------------------------------------
@require_POST
def add_task(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST

    day_id = data.get('day_id')
    subject_id = data.get('subject_id')
    title = data.get('title', '').strip()
    resource_url = data.get('resource_url', '').strip() or None
    resource_label = data.get('resource_label', '').strip()

    if not all([day_id, subject_id, title]):
        return JsonResponse({'success': False, 'error': 'Missing required fields.'}, status=400)

    day = get_object_or_404(StudyDay, id=day_id)
    subject = get_object_or_404(Subject, id=subject_id)

    task = Task.objects.create(
        day=day,
        subject=subject,
        title=title,
        resource_url=resource_url,
        resource_label=resource_label,
        order=Task.objects.filter(day=day).count(),
    )

    overall = _compute_stats()
    return JsonResponse({
        'success': True,
        'task': {
            'id': task.id,
            'title': task.title,
            'is_completed': task.is_completed,
            'resource_url': task.resource_url,
            'resource_label': task.resource_label,
            'subject_code': subject.code,
            'subject_id': subject.id,
            'day_id': day.id,
            'notes': task.notes,
        },
        'day_total': day.total_tasks,
        'day_completed': day.completed_tasks,
        'day_pct': day.progress_pct,
        'overall_pct': overall['pct'],
        'overall_completed': overall['completed'],
        'overall_total': overall['total'],
        'overall_pending': overall['pending'],
    })


# ---------------------------------------------------------------------------
# AJAX: Update Coding Practice
# ---------------------------------------------------------------------------
@require_POST
def update_coding_practice(request, cp_id):
    cp = get_object_or_404(CodingPractice, id=cp_id)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST

    if 'status' in data:
        cp.status = data['status']
    if 'time_taken_mins' in data and data['time_taken_mins']:
        try:
            cp.time_taken_mins = int(data['time_taken_mins'])
        except (ValueError, TypeError):
            pass
    if 'key_edge_cases' in data:
        cp.key_edge_cases = data['key_edge_cases'].strip()
    cp.save()

    return JsonResponse({
        'success': True,
        'id': cp.id,
        'status': cp.status,
        'status_display': cp.get_status_display(),
        'time_taken_mins': cp.time_taken_mins,
        'key_edge_cases': cp.key_edge_cases,
    })


# ---------------------------------------------------------------------------
# AJAX: Add Coding Practice
# ---------------------------------------------------------------------------
@require_POST
def add_coding_practice(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST

    title = data.get('title', '').strip()
    category = data.get('category', CodingPractice.CAT_15)
    url = data.get('url', '').strip()
    key_edge_cases = data.get('key_edge_cases', '').strip()

    if not all([title, url]):
        return JsonResponse({'success': False, 'error': 'Title and URL are required.'}, status=400)

    cp = CodingPractice.objects.create(
        title=title,
        category=category,
        url=url,
        key_edge_cases=key_edge_cases,
        status=CodingPractice.STATUS_PENDING,
    )
    return JsonResponse({
        'success': True,
        'id': cp.id,
        'title': cp.title,
        'category': cp.category,
        'category_display': cp.get_category_display(),
        'url': cp.url,
        'status': cp.status,
        'status_display': cp.get_status_display(),
        'key_edge_cases': cp.key_edge_cases,
    })


# ---------------------------------------------------------------------------
# AJAX: Add Mistake Log
# ---------------------------------------------------------------------------
@require_POST
def add_mistake(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST

    subject_id = data.get('subject_id')
    topic = data.get('topic_or_question', '').strip()
    wrong = data.get('what_went_wrong', '').strip()
    fix = data.get('correct_concept_or_fix', '').strip()

    if not all([subject_id, topic, wrong, fix]):
        return JsonResponse({'success': False, 'error': 'All fields are required.'}, status=400)

    subject = get_object_or_404(Subject, id=subject_id)
    mistake = MistakeLog.objects.create(
        subject=subject,
        topic_or_question=topic,
        what_went_wrong=wrong,
        correct_concept_or_fix=fix,
    )
    return JsonResponse({
        'success': True,
        'id': mistake.id,
        'subject_code': subject.code,
        'subject_name': subject.name,
        'topic_or_question': mistake.topic_or_question,
        'what_went_wrong': mistake.what_went_wrong,
        'correct_concept_or_fix': mistake.correct_concept_or_fix,
        'is_resolved': mistake.is_resolved,
        'created_at': mistake.created_at.strftime('%d %b %Y'),
    })


# ---------------------------------------------------------------------------
# AJAX: Toggle Mistake Resolved
# ---------------------------------------------------------------------------
@require_POST
def toggle_mistake(request, mistake_id):
    mistake = get_object_or_404(MistakeLog, id=mistake_id)
    mistake.is_resolved = not mistake.is_resolved
    mistake.save()
    return JsonResponse({
        'success': True,
        'id': mistake.id,
        'is_resolved': mistake.is_resolved,
    })


# ---------------------------------------------------------------------------
# AJAX: Delete Mistake
# ---------------------------------------------------------------------------
@require_POST
def delete_mistake(request, mistake_id):
    mistake = get_object_or_404(MistakeLog, id=mistake_id)
    mistake.delete()
    return JsonResponse({'success': True, 'id': mistake_id})


# ---------------------------------------------------------------------------
# AJAX: Overall Progress Data (for live KPI refresh)
# ---------------------------------------------------------------------------
def get_progress_data(request):
    overall = _compute_stats()
    subjects_data = []
    for s in Subject.objects.prefetch_related('tasks').all():
        subjects_data.append({
            'id': s.id,
            'code': s.code,
            'completed': s.completed_tasks,
            'total': s.total_tasks,
            'pct': s.progress_pct,
        })
    days_data = []
    for d in StudyDay.objects.prefetch_related('tasks').all():
        days_data.append({
            'id': d.id,
            'completed': d.completed_tasks,
            'total': d.total_tasks,
            'pct': d.progress_pct,
        })
    return JsonResponse({
        'overall': overall,
        'subjects': subjects_data,
        'days': days_data,
    })
