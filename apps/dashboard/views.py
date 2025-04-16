# apps/dashboard/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Avg, Sum
import datetime

from apps.attendance.models import Attendance
from apps.users.models import User

class DashboardDataView(APIView):
    def get(self, request):
        now = timezone.now()
        week_ago = now - datetime.timedelta(days=7)

        qs = Attendance.objects.filter(check_in__gte=week_ago)

        # graph 1 - office visits by hour
        chart_hours = []
        for hour in range(8, 21):
            count = 0
            for attend in qs:
                ci = attend.check_in
                co = attend.check_out
                if co is None:
                    co = now
                if ci.hour <= hour < co.hour:
                    count += 1
            
            chart_hours.append({"hour": hour, "count": count})

        # graph 2 - average check in check out times
        day_name = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_stats = {i: {"arrivals": [], "departures": []} for i in range(7)}

        for attend in qs:
            wd = attend.check_in.weekday()
            arrival_hour = attend.check_in.hour + attend.check_in.minute/60
            day_stats[wd]["arrivals"].append(arrival_hour)

            if attend.check_out:
                departure_hour = attend.check_out.hour + attend.check_out.minute/60
                day_stats[wd]["departures"].append(departure_hour)

        chart_time_stats = []
        for wd, info in day_stats.items():
            arr_list = info["arrivals"]
            dep_list = info["departures"]
            if arr_list:
                avg_arr = sum(arr_list) / len(arr_list)
            else:
                avg_arr = None
            if dep_list:
                avg_dep = sum(dep_list) / len(dep_list)
            else:
                avg_dep = None
            
            chart_time_stats.append({
                "day": day_name[wd],
                "arrival": round(avg_arr, 2) if avg_arr else None,
                "departure": round(avg_dep, 2) if avg_dep else None,
            })

        leaderboard_data = []

        # graph 3 - leaderboard
        user_sums = qs.filter(duration__isnull=False) \
                      .values("user_id") \
                      .annotate(total_dur=Sum("duration")) \
                      .order_by("-total_dur")[:5]

        for row in user_sums:
            hours = row["total_dur"].total_seconds() / 3600
            try:
                usr = User.objects.get(user_id=row["user_id"])
                leaderboard_data.append({
                    "name": f"{usr.first_name} {usr.last_name}",
                    "hours": round(hours, 2)
                })
            except User.DoesNotExist:
                pass

        data = {
            "chart_hours": chart_hours,
            "chart_time_stats": chart_time_stats,
            "chart_leaderboard": leaderboard_data,
        }
        return Response(data, status=status.HTTP_200_OK)
