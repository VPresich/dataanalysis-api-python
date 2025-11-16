import os

REQUIRE_EMAIL_VERIFICATION = (
    os.getenv("REQUIRE_EMAIL_VERIFICATION", "true").lower() == "true"
)

__all__ = ("REQUIRE_EMAIL_VERIFICATION",)
