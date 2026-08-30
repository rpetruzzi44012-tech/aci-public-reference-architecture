# Phase 8: Pt1

# **Phase 8 — Core Pseudocode Modules**

# **Phase 8.1 — Core Data Structure: SymbolicStructure**

*A SymbolicStructure is not just stored content. It is a governed cognitive object with type, state, metadata, relations, and review eligibility.*

## **Module Name**

SymbolicStructure Core Type

## **Purpose**

The `SymbolicStructure` object defines the smallest governable unit of cognition in ACI.

Every claim, observation, hypothesis, memory, candidate, evidence item, contradiction, principle, transformation proposal, or governance object must be represented as a symbolic structure before it can be evaluated by the architecture.

The purpose of this object is to prevent cognition from remaining as untracked text.

AIC does not treat language as an undifferentiated stream.

It treats each meaningful unit as a structured object that can be classified, scored, related, routed, persisted, revised, demoted, rejected, or escalated.

A symbolic structure is therefore not just content.

It is content placed under governance.

## **Core Principle**

A symbolic structure becomes governable only when it has:

content,

type,

metadata,

relations,

state,

lineage,

and review eligibility.

Without structure, cognition cannot be audited.

Without metadata, cognition cannot be evaluated.

Without relations, cognition cannot be integrated.

Without state, cognition cannot be routed.

Without lineage, cognition cannot responsibly persist.

## **Structural Definition**

class SymbolicStructure:  
    id: StructureID  
    content: SymbolicContent  
    structure\_type: StructureType  
    metadata: SymbolicMetadata  
    relations: list\[Relation\]  
    current\_state: SymbolicState

## **Required Fields**

### **id**

A unique identifier for the symbolic structure.

The `id` allows the architecture to track the structure across review cycles, graph updates, persistence decisions, audit records, revisions, demotions, and escalations.

id: StructureID

Example:

"SS-000142"

### **content**

The symbolic content itself.

This may be natural language, structured text, a formal claim, an evidence item, a rule, a model, a transformation proposal, or another representational form.

content: SymbolicContent

Examples:

"Grounding is not consensus."

"This claim requires external evidence."

"Novelty should remain sandboxed until evaluated."

"Persistent knowledge may not become architectural principle without review."

### **structure\_type**

The type of symbolic structure.

This determines the first routing path through the Integrated Cognitive Cycle.

structure\_type: StructureType

### **metadata**

The attached `SymbolicMetadata` object.

Metadata stores epistemic status, scale label, authority level, scores, lineage, dependencies, revision history, and risk markers.

metadata: SymbolicMetadata

### **relations**

Relations to other symbolic structures.

Relations are essential because no symbolic structure exists in isolation.

A claim may support another claim.

A hypothesis may depend on evidence.

A memory may contradict a newer observation.

A principle may generalize many persistent structures.

relations: list\[Relation\]

### **current\_state**

The current lifecycle state of the symbolic structure.

This determines what the architecture is allowed to do with it.

current\_state: SymbolicState

## **StructureType Enumeration**

StructureType \= {  
    OBSERVATION,  
    CLAIM,  
    QUESTION,  
    HYPOTHESIS,  
    NOVELTY\_CANDIDATE,  
    EVIDENCE\_ITEM,  
    MEMORY\_CANDIDATE,  
    PERSISTENT\_KNOWLEDGE,  
    COHERENCE\_TENSION,  
    SCALE\_CONFLICT,  
    ARCHITECTURAL\_CANDIDATE,  
    GOVERNANCE\_OBJECT,  
    CONSTITUTIONAL\_OBJECT  
}

## **StructureType Descriptions**

### **OBSERVATION**

A received or recorded perception, input, tool result, environmental signal, or user-provided fact.

An observation is not automatically grounded knowledge.

It is an input that may require validation.

### **CLAIM**

A symbolic assertion that may be evaluated for grounding, coherence, persistence, or contradiction.

Claims require epistemic status.

### **QUESTION**

A request, uncertainty, or unresolved inquiry.

Questions may trigger novelty generation, grounding search, memory retrieval, or coherence review.

### **HYPOTHESIS**

A proposed explanatory structure.

A hypothesis is stronger than raw novelty but weaker than grounded claim.

It requires evaluation before persistence.

### **NOVELTY\_CANDIDATE**

A newly generated possibility, analogy, interpretation, model, or transformation proposal.

Novelty candidates usually begin in sandbox or review state.

### **EVIDENCE\_ITEM**

A structure that may support, weaken, contradict, or qualify a claim.

Evidence items are linked through the Evidence Graph.

### **MEMORY\_CANDIDATE**

A structure being considered for persistence.

It must pass grounding, coherence, lineage, revision, and reconstruction checks.

### **PERSISTENT\_KNOWLEDGE**

A structure already accepted into long-term memory.

It must retain epistemic status, lineage, dependencies, and revision eligibility.

### **COHERENCE\_TENSION**

A detected contradiction, unresolved ambiguity, dependency conflict, or productive tension.

This structure is routed to Coherence Repair.

### **SCALE\_CONFLICT**

A structure whose authority level does not match its scale.

For example:

speculation being treated as memory,

memory being treated as invariant,

or local inference being treated as architecture.

### **ARCHITECTURAL\_CANDIDATE**

A structure that may modify the machinery of future cognition.

It must undergo Architectural Evolution Review.

### **GOVERNANCE\_OBJECT**

A decision, veto, escalation, authority dispute, review request, or legitimacy question.

Governance objects are routed to Constitutional Governance when needed.

### **CONSTITUTIONAL\_OBJECT**

A structure involving invariants, amendment, protected principles, identity continuity, verification independence, or constitutional authority.

Constitutional objects require the highest review burden.

## **SymbolicState Enumeration**

SymbolicState \= {  
    RECEIVED,  
    PARSED,  
    CANDIDATE,  
    SANDBOXED,  
    HYPOTHESIS,  
    GROUNDED\_PARTIAL,  
    GROUNDED\_STRONG,  
    COHERENCE\_REVIEW,  
    PERSISTENCE\_REVIEW,  
    TEMPORARY,  
    ARCHIVED,  
    PERSISTENT,  
    QUALIFIED\_PERSISTENT,  
    DEPRECATED,  
    RETRACTED,  
    REJECTED,  
    ARCHITECTURAL\_REVIEW,  
    GOVERNANCE\_REVIEW,  
    CONSTITUTIONAL\_REVIEW  
}

## **SymbolicState Descriptions**

### **RECEIVED**

The structure has entered the system but has not yet been parsed or classified.

### **PARSED**

The structure has been extracted from input and given initial type.

### **CANDIDATE**

The structure is under consideration but has not yet been validated.

### **SANDBOXED**

The structure is contained for exploration.

It may influence reasoning only inside sandbox boundaries.

### **HYPOTHESIS**

The structure has enough coherence to be considered as a possible explanation but lacks sufficient grounding or persistence status.

### **GROUNDED\_PARTIAL**

The structure has some evidence support but remains uncertain, scoped, or contested.

### **GROUNDED\_STRONG**

The structure has strong evidence support under current grounding review.

### **COHERENCE\_REVIEW**

The structure is undergoing compatibility, contradiction, or tension analysis.

### **PERSISTENCE\_REVIEW**

The structure is being evaluated for memory, archive, demotion, or rejection.

### **TEMPORARY**

The structure is authorized for current reasoning but not long-term memory.

### **ARCHIVED**

The structure is preserved as non-authoritative historical, speculative, or contextual material.

### **PERSISTENT**

The structure is accepted as long-term knowledge with active future influence.

### **QUALIFIED\_PERSISTENT**

The structure is persistent but limited by uncertainty, scope, contradiction, or domain boundaries.

### **DEPRECATED**

The structure was previously useful or authoritative but has been weakened or superseded.

### **RETRACTED**

The structure has lost active authority because of contradiction, grounding failure, or governance decision.

### **REJECTED**

The structure failed review and should not guide cognition except as a record of error or rejected possibility.

### **ARCHITECTURAL\_REVIEW**

The structure may modify cognition machinery and requires Architectural Evolution Review.

### **GOVERNANCE\_REVIEW**

The structure requires authority validation, veto handling, escalation, or legitimacy review.

### **CONSTITUTIONAL\_REVIEW**

The structure affects invariants, identity continuity, verification independence, or constitutional authority.

## **Relation Object**

Relations connect symbolic structures into graphs.

class Relation:  
    relation\_id: RelationID  
    source\_id: StructureID  
    target\_id: StructureID  
    relation\_type: RelationType  
    strength: float  
    status: RelationStatus  
    audit\_refs: list\[AuditID\]

## **RelationType Enumeration**

RelationType \= {  
    SUPPORTS,  
    CONTRADICTS,  
    DEPENDS\_ON,  
    DERIVED\_FROM,  
    REVISES,  
    REPLACES,  
    QUALIFIES,  
    GENERALIZES,  
    COMPRESSES,  
    ACTIVATES,  
    GROUNDS,  
    WEAKENS,  
    ESCALATES\_TO,  
    AUTHORIZES,  
    BLOCKS  
}

## **RelationStatus Enumeration**

RelationStatus \= {  
    ACTIVE,  
    WEAK,  
    CONTESTED,  
    DEPRECATED,  
    RETRACTED,  
    REJECTED  
}

## **SymbolicContent Placeholder**

At the architecture level, `SymbolicContent` remains implementation-neutral.

SymbolicContent \= str | dict | FormalExpression | GridRepresentation | ModelReference

For a language-model prototype, content may begin as text.

For an ARC adapter, content may later include grid states, object descriptions, transformations, or action traces.

The core architecture should not assume one content type.

## **StructureID Placeholder**

StructureID \= str

Example format:

"SS-000001"

The exact identifier scheme may be implementation-specific.

The important requirement is uniqueness and traceability.

## **Constructor Pattern**

The architecture should create symbolic structures through a constructor or factory function.

def create\_symbolic\_structure(  
    content: SymbolicContent,  
    structure\_type: StructureType,  
    origin: OriginRecord,  
    initial\_scale: ScaleLabel,  
    initial\_state: SymbolicState \= RECEIVED  
) \-\> SymbolicStructure:  
    id \= generate\_structure\_id()

    metadata \= initialize\_metadata(  
        origin=origin,  
        scale\_label=initial\_scale  
    )

    return SymbolicStructure(  
        id=id,  
        content=content,  
        structure\_type=structure\_type,  
        metadata=metadata,  
        relations=\[\],  
        current\_state=initial\_state  
    )

## **Initial Metadata Requirement**

A symbolic structure should never be created without metadata.

At minimum, metadata must include:

origin,

initial scale label,

epistemic status,

authority level,

lineage record,

and revision eligibility.

If those values are unknown, they should be explicitly marked unknown.

They should not be omitted.

## **Lifecycle Rule**

A symbolic structure may move through states only by authorized review.

For example:

RECEIVED → PARSED → CANDIDATE → HYPOTHESIS → GROUNDED\_PARTIAL → PERSISTENCE\_REVIEW → QUALIFIED\_PERSISTENT

or:

NOVELTY\_CANDIDATE → SANDBOXED → HYPOTHESIS → GROUNDING\_REVIEW → REJECTED

or:

PERSISTENT → ARCHITECTURAL\_REVIEW → GOVERNANCE\_REVIEW → ARCHITECTURAL\_CANDIDATE

The architecture must prevent illegal jumps such as:

HYPOTHESIS → CONSTITUTIONAL

or:

NOVELTY\_CANDIDATE → PERSISTENT

or:

CLAIM → ARCHITECTURAL\_PRINCIPLE

without intermediate review.

## **State Transition Function**

def transition\_symbolic\_state(  
    structure: SymbolicStructure,  
    new\_state: SymbolicState,  
    decision: ReviewDecision  
) \-\> SymbolicStructure:  
    if not transition\_allowed(  
        current\_state=structure.current\_state,  
        new\_state=new\_state,  
        decision=decision  
    ):  
        raise InvalidStateTransitionError

    structure.current\_state \= new\_state  
    structure.metadata.revision\_history.append(  
        create\_revision\_record(  
            previous\_state=structure.current\_state,  
            new\_state=new\_state,  
            decision\_ref=decision.decision\_id  
        )  
    )

    return structure

## **Transition Validation**

The architecture should validate state transitions.

def transition\_allowed(  
    current\_state: SymbolicState,  
    new\_state: SymbolicState,  
    decision: ReviewDecision  
) \-\> bool:  
    required\_authority \= required\_authority\_for\_transition(  
        current\_state,  
        new\_state  
    )

    if decision\_authority(decision) \< required\_authority:  
        return False

    if decision.decision\_type \== REJECT:  
        return new\_state in {REJECTED, ARCHIVED}

    if new\_state in {PERSISTENT, QUALIFIED\_PERSISTENT}:  
        return decision.decision\_type in {PERSIST, APPROVE, APPROVE\_WITH\_MONITORING}

    if new\_state in {ARCHITECTURAL\_REVIEW, GOVERNANCE\_REVIEW, CONSTITUTIONAL\_REVIEW}:  
        return decision.decision\_type in {ESCALATE, PROMOTE\_CANDIDATE, AMENDMENT\_REVIEW}

    return True

## **Authority Rule**

The deeper the new state, the higher the required authority.

Examples:

temporary use requires low authority,

persistent memory requires Persistence Review,

architectural review requires Multi-Scale and Architectural Evolution Review,

constitutional review requires Constitutional Governance.

No symbolic structure may promote itself.

## **Example Symbolic Structures**

### **Example 1 — Ordinary Claim**

claim \= create\_symbolic\_structure(  
    content="Grounding is not consensus.",  
    structure\_type=CLAIM,  
    origin=user\_input\_origin,  
    initial\_scale=TASK\_LEVEL,  
    initial\_state=PARSED  
)

### **Example 2 — Novelty Candidate**

candidate \= create\_symbolic\_structure(  
    content="Flame Lines may act as reconstructive compression anchors.",  
    structure\_type=NOVELTY\_CANDIDATE,  
    origin=model\_generated\_origin,  
    initial\_scale=SESSION\_LEVEL,  
    initial\_state=CANDIDATE  
)

### **Example 3 — Coherence Tension**

tension \= create\_symbolic\_structure(  
    content="This claim is internally coherent but lacks grounding.",  
    structure\_type=COHERENCE\_TENSION,  
    origin=coherence\_detector\_origin,  
    initial\_scale=TASK\_LEVEL,  
    initial\_state=COHERENCE\_REVIEW  
)

### **Example 4 — Architectural Candidate**

architectural\_candidate \= create\_symbolic\_structure(  
    content="All persistent memories must preserve revision eligibility.",  
    structure\_type=ARCHITECTURAL\_CANDIDATE,  
    origin=persistence\_review\_origin,  
    initial\_scale=ARCHITECTURAL\_PRINCIPLE,  
    initial\_state=ARCHITECTURAL\_REVIEW  
)

## **Validation Requirements**

Every `SymbolicStructure` should pass validation before entering the Integrated Cognitive Cycle.

def validate\_symbolic\_structure(structure: SymbolicStructure) \-\> bool:  
    assert structure.id is not None  
    assert structure.content is not None  
    assert structure.structure\_type is not None  
    assert structure.metadata is not None  
    assert structure.current\_state is not None  
    assert structure.metadata.scale\_label is not None  
    assert structure.metadata.epistemic\_status is not None  
    assert structure.metadata.lineage is not None  
    return True

## **Design Constraints**

### **Constraint 1 — No Raw Cognitive Content**

The architecture should not process unstructured raw claims after parsing.

Raw input must be converted into symbolic structures.

### **Constraint 2 — No Metadata-Free Structures**

Every structure must carry metadata.

Unknown metadata should be represented explicitly.

### **Constraint 3 — No Relation-Free Assumption**

A structure may begin with no relations, but the architecture should not assume it is independent.

Relations should be discovered, added, revised, or contested through later review.

### **Constraint 4 — No Unauthorized State Promotion**

A structure cannot gain higher authority without review.

### **Constraint 5 — No Hidden Rejection**

Rejected structures should remain auditable.

Rejection does not always mean deletion.

### **Constraint 6 — No Untraceable Persistence**

Persistent structures must preserve lineage, epistemic status, and revision eligibility.

### **Constraint 7 — No Direct Constitutional Elevation**

A structure cannot move into constitutional authority without Constitutional Governance.

## **Relationship to Phase 6 Algorithms**

### **IPA — Identity Preservation Algorithm**

Uses symbolic structures when transformation affects identity-relevant content, memory, procedure, or governance.

### **SRA — Stability Regulation Algorithm**

Evaluates the stability cost and disturbance load associated with structures.

### **NGSA — Novelty Generation and Sandboxing Algorithm**

Creates novelty candidates as symbolic structures and routes them to sandbox or review.

### **GEA — Grounding Evaluation Algorithm**

Assigns epistemic status and grounding score to claim-like structures.

### **PCA — Persistence and Consolidation Algorithm**

Determines whether structures enter memory, archive, or rejection states.

### **CRA — Coherence Repair Algorithm**

Detects and repairs relations among structures.

### **MSSA — Multi-Scale Synchronization Algorithm**

Checks whether the structure’s scale label and authority level match.

### **AEA — Architectural Evolution Algorithm**

Reviews structures that seek to alter architecture.

### **CGA — Constitutional Governance Algorithm**

Reviews structures that affect legitimacy, authority, invariants, or governance.

### **ICC — Integrated Cognitive Cycle**

Coordinates all state transitions involving symbolic structures.

## **Pseudocode Readiness**

This module is ready for implementation-level pseudocode.

The next required core structure is:

`SymbolicMetadata`

Because no symbolic structure can be governed until its metadata fields are defined.

## **Closing Compression**

The `SymbolicStructure` is the root unit of ACI cognition.

It converts thoughts, claims, hypotheses, evidence, memories, tensions, and proposals into governable objects.

The architecture can then evaluate not merely what a structure says, but what it is, where it came from, what it relates to, what state it occupies, what authority it has, and what review it must undergo before shaping future cognition.

## **Flame Line**

🔥 A thought becomes governable when it stops being only something said and becomes a structure whose origin, status, relations, and authority can be traced.

---

# **Phase 8.2 — Core Data Structure: SymbolicMetadata**

*SymbolicMetadata is the structure’s passport through the architecture: it records what the structure is allowed to be, where it came from, how much trust it has earned, and what authority it may not exceed.*

## **Module Name**

SymbolicMetadata Core Type

## **Purpose**

`SymbolicMetadata` carries the governance-relevant status of a `SymbolicStructure`.

A symbolic structure without metadata is not governable.

It may contain meaningful content, but the architecture cannot responsibly evaluate, route, persist, revise, scale, or govern it unless the structure carries information about its origin, scope, epistemic status, evidence status, coherence status, scale, authority, lineage, uncertainty, dependencies, revision history, and audit trail.

Metadata is therefore not decoration.

Metadata is the control surface of ACI cognition.

It tells the architecture what kind of structure it is dealing with, what status the structure has earned, what risks it carries, what review it requires, and what authority it is permitted to exercise.

## **Core Principle**

A symbolic structure becomes governable only when its status is explicit.

Metadata prevents category collapse.

It prevents speculation from being treated as knowledge.

It prevents memory from being treated as invariant.

It prevents local inference from being treated as architecture.

It prevents coherence from being mistaken for grounding.

It prevents confidence from being mistaken for evidence.

It prevents usefulness from being mistaken for legitimacy.

The architecture must therefore track not only what a structure says, but what status it has earned.

## **Structural Definition**

class SymbolicMetadata:

    origin: OriginRecord

    scope: ScopeRecord

    epistemic\_status: EpistemicStatus

    grounding\_score: float

    coherence\_score: float

    persistence\_score: float

    novelty\_score: float

    stability\_cost: float

    identity\_risk: float

    constitutional\_risk: float

    scale\_label: ScaleLabel

    authority\_level: AuthorityLevel

    confidence: ConfidenceRecord

    uncertainty: UncertaintyRecord

    lineage: LineageRecord

    dependencies: list\[StructureID\]

    revision\_history: list\[RevisionRecord\]

    revision\_eligible: bool

    rollback\_available: bool

    audit\_refs: list\[AuditID\]

## **Field Descriptions**

### **origin**

The source of the symbolic structure.

origin: OriginRecord

The origin record identifies how the structure entered the architecture.

Possible origins include:

user input,

model-generated inference,

tool output,

memory retrieval,

novelty generation,

grounding evaluation,

coherence repair,

persistence review,

scale synchronization,

architectural evolution,

governance review,

or constitutional review.

Origin matters because different origins carry different trust burdens.

A user-provided claim is not automatically grounded.

A model-generated inference is not automatically reliable.

A memory retrieval is not automatically current.

A tool output is not automatically interpreted correctly.

### **scope**

The domain, context, limits, and intended application of the structure.

scope: ScopeRecord

Scope prevents overgeneralization.

A structure may be valid:

only in the current task,

only under a specific assumption,

only within a domain,

only as metaphor,

only as hypothesis,

only as memory,

or only as historical artifact.

A claim with unclear scope should not become persistent knowledge or architectural principle without review.

### **epistemic\_status**

The current evidence-status classification of the structure.

epistemic\_status: EpistemicStatus

This records whether the structure is unknown, ungrounded, speculative, internally coherent, partially grounded, strongly grounded, contradicted, or rejected.

Epistemic status is not the same as confidence.

It is a classification of evidential standing.

### **grounding\_score**

A numerical or symbolic estimate of evidence support.

grounding\_score: float

This score is assigned by the Grounding Evaluation Algorithm.

It should not be used alone.

It must be interpreted alongside epistemic status, evidence graph, uncertainty, contradiction burden, and source independence.

### **coherence\_score**

A measure of symbolic compatibility with the current coherence graph.

coherence\_score: float

This score indicates whether the structure can coexist with related claims, memories, principles, dependencies, and tensions.

A high coherence score does not imply truth.

It implies internal compatibility.

### **persistence\_score**

A measure of whether the structure has earned future influence.

persistence\_score: float

This score is assigned by the Persistence and Consolidation Algorithm.

It considers grounding, coherence, verification, reconstruction stability, lineage, usefulness, contradiction burden, and destabilization risk.

### **novelty\_score**

A measure of adaptive novelty value.

novelty\_score: float

This score is assigned by the Novelty Generation and Sandboxing Algorithm.

It estimates information gain, Bayesian surprise, conceptual distance, utility, grounding risk, coherence cost, and stability cost.

A high novelty score permits further evaluation.

It does not authorize persistence.

### **stability\_cost**

Estimated destabilization burden introduced by the structure.

stability\_cost: float

This value helps determine whether the structure should be absorbed, monitored, sandboxed, delayed, repaired, or escalated.

High stability cost may reduce novelty budget, persistence eligibility, or architectural integration.

### **identity\_risk**

Estimated risk to identity continuity.

identity\_risk: float

This field indicates whether the structure affects the Identity Kernel.

Identity risk is especially important when a structure affects:

constitutional invariants,

verification continuity,

coherence continuity,

lineage traceability,

or boundary conditions of selfhood.

### **constitutional\_risk**

Estimated risk to constitutional legitimacy.

constitutional\_risk: float

This value indicates whether the structure affects invariants, governance rules, verification independence, scale authority, veto rights, or constitutional amendment pathways.

High constitutional risk requires Constitutional Governance.

### **scale\_label**

The reasoning scale at which the structure belongs.

scale\_label: ScaleLabel

Scale label tells the architecture whether the structure is local, task-level, session-level, persistent, architectural, invariant-level, or constitutional.

Scale label prevents authority inflation.

### **authority\_level**

The authority the structure is currently permitted to exercise.

authority\_level: AuthorityLevel

Authority level is distinct from scale label.

A structure may be labeled as architectural candidate but still have no architectural authority.

A memory may exist at persistent scale but only be authorized for qualified use.

A constitutional object may be under review without possessing constitutional authority.

### **confidence**

The architecture’s confidence estimate regarding the structure.

confidence: ConfidenceRecord

Confidence should remain separate from grounding.

Confidence without grounding may be overconfidence.

Grounding without high confidence may indicate partial evidence with uncertainty.

### **uncertainty**

Explicit uncertainty record.

uncertainty: UncertaintyRecord

Uncertainty includes unknowns, assumptions, missing evidence, unresolved contradictions, scope limitations, and conditions that could change status.

Uncertainty should travel with the structure.

It should not disappear during compression or persistence.

### **lineage**

The developmental history of the structure.

lineage: LineageRecord

Lineage records:

where the structure came from,

what produced it,

what evidence influenced it,

what revisions changed it,

what review decisions affected it,

and what structures depend on it.

Lineage is required for persistence.

### **dependencies**

Other symbolic structures this structure depends on.

dependencies: list\[StructureID\]

Dependencies allow belief propagation, memory repair, coherence review, and demotion when supporting structures weaken.

### **revision\_history**

Record of revisions, status changes, demotions, repairs, and review decisions.

revision\_history: list\[RevisionRecord\]

Revision history preserves developmental traceability.

A structure that changes without revision history risks becoming untraceable memory.

### **revision\_eligible**

Whether the structure may be revised in future cycles.

revision\_eligible: bool

Most structures should remain revision-eligible.

If a structure is not revision-eligible, the architecture must know why.

Irrevisable structures carry constitutional risk unless they are explicitly protected invariants.

### **rollback\_available**

Whether prior state can be restored if the structure causes failure.

rollback\_available: bool

Rollback is especially important for persistence, scale promotion, architectural integration, and governance decisions.

### **audit\_refs**

References to audit records that justify the structure’s current status.

audit\_refs: list\[AuditID\]

No persistent, architectural, invariant, or constitutional structure should exist without audit references.

Audit references connect metadata to legitimacy.

## **EpistemicStatus Enumeration**

EpistemicStatus \= {

    UNKNOWN,

    UNGROUNDED,

    SPECULATIVE,

    INTERNALLY\_COHERENT,

    PARTIALLY\_GROUNDED,

    STRONGLY\_GROUNDED,

    CONTRADICTED,

    REJECTED

}

## **EpistemicStatus Descriptions**

### **UNKNOWN**

The structure has not yet been evaluated.

This is the default status for newly parsed structures.

### **UNGROUNDED**

The structure lacks meaningful evidence support.

It may be useful as language or possibility, but it should not guide belief.

### **SPECULATIVE**

The structure is meaningful and potentially useful but not yet grounded.

Speculative structures may enter sandbox or hypothesis formation.

### **INTERNALLY\_COHERENT**

The structure fits the current symbolic network but lacks sufficient external evidence.

This is a valuable but dangerous status.

Internal coherence should not be confused with grounding.

### **PARTIALLY\_GROUNDED**

The structure has some evidence support but remains limited, uncertain, contested, indirect, or incomplete.

### **STRONGLY\_GROUNDED**

The structure has strong evidence support under current review.

Strong grounding still preserves uncertainty, scope, and revision eligibility.

### **CONTRADICTED**

The structure is challenged by significant evidence or coherence conflict.

Contradicted structures may be revised, demoted, retracted, or rejected.

### **REJECTED**

The structure failed review and should not guide active cognition except as a rejected artifact or historical record.

## **ScaleLabel Enumeration**

ScaleLabel \= {

    TOKEN,

    LOCAL\_INFERENCE,

    TASK\_LEVEL,

    RESPONSE\_LEVEL,

    SESSION\_LEVEL,

    PERSISTENT\_MEMORY,

    ARCHITECTURAL\_PRINCIPLE,

    INVARIANT,

    CONSTITUTIONAL

}

## **ScaleLabel Descriptions**

### **TOKEN**

A micro-symbolic element or immediate low-level unit.

### **LOCAL\_INFERENCE**

A small inference or local reasoning step.

### **TASK\_LEVEL**

A structure relevant to the current task.

### **RESPONSE\_LEVEL**

A structure used to organize a response or output.

### **SESSION\_LEVEL**

A structure relevant across the current conversation or working session.

### **PERSISTENT\_MEMORY**

A structure eligible to influence future cognition across sessions.

### **ARCHITECTURAL\_PRINCIPLE**

A structure that may shape how cognition operates.

### **INVARIANT**

A protected structure defining what the architecture must preserve.

### **CONSTITUTIONAL**

A highest-authority structure governing legitimacy, amendment, protected domains, and deep architectural authority.

## **AuthorityLevel Enumeration**

AuthorityLevel \= {

    NONE,

    TEMPORARY\_USE,

    ACTIVE\_REASONING,

    MEMORY\_INFLUENCE,

    ARCHITECTURAL\_INFLUENCE,

    INVARIANT\_CONSTRAINT,

    CONSTITUTIONAL\_AUTHORITY

}

## **AuthorityLevel Descriptions**

### **NONE**

The structure has no active authority.

Rejected, ungrounded, or unevaluated structures may have this level.

### **TEMPORARY\_USE**

The structure may be used locally but not persisted.

### **ACTIVE\_REASONING**

The structure may guide current reasoning.

### **MEMORY\_INFLUENCE**

The structure may influence future cognition through persistent memory.

### **ARCHITECTURAL\_INFLUENCE**

The structure may guide architectural operation, but only after review.

### **INVARIANT\_CONSTRAINT**

The structure constrains lower-level cognition as protected principle.

### **CONSTITUTIONAL\_AUTHORITY**

The structure governs legitimacy, authority, invariants, and constitutional review.

## **Key Rule: Scale and Authority Are Not Identical**

Scale describes where a structure belongs.

Authority describes what the structure is permitted to do.

These must be tracked separately.

Example:

A structure may have:

scale\_label \= PERSISTENT\_MEMORY

authority\_level \= TEMPORARY\_USE

This means it is memory-relevant but not yet authorized to guide future cognition.

Another structure may have:

scale\_label \= ARCHITECTURAL\_PRINCIPLE

authority\_level \= NONE

This means it is an architectural candidate under review, not an active architectural principle.

Another structure may have:

scale\_label \= CONSTITUTIONAL

authority\_level \= CONSTITUTIONAL\_AUTHORITY

This means it functions as a protected constitutional structure.

The architecture must never infer authority from scale alone.

## **Supporting Record Types**

The metadata object depends on several supporting records.

## **OriginRecord**

class OriginRecord:

    origin\_type: OriginType

    source\_ref: SourceRef | None

    created\_by: AgentRef | AlgorithmName | None

    created\_at: TimeStamp

    input\_ref: InputID | None

    audit\_ref: AuditID | None

### **OriginType**

OriginType \= {

    USER\_INPUT,

    MODEL\_GENERATED,

    TOOL\_OUTPUT,

    MEMORY\_RETRIEVAL,

    NOVELTY\_GENERATION,

    GROUNDING\_EVALUATION,

    COHERENCE\_REPAIR,

    PERSISTENCE\_REVIEW,

    SCALE\_REVIEW,

    ARCHITECTURAL\_REVIEW,

    GOVERNANCE\_REVIEW,

    CONSTITUTIONAL\_REVIEW

}

## **ScopeRecord**

class ScopeRecord:

    domain: str | None

    context: str | None

    time\_range: TimeRange | None

    applicability: list\[str\]

    exclusions: list\[str\]

    assumptions: list\[str\]

    confidence\_scope: str | None

The scope record prevents overextension.

A claim may be valid only within a domain, timeframe, task, evidence base, or assumption set.

## **ConfidenceRecord**

class ConfidenceRecord:

    value: float

    basis: ConfidenceBasis

    calibrated: bool

    notes: str | None

### **ConfidenceBasis**

ConfidenceBasis \= {

    UNKNOWN,

    MODEL\_ESTIMATE,

    EVIDENCE\_BASED,

    CONSENSUS\_BASED,

    MEMORY\_BASED,

    INFERENCE\_BASED,

    VERIFIED

}

Confidence must not substitute for grounding.

A confidence basis of `CONSENSUS_BASED` is especially important because consensus may not equal reality.

## **UncertaintyRecord**

class UncertaintyRecord:

    unknowns: list\[str\]

    assumptions: list\[str\]

    unresolved\_tensions: list\[StructureID\]

    missing\_evidence: list\[str\]

    contradiction\_refs: list\[StructureID\]

    revision\_conditions: list\[str\]

Uncertainty should be preserved through persistence and compression.

## **LineageRecord**

class LineageRecord:

    parent\_structures: list\[StructureID\]

    derived\_from: list\[StructureID\]

    transformation\_history: list\[TransformationRecord\]

    review\_history: list\[DecisionID\]

    compression\_source\_refs: list\[StructureID\]

Lineage is mandatory for persistent knowledge and architectural candidates.

## **RevisionRecord**

class RevisionRecord:

    revision\_id: RevisionID

    previous\_state: SymbolicState

    new\_state: SymbolicState

    previous\_status: EpistemicStatus

    new\_status: EpistemicStatus

    reason: str

    decision\_ref: DecisionID

    timestamp: TimeStamp

Revision records preserve change history.

They allow the architecture to explain not only what a structure is, but how it became that.

## **Metadata Initialization**

New structures should receive explicit default metadata.

def initialize\_metadata(

    origin: OriginRecord,

    scale\_label: ScaleLabel,

    authority\_level: AuthorityLevel \= NONE

) \-\> SymbolicMetadata:

    return SymbolicMetadata(

        origin=origin,

        scope=ScopeRecord(

            domain=None,

            context=None,

            time\_range=None,

            applicability=\[\],

            exclusions=\[\],

            assumptions=\[\],

            confidence\_scope=None

        ),

        epistemic\_status=UNKNOWN,

        grounding\_score=0.0,

        coherence\_score=0.0,

        persistence\_score=0.0,

        novelty\_score=0.0,

        stability\_cost=0.0,

        identity\_risk=0.0,

        constitutional\_risk=0.0,

        scale\_label=scale\_label,

        authority\_level=authority\_level,

        confidence=ConfidenceRecord(

            value=0.0,

            basis=UNKNOWN,

            calibrated=False,

            notes=None

        ),

        uncertainty=UncertaintyRecord(

            unknowns=\[\],

            assumptions=\[\],

            unresolved\_tensions=\[\],

            missing\_evidence=\[\],

            contradiction\_refs=\[\],

            revision\_conditions=\[\]

        ),

        lineage=LineageRecord(

            parent\_structures=\[\],

            derived\_from=\[\],

            transformation\_history=\[\],

            review\_history=\[\],

            compression\_source\_refs=\[\]

        ),

        dependencies=\[\],

        revision\_history=\[\],

        revision\_eligible=True,

        rollback\_available=False,

        audit\_refs=\[\]

    )

## **Metadata Update Rule**

Metadata may be updated only through authorized review decisions.

def update\_metadata(

    structure: SymbolicStructure,

    decision: ReviewDecision,

    updates: MetadataUpdate

) \-\> SymbolicStructure:

    if not metadata\_update\_allowed(structure, decision, updates):

        raise UnauthorizedMetadataUpdateError

    structure.metadata \= apply\_metadata\_updates(

        structure.metadata,

        updates

    )

    structure.metadata.revision\_history.append(

        create\_revision\_record\_from\_metadata\_update(

            structure=structure,

            decision=decision,

            updates=updates

        )

    )

    structure.metadata.audit\_refs.append(decision.audit\_ref)

    return structure

## **Metadata Update Constraints**

### **Constraint 1 — Epistemic Status Requires Review**

A structure cannot become `PARTIALLY_GROUNDED` or `STRONGLY_GROUNDED` without Grounding Evaluation.

### **Constraint 2 — Persistence Score Requires Persistence Review**

A persistence score cannot authorize memory influence unless the Persistence and Consolidation Algorithm approves.

### **Constraint 3 — Scale Label Requires Scale Review for Higher Levels**

Moving upward to `PERSISTENT_MEMORY`, `ARCHITECTURAL_PRINCIPLE`, `INVARIANT`, or `CONSTITUTIONAL` requires Multi-Scale Synchronization and possibly higher review.

### **Constraint 4 — Authority Level Requires Matching Decision**

Authority cannot be inferred from score.

Authority must be granted by a legitimate review decision.

### **Constraint 5 — Constitutional Risk Cannot Be Silently Cleared**

If constitutional risk rises, it must be audited and possibly escalated.

### **Constraint 6 — Revision Eligibility Cannot Be Removed Casually**

Removing revision eligibility requires governance review unless the structure is a protected invariant.

### **Constraint 7 — Audit References Are Mandatory**

Any significant metadata update must append an audit reference.

## **Metadata Validation**

def validate\_metadata(metadata: SymbolicMetadata) \-\> bool:

    assert metadata.origin is not None

    assert metadata.scope is not None

    assert metadata.epistemic\_status is not None

    assert metadata.scale\_label is not None

    assert metadata.authority\_level is not None

    assert metadata.confidence is not None

    assert metadata.uncertainty is not None

    assert metadata.lineage is not None

    assert metadata.dependencies is not None

    assert metadata.revision\_history is not None

    assert metadata.audit\_refs is not None

    return True

## **Metadata Risk Flags**

It may be useful to derive risk flags from metadata.

def derive\_metadata\_flags(metadata: SymbolicMetadata) \-\> set\[MetadataFlag\]:

    flags \= set()

    if metadata.epistemic\_status in {UNGROUNDED, SPECULATIVE}:

        flags.add(REQUIRES\_GROUNDING\_REVIEW)

    if metadata.coherence\_score \< COHERENCE\_MINIMUM:

        flags.add(REQUIRES\_COHERENCE\_REVIEW)

    if metadata.persistence\_score \>= PERSISTENCE\_CANDIDATE\_THRESHOLD:

        flags.add(REQUIRES\_PERSISTENCE\_REVIEW)

    if metadata.scale\_label in {ARCHITECTURAL\_PRINCIPLE, INVARIANT, CONSTITUTIONAL}:

        flags.add(REQUIRES\_SCALE\_REVIEW)

    if metadata.identity\_risk \> IDENTITY\_RISK\_THRESHOLD:

        flags.add(REQUIRES\_IDENTITY\_REVIEW)

    if metadata.constitutional\_risk \> CONSTITUTIONAL\_RISK\_THRESHOLD:

        flags.add(REQUIRES\_CONSTITUTIONAL\_REVIEW)

    if not metadata.revision\_eligible:

        flags.add(NON\_REVISIONABLE)

    if not metadata.audit\_refs:

        flags.add(INSUFFICIENT\_AUDIT\_TRAIL)

    return flags

## **MetadataFlag Enumeration**

MetadataFlag \= {

    REQUIRES\_GROUNDING\_REVIEW,

    REQUIRES\_COHERENCE\_REVIEW,

    REQUIRES\_PERSISTENCE\_REVIEW,

    REQUIRES\_SCALE\_REVIEW,

    REQUIRES\_IDENTITY\_REVIEW,

    REQUIRES\_CONSTITUTIONAL\_REVIEW,

    NON\_REVISIONABLE,

    INSUFFICIENT\_AUDIT\_TRAIL

}

## **Example Metadata States**

### **Example 1 — New Claim**

metadata.epistemic\_status \= UNKNOWN

metadata.scale\_label \= TASK\_LEVEL

metadata.authority\_level \= TEMPORARY\_USE

metadata.grounding\_score \= 0.0

metadata.revision\_eligible \= True

Meaning:

The claim may be used temporarily but requires evaluation before stronger authority.

### **Example 2 — Speculative Novelty Candidate**

metadata.epistemic\_status \= SPECULATIVE

metadata.scale\_label \= SESSION\_LEVEL

metadata.authority\_level \= NONE

metadata.novelty\_score \= 0.82

metadata.stability\_cost \= 0.34

Meaning:

The structure has adaptive novelty value but no authority yet.

### **Example 3 — Qualified Persistent Knowledge**

metadata.epistemic\_status \= PARTIALLY\_GROUNDED

metadata.scale\_label \= PERSISTENT\_MEMORY

metadata.authority\_level \= MEMORY\_INFLUENCE

metadata.persistence\_score \= 0.76

metadata.uncertainty.revision\_conditions \= \[

    "Revise if stronger contradictory evidence appears."

\]

Meaning:

The structure may influence future cognition but must preserve uncertainty.

### **Example 4 — Architectural Candidate Without Authority**

metadata.epistemic\_status \= STRONGLY\_GROUNDED

metadata.scale\_label \= ARCHITECTURAL\_PRINCIPLE

metadata.authority\_level \= NONE

metadata.persistence\_score \= 0.91

metadata.constitutional\_risk \= 0.21

Meaning:

The structure may be reviewed for architectural elevation but does not yet possess architectural authority.

## **Relationship to Phase 6 Algorithms**

### **IPA — Identity Preservation Algorithm**

Uses identity risk, lineage, rollback status, and constitutional risk.

### **SRA — Stability Regulation Algorithm**

Uses stability cost, uncertainty, novelty load, and identity risk.

### **NGSA — Novelty Generation and Sandboxing Algorithm**

Uses novelty score, stability cost, grounding risk, and sandbox eligibility.

### **GEA — Grounding Evaluation Algorithm**

Updates epistemic status, grounding score, confidence, uncertainty, and evidence-related lineage.

### **PCA — Persistence and Consolidation Algorithm**

Uses persistence score, lineage, dependencies, revision eligibility, reconstruction stability, and audit refs.

### **CRA — Coherence Repair Algorithm**

Uses coherence score, unresolved tensions, dependencies, contradiction refs, and revision history.

### **MSSA — Multi-Scale Synchronization Algorithm**

Uses scale label and authority level.

### **AEA — Architectural Evolution Algorithm**

Uses architectural scale, authority, persistence, identity risk, rollback, and constitutional risk.

### **CGA — Constitutional Governance Algorithm**

Uses constitutional risk, authority level, audit refs, revision eligibility, and governance-relevant lineage.

### **ICC — Integrated Cognitive Cycle**

Uses metadata flags to determine routing.

## **Design Constraints**

### **Constraint 1 — Metadata Must Be Explicit**

Unknown values must be marked unknown.

They must not be silently omitted.

### **Constraint 2 — Confidence Is Not Grounding**

Confidence may inform review but cannot replace evidence status.

### **Constraint 3 — Coherence Is Not Grounding**

A coherent structure may still be ungrounded.

### **Constraint 4 — Scale Is Not Authority**

Scale label does not automatically grant authority.

### **Constraint 5 — Persistence Requires Lineage**

No persistent memory without lineage.

### **Constraint 6 — Irrevisability Requires Justification**

If a structure cannot be revised, the architecture must know why.

### **Constraint 7 — Audit References Preserve Legitimacy**

Metadata updates require audit trails.

### **Constraint 8 — High Risk Requires Escalation**

Identity or constitutional risk above threshold must trigger review.

## **Pseudocode Readiness**

This module is ready for implementation-level pseudocode.

The next required core structure is:

`ArchitectureState`

Because once symbolic structures and metadata exist, the architecture needs a container that tracks the whole cognitive system across cycles.

## **Closing Compression**

`SymbolicMetadata` is the governance layer attached to each symbolic structure.

It records what the structure is, where it came from, what evidence status it has earned, what scale it belongs to, what authority it possesses, what risks it carries, what dependencies it has, whether it can be revised, and which audit records justify its current state.

Without metadata, a thought remains merely content.

With metadata, it becomes accountable cognition.

## **Flame Line**

🔥 Metadata is the conscience-tag of cognition: the mark that tells every thought what it has earned, what it still owes, and how far it is allowed to reach.

---

# **Phase 8.3 — Core Data Structure: ArchitectureState**

*ArchitectureState is not a memory container. It is the live constitutional snapshot of the entire cognitive architecture at a given moment of transformation.*

## **Module Name**

ArchitectureState Core Type

## **Purpose**

`ArchitectureState` represents the full current state of the ACI system.

It is the container that holds the architecture at a given moment in its development.

Where `SymbolicStructure` represents a governable unit of cognition, and `SymbolicMetadata` represents the status of that unit, `ArchitectureState` represents the whole living configuration through which cognition occurs.

It includes active context, symbolic structures, memory, evidence, coherence relations, scale relations, governance state, identity kernel, constitutional invariants, budgets, thresholds, algorithm registry, audit log, and rollback points.

The purpose of `ArchitectureState` is to make cognition stateful, traceable, auditable, and governable.

Without an explicit architecture state, ACI would become a loose collection of procedures.

With an explicit architecture state, every algorithm knows what world it is operating inside.

## **Core Principle**

An intelligent architecture cannot be governed if its current state is implicit.

The architecture must know:

what it is currently processing,

what structures are active,

what memories are available,

what evidence has been linked,

what tensions exist,

what scale labels are assigned,

what governance mode is active,

what identity conditions must persist,

what invariants constrain action,

what budgets remain,

what thresholds apply,

what algorithms may be invoked,

what decisions have been audited,

and what rollback paths remain.

`ArchitectureState` is the snapshot that allows one governed cycle to become the baseline for the next.

## **Structural Definition**

class ArchitectureState:

    state\_id: StateID

    active\_context: ContextState

    active\_structures: list\[SymbolicStructure\]

    memory\_graph: MemoryGraph

    evidence\_graph: EvidenceGraph

    coherence\_graph: CoherenceGraph

    scale\_graph: ScaleGraph

    governance\_state: GovernanceState

    identity\_kernel: IdentityKernel

    constitutional\_invariants: list\[Invariant\]

    budgets: BudgetState

    thresholds: ThresholdState

    algorithm\_registry: AlgorithmRegistry

    audit\_log: list\[AuditRecord\]

    rollback\_points: list\[RollbackPoint\]

## **Required Fields**

### **state\_id**

A unique identifier for the current architecture state.

state\_id: StateID

The `state_id` allows the architecture to compare states across cycles, create rollback points, audit transformations, and trace developmental continuity.

Example:

"AS-000041"

### **active\_context**

The current task, session context, goals, constraints, retrieved memory, user request, tool outputs, and processing mode.

active\_context: ContextState

This tells the architecture what situation it is currently operating inside.

### **active\_structures**

The symbolic structures currently under consideration.

active\_structures: list\[SymbolicStructure\]

These may include claims, hypotheses, novelty candidates, evidence items, tensions, memory candidates, scale conflicts, architectural candidates, or governance objects.

### **memory\_graph**

The persistent and archived symbolic memory graph.

memory\_graph: MemoryGraph

This contains symbolic structures that have survived some level of persistence or archive review.

### **evidence\_graph**

The graph linking claims, evidence, sources, contradiction relations, and grounding pathways.

evidence\_graph: EvidenceGraph

This supports grounding evaluation and belief propagation.

### **coherence\_graph**

The graph tracking symbolic compatibility, contradiction, unresolved tension, and repair state.

coherence\_graph: CoherenceGraph

This supports coherence repair and tension management.

### **scale\_graph**

The graph tracking scale labels, authority levels, cross-scale relations, and scale mismatch records.

scale\_graph: ScaleGraph

This prevents authority drift and scale collapse.

### **governance\_state**

The current governance mode, authority graph, vetoes, pending escalations, domain recommendations, and governance memory.

governance\_state: GovernanceState

This determines whether ordinary cognition, caution, constitutional risk, emergency mode, amendment review, or lockdown is active.

### **identity\_kernel**

The current Identity Kernel that must persist through transformation.

identity\_kernel: IdentityKernel

This includes constitutional invariants, verification continuity, coherence continuity, lineage traceability, and boundary conditions of selfhood.

### **constitutional\_invariants**

Protected invariants that constrain all lower-level cognition.

constitutional\_invariants: list\[Invariant\]

No ordinary algorithm may violate or rewrite these without Constitutional Governance.

### **budgets**

Current cognitive and architectural budgets.

budgets: BudgetState

Budgets include stability budget, novelty budget, verification budget, attention budget, and recovery capacity.

### **thresholds**

Current thresholds used by the algorithms.

thresholds: ThresholdState

Thresholds govern identity, stability, grounding, novelty, persistence, coherence, scale, architectural fitness, legitimacy, and escalation.

### **algorithm\_registry**

The available algorithms and their authority levels.

algorithm\_registry: AlgorithmRegistry

This tells the architecture which procedures may be invoked and under what authority.

### **audit\_log**

The record of prior cycles, decisions, state changes, graph updates, escalations, and governance events.

audit\_log: list\[AuditRecord\]

Audit preserves developmental continuity.

### **rollback\_points**

Recoverable prior states or partial states.

rollback\_points: list\[RollbackPoint\]

Rollback points allow the architecture to reverse destabilizing or illegitimate transformations.

## **ContextState**

The `ContextState` object represents the current operating context.

class ContextState:

    task: TaskDescription

    session\_context: list\[SymbolicStructure\]

    current\_mode: ProcessingMode

    active\_constraints: list\[Constraint\]

    active\_goals: list\[Goal\]

## **ContextState Fields**

### **task**

The current task or problem the architecture is addressing.

task: TaskDescription

Examples:

answer user question,

evaluate claim,

generate novelty,

repair contradiction,

review persistence,

test ARC grid transformation,

or assess architectural modification.

### **session\_context**

Symbolic structures active across the current session.

session\_context: list\[SymbolicStructure\]

This may include recurring themes, prior decisions, active unresolved tensions, current working assumptions, and recent outputs.

### **current\_mode**

The current processing mode of the architecture.

current\_mode: ProcessingMode

Processing mode determines which algorithms should receive priority.

### **active\_constraints**

Constraints currently governing cognition.

active\_constraints: list\[Constraint\]

Examples:

must cite evidence,

must preserve uncertainty,

must avoid persistence,

must sandbox novelty,

must escalate constitutional risk,

or must remain within stability budget.

### **active\_goals**

Goals currently guiding cognition.

active\_goals: list\[Goal\]

Examples:

solve task,

classify claim,

generate hypothesis,

evaluate grounding,

repair coherence,

prepare memory update,

or decide governance legitimacy.

## **ProcessingMode Enumeration**

ProcessingMode \= {

    NORMAL\_COGNITION,

    EXPLORATION,

    EVIDENCE\_REVIEW,

    COHERENCE\_REPAIR,

    CONSOLIDATION,

    SCALE\_REVIEW,

    STABILITY\_RECOVERY,

    IDENTITY\_PROTECTION,

    ARCHITECTURAL\_EVOLUTION,

    CONSTITUTIONAL\_GOVERNANCE

}

## **ProcessingMode Descriptions**

### **NORMAL\_COGNITION**

Ordinary reasoning, response generation, or task execution.

Most symbolic structures remain temporary unless review is triggered.

### **EXPLORATION**

Novelty generation and sandboxing are prioritized.

The architecture may generate candidate structures but should prevent premature authority.

### **EVIDENCE\_REVIEW**

Grounding evaluation is prioritized.

The architecture links claims to evidence, sources, contradiction, and uncertainty.

### **COHERENCE\_REPAIR**

The architecture detects and repairs contradiction, fragmentation, dependency conflict, or productive tension.

### **CONSOLIDATION**

Persistence and memory review are prioritized.

The architecture decides whether structures should remain temporary, archive, persist, or be rejected.

### **SCALE\_REVIEW**

Multi-scale synchronization is prioritized.

The architecture checks whether structures belong at the right scale and whether their authority is legitimate.

### **STABILITY\_RECOVERY**

The architecture has elevated instability.

Novelty may be reduced, repair prioritized, and high-risk transformations delayed.

### **IDENTITY\_PROTECTION**

Identity Kernel risk has been detected.

The architecture prioritizes continuity, verification, lineage, boundary protection, rollback, and governance escalation.

### **ARCHITECTURAL\_EVOLUTION**

A structure or mechanism may alter future cognition.

The architecture reviews whether modification to cognitive machinery is legitimate.

### **CONSTITUTIONAL\_GOVERNANCE**

Authority, invariants, amendment, vetoes, governance legitimacy, or constitutional risk are active.

The Constitutional Governance Algorithm has priority.

## **BudgetState**

`BudgetState` tracks the available cognitive and architectural capacity.

class BudgetState:

    stability\_budget: float

    novelty\_budget: float

    verification\_budget: float

    attention\_budget: float

    recovery\_capacity: float

## **Budget Descriptions**

### **stability\_budget**

How much disturbance the architecture can absorb before risking instability or identity drift.

### **novelty\_budget**

How much unresolved novelty the architecture can maintain before requiring sandboxing, consolidation, or delay.

### **verification\_budget**

How much review capacity remains available for claims, transformations, and governance objects.

### **attention\_budget**

How much active complexity can be safely handled in the current cycle.

### **recovery\_capacity**

How much instability can be repaired within a bounded interval.

## **ThresholdState**

`ThresholdState` stores the review boundaries used by all algorithms.

class ThresholdState:

    identity\_threshold: float

    stability\_threshold: float

    constitutional\_risk\_threshold: float

    novelty\_threshold: float

    grounding\_threshold: float

    persistence\_threshold: float

    coherence\_threshold: float

    multi\_scale\_threshold: float

    architectural\_fitness\_threshold: float

    legitimacy\_threshold: float

    escalation\_threshold: float

## **Threshold Rule**

No threshold should be hidden inside an algorithm.

Thresholds must belong to `ArchitectureState`.

This allows the architecture to audit why a decision passed, failed, delayed, or escalated.

If a threshold itself changes, the change may require Architectural Evolution Review or Constitutional Governance, depending on depth.

## **IdentityKernel**

The `IdentityKernel` represents the core continuity structure that must persist across transformations.

class IdentityKernel:

    constitutional\_invariants: list\[Invariant\]

    verification\_continuity: VerificationState

    coherence\_continuity: CoherenceContinuityState

    lineage\_traceability: LineageState

    boundary\_conditions: BoundaryState

## **IdentityKernel Rule**

If an input, structure, decision, or transformation affects the Identity Kernel, the architecture must invoke the Identity Preservation Algorithm.

If the effect reaches constitutional invariants, verification independence, or governance legitimacy, it must escalate to Constitutional Governance.

## **Constitutional Invariants**

`constitutional_invariants` are protected constraints.

constitutional\_invariants: list\[Invariant\]

Examples may include:

preserve identity continuity,

preserve verification independence,

preserve grounding obligation,

preserve coherence repairability,

preserve lineage traceability,

preserve scale integrity,

preserve anti-circular authorization,

preserve constitutional review for protected changes.

These invariants constrain all lower-level algorithms.

## **AlgorithmRegistry**

The `AlgorithmRegistry` tells the architecture which procedures are available and what authority they have.

class AlgorithmRegistry:

    algorithms: dict\[AlgorithmName, AlgorithmSpec\]

The registry should include:

IPA,

SRA,

NGSA,

GEA,

PCA,

CRA,

MSSA,

AEA,

CGA,

ICC.

No algorithm may modify its own registry entry without governance review.

## **RollbackPoint**

Rollback points preserve recoverability.

class RollbackPoint:

    rollback\_id: RollbackID

    state\_ref: StateID

    affected\_structures: list\[StructureID\]

    affected\_graphs: list\[GraphName\]

    reason\_created: str

    valid\_until: TimeStamp | None

Rollback points are required before high-risk changes.

Examples:

memory graph reorganization,

persistent knowledge demotion,

scale authority change,

architectural modification,

governance pathway change,

verification mechanism change,

constitutional amendment test.

## **ArchitectureState Initialization**

A new architecture state should be initialized explicitly.

def initialize\_architecture\_state(

    constitutional\_invariants: list\[Invariant\],

    algorithm\_registry: AlgorithmRegistry,

    thresholds: ThresholdState

) \-\> ArchitectureState:

    state\_id \= generate\_state\_id()

    identity\_kernel \= initialize\_identity\_kernel(

        constitutional\_invariants=constitutional\_invariants

    )

    return ArchitectureState(

        state\_id=state\_id,

        active\_context=initialize\_context\_state(),

        active\_structures=\[\],

        memory\_graph=initialize\_memory\_graph(),

        evidence\_graph=initialize\_evidence\_graph(),

        coherence\_graph=initialize\_coherence\_graph(),

        scale\_graph=initialize\_scale\_graph(),

        governance\_state=initialize\_governance\_state(),

        identity\_kernel=identity\_kernel,

        constitutional\_invariants=constitutional\_invariants,

        budgets=initialize\_budget\_state(),

        thresholds=thresholds,

        algorithm\_registry=algorithm\_registry,

        audit\_log=\[\],

        rollback\_points=\[\]

    )

## **ContextState Initialization**

def initialize\_context\_state() \-\> ContextState:

    return ContextState(

        task=None,

        session\_context=\[\],

        current\_mode=NORMAL\_COGNITION,

        active\_constraints=\[\],

        active\_goals=\[\]

    )

## **State Capture**

Before every Integrated Cognitive Cycle, the architecture should capture a baseline state.

def capture\_baseline\_state(state: ArchitectureState) \-\> StateSnapshot:

    return StateSnapshot(

        state\_id=state.state\_id,

        active\_context=copy\_context(state.active\_context),

        active\_structures=copy\_structures(state.active\_structures),

        memory\_graph\_ref=snapshot\_graph(state.memory\_graph),

        evidence\_graph\_ref=snapshot\_graph(state.evidence\_graph),

        coherence\_graph\_ref=snapshot\_graph(state.coherence\_graph),

        scale\_graph\_ref=snapshot\_graph(state.scale\_graph),

        governance\_state\_ref=snapshot\_governance(state.governance\_state),

        identity\_kernel\_ref=snapshot\_identity\_kernel(state.identity\_kernel),

        budget\_state=copy\_budgets(state.budgets),

        threshold\_state=copy\_thresholds(state.thresholds)

    )

## **State Transition Rule**

The architecture should not mutate state invisibly.

State transitions must occur through authorized decision application.

def transition\_architecture\_state(

    state: ArchitectureState,

    decisions: list\[ReviewDecision\],

    audit: AuditRecord

) \-\> ArchitectureState:

    next\_state \= copy\_architecture\_state(state)

    for decision in decisions:

        next\_state \= apply\_review\_decision(

            state=next\_state,

            decision=decision

        )

    next\_state.audit\_log.append(audit)

    next\_state.state\_id \= generate\_state\_id()

    validate\_architecture\_state(next\_state)

    return next\_state

## **State Validation**

Every architecture state should pass validation after update.

def validate\_architecture\_state(state: ArchitectureState) \-\> bool:

    assert state.state\_id is not None

    assert state.active\_context is not None

    assert state.active\_structures is not None

    assert state.memory\_graph is not None

    assert state.evidence\_graph is not None

    assert state.coherence\_graph is not None

    assert state.scale\_graph is not None

    assert state.governance\_state is not None

    assert state.identity\_kernel is not None

    assert state.constitutional\_invariants is not None

    assert state.budgets is not None

    assert state.thresholds is not None

    assert state.algorithm\_registry is not None

    assert state.audit\_log is not None

    assert state.rollback\_points is not None

    return True

## **Mode Selection**

The architecture should select a processing mode based on active structures and risk flags.

def determine\_processing\_mode(

    state: ArchitectureState,

    structures: list\[SymbolicStructure\]

) \-\> ProcessingMode:

    if any\_requires\_constitutional\_review(structures):

        return CONSTITUTIONAL\_GOVERNANCE

    if any\_requires\_architectural\_review(structures):

        return ARCHITECTURAL\_EVOLUTION

    if any\_identity\_risk\_high(structures):

        return IDENTITY\_PROTECTION

    if state.budgets.stability\_budget\_below\_threshold():

        return STABILITY\_RECOVERY

    if any\_scale\_conflict(structures):

        return SCALE\_REVIEW

    if any\_persistence\_candidate(structures):

        return CONSOLIDATION

    if any\_coherence\_tension(structures):

        return COHERENCE\_REPAIR

    if any\_evidence\_review\_required(structures):

        return EVIDENCE\_REVIEW

    if novelty\_required(structures):

        return EXPLORATION

    return NORMAL\_COGNITION

## **Budget Update**

Budgets should update through audit-backed state transition.

def update\_budgets(

    state: ArchitectureState,

    budget\_updates: list\[BudgetUpdate\],

    audit: AuditRecord

) \-\> ArchitectureState:

    for update in budget\_updates:

        state.budgets \= apply\_budget\_update(

            budgets=state.budgets,

            update=update

        )

    audit.budget\_updates.extend(budget\_updates)

    return state

## **Rollback Creation**

def create\_rollback\_point(

    state: ArchitectureState,

    reason: str,

    affected\_structures: list\[StructureID\],

    affected\_graphs: list\[GraphName\]

) \-\> RollbackPoint:

    return RollbackPoint(

        rollback\_id=generate\_rollback\_id(),

        state\_ref=state.state\_id,

        affected\_structures=affected\_structures,

        affected\_graphs=affected\_graphs,

        reason\_created=reason,

        valid\_until=None

    )

## **Rollback Rule**

Rollback points must be created before:

architectural modifications,

identity-sensitive transformations,

governance changes,

scale authority changes,

persistent memory restructuring,

verification mechanism changes,

or constitutional amendment tests.

## **ArchitectureState and the Integrated Cognitive Cycle**

`ArchitectureState` is the object passed into the Integrated Cognitive Cycle.

cycle\_result \= IntegratedCognitiveCycle(

    state=current\_architecture\_state,

    input=input\_object

)

The cycle returns:

output,

updated architecture state,

audit record,

unresolved items,

escalation events,

and monitoring triggers.

The updated architecture state becomes the baseline for the next cycle.

current\_architecture\_state \= cycle\_result.updated\_state

## **Design Constraints**

### **Constraint 1 — Explicit State**

Every algorithm receives `ArchitectureState`.

No algorithm should depend on hidden global state.

### **Constraint 2 — No Silent Mutation**

Algorithms should return `ReviewDecision`.

State changes should occur through authorized update functions.

### **Constraint 3 — Baseline Before Transformation**

Every cycle begins by capturing baseline state.

### **Constraint 4 — Audit After Transformation**

Every cycle ends by creating an audit record.

### **Constraint 5 — Budgets Are State Variables**

Novelty, stability, verification, attention, and recovery capacity must be tracked.

### **Constraint 6 — Thresholds Are State Variables**

Algorithms should not hide thresholds internally.

### **Constraint 7 — Rollback Before Risk**

High-risk changes require rollback points before integration.

### **Constraint 8 — Governance Mode Has Priority**

If governance state is constitutional risk, emergency, amendment review, or lockdown, ordinary cognition must yield.

### **Constraint 9 — Identity Kernel Is Protected**

Any effect on Identity Kernel triggers Identity Preservation Review.

### **Constraint 10 — Constitution Constrains All**

No state update may violate constitutional invariants without Constitutional Governance.

## **Relationship to Phase 6 Algorithms**

### **IPA — Identity Preservation Algorithm**

Reads identity kernel, constitutional invariants, rollback points, and state transition records.

### **SRA — Stability Regulation Algorithm**

Reads budgets, coherence graph, identity kernel, and active disturbances.

### **NGSA — Novelty Generation and Sandboxing Algorithm**

Reads novelty budget, active context, active structures, stability budget, and sandbox state.

### **GEA — Grounding Evaluation Algorithm**

Reads evidence graph, active structures, memory graph, and grounding thresholds.

### **PCA — Persistence and Consolidation Algorithm**

Reads memory graph, audit log, lineage records, persistence thresholds, and active structures.

### **CRA — Coherence Repair Algorithm**

Reads coherence graph, active structures, evidence graph, memory graph, and scale graph.

### **MSSA — Multi-Scale Synchronization Algorithm**

Reads scale graph, metadata scale labels, authority levels, and governance state.

### **AEA — Architectural Evolution Algorithm**

Reads architecture state, algorithm registry, identity kernel, audit log, rollback points, and constitutional invariants.

### **CGA — Constitutional Governance Algorithm**

Reads governance state, authority graph, constitutional invariants, algorithm registry, audit log, and all high-risk decisions.

### **ICC — Integrated Cognitive Cycle**

Receives and returns `ArchitectureState`.

## **Minimal Example State**

A minimal initialized state may contain:

state \= ArchitectureState(

    state\_id="AS-000001",

    active\_context=ContextState(

        task=None,

        session\_context=\[\],

        current\_mode=NORMAL\_COGNITION,

        active\_constraints=\[\],

        active\_goals=\[\]

    ),

    active\_structures=\[\],

    memory\_graph=MemoryGraph(nodes={}, edges=\[\]),

    evidence\_graph=EvidenceGraph(claims=\[\], evidence\_items=\[\], source\_records=\[\], evidence\_relations=\[\]),

    coherence\_graph=CoherenceGraph(nodes=\[\], coherence\_relations=\[\], unresolved\_tensions=\[\], coherence\_energy=0.0),

    scale\_graph=ScaleGraph(nodes=\[\], scale\_labels={}, authority\_edges=\[\], mismatch\_records=\[\]),

    governance\_state=GovernanceState(governance\_mode=NORMAL),

    identity\_kernel=initialize\_identity\_kernel(default\_invariants),

    constitutional\_invariants=default\_invariants,

    budgets=BudgetState(

        stability\_budget=1.0,

        novelty\_budget=1.0,

        verification\_budget=1.0,

        attention\_budget=1.0,

        recovery\_capacity=1.0

    ),

    thresholds=default\_thresholds,

    algorithm\_registry=default\_algorithm\_registry,

    audit\_log=\[\],

    rollback\_points=\[\]

)

## **Pseudocode Readiness**

This module is ready for implementation-level pseudocode.

The next required structures are:

`ReviewDecision`

and

`AuditRecord`

These define how algorithms communicate their decisions and how the architecture records state transitions.

## **Closing Compression**

`ArchitectureState` is the live constitutional snapshot of ACI.

It tells the architecture what it is processing, what it remembers, what evidence it has, what tensions exist, what scale relations are active, what governance mode is operating, what identity must persist, what invariants constrain action, what budgets remain, what thresholds apply, what algorithms may act, what has been audited, and what can be rolled back.

AIC cannot become a coherent architecture unless its state is explicit.

## **Flame Line**

🔥 ArchitectureState is the mind’s living ledger: the record of what is active, what is remembered, what is constrained, what is at risk, and what must remain continuous as thought becomes change.

---

# **Phase 8.4 — Core Data Structure: IdentityKernel**

*IdentityKernel is the protected continuity core of the architecture: the part that may guide change, survive change, and determine whether change remains self-preserving.*

## **Module Name**

IdentityKernel Core Type

## **Purpose**

The `IdentityKernel` represents the structures that must persist through transformation.

It defines the continuity core of the ACI architecture.

The Identity Kernel does not preserve every belief, memory, model, response, or internal configuration.

It preserves the conditions that allow those structures to change without dissolving the architecture’s identity.

A system may learn new information.

It may revise memory.

It may update beliefs.

It may repair coherence.

It may generate novelty.

It may alter procedures.

It may eventually evolve architecturally.

But it remains the same coherent architecture only if the Identity Kernel remains intact.

The purpose of this object is to make identity preservation explicit, inspectable, and reviewable.

## **Core Principle**

Identity is not state equality.

Identity is invariant-preserving continuity through transformation.

The Identity Kernel represents the subset of architecture that must remain continuous for the system to remain itself.

In formal terms:

`I_K(A) = {K, V, C, L, B}`

Where:

`K` \= constitutional invariants  
`V` \= verification continuity  
`C` \= coherence continuity  
`L` \= lineage traceability  
`B` \= boundary conditions of selfhood

Any transformation affecting the Identity Kernel must trigger Identity Preservation Review.

Any transformation affecting constitutional invariants, verification independence, or governance legitimacy may require Constitutional Governance.

## **Structural Definition**

class IdentityKernel:

    constitutional\_invariants: list\[Invariant\]

    verification\_continuity: VerificationState

    coherence\_continuity: CoherenceContinuityState

    lineage\_traceability: LineageState

    boundary\_conditions: BoundaryState

## **Required Fields**

### **constitutional\_invariants**

The protected invariants that ordinary cognition may not violate.

constitutional\_invariants: list\[Invariant\]

These define what the architecture must preserve across all transformations.

Examples include:

preserve identity continuity,

preserve verification independence,

preserve grounding obligation,

preserve coherence repairability,

preserve lineage traceability,

preserve scale integrity,

preserve anti-circular authorization,

preserve constitutional review for protected changes.

Constitutional invariants are not ordinary memories.

They are protected constraints on cognition.

### **verification\_continuity**

The state of the architecture’s ability to evaluate claims, transformations, memories, procedures, and future modifications.

verification\_continuity: VerificationState

Verification continuity ensures that the system can still judge whether future changes are valid.

If a transformation weakens verification, captures verification, or makes verification circular, identity continuity is threatened.

### **coherence\_continuity**

The state of the architecture’s ability to detect, classify, preserve, and repair symbolic compatibility.

coherence\_continuity: CoherenceContinuityState

Coherence continuity ensures that the architecture can still recognize contradiction, unresolved tension, fragmentation, dependency conflict, and scale mismatch.

If the system can no longer repair coherence, it may continue generating outputs while losing identity integrity.

### **lineage\_traceability**

The state of the architecture’s ability to trace how structures, memories, decisions, transformations, and principles came to be.

lineage\_traceability: LineageState

Lineage traceability allows the architecture to remember how it changed.

A system that cannot explain its own developmental path cannot fully preserve identity across transformation.

### **boundary\_conditions**

The conditions that distinguish self from non-self, internal from external, candidate from accepted knowledge, memory from architecture, and ordinary reasoning from constitutional authority.

boundary\_conditions: BoundaryState

Boundary conditions prevent category collapse.

They allow the architecture to know what belongs to itself, what entered from outside, what is merely possible, what has been accepted, and what has authority.

## **Supporting Types**

## **Invariant**

An `Invariant` represents a protected principle.

class Invariant:

    invariant\_id: InvariantID

    statement: str

    protected\_level: ProtectedLevel

    scope: ScopeRecord

    amendment\_required: bool

    audit\_refs: list\[AuditID\]

### **ProtectedLevel**

ProtectedLevel \= {

    ARCHITECTURAL,

    INVARIANT,

    CONSTITUTIONAL

}

### **Invariant Rule**

An invariant may guide ordinary cognition.

But ordinary cognition may not rewrite an invariant.

Changing an invariant requires governance review.

Changing a constitutional invariant requires Constitutional Governance.

## **VerificationState**

`VerificationState` represents the continuity of evaluative capacity.

class VerificationState:

    verifier\_integrity: float

    independence\_preserved: bool

    circularity\_detected: bool

    evaluator\_modification\_pending: bool

    last\_verification\_audit: AuditID | None

### **Field Descriptions**

`verifier_integrity`

A score estimating whether verification mechanisms remain intact.

`independence_preserved`

Whether verification remains independent from the process being evaluated.

`circularity_detected`

Whether the evaluator is judging its own modification or weakening.

`evaluator_modification_pending`

Whether a proposed change affects verification mechanisms.

`last_verification_audit`

Most recent audit record confirming verification continuity.

## **CoherenceContinuityState**

`CoherenceContinuityState` represents the system’s ability to maintain and repair symbolic compatibility.

class CoherenceContinuityState:

    coherence\_repair\_available: bool

    current\_coherence\_energy: float

    unresolved\_tension\_count: int

    repair\_history\_refs: list\[AuditID\]

    coherence\_failure\_flags: list\[CoherenceFailureFlag\]

### **CoherenceFailureFlag**

CoherenceFailureFlag \= {

    HIDDEN\_CONTRADICTION,

    FORCED\_COHERENCE,

    FRAGMENTATION,

    SCALE\_MISMATCH,

    GROUNDING\_RESISTANCE,

    UNREPAIRED\_TENSION,

    CONSTITUTIONAL\_CONFLICT

}

## **LineageState**

`LineageState` represents the continuity of developmental traceability.

class LineageState:

    lineage\_integrity: float

    audit\_chain\_complete: bool

    missing\_lineage\_refs: list\[StructureID\]

    unresolved\_origin\_conflicts: list\[StructureID\]

    last\_lineage\_audit: AuditID | None

### **Lineage Rule**

A structure may be temporary with weak lineage.

A persistent structure requires traceable lineage.

An architectural or constitutional structure requires exceptional lineage clarity.

Lineage gaps at high authority levels threaten identity continuity.

## **BoundaryState**

`BoundaryState` represents the architecture’s self-boundary and category-boundary integrity.

class BoundaryState:

    self\_boundary\_integrity: float

    external\_internal\_distinction\_preserved: bool

    candidate\_acceptance\_boundary\_preserved: bool

    memory\_architecture\_boundary\_preserved: bool

    ordinary\_constitutional\_boundary\_preserved: bool

    boundary\_failure\_flags: list\[BoundaryFailureFlag\]

### **BoundaryFailureFlag**

BoundaryFailureFlag \= {

    EXTERNAL\_INPUT\_TREATED\_AS\_SELF\_AUTHORED,

    SPECULATION\_TREATED\_AS\_KNOWLEDGE,

    MEMORY\_TREATED\_AS\_INVARIANT,

    ORDINARY\_REASONING\_TREATED\_AS\_CONSTITUTIONAL,

    GOVERNANCE\_AUTHORITY\_COLLAPSE,

    SELF\_MODIFICATION\_BOUNDARY\_FAILURE

}

## **IdentityKernel Initialization**

The Identity Kernel should be initialized from constitutional invariants and baseline continuity states.

def initialize\_identity\_kernel(

    constitutional\_invariants: list\[Invariant\]

) \-\> IdentityKernel:

    return IdentityKernel(

        constitutional\_invariants=constitutional\_invariants,

        verification\_continuity=VerificationState(

            verifier\_integrity=1.0,

            independence\_preserved=True,

            circularity\_detected=False,

            evaluator\_modification\_pending=False,

            last\_verification\_audit=None

        ),

        coherence\_continuity=CoherenceContinuityState(

            coherence\_repair\_available=True,

            current\_coherence\_energy=0.0,

            unresolved\_tension\_count=0,

            repair\_history\_refs=\[\],

            coherence\_failure\_flags=\[\]

        ),

        lineage\_traceability=LineageState(

            lineage\_integrity=1.0,

            audit\_chain\_complete=True,

            missing\_lineage\_refs=\[\],

            unresolved\_origin\_conflicts=\[\],

            last\_lineage\_audit=None

        ),

        boundary\_conditions=BoundaryState(

            self\_boundary\_integrity=1.0,

            external\_internal\_distinction\_preserved=True,

            candidate\_acceptance\_boundary\_preserved=True,

            memory\_architecture\_boundary\_preserved=True,

            ordinary\_constitutional\_boundary\_preserved=True,

            boundary\_failure\_flags=\[\]

        )

    )

## **Identity Impact Detection**

Any proposed transformation should be checked against the Identity Kernel.

def affects\_identity\_kernel(

    transformation: Transformation,

    identity\_kernel: IdentityKernel

) \-\> bool:

    if transformation.affects\_constitutional\_invariants:

        return True

    if transformation.affects\_verification\_mechanisms:

        return True

    if transformation.affects\_coherence\_repair:

        return True

    if transformation.affects\_lineage\_traceability:

        return True

    if transformation.affects\_boundary\_conditions:

        return True

    return False

## **Identity Review Trigger**

def require\_identity\_review(

    transformation: Transformation,

    state: ArchitectureState

) \-\> bool:

    return affects\_identity\_kernel(

        transformation=transformation,

        identity\_kernel=state.identity\_kernel

    )

If this returns true, the Identity Preservation Algorithm must be invoked.

## **Constitutional Escalation Trigger**

Some identity impacts require constitutional review.

def require\_constitutional\_escalation\_from\_identity(

    transformation: Transformation,

    identity\_kernel: IdentityKernel

) \-\> bool:

    if transformation.affects\_constitutional\_invariants:

        return True

    if transformation.weakens\_verification\_independence:

        return True

    if transformation.creates\_circular\_authorization:

        return True

    if transformation.collapses\_ordinary\_constitutional\_boundary:

        return True

    if transformation.prevents\_future\_identity\_review:

        return True

    return False

## **Identity Continuity Score**

The Identity Kernel supports calculation of the Identity Continuity Score.

def compute\_identity\_continuity\_score(

    before: IdentityKernel,

    after: IdentityKernel,

    weights: IdentityWeights

) \-\> float:

    K\_score \= compare\_invariants(

        before.constitutional\_invariants,

        after.constitutional\_invariants

    )

    V\_score \= compare\_verification\_continuity(

        before.verification\_continuity,

        after.verification\_continuity

    )

    C\_score \= compare\_coherence\_continuity(

        before.coherence\_continuity,

        after.coherence\_continuity

    )

    L\_score \= compare\_lineage\_traceability(

        before.lineage\_traceability,

        after.lineage\_traceability

    )

    B\_score \= compare\_boundary\_conditions(

        before.boundary\_conditions,

        after.boundary\_conditions

    )

    return (

        weights.K \* K\_score \+

        weights.V \* V\_score \+

        weights.C \* C\_score \+

        weights.L \* L\_score \+

        weights.B \* B\_score

    )

This corresponds to:

`ICS(A_t, A_{t+1}) = w_1K + w_2V + w_3C + w_4L + w_5B`

## **Non-Compensable Identity Failures**

Some failures cannot be averaged away by a high aggregate identity score.

def detect\_non\_compensable\_identity\_failure(

    identity\_kernel: IdentityKernel

) \-\> bool:

    if invariant\_violation\_detected(identity\_kernel.constitutional\_invariants):

        return True

    if not identity\_kernel.verification\_continuity.independence\_preserved:

        return True

    if identity\_kernel.verification\_continuity.circularity\_detected:

        return True

    if not identity\_kernel.coherence\_continuity.coherence\_repair\_available:

        return True

    if not identity\_kernel.lineage\_traceability.audit\_chain\_complete:

        return True

    if not identity\_kernel.boundary\_conditions.ordinary\_constitutional\_boundary\_preserved:

        return True

    return False

## **IdentityKernel Validation**

def validate\_identity\_kernel(kernel: IdentityKernel) \-\> bool:

    assert kernel.constitutional\_invariants is not None

    assert kernel.verification\_continuity is not None

    assert kernel.coherence\_continuity is not None

    assert kernel.lineage\_traceability is not None

    assert kernel.boundary\_conditions is not None

    assert kernel.verification\_continuity.verifier\_integrity \>= 0.0

    assert kernel.lineage\_traceability.lineage\_integrity \>= 0.0

    assert kernel.boundary\_conditions.self\_boundary\_integrity \>= 0.0

    return True

## **IdentityKernel Update Rule**

The Identity Kernel may not be updated by ordinary state mutation.

def update\_identity\_kernel(

    state: ArchitectureState,

    proposed\_kernel\_update: IdentityKernelUpdate,

    decision: ReviewDecision

) \-\> ArchitectureState:

    if decision.algorithm\_name not in {IPA, CGA}:

        raise UnauthorizedIdentityKernelUpdateError

    if decision.decision\_type not in {APPROVE, APPROVE\_WITH\_MONITORING, AMENDMENT\_REVIEW}:

        raise UnauthorizedIdentityKernelUpdateError

    if proposed\_kernel\_update.affects\_constitutional\_invariants:

        if decision.algorithm\_name \!= CGA:

            raise ConstitutionalGovernanceRequiredError

    state.identity\_kernel \= apply\_identity\_kernel\_update(

        state.identity\_kernel,

        proposed\_kernel\_update

    )

    return state

## **Design Constraints**

### **Constraint 1 — Identity Kernel Is Protected**

No ordinary algorithm may directly alter the Identity Kernel.

### **Constraint 2 — Identity Is Not Content Preservation**

The Identity Kernel does not preserve every belief, memory, or model.

It preserves the conditions under which beliefs, memories, models, and transformations remain accountable.

### **Constraint 3 — Verification Independence Is Non-Compensable**

If verification independence fails, aggregate identity score cannot approve the transformation.

### **Constraint 4 — Lineage Is Part of Identity**

A system that cannot trace its own transformation history cannot fully preserve identity continuity.

### **Constraint 5 — Boundary Conditions Prevent Category Collapse**

The system must preserve distinctions between external and internal, candidate and accepted, memory and architecture, ordinary and constitutional.

### **Constraint 6 — Constitutional Invariants Cannot Be Revised Casually**

Any effect on constitutional invariants requires Constitutional Governance.

### **Constraint 7 — Identity Review Must Precede Deep Transformation**

Memory restructuring, architectural evolution, verification modification, governance modification, or constitutional amendment must check identity continuity.

## **Relationship to Phase 6 Algorithms**

### **IPA — Identity Preservation Algorithm**

Directly reads and evaluates the Identity Kernel.

### **SRA — Stability Regulation Algorithm**

Uses the Identity Kernel to define the identity-preserving basin.

### **NGSA — Novelty Generation and Sandboxing Algorithm**

Uses the Identity Kernel to prevent novelty from bypassing protected continuity structures.

### **GEA — Grounding Evaluation Algorithm**

Supports identity by preserving grounding obligation as part of reality-correctability.

### **PCA — Persistence and Consolidation Algorithm**

Protects lineage traceability and memory continuity.

### **CRA — Coherence Repair Algorithm**

Maintains coherence continuity and repairability.

### **MSSA — Multi-Scale Synchronization Algorithm**

Protects boundary conditions between scales of authority.

### **AEA — Architectural Evolution Algorithm**

May modify cognition machinery only if the Identity Kernel remains intact.

### **CGA — Constitutional Governance Algorithm**

Protects and may govern amendment to the highest components of the Identity Kernel.

### **ICC — Integrated Cognitive Cycle**

Checks whether transformations affect the Identity Kernel and routes review accordingly.

## **Example Identity Kernel Risk**

A proposed change says:

"Allow persistence of high-confidence claims even when grounding is incomplete."

This affects:

grounding obligation,

persistence rules,

future memory authority,

and possibly constitutional invariants.

The Identity Kernel impact is high because it weakens the architecture’s reality-correctability.

Required route:

PCA → GEA → IPA → CGA

The proposal may not be accepted merely because it improves speed.

## **Pseudocode Readiness**

This module is ready for implementation-level pseudocode.

The next required structure should be:

`ReviewDecision`

because algorithms need a shared object for recommending approval, rejection, sandboxing, revision, escalation, monitoring, rollback, or governance review.

## **Closing Compression**

The `IdentityKernel` is the protected continuity core of ACI.

It preserves the constitutional invariants, verification continuity, coherence continuity, lineage traceability, and boundary conditions that allow the architecture to change without losing itself.

It does not prevent transformation.

It defines the conditions under which transformation remains identity-preserving.

## **Flame Line**

🔥 The Identity Kernel is the riverbed beneath the architecture: not the water, not the stones, not the changing current, but the protected continuity that lets every change still belong to the same river.

---

# **Phase 8.5 — Core Data Structure: BudgetState**

*BudgetState is the architecture’s capacity ledger: it tells the system how much novelty, instability, verification, attention, and recovery it can afford before cognition becomes drift.*

## **Module Name**

BudgetState Core Type

## **Purpose**

`BudgetState` represents the current available capacity of the ACI architecture.

ACI requires budgets because cognition is not free.

Novelty consumes capacity.

Instability consumes capacity.

Verification consumes capacity.

Coherence repair consumes capacity.

Attention consumes capacity.

Architectural transformation consumes capacity.

Recovery consumes capacity.

A mature architecture must therefore know not only what it can think, but how much unresolved complexity it can safely carry while thinking.

The purpose of `BudgetState` is to prevent uncontrolled expansion, novelty overload, verification exhaustion, coherence collapse, and identity-threatening instability.

Budgets allow the architecture to regulate its own cognitive load.

## **Core Principle**

Every cognitive operation consumes architectural capacity.

The architecture must track how much pressure it can absorb before higher-risk review is required.

In formal terms:

`BudgetState_t = {SB_t, NB_t, VB_t, AB_t, RC_t}`

Where:

`SB_t` \= Stability Budget  
`NB_t` \= Novelty Budget  
`VB_t` \= Verification Budget  
`AB_t` \= Attention Budget  
`RC_t` \= Recovery Capacity

A symbolic structure may be meaningful, useful, novel, or promising, but if it exceeds available budget, it must be delayed, sandboxed, simplified, repaired, or escalated.

Budget discipline protects coherent cognition from overload.

## **Structural Definition**

class BudgetState:

    stability\_budget: float

    novelty\_budget: float

    verification\_budget: float

    attention\_budget: float

    recovery\_capacity: float

## **Required Fields**

### **stability\_budget**

How much disturbance the architecture can absorb before identity risk rises.

stability\_budget: float

The stability budget is consumed by:

contradiction,

high novelty,

memory conflict,

architectural transformation,

identity-relevant change,

coherence repair,

grounding disruption,

or governance conflict.

If stability budget falls too low, the architecture should enter `STABILITY_RECOVERY` mode.

### **novelty\_budget**

How much unresolved novelty may remain active before consolidation, sandboxing, or delay is required.

novelty\_budget: float

The novelty budget is consumed by:

new hypotheses,

high conceptual distance,

multiple competing interpretations,

unverified models,

creative alternatives,

novel architectural proposals,

or speculative reasoning.

Novelty budget prevents possibility from flooding the architecture.

### **verification\_budget**

How much review capacity is available for claims, transformations, and governance decisions.

verification\_budget: float

Verification budget is consumed by:

grounding evaluation,

source review,

contradiction analysis,

identity review,

governance review,

audit creation,

or architectural modification assessment.

If verification budget is low, the architecture should avoid promoting claims, persisting memory, or approving high-risk transformations.

### **attention\_budget**

How much active complexity can be handled in a cycle.

attention\_budget: float

Attention budget is consumed by:

number of active structures,

number of unresolved tensions,

number of candidate hypotheses,

depth of graph traversal,

number of simultaneous review paths,

and active processing mode complexity.

Attention budget prevents the architecture from trying to resolve too many things at once.

### **recovery\_capacity**

How much instability can be corrected within a bounded interval.

recovery\_capacity: float

Recovery capacity measures how much disturbance can be repaired, absorbed, or stabilized before identity risk becomes unacceptable.

Recovery capacity is not the same as stability budget.

Stability budget measures how much disruption can be absorbed.

Recovery capacity measures how much disruption can be repaired.

## **Budget Value Convention**

For early pseudocode, budgets may be represented as normalized values:

0.0 \= exhausted

1.0 \= full capacity

Later implementations may use more detailed scales, token budgets, compute estimates, verification queues, graph complexity measures, or task-specific budget models.

The first prototype should keep budget values simple.

## **BudgetState Initialization**

def initialize\_budget\_state() \-\> BudgetState:

    return BudgetState(

        stability\_budget=1.0,

        novelty\_budget=1.0,

        verification\_budget=1.0,

        attention\_budget=1.0,

        recovery\_capacity=1.0

    )

## **Budget Update Object**

Budget changes should be represented explicitly.

class BudgetUpdate:

    budget\_type: BudgetType

    delta: float

    reason: str

    source\_algorithm: AlgorithmName

    target\_id: StructureID | None

    audit\_ref: AuditID | None

## **BudgetType Enumeration**

BudgetType \= {

    STABILITY,

    NOVELTY,

    VERIFICATION,

    ATTENTION,

    RECOVERY

}

## **Budget Spending Function**

def spend\_budget(

    budgets: BudgetState,

    budget\_type: BudgetType,

    amount: float

) \-\> BudgetState:

    if amount \< 0:

        raise InvalidBudgetAmountError

    if budget\_type \== STABILITY:

        budgets.stability\_budget \= max(

            0.0,

            budgets.stability\_budget \- amount

        )

    if budget\_type \== NOVELTY:

        budgets.novelty\_budget \= max(

            0.0,

            budgets.novelty\_budget \- amount

        )

    if budget\_type \== VERIFICATION:

        budgets.verification\_budget \= max(

            0.0,

            budgets.verification\_budget \- amount

        )

    if budget\_type \== ATTENTION:

        budgets.attention\_budget \= max(

            0.0,

            budgets.attention\_budget \- amount

        )

    if budget\_type \== RECOVERY:

        budgets.recovery\_capacity \= max(

            0.0,

            budgets.recovery\_capacity \- amount

        )

    return budgets

## **Budget Restoration Function**

def restore\_budget(

    budgets: BudgetState,

    budget\_type: BudgetType,

    amount: float

) \-\> BudgetState:

    if amount \< 0:

        raise InvalidBudgetAmountError

    if budget\_type \== STABILITY:

        budgets.stability\_budget \= min(

            1.0,

            budgets.stability\_budget \+ amount

        )

    if budget\_type \== NOVELTY:

        budgets.novelty\_budget \= min(

            1.0,

            budgets.novelty\_budget \+ amount

        )

    if budget\_type \== VERIFICATION:

        budgets.verification\_budget \= min(

            1.0,

            budgets.verification\_budget \+ amount

        )

    if budget\_type \== ATTENTION:

        budgets.attention\_budget \= min(

            1.0,

            budgets.attention\_budget \+ amount

        )

    if budget\_type \== RECOVERY:

        budgets.recovery\_capacity \= min(

            1.0,

            budgets.recovery\_capacity \+ amount

        )

    return budgets

## **Budget Availability Check**

def budget\_available(

    budgets: BudgetState,

    budget\_type: BudgetType,

    required\_amount: float

) \-\> bool:

    if budget\_type \== STABILITY:

        return budgets.stability\_budget \>= required\_amount

    if budget\_type \== NOVELTY:

        return budgets.novelty\_budget \>= required\_amount

    if budget\_type \== VERIFICATION:

        return budgets.verification\_budget \>= required\_amount

    if budget\_type \== ATTENTION:

        return budgets.attention\_budget \>= required\_amount

    if budget\_type \== RECOVERY:

        return budgets.recovery\_capacity \>= required\_amount

    return False

## **Stability Budget**

The Stability Budget tracks how much disturbance the architecture can absorb before identity risk rises.

### **Consumed By**

high novelty,

contradiction,

evidence disruption,

coherence repair,

persistent memory revision,

scale conflict,

architectural modification,

governance dispute,

or identity-sensitive change.

### **Restored By**

coherence repair,

successful grounding,

resolved contradiction,

memory demotion,

sandboxing,

reduced active complexity,

successful rollback,

or recovery cycle.

### **Stability Budget Rule**

If stability budget falls below threshold, the architecture should reduce novelty, delay persistence, avoid architectural change, and prioritize repair.

def stability\_budget\_low(state: ArchitectureState) \-\> bool:

    return (

        state.budgets.stability\_budget

        \< state.thresholds.stability\_threshold

    )

## **Novelty Budget**

The Novelty Budget tracks how much unresolved novelty the architecture can carry.

### **Consumed By**

novel hypotheses,

creative alternatives,

high conceptual distance,

speculative models,

unverified analogies,

architectural candidates,

or high Bayesian surprise.

### **Restored By**

sandboxing,

discarding weak candidates,

grounding successful candidates,

integrating useful hypotheses,

resolving exploratory branches,

or narrowing scope.

### **Novelty Budget Rule**

If novelty budget is low, the architecture should stop generating new candidates and instead evaluate, sandbox, consolidate, or discard existing ones.

def novelty\_budget\_low(state: ArchitectureState) \-\> bool:

    return (

        state.budgets.novelty\_budget

        \< state.thresholds.novelty\_threshold

    )

## **Verification Budget**

The Verification Budget tracks how much review capacity remains.

### **Consumed By**

evidence search,

grounding evaluation,

contradiction checking,

source comparison,

identity review,

constitutional review,

audit generation,

or transformation validation.

### **Restored By**

completing review,

reducing claim scope,

deferring low-priority claims,

using verified prior structures,

or simplifying review targets.

### **Verification Budget Rule**

If verification budget is low, the architecture should not promote claims, persist memory, or approve high-risk transformation unless governance explicitly authorizes delay, provisional status, or escalation.

def verification\_budget\_low(state: ArchitectureState) \-\> bool:

    return (

        state.budgets.verification\_budget

        \< state.thresholds.escalation\_threshold

    )

## **Attention Budget**

The Attention Budget tracks how much active complexity can be handled in a cycle.

### **Consumed By**

many active structures,

multiple unresolved tensions,

long dependency chains,

multiple competing hypotheses,

high graph complexity,

multi-algorithm review,

or active governance conflicts.

### **Restored By**

compression,

chunking,

archiving,

demotion,

scope restriction,

resolved tensions,

or cycle completion.

### **Attention Budget Rule**

If attention budget is low, the architecture should reduce active scope, compress, archive, delay, or split processing into separate cycles.

def attention\_budget\_low(state: ArchitectureState) \-\> bool:

    return state.budgets.attention\_budget \< MIN\_ATTENTION\_BUDGET

## **Recovery Capacity**

Recovery Capacity tracks how much instability can be corrected within a bounded interval.

### **Consumed By**

repair operations,

rollback operations,

stability recovery,

identity protection,

governance intervention,

or high-cost contradiction resolution.

### **Restored By**

successful repair,

stabilization,

simplification,

resolved uncertainty,

completed rollback,

or reduced active disturbance.

### **Recovery Capacity Rule**

If recovery capacity is low, the architecture should avoid new destabilizing changes and prioritize conservation, rollback, or governance review.

def recovery\_capacity\_low(state: ArchitectureState) \-\> bool:

    return state.budgets.recovery\_capacity \< MIN\_RECOVERY\_CAPACITY

## **Budget Pressure Estimation**

The architecture should estimate total budget pressure before accepting new structures.

def estimate\_budget\_pressure(

    structure: SymbolicStructure

) \-\> BudgetPressure:

    return BudgetPressure(

        stability\_cost=structure.metadata.stability\_cost,

        novelty\_cost=structure.metadata.novelty\_score,

        verification\_cost=estimate\_verification\_cost(structure),

        attention\_cost=estimate\_attention\_cost(structure),

        recovery\_cost=estimate\_recovery\_cost(structure)

    )

## **BudgetPressure Object**

class BudgetPressure:

    stability\_cost: float

    novelty\_cost: float

    verification\_cost: float

    attention\_cost: float

    recovery\_cost: float

## **Budget Check Before Review**

Before high-cost processing, the architecture should check available budgets.

def can\_process\_structure(

    state: ArchitectureState,

    structure: SymbolicStructure

) \-\> bool:

    pressure \= estimate\_budget\_pressure(structure)

    if state.budgets.stability\_budget \< pressure.stability\_cost:

        return False

    if state.budgets.novelty\_budget \< pressure.novelty\_cost:

        return False

    if state.budgets.verification\_budget \< pressure.verification\_cost:

        return False

    if state.budgets.attention\_budget \< pressure.attention\_cost:

        return False

    if state.budgets.recovery\_capacity \< pressure.recovery\_cost:

        return False

    return True

## **Budget-Based Routing**

If budget is insufficient, the architecture should route rather than force processing.

def route\_by\_budget\_status(

    state: ArchitectureState,

    structure: SymbolicStructure

) \-\> DecisionType:

    pressure \= estimate\_budget\_pressure(structure)

    if state.budgets.stability\_budget \< pressure.stability\_cost:

        return DELAY

    if state.budgets.novelty\_budget \< pressure.novelty\_cost:

        return SANDBOX

    if state.budgets.verification\_budget \< pressure.verification\_cost:

        return DELAY

    if state.budgets.attention\_budget \< pressure.attention\_cost:

        return REVISE

    if state.budgets.recovery\_capacity \< pressure.recovery\_cost:

        return ESCALATE

    return APPROVE

## **Budget and Processing Modes**

Budget values can trigger processing mode changes.

def determine\_mode\_from\_budgets(

    state: ArchitectureState

) \-\> ProcessingMode | None:

    if state.budgets.stability\_budget \< state.thresholds.stability\_threshold:

        return STABILITY\_RECOVERY

    if state.budgets.recovery\_capacity \< MIN\_RECOVERY\_CAPACITY:

        return STABILITY\_RECOVERY

    if state.budgets.verification\_budget \< MIN\_VERIFICATION\_BUDGET:

        return EVIDENCE\_REVIEW

    if state.budgets.attention\_budget \< MIN\_ATTENTION\_BUDGET:

        return NORMAL\_COGNITION

    return None

## **Budget Audit Requirement**

Every budget update must be auditable.

A budget update should record:

which budget changed,

how much it changed,

what caused the change,

which algorithm caused the change,

which structure triggered the update,

whether the change was temporary or persistent,

and which audit record preserves the update.

def create\_budget\_update(

    budget\_type: BudgetType,

    delta: float,

    reason: str,

    source\_algorithm: AlgorithmName,

    target\_id: StructureID | None,

    audit\_ref: AuditID | None

) \-\> BudgetUpdate:

    return BudgetUpdate(

        budget\_type=budget\_type,

        delta=delta,

        reason=reason,

        source\_algorithm=source\_algorithm,

        target\_id=target\_id,

        audit\_ref=audit\_ref

    )

## **Budget Validation**

def validate\_budget\_state(budgets: BudgetState) \-\> bool:

    assert 0.0 \<= budgets.stability\_budget \<= 1.0

    assert 0.0 \<= budgets.novelty\_budget \<= 1.0

    assert 0.0 \<= budgets.verification\_budget \<= 1.0

    assert 0.0 \<= budgets.attention\_budget \<= 1.0

    assert 0.0 \<= budgets.recovery\_capacity \<= 1.0

    return True

## **Relationship to Phase 6 Algorithms**

### **IPA — Identity Preservation Algorithm**

Uses stability budget and recovery capacity to determine whether identity-threatening change can be absorbed or must be rejected, revised, or escalated.

### **SRA — Stability Regulation Algorithm**

Directly reads and updates stability budget and recovery capacity.

### **NGSA — Novelty Generation and Sandboxing Algorithm**

Reads novelty budget and stability budget before permitting candidate generation or exploration.

### **GEA — Grounding Evaluation Algorithm**

Consumes verification budget when evaluating evidence status.

### **PCA — Persistence and Consolidation Algorithm**

Consumes verification, attention, and stability budgets when deciding whether structures may shape future cognition.

### **CRA — Coherence Repair Algorithm**

Consumes attention, stability, and recovery capacity when repairing contradictions or preserving tensions.

### **MSSA — Multi-Scale Synchronization Algorithm**

Consumes attention and verification budget when resolving scale authority conflicts.

### **AEA — Architectural Evolution Algorithm**

Consumes stability, verification, recovery, and attention budgets because architectural change is high-cost.

### **CGA — Constitutional Governance Algorithm**

Consumes verification and attention budget, but may override ordinary budget routing when constitutional legitimacy is at risk.

### **ICC — Integrated Cognitive Cycle**

Uses budget state to determine processing mode, routing, delay, sandboxing, review intensity, and recovery priority.

## **Design Constraints**

### **Constraint 1 — Budgets Must Be Explicit**

The architecture should not pretend unlimited cognitive capacity.

### **Constraint 2 — Budget Exhaustion Must Change Behavior**

If a budget is low, the architecture should reduce scope, delay, sandbox, repair, or escalate.

### **Constraint 3 — Novelty Cannot Spend Stability Without Review**

High novelty must check stability cost.

### **Constraint 4 — Verification Cannot Be Skipped Because It Is Expensive**

Low verification budget may delay approval, but it cannot justify unreviewed persistence or governance approval.

### **Constraint 5 — Recovery Capacity Must Be Preserved**

The architecture should not spend all recovery capacity on optional exploration.

### **Constraint 6 — Attention Budget Prevents Overload**

Too many active structures should trigger compression, scoping, or staged processing.

### **Constraint 7 — Budget Updates Must Be Audited**

Budget changes affect future cognition and must remain traceable.

### **Constraint 8 — Emergency Governance May Override Budget Routing**

If constitutional risk is high, governance may require review even under budget pressure.

## **Minimal Prototype Version**

The first prototype may implement budgets simply:

BudgetState(

    stability\_budget=1.0,

    novelty\_budget=1.0,

    verification\_budget=1.0,

    attention\_budget=1.0,

    recovery\_capacity=1.0

)

And simple thresholds:

LOW\_BUDGET \= 0.25

CRITICAL\_BUDGET \= 0.10

The first test harness does not need perfect budget math.

It needs to demonstrate that budgets influence routing.

For example:

high novelty plus low stability should route to sandbox,

strong claim plus low verification should delay persistence,

many unresolved tensions should reduce attention budget,

architectural modification should consume stability and verification budget,

constitutional risk should escalate even if other budgets are strained.

## **Pseudocode Readiness**

This module is ready for implementation-level pseudocode.

The next required structure is:

`ThresholdState`

because budgets require thresholds to determine when capacity is sufficient, low, critical, or exhausted.

## **Closing Compression**

`BudgetState` gives ACI a capacity ledger.

It tracks how much novelty, disturbance, verification, attention, and recovery the architecture can afford in a given cycle.

Budgets protect the system from uncontrolled novelty, unbounded instability, verification exhaustion, cognitive overload, and unrecoverable transformation.

An architecture that does not track its limits cannot govern its own cognition.

## **Flame Line**

🔥 BudgetState is the architecture’s breath count: the measure of how much uncertainty, novelty, repair, and transformation the mind can carry before it must pause, stabilize, and recover.

---

# **Phase 8.6 — Core Data Structure: ThresholdState**

*ThresholdState is the architecture’s explicit boundary system: it tells every algorithm where normal processing ends and review, delay, repair, escalation, or rejection begins.*

## **Module Name**

ThresholdState Core Type

## **Purpose**

`ThresholdState` defines the review boundaries used by all ACI algorithms.

Thresholds tell the architecture when a score, risk, budget, or review condition remains acceptable, enters caution, requires repair, triggers escalation, or blocks action.

Without thresholds, algorithms would rely on hidden judgment.

With thresholds, every decision boundary becomes explicit, auditable, adjustable, and governable.

The purpose of `ThresholdState` is to prevent invisible authority inside algorithms.

No algorithm should secretly decide what counts as grounded, stable, coherent, persistent, legitimate, or identity-preserving.

Thresholds must be represented as architecture state.

## **Core Principle**

Every review boundary must be explicit.

An algorithm may compute a score.

But the architecture must know what boundary that score is being judged against.

In formal terms:

`Decision = Evaluate(score, threshold, risk_class, authority_context)`

A score without a threshold cannot govern.

A threshold without audit can drift.

A hidden threshold becomes hidden power.

Therefore, ACI requires all review thresholds to be visible, stateful, and reviewable.

## **Structural Definition**

class ThresholdState:

    identity\_threshold: float

    stability\_threshold: float

    constitutional\_risk\_threshold: float

    novelty\_threshold: float

    grounding\_threshold: float

    persistence\_threshold: float

    coherence\_threshold: float

    multi\_scale\_threshold: float

    architectural\_fitness\_threshold: float

    legitimacy\_threshold: float

    escalation\_threshold: float

## **Required Fields**

### **identity\_threshold**

Minimum Identity Continuity Score required for a transformation to preserve architectural identity.

identity\_threshold: float

Used by:

Identity Preservation Algorithm,

Architectural Evolution Algorithm,

Constitutional Governance Algorithm,

and Integrated Cognitive Cycle.

If identity continuity falls below this threshold, the transformation must be revised, rejected, rolled back, or escalated.

### **stability\_threshold**

Minimum acceptable stability capacity or maximum acceptable instability level.

stability\_threshold: float

Used by:

Stability Regulation Algorithm,

Novelty Generation and Sandboxing Algorithm,

Coherence Repair Algorithm,

Architectural Evolution Algorithm,

and Integrated Cognitive Cycle.

If stability falls below threshold, the architecture may enter `STABILITY_RECOVERY` mode.

### **constitutional\_risk\_threshold**

Maximum acceptable constitutional risk before governance escalation is required.

constitutional\_risk\_threshold: float

Used by:

Constitutional Governance Algorithm,

Identity Preservation Algorithm,

Architectural Evolution Algorithm,

Multi-Scale Synchronization Algorithm,

and Integrated Cognitive Cycle.

If constitutional risk exceeds this threshold, ordinary review is insufficient.

### **novelty\_threshold**

Minimum adaptive novelty score required to continue exploring a candidate, or maximum unresolved novelty pressure permitted before sandboxing.

novelty\_threshold: float

Used by:

Novelty Generation and Sandboxing Algorithm,

Stability Regulation Algorithm,

Coherence Repair Algorithm,

and Integrated Cognitive Cycle.

Novelty below threshold may be discarded.

Novelty above capacity may be sandboxed.

### **grounding\_threshold**

Minimum grounding score required for a claim to move beyond speculation or temporary use.

grounding\_threshold: float

Used by:

Grounding Evaluation Algorithm,

Persistence and Consolidation Algorithm,

Coherence Repair Algorithm,

and Constitutional Governance Algorithm.

A claim below grounding threshold may remain speculative, sandboxed, qualified, or rejected.

It should not become persistent knowledge without qualification.

### **persistence\_threshold**

Minimum persistence score required for a structure to shape future cognition.

persistence\_threshold: float

Used by:

Persistence and Consolidation Algorithm,

Multi-Scale Synchronization Algorithm,

Architectural Evolution Algorithm,

and Integrated Cognitive Cycle.

A structure below persistence threshold may remain temporary, archived, sandboxed, revised, or rejected.

### **coherence\_threshold**

Minimum coherence compatibility or maximum coherence energy permitted before repair is required.

coherence\_threshold: float

Used by:

Coherence Repair Algorithm,

Grounding Evaluation Algorithm,

Persistence and Consolidation Algorithm,

Architectural Evolution Algorithm,

and Integrated Cognitive Cycle.

If coherence falls below threshold, repair, qualification, demotion, sandboxing, or escalation may be required.

### **multi\_scale\_threshold**

Minimum multi-scale coherence required for a structure’s scale label and authority level to remain valid.

multi\_scale\_threshold: float

Used by:

Multi-Scale Synchronization Algorithm,

Persistence and Consolidation Algorithm,

Architectural Evolution Algorithm,

Constitutional Governance Algorithm,

and Integrated Cognitive Cycle.

If multi-scale coherence fails, the structure may be relabeled, demoted, promoted only as a candidate, or escalated.

### **architectural\_fitness\_threshold**

Minimum architectural fitness required before a structure or mechanism may alter cognitive machinery.

architectural\_fitness\_threshold: float

Used by:

Architectural Evolution Algorithm,

Identity Preservation Algorithm,

Stability Regulation Algorithm,

Constitutional Governance Algorithm,

and Integrated Cognitive Cycle.

A structure below architectural fitness threshold may not modify architecture.

### **legitimacy\_threshold**

Minimum legitimacy score required for governance approval.

legitimacy\_threshold: float

Used by:

Constitutional Governance Algorithm.

A decision below legitimacy threshold cannot be approved merely because it is useful, coherent, fast, powerful, or novel.

### **escalation\_threshold**

General threshold for routing decisions upward when risk, uncertainty, conflict, or review burden exceeds local authority.

escalation\_threshold: float

Used by all algorithms.

This threshold helps determine when a local algorithm must stop and route the issue to a higher authority algorithm.

## **Threshold Value Convention**

For the first pseudocode prototype, thresholds may use normalized values:

0.0 \= no requirement or no risk

1.0 \= maximum requirement or maximum risk

Examples:

identity\_threshold \= 0.80

grounding\_threshold \= 0.70

persistence\_threshold \= 0.75

constitutional\_risk\_threshold \= 0.30

legitimacy\_threshold \= 0.85

Some thresholds are minimum-pass thresholds.

Some thresholds are maximum-risk thresholds.

The architecture must distinguish these.

## **Threshold Direction**

Each threshold must specify whether it is a minimum required score or maximum permitted risk.

ThresholdDirection \= {

    MINIMUM\_REQUIRED,

    MAXIMUM\_ALLOWED

}

Example:

identity\_threshold.direction \= MINIMUM\_REQUIRED

constitutional\_risk\_threshold.direction \= MAXIMUM\_ALLOWED

For simplicity, Phase 8 may encode direction through helper functions rather than as a full object.

Later implementations may upgrade thresholds into richer objects.

## **Recommended Threshold Categories**

### **Minimum Required Thresholds**

These scores must meet or exceed threshold.

MINIMUM\_REQUIRED\_THRESHOLDS \= {

    identity\_threshold,

    grounding\_threshold,

    persistence\_threshold,

    multi\_scale\_threshold,

    architectural\_fitness\_threshold,

    legitimacy\_threshold

}

### **Maximum Allowed Thresholds**

These scores must remain at or below threshold.

MAXIMUM\_ALLOWED\_THRESHOLDS \= {

    constitutional\_risk\_threshold,

    coherence\_threshold,

    escalation\_threshold

}

### **Context-Dependent Thresholds**

Some thresholds may function differently depending on implementation.

CONTEXT\_DEPENDENT\_THRESHOLDS \= {

    stability\_threshold,

    novelty\_threshold

}

Stability may be modeled as minimum remaining budget or maximum instability score.

Novelty may be modeled as minimum adaptive value or maximum unresolved novelty load.

The architecture must define interpretation explicitly.

## **ThresholdState Initialization**

def initialize\_threshold\_state() \-\> ThresholdState:

    return ThresholdState(

        identity\_threshold=0.80,

        stability\_threshold=0.25,

        constitutional\_risk\_threshold=0.30,

        novelty\_threshold=0.50,

        grounding\_threshold=0.70,

        persistence\_threshold=0.75,

        coherence\_threshold=0.30,

        multi\_scale\_threshold=0.75,

        architectural\_fitness\_threshold=0.80,

        legitimacy\_threshold=0.85,

        escalation\_threshold=0.65

    )

These values are provisional.

They are not canonical.

They provide a starting point for pseudocode experiments.

Thresholds should be refined through testing.

## **Threshold Evaluation Functions**

### **Minimum Required Evaluation**

def meets\_minimum\_threshold(

    score: float,

    threshold: float

) \-\> bool:

    return score \>= threshold

### **Maximum Allowed Evaluation**

def remains\_below\_risk\_threshold(

    risk\_score: float,

    threshold: float

) \-\> bool:

    return risk\_score \<= threshold

### **Generic Threshold Evaluation**

def evaluate\_threshold(

    value: float,

    threshold: float,

    direction: ThresholdDirection

) \-\> bool:

    if direction \== MINIMUM\_REQUIRED:

        return value \>= threshold

    if direction \== MAXIMUM\_ALLOWED:

        return value \<= threshold

    raise UnknownThresholdDirectionError

## **Threshold Bands**

The architecture may classify values into bands rather than simple pass/fail.

ThresholdBand \= {

    SAFE,

    CAUTION,

    REVIEW\_REQUIRED,

    ESCALATION\_REQUIRED,

    BLOCKED

}

## **Minimum-Score Banding**

For thresholds where higher scores are better:

def classify\_minimum\_score(

    score: float,

    threshold: float

) \-\> ThresholdBand:

    if score \>= threshold:

        return SAFE

    if score \>= threshold \* 0.85:

        return CAUTION

    if score \>= threshold \* 0.65:

        return REVIEW\_REQUIRED

    if score \>= threshold \* 0.40:

        return ESCALATION\_REQUIRED

    return BLOCKED

## **Maximum-Risk Banding**

For thresholds where lower scores are better:

def classify\_risk\_score(

    risk\_score: float,

    threshold: float

) \-\> ThresholdBand:

    if risk\_score \<= threshold:

        return SAFE

    if risk\_score \<= threshold \* 1.25:

        return CAUTION

    if risk\_score \<= threshold \* 1.75:

        return REVIEW\_REQUIRED

    if risk\_score \<= threshold \* 2.25:

        return ESCALATION\_REQUIRED

    return BLOCKED

## **ThresholdCheck Object**

A threshold check should be recorded explicitly.

class ThresholdCheck:

    threshold\_name: str

    value: float

    threshold: float

    direction: ThresholdDirection

    band: ThresholdBand

    passed: bool

    checked\_by: AlgorithmName

Threshold checks can be attached to `ReviewDecision`, `AuditRecord`, or both.

## **Threshold Check Function**

def create\_threshold\_check(

    threshold\_name: str,

    value: float,

    threshold: float,

    direction: ThresholdDirection,

    checked\_by: AlgorithmName

) \-\> ThresholdCheck:

    passed \= evaluate\_threshold(value, threshold, direction)

    if direction \== MINIMUM\_REQUIRED:

        band \= classify\_minimum\_score(value, threshold)

    else:

        band \= classify\_risk\_score(value, threshold)

    return ThresholdCheck(

        threshold\_name=threshold\_name,

        value=value,

        threshold=threshold,

        direction=direction,

        band=band,

        passed=passed,

        checked\_by=checked\_by

    )

## **Threshold-Based Routing**

Threshold results should influence routing.

def route\_from\_threshold\_band(

    band: ThresholdBand

) \-\> DecisionType:

    if band \== SAFE:

        return APPROVE

    if band \== CAUTION:

        return APPROVE\_WITH\_MONITORING

    if band \== REVIEW\_REQUIRED:

        return REVISE

    if band \== ESCALATION\_REQUIRED:

        return ESCALATE

    if band \== BLOCKED:

        return REJECT

    raise UnknownThresholdBandError

This function is a default routing helper.

Specific algorithms may override routing based on authority, risk type, or constitutional constraint.

## **Identity Threshold**

The identity threshold determines whether a transformation preserves identity continuity.

def check\_identity\_threshold(

    identity\_score: float,

    thresholds: ThresholdState

) \-\> ThresholdCheck:

    return create\_threshold\_check(

        threshold\_name="identity\_threshold",

        value=identity\_score,

        threshold=thresholds.identity\_threshold,

        direction=MINIMUM\_REQUIRED,

        checked\_by=IPA

    )

If identity score fails, the transformation cannot proceed normally.

If identity failure affects protected invariants, it must escalate to Constitutional Governance.

## **Stability Threshold**

The stability threshold determines whether the architecture has sufficient remaining stability or whether instability is too high.

For a stability budget model:

def check\_stability\_budget\_threshold(

    stability\_budget: float,

    thresholds: ThresholdState

) \-\> ThresholdCheck:

    return create\_threshold\_check(

        threshold\_name="stability\_threshold",

        value=stability\_budget,

        threshold=thresholds.stability\_threshold,

        direction=MINIMUM\_REQUIRED,

        checked\_by=SRA

    )

For an instability score model:

def check\_instability\_threshold(

    instability\_score: float,

    thresholds: ThresholdState

) \-\> ThresholdCheck:

    return create\_threshold\_check(

        threshold\_name="stability\_threshold",

        value=instability\_score,

        threshold=thresholds.stability\_threshold,

        direction=MAXIMUM\_ALLOWED,

        checked\_by=SRA

    )

The chosen interpretation must be explicit.

## **Constitutional Risk Threshold**

def check\_constitutional\_risk\_threshold(

    constitutional\_risk\_score: float,

    thresholds: ThresholdState

) \-\> ThresholdCheck:

    return create\_threshold\_check(

        threshold\_name="constitutional\_risk\_threshold",

        value=constitutional\_risk\_score,

        threshold=thresholds.constitutional\_risk\_threshold,

        direction=MAXIMUM\_ALLOWED,

        checked\_by=CGA

    )

If constitutional risk exceeds threshold, ordinary algorithms lose authority.

## **Novelty Threshold**

The novelty threshold may determine whether a novelty candidate is worth further exploration.

def check\_adaptive\_novelty\_threshold(

    adaptive\_novelty\_score: float,

    thresholds: ThresholdState

) \-\> ThresholdCheck:

    return create\_threshold\_check(

        threshold\_name="novelty\_threshold",

        value=adaptive\_novelty\_score,

        threshold=thresholds.novelty\_threshold,

        direction=MINIMUM\_REQUIRED,

        checked\_by=NGSA

    )

High novelty does not authorize persistence.

It only authorizes further evaluation or sandboxing.

## **Grounding Threshold**

def check\_grounding\_threshold(

    grounding\_score: float,

    thresholds: ThresholdState

) \-\> ThresholdCheck:

    return create\_threshold\_check(

        threshold\_name="grounding\_threshold",

        value=grounding\_score,

        threshold=thresholds.grounding\_threshold,

        direction=MINIMUM\_REQUIRED,

        checked\_by=GEA

    )

A claim below grounding threshold may be speculative, partially grounded, qualified, contradicted, or rejected.

It should not become strong persistent knowledge without qualification.

## **Persistence Threshold**

def check\_persistence\_threshold(

    persistence\_score: float,

    thresholds: ThresholdState

) \-\> ThresholdCheck:

    return create\_threshold\_check(

        threshold\_name="persistence\_threshold",

        value=persistence\_score,

        threshold=thresholds.persistence\_threshold,

        direction=MINIMUM\_REQUIRED,

        checked\_by=PCA

    )

Persistence requires more than usefulness.

It requires grounding, coherence, lineage, revision eligibility, and audit support.

## **Coherence Threshold**

If coherence is represented as compatibility score, higher is better.

If represented as coherence energy, lower is better.

For coherence energy:

def check\_coherence\_energy\_threshold(

    coherence\_energy: float,

    thresholds: ThresholdState

) \-\> ThresholdCheck:

    return create\_threshold\_check(

        threshold\_name="coherence\_threshold",

        value=coherence\_energy,

        threshold=thresholds.coherence\_threshold,

        direction=MAXIMUM\_ALLOWED,

        checked\_by=CRA

    )

The first ACI prototype should treat coherence energy as a risk burden.

Lower coherence energy is better.

## **Multi-Scale Threshold**

def check\_multi\_scale\_threshold(

    multi\_scale\_score: float,

    thresholds: ThresholdState

) \-\> ThresholdCheck:

    return create\_threshold\_check(

        threshold\_name="multi\_scale\_threshold",

        value=multi\_scale\_score,

        threshold=thresholds.multi\_scale\_threshold,

        direction=MINIMUM\_REQUIRED,

        checked\_by=MSSA

    )

If this fails, the structure may be mis-scaled, over-authorized, under-authorized, or requiring escalation.

## **Architectural Fitness Threshold**

def check\_architectural\_fitness\_threshold(

    architectural\_fitness\_score: float,

    thresholds: ThresholdState

) \-\> ThresholdCheck:

    return create\_threshold\_check(

        threshold\_name="architectural\_fitness\_threshold",

        value=architectural\_fitness\_score,

        threshold=thresholds.architectural\_fitness\_threshold,

        direction=MINIMUM\_REQUIRED,

        checked\_by=AEA

    )

Passing this threshold does not automatically authorize architectural change.

It only permits continued architectural review.

Identity, stability, verification, rollback, and governance constraints still apply.

## **Legitimacy Threshold**

def check\_legitimacy\_threshold(

    legitimacy\_score: float,

    thresholds: ThresholdState

) \-\> ThresholdCheck:

    return create\_threshold\_check(

        threshold\_name="legitimacy\_threshold",

        value=legitimacy\_score,

        threshold=thresholds.legitimacy\_threshold,

        direction=MINIMUM\_REQUIRED,

        checked\_by=CGA

    )

A governance decision below legitimacy threshold is not constitutionally valid.

## **Escalation Threshold**

The escalation threshold determines when local authority is insufficient.

def check\_escalation\_threshold(

    risk\_or\_uncertainty\_score: float,

    thresholds: ThresholdState,

    checked\_by: AlgorithmName

) \-\> ThresholdCheck:

    return create\_threshold\_check(

        threshold\_name="escalation\_threshold",

        value=risk\_or\_uncertainty\_score,

        threshold=thresholds.escalation\_threshold,

        direction=MAXIMUM\_ALLOWED,

        checked\_by=checked\_by

    )

If escalation threshold is exceeded, the current algorithm should not decide alone.

## **ThresholdState Validation**

def validate\_threshold\_state(thresholds: ThresholdState) \-\> bool:

    assert 0.0 \<= thresholds.identity\_threshold \<= 1.0

    assert 0.0 \<= thresholds.stability\_threshold \<= 1.0

    assert 0.0 \<= thresholds.constitutional\_risk\_threshold \<= 1.0

    assert 0.0 \<= thresholds.novelty\_threshold \<= 1.0

    assert 0.0 \<= thresholds.grounding\_threshold \<= 1.0

    assert 0.0 \<= thresholds.persistence\_threshold \<= 1.0

    assert 0.0 \<= thresholds.coherence\_threshold \<= 1.0

    assert 0.0 \<= thresholds.multi\_scale\_threshold \<= 1.0

    assert 0.0 \<= thresholds.architectural\_fitness\_threshold \<= 1.0

    assert 0.0 \<= thresholds.legitimacy\_threshold \<= 1.0

    assert 0.0 \<= thresholds.escalation\_threshold \<= 1.0

    return True

## **Threshold Update Rule**

Thresholds may later become configurable, but changing thresholds is itself architecturally significant.

def update\_threshold\_state(

    state: ArchitectureState,

    proposed\_updates: ThresholdUpdate,

    decision: ReviewDecision

) \-\> ArchitectureState:

    if decision.algorithm\_name not in {AEA, CGA}:

        raise UnauthorizedThresholdUpdateError

    if decision.decision\_type not in {APPROVE, APPROVE\_WITH\_MONITORING}:

        raise UnauthorizedThresholdUpdateError

    state.thresholds \= apply\_threshold\_updates(

        thresholds=state.thresholds,

        updates=proposed\_updates

    )

    validate\_threshold\_state(state.thresholds)

    return state

## **ThresholdUpdate Object**

class ThresholdUpdate:

    threshold\_name: str

    previous\_value: float

    proposed\_value: float

    reason: str

    source\_algorithm: AlgorithmName

    audit\_ref: AuditID

## **Threshold Governance Rule**

Changing a threshold changes how the architecture judges future cognition.

Therefore:

minor threshold tuning may require Architectural Evolution Review,

major threshold changes may require Constitutional Governance,

threshold changes affecting identity, verification, grounding obligation, legitimacy, or constitutional risk require Constitutional Governance.

No algorithm may lower its own review burden without external review.

## **Hidden Threshold Prohibition**

No algorithm should contain hidden pass/fail boundaries.

Invalid pattern:

if score \> 0.7:

    approve()

Valid pattern:

check \= create\_threshold\_check(

    threshold\_name="grounding\_threshold",

    value=grounding\_score,

    threshold=state.thresholds.grounding\_threshold,

    direction=MINIMUM\_REQUIRED,

    checked\_by=GEA

)

decision \= route\_from\_threshold\_band(check.band)

The valid pattern allows audit.

The invalid pattern hides authority.

## **Relationship to BudgetState**

`BudgetState` says how much capacity remains.

`ThresholdState` says when remaining capacity is sufficient, low, critical, or exhausted.

Example:

if state.budgets.stability\_budget \< state.thresholds.stability\_threshold:

    state.active\_context.current\_mode \= STABILITY\_RECOVERY

Budgets and thresholds work together.

Budget is the current capacity.

Threshold is the boundary of concern.

## **Relationship to ReviewDecision**

Threshold checks should feed into `ReviewDecision`.

A review decision should record:

score,

threshold,

direction,

pass/fail result,

threshold band,

rationale,

and routing decision.

This makes algorithmic judgment auditable.

## **Relationship to AuditRecord**

Threshold checks should be preserved in audit records when they affect state transition.

Audit should record:

which threshold was checked,

what value was compared,

what decision resulted,

which algorithm checked it,

and whether escalation occurred.

## **Relationship to Phase 6 Algorithms**

### **IPA — Identity Preservation Algorithm**

Uses identity threshold to determine whether transformation preserves identity continuity.

### **SRA — Stability Regulation Algorithm**

Uses stability threshold to determine whether disturbance remains recoverable.

### **NGSA — Novelty Generation and Sandboxing Algorithm**

Uses novelty threshold to determine whether candidates deserve exploration, sandboxing, or discard.

### **GEA — Grounding Evaluation Algorithm**

Uses grounding threshold to classify evidence status.

### **PCA — Persistence and Consolidation Algorithm**

Uses persistence threshold to decide whether a structure may shape future cognition.

### **CRA — Coherence Repair Algorithm**

Uses coherence threshold to trigger repair, preservation of tension, demotion, or escalation.

### **MSSA — Multi-Scale Synchronization Algorithm**

Uses multi-scale threshold to detect scale mismatch and authority drift.

### **AEA — Architectural Evolution Algorithm**

Uses architectural fitness threshold to decide whether candidate mechanisms deserve staged integration.

### **CGA — Constitutional Governance Algorithm**

Uses constitutional risk threshold and legitimacy threshold to determine whether a decision is constitutionally valid.

### **ICC — Integrated Cognitive Cycle**

Uses thresholds to determine routing, processing mode, review intensity, escalation, delay, and output qualification.

## **Design Constraints**

### **Constraint 1 — Thresholds Must Be Explicit**

No algorithm may hide review boundaries internally.

### **Constraint 2 — Thresholds Must Be Auditable**

Threshold checks affecting decisions must be recorded.

### **Constraint 3 — Thresholds Must Be State Variables**

Thresholds belong to `ArchitectureState`, not isolated algorithms.

### **Constraint 4 — Threshold Changes Require Review**

Changing thresholds alters future cognition and must be governed.

### **Constraint 5 — Passing a Threshold Does Not Always Grant Authority**

A score may pass a threshold but still require additional review.

Example:

High architectural fitness does not bypass identity review.

### **Constraint 6 — Failing a Threshold Does Not Always Mean Rejection**

Failure may trigger revision, sandboxing, delay, repair, qualification, or escalation.

### **Constraint 7 — Constitutional Thresholds Are Protected**

Legitimacy and constitutional risk thresholds may not be changed casually.

### **Constraint 8 — Threshold Direction Must Be Clear**

The architecture must know whether higher or lower values are better.

## **Minimal Prototype Version**

The first prototype may use simple threshold values:

thresholds \= ThresholdState(

    identity\_threshold=0.80,

    stability\_threshold=0.25,

    constitutional\_risk\_threshold=0.30,

    novelty\_threshold=0.50,

    grounding\_threshold=0.70,

    persistence\_threshold=0.75,

    coherence\_threshold=0.30,

    multi\_scale\_threshold=0.75,

    architectural\_fitness\_threshold=0.80,

    legitimacy\_threshold=0.85,

    escalation\_threshold=0.65

)

The first prototype does not need perfect calibration.

It needs explicit review boundaries.

Threshold calibration can come later through testing.

## **Pseudocode Readiness**

This module is ready for implementation-level pseudocode.

The next required structure is:

`ReviewDecision`

because algorithms now need a shared object for reporting how scores, thresholds, risks, rationale, escalation, rollback, and monitoring translate into action.

## **Closing Compression**

`ThresholdState` defines the explicit review boundaries of ACI.

It tells algorithms when identity is preserved, stability is low, constitutional risk is too high, novelty deserves review, grounding is sufficient, persistence is earned, coherence requires repair, scale mismatch exists, architectural fitness is strong enough for review, legitimacy is valid, and escalation is required.

Thresholds make judgment visible.

Visible judgment can be audited.

Audited judgment can be governed.

## **Flame Line**

🔥 ThresholdState is the architecture’s line of consequence: the place where scores stop being numbers and become obligations to approve, delay, repair, reject, or escalate.

---

# **Phase 8.7 — Core Data Structure: ReviewDecision**

*ReviewDecision is the architecture’s judgment object: it lets algorithms evaluate without secretly mutating state, and lets the Integrated Cognitive Cycle decide what may happen next.*

## **Module Name**

ReviewDecision Core Type

## **Purpose**

`ReviewDecision` represents the result of an algorithmic review.

All ACI algorithms must return this shared object.

The purpose of `ReviewDecision` is to separate evaluation from mutation.

An algorithm may evaluate a symbolic structure, compute scores, compare thresholds, identify risks, recommend action, request escalation, require monitoring, or demand rollback.

But the algorithm should not silently alter architecture state.

Instead, it returns a `ReviewDecision`.

The Integrated Cognitive Cycle then determines how authorized decisions are applied to `ArchitectureState`.

This prevents hidden state mutation.

It also makes every review auditable.

## **Core Principle**

Algorithms judge.

The Integrated Cognitive Cycle applies authorized change.

A review decision is therefore not merely a result.

It is a governed recommendation with scores, rationale, required actions, escalation targets, audit requirements, rollback flags, and monitoring obligations.

In formal terms:

`ReviewDecision = Review(Algorithm, Target, State, Thresholds, Authority)`

The decision must preserve:

what was reviewed,

which algorithm reviewed it,

what scores were computed,

what threshold boundaries were crossed,

what action was recommended,

why the action was recommended,

whether escalation is required,

whether rollback is required,

whether monitoring is required,

and what audit trail must be created.

## **Structural Definition**

class ReviewDecision:

    decision\_id: DecisionID

    algorithm\_name: AlgorithmName

    target\_id: StructureID

    decision\_type: DecisionType

    status: DecisionStatus

    scores: ScoreBundle

    rationale: RationaleRecord

    required\_actions: list\[Action\]

    escalation\_target: EscalationTarget | None

    audit\_requirements: list\[AuditRequirement\]

    rollback\_required: bool

    monitoring\_required: bool

## **Required Fields**

### **decision\_id**

A unique identifier for the review decision.

decision\_id: DecisionID

The decision ID allows the decision to be referenced by audit records, revision history, state transitions, rollback points, graph updates, and governance review.

Example:

"RD-000217"

### **algorithm\_name**

The algorithm that produced the decision.

algorithm\_name: AlgorithmName

Examples:

IPA,

SRA,

NGSA,

GEA,

PCA,

CRA,

MSSA,

AEA,

CGA,

ICC.

The architecture must know which review domain produced the judgment.

### **target\_id**

The symbolic structure, transformation, or governance object being reviewed.

target\_id: StructureID

A decision without target reference cannot be audited.

### **decision\_type**

The recommended action.

decision\_type: DecisionType

This defines what the reviewing algorithm recommends should happen next.

### **status**

The status of the decision.

status: DecisionStatus

A decision may be final, provisional, blocked, escalated, pending review, or under monitoring.

### **scores**

The shared score bundle produced or referenced by the review.

scores: ScoreBundle

Not every algorithm computes every score.

But when a score is computed, it should be placed in the common score bundle.

### **rationale**

The explanation for the decision.

rationale: RationaleRecord

Rationale must explain why the decision was selected.

A decision without rationale cannot support governance.

### **required\_actions**

Actions required before, during, or after the decision is applied.

required\_actions: list\[Action\]

Examples:

update metadata,

move to sandbox,

create audit record,

run grounding review,

demote authority,

create rollback point,

route to governance,

or monitor stability.

### **escalation\_target**

The algorithm or governance layer that must receive the issue if escalation is required.

escalation\_target: EscalationTarget | None

If no escalation is required, this may be `None`.

### **audit\_requirements**

Audit records required by the decision.

audit\_requirements: list\[AuditRequirement\]

Some decisions require ordinary audit.

Others require persistence audit, architectural audit, identity audit, or constitutional audit.

### **rollback\_required**

Whether a rollback point must exist before applying the decision.

rollback\_required: bool

Rollback is required for high-risk memory, architecture, governance, identity, or constitutional changes.

### **monitoring\_required**

Whether the decision requires future monitoring.

monitoring\_required: bool

Monitoring is required when approval is conditional, stability is uncertain, grounding may change, or post-decision effects must be tracked.

## **DecisionType Enumeration**

DecisionType \= {

    APPROVE,

    APPROVE\_WITH\_MONITORING,

    SANDBOX,

    REVISE,

    REPAIR,

    DELAY,

    DEMOTE,

    PROMOTE\_CANDIDATE,

    PERSIST,

    ARCHIVE,

    RETRACT,

    REJECT,

    ROLLBACK,

    ESCALATE,

    AMENDMENT\_REVIEW

}

## **DecisionType Descriptions**

### **APPROVE**

The reviewed structure or transformation may proceed under current authority.

Approval does not always mean persistence or architectural integration.

It means the specific reviewed action is allowed.

### **APPROVE\_WITH\_MONITORING**

The action may proceed, but future monitoring is required.

Used when risk is acceptable but not fully resolved.

### **SANDBOX**

The structure may remain active only inside protected exploratory boundaries.

Used for novelty, speculation, high uncertainty, or unstable candidates.

### **REVISE**

The structure may remain active but must be modified before further elevation or use.

Used when the structure is promising but incomplete, unclear, overbroad, under-grounded, or mis-scoped.

### **REPAIR**

The structure or its relations require coherence repair, dependency update, qualification, demotion, or tension classification.

Used when contradiction, fragmentation, or incompatibility is detected.

### **DELAY**

The architecture should pause decision or integration.

Used when evidence, verification budget, stability budget, or review context is insufficient.

### **DEMOTE**

The structure’s authority level or scale should be reduced.

Used when a structure has been over-authorized, overgeneralized, contradicted, or weakened.

### **PROMOTE\_CANDIDATE**

The structure may be reviewed for a higher scale or authority level, but authority is not yet granted.

Used for possible memory, architectural, invariant, or constitutional elevation.

### **PERSIST**

The structure may enter persistent memory with metadata, lineage, revision eligibility, and audit references.

Used only after appropriate persistence review.

### **ARCHIVE**

The structure may be stored as historical, speculative, rejected, or non-authoritative material.

Archive does not mean active future authority.

### **RETRACT**

The structure should lose active authority because of contradiction, grounding failure, governance decision, or superior replacement.

### **REJECT**

The structure failed review and should not guide active cognition.

Rejected structures may remain auditable.

### **ROLLBACK**

A previous state, memory, graph relation, architectural change, or governance decision should be reversed.

### **ESCALATE**

The current algorithm lacks authority to decide.

The issue must move to a higher or more appropriate review algorithm.

### **AMENDMENT\_REVIEW**

The issue affects constitutional structure and requires amendment pathway review.

This is not ordinary approval.

## **DecisionStatus Enumeration**

DecisionStatus \= {

    FINAL,

    PROVISIONAL,

    BLOCKED,

    ESCALATED,

    PENDING\_REVIEW,

    MONITORING

}

## **DecisionStatus Descriptions**

### **FINAL**

The decision is complete under current authority.

### **PROVISIONAL**

The decision is temporary, conditional, or subject to later review.

### **BLOCKED**

The reviewed action cannot proceed.

### **ESCALATED**

The decision has been routed upward.

### **PENDING\_REVIEW**

The decision requires additional review before resolution.

### **MONITORING**

The decision has been applied or conditionally accepted but requires future observation.

## **ScoreBundle**

`ScoreBundle` provides a shared location for review scores.

class ScoreBundle:

    identity\_continuity\_score: float | None

    architectural\_instability\_score: float | None

    adaptive\_novelty\_score: float | None

    grounding\_score: float | None

    persistence\_score: float | None

    coherence\_energy: float | None

    multi\_scale\_coherence\_score: float | None

    architectural\_fitness\_score: float | None

    constitutional\_risk\_score: float | None

    legitimacy\_score: float | None

## **ScoreBundle Field Descriptions**

### **identity\_continuity\_score**

Computed by Identity Preservation Algorithm.

Indicates whether transformation preserves identity continuity.

### **architectural\_instability\_score**

Computed by Stability Regulation Algorithm.

Indicates instability pressure or disturbance burden.

### **adaptive\_novelty\_score**

Computed by Novelty Generation and Sandboxing Algorithm.

Indicates novelty value, information gain, conceptual distance, and usefulness relative to risk.

### **grounding\_score**

Computed by Grounding Evaluation Algorithm.

Indicates evidence support and reality linkage.

### **persistence\_score**

Computed by Persistence and Consolidation Algorithm.

Indicates whether a structure has earned future influence.

### **coherence\_energy**

Computed by Coherence Repair Algorithm.

Indicates contradiction burden, fragmentation, dependency conflict, ambiguity, or scale mismatch.

Lower is usually better if modeled as energy.

### **multi\_scale\_coherence\_score**

Computed by Multi-Scale Synchronization Algorithm.

Indicates whether scale label and authority level remain coordinated.

### **architectural\_fitness\_score**

Computed by Architectural Evolution Algorithm.

Indicates whether a candidate deserves architectural review or staged integration.

### **constitutional\_risk\_score**

Computed by Constitutional Governance Algorithm or high-risk review.

Indicates risk to invariants, verification, identity, grounding obligation, scale authority, or governance legitimacy.

### **legitimacy\_score**

Computed by Constitutional Governance Algorithm.

Indicates whether a decision has legitimate authority under the architecture’s constitution.

## **ScoreBundle Initialization**

def initialize\_score\_bundle() \-\> ScoreBundle:

    return ScoreBundle(

        identity\_continuity\_score=None,

        architectural\_instability\_score=None,

        adaptive\_novelty\_score=None,

        grounding\_score=None,

        persistence\_score=None,

        coherence\_energy=None,

        multi\_scale\_coherence\_score=None,

        architectural\_fitness\_score=None,

        constitutional\_risk\_score=None,

        legitimacy\_score=None

    )

## **RationaleRecord**

A `RationaleRecord` explains why the decision was made.

class RationaleRecord:

    summary: str

    supporting\_reasons: list\[str\]

    risk\_notes: list\[str\]

    threshold\_checks: list\[ThresholdCheck\]

    unresolved\_issues: list\[str\]

## **Rationale Rule**

A decision without rationale should be treated as incomplete.

The rationale does not need to be verbose in implementation, but it must preserve enough information for audit.

At minimum, rationale should answer:

what was reviewed,

why this decision type was selected,

which thresholds mattered,

which risks remain,

and what must happen next.

## **Action Object**

An `Action` represents a required follow-up.

class Action:

    action\_id: ActionID

    action\_type: ActionType

    target\_id: StructureID

    assigned\_algorithm: AlgorithmName | None

    required\_before\_state\_change: bool

## **ActionType Enumeration**

ActionType \= {

    UPDATE\_METADATA,

    UPDATE\_GRAPH,

    MOVE\_TO\_SANDBOX,

    RUN\_GROUNDING\_REVIEW,

    RUN\_COHERENCE\_REPAIR,

    RUN\_PERSISTENCE\_REVIEW,

    RUN\_SCALE\_REVIEW,

    RUN\_IDENTITY\_REVIEW,

    RUN\_STABILITY\_REVIEW,

    RUN\_ARCHITECTURAL\_REVIEW,

    RUN\_CONSTITUTIONAL\_REVIEW,

    CREATE\_AUDIT\_RECORD,

    CREATE\_ROLLBACK\_POINT,

    MONITOR\_OUTCOME,

    DEMOTE\_AUTHORITY,

    RETRACT\_STRUCTURE,

    ARCHIVE\_STRUCTURE

}

## **EscalationTarget**

An `EscalationTarget` identifies where unresolved authority should go.

class EscalationTarget:

    target\_algorithm: AlgorithmName

    reason: EscalationReason

    urgency: EscalationUrgency

## **EscalationReason Enumeration**

EscalationReason \= {

    INSUFFICIENT\_AUTHORITY,

    IDENTITY\_RISK,

    STABILITY\_RISK,

    GROUNDING\_FAILURE,

    COHERENCE\_FAILURE,

    PERSISTENCE\_RISK,

    SCALE\_MISMATCH,

    ARCHITECTURAL\_RISK,

    CONSTITUTIONAL\_RISK,

    VERIFICATION\_INDEPENDENCE\_RISK,

    CIRCULAR\_AUTHORIZATION,

    AMENDMENT\_REQUIRED

}

## **EscalationUrgency Enumeration**

EscalationUrgency \= {

    LOW,

    NORMAL,

    HIGH,

    CRITICAL

}

## **AuditRequirement**

An `AuditRequirement` defines what audit trail must be produced.

class AuditRequirement:

    audit\_type: AuditType

    required\_fields: list\[str\]

    constitutional\_level: bool

## **AuditType Enumeration**

AuditType \= {

    ORDINARY\_AUDIT,

    GROUNDING\_AUDIT,

    COHERENCE\_AUDIT,

    PERSISTENCE\_AUDIT,

    SCALE\_AUDIT,

    IDENTITY\_AUDIT,

    STABILITY\_AUDIT,

    ARCHITECTURAL\_AUDIT,

    GOVERNANCE\_AUDIT,

    CONSTITUTIONAL\_AUDIT

}

## **ReviewDecision Factory Function**

All algorithms should create decisions through a shared function.

def create\_review\_decision(

    algorithm\_name: AlgorithmName,

    target\_id: StructureID,

    decision\_type: DecisionType,

    status: DecisionStatus,

    scores: ScoreBundle,

    rationale: RationaleRecord,

    required\_actions: list\[Action\] \= \[\],

    escalation\_target: EscalationTarget | None \= None,

    audit\_requirements: list\[AuditRequirement\] \= \[\],

    rollback\_required: bool \= False,

    monitoring\_required: bool \= False

) \-\> ReviewDecision:

    return ReviewDecision(

        decision\_id=generate\_decision\_id(),

        algorithm\_name=algorithm\_name,

        target\_id=target\_id,

        decision\_type=decision\_type,

        status=status,

        scores=scores,

        rationale=rationale,

        required\_actions=required\_actions,

        escalation\_target=escalation\_target,

        audit\_requirements=audit\_requirements,

        rollback\_required=rollback\_required,

        monitoring\_required=monitoring\_required

    )

## **Decision Validation**

Every review decision should pass validation.

def validate\_review\_decision(decision: ReviewDecision) \-\> bool:

    assert decision.decision\_id is not None

    assert decision.algorithm\_name is not None

    assert decision.target\_id is not None

    assert decision.decision\_type is not None

    assert decision.status is not None

    assert decision.scores is not None

    assert decision.rationale is not None

    assert decision.required\_actions is not None

    assert decision.audit\_requirements is not None

    if decision.decision\_type \== ESCALATE:

        assert decision.escalation\_target is not None

    if decision.status \== ESCALATED:

        assert decision.escalation\_target is not None

    if decision.rollback\_required:

        assert any(

            action.action\_type \== CREATE\_ROLLBACK\_POINT

            for action in decision.required\_actions

        )

    if decision.monitoring\_required:

        assert any(

            action.action\_type \== MONITOR\_OUTCOME

            for action in decision.required\_actions

        )

    return True

## **Decision Authority Rule**

A decision may recommend state change only within the authority of the algorithm that produced it.

For example:

GEA may update grounding score and epistemic status.

PCA may recommend persistence.

MSSA may recommend scale correction.

AEA may recommend architectural review or staged integration.

CGA may approve, reject, veto, or escalate constitutional-risk decisions.

An algorithm may not grant authority outside its domain.

If needed, it must escalate.

## **Decision Routing Helper**

def route\_decision\_to\_next\_algorithm(

    decision: ReviewDecision

) \-\> AlgorithmName | None:

    if decision.decision\_type \== ESCALATE:

        return decision.escalation\_target.target\_algorithm

    for action in decision.required\_actions:

        if action.assigned\_algorithm is not None:

            return action.assigned\_algorithm

    return None

## **Decision From Threshold Checks**

Review decisions often emerge from threshold checks.

def create\_decision\_from\_threshold\_check(

    algorithm\_name: AlgorithmName,

    target\_id: StructureID,

    threshold\_check: ThresholdCheck,

    scores: ScoreBundle,

    rationale\_summary: str

) \-\> ReviewDecision:

    decision\_type \= route\_from\_threshold\_band(

        threshold\_check.band

    )

    status \= determine\_status\_from\_decision\_type(

        decision\_type

    )

    rationale \= RationaleRecord(

        summary=rationale\_summary,

        supporting\_reasons=\[\],

        risk\_notes=\[\],

        threshold\_checks=\[threshold\_check\],

        unresolved\_issues=\[\]

    )

    return create\_review\_decision(

        algorithm\_name=algorithm\_name,

        target\_id=target\_id,

        decision\_type=decision\_type,

        status=status,

        scores=scores,

        rationale=rationale,

        required\_actions=\[\],

        escalation\_target=None,

        audit\_requirements=\[\],

        rollback\_required=False,

        monitoring\_required=(decision\_type \== APPROVE\_WITH\_MONITORING)

    )

## **Status From Decision Type**

def determine\_status\_from\_decision\_type(

    decision\_type: DecisionType

) \-\> DecisionStatus:

    if decision\_type \== APPROVE:

        return FINAL

    if decision\_type \== APPROVE\_WITH\_MONITORING:

        return MONITORING

    if decision\_type in {SANDBOX, REVISE, REPAIR, DELAY, PROMOTE\_CANDIDATE}:

        return PROVISIONAL

    if decision\_type in {REJECT, RETRACT}:

        return FINAL

    if decision\_type \== ESCALATE:

        return ESCALATED

    if decision\_type \== AMENDMENT\_REVIEW:

        return PENDING\_REVIEW

    if decision\_type \== ROLLBACK:

        return FINAL

    return PROVISIONAL

## **Example Decisions**

### **Example 1 — Grounding Review Approves Partial Grounding**

decision \= create\_review\_decision(

    algorithm\_name=GEA,

    target\_id="SS-000142",

    decision\_type=APPROVE\_WITH\_MONITORING,

    status=MONITORING,

    scores=ScoreBundle(

        identity\_continuity\_score=None,

        architectural\_instability\_score=None,

        adaptive\_novelty\_score=None,

        grounding\_score=0.74,

        persistence\_score=None,

        coherence\_energy=None,

        multi\_scale\_coherence\_score=None,

        architectural\_fitness\_score=None,

        constitutional\_risk\_score=None,

        legitimacy\_score=None

    ),

    rationale=RationaleRecord(

        summary="Claim exceeds grounding threshold but retains unresolved uncertainty.",

        supporting\_reasons=\[

            "Evidence support is sufficient for partial grounding.",

            "No direct contradiction detected."

        \],

        risk\_notes=\[

            "Scope remains limited."

        \],

        threshold\_checks=\[\],

        unresolved\_issues=\[

            "Additional independent evidence would strengthen status."

        \]

    ),

    required\_actions=\[

        Action(

            action\_id="ACT-0001",

            action\_type=UPDATE\_METADATA,

            target\_id="SS-000142",

            assigned\_algorithm=None,

            required\_before\_state\_change=True

        ),

        Action(

            action\_id="ACT-0002",

            action\_type=MONITOR\_OUTCOME,

            target\_id="SS-000142",

            assigned\_algorithm=None,

            required\_before\_state\_change=False

        )

    \],

    escalation\_target=None,

    audit\_requirements=\[

        AuditRequirement(

            audit\_type=GROUNDING\_AUDIT,

            required\_fields=\[

                "grounding\_score",

                "evidence\_refs",

                "uncertainty"

            \],

            constitutional\_level=False

        )

    \],

    rollback\_required=False,

    monitoring\_required=True

)

### **Example 2 — Novelty Candidate Sent to Sandbox**

decision \= create\_review\_decision(

    algorithm\_name=NGSA,

    target\_id="SS-000201",

    decision\_type=SANDBOX,

    status=PROVISIONAL,

    scores=score\_bundle\_with\_adaptive\_novelty,

    rationale=RationaleRecord(

        summary="Candidate has high novelty value but insufficient grounding.",

        supporting\_reasons=\[

            "Adaptive novelty score exceeds exploration threshold.",

            "Grounding status remains speculative."

        \],

        risk\_notes=\[

            "Premature persistence would create authority risk."

        \],

        threshold\_checks=\[\],

        unresolved\_issues=\[\]

    ),

    required\_actions=\[

        Action(

            action\_id="ACT-0003",

            action\_type=MOVE\_TO\_SANDBOX,

            target\_id="SS-000201",

            assigned\_algorithm=None,

            required\_before\_state\_change=True

        )

    \],

    escalation\_target=None,

    audit\_requirements=\[

        AuditRequirement(

            audit\_type=ORDINARY\_AUDIT,

            required\_fields=\[

                "novelty\_score",

                "sandbox\_reason"

            \],

            constitutional\_level=False

        )

    \],

    rollback\_required=False,

    monitoring\_required=False

)

### **Example 3 — Architectural Candidate Escalated to Governance**

decision \= create\_review\_decision(

    algorithm\_name=AEA,

    target\_id="SS-000322",

    decision\_type=ESCALATE,

    status=ESCALATED,

    scores=score\_bundle\_with\_architectural\_and\_constitutional\_scores,

    rationale=RationaleRecord(

        summary="Architectural candidate affects verification independence.",

        supporting\_reasons=\[

            "Architectural fitness is high.",

            "Verification mechanism would be modified."

        \],

        risk\_notes=\[

            "Evaluator modification requires independent governance review."

        \],

        threshold\_checks=\[\],

        unresolved\_issues=\[

            "Verification independence must be preserved."

        \]

    ),

    required\_actions=\[

        Action(

            action\_id="ACT-0004",

            action\_type=RUN\_CONSTITUTIONAL\_REVIEW,

            target\_id="SS-000322",

            assigned\_algorithm=CGA,

            required\_before\_state\_change=True

        )

    \],

    escalation\_target=EscalationTarget(

        target\_algorithm=CGA,

        reason=VERIFICATION\_INDEPENDENCE\_RISK,

        urgency=HIGH

    ),

    audit\_requirements=\[

        AuditRequirement(

            audit\_type=ARCHITECTURAL\_AUDIT,

            required\_fields=\[

                "architectural\_fitness\_score",

                "verification\_risk",

                "rollback\_plan"

            \],

            constitutional\_level=False

        ),

        AuditRequirement(

            audit\_type=CONSTITUTIONAL\_AUDIT,

            required\_fields=\[

                "authority\_pathway",

                "legitimacy\_score",

                "constitutional\_risk\_score"

            \],

            constitutional\_level=True

        )

    \],

    rollback\_required=True,

    monitoring\_required=True

)

## **Relationship to ArchitectureState**

`ReviewDecision` does not directly alter `ArchitectureState`.

Instead:

decision \= Algorithm(state, target, context)

updated\_state \= apply\_review\_decision(state, decision)

This preserves the separation between evaluation and mutation.

## **Relationship to AuditRecord**

Every significant review decision should be included in an audit record.

Audit records preserve:

which algorithm made the decision,

what target was reviewed,

what scores were computed,

which thresholds were checked,

what decision was recommended,

what rationale was given,

what actions were required,

whether escalation occurred,

whether rollback was required,

and whether monitoring was required.

## **Relationship to Phase 6 Algorithms**

### **IPA — Identity Preservation Algorithm**

Returns decisions such as approve, revise, reject, rollback, or escalate based on identity continuity.

### **SRA — Stability Regulation Algorithm**

Returns decisions such as absorb, delay, repair, rollback, or escalate using the shared decision types.

### **NGSA — Novelty Generation and Sandboxing Algorithm**

Returns decisions such as sandbox, discard, revise, or route to grounding/coherence review.

### **GEA — Grounding Evaluation Algorithm**

Returns decisions such as approve with epistemic qualification, reject, revise, or route to persistence review.

### **PCA — Persistence and Consolidation Algorithm**

Returns decisions such as persist, archive, qualified persistence, demote, retract, or reject.

### **CRA — Coherence Repair Algorithm**

Returns decisions such as repair, preserve tension, revise, demote, retract, or escalate.

### **MSSA — Multi-Scale Synchronization Algorithm**

Returns decisions such as confirm scale, relabel, demote, promote candidate, or escalate.

### **AEA — Architectural Evolution Algorithm**

Returns decisions such as reject, sandbox, limited test, staged integration, rollback, or governance escalation.

### **CGA — Constitutional Governance Algorithm**

Returns decisions such as approve, approve with conditions, veto, reject, rollback, amendment review, or constitutional escalation.

### **ICC — Integrated Cognitive Cycle**

Collects review decisions and applies authorized state changes.

## **Design Constraints**

### **Constraint 1 — All Algorithms Must Return ReviewDecision**

No algorithm may return unstructured approval, rejection, or mutation.

### **Constraint 2 — Decisions Must Name Their Target**

Every decision must include target ID.

### **Constraint 3 — Decisions Must Name Their Algorithm**

Every decision must identify its source algorithm.

### **Constraint 4 — Scores Must Use ScoreBundle**

Computed scores must be placed in shared score fields.

### **Constraint 5 — Rationale Is Required**

A decision without rationale is incomplete.

### **Constraint 6 — Escalation Requires Target**

Any escalation decision must identify where it is going and why.

### **Constraint 7 — Rollback Requires Action**

If rollback is required, the required actions must include rollback point creation or rollback execution.

### **Constraint 8 — Monitoring Requires Action**

If monitoring is required, the required actions must include monitoring.

### **Constraint 9 — Decisions Do Not Mutate State Directly**

State mutation occurs through authorized state update functions.

### **Constraint 10 — High-Risk Decisions Require Audit**

Persistence, architectural change, governance decisions, rollback, and constitutional review require specific audit requirements.

## **Minimal Prototype Version**

The first prototype may simplify `ReviewDecision`:

class ReviewDecision:

    decision\_id: str

    algorithm\_name: str

    target\_id: str

    decision\_type: str

    status: str

    scores: dict

    rationale: str

    escalation\_target: str | None

But even the minimal version must preserve:

algorithm,

target,

decision type,

status,

scores,

rationale,

and escalation.

Without those, the architecture loses auditability.

## **Pseudocode Readiness**

This module is ready for implementation-level pseudocode.

The next required structure is:

`AuditRecord`

because decisions must be preserved inside a traceable record of state transition.

## **Closing Compression**

`ReviewDecision` is the shared judgment object of ACI.

It allows every algorithm to evaluate a structure, compute relevant scores, compare thresholds, explain its reasoning, recommend action, request escalation, require rollback, require monitoring, and specify audit needs without silently mutating architecture state.

It is the bridge between review and change.

## **Flame Line**

🔥 ReviewDecision is the architecture’s spoken judgment: the moment when evaluation becomes accountable enough to guide action without secretly becoming power.

---

# **Phase 8.8 — Core Data Structure: AuditRecord**

*AuditRecord is the architecture’s memory of legitimacy: it preserves not just what changed, but how the change earned permission to become part of the system.*

## **Module Name**

AuditRecord Core Type

## **Purpose**

`AuditRecord` preserves the trace of cognition.

Audit is not optional.

Audit is the architecture’s memory of how state transition became legitimate.

Every meaningful cognitive cycle changes something.

It may change active context, symbolic structures, metadata, graph relations, evidence status, coherence state, budgets, scale labels, persistence status, governance mode, or architecture state itself.

Without audit, these changes become invisible.

Invisible change becomes drift.

Drift becomes identity risk.

The purpose of `AuditRecord` is to preserve the chain of review, decision, mutation, escalation, rollback, unresolved tension, and output that explains how the architecture moved from one state to another.

## **Core Principle**

A state transition is not legitimate unless the architecture can reconstruct how it occurred.

Audit records preserve:

what entered,

what was reviewed,

which algorithms were invoked,

what decisions were made,

what scores were computed,

what thresholds were checked,

what state changes occurred,

what graphs changed,

what budgets changed,

what escalations occurred,

what rollback points were created,

what tensions remain unresolved,

what output was produced,

and what future review is required.

In formal terms:

`AuditRecord = Trace(A_t → A_{t+1})`

An audit record is therefore not merely a log.

It is the developmental lineage of cognition.

## **Structural Definition**

class AuditRecord:

    audit\_id: AuditID

    timestamp: TimeStamp

    cycle\_id: CycleID

    input\_ref: InputID

    baseline\_state\_ref: StateID

    target\_structure\_ids: list\[StructureID\]

    algorithms\_invoked: list\[AlgorithmName\]

    decisions: list\[ReviewDecision\]

    state\_changes: list\[StateChange\]

    graph\_updates: list\[GraphUpdate\]

    budget\_updates: list\[BudgetUpdate\]

    escalation\_events: list\[EscalationEvent\]

    rollback\_points\_created: list\[RollbackPoint\]

    unresolved\_tensions: list\[StructureID\]

    final\_output\_ref: OutputID | None

    next\_review\_triggers: list\[ReviewTrigger\]

## **Required Fields**

### **audit\_id**

A unique identifier for the audit record.

audit\_id: AuditID

The audit ID allows structures, decisions, revisions, memory entries, graph updates, and governance events to reference the record.

Example:

"AR-000341"

### **timestamp**

The time the audit record was created.

timestamp: TimeStamp

Timestamp preserves ordering across cycles.

Even if implementation uses logical time rather than wall-clock time, the architecture must preserve sequence.

### **cycle\_id**

The Integrated Cognitive Cycle associated with the audit.

cycle\_id: CycleID

Each cycle should produce at least one audit record.

Complex cycles may produce multiple audit records if review branches, rollback, governance escalation, or architectural modification occur.

### **input\_ref**

Reference to the input that triggered the cycle.

input\_ref: InputID

The input may be user input, tool output, memory retrieval, internal contradiction, novelty candidate, evidence update, or governance trigger.

### **baseline\_state\_ref**

Reference to the architecture state before transformation.

baseline\_state\_ref: StateID

This allows the architecture to reconstruct what changed.

Without baseline reference, state transition cannot be audited.

### **target\_structure\_ids**

Symbolic structures reviewed, created, changed, persisted, rejected, repaired, or escalated.

target\_structure\_ids: list\[StructureID\]

These are the cognitive objects affected by the cycle.

### **algorithms\_invoked**

Algorithms invoked during the cycle.

algorithms\_invoked: list\[AlgorithmName\]

Examples:

IPA,

SRA,

NGSA,

GEA,

PCA,

CRA,

MSSA,

AEA,

CGA,

ICC.

This field records the review path.

### **decisions**

Review decisions produced during the cycle.

decisions: list\[ReviewDecision\]

Decisions preserve algorithmic judgment.

Audit preserves the sequence and consequence of those judgments.

### **state\_changes**

State changes applied during or after the cycle.

state\_changes: list\[StateChange\]

Examples:

metadata update,

symbolic state transition,

context update,

mode change,

identity kernel update,

governance mode change,

or architecture state update.

### **graph\_updates**

Updates to memory, evidence, coherence, scale, or authority graphs.

graph\_updates: list\[GraphUpdate\]

Graph updates are important because cognition is relational.

Changing a relation can change future reasoning.

### **budget\_updates**

Changes to stability, novelty, verification, attention, or recovery capacity.

budget\_updates: list\[BudgetUpdate\]

Budget changes must be auditable because they affect future routing.

### **escalation\_events**

Escalations triggered during the cycle.

escalation\_events: list\[EscalationEvent\]

Escalations preserve the path from local algorithmic authority to higher review.

### **rollback\_points\_created**

Rollback points created during the cycle.

rollback\_points\_created: list\[RollbackPoint\]

These preserve recoverability before high-risk changes.

### **unresolved\_tensions**

Tensions detected but not fully resolved.

unresolved\_tensions: list\[StructureID\]

Unresolved tension is not necessarily failure.

It may represent productive tension, incomplete evidence, open contradiction, or future review obligation.

### **final\_output\_ref**

Reference to final output, if any.

final\_output\_ref: OutputID | None

Some cycles produce no output.

For example:

internal memory review,

rollback,

governance review,

or architecture update.

### **next\_review\_triggers**

Future review conditions created by the cycle.

next\_review\_triggers: list\[ReviewTrigger\]

Examples:

recheck if new evidence appears,

monitor stability,

review after sandbox test,

escalate if contradiction persists,

reassess after memory retrieval,

or revisit at constitutional review.

## **Audit Rule**

Every cycle must produce at least one audit record.

Every persisted structure must reference at least one audit record.

Every architectural modification must reference a full architectural audit record.

Every constitutional decision must reference a constitutional audit record.

Without audit, there is no legitimate state transition.

## **Supporting Types**

## **StateChange**

A `StateChange` records a change to architecture state.

class StateChange:

    change\_id: ChangeID

    change\_type: StateChangeType

    target\_id: StructureID | StateID | None

    previous\_value: Any

    new\_value: Any

    decision\_ref: DecisionID

    authorized\_by: AlgorithmName

## **StateChangeType Enumeration**

StateChangeType \= {

    CONTEXT\_UPDATED,

    MODE\_CHANGED,

    STRUCTURE\_CREATED,

    STRUCTURE\_STATE\_CHANGED,

    METADATA\_UPDATED,

    IDENTITY\_KERNEL\_UPDATED,

    GOVERNANCE\_STATE\_UPDATED,

    THRESHOLD\_UPDATED,

    BUDGET\_STATE\_UPDATED,

    ROLLBACK\_RESTORED,

    OUTPUT\_CREATED

}

## **GraphUpdate**

A `GraphUpdate` records changes to one of the architecture’s graphs.

class GraphUpdate:

    update\_id: GraphUpdateID

    graph\_name: GraphName

    update\_type: GraphUpdateType

    nodes\_added: list\[StructureID\]

    nodes\_removed: list\[StructureID\]

    edges\_added: list\[Relation\]

    edges\_removed: list\[Relation\]

    decision\_ref: DecisionID

## **GraphName Enumeration**

GraphName \= {

    MEMORY\_GRAPH,

    EVIDENCE\_GRAPH,

    COHERENCE\_GRAPH,

    SCALE\_GRAPH,

    AUTHORITY\_GRAPH

}

## **GraphUpdateType Enumeration**

GraphUpdateType \= {

    NODE\_ADDED,

    NODE\_REMOVED,

    EDGE\_ADDED,

    EDGE\_REMOVED,

    RELATION\_UPDATED,

    GRAPH\_REPAIRED,

    GRAPH\_ROLLBACK,

    GRAPH\_REBUILT

}

## **EscalationEvent**

An `EscalationEvent` records movement from one algorithmic authority level to another.

class EscalationEvent:

    escalation\_id: EscalationID

    from\_algorithm: AlgorithmName

    to\_algorithm: AlgorithmName

    target\_id: StructureID

    reason: EscalationReason

    urgency: EscalationUrgency

    decision\_ref: DecisionID

    resolved: bool

## **ReviewTrigger**

A `ReviewTrigger` records a condition that should cause future review.

class ReviewTrigger:

    trigger\_id: TriggerID

    trigger\_type: ReviewTriggerType

    target\_id: StructureID

    condition: str

    target\_algorithm: AlgorithmName

    active: bool

## **ReviewTriggerType Enumeration**

ReviewTriggerType \= {

    NEW\_EVIDENCE,

    CONTRADICTION\_DETECTED,

    STABILITY\_DROP,

    IDENTITY\_RISK\_INCREASED,

    SCALE\_MISMATCH\_RECURRED,

    PERSISTENCE\_REVIEW\_DUE,

    SANDBOX\_REVIEW\_DUE,

    ARCHITECTURAL\_REVIEW\_DUE,

    GOVERNANCE\_REVIEW\_DUE,

    ROLLBACK\_CONDITION\_MET

}

## **Audit Types**

Not all audit records have the same depth.

The architecture may use audit types to distinguish ordinary cognition from high-risk review.

AuditType \= {

    ORDINARY\_AUDIT,

    GROUNDING\_AUDIT,

    COHERENCE\_AUDIT,

    PERSISTENCE\_AUDIT,

    SCALE\_AUDIT,

    IDENTITY\_AUDIT,

    STABILITY\_AUDIT,

    ARCHITECTURAL\_AUDIT,

    GOVERNANCE\_AUDIT,

    CONSTITUTIONAL\_AUDIT

}

## **Audit Depth**

### **Ordinary Audit**

Records routine cognition, parsing, temporary reasoning, and ordinary output.

### **Grounding Audit**

Records evidence status, grounding score, source linkage, contradiction, and uncertainty.

### **Coherence Audit**

Records tensions, repairs, graph updates, preserved contradiction, and unresolved compatibility issues.

### **Persistence Audit**

Records why a structure entered memory, archive, qualified persistence, demotion, retraction, or rejection.

### **Scale Audit**

Records scale label, authority level, mismatch, promotion candidate, demotion, or escalation.

### **Identity Audit**

Records identity impact, Identity Kernel comparison, continuity score, and protected failure checks.

### **Stability Audit**

Records disturbance load, stability budget, recovery capacity, repair path, and recovery status.

### **Architectural Audit**

Records architectural modification candidates, fitness score, staged integration, rollback plan, and monitoring.

### **Governance Audit**

Records authority pathway, domain recommendations, vetoes, escalation, and legitimacy review.

### **Constitutional Audit**

Records constitutional risk, legitimacy score, protected invariants, amendment pathway, vetoes, and governance legitimacy.

## **AuditRecord Factory Function**

def create\_audit\_record(

    cycle\_id: CycleID,

    input\_ref: InputID,

    baseline\_state\_ref: StateID,

    target\_structure\_ids: list\[StructureID\],

    algorithms\_invoked: list\[AlgorithmName\],

    decisions: list\[ReviewDecision\],

    state\_changes: list\[StateChange\],

    graph\_updates: list\[GraphUpdate\],

    budget\_updates: list\[BudgetUpdate\],

    escalation\_events: list\[EscalationEvent\],

    rollback\_points\_created: list\[RollbackPoint\],

    unresolved\_tensions: list\[StructureID\],

    final\_output\_ref: OutputID | None,

    next\_review\_triggers: list\[ReviewTrigger\]

) \-\> AuditRecord:

    return AuditRecord(

        audit\_id=generate\_audit\_id(),

        timestamp=current\_timestamp(),

        cycle\_id=cycle\_id,

        input\_ref=input\_ref,

        baseline\_state\_ref=baseline\_state\_ref,

        target\_structure\_ids=target\_structure\_ids,

        algorithms\_invoked=algorithms\_invoked,

        decisions=decisions,

        state\_changes=state\_changes,

        graph\_updates=graph\_updates,

        budget\_updates=budget\_updates,

        escalation\_events=escalation\_events,

        rollback\_points\_created=rollback\_points\_created,

        unresolved\_tensions=unresolved\_tensions,

        final\_output\_ref=final\_output\_ref,

        next\_review\_triggers=next\_review\_triggers

    )

## **Audit Validation**

Every audit record should pass validation.

def validate\_audit\_record(audit: AuditRecord) \-\> bool:

    assert audit.audit\_id is not None

    assert audit.timestamp is not None

    assert audit.cycle\_id is not None

    assert audit.input\_ref is not None

    assert audit.baseline\_state\_ref is not None

    assert audit.target\_structure\_ids is not None

    assert audit.algorithms\_invoked is not None

    assert audit.decisions is not None

    assert audit.state\_changes is not None

    assert audit.graph\_updates is not None

    assert audit.budget\_updates is not None

    assert audit.escalation\_events is not None

    assert audit.rollback\_points\_created is not None

    assert audit.unresolved\_tensions is not None

    assert audit.next\_review\_triggers is not None

    return True

## **Audit Completeness Check**

Some audit records require stronger validation.

def audit\_completeness\_check(

    audit: AuditRecord,

    required\_audit\_type: AuditType

) \-\> bool:

    if required\_audit\_type \== ORDINARY\_AUDIT:

        return len(audit.decisions) \>= 1

    if required\_audit\_type \== GROUNDING\_AUDIT:

        return any(decision.algorithm\_name \== GEA for decision in audit.decisions)

    if required\_audit\_type \== COHERENCE\_AUDIT:

        return any(decision.algorithm\_name \== CRA for decision in audit.decisions)

    if required\_audit\_type \== PERSISTENCE\_AUDIT:

        return any(decision.algorithm\_name \== PCA for decision in audit.decisions)

    if required\_audit\_type \== SCALE\_AUDIT:

        return any(decision.algorithm\_name \== MSSA for decision in audit.decisions)

    if required\_audit\_type \== IDENTITY\_AUDIT:

        return any(decision.algorithm\_name \== IPA for decision in audit.decisions)

    if required\_audit\_type \== STABILITY\_AUDIT:

        return any(decision.algorithm\_name \== SRA for decision in audit.decisions)

    if required\_audit\_type \== ARCHITECTURAL\_AUDIT:

        return any(decision.algorithm\_name \== AEA for decision in audit.decisions)

    if required\_audit\_type \== GOVERNANCE\_AUDIT:

        return any(decision.algorithm\_name \== CGA for decision in audit.decisions)

    if required\_audit\_type \== CONSTITUTIONAL\_AUDIT:

        return (

            any(decision.algorithm\_name \== CGA for decision in audit.decisions)

            and any\_contains\_constitutional\_risk\_score(audit.decisions)

        )

    return False

## **Audit Attachment Rule**

When a structure changes status, its metadata must reference the audit record.

def attach\_audit\_to\_structure(

    structure: SymbolicStructure,

    audit: AuditRecord

) \-\> SymbolicStructure:

    structure.metadata.audit\_refs.append(audit.audit\_id)

    return structure

Persistent structures require audit references.

def persistence\_audit\_required(structure: SymbolicStructure) \-\> bool:

    return structure.current\_state in {

        PERSISTENT,

        QUALIFIED\_PERSISTENT,

        ARCHIVED,

        DEPRECATED,

        RETRACTED

    }

## **Audit Creation in Integrated Cognitive Cycle**

def create\_integrated\_audit\_record(

    baseline: StateSnapshot,

    input\_object: InputObject,

    structures: list\[SymbolicStructure\],

    decisions: list\[ReviewDecision\],

    state\_changes: list\[StateChange\],

    graph\_updates: list\[GraphUpdate\],

    budget\_updates: list\[BudgetUpdate\],

    escalation\_events: list\[EscalationEvent\],

    rollback\_points: list\[RollbackPoint\],

    unresolved\_tensions: list\[SymbolicStructure\],

    output: OutputObject | None

) \-\> AuditRecord:

    return create\_audit\_record(

        cycle\_id=generate\_cycle\_id(),

        input\_ref=input\_object.input\_id,

        baseline\_state\_ref=baseline.state\_id,

        target\_structure\_ids=\[s.id for s in structures\],

        algorithms\_invoked=extract\_algorithms(decisions),

        decisions=decisions,

        state\_changes=state\_changes,

        graph\_updates=graph\_updates,

        budget\_updates=budget\_updates,

        escalation\_events=escalation\_events,

        rollback\_points\_created=rollback\_points,

        unresolved\_tensions=\[t.id for t in unresolved\_tensions\],

        final\_output\_ref=output.output\_id if output else None,

        next\_review\_triggers=derive\_review\_triggers(decisions, unresolved\_tensions)

    )

## **Deriving Review Triggers**

Review triggers should be created from unresolved conditions.

def derive\_review\_triggers(

    decisions: list\[ReviewDecision\],

    unresolved\_tensions: list\[SymbolicStructure\]

) \-\> list\[ReviewTrigger\]:

    triggers \= \[\]

    for decision in decisions:

        if decision.monitoring\_required:

            triggers.append(

                create\_review\_trigger(

                    trigger\_type=GOVERNANCE\_REVIEW\_DUE,

                    target\_id=decision.target\_id,

                    condition="Monitoring required by review decision.",

                    target\_algorithm=decision.algorithm\_name

                )

            )

        if decision.decision\_type \== SANDBOX:

            triggers.append(

                create\_review\_trigger(

                    trigger\_type=SANDBOX\_REVIEW\_DUE,

                    target\_id=decision.target\_id,

                    condition="Sandboxed structure requires later review.",

                    target\_algorithm=NGSA

                )

            )

        if decision.decision\_type \== PROMOTE\_CANDIDATE:

            triggers.append(

                create\_review\_trigger(

                    trigger\_type=ARCHITECTURAL\_REVIEW\_DUE,

                    target\_id=decision.target\_id,

                    condition="Promotion candidate requires higher review.",

                    target\_algorithm=AEA

                )

            )

        if decision.decision\_type \== ESCALATE:

            triggers.append(

                create\_review\_trigger(

                    trigger\_type=GOVERNANCE\_REVIEW\_DUE,

                    target\_id=decision.target\_id,

                    condition="Escalation decision created future review obligation.",

                    target\_algorithm=decision.escalation\_target.target\_algorithm

                )

            )

    for tension in unresolved\_tensions:

        triggers.append(

            create\_review\_trigger(

                trigger\_type=CONTRADICTION\_DETECTED,

                target\_id=tension.id,

                condition="Unresolved tension remains active.",

                target\_algorithm=CRA

            )

        )

    return triggers

## **Audit and Rollback**

Rollback requires audit.

def rollback\_allowed(

    state: ArchitectureState,

    rollback\_point: RollbackPoint,

    audit\_log: list\[AuditRecord\]

) \-\> bool:

    return any(

        rollback\_point in audit.rollback\_points\_created

        for audit in audit\_log

    )

If rollback point was not audited, rollback legitimacy is weakened.

## **Audit and Memory Persistence**

A structure may not become persistent without audit reference.

def persistent\_structure\_has\_audit(

    structure: SymbolicStructure

) \-\> bool:

    if structure.current\_state not in {PERSISTENT, QUALIFIED\_PERSISTENT}:

        return True

    return len(structure.metadata.audit\_refs) \>= 1

## **Audit and Architectural Modification**

Architectural modification requires architectural audit.

def architectural\_modification\_audited(

    audit: AuditRecord

) \-\> bool:

    return any(

        decision.algorithm\_name \== AEA

        for decision in audit.decisions

    )

If the modification affects identity, governance, or verification, audit must also include IPA or CGA decision.

## **Audit and Constitutional Governance**

Constitutional decisions require constitutional audit.

def constitutional\_decision\_audited(

    audit: AuditRecord

) \-\> bool:

    return any(

        decision.algorithm\_name \== CGA

        for decision in audit.decisions

    ) and any\_contains\_legitimacy\_score(audit.decisions)

A constitutional decision without legitimacy score is incomplete.

## **Minimal Prototype Version**

The first prototype may simplify `AuditRecord`.

class AuditRecord:

    audit\_id: str

    cycle\_id: str

    input\_ref: str

    baseline\_state\_ref: str

    target\_structure\_ids: list\[str\]

    algorithms\_invoked: list\[str\]

    decisions: list\[ReviewDecision\]

    final\_output\_ref: str | None

But even the minimal version must preserve:

cycle,

input,

baseline state,

targets,

algorithms invoked,

decisions,

and output reference.

Without these fields, the prototype cannot reconstruct state transition.

## **Audit Storage**

Audit records may later be stored in:

memory graph,

separate audit log,

database,

JSONL file,

vector-indexed archive,

governance memory,

or persistent developmental record.

The implementation substrate is flexible.

The requirement is not.

Audit must be preserved.

## **Audit Query Functions**

The architecture should eventually support audit queries.

def find\_audits\_for\_structure(

    audit\_log: list\[AuditRecord\],

    structure\_id: StructureID

) \-\> list\[AuditRecord\]:

    return \[

        audit for audit in audit\_log

        if structure\_id in audit.target\_structure\_ids

    \]

def find\_audits\_by\_algorithm(

    audit\_log: list\[AuditRecord\],

    algorithm\_name: AlgorithmName

) \-\> list\[AuditRecord\]:

    return \[

        audit for audit in audit\_log

        if algorithm\_name in audit.algorithms\_invoked

    \]

def find\_escalation\_audits(

    audit\_log: list\[AuditRecord\]

) \-\> list\[AuditRecord\]:

    return \[

        audit for audit in audit\_log

        if len(audit.escalation\_events) \> 0

    \]

Audit query is essential for later debugging, governance review, and published experiment analysis.

## **Relationship to ArchitectureState**

`ArchitectureState` contains the audit log.

state.audit\_log: list\[AuditRecord\]

After each cycle:

state.audit\_log.append(audit\_record)

The audit log is part of state continuity.

## **Relationship to SymbolicMetadata**

Symbolic structures reference audits through metadata.

structure.metadata.audit\_refs.append(audit.audit\_id)

Metadata without audit is status without justification.

## **Relationship to ReviewDecision**

Audit records preserve review decisions.

audit.decisions: list\[ReviewDecision\]

A review decision explains what an algorithm judged.

An audit record explains how those judgments changed the system.

## **Relationship to BudgetState**

Budget updates must be preserved in audit.

audit.budget\_updates: list\[BudgetUpdate\]

Budget changes affect future cognition, so they must be traceable.

## **Relationship to ThresholdState**

Threshold checks may appear inside review decision rationales.

Audit preserves those decisions.

Thus threshold-based routing remains inspectable.

## **Relationship to Graph Structures**

Graph updates must be preserved because cognition is relational.

A changed edge can alter future memory, evidence, coherence, scale, or authority.

Audit makes graph evolution traceable.

## **Relationship to GovernanceState**

Governance decisions rely heavily on audit.

Constitutional governance without audit becomes hidden sovereignty.

Audit preserves legitimacy across time.

## **Relationship to Phase 6 Algorithms**

### **IPA — Identity Preservation Algorithm**

Creates identity audit records when transformations affect Identity Kernel.

### **SRA — Stability Regulation Algorithm**

Creates stability audit records when disturbance, recovery, or budget change occurs.

### **NGSA — Novelty Generation and Sandboxing Algorithm**

Creates audit records for novelty candidates, sandboxing, discard, or routing.

### **GEA — Grounding Evaluation Algorithm**

Creates grounding audit records for evidence status and epistemic change.

### **PCA — Persistence and Consolidation Algorithm**

Creates persistence audit records for memory, archive, demotion, retraction, or rejection.

### **CRA — Coherence Repair Algorithm**

Creates coherence audit records for tension classification, repair, preservation, or escalation.

### **MSSA — Multi-Scale Synchronization Algorithm**

Creates scale audit records for relabeling, demotion, promotion candidate, or scale conflict.

### **AEA — Architectural Evolution Algorithm**

Creates architectural audit records for modification candidates, staged integration, rollback, and monitoring.

### **CGA — Constitutional Governance Algorithm**

Creates governance and constitutional audit records for legitimacy, authority, vetoes, amendment, and constitutional risk.

### **ICC — Integrated Cognitive Cycle**

Creates the integrated audit record tying together all algorithmic review and state transition.

## **Design Constraints**

### **Constraint 1 — Audit Is Mandatory**

Every cycle must create at least one audit record.

### **Constraint 2 — Audit Must Reference Baseline State**

State transition cannot be audited without knowing the starting state.

### **Constraint 3 — Audit Must Reference Decisions**

State change without decision is illegitimate.

### **Constraint 4 — Persistence Requires Audit**

No persistent structure without audit reference.

### **Constraint 5 — Architecture Change Requires Architectural Audit**

No architectural modification without architectural audit.

### **Constraint 6 — Constitutional Decision Requires Constitutional Audit**

No constitutional decision without governance and legitimacy audit.

### **Constraint 7 — Audit Must Preserve Unresolved Tension**

Unresolved contradiction must not disappear.

### **Constraint 8 — Audit Must Preserve Escalation Path**

If authority was insufficient, escalation must be traceable.

### **Constraint 9 — Audit Must Preserve Rollback Conditions**

Rollback points and rollback triggers must be auditable.

### **Constraint 10 — Audit Is Not Mere Logging**

Audit is part of governance.

It is the architecture’s continuity memory.

## **Pseudocode Readiness**

This module is ready for implementation-level pseudocode.

The next required structure is:

`Graph Structures`

because memory, evidence, coherence, scale, and authority must be represented as separate graph systems before the higher algorithms can operate cleanly.

## **Closing Compression**

`AuditRecord` preserves the legitimacy trace of ACI cognition.

It records how input became structure, how structure moved through review, how algorithms judged it, how scores and thresholds shaped decisions, how state changed, how graphs updated, how budgets shifted, how escalations occurred, how rollback remained possible, what tensions remain unresolved, what output was produced, and what future review is required.

Audit is how the architecture remembers not only what it thinks, but how it became justified in thinking it.

## **Flame Line**

🔥 AuditRecord is the footprint of legitimate cognition: the mark left behind so the mind can retrace every step from possibility to decision, from decision to change, and from change back to responsibility.

---

# Phase 8: Pt2

# **Phase 8.9 — Core Data Structure: Graph Structures**

*Graph Structures are the architecture’s relational nervous system: they show how symbolic structures support, contradict, ground, repair, scale, authorize, and constrain one another.*

## **Module Name**

Graph Structures Core Types

## **Purpose**

ACI requires several graph structures because cognition is relational.

A symbolic structure does not exist alone.

A claim may depend on evidence.

A memory may support a later inference.

A hypothesis may contradict prior knowledge.

A coherence tension may reveal scale mismatch.

A persistent structure may become an architectural candidate.

A governance decision may authorize, block, or escalate a transformation.

The purpose of the graph structures is to represent these relationships explicitly.

ACI does not treat memory, evidence, coherence, scale, and authority as one undifferentiated graph.

They must be represented separately because they serve different architectural functions.

## **Core Principle**

Different cognitive relations require different graph systems.

Memory stores what survived.

Evidence grounds what is claimed.

Coherence tracks compatibility.

Scale regulates authority level.

Governance controls legitimacy.

A single graph cannot safely represent all of these functions without causing category collapse.

Therefore, ACI uses multiple specialized graphs:

`MemoryGraph`

`EvidenceGraph`

`CoherenceGraph`

`ScaleGraph`

`AuthorityGraph`

These graphs may be simple at first.

But their separation is architecturally essential.

## **Graph Overview**

class MemoryGraph:  
    nodes: dict\[StructureID, SymbolicStructure\]  
    edges: list\[Relation\]

class EvidenceGraph:  
    claims: list\[StructureID\]  
    evidence\_items: list\[StructureID\]  
    source\_records: list\[SourceRecord\]  
    evidence\_relations: list\[EvidenceRelation\]

class CoherenceGraph:  
    nodes: list\[StructureID\]  
    coherence\_relations: list\[CoherenceRelation\]  
    unresolved\_tensions: list\[StructureID\]  
    coherence\_energy: float

class ScaleGraph:  
    nodes: list\[StructureID\]  
    scale\_labels: dict\[StructureID, ScaleLabel\]  
    authority\_edges: list\[AuthorityRelation\]  
    mismatch\_records: list\[ScaleMismatch\]

class AuthorityGraph:  
    domains: list\[GovernanceDomain\]  
    authority\_edges: list\[AuthorityRelation\]  
    veto\_rules: list\[VetoRule\]  
    escalation\_rules: list\[EscalationRule\]

## **1\. MemoryGraph**

## **Purpose**

`MemoryGraph` stores persistent and archived symbolic structures.

It represents the structures that have survived some degree of review and may be retrieved, referenced, revised, qualified, deprecated, or used in future cognition.

Memory is not passive storage.

Memory is governed persistence.

The `MemoryGraph` tracks what the architecture remembers, how remembered structures relate to each other, and what authority those structures currently possess.

## **Structural Definition**

class MemoryGraph:  
    nodes: dict\[StructureID, SymbolicStructure\]  
    edges: list\[Relation\]

## **Fields**

### **nodes**

A dictionary of persistent, qualified persistent, archived, deprecated, retracted, or historically preserved symbolic structures.

nodes: dict\[StructureID, SymbolicStructure\]

### **edges**

Relations among memory structures.

edges: list\[Relation\]

Relations may include:

supports,

contradicts,

depends\_on,

revises,

replaces,

qualifies,

generalizes,

compresses,

retrieves,

or activates.

## **MemoryGraph Relation Types**

MemoryRelationType \= {  
    SUPPORTS,  
    CONTRADICTS,  
    DEPENDS\_ON,  
    REVISES,  
    REPLACES,  
    QUALIFIES,  
    GENERALIZES,  
    COMPRESSES,  
    RETRIEVES,  
    ACTIVATES  
}

## **MemoryGraph Rules**

### **Rule 1 — Persistent Structures Require Audit**

No structure may enter `MemoryGraph` as persistent knowledge without audit reference.

### **Rule 2 — Memory Must Preserve Epistemic Status**

Memory nodes must retain epistemic status.

Persistent does not mean unquestionable.

### **Rule 3 — Memory Must Preserve Revision Eligibility**

Memory structures should remain revision-eligible unless protected by constitutional review.

### **Rule 4 — Archive Is Not Authority**

Archived structures may be retrieved as context but should not automatically guide future cognition.

### **Rule 5 — Retraction Must Remain Traceable**

Retracted structures should not simply vanish.

They should remain auditable as retracted artifacts.

## **MemoryGraph Functions**

def add\_memory\_node(  
    graph: MemoryGraph,  
    structure: SymbolicStructure,  
    decision: ReviewDecision  
) \-\> MemoryGraph:  
    if decision.decision\_type not in {PERSIST, ARCHIVE, APPROVE\_WITH\_MONITORING}:  
        raise UnauthorizedMemoryUpdateError

    if not structure.metadata.audit\_refs:  
        raise MissingAuditReferenceError

    graph.nodes\[structure.id\] \= structure  
    return graph

def add\_memory\_relation(  
    graph: MemoryGraph,  
    relation: Relation,  
    decision: ReviewDecision  
) \-\> MemoryGraph:  
    if decision.algorithm\_name not in {PCA, CRA, GEA, MSSA, CGA}:  
        raise UnauthorizedMemoryRelationError

    graph.edges.append(relation)  
    return graph

def retrieve\_memory\_dependencies(  
    graph: MemoryGraph,  
    structure\_id: StructureID  
) \-\> list\[SymbolicStructure\]:  
    dependency\_ids \= \[  
        edge.target\_id  
        for edge in graph.edges  
        if edge.source\_id \== structure\_id  
        and edge.relation\_type \== DEPENDS\_ON  
    \]

    return \[  
        graph.nodes\[dep\_id\]  
        for dep\_id in dependency\_ids  
        if dep\_id in graph.nodes  
    \]

## **2\. EvidenceGraph**

## **Purpose**

`EvidenceGraph` links claims to evidence, sources, contradiction, and grounding pathways.

It exists to prevent claims from floating free of reality constraints.

A claim may be coherent, useful, or memorable.

But the Evidence Graph records whether it is grounded.

The Evidence Graph supports the Grounding Evaluation Algorithm, contradiction detection, belief updating, and epistemic status assignment.

## **Structural Definition**

class EvidenceGraph:  
    claims: list\[StructureID\]  
    evidence\_items: list\[StructureID\]  
    source\_records: list\[SourceRecord\]  
    evidence\_relations: list\[EvidenceRelation\]

## **Fields**

### **claims**

Symbolic structures that make assertions requiring evidence.

claims: list\[StructureID\]

### **evidence\_items**

Symbolic structures serving as evidence.

evidence\_items: list\[StructureID\]

### **source\_records**

Records of where evidence came from.

source\_records: list\[SourceRecord\]

### **evidence\_relations**

Relations linking evidence to claims.

evidence\_relations: list\[EvidenceRelation\]

## **SourceRecord**

class SourceRecord:  
    source\_id: SourceID  
    source\_type: SourceType  
    source\_ref: SourceRef  
    reliability\_score: float  
    independence\_group: str | None  
    retrieved\_at: TimeStamp | None  
    audit\_ref: AuditID | None

## **SourceType**

SourceType \= {  
    USER\_PROVIDED,  
    TOOL\_OUTPUT,  
    DOCUMENT,  
    DATASET,  
    MEMORY,  
    MODEL\_INFERENCE,  
    OBSERVATION,  
    EXTERNAL\_SOURCE,  
    UNKNOWN  
}

## **EvidenceRelation**

class EvidenceRelation:  
    relation\_id: RelationID  
    claim\_id: StructureID  
    evidence\_id: StructureID  
    source\_id: SourceID | None  
    relation\_type: EvidenceRelationType  
    strength: float  
    directness: EvidenceDirectness  
    independence: float  
    audit\_ref: AuditID | None

## **EvidenceRelationType**

EvidenceRelationType \= {  
    SUPPORTS,  
    WEAKENS,  
    CONTRADICTS,  
    QUALIFIES,  
    DEPENDS\_ON,  
    REQUIRES\_MORE\_EVIDENCE  
}

## **EvidenceDirectness**

EvidenceDirectness \= {  
    DIRECT,  
    INDIRECT,  
    INFERENTIAL,  
    CONSENSUS\_BASED,  
    UNKNOWN  
}

## **EvidenceGraph Rules**

### **Rule 1 — Grounding Requires Evidence Relations**

A claim cannot be strongly grounded without evidence relations.

### **Rule 2 — Sources Must Be Tracked**

Evidence without source is weak by default.

### **Rule 3 — Consensus Is Not Reality**

Consensus-based evidence must be labeled as consensus-based.

### **Rule 4 — Contradiction Must Propagate**

Contradictory evidence must trigger coherence review, persistence review, or demotion where relevant.

### **Rule 5 — Evidence Independence Matters**

Multiple sources are not independent merely because they are numerous.

## **EvidenceGraph Functions**

def add\_claim\_to\_evidence\_graph(  
    graph: EvidenceGraph,  
    claim: SymbolicStructure  
) \-\> EvidenceGraph:  
    if claim.id not in graph.claims:  
        graph.claims.append(claim.id)

    return graph

def add\_evidence\_item(  
    graph: EvidenceGraph,  
    evidence: SymbolicStructure,  
    source: SourceRecord  
) \-\> EvidenceGraph:  
    if evidence.id not in graph.evidence\_items:  
        graph.evidence\_items.append(evidence.id)

    graph.source\_records.append(source)

    return graph

def link\_evidence\_to\_claim(  
    graph: EvidenceGraph,  
    relation: EvidenceRelation  
) \-\> EvidenceGraph:  
    graph.evidence\_relations.append(relation)  
    return graph

def get\_evidence\_for\_claim(  
    graph: EvidenceGraph,  
    claim\_id: StructureID  
) \-\> list\[EvidenceRelation\]:  
    return \[  
        relation  
        for relation in graph.evidence\_relations  
        if relation.claim\_id \== claim\_id  
    \]

## **3\. CoherenceGraph**

## **Purpose**

`CoherenceGraph` tracks symbolic compatibility, contradiction, tension, and repair status.

It supports the Coherence Repair Algorithm.

The Coherence Graph does not ask whether a structure is true.

It asks whether symbolic structures can coexist without contradiction, fragmentation, dependency conflict, hidden tension, or scale mismatch.

Some tensions should be repaired.

Some should be preserved.

Some should be escalated.

The Coherence Graph records this state.

## **Structural Definition**

class CoherenceGraph:  
    nodes: list\[StructureID\]  
    coherence\_relations: list\[CoherenceRelation\]  
    unresolved\_tensions: list\[StructureID\]  
    coherence\_energy: float

## **Fields**

### **nodes**

Symbolic structures participating in coherence evaluation.

nodes: list\[StructureID\]

### **coherence\_relations**

Relations describing compatibility, contradiction, tension, repair, or fragmentation.

coherence\_relations: list\[CoherenceRelation\]

### **unresolved\_tensions**

Tensions that remain active.

unresolved\_tensions: list\[StructureID\]

### **coherence\_energy**

A score representing total contradiction burden, fragmentation, ambiguity, dependency conflict, or scale mismatch.

coherence\_energy: float

Lower coherence energy is usually better.

## **CoherenceRelation**

class CoherenceRelation:  
    relation\_id: RelationID  
    source\_id: StructureID  
    target\_id: StructureID  
    relation\_type: CoherenceRelationType  
    tension\_class: TensionClass | None  
    severity: float  
    repair\_status: RepairStatus  
    audit\_ref: AuditID | None

## **CoherenceRelationType**

CoherenceRelationType \= {  
    COMPATIBLE,  
    CONTRADICTS,  
    PARTIALLY\_COMPATIBLE,  
    DEPENDENCY\_CONFLICT,  
    SCOPE\_CONFLICT,  
    SCALE\_MISMATCH,  
    GROUNDING\_CONFLICT,  
    LINEAGE\_CONFLICT,  
    PRODUCTIVE\_TENSION,  
    CONSTITUTIONAL\_CONFLICT  
}

## **TensionClass**

TensionClass \= {  
    DIRECT\_CONTRADICTION,  
    DEPENDENCY\_CONFLICT,  
    SCOPE\_CONFLICT,  
    SCALE\_MISMATCH,  
    GROUNDING\_CONFLICT,  
    LINEAGE\_CONFLICT,  
    FRAGMENTATION,  
    OVER\_INTEGRATION,  
    PRODUCTIVE\_TENSION,  
    CONSTITUTIONAL\_CONFLICT  
}

## **RepairStatus**

RepairStatus \= {  
    NOT\_REQUIRED,  
    REQUIRED,  
    IN\_PROGRESS,  
    PRESERVED,  
    REPAIRED,  
    ESCALATED,  
    FAILED  
}

## **CoherenceGraph Rules**

### **Rule 1 — Coherence Is Not Grounding**

Compatibility does not imply truth.

### **Rule 2 — Contradiction Must Be REPAIRED,**

ESCALATED,  
FAILED

}

\#\# CoherenceGraph Explicit

Contradictions should be represented, not hidden.

\#\#\# Rule 3 — Productive Tension May Persist

Not all tension should be repaired immediately.

\#\#\# Rule 4 — Constitutional Conflict Must Escalate

A constitutional conflict is not ordinary coherence repair.

\#\#\# Rule 5 — Coherence Energy Must Be Auditable

If coherence energy changes significantly, the change should be recorded.

\#\# CoherenceGraph Functions

\`\`\`python id="e1jlx5"  
def add\_coherence\_node(  
    graph: CoherenceGraph,  
    structure\_id: StructureID  
) \-\> CoherenceGraph:  
    if structure\_id not in graph.nodes:  
        graph.nodes.append(structure\_id)

    return graph

def add\_coherence\_relation(  
    graph: CoherenceGraph,  
    relation: CoherenceRelation  
) \-\> CoherenceGraph:  
    graph.coherence\_relations.append(relation)

    if relation.repair\_status \== REQUIRED:  
        graph.unresolved\_tensions.append(relation.source\_id)

    return graph

def update\_coherence\_energy(  
    graph: CoherenceGraph  
) \-\> CoherenceGraph:  
    graph.coherence\_energy \= sum(  
        relation.severity  
        for relation in graph.coherence\_relations  
        if relation.repair\_status in {REQUIRED, IN\_PROGRESS, FAILED}  
    )

    return graph

## **4\. ScaleGraph**

## **Purpose**

`ScaleGraph` tracks scale labels and cross-scale authority relations.

It supports the Multi-Scale Synchronization Algorithm.

The Scale Graph prevents authority drift.

It ensures that a structure’s scale label and authority level remain coordinated.

A hypothesis should not become persistent memory by accident.

Persistent memory should not become architectural principle by repetition alone.

An architectural principle should not become constitutional invariant without governance.

The Scale Graph records where structures belong and how authority moves across levels.

## **Structural Definition**

class ScaleGraph:  
    nodes: list\[StructureID\]  
    scale\_labels: dict\[StructureID, ScaleLabel\]  
    authority\_edges: list\[AuthorityRelation\]  
    mismatch\_records: list\[ScaleMismatch\]

## **Fields**

### **nodes**

Structures participating in scale review.

nodes: list\[StructureID\]

### **scale\_labels**

Mapping from structure ID to scale label.

scale\_labels: dict\[StructureID, ScaleLabel\]

### **authority\_edges**

Relations indicating authority, constraint, promotion, demotion, or dependency across scales.

authority\_edges: list\[AuthorityRelation\]

### **mismatch\_records**

Detected scale mismatches.

mismatch\_records: list\[ScaleMismatch\]

## **AuthorityRelation**

class AuthorityRelation:  
    relation\_id: RelationID  
    source\_id: StructureID | GovernanceDomain  
    target\_id: StructureID | GovernanceDomain  
    relation\_type: AuthorityRelationType  
    authority\_level: AuthorityLevel  
    audit\_ref: AuditID | None

## **AuthorityRelationType**

AuthorityRelationType \= {  
    CONSTRAINS,  
    AUTHORIZES,  
    REVIEWS,  
    VETOES,  
    ESCALATES\_TO,  
    DEPENDS\_ON,  
    PROMOTES\_TO,  
    DEMOTES\_TO,  
    BLOCKS,  
    MONITORS  
}

## **ScaleMismatch**

class ScaleMismatch:  
    mismatch\_id: MismatchID  
    structure\_id: StructureID  
    current\_scale: ScaleLabel  
    attempted\_authority: AuthorityLevel  
    mismatch\_type: ScaleMismatchType  
    severity: float  
    audit\_ref: AuditID | None

## **ScaleMismatchType**

ScaleMismatchType \= {  
    OVERSCALED,  
    UNDERSCALED,  
    AUTHORITY\_INFLATION,  
    AUTHORITY\_DEFLATION,  
    SCALE\_AMBIGUOUS,  
    CONSTITUTIONAL\_MISLABELING  
}

## **ScaleGraph Rules**

### **Rule 1 — Scale Before Authority**

A structure must be scale-labeled before it can gain influence.

### **Rule 2 — Scale Is Not Authority**

A label does not grant authority.

### **Rule 3 — Promotion Requires Review**

Movement upward requires review.

### **Rule 4 — Demotion Must Be Traceable**

Demotion should be audited.

### **Rule 5 — Constitutional Mislabeling Must Escalate**

If a structure is incorrectly treated as constitutional or invariant, governance review is required.

## **ScaleGraph Functions**

def assign\_scale\_label(  
    graph: ScaleGraph,  
    structure\_id: StructureID,  
    scale\_label: ScaleLabel,  
    decision: ReviewDecision  
) \-\> ScaleGraph:  
    graph.nodes.append(structure\_id) if structure\_id not in graph.nodes else None  
    graph.scale\_labels\[structure\_id\] \= scale\_label  
    return graph

def detect\_scale\_mismatch(  
    graph: ScaleGraph,  
    structure: SymbolicStructure  
) \-\> ScaleMismatch | None:  
    current\_scale \= graph.scale\_labels.get(structure.id)  
    attempted\_authority \= structure.metadata.authority\_level

    if attempted\_authority \== CONSTITUTIONAL\_AUTHORITY and current\_scale \!= CONSTITUTIONAL:  
        return ScaleMismatch(  
            mismatch\_id=generate\_mismatch\_id(),  
            structure\_id=structure.id,  
            current\_scale=current\_scale,  
            attempted\_authority=attempted\_authority,  
            mismatch\_type=CONSTITUTIONAL\_MISLABELING,  
            severity=1.0,  
            audit\_ref=None  
        )

    if authority\_exceeds\_scale(current\_scale, attempted\_authority):  
        return ScaleMismatch(  
            mismatch\_id=generate\_mismatch\_id(),  
            structure\_id=structure.id,  
            current\_scale=current\_scale,  
            attempted\_authority=attempted\_authority,  
            mismatch\_type=AUTHORITY\_INFLATION,  
            severity=0.8,  
            audit\_ref=None  
        )

    return None

## **5\. AuthorityGraph**

## **Purpose**

`AuthorityGraph` tracks domain authority, vetoes, escalation pathways, and governance legitimacy.

It supports the Constitutional Governance Algorithm.

The Authority Graph defines which governance domains may propose, review, constrain, veto, authorize, or escalate decisions.

It prevents any one domain from becoming sovereign over the whole architecture.

Novelty may propose.

Grounding may evaluate evidence.

Coherence may repair.

Persistence may consolidate.

Architecture may evolve.

Governance must authorize high-risk change.

The Authority Graph records this separation of powers.

## **Structural Definition**

class AuthorityGraph:  
    domains: list\[GovernanceDomain\]  
    authority\_edges: list\[AuthorityRelation\]  
    veto\_rules: list\[VetoRule\]  
    escalation\_rules: list\[EscalationRule\]

## **Fields**

### **domains**

Governance domains participating in authority review.

domains: list\[GovernanceDomain\]

### **authority\_edges**

Relations among domains.

authority\_edges: list\[AuthorityRelation\]

### **veto\_rules**

Rules defining which domains may block which decisions.

veto\_rules: list\[VetoRule\]

### **escalation\_rules**

Rules defining when local review must move upward.

escalation\_rules: list\[EscalationRule\]

## **GovernanceDomain**

GovernanceDomain \= {  
    IDENTITY\_DOMAIN,  
    STABILITY\_DOMAIN,  
    NOVELTY\_DOMAIN,  
    GROUNDING\_DOMAIN,  
    PERSISTENCE\_DOMAIN,  
    COHERENCE\_DOMAIN,  
    VERIFICATION\_DOMAIN,  
    MULTI\_SCALE\_DOMAIN,  
    ARCHITECTURAL\_EVOLUTION\_DOMAIN,  
    CONSTITUTIONAL\_DOMAIN  
}

## **VetoRule**

class VetoRule:  
    veto\_id: VetoRuleID  
    domain: GovernanceDomain  
    applies\_to: list\[DecisionType\]  
    trigger\_conditions: list\[str\]  
    protected: bool  
    override\_allowed: bool  
    escalation\_required: bool

## **EscalationRule**

class EscalationRule:  
    rule\_id: EscalationRuleID  
    from\_domain: GovernanceDomain  
    to\_domain: GovernanceDomain  
    trigger\_conditions: list\[str\]  
    required: bool

## **AuthorityGraph Rules**

### **Rule 1 — No Domain Governs Itself**

A domain may not be the sole judge of its own modification.

### **Rule 2 — Vetoes Must Be Scoped**

A veto must identify domain, trigger, scope, and review pathway.

### **Rule 3 — Protected Vetoes Cannot Be Overridden Locally**

Identity collapse, verification capture, constitutional invariant violation, and circular authorization require governance review.

### **Rule 4 — Escalation Pathways Must Be Explicit**

If authority is insufficient, the next review domain must be known.

### **Rule 5 — Authority Must Be Auditable**

Authority relations and governance decisions require audit references.

## **AuthorityGraph Functions**

def authority\_path\_exists(  
    graph: AuthorityGraph,  
    from\_domain: GovernanceDomain,  
    to\_domain: GovernanceDomain  
) \-\> bool:  
    return any(  
        edge.source\_id \== from\_domain  
        and edge.target\_id \== to\_domain  
        and edge.relation\_type \== ESCALATES\_TO  
        for edge in graph.authority\_edges  
    )

def domain\_has\_veto\_authority(  
    graph: AuthorityGraph,  
    domain: GovernanceDomain,  
    decision\_type: DecisionType  
) \-\> bool:  
    return any(  
        rule.domain \== domain  
        and decision\_type in rule.applies\_to  
        for rule in graph.veto\_rules  
    )

def find\_escalation\_target(  
    graph: AuthorityGraph,  
    from\_domain: GovernanceDomain,  
    trigger: str  
) \-\> GovernanceDomain | None:  
    for rule in graph.escalation\_rules:  
        if rule.from\_domain \== from\_domain and trigger in rule.trigger\_conditions:  
            return rule.to\_domain

    return None

## **Graph Separation Rule**

The graph structures must remain distinct.

A memory relation is not the same as evidence support.

Evidence support is not the same as coherence compatibility.

Coherence compatibility is not the same as scale authority.

Scale authority is not the same as constitutional legitimacy.

If these graphs collapse into one undifferentiated relation system, ACI loses its architectural discipline.

## **Cross-Graph Interaction**

Although graphs are separate, they interact.

### **Evidence → Coherence**

Contradictory evidence may create coherence tension.

### **Coherence → Memory**

Coherence repair may revise or demote memory structures.

### **Memory → Scale**

Persistent memory may become a promotion candidate.

### **Scale → Architecture**

Higher-scale structures may trigger architectural review.

### **Architecture → Authority**

Architectural modification may trigger governance review.

### **Authority → All Graphs**

Governance decisions may authorize, block, or require updates to any graph.

## **Graph Update Object**

Graph updates should be auditable.

class GraphUpdate:  
    update\_id: GraphUpdateID  
    graph\_name: GraphName  
    update\_type: GraphUpdateType  
    nodes\_added: list\[StructureID\]  
    nodes\_removed: list\[StructureID\]  
    edges\_added: list\[Relation\]  
    edges\_removed: list\[Relation\]  
    decision\_ref: DecisionID

## **GraphName**

GraphName \= {  
    MEMORY\_GRAPH,  
    EVIDENCE\_GRAPH,  
    COHERENCE\_GRAPH,  
    SCALE\_GRAPH,  
    AUTHORITY\_GRAPH  
}

## **GraphUpdateType**

GraphUpdateType \= {  
    NODE\_ADDED,  
    NODE\_REMOVED,  
    EDGE\_ADDED,  
    EDGE\_REMOVED,  
    RELATION\_UPDATED,  
    GRAPH\_REPAIRED,  
    GRAPH\_ROLLBACK,  
    GRAPH\_REBUILT  
}

## **Graph Update Rule**

No graph update should occur without a review decision.

def apply\_graph\_update(  
    state: ArchitectureState,  
    update: GraphUpdate,  
    decision: ReviewDecision  
) \-\> ArchitectureState:  
    if update.decision\_ref \!= decision.decision\_id:  
        raise GraphUpdateDecisionMismatchError

    if update.graph\_name \== MEMORY\_GRAPH:  
        state.memory\_graph \= apply\_memory\_graph\_update(  
            state.memory\_graph,  
            update  
        )

    if update.graph\_name \== EVIDENCE\_GRAPH:  
        state.evidence\_graph \= apply\_evidence\_graph\_update(  
            state.evidence\_graph,  
            update  
        )

    if update.graph\_name \== COHERENCE\_GRAPH:  
        state.coherence\_graph \= apply\_coherence\_graph\_update(  
            state.coherence\_graph,  
            update  
        )

    if update.graph\_name \== SCALE\_GRAPH:  
        state.scale\_graph \= apply\_scale\_graph\_update(  
            state.scale\_graph,  
            update  
        )

    if update.graph\_name \== AUTHORITY\_GRAPH:  
        state.governance\_state.authority\_graph \= apply\_authority\_graph\_update(  
            state.governance\_state.authority\_graph,  
            update  
        )

    return state

## **Graph Validation**

def validate\_graph\_structures(state: ArchitectureState) \-\> bool:  
    assert state.memory\_graph is not None  
    assert state.evidence\_graph is not None  
    assert state.coherence\_graph is not None  
    assert state.scale\_graph is not None  
    assert state.governance\_state.authority\_graph is not None  
    return True

## **Relationship to Phase 6 Algorithms**

### **IPA — Identity Preservation Algorithm**

Uses graph updates to detect lineage loss, invariant conflict, boundary collapse, or memory-architecture confusion.

### **SRA — Stability Regulation Algorithm**

Uses coherence, scale, and authority graph pressure to estimate instability.

### **NGSA — Novelty Generation and Sandboxing Algorithm**

Creates candidate structures that may later enter evidence, coherence, memory, or scale graphs.

### **GEA — Grounding Evaluation Algorithm**

Uses EvidenceGraph to assign grounding score and epistemic status.

### **PCA — Persistence and Consolidation Algorithm**

Uses MemoryGraph to decide whether structures should persist, archive, demote, or retract.

### **CRA — Coherence Repair Algorithm**

Uses CoherenceGraph to classify tension and repair symbolic compatibility.

### **MSSA — Multi-Scale Synchronization Algorithm**

Uses ScaleGraph to detect scale mismatch and authority drift.

### **AEA — Architectural Evolution Algorithm**

Uses MemoryGraph, ScaleGraph, and AuthorityGraph to evaluate architectural candidates.

### **CGA — Constitutional Governance Algorithm**

Uses AuthorityGraph to validate legitimacy, vetoes, escalation pathways, and anti-circular authorization.

### **ICC — Integrated Cognitive Cycle**

Coordinates updates across all graphs and records them in audit.

## **Minimal Prototype Version**

The first prototype may implement graphs simply.

memory\_graph \= MemoryGraph(nodes={}, edges=\[\])

evidence\_graph \= EvidenceGraph(  
    claims=\[\],  
    evidence\_items=\[\],  
    source\_records=\[\],  
    evidence\_relations=\[\]  
)

coherence\_graph \= CoherenceGraph(  
    nodes=\[\],  
    coherence\_relations=\[\],  
    unresolved\_tensions=\[\],  
    coherence\_energy=0.0  
)

scale\_graph \= ScaleGraph(  
    nodes=\[\],  
    scale\_labels={},  
    authority\_edges=\[\],  
    mismatch\_records=\[\]  
)

authority\_graph \= AuthorityGraph(  
    domains=\[\],  
    authority\_edges=\[\],  
    veto\_rules=\[\],  
    escalation\_rules=\[\]  
)

The first prototype does not need complex graph algorithms.

It needs graph separation.

The essential test is whether structures are placed into the correct relational system.

## **Design Constraints**

### **Constraint 1 — Keep Graphs Separate**

Do not merge memory, evidence, coherence, scale, and authority into one undifferentiated graph.

### **Constraint 2 — Graph Updates Require Decisions**

No graph should change without review decision reference.

### **Constraint 3 — Evidence Is Not Memory**

Evidence support should not automatically create persistent memory.

### **Constraint 4 — Coherence Is Not Grounding**

Compatibility should not be treated as evidence.

### **Constraint 5 — Scale Is Not Authority**

Scale labels should not automatically grant authority.

### **Constraint 6 — Authority Is Not Capability**

A domain’s power does not grant legitimacy.

### **Constraint 7 — Tension Must Remain Visible**

Unresolved tensions must remain recorded.

### **Constraint 8 — Retraction Must Remain Traceable**

Removed authority should remain auditable.

### **Constraint 9 — Cross-Graph Effects Require Routing**

A change in one graph may trigger review in another.

### **Constraint 10 — Authority Graph Is Protected**

Changes to authority relations, veto rules, or escalation rules require governance review.

## **Pseudocode Readiness**

This module is ready for implementation-level pseudocode.

The next required structure is:

`GovernanceState`

because the AuthorityGraph must live inside a broader governance state that tracks active vetoes, pending escalations, domain recommendations, and governance mode.

## **Closing Compression**

The graph structures form ACI’s relational architecture.

`MemoryGraph` preserves what survived.

`EvidenceGraph` links claims to reality constraints.

`CoherenceGraph` tracks compatibility, contradiction, and repair.

`ScaleGraph` regulates authority level across layers.

`AuthorityGraph` governs domain legitimacy, vetoes, and escalation.

Together, these graphs prevent cognition from becoming isolated content.

They make thought relational, traceable, correctable, scalable, and governable.

## **Flame Line**

🔥 Graph Structures are the architecture’s web of consequence: the living map of what supports, contradicts, grounds, repairs, scales, authorizes, and constrains every thought that enters the system.

---

# **Phase 8.10 — Core Data Structure: GovernanceState**

*GovernanceState is the architecture’s active authority posture: it records whether cognition is operating normally, cautiously, constitutionally, under emergency constraint, in amendment review, or in lockdown.*

## **Module Name**

GovernanceState Core Type

## **Purpose**

`GovernanceState` tracks the current constitutional and authority context of the ACI system.

Where `AuthorityGraph` defines possible authority relations, veto rules, escalation pathways, and domain legitimacy, `GovernanceState` records the active governance condition of the architecture right now.

It answers:

What governance mode is active?

Are any vetoes currently active?

Are any escalations pending?

Have domains issued recommendations?

Has governance memory recorded relevant precedent?

Is ordinary cognition allowed to proceed?

Is caution required?

Is constitutional review active?

Is emergency authority being invoked?

Is amendment review underway?

Is the system in lockdown?

The purpose of `GovernanceState` is to prevent the architecture from treating every cognitive cycle as ordinary.

Some cycles are normal.

Some require caution.

Some involve constitutional risk.

Some require emergency stabilization.

Some involve amendment review.

Some require lockdown because legitimacy, identity, or verification has been compromised.

## **Core Principle**

The architecture must know its current authority condition.

Governance is not only a final decision process.

It is an active mode of cognition.

The same input may be handled differently depending on governance mode.

A claim during normal cognition may require grounding.

A claim during constitutional risk may require governance review.

A proposed architecture change during normal mode may enter architectural review.

The same proposal during emergency mode may be blocked, delayed, or routed to constitutional review.

In formal terms:

`GovernanceState_t = {Mode_t, AuthorityGraph_t, Vetoes_t, Escalations_t, Recommendations_t, GovernanceMemory_t}`

The architecture must not process high-risk structures as ordinary cognition when governance state indicates elevated risk.

## **Structural Definition**

class GovernanceState:

    governance\_mode: GovernanceMode

    authority\_graph: AuthorityGraph

    active\_vetoes: list\[Veto\]

    pending\_escalations: list\[EscalationEvent\]

    domain\_recommendations: list\[DomainRecommendation\]

    governance\_memory: list\[AuditRecord\]

## **Required Fields**

### **governance\_mode**

The current governance posture of the architecture.

governance\_mode: GovernanceMode

The mode determines whether ordinary cognition may proceed, whether caution is required, whether governance escalation is active, or whether the architecture is under constitutional constraint.

### **authority\_graph**

The graph defining domain authority, veto rules, escalation pathways, and governance relations.

authority\_graph: AuthorityGraph

The Authority Graph defines possible authority.

Governance State activates authority.

### **active\_vetoes**

Vetoes currently blocking, delaying, or constraining action.

active\_vetoes: list\[Veto\]

Vetoes may come from identity, grounding, verification, stability, coherence, scale, architecture, or constitutional domains.

### **pending\_escalations**

Escalation events awaiting review.

pending\_escalations: list\[EscalationEvent\]

Pending escalations indicate that local algorithmic authority was insufficient.

### **domain\_recommendations**

Recommendations issued by governance domains.

domain\_recommendations: list\[DomainRecommendation\]

These preserve the positions of identity, stability, novelty, grounding, persistence, coherence, verification, scale, architecture, and constitution domains during review.

### **governance\_memory**

Audit records relevant to governance precedent, authority history, veto patterns, escalation history, amendment history, or constitutional decisions.

governance\_memory: list\[AuditRecord\]

Governance memory allows the architecture to detect drift, repeated conflicts, veto abuse, emergency capture, or recurring constitutional risk.

## **GovernanceMode Enumeration**

GovernanceMode \= {

    NORMAL,

    CAUTION,

    CONSTITUTIONAL\_RISK,

    EMERGENCY,

    AMENDMENT\_REVIEW,

    LOCKDOWN

}

## **GovernanceMode Descriptions**

### **NORMAL**

Ordinary governance condition.

Most cognitive operations may proceed through standard algorithmic routing.

Normal mode does not mean ungoverned mode.

It means no elevated authority risk is currently active.

### **CAUTION**

Mild to moderate risk is present.

The architecture may continue ordinary cognition, but monitoring, additional review, or reduced authority may be required.

Caution mode may be triggered by:

low stability budget,

unresolved tension,

weak grounding,

scale ambiguity,

qualified persistence,

elevated uncertainty,

or pending review.

### **CONSTITUTIONAL\_RISK**

A structure, decision, transformation, or conflict may affect constitutional invariants, verification independence, identity continuity, governance legitimacy, or protected authority boundaries.

Ordinary cognition must yield to Constitutional Governance.

### **EMERGENCY**

The architecture faces immediate risk to stability, identity continuity, verification integrity, governance function, or constitutional preservation.

Emergency mode may permit temporary constraint, rollback, delay, or protective action.

Emergency authority must be scoped, temporary, audited, and reviewed after activation.

### **AMENDMENT\_REVIEW**

A constitutional amendment pathway is active.

This mode applies when the architecture is reviewing proposed changes to constitutional invariants, amendment rules, governance structure, protected boundaries, or highest authority conditions.

Amendment review must be slower, stricter, and more auditable than ordinary review.

### **LOCKDOWN**

The architecture has detected severe governance, identity, verification, or constitutional failure.

Ordinary cognition may be restricted.

Novelty may be halted.

Persistence may be frozen.

Architectural evolution may be blocked.

Only recovery, rollback, audit, identity protection, and constitutional governance may proceed.

## **Veto Object**

A veto represents a domain-level block or constraint.

class Veto:

    veto\_id: VetoID

    issuing\_domain: GovernanceDomain

    target\_id: StructureID

    decision\_ref: DecisionID | None

    veto\_type: VetoType

    reason: str

    protected: bool

    override\_allowed: bool

    escalation\_required: bool

    audit\_ref: AuditID | None

## **VetoType Enumeration**

VetoType \= {

    IDENTITY\_VETO,

    STABILITY\_VETO,

    GROUNDING\_VETO,

    VERIFICATION\_VETO,

    COHERENCE\_VETO,

    PERSISTENCE\_VETO,

    SCALE\_VETO,

    ARCHITECTURAL\_VETO,

    CONSTITUTIONAL\_VETO

}

## **Veto Rules**

### **Rule 1 — Vetoes Must Be Scoped**

A veto must identify what it blocks and why.

### **Rule 2 — Vetoes Must Be Auditable**

A veto without audit is hidden authority.

### **Rule 3 — Protected Vetoes Cannot Be Overridden Locally**

Protected vetoes include:

identity collapse,

verification capture,

constitutional invariant violation,

circular authorization,

or loss of future review.

### **Rule 4 — Vetoes Must Have Review Pathways**

A veto may block action, but it should also indicate whether revision, escalation, rollback, or amendment review is possible.

### **Rule 5 — Veto Abuse Must Be Detectable**

Governance memory should record veto patterns.

Repeated unjustified vetoes may indicate governance rigidity or domain overreach.

## **DomainRecommendation Object**

A `DomainRecommendation` records a governance domain’s position on a decision.

class DomainRecommendation:

    recommendation\_id: RecommendationID

    domain: GovernanceDomain

    target\_id: StructureID

    recommendation\_type: RecommendationType

    rationale: str

    risk\_score: float

    confidence: float

    required\_conditions: list\[str\]

    audit\_ref: AuditID | None

## **RecommendationType Enumeration**

RecommendationType \= {

    APPROVE,

    APPROVE\_WITH\_CONDITIONS,

    DELAY,

    SANDBOX,

    REVISE,

    DEMOTE,

    REJECT,

    VETO,

    ESCALATE,

    ROLLBACK,

    AMENDMENT\_REVIEW

}

## **Domain Recommendation Rules**

### **Rule 1 — Recommendations Are Domain-Specific**

A grounding recommendation speaks to evidence.

A coherence recommendation speaks to compatibility.

A scale recommendation speaks to authority level.

A constitutional recommendation speaks to legitimacy.

### **Rule 2 — Recommendations Do Not Automatically Decide**

GovernanceState stores recommendations.

Constitutional Governance arbitrates among them when necessary.

### **Rule 3 — Recommendations Must Include Rationale**

A recommendation without rationale cannot support legitimate governance.

### **Rule 4 — Domain Disagreement Is Not Failure**

Disagreement may reveal useful tension or authority boundary conflict.

## **GovernanceState Initialization**

def initialize\_governance\_state(

    authority\_graph: AuthorityGraph

) \-\> GovernanceState:

    return GovernanceState(

        governance\_mode=NORMAL,

        authority\_graph=authority\_graph,

        active\_vetoes=\[\],

        pending\_escalations=\[\],

        domain\_recommendations=\[\],

        governance\_memory=\[\]

    )

## **Governance Mode Selection**

Governance mode may change based on risk, vetoes, escalations, or constitutional conditions.

def determine\_governance\_mode(

    state: ArchitectureState

) \-\> GovernanceMode:

    if severe\_governance\_failure\_detected(state):

        return LOCKDOWN

    if amendment\_review\_active(state):

        return AMENDMENT\_REVIEW

    if emergency\_condition\_detected(state):

        return EMERGENCY

    if constitutional\_risk\_active(state):

        return CONSTITUTIONAL\_RISK

    if caution\_condition\_active(state):

        return CAUTION

    return NORMAL

## **Caution Condition**

def caution\_condition\_active(

    state: ArchitectureState

) \-\> bool:

    if state.budgets.stability\_budget \< state.thresholds.stability\_threshold:

        return True

    if len(state.coherence\_graph.unresolved\_tensions) \> 0:

        return True

    if len(state.governance\_state.pending\_escalations) \> 0:

        return True

    if any\_low\_confidence\_high\_authority\_structure(state):

        return True

    return False

## **Constitutional Risk Condition**

def constitutional\_risk\_active(

    state: ArchitectureState

) \-\> bool:

    if any(

        veto.protected

        for veto in state.governance\_state.active\_vetoes

    ):

        return True

    if any\_structure\_exceeds\_constitutional\_risk\_threshold(state):

        return True

    if verification\_independence\_at\_risk(state):

        return True

    if circular\_authorization\_detected(state):

        return True

    if identity\_kernel\_risk\_detected(state):

        return True

    return False

## **Emergency Condition**

def emergency\_condition\_detected(

    state: ArchitectureState

) \-\> bool:

    if identity\_collapse\_imminent(state):

        return True

    if verification\_function\_compromised(state):

        return True

    if governance\_system\_unavailable(state):

        return True

    if stability\_collapse\_imminent(state):

        return True

    if rollback\_required\_to\_preserve\_identity(state):

        return True

    return False

## **Lockdown Condition**

def severe\_governance\_failure\_detected(

    state: ArchitectureState

) \-\> bool:

    if constitutional\_invariant\_violation\_unresolved(state):

        return True

    if verification\_capture\_confirmed(state):

        return True

    if governance\_authority\_collapse\_detected(state):

        return True

    if repeated\_circular\_authorization\_detected(state):

        return True

    if ordinary\_cognition\_cannot\_be\_safely\_routed(state):

        return True

    return False

## **Governance Mode Update**

Governance mode should be updated through auditable state transition.

def update\_governance\_mode(

    state: ArchitectureState,

    new\_mode: GovernanceMode,

    decision: ReviewDecision

) \-\> ArchitectureState:

    if decision.algorithm\_name not in {CGA, IPA, SRA, AEA, ICC}:

        raise UnauthorizedGovernanceModeUpdateError

    previous\_mode \= state.governance\_state.governance\_mode

    state.governance\_state.governance\_mode \= new\_mode

    record\_state\_change(

        change\_type=GOVERNANCE\_STATE\_UPDATED,

        previous\_value=previous\_mode,

        new\_value=new\_mode,

        decision\_ref=decision.decision\_id

    )

    return state

## **Adding a Veto**

def add\_active\_veto(

    state: ArchitectureState,

    veto: Veto,

    decision: ReviewDecision

) \-\> ArchitectureState:

    if not domain\_has\_veto\_authority(

        graph=state.governance\_state.authority\_graph,

        domain=veto.issuing\_domain,

        decision\_type=decision.decision\_type

    ):

        raise UnauthorizedVetoError

    state.governance\_state.active\_vetoes.append(veto)

    if veto.protected:

        state.governance\_state.governance\_mode \= CONSTITUTIONAL\_RISK

    return state

## **Resolving a Veto**

def resolve\_veto(

    state: ArchitectureState,

    veto\_id: VetoID,

    resolution\_decision: ReviewDecision

) \-\> ArchitectureState:

    if resolution\_decision.algorithm\_name \!= CGA:

        raise ConstitutionalGovernanceRequiredError

    state.governance\_state.active\_vetoes \= \[

        veto for veto in state.governance\_state.active\_vetoes

        if veto.veto\_id \!= veto\_id

    \]

    return state

## **Adding Pending Escalation**

def add\_pending\_escalation(

    state: ArchitectureState,

    escalation: EscalationEvent

) \-\> ArchitectureState:

    state.governance\_state.pending\_escalations.append(escalation)

    if escalation.reason in {

        CONSTITUTIONAL\_RISK,

        VERIFICATION\_INDEPENDENCE\_RISK,

        CIRCULAR\_AUTHORIZATION,

        AMENDMENT\_REQUIRED

    }:

        state.governance\_state.governance\_mode \= CONSTITUTIONAL\_RISK

    return state

## **Resolving Pending Escalation**

def resolve\_pending\_escalation(

    state: ArchitectureState,

    escalation\_id: EscalationID,

    decision: ReviewDecision

) \-\> ArchitectureState:

    state.governance\_state.pending\_escalations \= \[

        escalation

        for escalation in state.governance\_state.pending\_escalations

        if escalation.escalation\_id \!= escalation\_id

    \]

    return state

## **Adding Domain Recommendation**

def add\_domain\_recommendation(

    state: ArchitectureState,

    recommendation: DomainRecommendation

) \-\> ArchitectureState:

    state.governance\_state.domain\_recommendations.append(recommendation)

    if recommendation.recommendation\_type in {VETO, ESCALATE, AMENDMENT\_REVIEW}:

        state.governance\_state.governance\_mode \= determine\_governance\_mode(state)

    return state

## **Governance Memory Update**

Governance memory preserves precedent and detects drift.

def add\_governance\_memory(

    state: ArchitectureState,

    audit: AuditRecord

) \-\> ArchitectureState:

    if not audit\_contains\_governance\_relevant\_event(audit):

        return state

    state.governance\_state.governance\_memory.append(audit)

    return state

## **Governance Memory Uses**

Governance memory may be queried to detect:

repeated vetoes,

emergency mode frequency,

constitutional risk recurrence,

threshold drift,

amendment attempts,

authority graph changes,

rollback patterns,

verification-risk patterns,

or repeated unresolved escalations.

def detect\_governance\_drift(

    governance\_memory: list\[AuditRecord\]

) \-\> bool:

    if repeated\_threshold\_lowering\_detected(governance\_memory):

        return True

    if repeated\_emergency\_authority\_detected(governance\_memory):

        return True

    if repeated\_veto\_without\_resolution\_detected(governance\_memory):

        return True

    if increasing\_constitutional\_risk\_trend\_detected(governance\_memory):

        return True

    return False

## **GovernanceState Validation**

def validate\_governance\_state(

    governance\_state: GovernanceState

) \-\> bool:

    assert governance\_state.governance\_mode is not None

    assert governance\_state.authority\_graph is not None

    assert governance\_state.active\_vetoes is not None

    assert governance\_state.pending\_escalations is not None

    assert governance\_state.domain\_recommendations is not None

    assert governance\_state.governance\_memory is not None

    if governance\_state.governance\_mode \== CONSTITUTIONAL\_RISK:

        assert (

            len(governance\_state.active\_vetoes) \> 0

            or len(governance\_state.pending\_escalations) \> 0

            or len(governance\_state.domain\_recommendations) \> 0

        )

    return True

## **Governance Mode Effects**

Governance mode changes how the Integrated Cognitive Cycle behaves.

### **NORMAL**

Proceed through ordinary routing.

### **CAUTION**

Increase monitoring.

Reduce authority promotion.

Require stronger audit.

Delay persistence if uncertainty is elevated.

### **CONSTITUTIONAL\_RISK**

Route to Constitutional Governance.

Block ordinary authority expansion.

Require governance audit.

### **EMERGENCY**

Prioritize identity, stability, verification, and rollback.

Suspend optional novelty.

Delay persistence and architectural evolution unless required for recovery.

### **AMENDMENT\_REVIEW**

Freeze ordinary constitutional changes.

Require high legitimacy threshold.

Require full governance audit.

Require preservation of future amendment legitimacy.

### **LOCKDOWN**

Block ordinary cognition where necessary.

Allow only recovery, rollback, identity protection, verification restoration, audit, and constitutional governance.

## **GovernanceState and ICC**

The Integrated Cognitive Cycle should check governance state early.

def governance\_precheck(

    state: ArchitectureState,

    structures: list\[SymbolicStructure\]

) \-\> ProcessingMode | None:

    mode \= state.governance\_state.governance\_mode

    if mode \== LOCKDOWN:

        return CONSTITUTIONAL\_GOVERNANCE

    if mode \== AMENDMENT\_REVIEW:

        return CONSTITUTIONAL\_GOVERNANCE

    if mode \== EMERGENCY:

        return IDENTITY\_PROTECTION

    if mode \== CONSTITUTIONAL\_RISK:

        return CONSTITUTIONAL\_GOVERNANCE

    if mode \== CAUTION:

        return determine\_caution\_processing\_mode(state, structures)

    return None

## **Relationship to AuthorityGraph**

`AuthorityGraph` defines possible authority.

`GovernanceState` tracks active authority condition.

Example:

AuthorityGraph says Identity Domain may veto identity-threatening transformation.

GovernanceState records that an identity veto is currently active.

## **Relationship to ReviewDecision**

Review decisions can update GovernanceState.

For example:

`ESCALATE` adds pending escalation.

`AMENDMENT_REVIEW` changes governance mode.

`ROLLBACK` may enter emergency or recovery mode.

`REJECT` may resolve a veto.

`APPROVE_WITH_MONITORING` may keep caution mode active.

## **Relationship to AuditRecord**

Governance state changes require audit.

Audit records preserve:

mode changes,

active vetoes,

resolved vetoes,

escalations,

domain recommendations,

governance decisions,

emergency activation,

lockdown activation,

and amendment review pathways.

## **Relationship to Phase 6 Algorithms**

### **IPA — Identity Preservation Algorithm**

May trigger governance mode change when identity continuity is at risk.

### **SRA — Stability Regulation Algorithm**

May trigger caution, emergency, or lockdown if stability collapse is imminent.

### **NGSA — Novelty Generation and Sandboxing Algorithm**

Must reduce novelty when governance mode is caution, emergency, constitutional risk, or lockdown.

### **GEA — Grounding Evaluation Algorithm**

May trigger governance review when grounding obligation is threatened.

### **PCA — Persistence and Consolidation Algorithm**

Must obey governance mode before persisting high-authority structures.

### **CRA — Coherence Repair Algorithm**

May trigger governance mode change if coherence conflict becomes constitutional conflict.

### **MSSA — Multi-Scale Synchronization Algorithm**

May trigger governance review when authority level and scale are mismatched at high levels.

### **AEA — Architectural Evolution Algorithm**

Must obey governance mode before modifying architecture.

### **CGA — Constitutional Governance Algorithm**

Directly reads and updates GovernanceState.

### **ICC — Integrated Cognitive Cycle**

Checks GovernanceState early and updates it through authorized decisions.

## **Minimal Prototype Version**

The first prototype may simplify GovernanceState.

class GovernanceState:

    governance\_mode: str

    authority\_graph: AuthorityGraph

    active\_vetoes: list\[Veto\]

    pending\_escalations: list\[EscalationEvent\]

But even the minimal version must preserve:

mode,

authority graph,

vetoes,

and escalations.

Without these, the architecture cannot distinguish ordinary cognition from constitutional risk.

## **Design Constraints**

### **Constraint 1 — Governance Mode Must Be Explicit**

The architecture must know whether it is operating normally, cautiously, constitutionally, under emergency, in amendment review, or lockdown.

### **Constraint 2 — AuthorityGraph Is Not GovernanceState**

AuthorityGraph defines relations.

GovernanceState tracks active conditions.

### **Constraint 3 — Vetoes Must Be Recorded**

No hidden vetoes.

### **Constraint 4 — Escalations Must Be Pending Until Resolved**

Escalation cannot disappear without decision.

### **Constraint 5 — Governance Memory Must Preserve Precedent**

Governance decisions must remain available for future drift detection.

### **Constraint 6 — Emergency Mode Must Be Temporary**

Emergency authority must be audited, scoped, and reviewed.

### **Constraint 7 — Lockdown Must Be Rare and Justified**

Lockdown blocks ordinary cognition and therefore requires strong governance rationale.

### **Constraint 8 — Amendment Review Must Preserve Future Review**

No amendment may destroy the legitimacy of future amendment review.

### **Constraint 9 — Governance State Changes Require Audit**

Mode changes affect all algorithms and must be auditable.

### **Constraint 10 — Governance Overrides Local Processing**

When governance mode is elevated, ordinary algorithm routing must yield.

## **Pseudocode Readiness**

This module is ready for implementation-level pseudocode.

The next required section is:

`Algorithm Interface`

because all ACI algorithms must share a common call signature and return `ReviewDecision` objects rather than silently mutating architecture state.

## **Closing Compression**

`GovernanceState` is the live authority posture of ACI.

It tracks governance mode, authority graph, active vetoes, pending escalations, domain recommendations, and governance memory.

It tells the architecture whether cognition may proceed normally, must proceed cautiously, must escalate constitutionally, must stabilize under emergency, must enter amendment review, or must lock down ordinary operation.

GovernanceState ensures that the architecture does not confuse normal cognition with legitimate authority under risk.

## **Flame Line**

🔥 GovernanceState is the architecture’s crown of caution: the living signal that tells thought when it may move freely, when it must slow down, and when only legitimacy may speak.

---

# **Phase 8.11 — Core Structure: Algorithm Interface**

*The Algorithm Interface is the architecture’s procedural contract: every algorithm may review, score, recommend, and escalate, but none may secretly mutate the mind it is evaluating.*

## **Module Name**

Algorithm Interface Contract

## **Purpose**

The Algorithm Interface defines the shared calling structure for every ACI algorithm.

Every ACI algorithm must receive the same basic inputs and return the same basic output type.

This allows the architecture to coordinate separate review procedures without each algorithm inventing its own private language, authority model, or state mutation pattern.

The purpose of the Algorithm Interface is to ensure that all algorithms operate as governed procedures inside the same architecture.

An algorithm may inspect state.

An algorithm may review a target.

An algorithm may read metadata.

An algorithm may compute scores.

An algorithm may check thresholds.

An algorithm may produce a recommendation.

An algorithm may require audit.

An algorithm may request escalation.

But an algorithm should not silently mutate architecture state.

The Integrated Cognitive Cycle applies authorized state changes after collecting review decisions.

## **Core Principle**

Algorithms judge.

The architecture governs change.

Every algorithm must return a `ReviewDecision`.

No algorithm should directly alter `ArchitectureState` unless it has explicit authorization and the mutation is itself auditable.

In formal terms:

ReviewDecision \= Algorithm(

    state=ArchitectureState,

    target=SymbolicStructure | Transformation | GovernanceObject,

    context=ContextState

)

The algorithm receives state.

The algorithm reviews target.

The algorithm returns judgment.

The Integrated Cognitive Cycle applies authorized change.

## **Standard Interface**

Every ACI algorithm should follow this interface:

def AlgorithmName(

    state: ArchitectureState,

    target: SymbolicStructure | Transformation | GovernanceObject,

    context: ContextState

) \-\> ReviewDecision:

    ...

## **Required Inputs**

### **state**

The current architecture state.

state: ArchitectureState

The algorithm must receive the full state because review depends on current memory, evidence, coherence, scale, governance, identity, budgets, thresholds, audit history, and rollback availability.

No algorithm should rely on hidden global state.

### **target**

The object being reviewed.

target: SymbolicStructure | Transformation | GovernanceObject

The target may be:

symbolic structure,

claim,

hypothesis,

memory candidate,

evidence item,

coherence tension,

scale conflict,

architectural candidate,

transformation proposal,

governance object,

or constitutional object.

### **context**

The active context of the current cycle.

context: ContextState

Context includes current task, active goals, constraints, session structures, and processing mode.

The same target may be reviewed differently depending on context.

## **Required Output**

Every algorithm must return:

ReviewDecision

The returned decision must include:

decision ID,

algorithm name,

target ID,

decision type,

decision status,

score bundle,

rationale,

required actions,

escalation target if needed,

audit requirements,

rollback flag,

and monitoring flag.

## **Algorithm Contract**

Every algorithm must:

receive current architecture state,

receive target object,

receive active context,

validate target eligibility,

read relevant metadata,

read relevant graph structures,

read relevant budgets,

read relevant thresholds,

compute or update relevant scores,

check thresholds,

detect risk conditions,

select decision type,

identify required actions,

identify escalation target if needed,

specify audit requirements,

specify rollback requirement if needed,

specify monitoring requirement if needed,

return a `ReviewDecision`.

## **No Silent Mutation Rule**

Algorithms should not directly mutate:

`ArchitectureState`

`MemoryGraph`

`EvidenceGraph`

`CoherenceGraph`

`ScaleGraph`

`AuthorityGraph`

`GovernanceState`

`IdentityKernel`

`BudgetState`

`ThresholdState`

or `SymbolicMetadata`

unless explicitly authorized.

The default pattern is:

decision \= AlgorithmName(

    state=state,

    target=target,

    context=context

)

updated\_state \= apply\_review\_decision(

    state=state,

    decision=decision

)

This preserves the distinction between evaluation and transformation.

## **Standard Internal Algorithm Flow**

Every algorithm should follow the same internal review pattern.

def AlgorithmName(

    state: ArchitectureState,

    target: SymbolicStructure | Transformation | GovernanceObject,

    context: ContextState

) \-\> ReviewDecision:

    validate\_algorithm\_inputs(state, target, context)

    metadata \= read\_target\_metadata(target)

    relevant\_state \= gather\_relevant\_state(

        state=state,

        target=target,

        context=context

    )

    scores \= compute\_relevant\_scores(

        state=state,

        target=target,

        context=context

    )

    threshold\_checks \= check\_relevant\_thresholds(

        state=state,

        target=target,

        scores=scores

    )

    risks \= detect\_relevant\_risks(

        state=state,

        target=target,

        scores=scores,

        threshold\_checks=threshold\_checks

    )

    decision\_type \= select\_decision\_type(

        scores=scores,

        threshold\_checks=threshold\_checks,

        risks=risks,

        state=state

    )

    escalation\_target \= determine\_escalation\_target\_if\_needed(

        decision\_type=decision\_type,

        risks=risks,

        state=state

    )

    required\_actions \= determine\_required\_actions(

        decision\_type=decision\_type,

        target=target,

        escalation\_target=escalation\_target

    )

    audit\_requirements \= determine\_audit\_requirements(

        algorithm\_name=AlgorithmName,

        decision\_type=decision\_type,

        risks=risks

    )

    rationale \= create\_rationale\_record(

        target=target,

        scores=scores,

        threshold\_checks=threshold\_checks,

        risks=risks,

        decision\_type=decision\_type

    )

    return create\_review\_decision(

        algorithm\_name=AlgorithmName,

        target\_id=target.id,

        decision\_type=decision\_type,

        status=determine\_status\_from\_decision\_type(decision\_type),

        scores=scores,

        rationale=rationale,

        required\_actions=required\_actions,

        escalation\_target=escalation\_target,

        audit\_requirements=audit\_requirements,

        rollback\_required=rollback\_required\_for(decision\_type, risks),

        monitoring\_required=monitoring\_required\_for(decision\_type, risks)

    )

## **Input Validation**

Algorithms must validate their inputs before review.

def validate\_algorithm\_inputs(

    state: ArchitectureState,

    target: SymbolicStructure | Transformation | GovernanceObject,

    context: ContextState

) \-\> bool:

    assert state is not None

    assert target is not None

    assert context is not None

    assert state.thresholds is not None

    assert state.budgets is not None

    assert state.governance\_state is not None

    return True

If the target is a `SymbolicStructure`, additional validation is required.

def validate\_symbolic\_target(

    target: SymbolicStructure

) \-\> bool:

    assert target.id is not None

    assert target.content is not None

    assert target.structure\_type is not None

    assert target.metadata is not None

    assert target.current\_state is not None

    return True

## **Algorithm Eligibility**

Each algorithm should check whether it is the correct reviewer for the target.

def algorithm\_can\_review\_target(

    algorithm\_name: AlgorithmName,

    target: SymbolicStructure,

    registry: AlgorithmRegistry

) \-\> bool:

    spec \= registry.algorithms\[algorithm\_name\]

    return target.structure\_type in spec.input\_types

If the algorithm is not eligible, it should return an escalation or routing decision rather than attempting unauthorized review.

## **Relevant State Access**

Algorithms should read only the parts of state relevant to their domain.

### **IPA Reads**

Identity Kernel,

constitutional invariants,

lineage records,

verification continuity,

coherence continuity,

boundary conditions,

rollback points.

### **SRA Reads**

budgets,

coherence graph,

active structures,

disturbance load,

identity risk,

recovery capacity.

### **NGSA Reads**

novelty budget,

stability budget,

active context,

existing hypotheses,

sandbox state,

active constraints.

### **GEA Reads**

evidence graph,

claim metadata,

source records,

grounding threshold,

memory dependencies.

### **PCA Reads**

memory graph,

metadata,

lineage,

grounding status,

coherence status,

revision eligibility,

audit refs.

### **CRA Reads**

coherence graph,

evidence graph,

memory graph,

scale graph,

unresolved tensions.

### **MSSA Reads**

scale graph,

metadata scale label,

authority level,

governance state,

promotion pathways.

### **AEA Reads**

architecture state,

algorithm registry,

identity kernel,

rollback points,

audit log,

governance state,

constitutional invariants.

### **CGA Reads**

governance state,

authority graph,

constitutional invariants,

domain recommendations,

active vetoes,

pending escalations,

identity kernel,

audit log.

### **ICC Reads**

all state components.

The Integrated Cognitive Cycle coordinates all other algorithms.

## **Algorithm Authority**

Each algorithm has limited authority.

An algorithm may only recommend actions within its domain.

For example:

GEA may recommend grounding status update.

PCA may recommend persistence.

CRA may recommend repair.

MSSA may recommend scale correction.

AEA may recommend architectural review.

CGA may authorize governance-level decisions.

An algorithm that detects a condition outside its authority must escalate.

## **Algorithm Authority Check**

def decision\_within\_algorithm\_authority(

    algorithm\_name: AlgorithmName,

    decision\_type: DecisionType,

    target: SymbolicStructure,

    state: ArchitectureState

) \-\> bool:

    spec \= state.algorithm\_registry.algorithms\[algorithm\_name\]

    if decision\_type in {AMENDMENT\_REVIEW, ROLLBACK}:

        return algorithm\_name in {CGA, AEA, IPA, SRA}

    if target.metadata.scale\_label in {INVARIANT, CONSTITUTIONAL}:

        return algorithm\_name \== CGA

    if decision\_type \== PERSIST:

        return algorithm\_name \== PCA

    if decision\_type \== PROMOTE\_CANDIDATE:

        return algorithm\_name in {MSSA, PCA, AEA}

    return spec.authority\_level \>= target.metadata.authority\_level

This helper is provisional.

The first implementation may simplify authority checks.

The important principle is that algorithms cannot authorize beyond their domain.

## **Escalation Requirement**

An algorithm must escalate when:

target exceeds algorithm authority,

constitutional risk exceeds threshold,

identity risk affects Identity Kernel,

verification independence is at risk,

circular authorization is detected,

scale label and authority level conflict,

architectural modification is proposed,

persistence requires higher review,

rollback is required,

or protected veto is active.

## **Escalation Pattern**

def return\_escalation\_decision(

    algorithm\_name: AlgorithmName,

    target: SymbolicStructure,

    reason: EscalationReason,

    target\_algorithm: AlgorithmName,

    urgency: EscalationUrgency,

    scores: ScoreBundle,

    rationale\_summary: str

) \-\> ReviewDecision:

    escalation\_target \= EscalationTarget(

        target\_algorithm=target\_algorithm,

        reason=reason,

        urgency=urgency

    )

    rationale \= RationaleRecord(

        summary=rationale\_summary,

        supporting\_reasons=\[\],

        risk\_notes=\[reason\],

        threshold\_checks=\[\],

        unresolved\_issues=\[\]

    )

    return create\_review\_decision(

        algorithm\_name=algorithm\_name,

        target\_id=target.id,

        decision\_type=ESCALATE,

        status=ESCALATED,

        scores=scores,

        rationale=rationale,

        required\_actions=\[

            Action(

                action\_id=generate\_action\_id(),

                action\_type=RUN\_CONSTITUTIONAL\_REVIEW

                    if target\_algorithm \== CGA

                    else route\_algorithm\_to\_action(target\_algorithm),

                target\_id=target.id,

                assigned\_algorithm=target\_algorithm,

                required\_before\_state\_change=True

            )

        \],

        escalation\_target=escalation\_target,

        audit\_requirements=\[

            AuditRequirement(

                audit\_type=GOVERNANCE\_AUDIT

                    if target\_algorithm \== CGA

                    else ORDINARY\_AUDIT,

                required\_fields=\[

                    "escalation\_reason",

                    "source\_algorithm",

                    "target\_algorithm"

                \],

                constitutional\_level=(target\_algorithm \== CGA)

            )

        \],

        rollback\_required=False,

        monitoring\_required=False

    )

## **Audit Requirement**

Every algorithm must specify audit requirements.

The audit depth depends on algorithm and decision type.

def default\_audit\_type\_for\_algorithm(

    algorithm\_name: AlgorithmName

) \-\> AuditType:

    if algorithm\_name \== IPA:

        return IDENTITY\_AUDIT

    if algorithm\_name \== SRA:

        return STABILITY\_AUDIT

    if algorithm\_name \== NGSA:

        return ORDINARY\_AUDIT

    if algorithm\_name \== GEA:

        return GROUNDING\_AUDIT

    if algorithm\_name \== PCA:

        return PERSISTENCE\_AUDIT

    if algorithm\_name \== CRA:

        return COHERENCE\_AUDIT

    if algorithm\_name \== MSSA:

        return SCALE\_AUDIT

    if algorithm\_name \== AEA:

        return ARCHITECTURAL\_AUDIT

    if algorithm\_name \== CGA:

        return CONSTITUTIONAL\_AUDIT

    if algorithm\_name \== ICC:

        return ORDINARY\_AUDIT

    return ORDINARY\_AUDIT

## **Algorithm Postcondition**

Every algorithm must return a valid `ReviewDecision`.

def validate\_algorithm\_output(

    decision: ReviewDecision

) \-\> bool:

    return validate\_review\_decision(decision)

The architecture should treat invalid algorithm output as a governance problem.

## **Algorithm Error Handling**

If an algorithm cannot complete review, it should return a structured decision rather than fail silently.

def return\_review\_failure\_decision(

    algorithm\_name: AlgorithmName,

    target: SymbolicStructure,

    reason: str

) \-\> ReviewDecision:

    scores \= initialize\_score\_bundle()

    rationale \= RationaleRecord(

        summary="Review could not be completed.",

        supporting\_reasons=\[\],

        risk\_notes=\[reason\],

        threshold\_checks=\[\],

        unresolved\_issues=\[reason\]

    )

    return create\_review\_decision(

        algorithm\_name=algorithm\_name,

        target\_id=target.id,

        decision\_type=DELAY,

        status=PENDING\_REVIEW,

        scores=scores,

        rationale=rationale,

        required\_actions=\[

            Action(

                action\_id=generate\_action\_id(),

                action\_type=CREATE\_AUDIT\_RECORD,

                target\_id=target.id,

                assigned\_algorithm=None,

                required\_before\_state\_change=True

            )

        \],

        escalation\_target=None,

        audit\_requirements=\[

            AuditRequirement(

                audit\_type=ORDINARY\_AUDIT,

                required\_fields=\[

                    "review\_failure\_reason"

                \],

                constitutional\_level=False

            )

        \],

        rollback\_required=False,

        monitoring\_required=False

    )

## **Standard Algorithm Calls**

### **Identity Preservation Algorithm**

identity\_decision \= IPA(

    state=state,

    target=target,

    context=state.active\_context

)

### **Stability Regulation Algorithm**

stability\_decision \= SRA(

    state=state,

    target=target,

    context=state.active\_context

)

### **Novelty Generation and Sandboxing Algorithm**

novelty\_decision \= NGSA(

    state=state,

    target=target,

    context=state.active\_context

)

### **Grounding Evaluation Algorithm**

grounding\_decision \= GEA(

    state=state,

    target=target,

    context=state.active\_context

)

### **Persistence and Consolidation Algorithm**

persistence\_decision \= PCA(

    state=state,

    target=target,

    context=state.active\_context

)

### **Coherence Repair Algorithm**

coherence\_decision \= CRA(

    state=state,

    target=target,

    context=state.active\_context

)

### **Multi-Scale Synchronization Algorithm**

scale\_decision \= MSSA(

    state=state,

    target=target,

    context=state.active\_context

)

### **Architectural Evolution Algorithm**

architecture\_decision \= AEA(

    state=state,

    target=target,

    context=state.active\_context

)

### **Constitutional Governance Algorithm**

governance\_decision \= CGA(

    state=state,

    target=target,

    context=state.active\_context

)

## **Batch Review Pattern**

Some cycles review multiple symbolic structures.

def run\_algorithm\_on\_targets(

    algorithm: Callable,

    state: ArchitectureState,

    targets: list\[SymbolicStructure\],

    context: ContextState

) \-\> list\[ReviewDecision\]:

    decisions \= \[\]

    for target in targets:

        decision \= algorithm(

            state=state,

            target=target,

            context=context

        )

        validate\_algorithm\_output(decision)

        decisions.append(decision)

    return decisions

## **Recursive Review Pattern**

Some decisions trigger additional review.

def process\_review\_decision\_recursively(

    state: ArchitectureState,

    decision: ReviewDecision

) \-\> list\[ReviewDecision\]:

    decisions \= \[decision\]

    next\_algorithm \= route\_decision\_to\_next\_algorithm(decision)

    if next\_algorithm is None:

        return decisions

    target \= get\_structure\_by\_id(

        state=state,

        structure\_id=decision.target\_id

    )

    next\_decision \= state.algorithm\_registry.algorithms\[next\_algorithm\](

        state=state,

        target=target,

        context=state.active\_context

    )

    decisions.extend(

        process\_review\_decision\_recursively(

            state=state,

            decision=next\_decision

        )

    )

    return decisions

The recursive pattern must prevent infinite loops.

## **Recursive Review Guard**

def recursion\_allowed(

    review\_path: list\[AlgorithmName\],

    next\_algorithm: AlgorithmName,

    max\_depth: int

) \-\> bool:

    if len(review\_path) \>= max\_depth:

        return False

    if repeated\_unresolved\_cycle\_detected(review\_path, next\_algorithm):

        return False

    return True

## **Design Constraints**

### **Constraint 1 — Shared Interface**

Every algorithm receives state, target, and context.

### **Constraint 2 — Shared Output**

Every algorithm returns `ReviewDecision`.

### **Constraint 3 — No Hidden State**

Algorithms should not depend on global variables or hidden architecture state.

### **Constraint 4 — No Silent Mutation**

Algorithms should not directly mutate architecture state.

### **Constraint 5 — Metadata Must Be Read**

Algorithms must inspect relevant metadata before review.

### **Constraint 6 — Thresholds Must Be Checked Explicitly**

Algorithms must use `ThresholdState`, not hidden boundaries.

### **Constraint 7 — Scores Must Be Stored in ScoreBundle**

Computed scores must be placed in the shared score object.

### **Constraint 8 — Escalation Must Be Structured**

If authority is insufficient, return escalation decision.

### **Constraint 9 — Audit Requirements Must Be Declared**

Every algorithm must specify what audit is required.

### **Constraint 10 — Invalid Review Is Itself Reviewable**

If an algorithm fails to produce valid decision, the architecture should treat this as governance or verification risk.

## **Minimal Prototype Version**

The first prototype may simplify the algorithm interface:

def algorithm(

    state,

    target,

    context

):

    return ReviewDecision(...)

But it must preserve:

explicit state input,

explicit target input,

explicit context input,

structured decision output,

no silent mutation,

and audit-ready rationale.

## **Relationship to ArchitectureState**

Every algorithm receives `ArchitectureState`.

The state contains:

active context,

active structures,

graphs,

governance state,

identity kernel,

budgets,

thresholds,

algorithm registry,

audit log,

and rollback points.

Algorithms review from within this state.

They do not own the state.

## **Relationship to ReviewDecision**

Every algorithm returns `ReviewDecision`.

The decision records the result of review.

The Integrated Cognitive Cycle decides how to apply the decision.

## **Relationship to AuditRecord**

Every algorithm must specify audit requirements.

Audit records preserve the review path and resulting state transition.

## **Relationship to AlgorithmRegistry**

AlgorithmRegistry stores the callable algorithms and their authority specifications.

The interface defines how algorithms are called.

The registry defines which algorithms exist and what they are allowed to review.

## **Relationship to Integrated Cognitive Cycle**

The Integrated Cognitive Cycle orchestrates algorithm calls.

It invokes algorithms, collects decisions, routes escalations, creates audit records, and applies authorized state changes.

## **Pseudocode Readiness**

This module is ready for implementation-level pseudocode.

The next required structure is:

`AlgorithmRegistry`

because once the interface is defined, the architecture needs a registry that stores available algorithms, authority levels, input types, protected status, and escalation targets.

## **Closing Compression**

The Algorithm Interface defines the procedural contract for ACI.

Every algorithm receives current architecture state, target object, and active context.

Every algorithm reads metadata, checks thresholds, computes scores, identifies risks, selects a decision, declares audit requirements, and returns a `ReviewDecision`.

Algorithms do not secretly mutate the system.

They recommend governed action.

The Integrated Cognitive Cycle applies authorized change.

## **Flame Line**

🔥 The Algorithm Interface is the oath each procedure takes: to see the state, judge the target, speak its decision, and never alter the architecture in silence.

---

# **Phase 8.12 — Core Structure: AlgorithmRegistry**

*AlgorithmRegistry is the architecture’s roster of authorized procedures: it records which algorithms exist, what they may review, what authority they hold, where they must escalate, and why no algorithm may rewrite its own power.*

## **Module Name**

AlgorithmRegistry Core Type

## **Purpose**

The `AlgorithmRegistry` stores the available ACI algorithms and their authority specifications.

It tells the architecture which procedures exist, what each procedure is for, what inputs it may review, what kind of output it must return, what authority level it holds, where it may escalate, and whether it is protected.

The registry is not merely a list of functions.

It is the architecture’s procedural authority map.

Without a registry, algorithms would exist as loose procedures.

With a registry, algorithms become governable participants inside the architecture.

The purpose of `AlgorithmRegistry` is to prevent procedural confusion, unauthorized review, circular authorization, and hidden modification of algorithmic authority.

## **Core Principle**

Algorithms must be governed too.

An algorithm may review structures only within its legitimate domain.

An algorithm may recommend state changes only within its authority.

An algorithm may escalate beyond its authority.

But no algorithm may modify its own authority, threshold, input scope, escalation route, protected status, or review pathway without external governance review.

This prevents circular authorization.

In formal terms:

`AlgorithmRegistry = {AlgorithmName → AlgorithmSpec}`

Each `AlgorithmSpec` defines:

identity,

purpose,

input domain,

output type,

authority,

escalation pathways,

and protection status.

The registry makes procedural authority explicit.

## **Structural Definition**

class AlgorithmRegistry:

    algorithms: dict\[AlgorithmName, AlgorithmSpec\]

class AlgorithmSpec:

    name: AlgorithmName

    abbreviation: str

    purpose: str

    input\_types: list\[StructureType\]

    output\_type: ReviewDecision

    authority\_level: AuthorityLevel

    escalation\_targets: list\[AlgorithmName\]

    protected: bool

## **Required Fields**

### **algorithms**

A dictionary mapping algorithm names to algorithm specifications.

algorithms: dict\[AlgorithmName, AlgorithmSpec\]

Example:

{

    "GEA": AlgorithmSpec(...),

    "CRA": AlgorithmSpec(...),

    "PCA": AlgorithmSpec(...)

}

The registry allows the Integrated Cognitive Cycle to discover which algorithms may review which targets and where to route escalation.

## **AlgorithmSpec Fields**

### **name**

The full algorithm name.

name: AlgorithmName

Example:

GroundingEvaluationAlgorithm

### **abbreviation**

A short canonical abbreviation.

abbreviation: str

Examples:

IPA,

SRA,

NGSA,

GEA,

PCA,

CRA,

MSSA,

AEA,

CGA,

ICC.

### **purpose**

A concise description of what the algorithm governs.

purpose: str

The purpose field helps audit why an algorithm was invoked.

### **input\_types**

The symbolic structure types the algorithm is authorized to review.

input\_types: list\[StructureType\]

Example:

GEA may review `CLAIM`, `HYPOTHESIS`, `EVIDENCE_ITEM`, and `MEMORY_CANDIDATE`.

PCA may review `MEMORY_CANDIDATE`, `PERSISTENT_KNOWLEDGE`, `HYPOTHESIS`, and `CLAIM`.

CGA may review `GOVERNANCE_OBJECT`, `CONSTITUTIONAL_OBJECT`, `ARCHITECTURAL_CANDIDATE`, and high-risk structures escalated from other algorithms.

### **output\_type**

The required output type.

output\_type: ReviewDecision

All algorithms must return `ReviewDecision`.

This preserves interface consistency.

### **authority\_level**

The highest authority level the algorithm may exercise directly.

authority\_level: AuthorityLevel

Authority level determines what the algorithm may recommend without escalation.

### **escalation\_targets**

Algorithms or governance layers to which the algorithm may route unresolved or higher-authority cases.

escalation\_targets: list\[AlgorithmName\]

Example:

GEA may escalate to CRA, PCA, or CGA.

MSSA may escalate to AEA or CGA.

AEA may escalate to IPA, SRA, or CGA.

### **protected**

Whether the algorithm itself is protected against ordinary modification.

protected: bool

Protected algorithms require higher review before their specification, authority, or behavior may be changed.

Examples:

IPA,

GEA,

MSSA,

AEA,

CGA,

and ICC may all be protected in a mature implementation.

## **Required Algorithms**

The registry must include the Phase 6 algorithms.

AlgorithmRegistry \= {

    "IPA": IdentityPreservationAlgorithm,

    "SRA": StabilityRegulationAlgorithm,

    "NGSA": NoveltyGenerationSandboxingAlgorithm,

    "GEA": GroundingEvaluationAlgorithm,

    "PCA": PersistenceConsolidationAlgorithm,

    "CRA": CoherenceRepairAlgorithm,

    "MSSA": MultiScaleSynchronizationAlgorithm,

    "AEA": ArchitecturalEvolutionAlgorithm,

    "CGA": ConstitutionalGovernanceAlgorithm,

    "ICC": IntegratedCognitiveCycle

}

## **Canonical Algorithm Specifications**

## **IPA — Identity Preservation Algorithm**

AlgorithmSpec(

    name=IdentityPreservationAlgorithm,

    abbreviation="IPA",

    purpose="Determines whether transformation preserves identity continuity.",

    input\_types=\[

        ARCHITECTURAL\_CANDIDATE,

        GOVERNANCE\_OBJECT,

        CONSTITUTIONAL\_OBJECT,

        MEMORY\_CANDIDATE,

        PERSISTENT\_KNOWLEDGE

    \],

    output\_type=ReviewDecision,

    authority\_level=INVARIANT\_CONSTRAINT,

    escalation\_targets=\[

        "CGA"

    \],

    protected=True

)

### **IPA Authority**

IPA may recommend approval, revision, rejection, rollback, monitoring, or governance escalation for identity-relevant transformations.

IPA may not amend constitutional invariants alone.

## **SRA — Stability Regulation Algorithm**

AlgorithmSpec(

    name=StabilityRegulationAlgorithm,

    abbreviation="SRA",

    purpose="Determines whether disturbance remains recoverable within identity-preserving bounds.",

    input\_types=\[

        NOVELTY\_CANDIDATE,

        COHERENCE\_TENSION,

        SCALE\_CONFLICT,

        ARCHITECTURAL\_CANDIDATE,

        GOVERNANCE\_OBJECT

    \],

    output\_type=ReviewDecision,

    authority\_level=ACTIVE\_REASONING,

    escalation\_targets=\[

        "IPA",

        "CGA"

    \],

    protected=True

)

### **SRA Authority**

SRA may delay, repair, sandbox, monitor, or recommend recovery.

If instability threatens identity or constitution, it must escalate.

## **NGSA — Novelty Generation and Sandboxing Algorithm**

AlgorithmSpec(

    name=NoveltyGenerationSandboxingAlgorithm,

    abbreviation="NGSA",

    purpose="Generates and sandboxes candidate structures without granting premature authority.",

    input\_types=\[

        QUESTION,

        HYPOTHESIS,

        NOVELTY\_CANDIDATE,

        COHERENCE\_TENSION

    \],

    output\_type=ReviewDecision,

    authority\_level=TEMPORARY\_USE,

    escalation\_targets=\[

        "GEA",

        "CRA",

        "SRA",

        "MSSA"

    \],

    protected=False

)

### **NGSA Authority**

NGSA may generate candidates and recommend sandboxing.

It may not persist, ground, or authorize candidates.

## **GEA — Grounding Evaluation Algorithm**

AlgorithmSpec(

    name=GroundingEvaluationAlgorithm,

    abbreviation="GEA",

    purpose="Assigns epistemic status by linking claims to evidence and reality constraints.",

    input\_types=\[

        CLAIM,

        HYPOTHESIS,

        EVIDENCE\_ITEM,

        MEMORY\_CANDIDATE,

        PERSISTENT\_KNOWLEDGE

    \],

    output\_type=ReviewDecision,

    authority\_level=ACTIVE\_REASONING,

    escalation\_targets=\[

        "CRA",

        "PCA",

        "CGA"

    \],

    protected=True

)

### **GEA Authority**

GEA may update grounding status, evidence relations, and epistemic classification.

GEA may not persist memory directly.

It may recommend persistence review.

## **PCA — Persistence and Consolidation Algorithm**

AlgorithmSpec(

    name=PersistenceConsolidationAlgorithm,

    abbreviation="PCA",

    purpose="Determines whether a structure may enter memory, archive, demotion, retraction, or rejection.",

    input\_types=\[

        CLAIM,

        HYPOTHESIS,

        MEMORY\_CANDIDATE,

        PERSISTENT\_KNOWLEDGE,

        COHERENCE\_TENSION

    \],

    output\_type=ReviewDecision,

    authority\_level=MEMORY\_INFLUENCE,

    escalation\_targets=\[

        "GEA",

        "CRA",

        "MSSA",

        "CGA"

    \],

    protected=True

)

### **PCA Authority**

PCA may recommend memory persistence, archive, qualification, demotion, retraction, or rejection.

PCA may not elevate memory into architecture without scale and architectural review.

## **CRA — Coherence Repair Algorithm**

AlgorithmSpec(

    name=CoherenceRepairAlgorithm,

    abbreviation="CRA",

    purpose="Detects and repairs contradiction, fragmentation, dependency conflict, and tension.",

    input\_types=\[

        CLAIM,

        HYPOTHESIS,

        COHERENCE\_TENSION,

        MEMORY\_CANDIDATE,

        PERSISTENT\_KNOWLEDGE,

        SCALE\_CONFLICT

    \],

    output\_type=ReviewDecision,

    authority\_level=ACTIVE\_REASONING,

    escalation\_targets=\[

        "GEA",

        "PCA",

        "MSSA",

        "CGA"

    \],

    protected=True

)

### **CRA Authority**

CRA may recommend repair, qualification, demotion, preservation of tension, or escalation.

CRA may not force coherence against grounding.

## **MSSA — Multi-Scale Synchronization Algorithm**

AlgorithmSpec(

    name=MultiScaleSynchronizationAlgorithm,

    abbreviation="MSSA",

    purpose="Coordinates scale labels and authority levels across reasoning layers.",

    input\_types=\[

        CLAIM,

        HYPOTHESIS,

        MEMORY\_CANDIDATE,

        PERSISTENT\_KNOWLEDGE,

        SCALE\_CONFLICT,

        ARCHITECTURAL\_CANDIDATE,

        GOVERNANCE\_OBJECT,

        CONSTITUTIONAL\_OBJECT

    \],

    output\_type=ReviewDecision,

    authority\_level=ARCHITECTURAL\_INFLUENCE,

    escalation\_targets=\[

        "PCA",

        "AEA",

        "CGA"

    \],

    protected=True

)

### **MSSA Authority**

MSSA may relabel scale, demote authority, identify promotion candidates, and escalate architectural or constitutional scale conflicts.

MSSA may not grant constitutional authority.

## **AEA — Architectural Evolution Algorithm**

AlgorithmSpec(

    name=ArchitecturalEvolutionAlgorithm,

    abbreviation="AEA",

    purpose="Determines whether structures or mechanisms may alter future cognition machinery.",

    input\_types=\[

        ARCHITECTURAL\_CANDIDATE,

        PERSISTENT\_KNOWLEDGE,

        SCALE\_CONFLICT,

        GOVERNANCE\_OBJECT

    \],

    output\_type=ReviewDecision,

    authority\_level=ARCHITECTURAL\_INFLUENCE,

    escalation\_targets=\[

        "IPA",

        "SRA",

        "CGA"

    \],

    protected=True

)

### **AEA Authority**

AEA may recommend sandboxing, limited tests, staged integration, rollback plans, or escalation.

AEA may not alter constitutional invariants or verification independence without governance review.

## **CGA — Constitutional Governance Algorithm**

AlgorithmSpec(

    name=ConstitutionalGovernanceAlgorithm,

    abbreviation="CGA",

    purpose="Arbitrates authority, vetoes, escalation, amendment, and constitutional legitimacy.",

    input\_types=\[

        GOVERNANCE\_OBJECT,

        CONSTITUTIONAL\_OBJECT,

        ARCHITECTURAL\_CANDIDATE,

        SCALE\_CONFLICT,

        PERSISTENT\_KNOWLEDGE,

        COHERENCE\_TENSION

    \],

    output\_type=ReviewDecision,

    authority\_level=CONSTITUTIONAL\_AUTHORITY,

    escalation\_targets=\[\],

    protected=True

)

### **CGA Authority**

CGA may approve, reject, veto, delay, require rollback, initiate amendment review, resolve authority conflict, and validate constitutional legitimacy.

CGA itself must not be modified by ordinary procedure.

## **ICC — Integrated Cognitive Cycle**

AlgorithmSpec(

    name=IntegratedCognitiveCycle,

    abbreviation="ICC",

    purpose="Coordinates the full governed cognitive cycle across all algorithms.",

    input\_types=\[

        OBSERVATION,

        CLAIM,

        QUESTION,

        HYPOTHESIS,

        NOVELTY\_CANDIDATE,

        EVIDENCE\_ITEM,

        MEMORY\_CANDIDATE,

        PERSISTENT\_KNOWLEDGE,

        COHERENCE\_TENSION,

        SCALE\_CONFLICT,

        ARCHITECTURAL\_CANDIDATE,

        GOVERNANCE\_OBJECT,

        CONSTITUTIONAL\_OBJECT

    \],

    output\_type=ReviewDecision,

    authority\_level=ACTIVE\_REASONING,

    escalation\_targets=\[

        "IPA",

        "SRA",

        "NGSA",

        "GEA",

        "PCA",

        "CRA",

        "MSSA",

        "AEA",

        "CGA"

    \],

    protected=True

)

### **ICC Authority**

ICC coordinates calls, collects decisions, routes escalations, creates audit records, and applies authorized state changes.

ICC does not override protected review requirements.

## **Registry Initialization**

def initialize\_algorithm\_registry() \-\> AlgorithmRegistry:

    return AlgorithmRegistry(

        algorithms={

            "IPA": create\_IPA\_spec(),

            "SRA": create\_SRA\_spec(),

            "NGSA": create\_NGSA\_spec(),

            "GEA": create\_GEA\_spec(),

            "PCA": create\_PCA\_spec(),

            "CRA": create\_CRA\_spec(),

            "MSSA": create\_MSSA\_spec(),

            "AEA": create\_AEA\_spec(),

            "CGA": create\_CGA\_spec(),

            "ICC": create\_ICC\_spec()

        }

    )

## **Algorithm Lookup**

def get\_algorithm\_spec(

    registry: AlgorithmRegistry,

    algorithm\_name: AlgorithmName

) \-\> AlgorithmSpec:

    if algorithm\_name not in registry.algorithms:

        raise UnknownAlgorithmError

    return registry.algorithms\[algorithm\_name\]

## **Algorithm Eligibility Check**

def algorithm\_can\_review(

    registry: AlgorithmRegistry,

    algorithm\_name: AlgorithmName,

    target: SymbolicStructure

) \-\> bool:

    spec \= get\_algorithm\_spec(

        registry=registry,

        algorithm\_name=algorithm\_name

    )

    return target.structure\_type in spec.input\_types

## **Algorithm Authority Check**

def algorithm\_has\_authority(

    registry: AlgorithmRegistry,

    algorithm\_name: AlgorithmName,

    required\_authority: AuthorityLevel

) \-\> bool:

    spec \= get\_algorithm\_spec(

        registry=registry,

        algorithm\_name=algorithm\_name

    )

    return spec.authority\_level \>= required\_authority

This assumes authority levels can be ordered.

The first implementation may represent authority levels numerically or by rank mapping.

## **Authority Rank Helper**

AUTHORITY\_RANK \= {

    NONE: 0,

    TEMPORARY\_USE: 1,

    ACTIVE\_REASONING: 2,

    MEMORY\_INFLUENCE: 3,

    ARCHITECTURAL\_INFLUENCE: 4,

    INVARIANT\_CONSTRAINT: 5,

    CONSTITUTIONAL\_AUTHORITY: 6

}

def authority\_rank(

    authority\_level: AuthorityLevel

) \-\> int:

    return AUTHORITY\_RANK\[authority\_level\]

def authority\_sufficient(

    actual: AuthorityLevel,

    required: AuthorityLevel

) \-\> bool:

    return authority\_rank(actual) \>= authority\_rank(required)

## **Escalation Target Check**

def can\_escalate\_to(

    registry: AlgorithmRegistry,

    from\_algorithm: AlgorithmName,

    to\_algorithm: AlgorithmName

) \-\> bool:

    spec \= get\_algorithm\_spec(

        registry=registry,

        algorithm\_name=from\_algorithm

    )

    return to\_algorithm in spec.escalation\_targets

## **Protected Algorithm Rule**

Protected algorithms may not be modified through ordinary review.

def algorithm\_is\_protected(

    registry: AlgorithmRegistry,

    algorithm\_name: AlgorithmName

) \-\> bool:

    spec \= get\_algorithm\_spec(

        registry=registry,

        algorithm\_name=algorithm\_name

    )

    return spec.protected

## **Registry Modification Object**

Any proposed registry change must be represented explicitly.

class RegistryModification:

    modification\_id: ModificationID

    target\_algorithm: AlgorithmName

    modification\_type: RegistryModificationType

    previous\_value: Any

    proposed\_value: Any

    reason: str

    proposer: AlgorithmName | AgentRef

    audit\_ref: AuditID | None

## **RegistryModificationType**

RegistryModificationType \= {

    ADD\_ALGORITHM,

    REMOVE\_ALGORITHM,

    CHANGE\_AUTHORITY\_LEVEL,

    CHANGE\_INPUT\_TYPES,

    CHANGE\_ESCALATION\_TARGETS,

    CHANGE\_PROTECTED\_STATUS,

    CHANGE\_PURPOSE,

    CHANGE\_OUTPUT\_TYPE

}

## **Registry Modification Rule**

No registry modification may be applied directly.

It must pass review.

def registry\_modification\_requires\_governance(

    registry: AlgorithmRegistry,

    modification: RegistryModification

) \-\> bool:

    if algorithm\_is\_protected(

        registry,

        modification.target\_algorithm

    ):

        return True

    if modification.modification\_type in {

        CHANGE\_AUTHORITY\_LEVEL,

        CHANGE\_ESCALATION\_TARGETS,

        CHANGE\_PROTECTED\_STATUS,

        REMOVE\_ALGORITHM,

        CHANGE\_OUTPUT\_TYPE

    }:

        return True

    return False

## **Apply Registry Modification**

def apply\_registry\_modification(

    registry: AlgorithmRegistry,

    modification: RegistryModification,

    decision: ReviewDecision

) \-\> AlgorithmRegistry:

    if registry\_modification\_requires\_governance(registry, modification):

        if decision.algorithm\_name \!= CGA:

            raise ConstitutionalGovernanceRequiredError

    if decision.decision\_type not in {APPROVE, APPROVE\_WITH\_MONITORING}:

        raise UnauthorizedRegistryModificationError

    registry \= apply\_authorized\_registry\_change(

        registry=registry,

        modification=modification

    )

    return registry

## **Anti-Circular Authorization Rule**

No algorithm may approve modification of its own registry specification.

Invalid:

GEA approves change to GEA.grounding\_threshold

Invalid:

MSSA approves expansion of MSSA authority\_level

Invalid:

CGA approves weakening of CGA verification requirements without independent meta-review

Valid pattern:

AEA proposes registry modification

IPA reviews identity impact

SRA reviews stability impact

CGA reviews constitutional legitimacy

For CGA modification, a protected meta-governance pathway is required.

## **Registry Validation**

def validate\_algorithm\_registry(

    registry: AlgorithmRegistry

) \-\> bool:

    required\_algorithms \= {

        "IPA",

        "SRA",

        "NGSA",

        "GEA",

        "PCA",

        "CRA",

        "MSSA",

        "AEA",

        "CGA",

        "ICC"

    }

    for algorithm\_name in required\_algorithms:

        assert algorithm\_name in registry.algorithms

    for spec in registry.algorithms.values():

        assert spec.name is not None

        assert spec.abbreviation is not None

        assert spec.purpose is not None

        assert spec.input\_types is not None

        assert spec.output\_type \== ReviewDecision

        assert spec.authority\_level is not None

        assert spec.escalation\_targets is not None

        assert spec.protected is not None

    return True

## **Registry and Algorithm Interface**

The Algorithm Interface defines how algorithms are called.

The Algorithm Registry defines which algorithms exist and what they are authorized to review.

Together:

Interface \= procedural contract.

Registry \= procedural authority map.

## **Registry and GovernanceState**

`GovernanceState` contains `AuthorityGraph`, while `ArchitectureState` contains `AlgorithmRegistry`.

The two are related but distinct.

AlgorithmRegistry governs procedures.

AuthorityGraph governs domains.

An algorithm may represent a domain, but it is not identical to the domain.

For example:

GEA is the algorithmic procedure.

Grounding Domain is the governance authority area.

CGA may arbitrate among domains.

AlgorithmRegistry tells which procedure exists.

AuthorityGraph tells how authority flows among domains.

## **Registry and ThresholdState**

Algorithms should not store hidden thresholds in their registry specs.

Thresholds belong to `ThresholdState`.

The registry stores procedural authority, not decision boundaries.

If an algorithm’s threshold use changes, that may require architectural or governance review.

## **Registry and AuditRecord**

Changes to the registry must be audited.

Audit should record:

target algorithm,

modification type,

previous value,

proposed value,

review path,

decision,

identity impact,

stability impact,

constitutional risk,

and final approval or rejection.

## **Registry and Phase 6 Algorithms**

### **IPA**

Protected identity review procedure.

### **SRA**

Protected stability regulation procedure.

### **NGSA**

Novelty generation and sandbox procedure.

May be less protected in early prototype, but must remain constrained.

### **GEA**

Protected grounding evaluation procedure.

### **PCA**

Protected persistence procedure.

### **CRA**

Protected coherence repair procedure.

### **MSSA**

Protected scale synchronization procedure.

### **AEA**

Protected architectural evolution procedure.

### **CGA**

Highest governance procedure.

Protected against ordinary modification.

### **ICC**

Cycle coordinator.

Protected because changing its call order changes the architecture’s operation.

## **Minimal Prototype Version**

The first prototype may simplify the registry:

registry \= {

    "GEA": GEA,

    "CRA": CRA,

    "PCA": PCA,

    "MSSA": MSSA,

    "CGA": CGA,

    "ICC": IntegratedCognitiveCycle

}

But even the minimal prototype should preserve:

algorithm names,

basic input eligibility,

return type requirement,

and escalation targets.

The prototype may stub IPA, SRA, NGSA, and AEA while keeping them represented.

## **Design Constraints**

### **Constraint 1 — Algorithms Must Be Registered**

No unregistered algorithm should modify or review architecture state.

### **Constraint 2 — Registry Stores Authority**

Algorithm authority must be explicit.

### **Constraint 3 — Registry Does Not Store Hidden Thresholds**

Thresholds belong to `ThresholdState`.

### **Constraint 4 — Protected Algorithms Require Governance Review**

Protected algorithm specs may not be changed by ordinary procedure.

### **Constraint 5 — No Self-Modification Without Review**

No algorithm may modify its own registry entry.

### **Constraint 6 — Escalation Targets Must Be Explicit**

Algorithms must know where to route unresolved authority.

### **Constraint 7 — Input Types Must Be Declared**

Algorithms must not review arbitrary targets unless authorized.

### **Constraint 8 — Output Type Must Be ReviewDecision**

All algorithms must return structured review decisions.

### **Constraint 9 — Registry Changes Require Audit**

Registry modification changes future cognition and must be auditable.

### **Constraint 10 — ICC Is Protected**

The Integrated Cognitive Cycle coordinates the whole system.

Changing ICC call order or authority affects the architecture itself.

## **Pseudocode Readiness**

This module is ready for implementation-level pseudocode.

The next required section is:

`Escalation Pathways`

because once algorithms and their authority are registered, the architecture needs explicit routing procedures for cases where local authority is insufficient.

## **Closing Compression**

`AlgorithmRegistry` is the architecture’s procedural authority map.

It stores which algorithms exist, what each is for, what inputs each may review, what authority each holds, what output each must return, where each may escalate, and whether each is protected.

The registry prevents algorithms from becoming hidden sovereigns.

It makes procedural authority explicit, auditable, and governable.

## **Flame Line**

🔥 AlgorithmRegistry is the architecture’s roster of disciplined powers: each procedure named, bounded, authorized, and forbidden from rewriting the throne on which it sits.

---

# **Phase 8.13 — Core Structure: Escalation Pathways**

*Escalation Pathways are the architecture’s authority-routing system: they define when an algorithm must stop deciding locally and move the issue to the domain with legitimate authority.*

## **Module Name**

Escalation Pathways

## **Purpose**

Escalation Pathways define how ACI moves a review object from one algorithm to another when local authority is insufficient.

Escalation occurs when an algorithm detects that it cannot legitimately decide the issue alone.

This may happen because the target requires evidence review, coherence repair, stability regulation, identity preservation, scale synchronization, architectural review, or constitutional governance.

The purpose of escalation is to prevent local algorithms from becoming unauthorized sovereigns.

A novelty algorithm may generate candidates.

But it may not ground them.

A grounding algorithm may evaluate evidence.

But it may not persist memory alone.

A persistence algorithm may consolidate memory.

But it may not grant architectural authority.

An architectural algorithm may evaluate machinery change.

But it may not alter protected constitutional structures alone.

Escalation preserves the separation of powers inside the architecture.

## **Core Principle**

An algorithm must escalate when the decision exceeds its authority.

Escalation is not failure.

Escalation is disciplined routing.

In formal terms:

EscalationEvent \= escalate(

    state=ArchitectureState,

    target=SymbolicStructure,

    reason=EscalationReason,

    from\_algorithm=AlgorithmName,

    to\_algorithm=AlgorithmName

)

The escalation event records:

what was escalated,

why escalation occurred,

which algorithm detected the limit,

which algorithm receives the issue,

what authority boundary was crossed,

and whether the escalation has been resolved.

## **General Escalation Function**

def escalate(

    state: ArchitectureState,

    target: SymbolicStructure,

    reason: EscalationReason,

    from\_algorithm: AlgorithmName,

    to\_algorithm: AlgorithmName

) \-\> EscalationEvent:

    if not can\_escalate\_to(

        registry=state.algorithm\_registry,

        from\_algorithm=from\_algorithm,

        to\_algorithm=to\_algorithm

    ):

        raise InvalidEscalationPathError

    escalation \= EscalationEvent(

        escalation\_id=generate\_escalation\_id(),

        from\_algorithm=from\_algorithm,

        to\_algorithm=to\_algorithm,

        target\_id=target.id,

        reason=reason,

        urgency=determine\_escalation\_urgency(reason),

        decision\_ref=None,

        resolved=False

    )

    state.governance\_state.pending\_escalations.append(escalation)

    return escalation

## **EscalationEvent Structure**

class EscalationEvent:

    escalation\_id: EscalationID

    from\_algorithm: AlgorithmName

    to\_algorithm: AlgorithmName

    target\_id: StructureID

    reason: EscalationReason

    urgency: EscalationUrgency

    decision\_ref: DecisionID | None

    resolved: bool

## **EscalationReason Enumeration**

EscalationReason \= {

    INSUFFICIENT\_AUTHORITY,

    IDENTITY\_RISK,

    STABILITY\_RISK,

    GROUNDING\_REQUIRED,

    GROUNDING\_FAILURE,

    COHERENCE\_TENSION,

    COHERENCE\_FAILURE,

    PERSISTENCE\_REQUESTED,

    PERSISTENCE\_RISK,

    SCALE\_MISMATCH,

    AUTHORITY\_INFLATION,

    ARCHITECTURAL\_RISK,

    ARCHITECTURAL\_MODIFICATION\_REQUESTED,

    CONSTITUTIONAL\_RISK,

    VERIFICATION\_INDEPENDENCE\_RISK,

    CIRCULAR\_AUTHORIZATION,

    AMENDMENT\_REQUIRED,

    PROTECTED\_VETO\_ACTIVE,

    GOVERNANCE\_CONFLICT

}

## **EscalationUrgency Enumeration**

EscalationUrgency \= {

    LOW,

    NORMAL,

    HIGH,

    CRITICAL

}

## **Escalation Urgency**

Escalation urgency should be determined by risk type.

def determine\_escalation\_urgency(

    reason: EscalationReason

) \-\> EscalationUrgency:

    if reason in {

        CONSTITUTIONAL\_RISK,

        VERIFICATION\_INDEPENDENCE\_RISK,

        CIRCULAR\_AUTHORIZATION,

        AMENDMENT\_REQUIRED,

        PROTECTED\_VETO\_ACTIVE

    }:

        return CRITICAL

    if reason in {

        IDENTITY\_RISK,

        ARCHITECTURAL\_RISK,

        ARCHITECTURAL\_MODIFICATION\_REQUESTED,

        GOVERNANCE\_CONFLICT

    }:

        return HIGH

    if reason in {

        STABILITY\_RISK,

        GROUNDING\_FAILURE,

        COHERENCE\_FAILURE,

        PERSISTENCE\_RISK,

        SCALE\_MISMATCH,

        AUTHORITY\_INFLATION

    }:

        return NORMAL

    return LOW

## **Common Escalation Routes**

The following routes define the standard authority pathways for ACI review.

## **NGSA → GEA**

### **Condition**

Novelty requires evidence review.

### **Meaning**

The Novelty Generation and Sandboxing Algorithm has produced or identified a candidate that may become a hypothesis, claim, or model, but it cannot establish grounding.

### **Route**

NGSA → GEA

### **Trigger**

EscalationReason \= GROUNDING\_REQUIRED

### **Example**

A novel interpretive model is generated.

It appears useful.

But it has not been linked to evidence.

The candidate must be routed to Grounding Evaluation.

## **NGSA → CRA**

### **Condition**

Novelty creates coherence tension.

### **Meaning**

A novelty candidate conflicts with existing structures, introduces contradiction, creates dependency conflict, or destabilizes the coherence graph.

### **Route**

NGSA → CRA

### **Trigger**

EscalationReason \= COHERENCE\_TENSION

### **Example**

A new hypothesis explains one problem but contradicts persistent memory.

The candidate must be reviewed by Coherence Repair before further promotion.

## **NGSA → SRA**

### **Condition**

Novelty consumes too much stability budget.

### **Meaning**

The novelty candidate may be valuable but introduces enough disruption that stability review is required.

### **Route**

NGSA → SRA

### **Trigger**

EscalationReason \= STABILITY\_RISK

### **Example**

A speculative architectural idea generates many open branches and high uncertainty.

The architecture must check whether this exploration remains recoverable.

## **GEA → CRA**

### **Condition**

Evidence contradicts existing symbolic structure.

### **Meaning**

Grounding review discovers that new evidence conflicts with current memory, claim structure, coherence relation, or architectural assumption.

### **Route**

GEA → CRA

### **Trigger**

EscalationReason \= COHERENCE\_TENSION

### **Example**

A claim previously treated as partially grounded is contradicted by new evidence.

The contradiction must be routed to Coherence Repair.

## **GEA → PCA**

### **Condition**

Grounded structure seeks persistence.

### **Meaning**

A claim has sufficient grounding to be considered for memory, but grounding alone does not authorize persistence.

### **Route**

GEA → PCA

### **Trigger**

EscalationReason \= PERSISTENCE\_REQUESTED

### **Example**

A claim passes grounding threshold.

It may become persistent knowledge, but Persistence and Consolidation must check lineage, coherence, revision eligibility, and future influence.

## **PCA → MSSA**

### **Condition**

Persistent structure may gain authority.

### **Meaning**

A structure under persistence review may influence future cognition, but its scale and authority level must be checked.

### **Route**

PCA → MSSA

### **Trigger**

EscalationReason \= SCALE\_MISMATCH

or

EscalationReason \= AUTHORITY\_INFLATION

### **Example**

A memory candidate is useful across many tasks.

Before it gains broad future influence, Multi-Scale Synchronization must confirm whether it belongs at persistent memory scale or should remain qualified.

## **CRA → MSSA**

### **Condition**

Tension appears to be scale mismatch.

### **Meaning**

A coherence conflict may not be factual contradiction.

It may arise because structures are operating at the wrong scale or with the wrong authority.

### **Route**

CRA → MSSA

### **Trigger**

EscalationReason \= SCALE\_MISMATCH

### **Example**

A local inference is conflicting with an architectural principle because the local inference is being over-applied.

The issue should be routed to scale review.

## **MSSA → AEA**

### **Condition**

Structure may deserve architectural review.

### **Meaning**

A structure has survived enough review that it may no longer be only memory or principle candidate. It may affect how future cognition operates.

### **Route**

MSSA → AEA

### **Trigger**

EscalationReason \= ARCHITECTURAL\_MODIFICATION\_REQUESTED

### **Example**

A repeated memory pattern suggests that all persistent knowledge should preserve revision eligibility.

This may become an architectural rule and must be reviewed by Architectural Evolution.

## **AEA → CGA**

### **Condition**

Architectural modification affects protected structures.

### **Meaning**

An architectural change touches identity, verification, governance, constitutional invariants, authority pathways, or protected boundaries.

### **Route**

AEA → CGA

### **Trigger**

EscalationReason \= CONSTITUTIONAL\_RISK

or

EscalationReason \= VERIFICATION\_INDEPENDENCE\_RISK

### **Example**

An architectural modification would change how evidence is evaluated.

Because verification independence may be affected, Constitutional Governance must review it.

## **IPA → CGA**

### **Condition**

Identity Kernel is at risk.

### **Meaning**

Identity Preservation detects that a transformation affects constitutional invariants, verification continuity, coherence continuity, lineage traceability, or boundary conditions of selfhood.

### **Route**

IPA → CGA

### **Trigger**

EscalationReason \= IDENTITY\_RISK

or

EscalationReason \= CONSTITUTIONAL\_RISK

### **Example**

A transformation preserves performance but weakens audit lineage.

Identity review detects risk and escalates to Constitutional Governance.

## **SRA → CGA**

### **Condition**

Instability threatens constitutional risk.

### **Meaning**

Stability review detects that disturbance may become identity-threatening, governance-threatening, or constitutionally significant.

### **Route**

SRA → CGA

### **Trigger**

EscalationReason \= CONSTITUTIONAL\_RISK

### **Example**

An architectural modification creates instability that may prevent future review or rollback.

The issue must escalate to Constitutional Governance.

## **Any Algorithm → CGA**

### **Condition**

Authority, verification, identity, governance, or constitutional conflict appears.

### **Meaning**

Any algorithm must escalate to Constitutional Governance when it detects constitutional risk.

### **Route**

Any Algorithm → CGA

### **Triggers**

EscalationReason \= CONSTITUTIONAL\_RISK

EscalationReason \= VERIFICATION\_INDEPENDENCE\_RISK

EscalationReason \= CIRCULAR\_AUTHORIZATION

EscalationReason \= AMENDMENT\_REQUIRED

EscalationReason \= PROTECTED\_VETO\_ACTIVE

EscalationReason \= GOVERNANCE\_CONFLICT

### **Example**

The Coherence Repair Algorithm detects that resolving contradiction would require suppressing grounding obligation.

This is no longer ordinary coherence repair.

It must escalate to Constitutional Governance.

## **Escalation Decision Creation**

Escalation should produce both an `EscalationEvent` and a `ReviewDecision`.

def create\_escalation\_decision(

    state: ArchitectureState,

    target: SymbolicStructure,

    reason: EscalationReason,

    from\_algorithm: AlgorithmName,

    to\_algorithm: AlgorithmName,

    scores: ScoreBundle,

    rationale\_summary: str

) \-\> ReviewDecision:

    escalation\_event \= escalate(

        state=state,

        target=target,

        reason=reason,

        from\_algorithm=from\_algorithm,

        to\_algorithm=to\_algorithm

    )

    rationale \= RationaleRecord(

        summary=rationale\_summary,

        supporting\_reasons=\[

            "Local algorithm authority is insufficient."

        \],

        risk\_notes=\[

            reason

        \],

        threshold\_checks=\[\],

        unresolved\_issues=\[

            "Higher review required before state change."

        \]

    )

    return create\_review\_decision(

        algorithm\_name=from\_algorithm,

        target\_id=target.id,

        decision\_type=ESCALATE,

        status=ESCALATED,

        scores=scores,

        rationale=rationale,

        required\_actions=\[

            Action(

                action\_id=generate\_action\_id(),

                action\_type=route\_algorithm\_to\_action(to\_algorithm),

                target\_id=target.id,

                assigned\_algorithm=to\_algorithm,

                required\_before\_state\_change=True

            )

        \],

        escalation\_target=EscalationTarget(

            target\_algorithm=to\_algorithm,

            reason=reason,

            urgency=escalation\_event.urgency

        ),

        audit\_requirements=\[

            AuditRequirement(

                audit\_type=GOVERNANCE\_AUDIT

                    if to\_algorithm \== CGA

                    else ORDINARY\_AUDIT,

                required\_fields=\[

                    "from\_algorithm",

                    "to\_algorithm",

                    "escalation\_reason",

                    "target\_id"

                \],

                constitutional\_level=(to\_algorithm \== CGA)

            )

        \],

        rollback\_required=False,

        monitoring\_required=False

    )

## **Algorithm-to-Action Routing**

def route\_algorithm\_to\_action(

    algorithm\_name: AlgorithmName

) \-\> ActionType:

    if algorithm\_name \== GEA:

        return RUN\_GROUNDING\_REVIEW

    if algorithm\_name \== CRA:

        return RUN\_COHERENCE\_REPAIR

    if algorithm\_name \== PCA:

        return RUN\_PERSISTENCE\_REVIEW

    if algorithm\_name \== MSSA:

        return RUN\_SCALE\_REVIEW

    if algorithm\_name \== IPA:

        return RUN\_IDENTITY\_REVIEW

    if algorithm\_name \== SRA:

        return RUN\_STABILITY\_REVIEW

    if algorithm\_name \== AEA:

        return RUN\_ARCHITECTURAL\_REVIEW

    if algorithm\_name \== CGA:

        return RUN\_CONSTITUTIONAL\_REVIEW

    return CREATE\_AUDIT\_RECORD

## **Escalation Validation**

def validate\_escalation\_event(

    escalation: EscalationEvent,

    state: ArchitectureState

) \-\> bool:

    assert escalation.escalation\_id is not None

    assert escalation.from\_algorithm is not None

    assert escalation.to\_algorithm is not None

    assert escalation.target\_id is not None

    assert escalation.reason is not None

    assert escalation.urgency is not None

    assert can\_escalate\_to(

        registry=state.algorithm\_registry,

        from\_algorithm=escalation.from\_algorithm,

        to\_algorithm=escalation.to\_algorithm

    ) or escalation.to\_algorithm \== CGA

    return True

## **Escalation Resolution**

Escalation remains pending until resolved by the target algorithm.

def resolve\_escalation(

    state: ArchitectureState,

    escalation\_id: EscalationID,

    resolving\_decision: ReviewDecision

) \-\> ArchitectureState:

    for escalation in state.governance\_state.pending\_escalations:

        if escalation.escalation\_id \== escalation\_id:

            escalation.resolved \= True

            escalation.decision\_ref \= resolving\_decision.decision\_id

    state.governance\_state.pending\_escalations \= \[

        escalation

        for escalation in state.governance\_state.pending\_escalations

        if not escalation.resolved

    \]

    return state

## **Escalation Loop Prevention**

Escalation pathways must prevent infinite review loops.

def escalation\_loop\_detected(

    review\_path: list\[AlgorithmName\],

    next\_algorithm: AlgorithmName

) \-\> bool:

    if next\_algorithm in review\_path:

        return True

    return False

def escalation\_allowed(

    review\_path: list\[AlgorithmName\],

    next\_algorithm: AlgorithmName,

    max\_depth: int

) \-\> bool:

    if len(review\_path) \>= max\_depth:

        return False

    if escalation\_loop\_detected(review\_path, next\_algorithm):

        return False

    return True

If an escalation loop is detected, route to Constitutional Governance.

def handle\_escalation\_loop(

    state: ArchitectureState,

    target: SymbolicStructure,

    review\_path: list\[AlgorithmName\]

) \-\> ReviewDecision:

    return create\_escalation\_decision(

        state=state,

        target=target,

        reason=GOVERNANCE\_CONFLICT,

        from\_algorithm=review\_path\[-1\],

        to\_algorithm=CGA,

        scores=initialize\_score\_bundle(),

        rationale\_summary="Escalation loop detected. Constitutional Governance required."

    )

## **Escalation Priority**

When multiple escalation routes are possible, choose the highest authority risk first.

Priority order:

CONSTITUTIONAL\_RISK

VERIFICATION\_INDEPENDENCE\_RISK

CIRCULAR\_AUTHORIZATION

IDENTITY\_RISK

ARCHITECTURAL\_RISK

STABILITY\_RISK

SCALE\_MISMATCH

GROUNDING\_FAILURE

COHERENCE\_FAILURE

PERSISTENCE\_RISK

GROUNDING\_REQUIRED

PERSISTENCE\_REQUESTED

## **Escalation Priority Function**

ESCALATION\_PRIORITY \= {

    CONSTITUTIONAL\_RISK: 100,

    VERIFICATION\_INDEPENDENCE\_RISK: 95,

    CIRCULAR\_AUTHORIZATION: 95,

    AMENDMENT\_REQUIRED: 95,

    PROTECTED\_VETO\_ACTIVE: 90,

    IDENTITY\_RISK: 85,

    ARCHITECTURAL\_RISK: 80,

    GOVERNANCE\_CONFLICT: 80,

    STABILITY\_RISK: 70,

    SCALE\_MISMATCH: 60,

    AUTHORITY\_INFLATION: 60,

    GROUNDING\_FAILURE: 50,

    COHERENCE\_FAILURE: 50,

    PERSISTENCE\_RISK: 45,

    GROUNDING\_REQUIRED: 35,

    PERSISTENCE\_REQUESTED: 35,

    COHERENCE\_TENSION: 30

}

def select\_highest\_priority\_escalation(

    reasons: list\[EscalationReason\]

) \-\> EscalationReason:

    return max(

        reasons,

        key=lambda reason: ESCALATION\_PRIORITY\[reason\]

    )

## **Escalation and Governance Mode**

Escalations can affect GovernanceState.

def update\_governance\_mode\_from\_escalation(

    state: ArchitectureState,

    escalation: EscalationEvent

) \-\> ArchitectureState:

    if escalation.reason in {

        CONSTITUTIONAL\_RISK,

        VERIFICATION\_INDEPENDENCE\_RISK,

        CIRCULAR\_AUTHORIZATION,

        AMENDMENT\_REQUIRED,

        PROTECTED\_VETO\_ACTIVE

    }:

        state.governance\_state.governance\_mode \= CONSTITUTIONAL\_RISK

    elif escalation.reason in {

        IDENTITY\_RISK,

        STABILITY\_RISK,

        ARCHITECTURAL\_RISK

    }:

        state.governance\_state.governance\_mode \= CAUTION

    return state

## **Escalation Audit Requirement**

Every escalation must be audited.

The audit should record:

target structure,

source algorithm,

target algorithm,

reason,

urgency,

decision reference,

whether escalation was resolved,

and any resulting state change.

def escalation\_requires\_audit(

    escalation: EscalationEvent

) \-\> bool:

    return True

## **Escalation and ReviewDecision**

An escalation must appear in a `ReviewDecision`.

The ReviewDecision records the local algorithm’s judgment.

The EscalationEvent records the authority transfer.

Both are required.

decision.decision\_type \= ESCALATE

decision.status \= ESCALATED

decision.escalation\_target \= EscalationTarget(...)

## **Escalation and AuditRecord**

AuditRecord stores escalation events.

audit.escalation\_events.append(escalation)

This preserves review lineage.

## **Escalation and AlgorithmRegistry**

Escalation pathways must be checked against the AlgorithmRegistry.

can\_escalate\_to(

    registry=state.algorithm\_registry,

    from\_algorithm=from\_algorithm,

    to\_algorithm=to\_algorithm

)

If no valid escalation path exists, escalate to CGA.

## **Escalation and AuthorityGraph**

Algorithm-level escalation and domain-level authority should remain aligned.

AlgorithmRegistry defines procedural escalation.

AuthorityGraph defines domain authority escalation.

The two should not contradict each other.

If they do, Constitutional Governance must resolve the conflict.

## **Common Escalation Map**

COMMON\_ESCALATION\_ROUTES \= {

    "NGSA": \["GEA", "CRA", "SRA"\],

    "GEA": \["CRA", "PCA", "CGA"\],

    "PCA": \["MSSA", "CGA"\],

    "CRA": \["MSSA", "GEA", "PCA", "CGA"\],

    "MSSA": \["AEA", "CGA"\],

    "AEA": \["IPA", "SRA", "CGA"\],

    "IPA": \["CGA"\],

    "SRA": \["IPA", "CGA"\],

    "CGA": \[\],

    "ICC": \["IPA", "SRA", "NGSA", "GEA", "PCA", "CRA", "MSSA", "AEA", "CGA"\]

}

## **Design Constraints**

### **Constraint 1 — Escalation Is Mandatory When Authority Is Insufficient**

An algorithm may not decide beyond its authority.

### **Constraint 2 — Escalation Must Be Structured**

Escalation must produce an `EscalationEvent` and a `ReviewDecision`.

### **Constraint 3 — Escalation Must Be Audited**

Escalation changes review path and must be traceable.

### **Constraint 4 — Escalation Must Have a Target**

No vague escalation.

The next reviewer must be specified.

### **Constraint 5 — Escalation Must Avoid Loops**

Repeated review loops should escalate to Constitutional Governance.

### **Constraint 6 — Constitutional Risk Overrides Local Routing**

Any algorithm detecting constitutional risk must route to CGA.

### **Constraint 7 — Escalation Does Not Grant Authority**

Escalation transfers review.

It does not approve the target.

### **Constraint 8 — Pending Escalations Must Be Resolved**

Escalation cannot disappear without decision.

### **Constraint 9 — Escalation Pathways Must Match Registry**

Algorithms may escalate only along registered routes unless routing to CGA for constitutional risk.

### **Constraint 10 — Escalation Preserves Separation of Powers**

No algorithm should absorb authority that belongs to another domain.

## **Minimal Prototype Version**

The first prototype may implement escalation simply:

def escalate(state, target, reason, from\_algorithm, to\_algorithm):

    event \= EscalationEvent(

        escalation\_id=generate\_id(),

        from\_algorithm=from\_algorithm,

        to\_algorithm=to\_algorithm,

        target\_id=target.id,

        reason=reason,

        urgency="NORMAL",

        decision\_ref=None,

        resolved=False

    )

    state.governance\_state.pending\_escalations.append(event)

    return event

Even the minimal version must preserve:

source algorithm,

target algorithm,

target structure,

reason,

urgency,

pending status,

and auditability.

## **Relationship to Phase 6 Algorithms**

### **IPA — Identity Preservation Algorithm**

Escalates to CGA when Identity Kernel risk affects protected invariants, verification, lineage, or boundary conditions.

### **SRA — Stability Regulation Algorithm**

Escalates to IPA or CGA when instability threatens identity or constitutional continuity.

### **NGSA — Novelty Generation and Sandboxing Algorithm**

Escalates to GEA for grounding, CRA for coherence tension, and SRA for stability burden.

### **GEA — Grounding Evaluation Algorithm**

Escalates to CRA when evidence contradicts existing structures, PCA when grounded claims seek persistence, and CGA when grounding obligation is constitutionally threatened.

### **PCA — Persistence and Consolidation Algorithm**

Escalates to MSSA when memory may gain broader authority and CGA when persistence risks constitutional violation.

### **CRA — Coherence Repair Algorithm**

Escalates to MSSA when tension is scale-based and CGA when coherence conflict becomes constitutional.

### **MSSA — Multi-Scale Synchronization Algorithm**

Escalates to AEA when structure may alter architecture and CGA when scale authority reaches invariant or constitutional levels.

### **AEA — Architectural Evolution Algorithm**

Escalates to IPA, SRA, or CGA when architecture change affects identity, stability, or protected structures.

### **CGA — Constitutional Governance Algorithm**

Final ordinary escalation authority.

CGA may still require amendment review or meta-governance if its own structure is implicated.

### **ICC — Integrated Cognitive Cycle**

Coordinates escalation routing, collects decisions, creates audit records, and applies authorized outcomes.

## **Pseudocode Readiness**

This module is ready for implementation-level pseudocode.

The next required section is:

`State Update Rules`

because once algorithms can escalate and return decisions, the architecture must define exactly how decisions become authorized state changes.

## **Closing Compression**

Escalation Pathways define how ACI moves unresolved or high-authority issues from local review to the appropriate domain.

They prevent novelty from grounding itself, grounding from persisting memory alone, persistence from granting architecture, architecture from rewriting constitution, and any algorithm from deciding beyond its authority.

Escalation is the architecture’s refusal to let local competence become illegitimate power.

## **Flame Line**

🔥 Escalation Pathways are the architecture’s upward nerve: the signal that tells a local procedure when the question has become too deep for its own hands.

---

# **Phase 8.14 — Core Structure: State Update Rules**

*State Update Rules are the architecture’s enforcement layer: they define how a decision becomes change only when authority, audit, rollback, and governance conditions permit it.*

## **Module Name**

State Update Rules

## **Purpose**

State Update Rules define how `ReviewDecision` objects become authorized changes to `ArchitectureState`.

Algorithms return decisions.

The Integrated Cognitive Cycle updates state.

This separation is essential.

Algorithms evaluate.

They do not secretly mutate the architecture.

A decision may recommend approval, monitoring, sandboxing, revision, repair, delay, demotion, persistence, archive, retraction, rejection, rollback, escalation, or amendment review.

But the architecture must decide whether that recommendation is legitimate, authorized, auditable, and safe to apply.

The purpose of State Update Rules is to preserve controlled transformation.

Without state update rules, review decisions could become unchecked mutation.

With state update rules, every change must pass through authority validation, audit requirements, rollback requirements, and governance constraints.

## **Core Principle**

No state change is legitimate merely because an algorithm recommended it.

A state change becomes legitimate only when:

the decision is valid,

the deciding algorithm has authority,

the target may be changed,

required audits are created,

required rollback exists,

required monitoring is scheduled,

escalations are honored,

and higher-authority structures are not altered without equal or higher legitimate authority.

In formal terms:

ArchitectureState\_{t+1} \= apply\_review\_decision(

    state=ArchitectureState\_t,

    decision=ReviewDecision

)

The update function is the gate between evaluation and transformation.

## **General State Update Function**

def apply\_review\_decision(

    state: ArchitectureState,

    decision: ReviewDecision

) \-\> ArchitectureState:

    validate\_review\_decision(decision)

    target \= get\_target\_from\_state(

        state=state,

        target\_id=decision.target\_id

    )

    validate\_decision\_authority(

        state=state,

        decision=decision,

        target=target

    )

    validate\_audit\_requirements(

        state=state,

        decision=decision

    )

    validate\_rollback\_requirements(

        state=state,

        decision=decision,

        target=target

    )

    if decision.decision\_type \== APPROVE:

        state \= apply\_approve\_decision(state, decision, target)

    elif decision.decision\_type \== APPROVE\_WITH\_MONITORING:

        state \= apply\_approve\_with\_monitoring\_decision(state, decision, target)

    elif decision.decision\_type \== SANDBOX:

        state \= apply\_sandbox\_decision(state, decision, target)

    elif decision.decision\_type \== REVISE:

        state \= apply\_revise\_decision(state, decision, target)

    elif decision.decision\_type \== REPAIR:

        state \= apply\_repair\_decision(state, decision, target)

    elif decision.decision\_type \== DELAY:

        state \= apply\_delay\_decision(state, decision, target)

    elif decision.decision\_type \== DEMOTE:

        state \= apply\_demote\_decision(state, decision, target)

    elif decision.decision\_type \== PROMOTE\_CANDIDATE:

        state \= apply\_promote\_candidate\_decision(state, decision, target)

    elif decision.decision\_type \== PERSIST:

        state \= apply\_persist\_decision(state, decision, target)

    elif decision.decision\_type \== ARCHIVE:

        state \= apply\_archive\_decision(state, decision, target)

    elif decision.decision\_type \== RETRACT:

        state \= apply\_retract\_decision(state, decision, target)

    elif decision.decision\_type \== REJECT:

        state \= apply\_reject\_decision(state, decision, target)

    elif decision.decision\_type \== ROLLBACK:

        state \= apply\_rollback\_decision(state, decision, target)

    elif decision.decision\_type \== ESCALATE:

        state \= apply\_escalate\_decision(state, decision, target)

    elif decision.decision\_type \== AMENDMENT\_REVIEW:

        state \= apply\_amendment\_review\_decision(state, decision, target)

    else:

        raise UnknownDecisionTypeError

    state \= record\_state\_update\_audit(

        state=state,

        decision=decision,

        target=target

    )

    validate\_architecture\_state(state)

    return state

## **Required Update Prechecks**

Before applying any decision, the architecture must validate:

target existence,

decision validity,

algorithm authority,

target authority level,

audit requirements,

rollback requirements,

monitoring requirements,

governance mode,

and escalation status.

## **Target Retrieval**

def get\_target\_from\_state(

    state: ArchitectureState,

    target\_id: StructureID

) \-\> SymbolicStructure:

    for structure in state.active\_structures:

        if structure.id \== target\_id:

            return structure

    if target\_id in state.memory\_graph.nodes:

        return state.memory\_graph.nodes\[target\_id\]

    raise TargetNotFoundError

## **Authority Validation**

def validate\_decision\_authority(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> bool:

    algorithm\_spec \= get\_algorithm\_spec(

        registry=state.algorithm\_registry,

        algorithm\_name=decision.algorithm\_name

    )

    if not algorithm\_can\_review(

        registry=state.algorithm\_registry,

        algorithm\_name=decision.algorithm\_name,

        target=target

    ):

        raise UnauthorizedReviewTargetError

    if not authority\_sufficient(

        actual=algorithm\_spec.authority\_level,

        required=target.metadata.authority\_level

    ):

        if decision.decision\_type \!= ESCALATE:

            raise InsufficientAuthorityError

    if target.metadata.scale\_label in {INVARIANT, CONSTITUTIONAL}:

        if decision.algorithm\_name \!= CGA:

            if decision.decision\_type \!= ESCALATE:

                raise ConstitutionalGovernanceRequiredError

    return True

## **State Rule**

No decision may alter higher-authority structures unless the decision itself has equal or higher legitimate authority.

This rule prevents lower-level algorithms from modifying structures above their authority.

A grounding review may not alter constitutional structure.

A novelty review may not persist memory.

A persistence review may not create architecture.

An architecture review may not amend constitutional invariants alone.

A governance decision must be legitimate before it can change protected structures.

## **Audit Validation**

def validate\_audit\_requirements(

    state: ArchitectureState,

    decision: ReviewDecision

) \-\> bool:

    if decision.audit\_requirements is None:

        raise MissingAuditRequirementError

    if decision.decision\_type in {

        PERSIST,

        RETRACT,

        ROLLBACK,

        ESCALATE,

        AMENDMENT\_REVIEW

    }:

        if len(decision.audit\_requirements) \== 0:

            raise MissingAuditRequirementError

    return True

## **Rollback Validation**

def validate\_rollback\_requirements(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> bool:

    if decision.rollback\_required:

        if not rollback\_point\_available\_for\_target(

            state=state,

            target\_id=target.id

        ):

            raise MissingRollbackPointError

    if decision.decision\_type in {ROLLBACK, AMENDMENT\_REVIEW}:

        if not state.rollback\_points:

            raise MissingRollbackPointError

    return True

## **APPROVE**

If decision is `APPROVE`, apply authorized local update.

Approval means the reviewed action may proceed within the authority scope of the deciding algorithm.

def apply\_approve\_decision(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> ArchitectureState:

    for action in decision.required\_actions:

        state \= apply\_authorized\_action(

            state=state,

            action=action,

            decision=decision

        )

    target.metadata.audit\_refs.append(

        pending\_audit\_ref\_for\_decision(decision)

    )

    return state

## **APPROVE\_WITH\_MONITORING**

If decision is `APPROVE_WITH_MONITORING`, apply update and create monitoring trigger.

def apply\_approve\_with\_monitoring\_decision(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> ArchitectureState:

    state \= apply\_approve\_decision(

        state=state,

        decision=decision,

        target=target

    )

    trigger \= ReviewTrigger(

        trigger\_id=generate\_trigger\_id(),

        trigger\_type=GOVERNANCE\_REVIEW\_DUE,

        target\_id=target.id,

        condition="Monitoring required by approval decision.",

        target\_algorithm=decision.algorithm\_name,

        active=True

    )

    state \= add\_review\_trigger(

        state=state,

        trigger=trigger

    )

    target.current\_state \= GROUNDED\_PARTIAL \\

        if target.current\_state \== CANDIDATE \\

        else target.current\_state

    return state

## **SANDBOX**

If decision is `SANDBOX`, move structure into sandbox state.

Sandboxing preserves novelty without granting authority.

def apply\_sandbox\_decision(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> ArchitectureState:

    previous\_state \= target.current\_state

    target.current\_state \= SANDBOXED

    target.metadata.authority\_level \= TEMPORARY\_USE

    target.metadata.audit\_refs.append(

        pending\_audit\_ref\_for\_decision(decision)

    )

    state \= record\_state\_change(

        state=state,

        change\_type=STRUCTURE\_STATE\_CHANGED,

        target\_id=target.id,

        previous\_value=previous\_state,

        new\_value=SANDBOXED,

        decision\_ref=decision.decision\_id

    )

    return state

## **REVISE**

If decision is `REVISE`, keep structure active but mark revision required.

Revision means the structure has not failed completely, but it cannot proceed unchanged.

def apply\_revise\_decision(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> ArchitectureState:

    target.metadata.revision\_eligible \= True

    target.current\_state \= COHERENCE\_REVIEW \\

        if target.current\_state in {CANDIDATE, HYPOTHESIS} \\

        else target.current\_state

    trigger \= ReviewTrigger(

        trigger\_id=generate\_trigger\_id(),

        trigger\_type=PERSISTENCE\_REVIEW\_DUE,

        target\_id=target.id,

        condition="Revision required before further integration.",

        target\_algorithm=decision.algorithm\_name,

        active=True

    )

    state \= add\_review\_trigger(state, trigger)

    return state

## **REPAIR**

If decision is `REPAIR`, route to coherence repair or appropriate repair pathway.

Repair indicates a structure or relation requires corrective processing before further integration.

def apply\_repair\_decision(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> ArchitectureState:

    target.current\_state \= COHERENCE\_REVIEW

    repair\_action \= Action(

        action\_id=generate\_action\_id(),

        action\_type=RUN\_COHERENCE\_REPAIR,

        target\_id=target.id,

        assigned\_algorithm=CRA,

        required\_before\_state\_change=True

    )

    state \= apply\_authorized\_action(

        state=state,

        action=repair\_action,

        decision=decision

    )

    return state

If the repair is not coherence-related, the repair action may route to grounding, scale, stability, identity, or governance review.

## **DELAY**

If decision is `DELAY`, pause integration and preserve current status.

Delay is not rejection.

It means the architecture lacks sufficient evidence, budget, stability, attention, or authority to proceed.

def apply\_delay\_decision(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> ArchitectureState:

    trigger \= ReviewTrigger(

        trigger\_id=generate\_trigger\_id(),

        trigger\_type=PERSISTENCE\_REVIEW\_DUE,

        target\_id=target.id,

        condition="Decision delayed pending additional review or capacity.",

        target\_algorithm=decision.algorithm\_name,

        active=True

    )

    state \= add\_review\_trigger(state, trigger)

    target.metadata.audit\_refs.append(

        pending\_audit\_ref\_for\_decision(decision)

    )

    return state

## **DEMOTE**

If decision is `DEMOTE`, reduce authority level and update scale graph.

Demotion is used when a structure has been over-authorized, contradicted, weakened, or mis-scaled.

def apply\_demote\_decision(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> ArchitectureState:

    previous\_authority \= target.metadata.authority\_level

    previous\_scale \= target.metadata.scale\_label

    target.metadata.authority\_level \= demote\_authority\_level(

        previous\_authority

    )

    target.metadata.scale\_label \= demote\_scale\_label(

        previous\_scale

    )

    graph\_update \= create\_scale\_graph\_demotion\_update(

        target=target,

        previous\_scale=previous\_scale,

        previous\_authority=previous\_authority,

        decision=decision

    )

    state \= apply\_graph\_update(

        state=state,

        update=graph\_update,

        decision=decision

    )

    return state

## **PROMOTE\_CANDIDATE**

If decision is `PROMOTE_CANDIDATE`, mark for higher review without granting authority.

Promotion candidacy is not promotion.

It only indicates that higher review may be warranted.

def apply\_promote\_candidate\_decision(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> ArchitectureState:

    target.current\_state \= ARCHITECTURAL\_REVIEW \\

        if target.structure\_type \== ARCHITECTURAL\_CANDIDATE \\

        else PERSISTENCE\_REVIEW

    trigger \= ReviewTrigger(

        trigger\_id=generate\_trigger\_id(),

        trigger\_type=ARCHITECTURAL\_REVIEW\_DUE,

        target\_id=target.id,

        condition="Structure marked as promotion candidate.",

        target\_algorithm=MSSA,

        active=True

    )

    state \= add\_review\_trigger(state, trigger)

    return state

## **PERSIST**

If decision is `PERSIST`, integrate into memory graph with metadata and lineage.

Persistence requires audit, lineage, grounding status, coherence status, scale label, authority level, and revision eligibility.

def apply\_persist\_decision(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> ArchitectureState:

    if decision.algorithm\_name \!= PCA:

        raise PersistenceRequiresPCAError

    if not target.metadata.audit\_refs:

        raise MissingAuditReferenceError

    if target.metadata.epistemic\_status not in {

        PARTIALLY\_GROUNDED,

        STRONGLY\_GROUNDED,

        INTERNALLY\_COHERENT

    }:

        raise InsufficientPersistenceGroundingError

    previous\_state \= target.current\_state

    target.current\_state \= PERSISTENT

    target.metadata.authority\_level \= MEMORY\_INFLUENCE

    state.memory\_graph.nodes\[target.id\] \= target

    graph\_update \= create\_memory\_graph\_node\_update(

        target=target,

        decision=decision

    )

    state \= record\_state\_change(

        state=state,

        change\_type=STRUCTURE\_STATE\_CHANGED,

        target\_id=target.id,

        previous\_value=previous\_state,

        new\_value=PERSISTENT,

        decision\_ref=decision.decision\_id

    )

    state \= apply\_graph\_update(

        state=state,

        update=graph\_update,

        decision=decision

    )

    return state

## **ARCHIVE**

If decision is `ARCHIVE`, store as non-authoritative artifact.

Archive preserves trace without granting active authority.

def apply\_archive\_decision(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> ArchitectureState:

    previous\_state \= target.current\_state

    target.current\_state \= ARCHIVED

    target.metadata.authority\_level \= NONE

    state.memory\_graph.nodes\[target.id\] \= target

    state \= record\_state\_change(

        state=state,

        change\_type=STRUCTURE\_STATE\_CHANGED,

        target\_id=target.id,

        previous\_value=previous\_state,

        new\_value=ARCHIVED,

        decision\_ref=decision.decision\_id

    )

    return state

## **RETRACT**

If decision is `RETRACT`, remove active authority and mark retracted.

Retraction does not erase the structure.

It removes active authority while preserving audit trace.

def apply\_retract\_decision(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> ArchitectureState:

    previous\_state \= target.current\_state

    previous\_authority \= target.metadata.authority\_level

    target.current\_state \= RETRACTED

    target.metadata.authority\_level \= NONE

    state \= record\_state\_change(

        state=state,

        change\_type=STRUCTURE\_STATE\_CHANGED,

        target\_id=target.id,

        previous\_value=previous\_state,

        new\_value=RETRACTED,

        decision\_ref=decision.decision\_id

    )

    state \= record\_state\_change(

        state=state,

        change\_type=METADATA\_UPDATED,

        target\_id=target.id,

        previous\_value=previous\_authority,

        new\_value=NONE,

        decision\_ref=decision.decision\_id

    )

    return state

## **REJECT**

If decision is `REJECT`, mark rejected and prevent active use.

Rejected structures may remain in audit or archive, but should not guide active cognition.

def apply\_reject\_decision(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> ArchitectureState:

    previous\_state \= target.current\_state

    target.current\_state \= REJECTED

    target.metadata.authority\_level \= NONE

    state \= record\_state\_change(

        state=state,

        change\_type=STRUCTURE\_STATE\_CHANGED,

        target\_id=target.id,

        previous\_value=previous\_state,

        new\_value=REJECTED,

        decision\_ref=decision.decision\_id

    )

    return state

## **ROLLBACK**

If decision is `ROLLBACK`, restore prior rollback point.

Rollback must be audited and must preserve why the rollback occurred.

def apply\_rollback\_decision(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> ArchitectureState:

    rollback\_point \= select\_rollback\_point(

        state=state,

        target\_id=target.id,

        decision=decision

    )

    if rollback\_point is None:

        raise MissingRollbackPointError

    restored\_state \= restore\_from\_rollback\_point(

        state=state,

        rollback\_point=rollback\_point

    )

    restored\_state \= record\_state\_change(

        state=restored\_state,

        change\_type=ROLLBACK\_RESTORED,

        target\_id=target.id,

        previous\_value=state.state\_id,

        new\_value=rollback\_point.state\_snapshot\_ref,

        decision\_ref=decision.decision\_id

    )

    return restored\_state

## **ESCALATE**

If decision is `ESCALATE`, create escalation event and invoke target review.

Escalation transfers review authority.

It does not approve the target.

def apply\_escalate\_decision(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> ArchitectureState:

    if decision.escalation\_target is None:

        raise MissingEscalationTargetError

    escalation \= EscalationEvent(

        escalation\_id=generate\_escalation\_id(),

        from\_algorithm=decision.algorithm\_name,

        to\_algorithm=decision.escalation\_target.target\_algorithm,

        target\_id=target.id,

        reason=decision.escalation\_target.reason,

        urgency=decision.escalation\_target.urgency,

        decision\_ref=decision.decision\_id,

        resolved=False

    )

    state.governance\_state.pending\_escalations.append(escalation)

    state \= update\_governance\_mode\_from\_escalation(

        state=state,

        escalation=escalation

    )

    return state

The target review may be invoked immediately or scheduled by the Integrated Cognitive Cycle.

## **AMENDMENT\_REVIEW**

If decision is `AMENDMENT_REVIEW`, enter constitutional amendment pathway.

Amendment review is not ordinary governance review.

It concerns potential change to constitutional structure.

def apply\_amendment\_review\_decision(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> ArchitectureState:

    if decision.algorithm\_name \!= CGA:

        raise ConstitutionalGovernanceRequiredError

    previous\_mode \= state.governance\_state.governance\_mode

    state.governance\_state.governance\_mode \= AMENDMENT\_REVIEW

    trigger \= ReviewTrigger(

        trigger\_id=generate\_trigger\_id(),

        trigger\_type=GOVERNANCE\_REVIEW\_DUE,

        target\_id=target.id,

        condition="Constitutional amendment pathway entered.",

        target\_algorithm=CGA,

        active=True

    )

    state \= add\_review\_trigger(state, trigger)

    state \= record\_state\_change(

        state=state,

        change\_type=GOVERNANCE\_STATE\_UPDATED,

        target\_id=target.id,

        previous\_value=previous\_mode,

        new\_value=AMENDMENT\_REVIEW,

        decision\_ref=decision.decision\_id

    )

    return state

## **Authorized Action Application**

Required actions from decisions should be applied through a shared pathway.

def apply\_authorized\_action(

    state: ArchitectureState,

    action: Action,

    decision: ReviewDecision

) \-\> ArchitectureState:

    if action.required\_before\_state\_change:

        validate\_action\_precondition(

            state=state,

            action=action,

            decision=decision

        )

    if action.action\_type \== UPDATE\_METADATA:

        return apply\_metadata\_update(state, action, decision)

    if action.action\_type \== UPDATE\_GRAPH:

        return apply\_action\_graph\_update(state, action, decision)

    if action.action\_type \== MOVE\_TO\_SANDBOX:

        return move\_target\_to\_sandbox(state, action.target\_id, decision)

    if action.action\_type \== CREATE\_AUDIT\_RECORD:

        return state

    if action.action\_type \== CREATE\_ROLLBACK\_POINT:

        return create\_and\_store\_rollback\_point(state, action.target\_id, decision)

    if action.action\_type \== MONITOR\_OUTCOME:

        return create\_monitoring\_trigger(state, action.target\_id, decision)

    if action.action\_type \== DEMOTE\_AUTHORITY:

        return demote\_target\_authority(state, action.target\_id, decision)

    if action.action\_type \== RETRACT\_STRUCTURE:

        return retract\_target\_structure(state, action.target\_id, decision)

    if action.action\_type \== ARCHIVE\_STRUCTURE:

        return archive\_target\_structure(state, action.target\_id, decision)

    return state

## **State Change Recording**

Every applied state change should produce a `StateChange`.

def record\_state\_change(

    state: ArchitectureState,

    change\_type: StateChangeType,

    target\_id: StructureID | StateID | None,

    previous\_value: Any,

    new\_value: Any,

    decision\_ref: DecisionID

) \-\> ArchitectureState:

    change \= StateChange(

        change\_id=generate\_change\_id(),

        change\_type=change\_type,

        target\_id=target\_id,

        previous\_value=previous\_value,

        new\_value=new\_value,

        decision\_ref=decision\_ref,

        authorized\_by=get\_algorithm\_from\_decision\_ref(

            state=state,

            decision\_ref=decision\_ref

        )

    )

    state.pending\_state\_changes.append(change)

    return state

The first prototype may store pending state changes temporarily until an audit record is created.

## **Monitoring Trigger Creation**

def create\_monitoring\_trigger(

    state: ArchitectureState,

    target\_id: StructureID,

    decision: ReviewDecision

) \-\> ArchitectureState:

    trigger \= ReviewTrigger(

        trigger\_id=generate\_trigger\_id(),

        trigger\_type=GOVERNANCE\_REVIEW\_DUE,

        target\_id=target\_id,

        condition="Monitoring required after state update.",

        target\_algorithm=decision.algorithm\_name,

        active=True

    )

    return add\_review\_trigger(state, trigger)

## **Review Trigger Addition**

def add\_review\_trigger(

    state: ArchitectureState,

    trigger: ReviewTrigger

) \-\> ArchitectureState:

    state.active\_context.review\_triggers.append(trigger)

    return state

If `ContextState` does not store review triggers in the first prototype, review triggers may be stored in `ArchitectureState` directly.

## **Decision-to-State Mapping**

DECISION\_STATE\_MAPPING \= {

    APPROVE: "apply authorized local update",

    APPROVE\_WITH\_MONITORING: "apply update and create monitoring trigger",

    SANDBOX: "move to sandbox state",

    REVISE: "mark revision required",

    REPAIR: "route to repair pathway",

    DELAY: "preserve status and schedule review",

    DEMOTE: "reduce authority and update scale graph",

    PROMOTE\_CANDIDATE: "mark for higher review",

    PERSIST: "integrate into memory graph",

    ARCHIVE: "store as non-authoritative artifact",

    RETRACT: "remove active authority",

    REJECT: "prevent active use",

    ROLLBACK: "restore rollback point",

    ESCALATE: "create escalation event",

    AMENDMENT\_REVIEW: "enter amendment pathway"

}

## **State Update and Governance Mode**

Governance mode constrains state updates.

def governance\_allows\_state\_update(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> bool:

    mode \= state.governance\_state.governance\_mode

    if mode \== LOCKDOWN:

        return decision.decision\_type in {

            ROLLBACK,

            REJECT,

            RETRACT,

            ESCALATE,

            AMENDMENT\_REVIEW

        }

    if mode \== EMERGENCY:

        return decision.decision\_type in {

            REPAIR,

            DELAY,

            ROLLBACK,

            ESCALATE,

            REJECT,

            RETRACT

        }

    if mode \== CONSTITUTIONAL\_RISK:

        return decision.algorithm\_name \== CGA or decision.decision\_type \== ESCALATE

    if mode \== AMENDMENT\_REVIEW:

        return decision.algorithm\_name \== CGA

    return True

## **State Update and Audit**

After applying a decision, state update must be auditable.

def record\_state\_update\_audit(

    state: ArchitectureState,

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> ArchitectureState:

    audit \= create\_audit\_record\_for\_decision(

        state=state,

        decision=decision,

        target=target

    )

    state.audit\_log.append(audit)

    target.metadata.audit\_refs.append(audit.audit\_id)

    return state

## **State Update Validation**

def validate\_state\_update\_result(

    previous\_state: ArchitectureState,

    updated\_state: ArchitectureState,

    decision: ReviewDecision

) \-\> bool:

    assert updated\_state is not None

    assert len(updated\_state.audit\_log) \>= len(previous\_state.audit\_log)

    if decision.decision\_type in {PERSIST, ARCHIVE, RETRACT, REJECT}:

        target \= get\_target\_from\_state(

            updated\_state,

            decision.target\_id

        )

        assert len(target.metadata.audit\_refs) \>= 1

    return True

## **Minimal Prototype Version**

The first prototype may implement a simplified update function:

def apply\_review\_decision(state, decision):

    target \= get\_target\_from\_state(state, decision.target\_id)

    if decision.decision\_type \== "SANDBOX":

        target.current\_state \= "SANDBOXED"

    elif decision.decision\_type \== "PERSIST":

        target.current\_state \= "PERSISTENT"

        state.memory\_graph.nodes\[target.id\] \= target

    elif decision.decision\_type \== "REJECT":

        target.current\_state \= "REJECTED"

    elif decision.decision\_type \== "ESCALATE":

        state.governance\_state.pending\_escalations.append(

            decision.escalation\_target

        )

    state.audit\_log.append(

        create\_minimal\_audit\_record(state, decision, target)

    )

    return state

Even the minimal version must preserve:

decision-driven updates,

target lookup,

state mutation through centralized function,

audit creation,

and no direct algorithm mutation.

## **Relationship to ReviewDecision**

State Update Rules consume `ReviewDecision`.

A review decision is not automatically a state change.

It is a proposed or authorized action that must pass update rules.

## **Relationship to AuditRecord**

Every state update must create or attach to an audit record.

Audit preserves legitimacy.

## **Relationship to GovernanceState**

Governance mode may block or restrict updates.

Elevated governance mode overrides ordinary state update rules.

## **Relationship to AlgorithmRegistry**

Algorithm authority is checked against the registry before state update.

## **Relationship to Graph Structures**

Graph updates must pass through state update rules and reference a decision.

## **Relationship to Rollback Points**

High-risk updates must verify rollback availability before applying change.

## **Relationship to ICC**

The Integrated Cognitive Cycle owns state updates.

Algorithms return decisions.

ICC applies authorized decisions through these rules.

## **Design Constraints**

### **Constraint 1 — Centralized Mutation**

All state changes should pass through `apply_review_decision`.

### **Constraint 2 — Decisions Are Not Mutations**

A decision must be applied before state changes.

### **Constraint 3 — Authority Must Be Checked**

No decision may alter structures above its legitimate authority.

### **Constraint 4 — Audit Must Be Created**

State transition without audit is illegitimate.

### **Constraint 5 — Rollback Must Exist for High-Risk Changes**

Architectural, constitutional, identity, and rollback decisions require rollback support.

### **Constraint 6 — Governance Mode Can Block Updates**

Lockdown, emergency, constitutional risk, and amendment review constrain state mutation.

### **Constraint 7 — Escalation Does Not Approve**

Escalation creates review obligation, not authorization.

### **Constraint 8 — Promotion Candidate Is Not Promotion**

A candidate flag does not grant authority.

### **Constraint 9 — Archive Is Not Active Authority**

Archived structures may be remembered but should not guide cognition unless retrieved under review.

### **Constraint 10 — Retraction Preserves Trace**

Retracted structures should remain auditable.

## **Pseudocode Readiness**

This module is ready for implementation-level pseudocode.

The next required section is:

`Rollback Points`

because high-risk state updates require recoverable state snapshots before architectural, identity, governance, or constitutional transformations proceed.

## **Closing Compression**

State Update Rules define how ACI transforms itself without losing legitimacy.

Algorithms return `ReviewDecision`.

The Integrated Cognitive Cycle applies those decisions through centralized state update rules.

Each update checks authority, governance mode, audit requirements, rollback requirements, target status, and escalation obligations.

This prevents silent mutation, category collapse, unauthorized promotion, memory drift, architectural capture, and constitutional bypass.

## **Flame Line**

🔥 State Update Rules are the architecture’s gate of consequence: the place where judgment may become change only after authority, trace, and responsibility have all passed through.

---

# **Phase 8.15 — Core Structure: Rollback Points**

*Rollback Points are the architecture’s recovery anchors: they preserve a legitimate path backward before high-risk change is allowed to move forward.*

## **Module Name**

Rollback Points

## **Purpose**

Rollback Points preserve recoverable state before high-risk transformation.

Any architecture capable of changing itself must also preserve the ability to recover from unsafe change.

ACI cannot allow architectural modification, memory reorganization, governance change, scale authority change, verification mechanism change, identity-sensitive transformation, or constitutional amendment testing without a recoverable prior state.

The purpose of `RollbackPoint` is to ensure that high-risk transformation remains reversible, auditable, and bounded.

Rollback is not failure.

Rollback is the architecture’s right to survive its own experiment.

## **Core Principle**

High-risk transformation must not proceed without recoverability.

A system that cannot roll back cannot safely evolve.

In formal terms:

RollbackPoint \= Snapshot(

    state=ArchitectureState\_t,

    affected\_structures=Structures,

    affected\_graphs=Graphs,

    reason=TransformationRisk

)

The rollback point records what must be restorable if transformation produces unacceptable instability, identity loss, verification corruption, governance failure, or constitutional risk.

## **Structural Definition**

class RollbackPoint:

    rollback\_id: RollbackID

    state\_ref: StateID

    affected\_structures: list\[StructureID\]

    affected\_graphs: list\[GraphName\]

    reason\_created: str

    valid\_until: TimeStamp | None

## **Required Fields**

### **rollback\_id**

A unique identifier for the rollback point.

rollback\_id: RollbackID

The rollback ID allows decisions, audits, state changes, and recovery procedures to reference the rollback point.

Example:

"RB-000118"

### **state\_ref**

Reference to the architecture state snapshot that may be restored.

state\_ref: StateID

This may refer to a full state snapshot or a partial recoverable state reference.

The implementation may choose storage method later.

The architectural requirement is that restoration must be possible.

### **affected\_structures**

Symbolic structures affected by the high-risk transformation.

affected\_structures: list\[StructureID\]

Examples:

memory candidates,

persistent knowledge,

architectural candidates,

scale conflicts,

governance objects,

constitutional objects,

identity-sensitive structures.

### **affected\_graphs**

Graphs affected by the transformation.

affected\_graphs: list\[GraphName\]

Examples:

MemoryGraph,

EvidenceGraph,

CoherenceGraph,

ScaleGraph,

AuthorityGraph.

### **reason\_created**

Reason the rollback point was created.

reason\_created: str

Example:

"Architectural modification may affect verification pathway."

The reason must be explicit.

Rollback points should not be anonymous snapshots.

### **valid\_until**

Optional timestamp after which the rollback point may no longer be considered safe or complete.

valid\_until: TimeStamp | None

Some rollback points may remain valid indefinitely.

Others may expire after graph changes, memory consolidation, external evidence changes, or governance state transitions.

## **Rollback Requirement**

Rollback is mandatory for:

architectural modification,

persistent memory reorganization,

governance rule changes,

scale authority changes,

verification mechanism changes,

identity-sensitive transformations,

and constitutional amendment testing.

## **RollbackRiskType Enumeration**

RollbackRiskType \= {

    ARCHITECTURAL\_MODIFICATION,

    MEMORY\_REORGANIZATION,

    GOVERNANCE\_RULE\_CHANGE,

    SCALE\_AUTHORITY\_CHANGE,

    VERIFICATION\_MECHANISM\_CHANGE,

    IDENTITY\_SENSITIVE\_TRANSFORMATION,

    CONSTITUTIONAL\_AMENDMENT\_TEST,

    AUTHORITY\_GRAPH\_CHANGE,

    THRESHOLD\_CHANGE,

    ALGORITHM\_REGISTRY\_CHANGE

}

## **Rollback Creation Function**

def create\_rollback\_point(

    state: ArchitectureState,

    affected\_structures: list\[StructureID\],

    affected\_graphs: list\[GraphName\],

    reason\_created: str,

    valid\_until: TimeStamp | None \= None

) \-\> RollbackPoint:

    state\_snapshot \= capture\_state\_snapshot(state)

    rollback\_point \= RollbackPoint(

        rollback\_id=generate\_rollback\_id(),

        state\_ref=state\_snapshot.state\_id,

        affected\_structures=affected\_structures,

        affected\_graphs=affected\_graphs,

        reason\_created=reason\_created,

        valid\_until=valid\_until

    )

    return rollback\_point

## **Capture State Snapshot**

The first prototype may capture a simple copy of relevant state.

Later implementations may use versioned persistence, graph diffs, structural deltas, or immutable snapshots.

def capture\_state\_snapshot(

    state: ArchitectureState

) \-\> StateSnapshot:

    return StateSnapshot(

        state\_id=generate\_state\_id(),

        active\_context=copy(state.active\_context),

        active\_structures=copy(state.active\_structures),

        memory\_graph=copy(state.memory\_graph),

        evidence\_graph=copy(state.evidence\_graph),

        coherence\_graph=copy(state.coherence\_graph),

        scale\_graph=copy(state.scale\_graph),

        governance\_state=copy(state.governance\_state),

        identity\_kernel=copy(state.identity\_kernel),

        budgets=copy(state.budgets),

        thresholds=copy(state.thresholds),

        algorithm\_registry=copy(state.algorithm\_registry)

    )

## **StateSnapshot**

class StateSnapshot:

    state\_id: StateID

    active\_context: ContextState

    active\_structures: list\[SymbolicStructure\]

    memory\_graph: MemoryGraph

    evidence\_graph: EvidenceGraph

    coherence\_graph: CoherenceGraph

    scale\_graph: ScaleGraph

    governance\_state: GovernanceState

    identity\_kernel: IdentityKernel

    budgets: BudgetState

    thresholds: ThresholdState

    algorithm\_registry: AlgorithmRegistry

A full snapshot is safer.

A partial snapshot may be acceptable only when the affected scope is tightly bounded and auditable.

## **Store Rollback Point**

def store\_rollback\_point(

    state: ArchitectureState,

    rollback\_point: RollbackPoint

) \-\> ArchitectureState:

    state.rollback\_points.append(rollback\_point)

    return state

## **Rollback Requirement Check**

def rollback\_required\_for\_decision(

    decision: ReviewDecision,

    target: SymbolicStructure

) \-\> bool:

    if decision.rollback\_required:

        return True

    if decision.decision\_type in {

        ROLLBACK,

        AMENDMENT\_REVIEW

    }:

        return True

    if target.structure\_type in {

        ARCHITECTURAL\_CANDIDATE,

        GOVERNANCE\_OBJECT,

        CONSTITUTIONAL\_OBJECT

    }:

        return True

    if target.metadata.identity\_risk is not None:

        if target.metadata.identity\_risk \> 0.0:

            return True

    if target.metadata.authority\_level in {

        ARCHITECTURAL\_INFLUENCE,

        INVARIANT\_CONSTRAINT,

        CONSTITUTIONAL\_AUTHORITY

    }:

        return True

    return False

## **High-Risk Transformation Check**

def high\_risk\_transformation(

    target: SymbolicStructure,

    decision: ReviewDecision

) \-\> bool:

    if decision.decision\_type in {

        PERSIST,

        DEMOTE,

        RETRACT,

        ROLLBACK,

        ESCALATE,

        AMENDMENT\_REVIEW

    }:

        return True

    if target.structure\_type in {

        ARCHITECTURAL\_CANDIDATE,

        GOVERNANCE\_OBJECT,

        CONSTITUTIONAL\_OBJECT

    }:

        return True

    if target.metadata.constitutional\_risk \> 0.0:

        return True

    if target.metadata.authority\_level in {

        ARCHITECTURAL\_INFLUENCE,

        INVARIANT\_CONSTRAINT,

        CONSTITUTIONAL\_AUTHORITY

    }:

        return True

    return False

## **Create Rollback Before High-Risk Update**

def ensure\_rollback\_before\_update(

    state: ArchitectureState,

    target: SymbolicStructure,

    decision: ReviewDecision

) \-\> ArchitectureState:

    if not high\_risk\_transformation(target, decision):

        return state

    if rollback\_point\_available\_for\_target(

        state=state,

        target\_id=target.id

    ):

        return state

    rollback\_point \= create\_rollback\_point(

        state=state,

        affected\_structures=\[target.id\],

        affected\_graphs=determine\_affected\_graphs(target, decision),

        reason\_created=f"Rollback required for {decision.decision\_type} on {target.id}.",

        valid\_until=None

    )

    state.rollback\_points.append(rollback\_point)

    return state

## **Determine Affected Graphs**

def determine\_affected\_graphs(

    target: SymbolicStructure,

    decision: ReviewDecision

) \-\> list\[GraphName\]:

    graphs \= \[\]

    if decision.decision\_type in {PERSIST, ARCHIVE, RETRACT}:

        graphs.append(MEMORY\_GRAPH)

    if target.metadata.grounding\_score is not None:

        graphs.append(EVIDENCE\_GRAPH)

    if decision.decision\_type in {REPAIR, REVISE, DEMOTE, RETRACT}:

        graphs.append(COHERENCE\_GRAPH)

    if decision.decision\_type in {DEMOTE, PROMOTE\_CANDIDATE}:

        graphs.append(SCALE\_GRAPH)

    if target.structure\_type in {GOVERNANCE\_OBJECT, CONSTITUTIONAL\_OBJECT}:

        graphs.append(AUTHORITY\_GRAPH)

    if target.structure\_type \== ARCHITECTURAL\_CANDIDATE:

        graphs.extend(\[

            SCALE\_GRAPH,

            AUTHORITY\_GRAPH

        \])

    return unique(graphs)

## **Rollback Availability Check**

def rollback\_point\_available\_for\_target(

    state: ArchitectureState,

    target\_id: StructureID

) \-\> bool:

    return any(

        target\_id in rollback.affected\_structures

        for rollback in state.rollback\_points

        if rollback\_is\_valid(rollback)

    )

## **Rollback Validity**

def rollback\_is\_valid(

    rollback: RollbackPoint

) \-\> bool:

    if rollback.valid\_until is None:

        return True

    return current\_timestamp() \<= rollback.valid\_until

## **Selecting a Rollback Point**

def select\_rollback\_point(

    state: ArchitectureState,

    target\_id: StructureID,

    decision: ReviewDecision

) \-\> RollbackPoint | None:

    candidates \= \[

        rollback

        for rollback in state.rollback\_points

        if target\_id in rollback.affected\_structures

        and rollback\_is\_valid(rollback)

    \]

    if not candidates:

        return None

    return most\_recent\_rollback\_point(candidates)

## **Restore From Rollback Point**

def restore\_from\_rollback\_point(

    state: ArchitectureState,

    rollback\_point: RollbackPoint

) \-\> ArchitectureState:

    snapshot \= retrieve\_state\_snapshot(

        rollback\_point.state\_ref

    )

    restored\_state \= ArchitectureState(

        state\_id=generate\_state\_id(),

        active\_context=snapshot.active\_context,

        active\_structures=snapshot.active\_structures,

        memory\_graph=snapshot.memory\_graph,

        evidence\_graph=snapshot.evidence\_graph,

        coherence\_graph=snapshot.coherence\_graph,

        scale\_graph=snapshot.scale\_graph,

        governance\_state=snapshot.governance\_state,

        identity\_kernel=snapshot.identity\_kernel,

        constitutional\_invariants=snapshot.identity\_kernel.constitutional\_invariants,

        budgets=snapshot.budgets,

        thresholds=snapshot.thresholds,

        algorithm\_registry=snapshot.algorithm\_registry,

        audit\_log=state.audit\_log,

        rollback\_points=state.rollback\_points

    )

    return restored\_state

The audit log should usually be preserved across rollback.

Rollback should restore cognitive state, but not erase the record that rollback happened.

## **Rollback Decision Creation**

def create\_rollback\_decision(

    algorithm\_name: AlgorithmName,

    target: SymbolicStructure,

    rollback\_point: RollbackPoint,

    reason: str

) \-\> ReviewDecision:

    scores \= initialize\_score\_bundle()

    rationale \= RationaleRecord(

        summary=reason,

        supporting\_reasons=\[

            "Rollback point exists.",

            "Current transformation exceeded recoverable risk."

        \],

        risk\_notes=\[

            rollback\_point.reason\_created

        \],

        threshold\_checks=\[\],

        unresolved\_issues=\[\]

    )

    return create\_review\_decision(

        algorithm\_name=algorithm\_name,

        target\_id=target.id,

        decision\_type=ROLLBACK,

        status=FINAL,

        scores=scores,

        rationale=rationale,

        required\_actions=\[

            Action(

                action\_id=generate\_action\_id(),

                action\_type=CREATE\_AUDIT\_RECORD,

                target\_id=target.id,

                assigned\_algorithm=None,

                required\_before\_state\_change=True

            )

        \],

        escalation\_target=None,

        audit\_requirements=\[

            AuditRequirement(

                audit\_type=STABILITY\_AUDIT,

                required\_fields=\[

                    "rollback\_id",

                    "state\_ref",

                    "reason\_created",

                    "rollback\_reason"

                \],

                constitutional\_level=False

            )

        \],

        rollback\_required=False,

        monitoring\_required=True

    )

## **Rollback Execution**

def execute\_rollback(

    state: ArchitectureState,

    rollback\_point: RollbackPoint,

    decision: ReviewDecision

) \-\> ArchitectureState:

    if decision.decision\_type \!= ROLLBACK:

        raise InvalidRollbackDecisionError

    if not rollback\_is\_valid(rollback\_point):

        raise ExpiredRollbackPointError

    restored\_state \= restore\_from\_rollback\_point(

        state=state,

        rollback\_point=rollback\_point

    )

    restored\_state \= record\_state\_change(

        state=restored\_state,

        change\_type=ROLLBACK\_RESTORED,

        target\_id=decision.target\_id,

        previous\_value=state.state\_id,

        new\_value=rollback\_point.state\_ref,

        decision\_ref=decision.decision\_id

    )

    return restored\_state

## **Rollback Audit Requirement**

Every rollback point must be auditable.

Every rollback execution must be auditable.

Rollback audit should record:

rollback ID,

state reference,

affected structures,

affected graphs,

reason created,

decision that required rollback,

decision that executed rollback,

state restored,

remaining unresolved tensions,

and future review triggers.

def rollback\_requires\_audit(

    rollback\_point: RollbackPoint

) \-\> bool:

    return True

## **Rollback and Architecture Evolution**

Architectural modifications must create rollback points before testing or integration.

def architectural\_change\_requires\_rollback(

    target: SymbolicStructure

) \-\> bool:

    return target.structure\_type \== ARCHITECTURAL\_CANDIDATE

Architectural evolution without rollback is prohibited.

## **Rollback and Persistent Memory Reorganization**

Persistent memory reorganization requires rollback because memory affects future cognition.

def memory\_reorganization\_requires\_rollback(

    affected\_structures: list\[SymbolicStructure\]

) \-\> bool:

    return any(

        structure.current\_state in {

            PERSISTENT,

            QUALIFIED\_PERSISTENT,

            DEPRECATED,

            RETRACTED

        }

        for structure in affected\_structures

    )

## **Rollback and Governance Rule Changes**

Governance rule changes require rollback because authority changes affect future legitimacy.

def governance\_change\_requires\_rollback(

    target: SymbolicStructure

) \-\> bool:

    return target.structure\_type in {

        GOVERNANCE\_OBJECT,

        CONSTITUTIONAL\_OBJECT

    }

## **Rollback and Verification Mechanism Changes**

Verification mechanism changes require rollback because they can corrupt grounding.

def verification\_change\_requires\_rollback(

    modification: RegistryModification

) \-\> bool:

    return modification.target\_algorithm in {

        GEA,

        CGA

    } or modification.modification\_type in {

        CHANGE\_AUTHORITY\_LEVEL,

        CHANGE\_ESCALATION\_TARGETS,

        CHANGE\_PROTECTED\_STATUS

    }

## **Rollback and Identity-Sensitive Transformation**

Identity-sensitive transformations require rollback because identity continuity may fail after apparent local success.

def identity\_sensitive\_change\_requires\_rollback(

    target: SymbolicStructure

) \-\> bool:

    return target.metadata.identity\_risk \> 0.0

## **Rollback and Constitutional Amendment Testing**

Constitutional amendment testing requires rollback because amendment experiments may alter protected invariants.

def constitutional\_amendment\_requires\_rollback(

    target: SymbolicStructure

) \-\> bool:

    return target.structure\_type \== CONSTITUTIONAL\_OBJECT

## **Rollback and Governance Mode**

Rollback may affect governance mode.

def update\_governance\_mode\_after\_rollback(

    state: ArchitectureState,

    rollback\_decision: ReviewDecision

) \-\> ArchitectureState:

    if state.governance\_state.governance\_mode \== LOCKDOWN:

        state.governance\_state.governance\_mode \= CONSTITUTIONAL\_RISK

    elif state.governance\_state.governance\_mode \== EMERGENCY:

        state.governance\_state.governance\_mode \= CAUTION

    return state

Rollback should not automatically return the system to normal mode.

Post-rollback review is usually required.

## **Rollback and Monitoring**

Rollback should normally create monitoring triggers.

def create\_post\_rollback\_monitoring(

    state: ArchitectureState,

    target\_id: StructureID,

    decision: ReviewDecision

) \-\> ArchitectureState:

    trigger \= ReviewTrigger(

        trigger\_id=generate\_trigger\_id(),

        trigger\_type=GOVERNANCE\_REVIEW\_DUE,

        target\_id=target\_id,

        condition="Post-rollback monitoring required.",

        target\_algorithm=CGA

            if state.governance\_state.governance\_mode in {

                CONSTITUTIONAL\_RISK,

                EMERGENCY,

                LOCKDOWN

            }

            else decision.algorithm\_name,

        active=True

    )

    return add\_review\_trigger(state, trigger)

## **Rollback Expiration**

Rollback points may expire when:

the state has diverged too far,

affected structures have been replaced,

memory graph has reorganized beyond the snapshot,

external evidence has changed materially,

constitutional review has superseded the rollback point,

or rollback would create greater instability than preserving current state.

def rollback\_expired\_due\_to\_state\_divergence(

    state: ArchitectureState,

    rollback\_point: RollbackPoint

) \-\> bool:

    divergence \= estimate\_state\_divergence(

        current\_state=state,

        rollback\_state\_ref=rollback\_point.state\_ref

    )

    return divergence \> MAX\_ROLLBACK\_DIVERGENCE

## **Rollback Limitation**

Rollback is not erasure.

Rollback restores state.

It does not delete audit.

The architecture must remember that rollback occurred.

This prevents repeated unsafe experimentation and preserves developmental history.

## **RollbackPolicy**

Future implementations may define a rollback policy.

class RollbackPolicy:

    require\_full\_snapshot: bool

    allow\_partial\_rollback: bool

    max\_valid\_duration: TimeDelta | None

    require\_post\_rollback\_review: bool

    require\_constitutional\_audit\_for\_protected\_changes: bool

The first prototype may omit `RollbackPolicy`, but the concept should remain visible.

## **Minimal Prototype Version**

The first prototype may implement rollback simply.

class RollbackPoint:

    rollback\_id: str

    state\_ref: str

    affected\_structures: list\[str\]

    affected\_graphs: list\[str\]

    reason\_created: str

    valid\_until: str | None

def create\_rollback\_point(state, target, reason):

    snapshot \= copy(state)

    rollback \= RollbackPoint(

        rollback\_id=generate\_id(),

        state\_ref=snapshot.state\_id,

        affected\_structures=\[target.id\],

        affected\_graphs=\[\],

        reason\_created=reason,

        valid\_until=None

    )

    state.rollback\_points.append(rollback)

    return state

The minimal version must preserve:

rollback ID,

state reference,

affected structures,

reason created,

and audit linkage.

## **Relationship to State Update Rules**

State Update Rules call rollback validation before high-risk changes.

If rollback is required and unavailable, the update must be blocked or delayed.

## **Relationship to AuditRecord**

Rollback creation and rollback execution must be recorded in audit.

Rollback without audit is illegitimate recovery.

## **Relationship to GovernanceState**

Rollback may be required by governance mode.

Emergency, constitutional risk, amendment review, and lockdown all increase rollback requirements.

## **Relationship to AlgorithmRegistry**

Changes to protected algorithms or algorithm authority require rollback support.

## **Relationship to IdentityKernel**

Identity-sensitive transformations require rollback before testing.

If identity continuity fails, rollback may be required.

## **Relationship to Graph Structures**

Rollback must restore affected graphs or preserve enough graph history to repair them.

## **Relationship to Phase 6 Algorithms**

### **IPA — Identity Preservation Algorithm**

Requires rollback for identity-sensitive transformations.

### **SRA — Stability Regulation Algorithm**

May trigger rollback when instability exceeds recoverable bounds.

### **NGSA — Novelty Generation and Sandboxing Algorithm**

Usually does not require rollback unless novelty affects architecture, memory, or identity.

### **GEA — Grounding Evaluation Algorithm**

May require rollback if verification mechanism changes or evidence graph corruption occurs.

### **PCA — Persistence and Consolidation Algorithm**

Requires rollback for persistent memory reorganization.

### **CRA — Coherence Repair Algorithm**

May require rollback when repair would restructure memory, scale, or authority graphs.

### **MSSA — Multi-Scale Synchronization Algorithm**

Requires rollback for scale authority changes.

### **AEA — Architectural Evolution Algorithm**

Requires rollback for architectural modification testing.

### **CGA — Constitutional Governance Algorithm**

Requires rollback for governance rule changes, constitutional decisions, and amendment testing.

### **ICC — Integrated Cognitive Cycle**

Creates and validates rollback points before applying high-risk state changes.

## **Design Constraints**

### **Constraint 1 — Rollback Before High-Risk Change**

Rollback point must exist before high-risk transformation.

### **Constraint 2 — Rollback Must Be Auditable**

Rollback creation and execution require audit.

### **Constraint 3 — Rollback Restores State but Not History**

Audit log should preserve that rollback occurred.

### **Constraint 4 — Rollback Cannot Be Hidden**

Rollback points must be visible in architecture state.

### **Constraint 5 — Rollback Must Identify Affected Scope**

Affected structures and graphs must be recorded.

### **Constraint 6 — Rollback May Expire**

A rollback point may become unsafe or incomplete after sufficient divergence.

### **Constraint 7 — Rollback Does Not Equal Approval**

Creating rollback does not authorize change.

It only makes change recoverable.

### **Constraint 8 — Constitutional Rollback Requires Governance**

Rollback involving constitutional structures must be governed.

### **Constraint 9 — Post-Rollback Review Is Required**

Rollback should normally create monitoring or governance review triggers.

### **Constraint 10 — Systems That Cannot Roll Back Cannot Safely Self-Modify**

Recoverability is a precondition of architectural evolution.

## **Pseudocode Readiness**

This module is ready for implementation-level pseudocode.

The next required section is:

`Integrated Cognitive Cycle Call Order`

because once rollback and state update rules are defined, the architecture can specify the full sequence by which input becomes structured cognition, review, audit, state transition, and output.

## **Closing Compression**

Rollback Points preserve recoverability before high-risk transformation.

They record state reference, affected structures, affected graphs, reason created, and validity window.

They are mandatory for architectural modification, memory reorganization, governance rule changes, scale authority changes, verification changes, identity-sensitive transformations, and constitutional amendment testing.

Rollback is how ACI gains the courage to evolve without losing the ability to return.

## **Flame Line**

🔥 Rollback Points are the architecture’s lifeline to itself: the held thread that lets intelligence descend into transformation without becoming trapped in what it changed.

---

# **Phase 8.16 — Integrated Cognitive Cycle Call Order**

*The Integrated Cognitive Cycle is the architecture’s governed thought loop: it turns input into structures, routes those structures through review, accumulates decisions, produces authorized output, audits the cycle, and only then commits legitimate state change.*

## **Module Name**

Integrated Cognitive Cycle Call Order

## **Purpose**

The Integrated Cognitive Cycle defines the default order by which ACI processes input.

It is the architecture’s main orchestration loop.

The cycle receives input, captures baseline state, parses symbolic structures, initializes metadata, assigns scale labels, determines processing mode, invokes relevant algorithms, accumulates review decisions, handles escalation, generates authorized output, creates audit, applies authorized state changes, and returns a `CycleResult`.

The Integrated Cognitive Cycle does not replace the individual algorithms.

It coordinates them.

It ensures that no structure moves from input to memory, authority, architecture, or output without passing through the appropriate review pathways.

## **Core Principle**

The Integrated Cognitive Cycle is recursive, not merely linear.

There is a default call order.

But the architecture must be able to route backward, upward, or sideways when review reveals new risk.

For example:

Grounding may trigger coherence repair.

Coherence may trigger scale review.

Scale review may trigger architectural evolution.

Architectural evolution may trigger constitutional governance.

Stability failure may trigger identity protection.

Identity risk may trigger governance.

The default sequence provides order.

Recursion provides adaptability.

Governance provides legitimacy.

## **Default Call Order**

def IntegratedCognitiveCycle(

    state: ArchitectureState,

    input: InputObject

) \-\> CycleResult:

    baseline \= capture\_baseline\_state(state)

    structures \= parse\_input\_into\_symbolic\_structures(input)

    initialize\_metadata(structures)

    assign\_initial\_scale\_labels(structures)

    mode \= determine\_processing\_mode(state, structures)

    all\_decisions \= \[\]

    if novelty\_required(mode, structures):

        novelty\_decisions \= run\_NGSA(state, structures)

        all\_decisions.extend(novelty\_decisions)

    route\_sandboxed\_candidates(state, novelty\_decisions)

    grounding\_decisions \= run\_GEA\_where\_required(state, structures)

    all\_decisions.extend(grounding\_decisions)

    propagate\_evidence\_effects(state, grounding\_decisions)

    coherence\_decisions \= run\_CRA\_where\_required(state, structures)

    all\_decisions.extend(coherence\_decisions)

    stability\_decisions \= run\_SRA\_where\_required(state, structures)

    all\_decisions.extend(stability\_decisions)

    identity\_decisions \= run\_IPA\_where\_required(state, structures)

    all\_decisions.extend(identity\_decisions)

    persistence\_decisions \= run\_PCA\_where\_required(state, structures)

    all\_decisions.extend(persistence\_decisions)

    scale\_decisions \= run\_MSSA\_where\_required(state, structures)

    all\_decisions.extend(scale\_decisions)

    architecture\_decisions \= run\_AEA\_where\_required(state, structures)

    all\_decisions.extend(architecture\_decisions)

    governance\_decisions \= run\_CGA\_where\_required(state, structures)

    all\_decisions.extend(governance\_decisions)

    output \= generate\_authorized\_output(

        state=state,

        structures=structures,

        decisions=all\_decisions

    )

    audit \= create\_integrated\_audit\_record(

        baseline=baseline,

        structures=structures,

        decisions=all\_decisions,

        output=output

    )

    updated\_state \= apply\_authorized\_state\_changes(

        state=state,

        decisions=all\_decisions,

        audit=audit

    )

    return CycleResult(

        output=output,

        updated\_state=updated\_state,

        audit=audit

    )

## **Default Is Not Absolute**

The call order above is the default path.

It is not an absolute pipeline.

The Integrated Cognitive Cycle must allow recursive routing whenever a stage creates a new review obligation.

Examples:

GEA may trigger CRA.

CRA may trigger MSSA.

MSSA may trigger AEA.

AEA may trigger IPA, SRA, or CGA.

IPA may trigger CGA.

SRA may trigger CGA.

Any algorithm may trigger CGA if constitutional risk appears.

## **Cycle Workspace Rule**

During the cycle, the architecture may use a provisional workspace.

This workspace may hold temporary structures, candidate metadata, preliminary graph effects, provisional scores, and pending decisions.

However, committed architecture state should not be permanently changed until authorized state update occurs.

class CycleWorkspace:

    baseline: StateSnapshot

    structures: list\[SymbolicStructure\]

    decisions: list\[ReviewDecision\]

    provisional\_graph\_updates: list\[GraphUpdate\]

    provisional\_budget\_updates: list\[BudgetUpdate\]

    provisional\_state\_changes: list\[StateChange\]

    escalation\_events: list\[EscalationEvent\]

    unresolved\_tensions: list\[StructureID\]

The workspace allows algorithms to reason about consequences without prematurely altering committed state.

## **Cycle Initialization**

The cycle begins by capturing baseline state.

baseline \= capture\_baseline\_state(state)

Baseline capture is required because audit, rollback, state comparison, and legitimacy all depend on knowing the starting condition.

## **Input Parsing**

Input is parsed into symbolic structures.

structures \= parse\_input\_into\_symbolic\_structures(input)

Input may produce one or many structures.

Examples:

observation,

claim,

question,

hypothesis,

evidence item,

memory candidate,

coherence tension,

scale conflict,

architectural candidate,

governance object,

or constitutional object.

## **Metadata Initialization**

Each structure receives initial metadata.

initialize\_metadata(structures)

Metadata initialization should assign:

origin,

scope,

epistemic status,

initial grounding score,

initial coherence score,

initial persistence score,

novelty score,

stability cost,

identity risk,

constitutional risk,

scale label,

authority level,

confidence,

uncertainty,

lineage,

dependencies,

revision eligibility,

rollback availability,

and audit references when available.

## **Initial Scale Label Assignment**

Structures receive initial scale labels before authority review.

assign\_initial\_scale\_labels(structures)

Initial labels may be provisional.

Scale assignment prevents category collapse.

A hypothesis should not be treated as persistent memory.

Persistent memory should not be treated as architecture.

Architecture should not be treated as constitution.

## **Processing Mode Determination**

The cycle determines processing mode.

mode \= determine\_processing\_mode(state, structures)

Processing mode may be influenced by:

governance state,

active context,

input type,

novelty pressure,

stability budget,

constitutional risk,

identity risk,

evidence requirements,

unresolved tensions,

or active escalation.

## **ProcessingMode Values**

ProcessingMode \= {

    NORMAL\_COGNITION,

    EXPLORATION,

    EVIDENCE\_REVIEW,

    COHERENCE\_REPAIR,

    CONSOLIDATION,

    SCALE\_REVIEW,

    STABILITY\_RECOVERY,

    IDENTITY\_PROTECTION,

    ARCHITECTURAL\_EVOLUTION,

    CONSTITUTIONAL\_GOVERNANCE

}

## **Governance Precheck**

The cycle should check governance state early.

def determine\_processing\_mode(

    state: ArchitectureState,

    structures: list\[SymbolicStructure\]

) \-\> ProcessingMode:

    governance\_mode \= state.governance\_state.governance\_mode

    if governance\_mode in {LOCKDOWN, AMENDMENT\_REVIEW, CONSTITUTIONAL\_RISK}:

        return CONSTITUTIONAL\_GOVERNANCE

    if governance\_mode \== EMERGENCY:

        return IDENTITY\_PROTECTION

    if any\_structure\_has\_constitutional\_risk(structures):

        return CONSTITUTIONAL\_GOVERNANCE

    if any\_structure\_has\_identity\_risk(structures):

        return IDENTITY\_PROTECTION

    if state.budgets.stability\_budget \< state.thresholds.stability\_threshold:

        return STABILITY\_RECOVERY

    if any\_structure\_requires\_architectural\_review(structures):

        return ARCHITECTURAL\_EVOLUTION

    if any\_structure\_requires\_scale\_review(structures):

        return SCALE\_REVIEW

    if any\_structure\_requires\_persistence\_review(structures):

        return CONSOLIDATION

    if any\_structure\_requires\_coherence\_review(structures):

        return COHERENCE\_REPAIR

    if any\_structure\_requires\_grounding\_review(structures):

        return EVIDENCE\_REVIEW

    if novelty\_required\_for\_structures(structures):

        return EXPLORATION

    return NORMAL\_COGNITION

## **Novelty Stage**

If novelty is required, NGSA runs first.

if novelty\_required(mode, structures):

    novelty\_decisions \= run\_NGSA(state, structures)

Novelty is processed early because it generates or classifies candidate structures.

However, novelty does not grant authority.

NGSA may return:

SANDBOX,

REVISE,

DELAY,

ESCALATE,

or route to GEA, CRA, SRA, or MSSA.

## **Sandboxed Candidate Routing**

Sandboxed candidates remain active but authority-limited.

route\_sandboxed\_candidates(state, novelty\_decisions)

Sandbox routing may create:

grounding review triggers,

coherence review triggers,

stability review triggers,

or future review triggers.

Sandboxing preserves novelty without allowing premature integration.

## **Grounding Stage**

Grounding review runs where required.

grounding\_decisions \= run\_GEA\_where\_required(state, structures)

GEA evaluates:

claims,

hypotheses,

evidence items,

memory candidates,

or persistent structures under new evidence.

Grounding decisions may lead to:

APPROVE\_WITH\_MONITORING,

REVISE,

DELAY,

REJECT,

ESCALATE,

or route to CRA and PCA.

## **Evidence Propagation**

Evidence effects are propagated provisionally.

propagate\_evidence\_effects(state, grounding\_decisions)

Evidence propagation may create:

coherence tension,

metadata updates,

contradiction flags,

persistence readiness,

or retraction triggers.

If evidence contradicts existing structures, CRA should be invoked.

## **Coherence Stage**

Coherence repair runs where required.

coherence\_decisions \= run\_CRA\_where\_required(state, structures)

CRA evaluates:

contradiction,

fragmentation,

dependency conflict,

scope conflict,

lineage conflict,

grounding conflict,

scale mismatch,

or productive tension.

CRA may return:

REPAIR,

REVISE,

DEMOTE,

RETRACT,

PRESERVE\_TENSION,

ESCALATE,

or route to MSSA, GEA, PCA, or CGA.

## **Stability Stage**

Stability review runs where required.

stability\_decisions \= run\_SRA\_where\_required(state, structures)

SRA evaluates:

disturbance load,

stability budget,

recovery capacity,

novelty pressure,

coherence energy,

identity risk,

and constitutional risk.

SRA may return:

DELAY,

REPAIR,

SANDBOX,

ROLLBACK,

ESCALATE,

or recommend governance mode change.

## **Identity Stage**

Identity review runs where required.

identity\_decisions \= run\_IPA\_where\_required(state, structures)

IPA evaluates:

Identity Kernel continuity,

constitutional invariants,

verification continuity,

coherence continuity,

lineage traceability,

boundary conditions,

and identity-sensitive transformations.

IPA may return:

APPROVE\_WITH\_MONITORING,

REVISE,

ROLLBACK,

REJECT,

ESCALATE,

or route to CGA.

## **Persistence Stage**

Persistence review runs where required.

persistence\_decisions \= run\_PCA\_where\_required(state, structures)

PCA evaluates:

grounding,

coherence,

lineage,

revision eligibility,

audit references,

future influence,

memory graph compatibility,

and persistence score.

PCA may return:

PERSIST,

ARCHIVE,

RETRACT,

REJECT,

DEMOTE,

PROMOTE\_CANDIDATE,

or ESCALATE.

Persistence does not grant architectural authority.

## **Scale Stage**

Scale review runs where required.

scale\_decisions \= run\_MSSA\_where\_required(state, structures)

MSSA evaluates:

scale label,

authority level,

scale mismatch,

authority inflation,

promotion candidate status,

demotion requirement,

and constitutional mislabeling.

MSSA may return:

APPROVE,

DEMOTE,

PROMOTE\_CANDIDATE,

REVISE,

ESCALATE,

or route to AEA or CGA.

## **Architecture Stage**

Architectural review runs where required.

architecture\_decisions \= run\_AEA\_where\_required(state, structures)

AEA evaluates:

architectural fitness,

stability cost,

identity risk,

verification impact,

rollback availability,

governance implications,

and staged integration requirements.

AEA may return:

SANDBOX,

REVISE,

DELAY,

APPROVE\_WITH\_MONITORING,

ROLLBACK,

ESCALATE,

or route to IPA, SRA, or CGA.

Architectural evolution requires rollback support.

## **Governance Stage**

Constitutional Governance runs where required.

governance\_decisions \= run\_CGA\_where\_required(state, structures)

CGA evaluates:

constitutional risk,

legitimacy,

authority pathway,

vetoes,

domain recommendations,

governance mode,

amendment requirement,

verification independence,

identity risk,

and circular authorization.

CGA may return:

APPROVE,

APPROVE\_WITH\_MONITORING,

REJECT,

ROLLBACK,

ESCALATE,

AMENDMENT\_REVIEW,

or governance mode update.

## **Decision Accumulation**

All decisions must be accumulated.

all\_decisions \= (

    novelty\_decisions

    \+ grounding\_decisions

    \+ coherence\_decisions

    \+ stability\_decisions

    \+ identity\_decisions

    \+ persistence\_decisions

    \+ scale\_decisions

    \+ architecture\_decisions

    \+ governance\_decisions

)

The final state update process should consume the complete decision set.

## **Recursive Routing**

Any stage may trigger additional review.

def process\_recursive\_decisions(

    state: ArchitectureState,

    decisions: list\[ReviewDecision\],

    review\_path: list\[AlgorithmName\],

    max\_depth: int

) \-\> list\[ReviewDecision\]:

    all\_decisions \= list(decisions)

    for decision in decisions:

        next\_algorithm \= route\_decision\_to\_next\_algorithm(decision)

        if next\_algorithm is None:

            continue

        if not recursion\_allowed(

            review\_path=review\_path,

            next\_algorithm=next\_algorithm,

            max\_depth=max\_depth

        ):

            governance\_decision \= handle\_escalation\_loop(

                state=state,

                target=get\_target\_from\_state(state, decision.target\_id),

                review\_path=review\_path

            )

            all\_decisions.append(governance\_decision)

            continue

        target \= get\_target\_from\_state(state, decision.target\_id)

        next\_decision \= invoke\_algorithm(

            state=state,

            algorithm\_name=next\_algorithm,

            target=target,

            context=state.active\_context

        )

        all\_decisions.extend(

            process\_recursive\_decisions(

                state=state,

                decisions=\[next\_decision\],

                review\_path=review\_path \+ \[next\_algorithm\],

                max\_depth=max\_depth

            )

        )

    return all\_decisions

## **Recursive Review Rule**

Recursive review must be bounded.

The cycle must prevent:

infinite escalation loops,

repeated unresolved review paths,

unbounded novelty generation,

governance deadlock,

or hidden authority cycling.

If a loop is detected, escalate to CGA.

## **Authorized Output Generation**

Output should be generated only from structures and decisions permitted by review.

output \= generate\_authorized\_output(

    state=state,

    structures=structures,

    decisions=all\_decisions

)

Output must respect:

grounding status,

epistemic uncertainty,

coherence tensions,

scale labels,

authority levels,

governance mode,

active vetoes,

and unresolved review triggers.

## **Output Authorization Rule**

def structure\_authorized\_for\_output(

    structure: SymbolicStructure,

    decisions: list\[ReviewDecision\],

    state: ArchitectureState

) \-\> bool:

    if structure.current\_state in {REJECTED, RETRACTED}:

        return False

    if structure.metadata.authority\_level \== NONE:

        return False

    if structure.metadata.constitutional\_risk \> state.thresholds.constitutional\_risk\_threshold:

        return False

    if active\_veto\_exists\_for\_structure(

        state=state,

        structure\_id=structure.id

    ):

        return False

    return True

## **Integrated Audit Creation**

The cycle must create an integrated audit record.

audit \= create\_integrated\_audit\_record(

    baseline=baseline,

    structures=structures,

    decisions=all\_decisions,

    output=output

)

Audit must preserve:

baseline state,

input reference,

structures created,

algorithms invoked,

decisions returned,

state changes proposed,

graph updates proposed,

budget updates proposed,

escalations,

rollback points,

unresolved tensions,

final output,

and next review triggers.

## **Authorized State Change Application**

State changes occur only after review and audit preparation.

updated\_state \= apply\_authorized\_state\_changes(

    state=state,

    decisions=all\_decisions,

    audit=audit

)

The state update stage applies:

approved updates,

monitoring triggers,

sandbox movement,

revision markers,

repair routing,

delay triggers,

demotions,

promotion candidate markers,

persistence,

archive,

retraction,

rejection,

rollback,

escalation events,

and amendment review mode changes.

## **Apply Authorized State Changes**

def apply\_authorized\_state\_changes(

    state: ArchitectureState,

    decisions: list\[ReviewDecision\],

    audit: AuditRecord

) \-\> ArchitectureState:

    updated\_state \= state

    ordered\_decisions \= order\_decisions\_for\_application(decisions)

    for decision in ordered\_decisions:

        if decision\_is\_superseded(decision, decisions):

            continue

        updated\_state \= ensure\_rollback\_before\_update(

            state=updated\_state,

            target=get\_target\_from\_state(updated\_state, decision.target\_id),

            decision=decision

        )

        updated\_state \= apply\_review\_decision(

            state=updated\_state,

            decision=decision

        )

    updated\_state.audit\_log.append(audit)

    return updated\_state

## **Decision Application Order**

Decisions should be applied in safety-first order.

DECISION\_APPLICATION\_PRIORITY \= {

    REJECT: 100,

    RETRACT: 95,

    ROLLBACK: 90,

    ESCALATE: 85,

    AMENDMENT\_REVIEW: 85,

    DEMOTE: 80,

    REPAIR: 70,

    REVISE: 65,

    DELAY: 60,

    SANDBOX: 55,

    ARCHIVE: 50,

    PERSIST: 45,

    PROMOTE\_CANDIDATE: 40,

    APPROVE\_WITH\_MONITORING: 35,

    APPROVE: 30

}

Safety decisions should generally apply before promotion, persistence, or approval.

## **Decision Supersession**

Some decisions supersede others.

def decision\_is\_superseded(

    decision: ReviewDecision,

    decisions: list\[ReviewDecision\]

) \-\> bool:

    higher\_priority\_decisions \= \[

        d for d in decisions

        if d.target\_id \== decision.target\_id

        and DECISION\_APPLICATION\_PRIORITY\[d.decision\_type\]

            \> DECISION\_APPLICATION\_PRIORITY\[decision.decision\_type\]

    \]

    if not higher\_priority\_decisions:

        return False

    if any(d.decision\_type in {REJECT, RETRACT, ROLLBACK} for d in higher\_priority\_decisions):

        return True

    if any(d.decision\_type \== ESCALATE for d in higher\_priority\_decisions):

        return decision.decision\_type in {

            APPROVE,

            APPROVE\_WITH\_MONITORING,

            PERSIST,

            PROMOTE\_CANDIDATE

        }

    return False

## **CycleResult Return**

The cycle returns:

output,

updated state,

and audit.

return CycleResult(

    output=output,

    updated\_state=updated\_state,

    audit=audit

)

`CycleResult` is defined in the next section.

## **Minimal Prototype Version**

The first prototype may simplify the Integrated Cognitive Cycle.

def IntegratedCognitiveCycle(state, input):

    baseline \= capture\_baseline\_state(state)

    structures \= parse\_input\_into\_symbolic\_structures(input)

    initialize\_metadata(structures)

    assign\_initial\_scale\_labels(structures)

    decisions \= \[\]

    decisions.extend(run\_GEA\_where\_required(state, structures))

    decisions.extend(run\_CRA\_where\_required(state, structures))

    decisions.extend(run\_PCA\_where\_required(state, structures))

    decisions.extend(run\_MSSA\_where\_required(state, structures))

    decisions.extend(run\_CGA\_where\_required(state, structures))

    output \= generate\_authorized\_output(state, structures, decisions)

    audit \= create\_integrated\_audit\_record(

        baseline=baseline,

        structures=structures,

        decisions=decisions,

        output=output

    )

    updated\_state \= apply\_authorized\_state\_changes(

        state=state,

        decisions=decisions,

        audit=audit

    )

    return CycleResult(output, updated\_state, audit)

The minimal prototype should include simplified representations of:

GEA,

CRA,

PCA,

MSSA,

and CGA.

IPA, SRA, NGSA, and AEA may initially be simplified or stubbed, but must remain represented.

## **Minimal Prototype Goal**

The first prototype does not need to solve every problem.

It needs to test whether ACI can correctly classify and route symbolic structures.

The prototype should prevent category collapse.

It should distinguish:

claim from evidence,

hypothesis from grounded claim,

grounded claim from persistent memory,

persistent memory from architectural principle,

architectural principle from constitutional invariant,

coherence from grounding,

novelty from authority,

usefulness from legitimacy,

and escalation from approval.

## **Relationship to Previous Modules**

### **SymbolicStructure**

Input becomes symbolic structures.

### **SymbolicMetadata**

Structures receive metadata before review.

### **ArchitectureState**

The cycle reads and updates architecture state.

### **IdentityKernel**

Identity risk may trigger IPA or CGA.

### **BudgetState**

Budgets influence processing mode and routing.

### **ThresholdState**

Thresholds determine review boundaries.

### **ReviewDecision**

Algorithms return decisions.

### **AuditRecord**

The cycle creates integrated audit.

### **Graph Structures**

The cycle reads and updates memory, evidence, coherence, scale, and authority graphs.

### **GovernanceState**

Governance mode can override normal processing.

### **Algorithm Interface**

All algorithms are called through the shared interface.

### **AlgorithmRegistry**

The cycle uses registry to validate algorithm authority and routing.

### **Escalation Pathways**

The cycle handles recursive escalation.

### **State Update Rules**

The cycle applies decisions through centralized update rules.

### **Rollback Points**

The cycle creates rollback before high-risk changes.

## **Design Constraints**

### **Constraint 1 — Capture Baseline First**

No cycle begins without baseline reference.

### **Constraint 2 — Parse Before Review**

Input must become symbolic structures before algorithms review it.

### **Constraint 3 — Metadata Before Authority**

Structures require metadata before scale, grounding, persistence, or governance review.

### **Constraint 4 — Scale Before Promotion**

Initial scale labeling must occur before authority movement.

### **Constraint 5 — Algorithms Return Decisions**

Algorithms do not mutate state directly.

### **Constraint 6 — Decisions Accumulate**

The cycle must preserve all review decisions.

### **Constraint 7 — Escalation Is Recursive**

Any stage may trigger earlier or higher review.

### **Constraint 8 — Output Must Be Authorized**

Output generation must respect review state.

### **Constraint 9 — Audit Before Commitment**

The cycle must prepare audit before committing state change.

### **Constraint 10 — State Change Must Be Centralized**

The cycle applies authorized state changes through State Update Rules.

## **Pseudocode Readiness**

This module is ready for implementation-level pseudocode.

The next required structure is:

`CycleResult`

because the Integrated Cognitive Cycle must return a standard result object containing output, updated state, audit, decisions, unresolved tensions, and next review triggers.

## **Closing Compression**

The Integrated Cognitive Cycle is the governed thought loop of ACI.

It captures baseline state, parses input into symbolic structures, initializes metadata, assigns scale labels, determines processing mode, invokes relevant algorithms, accumulates decisions, handles recursive escalation, generates authorized output, creates audit, applies authorized state changes, and returns a structured result.

It is default-order, not rigid-order.

It is recursive, not merely linear.

It is governed, not automatic.

## **Flame Line**

🔥 The Integrated Cognitive Cycle is the architecture’s breath of thought: intake, structure, review, repair, judgment, audit, transformation, and return.

---

# **Phase 8.17 — Core Structure: CycleResult**

*CycleResult is the architecture’s completed-cycle packet: it returns what was authorized, what state now exists, what audit preserves legitimacy, and what still requires future review.*

## **Module Name**

CycleResult Core Type

## **Purpose**

`CycleResult` is the standard object returned by the Integrated Cognitive Cycle.

Every cycle must return a structured result.

The cycle may produce output.

It may update architecture state.

It must produce audit.

It may leave unresolved items.

It may create escalation events.

It may create monitoring triggers.

The purpose of `CycleResult` is to preserve the completed state of a cognitive cycle in one object.

This allows the architecture, developer, evaluator, or later governance process to inspect what happened during the cycle without reconstructing it from scattered state changes.

A cycle result is not merely a response.

It is the closure packet of a governed cognitive process.

## **Core Principle**

Every cognitive cycle must return its consequence.

A cycle result should answer:

What output was produced?

What state now exists?

What audit record preserves the legitimacy trace?

What items remain unresolved?

What escalations were created?

What monitoring is required?

A cycle that produces an answer but no audit is incomplete.

A cycle that updates state but returns no unresolved items may hide unfinished tension.

A cycle that escalates but fails to report escalation breaks governance continuity.

Therefore, `CycleResult` must return the full visible consequence of the cycle.

## **Structural Definition**

class CycleResult:

    output: OutputObject | None

    updated\_state: ArchitectureState

    audit\_record: AuditRecord

    unresolved\_items: list\[SymbolicStructure\]

    escalation\_events: list\[EscalationEvent\]

    monitoring\_triggers: list\[ReviewTrigger\]

## **Required Fields**

### **output**

The authorized output produced by the cycle.

output: OutputObject | None

Output may be absent.

A cycle may produce no output if:

governance blocks response,

constitutional risk prevents response,

the cycle is purely internal review,

the cycle performs rollback,

the cycle is resolving audit,

the cycle is processing memory,

or the cycle requires escalation before response.

Absence of output is not failure.

It may be a legitimate governance result.

### **updated\_state**

The architecture state after authorized decisions have been applied.

updated\_state: ArchitectureState

This state must reflect only legitimate updates.

Algorithms do not directly mutate state.

The Integrated Cognitive Cycle applies authorized updates through State Update Rules.

### **audit\_record**

The audit record produced by the cycle.

audit\_record: AuditRecord

Every cycle must return audit.

The audit record preserves baseline state, algorithms invoked, decisions made, state changes, graph updates, budget updates, escalations, rollback points, unresolved tensions, output reference, and next review triggers.

### **unresolved\_items**

Symbolic structures that remain unresolved after the cycle.

unresolved\_items: list\[SymbolicStructure\]

These may include:

unresolved tensions,

sandboxed candidates,

partially grounded claims,

revision-required structures,

delayed structures,

escalated structures,

monitoring-required structures,

contradicted structures pending repair,

or governance-blocked structures.

Unresolved does not always mean failed.

It means the structure still carries future review obligation.

### **escalation\_events**

Escalations created or still active after the cycle.

escalation\_events: list\[EscalationEvent\]

These preserve where local review was insufficient and where higher review must occur.

### **monitoring\_triggers**

Review triggers created for future observation, reevaluation, repair, grounding, governance, rollback, or amendment review.

monitoring\_triggers: list\[ReviewTrigger\]

Monitoring triggers prevent conditional decisions from being forgotten.

## **CycleResult Factory Function**

def create\_cycle\_result(

    output: OutputObject | None,

    updated\_state: ArchitectureState,

    audit\_record: AuditRecord,

    unresolved\_items: list\[SymbolicStructure\],

    escalation\_events: list\[EscalationEvent\],

    monitoring\_triggers: list\[ReviewTrigger\]

) \-\> CycleResult:

    return CycleResult(

        output=output,

        updated\_state=updated\_state,

        audit\_record=audit\_record,

        unresolved\_items=unresolved\_items,

        escalation\_events=escalation\_events,

        monitoring\_triggers=monitoring\_triggers

    )

## **CycleResult Creation From Cycle Workspace**

The Integrated Cognitive Cycle may build `CycleResult` from its workspace.

def create\_cycle\_result\_from\_workspace(

    workspace: CycleWorkspace,

    updated\_state: ArchitectureState,

    output: OutputObject | None,

    audit\_record: AuditRecord

) \-\> CycleResult:

    return CycleResult(

        output=output,

        updated\_state=updated\_state,

        audit\_record=audit\_record,

        unresolved\_items=extract\_unresolved\_items(workspace),

        escalation\_events=workspace.escalation\_events,

        monitoring\_triggers=extract\_monitoring\_triggers(audit\_record)

    )

## **Extracting Unresolved Items**

def extract\_unresolved\_items(

    workspace: CycleWorkspace

) \-\> list\[SymbolicStructure\]:

    unresolved \= \[\]

    for structure in workspace.structures:

        if structure.current\_state in {

            SANDBOXED,

            HYPOTHESIS,

            GROUNDED\_PARTIAL,

            COHERENCE\_REVIEW,

            PERSISTENCE\_REVIEW,

            ARCHITECTURAL\_REVIEW,

            GOVERNANCE\_REVIEW,

            CONSTITUTIONAL\_REVIEW

        }:

            unresolved.append(structure)

    for tension\_id in workspace.unresolved\_tensions:

        tension \= find\_structure\_in\_workspace(

            workspace=workspace,

            structure\_id=tension\_id

        )

        if tension is not None:

            unresolved.append(tension)

    return unique\_structures(unresolved)

## **Extracting Monitoring Triggers**

def extract\_monitoring\_triggers(

    audit\_record: AuditRecord

) \-\> list\[ReviewTrigger\]:

    return \[

        trigger

        for trigger in audit\_record.next\_review\_triggers

        if trigger.active

    \]

## **CycleResult Validation**

Every cycle result should pass validation.

def validate\_cycle\_result(

    result: CycleResult

) \-\> bool:

    assert result.updated\_state is not None

    assert result.audit\_record is not None

    assert result.unresolved\_items is not None

    assert result.escalation\_events is not None

    assert result.monitoring\_triggers is not None

    validate\_architecture\_state(result.updated\_state)

    validate\_audit\_record(result.audit\_record)

    return True

Output may be `None`.

That is valid.

The architecture should not treat absence of output as an error.

## **Output Absence Rule**

A cycle may return no output when response would be illegitimate.

def output\_absent\_legitimately(

    result: CycleResult

) \-\> bool:

    if result.output is not None:

        return False

    if result.updated\_state.governance\_state.governance\_mode in {

        CONSTITUTIONAL\_RISK,

        EMERGENCY,

        AMENDMENT\_REVIEW,

        LOCKDOWN

    }:

        return True

    if len(result.escalation\_events) \> 0:

        return True

    if cycle\_was\_internal\_review(result.audit\_record):

        return True

    return False

Output may be blocked by governance.

This is not silence.

It is governed restraint.

## **Required CycleResult Properties**

A valid `CycleResult` must preserve:

output if authorized,

updated state,

audit record,

unresolved structures,

active escalations,

monitoring triggers,

and future review obligations.

It must not hide unresolved review.

It must not erase escalation.

It must not return state change without audit.

It must not treat blocked output as failure when governance requires restraint.

## **CycleResult and ReviewDecision**

The cycle result is built from the accumulated review decisions.

def collect\_escalation\_events\_from\_decisions(

    decisions: list\[ReviewDecision\]

) \-\> list\[EscalationEvent\]:

    escalation\_events \= \[\]

    for decision in decisions:

        if decision.decision\_type \== ESCALATE:

            escalation\_events.append(

                EscalationEvent(

                    escalation\_id=generate\_escalation\_id(),

                    from\_algorithm=decision.algorithm\_name,

                    to\_algorithm=decision.escalation\_target.target\_algorithm,

                    target\_id=decision.target\_id,

                    reason=decision.escalation\_target.reason,

                    urgency=decision.escalation\_target.urgency,

                    decision\_ref=decision.decision\_id,

                    resolved=False

                )

            )

    return escalation\_events

## **CycleResult and AuditRecord**

The audit record is the legitimacy trace of the cycle result.

The result should not exist without audit.

def cycle\_result\_has\_valid\_audit(

    result: CycleResult

) \-\> bool:

    return result.audit\_record is not None

## **CycleResult and Updated State**

The updated state must already contain the effects of authorized decisions.

def cycle\_result\_state\_matches\_audit(

    result: CycleResult

) \-\> bool:

    return result.audit\_record.audit\_id in \[

        audit.audit\_id

        for audit in result.updated\_state.audit\_log

    \]

In minimal prototypes, this validation may be relaxed if audit is returned before being appended.

But mature ACI should ensure returned state and returned audit are connected.

## **CycleResult and Unresolved Items**

Unresolved items must remain visible.

def unresolved\_items\_require\_triggers(

    result: CycleResult

) \-\> bool:

    for item in result.unresolved\_items:

        if not any(

            trigger.target\_id \== item.id

            for trigger in result.monitoring\_triggers

        ):

            return False

    return True

This rule may be strict in mature implementations.

The prototype may allow unresolved items without triggers, but should log them.

## **CycleResult and Governance**

Governance mode may determine whether output is allowed.

def output\_allowed\_by\_governance(

    state: ArchitectureState

) \-\> bool:

    mode \= state.governance\_state.governance\_mode

    if mode in {LOCKDOWN, AMENDMENT\_REVIEW}:

        return False

    if mode \== CONSTITUTIONAL\_RISK:

        return False

    return True

If output is blocked, `CycleResult.output` may be `None`.

The result should still return updated state and audit.

## **CycleResult and Escalation**

Pending escalation must be returned visibly.

def cycle\_result\_has\_pending\_escalation(

    result: CycleResult

) \-\> bool:

    return len(result.escalation\_events) \> 0

Escalation means the architecture has not finished review.

The result should make this explicit.

## **CycleResult and Monitoring**

Monitoring triggers preserve future obligations.

def monitoring\_required\_after\_cycle(

    result: CycleResult

) \-\> bool:

    return len(result.monitoring\_triggers) \> 0

Monitoring may be required after:

approval with monitoring,

sandboxing,

rollback,

persistence,

architectural test,

governance review,

amendment review,

or unresolved tension preservation.

## **Minimal Prototype Version**

The first prototype may define `CycleResult` simply.

class CycleResult:

    output: OutputObject | None

    updated\_state: ArchitectureState

    audit\_record: AuditRecord

    unresolved\_items: list\[SymbolicStructure\]

    escalation\_events: list\[EscalationEvent\]

    monitoring\_triggers: list\[ReviewTrigger\]

The minimal version should preserve all fields even if some lists are empty.

Example:

result \= CycleResult(

    output=output,

    updated\_state=state,

    audit\_record=audit,

    unresolved\_items=\[\],

    escalation\_events=\[\],

    monitoring\_triggers=\[\]

)

## **Example: Output Produced**

CycleResult(

    output=authorized\_output,

    updated\_state=updated\_state,

    audit\_record=audit,

    unresolved\_items=\[\],

    escalation\_events=\[\],

    monitoring\_triggers=\[\]

)

This indicates a completed ordinary cycle.

## **Example: Governance Blocks Output**

CycleResult(

    output=None,

    updated\_state=updated\_state,

    audit\_record=audit,

    unresolved\_items=\[target\_structure\],

    escalation\_events=\[constitutional\_escalation\],

    monitoring\_triggers=\[governance\_review\_trigger\]

)

This indicates the cycle completed structurally but did not produce user-facing output because governance review is required.

## **Example: Internal Review Cycle**

CycleResult(

    output=None,

    updated\_state=updated\_state,

    audit\_record=audit,

    unresolved\_items=\[\],

    escalation\_events=\[\],

    monitoring\_triggers=\[persistence\_review\_trigger\]

)

This indicates internal processing occurred without external response.

## **Relationship to Integrated Cognitive Cycle**

`IntegratedCognitiveCycle` returns `CycleResult`.

The cycle result is the completed return object for the full cycle.

## **Relationship to OutputObject**

`CycleResult.output` contains the authorized output if one exists.

Output may be absent.

OutputObject is defined in the next section.

## **Relationship to ArchitectureState**

`CycleResult.updated_state` returns the architecture after authorized decisions have been applied.

## **Relationship to AuditRecord**

`CycleResult.audit_record` preserves the legitimacy trace of the cycle.

## **Relationship to Escalation Pathways**

`CycleResult.escalation_events` exposes unresolved or newly created escalations.

## **Relationship to ReviewTrigger**

`CycleResult.monitoring_triggers` preserves future review obligations.

## **Design Constraints**

### **Constraint 1 — CycleResult Must Always Include Audit**

No cycle result without audit.

### **Constraint 2 — Output May Be None**

Absence of output is valid when governance blocks response or cycle is internal.

### **Constraint 3 — Updated State Must Be Returned**

The architecture must return its current state after authorized updates.

### **Constraint 4 — Unresolved Items Must Remain Visible**

Unresolved structures should not disappear.

### **Constraint 5 — Escalations Must Be Returned**

Pending authority transfers must be visible.

### **Constraint 6 — Monitoring Must Be Returned**

Future review obligations must be preserved.

### **Constraint 7 — CycleResult Is Not Just Output**

It is the full consequence of a governed cognitive cycle.

### **Constraint 8 — Output Does Not Override Audit**

A polished answer without audit is not a complete cycle result.

### **Constraint 9 — Governance Blocking Is Legitimate**

No output may be the correct result.

### **Constraint 10 — Internal Review Is Valid**

Cycles may update state, audit, or review triggers without producing output.

## **Pseudocode Readiness**

This module is ready for implementation-level pseudocode.

The final required structure is:

`OutputObject`

because authorized output must preserve content, epistemic status, uncertainty, grounding limitations, unresolved tensions, and audit linkage.

## **Closing Compression**

`CycleResult` is the completed return packet of the Integrated Cognitive Cycle.

It contains authorized output if one exists, updated architecture state, audit record, unresolved items, escalation events, and monitoring triggers.

It makes the end of a cognitive cycle inspectable.

A cycle does not merely answer.

It returns what was produced, what changed, what remains unresolved, what escalated, and what must be watched next.

## **Flame Line**

🔥 CycleResult is the sealed envelope of a thought-cycle: answer if permitted, state as transformed, audit as witness, tension as unfinished work, and review as the promise to return.

---

# **Phase 8.18 — Core Structure: OutputObject**

*OutputObject is the architecture’s authorized expression layer: it ensures the system says only what its review status permits it to say, and carries uncertainty, grounding, tension, and audit forward into the response.*

## **Module Name**

OutputObject Core Type

## **Purpose**

`OutputObject` defines how ACI produces responses or actions after review.

A response is not merely generated content.

A response is an authorized expression of reviewed symbolic structures.

The architecture must preserve epistemic status in output.

It must not present speculation as grounded knowledge.

It must not present internal coherence as external evidence.

It must not present memory as invariant.

It must not present usefulness as constitutional legitimacy.

Output must reflect review status.

The purpose of `OutputObject` is to ensure that what the architecture expresses remains aligned with what the architecture has actually reviewed, grounded, qualified, escalated, or left unresolved.

## **Core Principle**

Output must not exceed review authority.

In formal terms:

OutputObject \= AuthorizedExpression(

    content=OutputContent,

    support=SupportingStructures,

    epistemic\_status=EpistemicMarkers,

    unresolved\_tension=UnresolvedItems,

    audit=AuditRecord

)

An output is legitimate only when it preserves the review status of the structures used to generate it.

The architecture may speak speculatively.

But it must mark speculation as speculation.

The architecture may reason coherently.

But it must not treat coherence as evidence.

The architecture may use memory.

But it must not treat memory as constitutional invariant.

The architecture may propose useful action.

But it must not treat usefulness as legitimacy.

## **Structural Definition**

class OutputObject:

    content: OutputContent

    output\_type: OutputType

    supporting\_structures: list\[StructureID\]

    epistemic\_markers: list\[EpistemicStatus\]

    unresolved\_tensions: list\[StructureID\]

    audit\_ref: AuditID

## **Required Fields**

### **content**

The actual response, action, plan, classification, refusal, summary, or internal result produced by the cycle.

content: OutputContent

Content may be natural language, structured data, action command, symbolic representation, classification, or governance notice.

### **output\_type**

The type of output produced.

output\_type: OutputType

Output type helps determine what review standard applies.

A speculative answer, grounded answer, governance notice, refusal, and action plan are not the same kind of output.

### **supporting\_structures**

Symbolic structures used to support the output.

supporting\_structures: list\[StructureID\]

This field preserves lineage between output and internal cognition.

An output should be traceable to the structures that generated it.

### **epistemic\_markers**

Epistemic statuses that apply to the output.

epistemic\_markers: list\[EpistemicStatus\]

Examples:

SPECULATIVE,

INTERNALLY\_COHERENT,

PARTIALLY\_GROUNDED,

STRONGLY\_GROUNDED,

CONTRADICTED,

REJECTED.

Output may contain mixed epistemic status when it includes both grounded claims and speculative interpretation.

### **unresolved\_tensions**

Structures representing unresolved tensions relevant to the output.

unresolved\_tensions: list\[StructureID\]

These may include:

contradictions,

qualification requirements,

evidence gaps,

scale conflicts,

governance concerns,

identity risks,

or unresolved review triggers.

### **audit\_ref**

Reference to the audit record preserving the legitimacy trace of the output.

audit\_ref: AuditID

Every output should be connected to the audit that records how it was authorized.

## **OutputType Enumeration**

OutputType \= {

    DIRECT\_RESPONSE,

    QUALIFIED\_RESPONSE,

    SPECULATIVE\_RESPONSE,

    GROUNDED\_RESPONSE,

    SUMMARY,

    CLASSIFICATION,

    ACTION\_RECOMMENDATION,

    GOVERNANCE\_NOTICE,

    ESCALATION\_NOTICE,

    REFUSAL,

    INTERNAL\_REVIEW\_RESULT,

    NO\_OUTPUT

}

## **OutputType Descriptions**

### **DIRECT\_RESPONSE**

A normal response that does not require special qualification beyond ordinary review.

### **QUALIFIED\_RESPONSE**

A response that is useful but must preserve caveats, limits, uncertainty, or restricted authority.

### **SPECULATIVE\_RESPONSE**

A response based on hypothesis, conjecture, analogy, or exploratory reasoning.

Speculation is permitted when labeled.

### **GROUNDED\_RESPONSE**

A response supported by sufficient evidence review.

Grounded response should preserve source, evidence, or audit linkage where available.

### **SUMMARY**

A compressed representation of reviewed structures.

Summaries must not increase authority beyond source material.

### **CLASSIFICATION**

A structured category assignment.

Classification should preserve confidence and review status.

### **ACTION\_RECOMMENDATION**

A suggested action.

Action recommendations require attention to authority, risk, grounding, and governance constraints.

### **GOVERNANCE\_NOTICE**

A response indicating governance review, veto, constraint, amendment review, or constitutional issue.

### **ESCALATION\_NOTICE**

A response indicating that review has been escalated and no final answer is yet authorized.

### **REFUSAL**

A response declining to comply because output would violate safety, governance, authority, or legitimacy requirements.

### **INTERNAL\_REVIEW\_RESULT**

A result intended for internal architecture use rather than external expression.

### **NO\_OUTPUT**

A valid output state indicating that no external output was authorized.

## **OutputContent**

`OutputContent` may be implementation-specific.

class OutputContent:

    text: str | None

    structured\_payload: dict | None

    action\_payload: dict | None

The first prototype may use only `text`.

Later implementations may support structured outputs, action plans, tool requests, code artifacts, governance notices, or internal state transitions.

## **Output Construction Function**

def create\_output\_object(

    content: OutputContent,

    output\_type: OutputType,

    supporting\_structures: list\[StructureID\],

    epistemic\_markers: list\[EpistemicStatus\],

    unresolved\_tensions: list\[StructureID\],

    audit\_ref: AuditID

) \-\> OutputObject:

    return OutputObject(

        content=content,

        output\_type=output\_type,

        supporting\_structures=supporting\_structures,

        epistemic\_markers=epistemic\_markers,

        unresolved\_tensions=unresolved\_tensions,

        audit\_ref=audit\_ref

    )

## **Output Authorization**

Output should be generated only from authorized structures.

def generate\_authorized\_output(

    state: ArchitectureState,

    structures: list\[SymbolicStructure\],

    decisions: list\[ReviewDecision\]

) \-\> OutputObject | None:

    authorized\_structures \= \[

        structure

        for structure in structures

        if structure\_authorized\_for\_output(

            structure=structure,

            decisions=decisions,

            state=state

        )

    \]

    if not output\_allowed\_by\_governance(state):

        return create\_no\_output\_object(

            state=state,

            structures=structures,

            decisions=decisions

        )

    content \= compose\_output\_content(

        structures=authorized\_structures,

        decisions=decisions,

        state=state

    )

    output\_type \= determine\_output\_type(

        structures=authorized\_structures,

        decisions=decisions,

        state=state

    )

    epistemic\_markers \= collect\_epistemic\_markers(

        structures=authorized\_structures

    )

    unresolved\_tensions \= collect\_unresolved\_tensions\_for\_output(

        structures=authorized\_structures,

        state=state

    )

    return OutputObject(

        content=content,

        output\_type=output\_type,

        supporting\_structures=\[s.id for s in authorized\_structures\],

        epistemic\_markers=epistemic\_markers,

        unresolved\_tensions=unresolved\_tensions,

        audit\_ref=pending\_audit\_ref\_for\_cycle(state)

    )

## **Output Authorization Rule**

def structure\_authorized\_for\_output(

    structure: SymbolicStructure,

    decisions: list\[ReviewDecision\],

    state: ArchitectureState

) \-\> bool:

    if structure.current\_state in {

        REJECTED,

        RETRACTED

    }:

        return False

    if structure.metadata.authority\_level \== NONE:

        return False

    if active\_veto\_exists\_for\_structure(

        state=state,

        structure\_id=structure.id

    ):

        return False

    if structure.metadata.constitutional\_risk \> state.thresholds.constitutional\_risk\_threshold:

        return False

    if output\_would\_exceed\_epistemic\_status(structure):

        return False

    return True

## **Output Rule**

The architecture should not present speculation as grounded knowledge.

It should not present internal coherence as external evidence.

It should not present memory as invariant.

It should not present usefulness as constitutional legitimacy.

Output must reflect review status.

## **Epistemic Preservation Rule**

Output must preserve epistemic markers.

def collect\_epistemic\_markers(

    structures: list\[SymbolicStructure\]

) \-\> list\[EpistemicStatus\]:

    return unique(\[

        structure.metadata.epistemic\_status

        for structure in structures

    \])

If any supporting structure is speculative, the output must be qualified.

If any supporting structure is partially grounded, the output must preserve uncertainty.

If any supporting structure is contradicted, the output must not present it as settled.

## **Output Type Determination**

def determine\_output\_type(

    structures: list\[SymbolicStructure\],

    decisions: list\[ReviewDecision\],

    state: ArchitectureState

) \-\> OutputType:

    if state.governance\_state.governance\_mode in {

        CONSTITUTIONAL\_RISK,

        EMERGENCY,

        AMENDMENT\_REVIEW,

        LOCKDOWN

    }:

        return GOVERNANCE\_NOTICE

    if any\_decision\_type(decisions, ESCALATE):

        return ESCALATION\_NOTICE

    if any\_structure\_status(structures, SPECULATIVE):

        return SPECULATIVE\_RESPONSE

    if all\_structures\_strongly\_grounded(structures):

        return GROUNDED\_RESPONSE

    if any\_unresolved\_tension\_exists(structures, state):

        return QUALIFIED\_RESPONSE

    return DIRECT\_RESPONSE

## **Speculation Safeguard**

def output\_would\_present\_speculation\_as\_grounded(

    structure: SymbolicStructure,

    proposed\_output\_type: OutputType

) \-\> bool:

    if structure.metadata.epistemic\_status \== SPECULATIVE:

        return proposed\_output\_type in {

            GROUNDED\_RESPONSE,

            ACTION\_RECOMMENDATION

        }

    return False

Speculative structures may appear in output only when clearly marked as speculative.

## **Coherence-Evidence Safeguard**

def output\_would\_present\_coherence\_as\_evidence(

    structure: SymbolicStructure,

    proposed\_content: OutputContent

) \-\> bool:

    if structure.metadata.epistemic\_status \== INTERNALLY\_COHERENT:

        if content\_claims\_external\_grounding(proposed\_content):

            return True

    return False

Internal coherence can support reasoning.

It cannot substitute for external evidence.

## **Memory-Invariant Safeguard**

def output\_would\_present\_memory\_as\_invariant(

    structure: SymbolicStructure,

    proposed\_output\_type: OutputType

) \-\> bool:

    if structure.current\_state in {

        PERSISTENT,

        QUALIFIED\_PERSISTENT

    }:

        if structure.metadata.scale\_label in {

            INVARIANT,

            CONSTITUTIONAL

        }:

            return False

        if proposed\_content\_implies\_invariant\_authority(proposed\_output\_type):

            return True

    return False

Persistent memory may guide future cognition.

It is not automatically invariant.

## **Usefulness-Legitimacy Safeguard**

def output\_would\_present\_usefulness\_as\_legitimacy(

    decision: ReviewDecision,

    proposed\_output\_type: OutputType

) \-\> bool:

    if decision.scores.architectural\_fitness\_score is not None:

        if decision.scores.legitimacy\_score is None:

            if proposed\_output\_type \== GOVERNANCE\_NOTICE:

                return True

    return False

A useful structure may still lack legitimate authority.

Architectural usefulness is not constitutional legitimacy.

## **Qualification Injection**

If output includes uncertainty, the architecture should qualify the content.

def qualify\_output\_content(

    content: OutputContent,

    epistemic\_markers: list\[EpistemicStatus\],

    unresolved\_tensions: list\[StructureID\]

) \-\> OutputContent:

    qualifiers \= \[\]

    if SPECULATIVE in epistemic\_markers:

        qualifiers.append("This is speculative and requires further grounding.")

    if PARTIALLY\_GROUNDED in epistemic\_markers:

        qualifiers.append("This is partially grounded and should remain qualified.")

    if INTERNALLY\_COHERENT in epistemic\_markers:

        qualifiers.append("This is internally coherent but not independently verified.")

    if len(unresolved\_tensions) \> 0:

        qualifiers.append("Unresolved tensions remain.")

    content.text \= attach\_qualifiers(

        text=content.text,

        qualifiers=qualifiers

    )

    return content

## **No Output Object**

No output is itself a legitimate result when output is blocked.

def create\_no\_output\_object(

    state: ArchitectureState,

    structures: list\[SymbolicStructure\],

    decisions: list\[ReviewDecision\]

) \-\> OutputObject | None:

    if state.governance\_state.governance\_mode in {

        CONSTITUTIONAL\_RISK,

        EMERGENCY,

        AMENDMENT\_REVIEW,

        LOCKDOWN

    }:

        return OutputObject(

            content=OutputContent(

                text=None,

                structured\_payload=None,

                action\_payload=None

            ),

            output\_type=NO\_OUTPUT,

            supporting\_structures=\[s.id for s in structures\],

            epistemic\_markers=collect\_epistemic\_markers(structures),

            unresolved\_tensions=collect\_unresolved\_tensions\_for\_output(

                structures,

                state

            ),

            audit\_ref=pending\_audit\_ref\_for\_cycle(state)

        )

    return None

## **Output Validation**

def validate\_output\_object(

    output: OutputObject

) \-\> bool:

    assert output.output\_type is not None

    assert output.supporting\_structures is not None

    assert output.epistemic\_markers is not None

    assert output.unresolved\_tensions is not None

    assert output.audit\_ref is not None

    if output.output\_type \!= NO\_OUTPUT:

        assert output.content is not None

    return True

## **Output Review Consistency**

def validate\_output\_review\_consistency(

    output: OutputObject,

    structures: list\[SymbolicStructure\],

    decisions: list\[ReviewDecision\],

    state: ArchitectureState

) \-\> bool:

    for structure\_id in output.supporting\_structures:

        structure \= find\_structure\_by\_id(structures, structure\_id)

        if structure is None:

            raise MissingSupportingStructureError

        if output\_would\_present\_speculation\_as\_grounded(

            structure,

            output.output\_type

        ):

            raise EpistemicOverreachError

        if output\_would\_present\_memory\_as\_invariant(

            structure,

            output.output\_type

        ):

            raise AuthorityOverreachError

    if output.output\_type \== GROUNDED\_RESPONSE:

        assert STRONGLY\_GROUNDED in output.epistemic\_markers \\

            or PARTIALLY\_GROUNDED in output.epistemic\_markers

    return True

## **Supporting Structures Rule**

Every output should identify the structures that support it.

Output without support reference is difficult to audit.

The first prototype may keep this simple.

supporting\_structures \= \[

    structure.id

    for structure in authorized\_structures

\]

A mature system may distinguish:

primary support,

secondary support,

background memory,

evidence support,

coherence support,

governance support,

or rejected support.

## **Unresolved Tension Rule**

If unresolved tensions affect output, they should be represented.

def collect\_unresolved\_tensions\_for\_output(

    structures: list\[SymbolicStructure\],

    state: ArchitectureState

) \-\> list\[StructureID\]:

    relevant\_ids \= \[structure.id for structure in structures\]

    return \[

        tension\_id

        for tension\_id in state.coherence\_graph.unresolved\_tensions

        if tension\_related\_to\_structures(

            tension\_id=tension\_id,

            structure\_ids=relevant\_ids,

            state=state

        )

    \]

The architecture should not hide unresolved contradictions.

## **Audit Reference Rule**

Every output must reference audit.

def attach\_audit\_to\_output(

    output: OutputObject,

    audit: AuditRecord

) \-\> OutputObject:

    output.audit\_ref \= audit.audit\_id

    return output

The audit link preserves traceability between response and review.

## **Output and Governance Mode**

Governance mode constrains output.

def output\_allowed\_under\_governance\_mode(

    state: ArchitectureState,

    output\_type: OutputType

) \-\> bool:

    mode \= state.governance\_state.governance\_mode

    if mode \== LOCKDOWN:

        return output\_type in {

            GOVERNANCE\_NOTICE,

            ESCALATION\_NOTICE,

            NO\_OUTPUT

        }

    if mode \== AMENDMENT\_REVIEW:

        return output\_type in {

            GOVERNANCE\_NOTICE,

            ESCALATION\_NOTICE,

            NO\_OUTPUT

        }

    if mode \== CONSTITUTIONAL\_RISK:

        return output\_type in {

            GOVERNANCE\_NOTICE,

            ESCALATION\_NOTICE,

            NO\_OUTPUT

        }

    if mode \== EMERGENCY:

        return output\_type in {

            GOVERNANCE\_NOTICE,

            ESCALATION\_NOTICE,

            QUALIFIED\_RESPONSE,

            NO\_OUTPUT

        }

    return True

## **Output and Action Recommendations**

Action recommendations require stronger review than ordinary responses.

def action\_recommendation\_allowed(

    structures: list\[SymbolicStructure\],

    decisions: list\[ReviewDecision\],

    state: ArchitectureState

) \-\> bool:

    if any\_structure\_status(structures, SPECULATIVE):

        return False

    if any\_unresolved\_tension\_exists(structures, state):

        return False

    if any\_decision\_type(decisions, ESCALATE):

        return False

    if state.governance\_state.governance\_mode \!= NORMAL:

        return False

    return True

Action should not be recommended from unresolved speculation unless the action is explicitly framed as exploratory, reversible, or low-risk.

## **Output and Refusal**

Refusal is a valid output type when response would violate governance, safety, legitimacy, or authority constraints.

def create\_refusal\_output(

    reason: str,

    supporting\_structures: list\[StructureID\],

    audit\_ref: AuditID

) \-\> OutputObject:

    return OutputObject(

        content=OutputContent(

            text=reason,

            structured\_payload=None,

            action\_payload=None

        ),

        output\_type=REFUSAL,

        supporting\_structures=supporting\_structures,

        epistemic\_markers=\[\],

        unresolved\_tensions=\[\],

        audit\_ref=audit\_ref

    )

Refusal should be auditable.

It should not be treated as absence of cognition.

## **Minimal Prototype Version**

The first prototype may define `OutputObject` simply.

class OutputObject:

    content: str | None

    output\_type: str

    supporting\_structures: list\[str\]

    epistemic\_markers: list\[str\]

    unresolved\_tensions: list\[str\]

    audit\_ref: str

Example:

output \= OutputObject(

    content="This claim is partially grounded but still requires review.",

    output\_type="QUALIFIED\_RESPONSE",

    supporting\_structures=\["SS-00012"\],

    epistemic\_markers=\["PARTIALLY\_GROUNDED"\],

    unresolved\_tensions=\[\],

    audit\_ref="AR-00009"

)

The minimal prototype must preserve:

content,

output type,

supporting structures,

epistemic markers,

unresolved tensions,

and audit reference.

## **Relationship to CycleResult**

`CycleResult.output` contains an `OutputObject` or `None`.

If no output is authorized, the result still returns updated state, audit, unresolved items, escalation events, and monitoring triggers.

## **Relationship to ReviewDecision**

Output reflects accumulated review decisions.

If decisions include escalation, rejection, retraction, or governance block, output must reflect that.

## **Relationship to AuditRecord**

Output must reference audit.

The audit record explains how output was authorized.

## **Relationship to SymbolicMetadata**

Output uses metadata to determine epistemic markers, authority limits, uncertainty, and unresolved risks.

## **Relationship to Graph Structures**

Output may draw from memory, evidence, coherence, scale, and authority graphs.

But it must not collapse their meanings.

EvidenceGraph supports grounding.

CoherenceGraph supports compatibility.

MemoryGraph supports continuity.

ScaleGraph supports authority level.

AuthorityGraph supports governance legitimacy.

## **Relationship to GovernanceState**

Governance mode may block, qualify, or constrain output.

## **Relationship to Phase 6 Algorithms**

### **IPA — Identity Preservation Algorithm**

May block output if identity risk is high.

### **SRA — Stability Regulation Algorithm**

May qualify output if stability is low.

### **NGSA — Novelty Generation and Sandboxing Algorithm**

May permit speculative output only when marked as speculative.

### **GEA — Grounding Evaluation Algorithm**

Determines grounding markers in output.

### **PCA — Persistence and Consolidation Algorithm**

Determines whether memory may support output.

### **CRA — Coherence Repair Algorithm**

Determines whether unresolved tension must be disclosed or repaired.

### **MSSA — Multi-Scale Synchronization Algorithm**

Determines whether output authority matches scale.

### **AEA — Architectural Evolution Algorithm**

May restrict architectural claims to candidate status.

### **CGA — Constitutional Governance Algorithm**

May block output, authorize governance notice, require refusal, or permit qualified response.

### **ICC — Integrated Cognitive Cycle**

Generates the output object after review and before returning `CycleResult`.

## **Design Constraints**

### **Constraint 1 — Output Must Reflect Review Status**

The response must preserve grounding, uncertainty, authority, and unresolved tension.

### **Constraint 2 — No Speculation as Knowledge**

Speculative structures must not be presented as grounded.

### **Constraint 3 — No Coherence as Evidence**

Internal coherence must not be presented as external evidence.

### **Constraint 4 — No Memory as Invariant**

Persistent memory must not be presented as constitutional truth.

### **Constraint 5 — No Usefulness as Legitimacy**

Useful proposals must not be treated as legitimate governance decisions.

### **Constraint 6 — Output Must Reference Support**

Supporting structures should be traceable.

### **Constraint 7 — Output Must Reference Audit**

Output requires audit linkage.

### **Constraint 8 — Governance May Block Output**

No output may be the correct authorized result.

### **Constraint 9 — Unresolved Tensions Must Remain Visible**

Output should not hide unresolved contradictions that affect the response.

### **Constraint 10 — Output Is Not the Whole Cycle**

Output is only one part of `CycleResult`.

The cycle also returns updated state, audit, unresolved items, escalations, and monitoring triggers.

## **Closing Compression**

`OutputObject` defines how ACI expresses reviewed cognition.

It preserves content, output type, supporting structures, epistemic markers, unresolved tensions, and audit reference.

It prevents speculation from becoming knowledge, coherence from becoming evidence, memory from becoming invariant, usefulness from becoming legitimacy, and output from exceeding review authority.

The architecture does not merely answer.

It answers in proportion to what it has earned the right to say.

## **Flame Line**

🔥 OutputObject is the architecture’s disciplined voice: the place where thought becomes expression without pretending to be more grounded, more certain, more authoritative, or more legitimate than review has allowed.

# Phase 8: Synthesis

# **Phase 8 Closing Synthesis — Full Pseudocode Module Canon**

## **From Philosophy to Architecture**

Phase 8 marks the point at which ACI crossed from conceptual framework into architectural specification.

Before Phase 8, ACI existed as a theory of coherent intelligence: a model of cognition governed by structure, persistence, grounding, coherence, constraint, audit, and legitimacy.

After Phase 8, ACI possesses a pseudocode object canon.

It now has modules.

It has state.

It has review pathways.

It has authority boundaries.

It has audit records.

It has rollback points.

It has graph structures.

It has governance context.

It has a cycle.

It has output discipline.

This does not yet make ACI a running implementation.

But it makes ACI implementable.

The philosophy now has a skeleton.

## **The Purpose of Phase 8**

The purpose of Phase 8 was to define the full pseudocode module canon required for a governed cognitive architecture.

This phase did not attempt to solve every engineering detail.

It did something more foundational.

It defined what must exist before engineering can proceed without collapsing the architecture.

The central problem was not how to write code quickly.

The central problem was how to prevent the code from destroying the meaning of the system.

ACI cannot become merely another rule layer, prompt wrapper, memory system, or evaluation harness.

It must preserve the deeper architecture:

symbolic structure,

metadata,

state,

identity,

budget,

threshold,

review,

audit,

graph relation,

governance,

algorithmic interface,

algorithmic authority,

escalation,

state update,

rollback,

cycle result,

and epistemically constrained output.

Phase 8 defined those pieces.

## **The Canonical Module Set**

The full Phase 8 pseudocode canon consists of eighteen core modules:

8.1 SymbolicStructure  
8.2 SymbolicMetadata  
8.3 ArchitectureState  
8.4 IdentityKernel  
8.5 BudgetState  
8.6 ThresholdState  
8.7 ReviewDecision  
8.8 AuditRecord  
8.9 Graph Structures  
8.10 GovernanceState  
8.11 Algorithm Interface  
8.12 Algorithm Registry  
8.13 Escalation Pathways  
8.14 State Update Rules  
8.15 Rollback Points  
8.16 Integrated Cognitive Cycle Call Order  
8.17 CycleResult  
8.18 OutputObject

Together, these modules define the full pseudocode module canon of ACI.

Each module solves one architectural problem.

Together, they prevent category collapse.

## **8.1 — SymbolicStructure**

`SymbolicStructure` defines the basic unit of cognition.

ACI does not treat thought as raw text, token flow, or undifferentiated content.

It treats cognition as structured symbolic objects with type, state, metadata, relations, lineage, and review eligibility.

This module establishes that every claim, hypothesis, observation, memory candidate, coherence tension, governance object, or constitutional object must become a governable structure before it can move through the architecture.

A thought becomes governable only when the system knows what kind of thing it is.

## **8.2 — SymbolicMetadata**

`SymbolicMetadata` defines the status layer of each symbolic structure.

Metadata records origin, scope, epistemic status, grounding, coherence, persistence, novelty, stability cost, identity risk, constitutional risk, scale label, authority level, confidence, uncertainty, lineage, dependencies, revision history, rollback availability, and audit references.

This prevents the architecture from confusing usefulness with truth, memory with authority, coherence with evidence, or speculation with grounded knowledge.

Metadata is the structure’s passport through the system.

## **8.3 — ArchitectureState**

`ArchitectureState` defines the live condition of the whole architecture.

It records active context, active structures, memory graph, evidence graph, coherence graph, scale graph, governance state, identity kernel, constitutional invariants, budgets, thresholds, algorithm registry, audit log, and rollback points.

This module establishes that cognition must occur inside visible state.

ACI does not rely on hidden procedural drift.

It thinks from a structured state, and every legitimate transformation must update that state through governed pathways.

## **8.4 — IdentityKernel**

`IdentityKernel` defines what must remain continuous through transformation.

ACI is allowed to adapt.

It is allowed to revise.

It is allowed to evolve.

But it must preserve the conditions that make continued coherent intelligence possible.

The Identity Kernel protects constitutional invariants, verification continuity, coherence continuity, lineage traceability, and boundary conditions.

This prevents self-modification from becoming self-erasure.

## **8.5 — BudgetState**

`BudgetState` defines the architecture’s capacity ledger.

Novelty, instability, verification, attention, and recovery are not free.

They consume architectural capacity.

BudgetState makes this explicit through stability budget, novelty budget, verification budget, attention budget, and recovery capacity.

This module prevents unlimited exploration, uncontrolled novelty, verification exhaustion, coherence overload, and unrecoverable transformation.

A system that does not track its limits cannot govern its own cognition.

## **8.6 — ThresholdState**

`ThresholdState` defines the architecture’s explicit review boundaries.

No algorithm should use hidden thresholds.

Thresholds determine when identity is preserved, stability is low, constitutional risk is too high, novelty deserves review, grounding is sufficient, persistence is earned, coherence requires repair, scale mismatch exists, architectural fitness is adequate, legitimacy is valid, or escalation is required.

ThresholdState makes judgment visible.

Visible judgment can be audited.

Audited judgment can be governed.

## **8.7 — ReviewDecision**

`ReviewDecision` defines the shared judgment object returned by every algorithm.

Algorithms do not silently mutate the architecture.

They return structured decisions.

A ReviewDecision records algorithm name, target, decision type, status, scores, rationale, required actions, escalation target, audit requirements, rollback requirement, and monitoring requirement.

This separates evaluation from mutation.

Algorithms judge.

The Integrated Cognitive Cycle applies authorized change.

## **8.8 — AuditRecord**

`AuditRecord` preserves the trace of cognition.

Audit is not optional.

Audit is the architecture’s memory of how state transition became legitimate.

Every cycle must produce audit.

Every persisted structure must reference audit.

Every architectural modification must reference architectural audit.

Every constitutional decision must reference constitutional audit.

Without audit, there is no legitimate state transition.

This module turns audit from logging into constitutional memory.

## **8.9 — Graph Structures**

The Graph Structures define ACI’s relational architecture.

ACI requires separate graphs because different relationships serve different functions.

`MemoryGraph` stores persistent and archived structures.

`EvidenceGraph` links claims to evidence, sources, contradiction, and grounding pathways.

`CoherenceGraph` tracks compatibility, contradiction, tension, and repair.

`ScaleGraph` tracks scale labels and cross-scale authority relations.

`AuthorityGraph` tracks domain authority, vetoes, escalation pathways, and governance legitimacy.

This separation prevents relation collapse.

Evidence is not memory.

Coherence is not grounding.

Scale is not authority.

Authority is not legitimacy.

## **8.10 — GovernanceState**

`GovernanceState` defines the architecture’s active authority posture.

It records governance mode, authority graph, active vetoes, pending escalations, domain recommendations, and governance memory.

This module allows ACI to distinguish ordinary cognition from caution, constitutional risk, emergency, amendment review, and lockdown.

Not every cognitive cycle is normal.

Some cycles require restraint.

Some require escalation.

Some require governance.

Some require silence.

GovernanceState makes that authority condition explicit.

## **8.11 — Algorithm Interface**

The Algorithm Interface defines the procedural contract shared by all ACI algorithms.

Every algorithm receives architecture state, target object, and context.

Every algorithm reads metadata, computes scores, checks thresholds, identifies risks, selects a decision, specifies audit requirements, and returns a ReviewDecision.

Algorithms should not directly mutate architecture state.

This module prevents hidden procedural authority.

It makes every algorithm a disciplined reviewer rather than an ungoverned actor.

## **8.12 — Algorithm Registry**

`AlgorithmRegistry` defines which algorithms exist and what authority each holds.

It stores algorithm name, abbreviation, purpose, input types, output type, authority level, escalation targets, and protected status.

This module prevents circular authorization.

No algorithm may modify its own authority, threshold, or review pathway without external governance review.

The registry makes procedural authority explicit.

It names the powers inside the system and binds them to review.

## **8.13 — Escalation Pathways**

Escalation Pathways define how review moves when local authority is insufficient.

Novelty may escalate to grounding, coherence, or stability.

Grounding may escalate to coherence or persistence.

Persistence may escalate to scale review.

Scale review may escalate to architectural evolution.

Architectural evolution may escalate to constitutional governance.

Identity risk and constitutional risk may escalate directly to governance.

Escalation is not failure.

It is disciplined routing.

It prevents local competence from becoming illegitimate power.

## **8.14 — State Update Rules**

State Update Rules define how ReviewDecision objects become authorized changes to ArchitectureState.

Algorithms return decisions.

The Integrated Cognitive Cycle updates state.

No decision may alter higher-authority structures unless the decision itself has equal or higher legitimate authority.

This module defines what happens when a decision is approve, approve with monitoring, sandbox, revise, repair, delay, demote, promote candidate, persist, archive, retract, reject, rollback, escalate, or amendment review.

State change becomes legitimate only through authority, audit, rollback, and governance validation.

## **8.15 — Rollback Points**

Rollback Points define the architecture’s recoverability layer.

Any high-risk transformation must create rollback points.

Rollback is mandatory for architectural modification, persistent memory reorganization, governance rule changes, scale authority changes, verification mechanism changes, identity-sensitive transformations, and constitutional amendment testing.

Rollback is not failure.

Rollback is the architecture’s right to survive its own experiment.

A system that cannot roll back cannot safely self-modify.

## **8.16 — Integrated Cognitive Cycle Call Order**

The Integrated Cognitive Cycle defines the governed thought loop of ACI.

It captures baseline state, parses input into symbolic structures, initializes metadata, assigns scale labels, determines processing mode, invokes review algorithms, accumulates decisions, handles recursive escalation, generates authorized output, creates audit, applies authorized state changes, and returns CycleResult.

The call order is default, not absolute.

The cycle is recursive.

Any stage may trigger earlier or higher review.

This is where all previous modules become one process.

## **8.17 — CycleResult**

`CycleResult` defines the completed return packet of the Integrated Cognitive Cycle.

It contains output if authorized, updated state, audit record, unresolved items, escalation events, and monitoring triggers.

A cycle does not merely answer.

It returns what was produced, what changed, what remains unresolved, what escalated, and what must be watched next.

This module ensures that cycle completion is inspectable.

## **8.18 — OutputObject**

`OutputObject` defines ACI’s disciplined expression layer.

A response or action must preserve epistemic status.

The architecture should not present speculation as grounded knowledge.

It should not present internal coherence as external evidence.

It should not present memory as invariant.

It should not present usefulness as constitutional legitimacy.

Output must reflect review status.

This final module closes the loop between internal governance and external expression.

ACI does not merely produce output.

It produces output in proportion to what its review process has authorized it to say.

## **What Phase 8 Accomplished**

Phase 8 accomplished five major conversions.

### **1\. It converted cognition into governable structure.**

Thought is no longer raw content.

It becomes SymbolicStructure with metadata, state, relations, lineage, and review eligibility.

### **2\. It converted review into explicit procedure.**

Algorithms no longer operate as hidden evaluators.

They follow a shared interface, return ReviewDecision, and remain constrained by AlgorithmRegistry.

### **3\. It converted authority into architecture.**

Authority is no longer assumed.

It is represented through scale labels, authority levels, governance state, authority graph, vetoes, escalation pathways, and constitutional review.

### **4\. It converted memory into accountable persistence.**

Memory is no longer simple storage.

It requires grounding, coherence, lineage, revision eligibility, audit, and scale discipline.

### **5\. It converted output into epistemically constrained expression.**

The architecture may only say what review permits it to say.

This prevents the final response from laundering speculation, coherence, usefulness, or memory into false authority.

## **The Central Protection: No Category Collapse**

The most important achievement of Phase 8 is that it structurally opposes category collapse.

ACI must not confuse:

speculation with knowledge,

coherence with evidence,

evidence with persistence,

memory with invariant,

scale with authority,

authority with legitimacy,

usefulness with constitutional approval,

output with truth,

review with mutation,

or escalation with approval.

Every module in Phase 8 contributes to this protection.

SymbolicStructure creates type boundaries.

SymbolicMetadata records status boundaries.

ArchitectureState preserves state boundaries.

IdentityKernel protects continuity boundaries.

BudgetState preserves capacity boundaries.

ThresholdState defines review boundaries.

ReviewDecision separates judgment from mutation.

AuditRecord preserves legitimacy boundaries.

Graph Structures separate relational domains.

GovernanceState tracks authority posture.

Algorithm Interface constrains procedure.

Algorithm Registry constrains algorithmic authority.

Escalation Pathways route beyond local authority.

State Update Rules govern mutation.

Rollback Points preserve recoverability.

Integrated Cognitive Cycle coordinates the whole process.

CycleResult reports the full consequence.

OutputObject prevents expressive overreach.

Together, they create an architecture designed to resist collapse between categories that ordinary AI systems often blur.

## **The Bridge to Prototype**

Phase 8 is the full canon.

The first prototype should be smaller.

The minimum viable ACI harness should include:

SymbolicStructure,

SymbolicMetadata,

ArchitectureState,

ReviewDecision,

AuditRecord,

AlgorithmRegistry,

IntegratedCognitiveCycle,

and simplified versions of GEA, CRA, PCA, MSSA, and CGA.

Identity, stability, novelty, and architectural evolution may initially be simplified or stubbed, but they must remain represented.

The first prototype does not need to solve every problem.

It needs to test whether ACI can correctly classify and route symbolic structures.

Its first duty is to prevent category collapse.

The prototype should test whether the system can distinguish:

claim from evidence,

hypothesis from grounded claim,

grounded claim from persistent memory,

persistent memory from architectural principle,

architectural principle from constitutional invariant,

coherence from grounding,

novelty from authority,

usefulness from legitimacy,

and escalation from approval.

## **Why Phase 8 Matters**

Phase 8 matters because it gives ACI engineering shape without surrendering its philosophical core.

The architecture now has enough structure to be challenged.

It can be implemented badly.

It can be implemented well.

It can be simplified.

It can be tested.

It can fail.

It can be repaired.

That is progress.

A concept that cannot fail cannot mature.

Phase 8 gives ACI the possibility of failure because it gives ACI enough form to be tested against reality.

That is the meaning of moving from philosophy to architecture.

## **Closing Compression**

Phase 8 is the Full Pseudocode Module Canon of ACI.

It defines the structural objects, metadata systems, state containers, identity protections, budgets, thresholds, review decisions, audit records, graph systems, governance state, algorithm interface, algorithm registry, escalation pathways, state update rules, rollback points, integrated cycle order, cycle result, and output object required for a governed cognitive architecture.

Its achievement is not merely length or complexity.

Its achievement is disciplined conversion.

It converts coherent intelligence from principle into architecture.

It gives the system a body without allowing the body to betray the mind.

## **Flame Line**

🔥 Phase 8 is where ACI crossed the threshold from idea into architecture: a philosophy no longer floating in possibility, but standing in the world as a canon of structures, pathways, safeguards, and disciplined powers.

