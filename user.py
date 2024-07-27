from datetime import datetime
from typing import Optional, List


class Friend:
    types = {
        0: "❓",
        1: "👫",
        2: "⛔",
        3: "📨",
        4: "⏳",
    }

    def __init__(self, fetched_user: dict):
        self.id: int = fetched_user.get("id", 0)
        self.nickname = fetched_user.get("nickname", None)
        self.since = fetched_user.get("since", None)  # 2024-05-14T07:35:43.175000+00:00
        self.type = fetched_user.get("type", 0)
        self.user = fetched_user.get("user", {})
        self.avatar = self.user.get("avatar", None)
        self.clan = self.user.get("clan", None)
        self.global_name = self.user.get("global_name", None)
        self.public_flags = self.user.get("public_flags", None)
        self.username = self.user.get("username", None)

        self.is_bot = self.public_flags == 65536

        self.is_unknown = self.type == 0
        self.is_friend = self.type == 1
        self.is_blocked = self.type == 2
        self.is_incoming = self.type == 3
        self.is_pending = self.type == 4

        self.raw_date: datetime = datetime.fromisoformat(self.since[:-6]) if self.since else None

        self.icon_status = self.types.get(self.type, "❓")
        # FIXME: Not using DATE_FORMAT
        self.pretty_since = self.raw_date.strftime("%H:%M %d.%m.%Y") if self.raw_date else "N/A"

    def __str__(self):
        return f"{self.username} {self.icon_status}"

    def extended_str(self):
        if self.is_bot:
            return f"{self.username} (🤖)"
        return f"{self.icon_status} {self.username} \"{self.global_name}\""

    def full_str(self):
        result = ""
        for key, value in self.__dict__.items():
            if key == "user":
                continue
            result += f"{key}: {value}\n"
        return result


class MyUser:
    premium_types = {
        0: ("", "None"),
        1: ("🌟", "Nitro Classic"),
        2: ("💎", "Nitro"),
        3: ("🚀", "Nitro Basic"),
    }

    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.username: str = data.get("username")
        self.avatar: Optional[str] = data.get("avatar")
        self.discriminator: str = data.get("discriminator")
        self.public_flags: int = data.get("public_flags", 0)
        self.flags: int = data.get("flags", 0)
        self.banner: Optional[str] = data.get("banner")
        self.accent_color: Optional[int] = data.get("accent_color")
        self.global_name: str = data.get("global_name")
        self.avatar_decoration_data: Optional[str] = data.get("avatar_decoration_data")
        self.banner_color: Optional[str] = data.get("banner_color")
        self.clan: Optional[str] = data.get("clan")
        self.mfa_enabled: bool = data.get("mfa_enabled", False)
        self.locale: str = data.get("locale")
        self.premium_type: int = data.get("premium_type", 0)
        self.email: Optional[str] = data.get("email")
        self.verified: bool = data.get("verified", False)
        self.phone: Optional[str] = data.get("phone")
        self.nsfw_allowed: bool = data.get("nsfw_allowed", False)
        self.premium_usage_flags: int = data.get("premium_usage_flags", 0)
        self.linked_users: List[str] = data.get("linked_users", [])
        self.purchased_flags: int = data.get("purchased_flags", 0)
        self.bio: Optional[str] = data.get("bio")
        self.authenticator_types: List[int] = data.get("authenticator_types", [])

        self.premium_emoji_type = self.premium_types.get(self.premium_type, "")

    def __str__(self):
        return f"{self.global_name} ({self.username}) {self.premium_emoji_type[0]}"

    def extended_str(self) -> str:
        mfa_emoji = "🔒" if self.mfa_enabled else "🔓"
        verified_emoji = "✅" if self.verified else "❌"

        return (
            f"{self.global_name} ({self.username})\n"
            f"{self.premium_emoji_type[0]} Premium: {self.premium_emoji_type[1]}\n"
            f"🔑 MFA: {mfa_emoji}\n"
            f"✅ Verified: {verified_emoji}"
        )

    def full_str(self):
        result = ""
        for key, value in self.__dict__.items():
            result += f"{key}: {value}\n"
        return result


if __name__ == "__main__":
    friend = Friend({
        "id": 1,
        "nickname": "nickname",
        "since": "2024-05-14T07:35:43.175000+00:00",
        "type": 1,
        "user": {
            "avatar": "avatar",
            "clan": "clan",
            "global_name": "global_name",
            "public_flags": 1,
            "username": "username",
        }
    })
    print(friend, end="\n\n")
    print(friend.extended_str(), end="\n\n")
    print(friend.full_str())

    user = MyUser({
        "id": "678186189538451111",
        "username": "usrn",
        "avatar": "f6de16f258638fb0d242b52c6e911111",
        "discriminator": "0",
        "public_flags": 128,
        "flags": 128,
        "banner": "a_e6722b00420c232eba70f9290e00bfd5",
        "accent_color": 3830189,
        "global_name": "MyName",
        "avatar_decoration_data": None,
        "banner_color": "#3a71ad",
        "clan": None,
        "mfa_enabled": True,
        "locale": "ru",
        "premium_type": 2,
        "email": "email@gmail.com",
        "verified": True,
        "phone": "+3806621323111",
        "nsfw_allowed": True,
        "premium_usage_flags": 4,
        "linked_users": [],
        "purchased_flags": 2,
        "bio": "<:chad:1013533191098867815> - this is literally me",
        "authenticator_types": [
            2
        ]
    })
    print(user.extended_str(), end="\n\n")
    print(user.full_str())
