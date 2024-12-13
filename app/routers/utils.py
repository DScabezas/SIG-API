from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from typing import List

from app.models.utils import Color, ColorBase, Chart, ChartBase, Icon, IconBase
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
    new_color = Color.model_validate(color)
    session.add(new_color)
    session.commit()
    session.refresh(new_color)
    return new_color


@router.delete(
    "/colors/{color_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Colors"],
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
    return


@router.get(
    "/colors/",
    response_model=List[Color],
    tags=["Colors"],
)
def get_colors(session: SessionDep):
    colors = session.exec(select(Color)).all()
    return colors


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
    new_chart = Chart.model_validate(chart)
    session.add(new_chart)
    session.commit()
    session.refresh(new_chart)
    return new_chart


@router.delete(
    "/charts/{chart_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Charts"],
)
def delete_chart(chart_id: int, session: SessionDep):
    chart = session.get(Chart, chart_id)
    if not chart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chart not found.",
        )
    session.delete(chart)
    session.commit()
    return


@router.get(
    "/charts/",
    response_model=List[Chart],
    tags=["Charts"],
)
def get_charts(session: SessionDep):
    charts = session.exec(select(Chart)).all()
    return charts


@router.post(
    "/icons/",
    response_model=Icon,
    status_code=status.HTTP_201_CREATED,
    tags=["Icons"],
)
def create_icon(icon: IconBase, session: SessionDep):
    existing_icon = session.exec(select(Icon).where(Icon.abbrev == icon.abbrev)).first()
    if existing_icon:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An icon with the same abbreviation already exists.",
        )
    new_icon = Icon.model_validate(icon)
    session.add(new_icon)
    session.commit()
    session.refresh(new_icon)
    return new_icon


@router.delete(
    "/icons/{icon_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Icons"],
)
def delete_icon(icon_id: int, session: SessionDep):
    icon = session.get(Icon, icon_id)
    if not icon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Icon not found.",
        )
    session.delete(icon)
    session.commit()
    return


@router.get(
    "/icons/",
    response_model=List[Icon],
    tags=["Icons"],
)
def get_icons(session: SessionDep):
    icons = session.exec(select(Icon)).all()
    return icons


@router.put(
    "/{icon_id}", response_model=Icon, status_code=status.HTTP_200_OK, tags=["Icons"]
)
def update_icon_handler(icon_id: int, icon: IconBase, session: SessionDep) -> Icon:
    db_icon = session.exec(select(Icon).where(Icon.id == icon_id)).first()
    if not db_icon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Icon not found"
        )

    icon_data = icon.model_dump(exclude_unset=True)

    for key, value in icon_data.items():
        setattr(db_icon, key, value)

    session.commit()
    session.refresh(db_icon)

    return db_icon
