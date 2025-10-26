from app.utils.constants import DEF_THEME

fake_users_db = {
    "user@example.com": {
        "name": "User Example",
        "email": "user@example.com",
        "password": "password123",
        "avatarURL": f"https://res.cloudinary.com/demo/image/upload/defavatar{DEF_THEME.lower()}1x.jpg",
        "theme": DEF_THEME,
    }
}
