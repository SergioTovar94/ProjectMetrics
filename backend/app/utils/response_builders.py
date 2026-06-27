from app.models.activity import Activity
from app.models.project import Project
from app.schemas.activity import ActivityResponse
from app.schemas.common import EVMIndicators
from app.schemas.project import ProjectResponse
from app.services.evm_service import EVMCalculator


def build_activity_response(activity: Activity) -> ActivityResponse:
    evm = EVMCalculator.calculate_activity_evm(
        activity_id=activity.id,
        name=activity.name,
        bac=float(activity.bac),
        planned_progress=float(activity.planned_progress),
        actual_progress=float(activity.actual_progress),
        ac=float(activity.ac),
    )

    return ActivityResponse(
        id=activity.id,
        project_id=activity.project_id,
        name=activity.name,
        bac=float(activity.bac),
        planned_progress=float(activity.planned_progress),
        actual_progress=float(activity.actual_progress),
        ac=float(activity.ac),
        created_at=activity.created_at,
        updated_at=activity.updated_at,
        evm=EVMIndicators(
            bac=evm.bac,
            pv=evm.pv,
            ev=evm.ev,
            ac=evm.ac,
            cv=evm.cv,
            sv=evm.sv,
            cpi=evm.cpi,
            spi=evm.spi,
            eac=evm.eac,
            vac=evm.vac,
            cost_status=evm.cost_status,
            schedule_status=evm.schedule_status,
        ),
    )


def build_project_response(project: Project) -> ProjectResponse:
    activities_data = [
        {
            "id": act.id,
            "name": act.name,
            "bac": float(act.bac),
            "planned_progress": float(act.planned_progress),
            "actual_progress": float(act.actual_progress),
            "ac": float(act.ac),
        }
        for act in project.activities
    ]

    evm_result = EVMCalculator.calculate_project_evm(
        project_id=project.id,
        project_name=project.name,
        activities_data=activities_data,
    )

    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        created_at=project.created_at,
        activities=[
            build_activity_response(activity) for activity in project.activities
        ],
        evm=EVMIndicators(
            bac=evm_result.bac,
            pv=evm_result.pv,
            ev=evm_result.ev,
            ac=evm_result.ac,
            cv=evm_result.cv,
            sv=evm_result.sv,
            cpi=evm_result.cpi,
            spi=evm_result.spi,
            eac=evm_result.eac,
            vac=evm_result.vac,
            cost_status=evm_result.cost_status,
            schedule_status=evm_result.schedule_status,
        ),
    )
