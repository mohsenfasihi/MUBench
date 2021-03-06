from copy import deepcopy
from typing import List

from data.detector_run import DetectorRun
from data.finding import Finding
from data.misuse import Misuse
from data.version_compile import VersionCompile


class PotentialHits:
    def __init__(self, findings: List[Finding]):
        self.findings = findings


def _to_potential_hit(misuse_id, finding: Finding):
    potential_hit = deepcopy(finding)
    potential_hit["misuse"] = misuse_id
    return potential_hit


class PotentialHitsFilterTask:
    def run(self, misuse: Misuse, detector_run: DetectorRun, version_compile: VersionCompile) -> PotentialHits:
        findings = detector_run.findings
        misuse_potential_hits = self._get_potential_hits(misuse, findings, version_compile.original_sources_paths, False)
        if not misuse_potential_hits:
            misuse_potential_hits = self._get_potential_hits(misuse, findings, version_compile.original_sources_paths, True)
        return PotentialHits(misuse_potential_hits)

    @staticmethod
    def _get_potential_hits(misuse: Misuse, findings: List[Finding], source_base_paths: List[str], method_name_only: bool):
        potential_hits = []
        for finding in findings:
            if finding.is_potential_hit(misuse, source_base_paths, method_name_only):
                potential_hits.append(_to_potential_hit(misuse.misuse_id, finding))
        return potential_hits


class AllFindingsFilterTask:
    def __init__(self, limit: int):
        self.limit = limit

    def run(self, detector_run: DetectorRun) -> PotentialHits:
        findings = detector_run.findings
        top_findings = self.__get_top_findings(findings)
        potential_hits = []
        for rank, top_finding in enumerate(top_findings):
            potential_hits.append(_to_potential_hit("finding-{}".format(rank), top_finding))
        return PotentialHits(potential_hits)

    def __get_top_findings(self, findings):
        return findings[0:self.limit]
