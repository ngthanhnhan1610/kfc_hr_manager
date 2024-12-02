import pytz
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime

from employee.models import Employee

# Create your views here.
def timekeeping(request):
    return render(request, "timekeeping.html")

@login_required
def worksheet(request):
    current_date = datetime.now()
    current_month = current_date.strftime("%m")
    current_year = current_date.strftime("%Y")
    current_month_year = f"Tháng {current_month} / {current_year}"
    # current_month_year = "Tháng 11/2024"
    
    employee = Employee.objects.get(user=request.user)
    attendances = employee.attendance_set.all()
    # get all attendances of the current month
    # attendances = attendances.filter(date__month=11, date__year=current_year)
    attendances = attendances.filter(date__month=current_month, date__year=current_year)

    grid_display_attendances = []
    vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")

    if not attendances:
        return render(request, "worksheet.html", context={"current_month_year": current_month_year})
    for attendance in attendances:
        date = attendance.date
        formatted_date = date.strftime("%d/%m/%Y")
        
        if attendance.check_in and not attendance.check_out:
            check_in = datetime.combine(date, attendance.check_in)
            check_in = check_in.astimezone(vietnam_tz).strftime("%H:%M")
            
            # Initialize a flag to check if the date was found
            date_found = False

            # Iterate through the grid_display_attendances to find the matching date
            for index, display_attendance in enumerate(grid_display_attendances):
                if display_attendance["date"] == formatted_date:
                    display_attendance["check_in_middle"] = check_in
                    check_out_middle = display_attendance["check_out_last"]
                    if check_out_middle:
                        display_attendance["check_out_last"] = None
                        display_attendance["check_out_middle"] = check_out_middle
                    
                    display_attendance["total_hours"] = None
                    grid_display_attendances[index] = display_attendance
                    date_found = True
                    break

            # If the date was not found, append a new element
            if not date_found:
                grid_display_attendances.append(
                    {
                        "date": formatted_date,
                        "check_in_first": check_in,
                        "check_out_middle": None,
                        "check_in_middle": None,
                        "check_out_last": None,
                        "total_hours": None
                    }
                )
        elif attendance.check_in and attendance.check_out:
            check_in = datetime.combine(date, attendance.check_in)
            check_in = check_in.astimezone(vietnam_tz).strftime("%H:%M")
            check_out = datetime.combine(date, attendance.check_out)
            check_out = check_out.astimezone(vietnam_tz).strftime("%H:%M")

            date_found = False
            for index, display_attendance in enumerate(grid_display_attendances):
                if display_attendance["date"] == formatted_date:
                    # Update the existing record
                    checkout_middle = display_attendance["check_out_last"]
                    display_attendance["check_out_middle"] = checkout_middle
                    display_attendance["check_in_middle"] = check_in
                    display_attendance["check_out_last"] = check_out

                    # Calculate the total hours
                    time_format = "%H:%M"
                    check_in_first = datetime.strptime(display_attendance["check_in_first"], time_format) if display_attendance["check_in_first"] else None
                    check_out_middle = datetime.strptime(display_attendance["check_out_middle"], time_format) if display_attendance["check_out_middle"] else None
                    check_in_middle = datetime.strptime(display_attendance["check_in_middle"], time_format) if display_attendance["check_in_middle"] else None
                    check_out_last = datetime.strptime(display_attendance["check_out_last"], time_format) if display_attendance["check_out_last"] else None
                    
                    if check_in_first and check_out_middle and check_in_middle and check_out_last:
                        total_hours = (check_out_middle - check_in_first) + (check_out_last - check_in_middle)
                        display_attendance["total_hours"] = round(total_hours.total_seconds() / 3600, 1)
                    
                    
                    grid_display_attendances[index] = display_attendance
                    date_found = True
                    break

            # If the date was not found, append a new element
            if not date_found:
                # calculate total hours
                time_format = "%H:%M"
                check_in_first = datetime.strptime(check_in, time_format)
                check_out_last = datetime.strptime(check_out, time_format)
                total_hours = check_out_last - check_in_first
                total_hours = round(total_hours.total_seconds() / 3600, 1)
                
                grid_display_attendances.append(
                    {
                        "date": formatted_date,
                        "check_in_first": check_in,
                        "check_out_middle": None,
                        "check_in_middle": None,
                        "check_out_last": check_out,
                        "total_hours": total_hours
                    }
                )
            
        list_display_attendances = []
        for attendance in attendances:
            date = attendance.date
            formatted_date = date.strftime("%d/%m/%Y")
            check_in = attendance.check_in
            check_out = attendance.check_out
            if check_in and check_out:
                check_in = datetime.combine(date, attendance.check_in)
                check_in = check_in.astimezone(vietnam_tz).strftime("%H:%M:%S")
                check_out = datetime.combine(date, attendance.check_out)
                check_out = check_out.astimezone(vietnam_tz).strftime("%H:%M:%S")
            elif check_in:
                check_in = datetime.combine(date, attendance.check_in)
                check_in = check_in.astimezone(vietnam_tz).strftime("%H:%M:%S")
                check_out = None
            else:
                check_in = None
                check_out = None
            
            list_display_attendances.append(
                {
                    "date": formatted_date,
                    "check_in": check_in,
                    "check_out": check_out,
                }
            )
            # reverse the list to display the latest attendance first
            list_display_attendances = list_display_attendances[::-1]
            
    return render(request, "worksheet.html", context={
        "current_month_year": current_month_year,
        "grid_display_attendances": grid_display_attendances,
        "list_display_attendances": list_display_attendances,
    })
