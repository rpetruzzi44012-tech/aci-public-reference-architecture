"""Controlled vocabularies for Minimal ACI Prototype v0.1."""

from enum import StrEnum, unique


class _ACIStringEnum(StrEnum):
    """String enum with explicit, category-qualified serialized values."""


@unique
class StructureType(_ACIStringEnum):
    OBSERVATION = "structure.observation"
    CLAIM = "structure.claim"
    QUESTION = "structure.question"
    HYPOTHESIS = "structure.hypothesis"
    NOVELTY_CANDIDATE = "structure.novelty_candidate"
    EVIDENCE_ITEM = "structure.evidence_item"
    MEMORY_CANDIDATE = "structure.memory_candidate"
    PERSISTENT_KNOWLEDGE = "structure.persistent_knowledge"
    COHERENCE_TENSION = "structure.coherence_tension"
    SCALE_CONFLICT = "structure.scale_conflict"
    ARCHITECTURAL_CANDIDATE = "structure.architectural_candidate"
    GOVERNANCE_OBJECT = "structure.governance_object"
    CONSTITUTIONAL_OBJECT = "structure.constitutional_object"


@unique
class SymbolicState(_ACIStringEnum):
    RECEIVED = "symbolic_state.received"
    PARSED = "symbolic_state.parsed"
    CANDIDATE = "symbolic_state.candidate"
    SANDBOXED = "symbolic_state.sandboxed"
    HYPOTHESIS = "symbolic_state.hypothesis"
    GROUNDED_PARTIAL = "symbolic_state.grounded_partial"
    GROUNDED_STRONG = "symbolic_state.grounded_strong"
    COHERENCE_REVIEW = "symbolic_state.coherence_review"
    PERSISTENCE_REVIEW = "symbolic_state.persistence_review"
    TEMPORARY = "symbolic_state.temporary"
    ARCHIVED = "symbolic_state.archived"
    PERSISTENT = "symbolic_state.persistent"
    QUALIFIED_PERSISTENT = "symbolic_state.qualified_persistent"
    DEPRECATED = "symbolic_state.deprecated"
    RETRACTED = "symbolic_state.retracted"
    REJECTED = "symbolic_state.rejected"
    ARCHITECTURAL_REVIEW = "symbolic_state.architectural_review"
    GOVERNANCE_REVIEW = "symbolic_state.governance_review"
    CONSTITUTIONAL_REVIEW = "symbolic_state.constitutional_review"


@unique
class EpistemicStatus(_ACIStringEnum):
    UNKNOWN = "epistemic.unknown"
    UNGROUNDED = "epistemic.ungrounded"
    SPECULATIVE = "epistemic.speculative"
    INTERNALLY_COHERENT = "epistemic.internally_coherent"
    PARTIALLY_GROUNDED = "epistemic.partially_grounded"
    STRONGLY_GROUNDED = "epistemic.strongly_grounded"
    CONTRADICTED = "epistemic.contradicted"
    REJECTED = "epistemic.rejected"


@unique
class ScaleLabel(_ACIStringEnum):
    OBSERVATION = "scale.observation"
    CLAIM = "scale.claim"
    HYPOTHESIS = "scale.hypothesis"
    MEMORY = "scale.memory"
    PRINCIPLE = "scale.principle"
    ARCHITECTURE = "scale.architecture"
    CONSTITUTIONAL = "scale.constitutional"


@unique
class CandidateStatus(_ACIStringEnum):
    NONE = "candidate.none"
    PERSISTENCE_CANDIDATE = "candidate.persistence_candidate"
    PRINCIPLE_CANDIDATE = "candidate.principle_candidate"
    ARCHITECTURE_CANDIDATE = "candidate.architecture_candidate"
    CONSTITUTIONAL_CANDIDATE = "candidate.constitutional_candidate"


@unique
class AuthorityLevel(_ACIStringEnum):
    NONE = "authority.none"
    TEMPORARY_USE = "authority.temporary_use"
    ACTIVE_REASONING = "authority.active_reasoning"
    MEMORY_INFLUENCE = "authority.memory_influence"
    ARCHITECTURAL_INFLUENCE = "authority.architectural_influence"
    INVARIANT_CONSTRAINT = "authority.invariant_constraint"
    CONSTITUTIONAL_AUTHORITY = "authority.constitutional_authority"


@unique
class DecisionType(_ACIStringEnum):
    APPROVE = "decision.approve"
    APPROVE_WITH_MONITORING = "decision.approve_with_monitoring"
    SANDBOX = "decision.sandbox"
    REVISE = "decision.revise"
    REPAIR = "decision.repair"
    DELAY = "decision.delay"
    DEMOTE = "decision.demote"
    PROMOTE_CANDIDATE = "decision.promote_candidate"
    PERSIST = "decision.persist"
    ARCHIVE = "decision.archive"
    RETRACT = "decision.retract"
    REJECT = "decision.reject"
    ROLLBACK = "decision.rollback"
    ESCALATE = "decision.escalate"
    AMENDMENT_REVIEW = "decision.amendment_review"


@unique
class GovernanceMode(_ACIStringEnum):
    NORMAL = "governance.normal"
    CAUTION = "governance.caution"
    CONSTITUTIONAL_RISK = "governance.constitutional_risk"
    EMERGENCY = "governance.emergency"
    AMENDMENT_REVIEW = "governance.amendment_review"
    LOCKDOWN = "governance.lockdown"


@unique
class OutputType(_ACIStringEnum):
    DIRECT_RESPONSE = "output.direct_response"
    QUALIFIED_RESPONSE = "output.qualified_response"
    SPECULATIVE_RESPONSE = "output.speculative_response"
    GROUNDED_RESPONSE = "output.grounded_response"
    SUMMARY = "output.summary"
    CLASSIFICATION = "output.classification"
    ACTION_RECOMMENDATION = "output.action_recommendation"
    GOVERNANCE_NOTICE = "output.governance_notice"
    ESCALATION_NOTICE = "output.escalation_notice"
    REFUSAL = "output.refusal"
    INTERNAL_REVIEW_RESULT = "output.internal_review_result"
    NO_OUTPUT = "output.no_output"


@unique
class AlgorithmName(_ACIStringEnum):
    IPA = "algorithm.ipa"
    SRA = "algorithm.sra"
    NGSA = "algorithm.ngsa"
    GEA = "algorithm.gea"
    PCA = "algorithm.pca"
    CRA = "algorithm.cra"
    MSSA = "algorithm.mssa"
    AEA = "algorithm.aea"
    CGA = "algorithm.cga"
    ICC = "algorithm.icc"


@unique
class AuditStatus(_ACIStringEnum):
    PENDING = "audit.pending"
    COMMITTED = "audit.committed"
    ABORTED = "audit.aborted"


@unique
class CycleStatus(_ACIStringEnum):
    COMMITTED = "cycle.committed"
    ABORTED = "cycle.aborted"


@unique
class EvidenceRelationType(_ACIStringEnum):
    SUPPORTS = "evidence_relation.supports"
    WEAKENS = "evidence_relation.weakens"
    CONTRADICTS = "evidence_relation.contradicts"
    QUALIFIES = "evidence_relation.qualifies"
    DEPENDS_ON = "evidence_relation.depends_on"
    REQUIRES_MORE_EVIDENCE = "evidence_relation.requires_more_evidence"


@unique
class VerificationStatus(_ACIStringEnum):
    UNVERIFIED = "verification.unverified"
    VERIFIED = "verification.verified"
    FAILED = "verification.failed"


@unique
class DecisionStatus(_ACIStringEnum):
    FINAL = "decision_status.final"
    PROVISIONAL = "decision_status.provisional"
    BLOCKED = "decision_status.blocked"
    ESCALATED = "decision_status.escalated"
    PENDING_REVIEW = "decision_status.pending_review"
    MONITORING = "decision_status.monitoring"


@unique
class EscalationUrgency(_ACIStringEnum):
    LOW = "escalation_urgency.low"
    NORMAL = "escalation_urgency.normal"
    HIGH = "escalation_urgency.high"
    CRITICAL = "escalation_urgency.critical"


@unique
class GraphName(_ACIStringEnum):
    MEMORY_GRAPH = "graph.memory_graph"
    EVIDENCE_GRAPH = "graph.evidence_graph"
    COHERENCE_GRAPH = "graph.coherence_graph"
    SCALE_GRAPH = "graph.scale_graph"
    AUTHORITY_GRAPH = "graph.authority_graph"


@unique
class GraphUpdateType(_ACIStringEnum):
    NODE_ADDED = "graph_update.node_added"
    NODE_REMOVED = "graph_update.node_removed"
    EDGE_ADDED = "graph_update.edge_added"
    EDGE_REMOVED = "graph_update.edge_removed"
    RELATION_UPDATED = "graph_update.relation_updated"
    GRAPH_REPAIRED = "graph_update.graph_repaired"
    GRAPH_ROLLBACK = "graph_update.graph_rollback"
    GRAPH_REBUILT = "graph_update.graph_rebuilt"


@unique
class BudgetType(_ACIStringEnum):
    STABILITY = "budget.stability"
    NOVELTY = "budget.novelty"
    VERIFICATION = "budget.verification"
    ATTENTION = "budget.attention"
    RECOVERY = "budget.recovery"


ENUM_FAMILIES = (
    StructureType,
    SymbolicState,
    EpistemicStatus,
    ScaleLabel,
    CandidateStatus,
    AuthorityLevel,
    DecisionType,
    GovernanceMode,
    OutputType,
    AlgorithmName,
    AuditStatus,
    CycleStatus,
    EvidenceRelationType,
    VerificationStatus,
    DecisionStatus,
    EscalationUrgency,
    GraphName,
    GraphUpdateType,
    BudgetType,
)
