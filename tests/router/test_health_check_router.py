import asyncio
from asyncio import AbstractEventLoop
from unittest import TestCase

from app.router import health_check_router


class Test(TestCase):
    __loop: AbstractEventLoop

    @classmethod
    def setUpClass(cls):
        cls.__loop = asyncio.new_event_loop()

    @classmethod
    def tearDownClass(cls):
        cls.__loop.close()

    def test_health_check(self):
        response = self.__loop.run_until_complete(health_check_router.health_check())
        assert response["text"] == "server is up!"
