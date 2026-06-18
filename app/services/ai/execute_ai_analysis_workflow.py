from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.models import Data
from app.schemas.ai_schema import AIChatResponse
from app.utils.ai_utils import send_to_llm_agent


async def run_ai_analysis(source_id: UUID, track_num: int, session: AsyncSession) -> dict:
    """
    Service: Extracts data trajectories, filters anomaly entries via query conditions,
    serializes structured records into context matrices, and targets the LLM node.
    """
    data_result = await session.execute(
        select(Data).where(
            (Data.id_source == source_id)
            & (Data.TrackNum == track_num)
            & (
                (Data.IMMconsistent == "0")
                | (Data.TrackConsistent == "0")
                | (Data.VelocityConsistent == "0")
            )
        )
    )
    records = data_result.scalars().all()

    if not records:
        output = AIChatResponse(
            status="success",
            response="AI Evaluation: No points violating consistency thresholds were discovered in the database for this track."
        )
        return output.model_dump()

    formatted_points = [
        f"Time: {r.Time}s | X: {r.X}, Y: {r.Y}, Z: {r.Z} | Speed: {r.speed} (vOK: {r.velocityOK}) | "
        f"IMM_consistent: {r.IMMconsistent} (Chi2_Value: {r.IMMconsistentValue}) | "
        f"Vel_consistent: {r.VelocityConsistent} | Track_consistent: {r.TrackConsistent} | "
        f"IMM_positive: {r.IMMpositive} | JPDA_prob: {r.probability} | "
        f"KDE: {r.Kde}, Gaussian: {r.Gaussian}"
        for r in records
    ]

    points_text = "\n".join(formatted_points)
    user_message = f"Analyze track number: {track_num}.\nAnomalous database data points:\n{points_text}"

    llm_content = await send_to_llm_agent(user_message)

    output = AIChatResponse(status="success", response=llm_content)
    return output.model_dump()
