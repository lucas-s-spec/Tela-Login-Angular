import reflex as rx
import asyncio


class AuthState(rx.State):
    email: str = ""
    password: str = ""
    remember_me: bool = False
    is_loading: bool = False
    error: str = ""

    @rx.event
    def set_email(self, value: str):
        self.email = value
        if self.error:
            self.error = ""

    @rx.event
    def set_password(self, value: str):
        self.password = value
        if self.error:
            self.error = ""

    @rx.event
    def toggle_remember_me(self):
        self.remember_me = not self.remember_me

    @rx.event(background=True)
    async def login(self):
        async with self:
            self.is_loading = True
            self.error = ""
        await asyncio.sleep(1.5)
        async with self:
            if not self.email or not self.password:
                self.error = "Please enter both email and password."
                self.is_loading = False
            elif "@" not in self.email:
                self.error = "Please enter a valid email address."
                self.is_loading = False
            else:
                self.is_loading = False
                yield rx.toast(
                    "Successfully logged in!",
                    description="Welcome back to the platform.",
                    position="top-center",
                    duration=3000,
                )