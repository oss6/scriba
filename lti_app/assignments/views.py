from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from lti_app.assignments import services


def show_content(request):
    is_instructor = request.session.get('is_instructor')
    template = 'teacher/index.html' if is_instructor else 'learner/index.html'
    return render(request, template)


def submit_assignment(request):
    assm_description = request.session.get('assignment_description')
    assm_type = request.session.get('assignment_type')
    assm_points_possible = request.session.get('assignment_points_possible')
    service_url = request.session.get('lis_outcome_service_url')
    source_did = request.session.get('lis_result_sourcedid')

    service = services.AssignmentService(
        assm_description,
        assm_type,
        assm_points_possible,
        service_url,
        source_did
    )

    data = service.run_analysis(request.POST.get('text'))

    print(data)

    template = (
        'learner/feedback.html'
        if assm_type == 'pilot'
        else 'learner/submission-confirmation.html'
    )

    return render(request, template, data)


@require_http_methods(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        return show_content(request)
    else:
        return submit_assignment(request)