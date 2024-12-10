from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from app.models.utils import Color, ColorBase
from app.db import SessionDep

router = APIRouter()


@router.post(
    "/colors/",
    response_model=Color,
    status_code=status.HTTP_201_CREATED,
    tags=["Colors"],
)
def create_color(color: ColorBase, session: SessionDep):
    existing_color = session.exec(
        select(Color).where(Color.abbrev == color.abbrev)
    ).first()
    if existing_color:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A color with the same abbreviation already exists.",
        )
    new_color = Color.from_orm(color)
    session.add(new_color)
    session.commit()
    session.refresh(new_color)
    return new_color


@router.delete(
    "/colors/{color_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Colors"]
)
def delete_color(color_id: int, session: SessionDep):
    color = session.get(Color, color_id)
    if not color:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Color not found.",
        )
    session.delete(color)
    session.commit()
    return {"detail": "Color deleted successfully."}


@router.get("/colors/", response_model=list[Color], tags=["Colors"])
def get_colors(session: SessionDep):
    colors = session.exec(select(Color)).all()
    return colors


from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select
from app.models.utils import Chart, ChartBase
from app.db import SessionDep


@router.post(
    "/charts/",
    response_model=Chart,
    status_code=status.HTTP_201_CREATED,
    tags=["Charts"],
)
def create_chart(chart: ChartBase, session: SessionDep):
    existing_chart = session.exec(
        select(Chart).where(Chart.abbrev == chart.abbrev)
    ).first()
    if existing_chart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A chart with the same abbreviation already exists.",
        )
    new_chart = Chart.from_orm(chart)
    session.add(new_chart)
    session.commit()
    session.refresh(new_chart)
    return new_chart


@router.delete(
    "/charts/{chart_type}", status_code=status.HTTP_204_NO_CONTENT, tags=["Charts"]
)
def delete_chart(chart_type: int, session: SessionDep):
    chart = session.get(Chart, chart_type)
    if not chart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chart not found.",
        )
    session.delete(chart)
    session.commit()
    return {"detail": "Chart deleted successfully."}


@router.get("/charts/", response_model=list[Chart], tags=["Charts"])
def get_charts(session: SessionDep):
    charts = session.exec(select(Chart)).all()
    return charts
