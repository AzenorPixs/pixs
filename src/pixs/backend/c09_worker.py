"""Worker C09 borné : aucun handler ni état de travail dans le payload."""
from __future__ import annotations

import threading

from pixs.backend.c09_contracts import validate_c09_policy
from pixs.backend.c09_job_repository import C09JobRepository, C09Refused

__all__ = ["C09Worker"]


class C09Worker:
    """Le signal local ferme les nouvelles admissions de ce processus.

    Les états de travail, baux, autorisations, résultats et checkpoints restent
    dans leurs propriétaires persistants. Le signal ne clôture pas un effet en
    cours et ne remplace pas la réadmission courante exigée par le repository.
    """

    def __init__(self, *, repository):
        if type(repository) is not C09JobRepository:
            raise C09Refused()
        self.repository = repository
        self._stop = threading.Event()

    def request_stop(self):
        self._stop.set()

    @property
    def admission_closed(self):
        return self._stop.is_set()

    def run_once(self, *, owner, policy):
        if validate_c09_policy(policy):
            raise C09Refused()
        if self._stop.is_set():
            return None
        lease = self.repository.acquire_next(owner=owner, policy=policy)
        if lease is None:
            return None
        if self._stop.is_set():
            return self.repository.restitute(handle=lease, policy=policy)
        return self.repository.run_unit(handle=lease, policy=policy)

    def run_batch(self, *, owner, policy):
        if validate_c09_policy(policy):
            raise C09Refused()
        results = []
        for _ in range(policy.max_units_per_poll):
            if self._stop.is_set():
                break
            result = self.run_once(owner=owner, policy=policy)
            if result is None:
                break
            results.append(result)
        return tuple(results)
