from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import csv
from datetime import datetime
from django.http import HttpResponse
from django.db.models import Avg
from apps.attendance.models import Attendance

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_csv_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    user_id = request.GET.get('user_id')

    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    except ValueError:
        return HttpResponse("Invalid date format. Use YYYY-MM-DD", status=400)

    records = Attendance.objects.all()
    if start_date_obj:
        records = records.filter(check_in__date__gte=start_date_obj)
    if end_date_obj:
        records = records.filter(check_in__date__lte=end_date_obj)
    if user_id:
        records = records.filter(user__user_id=user_id)

    total_attendances = records.count()
    avg_duration = records.aggregate(avg_duration=Avg('duration'))['avg_duration']
    avg_duration_str = str(avg_duration) if avg_duration else "N/A"

    response = HttpResponse(content_type='text/csv')
    filename = f"attendance_report_{start_date}_{end_date}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(["Total Attendances", total_attendances])
    writer.writerow(["Average Working Time", avg_duration_str])
    writer.writerow([])
    writer.writerow(["First Name", "Last Name", "Email", "Role", "Check-in", "Check-out", "Duration"])

    for attendance in records.select_related('user'):
        check_in = attendance.check_in.strftime("%Y-%m-%d %H:%M") if attendance.check_in else ""
        check_out = attendance.check_out.strftime("%Y-%m-%d %H:%M") if attendance.check_out else "Still in office"
        duration = str(attendance.duration) if attendance.duration else "N/A"
        writer.writerow([
            attendance.user.first_name,
            attendance.user.last_name,
            attendance.user.email,
            attendance.user.role,
            check_in,
            check_out,
            duration,
        ])

    return response
