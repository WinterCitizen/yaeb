"""Module testing the functionality of executor event handler."""
from concurrent.futures import ThreadPoolExecutor

from tests.factories.bus import EventBusFactory
from yaeb.base.bus import BaseEventBus
from yaeb.base.events import BaseEvent
from yaeb.base.handlers import BaseExecutorEventHandler


class ExecutorEventHandler(BaseExecutorEventHandler[BaseEvent]):
    """Test executor handler."""

    is_called: bool

    def handle_event(self, event: BaseEvent, bus: BaseEventBus) -> None:
        """Record call to this method ignoring event."""
        self.is_called = True


def test_executor_event_handler() -> None:
    """Test that executor event handler properly works with executors."""
    with ThreadPoolExecutor(max_workers=1) as executor:
        # Given: executor event handler with given thread pool executor
        executor_handler = ExecutorEventHandler(executor=executor)

        # When: execute method is called
        executor_handler.execute(
            event=BaseEvent(parent_event=None),
            bus=EventBusFactory.create(),
        )
        executor.shutdown()

        # Then: handle event is called via the executor
        assert executor_handler.is_called
