import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from export_teams_ccl_summary import collect_store_stats


class _Undefined:
    pass


class FakeRecord:
    def __init__(self, value):
        self.value = value


class FakeStore:
    def __init__(self, values):
        self._values = values

    def iterate_records(self, errors_to_stdout=True):
        del errors_to_stdout
        for value in self._values:
            yield FakeRecord(value)


class ExportSummaryTests(unittest.TestCase):
    def test_collect_store_stats_counts_replychain_messages_without_materializing_store(self) -> None:
        store = FakeStore(
            [
                {"conversationId": "t1", "replyChainId": "r1", "messageMap": {"m1": {"id": "m1"}, "m2": {"id": "m2"}}},
                {"conversationId": "t2", "replyChainId": "r2", "messageMap": {}},
                {"conversationId": "t3", "replyChainId": "r3", "messageMap": {"m3": {"id": "m3"}}},
            ]
        )

        summary, sample = collect_store_stats(store, "replychains", show_decode_errors=False)

        self.assertEqual(summary["record_count"], 3)
        self.assertEqual(summary["messages_total"], 3)
        self.assertEqual(summary["threads_with_messages"], 2)
        self.assertEqual(sample["conversationId"], "t1")
        self.assertEqual(sample["messageMap_count"], 2)

    def test_collect_store_stats_treats_undefined_sample_shapes_as_empty(self) -> None:
        undefined = _Undefined()
        conversations = FakeStore(
            [
                {"id": "t1", "type": "chat", "title": "Example", "members": undefined},
            ]
        )
        replychains = FakeStore(
            [
                {"conversationId": "t1", "replyChainId": "r1", "messageMap": undefined},
            ]
        )

        conversation_summary, conversation_sample = collect_store_stats(conversations, "conversations", show_decode_errors=False)
        replychain_summary, replychain_sample = collect_store_stats(replychains, "replychains", show_decode_errors=False)

        self.assertEqual(conversation_summary["record_count"], 1)
        self.assertEqual(conversation_sample["member_count"], 0)
        self.assertEqual(replychain_summary["record_count"], 1)
        self.assertNotIn("messages_total", replychain_summary)
        self.assertEqual(replychain_sample["messageMap_count"], 0)


if __name__ == "__main__":
    unittest.main()
