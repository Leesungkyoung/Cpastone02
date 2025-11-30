from sqlalchemy import func, case, extract
from sqlalchemy.orm import Session
from ..models import Alert
import datetime
from calendar import monthrange
from typing import Optional

def get_summary_data(db: Session, period_type: str, month_str: Optional[str] = None):
    # Base query excludes '2008-11' data for all report types
    query = db.query(Alert).filter(func.strftime('%Y-%m', Alert.timestamp) != '2008-11')
    
    # Date filtering
    if period_type != 'all' and month_str:
        try:
            year, month = map(int, month_str.split('-'))
            start_date = datetime.date(year, month, 1)
            end_date = start_date.replace(day=monthrange(year, month)[1])
            query = query.filter(Alert.timestamp.between(
                datetime.datetime.combine(start_date, datetime.time.min),
                datetime.datetime.combine(end_date, datetime.time.max)
            ))
        except (ValueError, TypeError):
            # Fallback for invalid month_str or if not provided for relevant period_types
            pass

    # Determine grouping label
    if period_type == 'monthly':
        grouping_label = func.strftime('%Y-%m', Alert.timestamp)
    elif period_type == 'weekly':
        grouping_label = (extract('day', Alert.timestamp) - 1) / 7 + 1
    elif period_type == 'daily':
        grouping_label = func.strftime('%d', Alert.timestamp)
    else: # 'all'
        grouping_label = func.strftime('%Y-%m', Alert.timestamp)

    # Base aggregation
    subquery = query.subquery()
    
    aggregation = db.query(
        grouping_label.label('period'),
        func.count(subquery.c.id).label('total_defects'),
        func.sum(case((subquery.c.resolved == True, 1), else_=0)).label('resolved_count')
    ).group_by('period').order_by('period').all()

    # Process aggregated data
    chart_data = []
    total_production_all = 0
    total_defects_all = 0
    resolved_all = 0

    # This is a placeholder for raw production data.
    # In a real scenario, this should come from another table/source.
    # For now, we estimate it based on defect rate.
    ASSUMED_DEFECT_RATE = 0.05 

    for row in aggregation:
        period_name = f"{int(row.period)}주차" if period_type == 'weekly' else (f"{row.period}일" if period_type == 'daily' else str(row.period))
        
        total_defects = row.total_defects
        resolved_count = row.resolved_count
        
        # Estimate production based on defects
        total_production = int(total_defects / ASSUMED_DEFECT_RATE) if ASSUMED_DEFECT_RATE > 0 else 0
        normal_production = total_production - total_defects
        
        # Calculate quality metrics based on user's rule (10% false alarm)
        false_alarms = int(resolved_count * 0.10)
        confirmed_defects = resolved_count - false_alarms
        unresolved = total_defects - resolved_count

        chart_data.append({
            "name": period_name,
            "정상 제품": normal_production,
            "불량 의심": total_defects,
            "확정 불량": confirmed_defects,
            "오경보": false_alarms,
            "미조치": unresolved,
        })
        
        total_production_all += total_production
        total_defects_all += total_defects
        resolved_all += resolved_count

    # Calculate overall KPIs
    false_alarms_all = int(resolved_all * 0.10)
    confirmed_defects_all = resolved_all - false_alarms_all
    unresolved_all = total_defects_all - resolved_all

    return {
        "production_overview": {
            "total_production": total_production_all,
            "total_defects": total_defects_all,
            "defect_rate": (total_defects_all / total_production_all * 100) if total_production_all > 0 else 0,
            "chart_data": chart_data
        },
        "alert_quality": {
            "total_defects": total_defects_all,
            "confirmed_defects": confirmed_defects_all,
            "false_alarms": false_alarms_all,
            "unresolved": unresolved_all,
            "resolution_rate": (resolved_all / total_defects_all * 100) if total_defects_all > 0 else 0,
            "false_alarm_rate": (false_alarms_all / total_defects_all * 100) if total_defects_all > 0 else 0,
            "chart_data": chart_data
        }
    }
