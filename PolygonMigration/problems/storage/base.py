from abc import ABC, abstractmethod


class StorageBackend(ABC):
    """Provider-independent interface for storing problem files.

    A provider only implements two primitives: upload_bytes and delete_prefix.
    The folder layout is defined once here, so it is identical for every provider:

        test_cases/{problem_id}/{test_number}      input file
        test_cases/{problem_id}/{test_number}.a    output file
    """

    ROOT = "test_cases"

    @abstractmethod
    def upload_bytes(self, key: str, data: bytes) -> None:
        """Store `data` under `key`. Must raise on failure."""

    @abstractmethod
    def delete_prefix(self, prefix: str) -> int:
        """Delete every object whose key starts with `prefix`. Returns the count."""

    def _prefix(self, problem_id) -> str:
        return f"{self.ROOT}/{problem_id}/"

    def upload_test_case(self, problem_id, test_number, input_data, output_data):
        base = f"{self._prefix(problem_id)}{test_number}"
        self.upload_bytes(base, input_data.encode("utf-8"))
        self.upload_bytes(f"{base}.a", output_data.encode("utf-8"))

    def upload_problem_file(self, problem_id, filename, data: bytes):
        self.upload_bytes(f"{self._prefix(problem_id)}{filename}", data)

    def delete_problem_files(self, problem_id) -> int:
        return self.delete_prefix(self._prefix(problem_id))