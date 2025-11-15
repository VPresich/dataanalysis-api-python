from jinja2 import Template
from fastapi import HTTPException
from sqlalchemy import select
from app.database import get_db_session
from app.models import User
from app.utils import send_mail, get_template_path


async def send_token(email: str, subject_email: str, redirect: str, template_name: str):
    """
    Send a verification email with a verification token via Brevo (using SQLAlchemy).
    The controller knows nothing about database sessions — the service manages them internally.
    """
    async with get_db_session() as session:
        result = await session.execute(select(User).where(User.email == email))

        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if the email template exists
        template_path = get_template_path(template_name)

        # Load and compile the template
        template_source = template_path.read_text(encoding="utf-8")
        template = Template(template_source)

        # Render HTML content with the verification link
        html_content = template.render(
            name=user.name,
            link=redirect,
        )
        # Send the email
        try:
            await send_mail(
                to=email,
                subject=subject_email,
                html=html_content
            )
            print(f"Verification email sent to {email}")
        except Exception as err:
            print(f"Failed to send verification email: {err}")
            raise HTTPException(status_code=502, detail="Failed to send verification email")
