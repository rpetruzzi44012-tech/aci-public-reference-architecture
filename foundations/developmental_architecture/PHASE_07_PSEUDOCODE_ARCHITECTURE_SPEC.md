# ACI Phase 7

# **Phase 7 — Pseudocode Architecture Specification**

## **Purpose**

Phase 7 defines the shared pseudocode architecture required before the individual ACI algorithms can be written as executable procedures.

Phase 6 translated the formal models into algorithmic procedures.

Phase 7 prepares those procedures for modular implementation.

The goal is not yet to write production code.

The goal is to define the common objects, state structures, decision formats, audit records, algorithm interfaces, escalation pathways, and cycle order that all ACI pseudocode must share.

Without this specification, each algorithm could be written in isolation.

With this specification, the algorithms can operate as one architecture.

## **Primary Question**

What shared architecture must exist before the individual algorithms can be written as pseudocode?

## **Core Principle**

ACI pseudocode must treat cognition as governed symbolic state transition.

The architecture must not merely receive input and generate output.

It must receive input, parse symbolic structures, assign metadata, evaluate evidence, classify tension, regulate stability, preserve identity, determine persistence, synchronize scale, evaluate architecture-level change, escalate governance when needed, and record the entire transition.

In formal terms:

`A_{t+1} = ICC(A_t, I_t, Ω_t, K_t)`

Where:

`A_t` \= current architecture state  
`I_t` \= incoming input, disturbance, candidate, or task  
`Ω_t` \= governance rules  
`K_t` \= constitutional invariants  
`ICC` \= Integrated Cognitive Cycle  
`A_{t+1}` \= updated architecture state

The pseudocode architecture must preserve the rule:

No symbolic structure may gain deeper authority than its review pathway permits.

## **Design Goal**

The first implementation target is a generic ACI cognitive architecture.

It should be able to wrap or guide an open-source language model, reasoning system, or experimental task solver.

The architecture should remain domain-general at first.

Later, adapters may specialize it for:

ARC-style grid reasoning,

tool use,

long-term memory,

agentic planning,

research workflows,

or other cognitive tasks.

The core architecture should not be contaminated too early by any one benchmark.

ACI first.

ARC adapter later.

## **Architectural Layers**

The pseudocode architecture should be organized into five layers.

### **Layer 1 — Symbolic Layer**

Represents claims, observations, hypotheses, memories, principles, evidence items, contradictions, candidates, and transformation proposals.

Primary object:

`SymbolicStructure`

### **Layer 2 — Metadata Layer**

Tracks epistemic status, scale, grounding, coherence, novelty, persistence, lineage, revision eligibility, authority level, and risk.

Primary object:

`SymbolicMetadata`

### **Layer 3 — State Layer**

Tracks the current architecture state, including memory graph, evidence graph, coherence graph, scale graph, budgets, governance state, and constitutional invariants.

Primary object:

`ArchitectureState`

### **Layer 4 — Review Layer**

Represents the outcome of algorithmic evaluation.

Primary object:

`ReviewDecision`

### **Layer 5 — Audit Layer**

Records how cognition moved from one state to another.

Primary object:

`AuditRecord`

These layers must remain separable.

Symbolic content is not the same as metadata.

Metadata is not the same as state.

State is not the same as review.

Review is not the same as audit.

Audit preserves the developmental trail of all four.

## **Core Data Structures**

The following structures define the minimum shared architecture.

They are written in Python-like pseudocode for clarity.

This is not implementation code.

It is structural pseudocode.

## **1\. SymbolicStructure**

A `SymbolicStructure` represents any unit of cognition that may be evaluated, routed, persisted, repaired, scaled, or governed.

It may be a claim, observation, hypothesis, candidate, memory, principle, contradiction, evidence item, transformation proposal, or governance object.

class SymbolicStructure:  
    id: StructureID  
    content: SymbolicContent  
    structure\_type: StructureType  
    metadata: SymbolicMetadata  
    relations: list\[Relation\]  
    current\_state: SymbolicState

### **Required Fields**

`id`

A unique identifier.

`content`

The symbolic content itself.

Examples:

claim,

hypothesis,

observation,

model,

rule,

principle,

memory,

candidate,

or proposal.

`structure_type`

The type of symbolic structure.

Possible values:

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

`metadata`

The associated `SymbolicMetadata` object.

`relations`

Relations to other symbolic structures.

Examples:

supports,

contradicts,

depends\_on,

derived\_from,

revises,

qualifies,

generalizes,

compresses,

activates,

or escalates\_to.

`current_state`

The current state in the symbolic lifecycle.

Possible values:

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

## **2\. SymbolicMetadata**

`SymbolicMetadata` carries the governance-relevant status of a symbolic structure.

A structure without metadata is not governable.

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

### **Epistemic Status**

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

### **Scale Label**

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

### **Authority Level**

AuthorityLevel \= {  
    NONE,  
    TEMPORARY\_USE,  
    ACTIVE\_REASONING,  
    MEMORY\_INFLUENCE,  
    ARCHITECTURAL\_INFLUENCE,  
    INVARIANT\_CONSTRAINT,  
    CONSTITUTIONAL\_AUTHORITY  
}

### **Key Rule**

Scale and authority are not identical.

A structure may be labeled as persistent memory but currently authorized only for qualified use.

A structure may be an architectural candidate but not yet possess architectural authority.

The architecture must track both.

## **3\. ArchitectureState**

`ArchitectureState` represents the full current state of the ACI system.

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

### **Active Context**

The active context includes:

current task,

session history,

active goals,

constraints,

user request,

tool outputs,

retrieved memory,

and current processing mode.

class ContextState:  
    task: TaskDescription  
    session\_context: list\[SymbolicStructure\]  
    current\_mode: ProcessingMode  
    active\_constraints: list\[Constraint\]  
    active\_goals: list\[Goal\]

### **Processing Modes**

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

## **4\. IdentityKernel**

The `IdentityKernel` represents the structures that must persist through transformation.

class IdentityKernel:  
    constitutional\_invariants: list\[Invariant\]  
    verification\_continuity: VerificationState  
    coherence\_continuity: CoherenceContinuityState  
    lineage\_traceability: LineageState  
    boundary\_conditions: BoundaryState

The Identity Kernel corresponds to:

`I_K(A) = {K, V, C, L, B}`

Where:

`K` \= constitutional invariants  
`V` \= verification continuity  
`C` \= coherence continuity  
`L` \= lineage traceability  
`B` \= boundary conditions of selfhood

Any transformation affecting this object must trigger Identity Preservation Review and possibly Constitutional Governance.

## **5\. BudgetState**

ACI requires budgets because novelty, instability, transformation, and evaluation consume architectural capacity.

class BudgetState:  
    stability\_budget: float  
    novelty\_budget: float  
    verification\_budget: float  
    attention\_budget: float  
    recovery\_capacity: float

### **Stability Budget**

How much disturbance the architecture can absorb before identity risk rises.

### **Novelty Budget**

How much unresolved novelty may remain active before consolidation, sandboxing, or delay is required.

### **Verification Budget**

How much review capacity is available for claims, transformations, and governance decisions.

### **Attention Budget**

How much active complexity can be handled in a cycle.

### **Recovery Capacity**

How much instability can be corrected within a bounded interval.

## **6\. ThresholdState**

Thresholds define the review boundaries used by all algorithms.

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

Thresholds may later become configurable.

At the pseudocode level, they must be represented explicitly.

No algorithm should use hidden thresholds.

## **7\. ReviewDecision**

`ReviewDecision` represents the result of an algorithmic review.

All algorithms must return this shared object.

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

### **Decision Types**

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

### **Decision Status**

DecisionStatus \= {  
    FINAL,  
    PROVISIONAL,  
    BLOCKED,  
    ESCALATED,  
    PENDING\_REVIEW,  
    MONITORING  
}

### **ScoreBundle**

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

Not every algorithm computes every score.

But every score should have a shared location when computed.

## **8\. AuditRecord**

`AuditRecord` preserves the trace of cognition.

Audit is not optional.

Audit is the architecture’s memory of how state transition became legitimate.

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

### **Audit Rule**

Every cycle must produce at least one audit record.

Every persisted structure must reference at least one audit record.

Every architectural modification must reference a full architectural audit record.

Every constitutional decision must reference a constitutional audit record.

Without audit, there is no legitimate state transition.

## **9\. Graph Structures**

ACI requires several graph structures.

These may be simple at first.

They should be represented separately because they serve different functions.

## **MemoryGraph**

Stores persistent and archived symbolic structures.

class MemoryGraph:  
    nodes: dict\[StructureID, SymbolicStructure\]  
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

## **EvidenceGraph**

Links claims to evidence, sources, contradiction, and grounding pathways.

class EvidenceGraph:  
    claims: list\[StructureID\]  
    evidence\_items: list\[StructureID\]  
    source\_records: list\[SourceRecord\]  
    evidence\_relations: list\[EvidenceRelation\]

## **CoherenceGraph**

Tracks symbolic compatibility, contradiction, tension, and repair status.

class CoherenceGraph:  
    nodes: list\[StructureID\]  
    coherence\_relations: list\[CoherenceRelation\]  
    unresolved\_tensions: list\[StructureID\]  
    coherence\_energy: float

## **ScaleGraph**

Tracks scale labels and cross-scale authority relations.

class ScaleGraph:  
    nodes: list\[StructureID\]  
    scale\_labels: dict\[StructureID, ScaleLabel\]  
    authority\_edges: list\[AuthorityRelation\]  
    mismatch\_records: list\[ScaleMismatch\]

## **AuthorityGraph**

Tracks domain authority, vetoes, escalation pathways, and governance legitimacy.

class AuthorityGraph:  
    domains: list\[GovernanceDomain\]  
    authority\_edges: list\[AuthorityRelation\]  
    veto\_rules: list\[VetoRule\]  
    escalation\_rules: list\[EscalationRule\]

## **10\. GovernanceState**

`GovernanceState` tracks the current constitutional and authority context.

class GovernanceState:  
    governance\_mode: GovernanceMode  
    authority\_graph: AuthorityGraph  
    active\_vetoes: list\[Veto\]  
    pending\_escalations: list\[EscalationEvent\]  
    domain\_recommendations: list\[DomainRecommendation\]  
    governance\_memory: list\[AuditRecord\]

### **Governance Modes**

GovernanceMode \= {  
    NORMAL,  
    CAUTION,  
    CONSTITUTIONAL\_RISK,  
    EMERGENCY,  
    AMENDMENT\_REVIEW,  
    LOCKDOWN  
}

## **11\. Algorithm Interface**

Every ACI algorithm should follow the same interface.

def AlgorithmName(  
    state: ArchitectureState,  
    target: SymbolicStructure | Transformation | GovernanceObject,  
    context: ContextState  
) \-\> ReviewDecision:  
    ...

Every algorithm must:

receive current architecture state,

receive a target object,

read relevant metadata,

compute or update scores,

check thresholds,

select decision,

identify escalation if needed,

specify audit requirements,

and return a `ReviewDecision`.

Algorithms should not directly mutate architecture state unless explicitly authorized.

They should recommend state changes through `ReviewDecision`.

The Integrated Cognitive Cycle applies authorized state changes.

## **12\. Algorithm Registry**

The `AlgorithmRegistry` stores available algorithms and their authority.

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

### **Required Algorithms**

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

### **Registry Rule**

No algorithm may modify its own authority, threshold, or review pathway without external governance review.

This prevents circular authorization.

## **13\. Escalation Pathways**

Escalation occurs when an algorithm detects that its authority is insufficient.

### **General Escalation Function**

def escalate(  
    state: ArchitectureState,  
    target: SymbolicStructure,  
    reason: EscalationReason,  
    from\_algorithm: AlgorithmName,  
    to\_algorithm: AlgorithmName  
) \-\> EscalationEvent:  
    ...

### **Common Escalation Routes**

`NGSA → GEA`

Novelty requires evidence review.

`NGSA → CRA`

Novelty creates coherence tension.

`NGSA → SRA`

Novelty consumes too much stability budget.

`GEA → CRA`

Evidence contradicts existing symbolic structure.

`GEA → PCA`

Grounded structure seeks persistence.

`PCA → MSSA`

Persistent structure may gain authority.

`CRA → MSSA`

Tension appears to be scale mismatch.

`MSSA → AEA`

Structure may deserve architectural review.

`AEA → CGA`

Architectural modification affects protected structures.

`IPA → CGA`

Identity Kernel is at risk.

`SRA → CGA`

Instability threatens constitutional risk.

`Any Algorithm → CGA`

Authority, verification, identity, governance, or constitutional conflict appears.

## **14\. State Update Rules**

Algorithms return decisions.

The Integrated Cognitive Cycle updates state.

### **State Update Function**

def apply\_review\_decision(  
    state: ArchitectureState,  
    decision: ReviewDecision  
) \-\> ArchitectureState:  
    ...

### **Update Rules**

If decision is `APPROVE`, apply authorized local update.

If decision is `APPROVE_WITH_MONITORING`, apply update and create monitoring trigger.

If decision is `SANDBOX`, move structure into sandbox state.

If decision is `REVISE`, keep structure active but mark revision required.

If decision is `REPAIR`, route to coherence repair or appropriate repair pathway.

If decision is `DELAY`, pause integration and preserve current status.

If decision is `DEMOTE`, reduce authority level and update scale graph.

If decision is `PROMOTE_CANDIDATE`, mark for higher review without granting authority.

If decision is `PERSIST`, integrate into memory graph with metadata and lineage.

If decision is `ARCHIVE`, store as non-authoritative artifact.

If decision is `RETRACT`, remove active authority and mark retracted.

If decision is `REJECT`, mark rejected and prevent active use.

If decision is `ROLLBACK`, restore prior rollback point.

If decision is `ESCALATE`, create escalation event and invoke target review.

If decision is `AMENDMENT_REVIEW`, enter constitutional amendment pathway.

### **State Rule**

No decision may alter higher-authority structures unless the decision itself has equal or higher legitimate authority.

## **15\. Rollback Points**

Any high-risk transformation must create rollback points.

class RollbackPoint:  
    rollback\_id: RollbackID  
    state\_ref: StateID  
    affected\_structures: list\[StructureID\]  
    affected\_graphs: list\[GraphName\]  
    reason\_created: str  
    valid\_until: TimeStamp | None

Rollback is mandatory for:

architectural modification,

persistent memory reorganization,

governance rule changes,

scale authority changes,

verification mechanism changes,

identity-sensitive transformations,

and constitutional amendment testing.

## **16\. Integrated Cognitive Cycle Call Order**

The default call order for the Integrated Cognitive Cycle is:

def IntegratedCognitiveCycle(state: ArchitectureState, input: InputObject) \-\> CycleResult:  
    baseline \= capture\_baseline\_state(state)

    structures \= parse\_input\_into\_symbolic\_structures(input)

    initialize\_metadata(structures)

    assign\_initial\_scale\_labels(structures)

    mode \= determine\_processing\_mode(state, structures)

    if novelty\_required(mode, structures):  
        novelty\_decisions \= run\_NGSA(state, structures)

    route\_sandboxed\_candidates(state, novelty\_decisions)

    grounding\_decisions \= run\_GEA\_where\_required(state, structures)

    propagate\_evidence\_effects(state, grounding\_decisions)

    coherence\_decisions \= run\_CRA\_where\_required(state, structures)

    stability\_decisions \= run\_SRA\_where\_required(state, structures)

    identity\_decisions \= run\_IPA\_where\_required(state, structures)

    persistence\_decisions \= run\_PCA\_where\_required(state, structures)

    scale\_decisions \= run\_MSSA\_where\_required(state, structures)

    architecture\_decisions \= run\_AEA\_where\_required(state, structures)

    governance\_decisions \= run\_CGA\_where\_required(state, structures)

    output \= generate\_authorized\_output(state, structures)

    audit \= create\_integrated\_audit\_record(  
        baseline,  
        structures,  
        all\_decisions,  
        output  
    )

    updated\_state \= apply\_authorized\_state\_changes(state, all\_decisions, audit)

    return CycleResult(output, updated\_state, audit)

This call order is default, not absolute.

The cycle is recursive.

Any stage may trigger earlier or higher review.

For example:

Grounding may trigger coherence repair.

Coherence may trigger scale review.

Scale review may trigger architectural evolution.

Architectural evolution may trigger constitutional governance.

Stability failure may trigger identity protection.

Identity risk may trigger governance.

## **17\. CycleResult**

The Integrated Cognitive Cycle returns a cycle result.

class CycleResult:  
    output: OutputObject | None  
    updated\_state: ArchitectureState  
    audit\_record: AuditRecord  
    unresolved\_items: list\[SymbolicStructure\]  
    escalation\_events: list\[EscalationEvent\]  
    monitoring\_triggers: list\[ReviewTrigger\]

Output may be absent if governance blocks response or if the cycle is purely internal review.

## **18\. Output Object**

A response or action should preserve epistemic status.

class OutputObject:  
    content: OutputContent  
    output\_type: OutputType  
    supporting\_structures: list\[StructureID\]  
    epistemic\_markers: list\[EpistemicStatus\]  
    unresolved\_tensions: list\[StructureID\]  
    audit\_ref: AuditID

### **Output Rule**

The architecture should not present speculation as grounded knowledge.

It should not present internal coherence as external evidence.

It should not present memory as invariant.

It should not present usefulness as constitutional legitimacy.

Output must reflect review status.

## **19\. Minimal First Prototype**

The first working pseudocode prototype should be smaller than the full architecture.

The minimum viable ACI harness should include:

`SymbolicStructure`

`SymbolicMetadata`

`ArchitectureState`

`ReviewDecision`

`AuditRecord`

`AlgorithmRegistry`

`IntegratedCognitiveCycle`

and simplified versions of:

GEA,

CRA,

PCA,

MSSA,

and CGA.

Identity, stability, novelty, and architectural evolution can initially be simplified but must remain represented.

The first prototype should test whether ACI can correctly classify and route symbolic structures.

It does not need to solve every problem.

It needs to prevent category collapse.

## **20\. Prototype Testing Priorities**

Early tests should examine whether the system can distinguish:

speculation from grounded claim,

coherence from grounding,

temporary inference from memory candidate,

memory from architectural principle,

novelty from validated knowledge,

contradiction from productive tension,

authority from usefulness,

and governance from capability.

The first prototype succeeds if it produces more disciplined symbolic state transitions.

It does not need to outperform a base model immediately.

It needs to become more governable.

## **21\. ARC Adapter Boundary**

ACI core should remain generic.

ARC-specific logic should be added later as an adapter.

The ARC adapter may define:

grid state objects,

object detection structures,

transformation candidates,

task memory,

failed transformation archive,

successful abstraction patterns,

environment feedback,

action history,

and puzzle-specific grounding.

But these should not be built into the ACI core.

ACI governs cognition.

The ARC adapter supplies domain-specific structures.

## **22\. Pseudocode Conventions**

ACI pseudocode should follow these conventions.

### **Convention 1 — Explicit State**

Every function receives state explicitly.

No hidden global cognition.

### **Convention 2 — No Silent Mutation**

Algorithms return decisions.

State updates occur through authorized update functions.

### **Convention 3 — Metadata First**

No symbolic structure may proceed without metadata.

### **Convention 4 — Audit Always**

Every cycle creates an audit record.

### **Convention 5 — Scale Before Authority**

A structure must be scale-labeled before it can gain influence.

### **Convention 6 — Grounding Is Not Coherence**

Evidence status and internal compatibility must remain distinct.

### **Convention 7 — Persistence Requires Lineage**

Memory without lineage cannot become active persistent knowledge.

### **Convention 8 — Architecture Changes Require Review**

No algorithm may alter cognitive machinery without Architectural Evolution Review.

### **Convention 9 — Constitution Overrides Utility**

High usefulness cannot override protected invariant failure.

### **Convention 10 — No Self-Authorization**

No process may authorize its own modification.

## **23\. Implementation-Neutral Design**

The pseudocode architecture should not assume:

a specific programming language,

a specific model,

a specific memory database,

a specific vector store,

a specific symbolic representation,

or a specific benchmark.

It should define the logic that any implementation must preserve.

Later implementations may use:

Python objects,

JSON schemas,

graphs,

databases,

vector stores,

LLM calls,

rule engines,

or hybrid symbolic-neural systems.

The architecture is defined by governed state transition, not by implementation substrate.

## **24\. Required Pseudocode Modules**

Phase 8 should produce the following modules in order:

### **Module 1 — Core Types**

Defines symbolic structures, metadata, states, decisions, audit records, and graphs.

### **Module 2 — Architecture State Manager**

Captures baseline, applies decisions, creates rollback points, updates graphs.

### **Module 3 — Algorithm Registry**

Defines algorithm specs, authority levels, and escalation pathways.

### **Module 4 — Integrated Cognitive Cycle**

Defines the top-level cycle.

### **Module 5 — Grounding Evaluation**

First substantive review algorithm.

### **Module 6 — Coherence Repair**

Detects and routes tension.

### **Module 7 — Persistence and Consolidation**

Controls memory state.

### **Module 8 — Multi-Scale Synchronization**

Controls authority level.

### **Module 9 — Identity and Stability Guards**

Protect continuity and boundedness.

### **Module 10 — Constitutional Governance**

Validates authority.

### **Module 11 — Architectural Evolution**

Controls machinery modification.

### **Module 12 — Test Harness**

Runs controlled experiments on symbolic inputs.

## **25\. First Engineering Constraint**

The first implementation should not attempt full autonomy.

It should be a review-and-routing harness.

A base model may generate candidate reasoning.

ACI should parse, classify, evaluate, route, audit, and constrain that reasoning.

The model is not the architecture.

The model is the generative substrate.

ACI is the governance scaffold.

## **26\. Minimal Pseudocode Skeleton**

A minimal skeleton may look like this:

state \= initialize\_architecture\_state()

while input\_available:  
    input\_object \= receive\_input()

    cycle\_result \= IntegratedCognitiveCycle(  
        state=state,  
        input=input\_object  
    )

    output \= cycle\_result.output  
    state \= cycle\_result.updated\_state  
    audit \= cycle\_result.audit\_record

    present\_output(output)  
    store\_audit(audit)

This skeleton is intentionally simple.

The complexity belongs inside governed review and state transition.

## **27\. Closing Compression**

Phase 7 defines the shared architecture required for ACI pseudocode.

It establishes the symbolic objects, metadata structures, state containers, review decisions, audit records, graphs, budgets, thresholds, algorithm registry, escalation pathways, state update rules, and pseudocode conventions that allow the nine Phase 6 algorithms to operate as one coherent system.

This specification is the bridge between theory and prototype.

It does not yet implement ACI.

It defines what implementation must preserve.

The next phase can now begin writing pseudocode modules without losing architectural coherence.

## **Flame Line**

🔥 Pseudocode begins not when the architecture learns to speak in code, but when every future function knows what kind of mind it is allowed to modify.

---

