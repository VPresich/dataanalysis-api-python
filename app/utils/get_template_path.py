from pathlib import Path
from app.utils.constants import TEMPLATES_DIR
from app.exceptions.custom_exception import CustomException


def get_template_path(template_name: str) -> Path:
    """
    Safely build an absolute path to a template file.
    Raises:
        CustomException: if the template file does not exist
    """
    base_dir = Path(TEMPLATES_DIR)
    template_path = base_dir / template_name

    if not template_path.exists():
        raise CustomException(
            name=f"Template '{template_name}' not found",
            status_code=500
        )

    return template_path
