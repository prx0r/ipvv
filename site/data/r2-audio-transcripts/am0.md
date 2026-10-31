S, Recognition, and the AM0 Framework
A complete mapping of the S/{0,1}/i ontology, pratyabhijñā, Gödel, and Levin's ingression space onto the constructor-theoretic formalization of AM0
Working document

This document maps the theoretical framework developed across our conversation — the S/{0,1}/i distinction ontology, the tractatus on articulated distinction, the pratyabhiñā formalization, the Gödelian incompleteness argument, Levin’s morphogenetic ingression space, and the Tibetan bardo/rebirth mechanism — onto the AM0 constructor-theoretic formalization. The mapping operates in both directions: our framework extends and grounds several components AM0 marks as □ Formal or ✗ Unsupported, while AM0’s precision exposes where our claims require sharper specification.
Conventions: we use AM0’s evidence markers (✓ □ ? ✗) throughout. New contributions from our framework are marked [NEW]. Extensions to existing AM0 components are marked [EXT]. Components our framework leaves unchanged are marked [AM0].




1. Ontological Grounding of the Substrate Structure
AM0 defines its substrates (Definition 1.2, Section 2) without grounding why the substrate structure takes the form it does. Our tractatus supplies this grounding directly.
1.1 S as the Prior Condition of All Substrates
AM0 defines S_bio, S_neural, S_embryo, and S_env as distinct physical substrates, and M as the mental substrate. What the formalization does not address is what makes any substrate possible at all — what the condition of co-articulation is that allows states to be distinguishable within a substrate in the first place.
Our framework supplies this as S — not an additional substrate to add to AM0’s list, but the condition of articulation that all AM0 substrates presuppose:
S := condition of co-articulation by virtue of which
      any distinction D(0,1) obtains within any substrate
This means:
Every AM0 substrate (S_bio, S_neural, S_embryo, S_env, M) is a particular constraint structure C within S.
Every AM0 state m ∈ M is an i — a realised unit of distinction within S.
The AM0 formal system A = ⟨S, M, X, Σ, Π, K, T, Γ⟩ is itself a configuration of S — and therefore contains G_A: the Gödel sentence of its own substrate.
This is not in tension with AM0. It grounds it. The substrate structure of AM0 is correct; S explains why any substrate structure of this kind is possible.
[NEW] [□] S as prior condition of all AM0 substrates. Formal. Mechanism: articulation condition of any distinction whatsoever. No new empirical claims required.

1.2 The Mental State Tuple Extended
AM0 defines the mental state as m = (e, p, h, b, o). Our framework suggests a sixth component is implicit but unnamed:
m = (e, p, h, b, o, σ)
where σ ∈ {Sv, ¬Sv} is the self-grounding status of O — whether the observer-function is currently operating under the false exemption (Sv(O)) or has undergone the modal shift to ¬Sv(O) (full recognition, FR).
σ is not an additional phenomenal content. It is a structural parameter determining the topology of all other components. When σ = Sv(O), the intentional object o is experienced as independently real (the māyīyamala error). When σ = ¬Sv(O), the same o is experienced as i within S — same content, different structural positioning.
This maps onto AM0’s accessibility profile p ∈ P in a specific way: σ is the meta-parameter governing the entire profile. A state with σ = Sv(O) has a structurally different P than the same state with σ = ¬Sv(O), because what counts as OPEN vs CLOSED vs PERM changes when the observer ceases to exempt itself.
[EXT] [□] Sixth component σ ∈ {Sv, ¬Sv} as meta-parameter of mental state tuple. Formal. Physical candidate: global workspace topology, self-referential network configuration.




2. Re-cognition as a Task in AM0
This is the central contribution. AM0 defines tasks as T: α_in → α_out on substrate S. Re-cognition — the transition from PR (partial recognition) to FR (full recognition) — is a task on M, and a highly specific one: it is the only task in AM0 that changes σ rather than e, p, h, b, or o.
2.1 Formal Definition of Re-cognition
T_rec : (e, p, h, b, o, Sv(O))  →  (e, p, h, b, o, ¬Sv(O))
Note carefully what T_rec does and does not change:
Unchanged: e (event-type), p (accessibility profile content), h (history), b (buffer), o (intentional object).
Changed: σ — the structural self-positioning of O with respect to S.
This is why Re-cognition is not acquisition of new information. The tuple content is identical before and after. What changes is the operator’s relation to its own dependence — its σ parameter. This is the formal expression of the claim that FR “subtracts a false exemption rather than adding a new object.”
2.2 PR and FR as Formal States
PR := K_O[D(0,1)] ∧ Meta_O[Dep(0)] ∧ Meta_O[Dep(1)]
      ∧ Sv(O)   [observer still self-exempting]

FR := K_O[D(0,1)] ∧ Meta_O[Dep(0)] ∧ Meta_O[Dep(1)]
      ∧ Meta_O[Dep(O)]   [σ = ¬Sv(O)]
In AM0 terms:
PR is a standard cognitive state: O registers the dependence structure of the poles (0,1) while its own σ remains Sv(O). This is consistent with any h (history) and any p (profile).
FR is the same state with σ flipped. The accessibility profile P may shift as a consequence — specifically, the PERM closures corresponding to the three malas may begin to open or lock closed depending on the direction of the transition.
2.3 Mapping the Three Malas onto AM0
Abhinavagupta’s three malas are formal failure modes — structural misdescriptions that constitute the Sv(O) state. They map onto AM0 components precisely:
Mala
Formal Error
AM0 Component
Evidence
Āṇavamala
O asserts Sv(O) — takes itself as self-grounding
σ = Sv(O): meta-parameter of mental state tuple
□ Formal
Māyīyamala
O treats 0,1 as Sv(0), Sv(1) — configurations as independently real
Intentional object o experienced without E(·) marker; p profiles treating percepts as intrinsically standing
□ Formal
Kārmamala
O keeps instantiating attractors consistent with Sv(O) self-model
Attractor-lock in Γ: conditioning graph reinforces Sv(O)-consistent event-types; deep basin in h
✓ Hebbian potentiation as mechanism


Kārmamala is the only mala with a confirmed physical mechanism in AM0 terms: Hebbian potentiation and LTP/LTD (AM0 Section 7.1) straightforwardly implement the deepening of attractor basins in Γ. Repeated Sv(O)-consistent processing strengthens exactly the synaptic configurations that make Sv(O) the default. This is kārmamala as neural dynamics.
2.4 T_rec and K_path
AM0 Section 8 defines path attainment and permanent closure via magga-citta at four stages, with profile updates U₂ⁿ closing specific event-types permanently. These are the constructor-theoretic expression of the four stages of liberation in Theravada Buddhism.
T_rec as defined here maps onto the first path-attainment (stream-winner, sotapatti-magga): the irreversible shift in σ from Sv(O) to ¬Sv(O). This is the permanent closure of the āṇavamala — the root contraction. Subsequent path stages (2nd, 3rd, 4th) are the progressive closure of māyīyamala and kārmamala that follows once σ = ¬Sv(O) is stabilised.
K_path(1st) := constructor achieving T_rec
             = irreversible σ-flip from Sv(O) to ¬Sv(O)
K_path(2nd-4th) := constructors achieving progressive
             closure of māyīyamala and kārmamala
             following stable σ = ¬Sv(O)
[EXT] [□] K_path(1st) as T_rec constructor. Physical candidate: irreversible global workspace reconfiguration; permanent change in self-referential network topology. Empirically undemonstrated but direction for research identified.




3. Gödel: Every Configuration Contains Its Own G_F
AM0 does not include a Gödelian incompleteness component. Our framework adds one that has structural consequences for AM0’s modal operator Π and for the status of T_rebirth.
3.1 G_F as the Gödel Sentence of Any AM0 Configuration
For any sufficiently complex AM0 configuration F (where F is any state m ∈ M rich enough to encode its own structure):
G_F := '∃S : F is a configuration of S'
G_F is true. F cannot prove G_F from within F, because proving it would require observing S directly — which collapses S into a configuration, producing another i rather than S itself. Every observation is already post-collapse.
This has a specific consequence for AM0’s Π (task possibility valuation):
Π(T_prove_G_F) = ×   [nomologically impossible]
Π(T_enact_G_F) = ✓   [T_rec is exactly this]
The distinction between proving and enacting G_F is the distinction between demanding proof of S and operating from the structural recognition that S is the condition. T_rec is the constructor that performs T_enact_G_F. This gives T_rec a second formal definition:
T_rec = T_enact_G_F
     := the task of transitioning from
        [σ = Sv(O), demanding proof of G_F]
        to
        [σ = ¬Sv(O), enacting G_F as operating condition]
3.2 Consequence for Π and the Final Theory
AM0’s modal operator Π asks whether laws of nature permit performance of a task with unbounded accuracy. The Gödelian point (supported by Kiefer 2024 instantiating this in physics via spacetime continuum cardinality) adds a structural constraint on Π itself:
Π(T_complete_A) = ×
where T_complete_A is the task of completing AM0 — of providing a substrate-complete account of M from within M. AM0 cannot be its own complete theory. This is not a failure of AM0. It is the Gödel sentence of AM0 as a formal system. AM0 is itself a configuration of S, and G_Á0 is true and unprovable within A.
This should be added to AM0’s extension points (Section 11) as:
[NEW] [□] Add to Section 11.3: Gödelian incompleteness as structural constraint on Π. Π(T_complete_A) = ×. AM0 is itself a configuration of S and contains G_A as a live structural limit.




4. Levin’s Ingression Space as S_env Specified
AM0 defines S_env (□ Formal) as “environmental substrate — physical fields, electromagnetic patterns, structured mathematical space” with mechanism candidates including EM fields and Platonic space. Our framework, following Levin (2025), gives S_env a precise structure.
4.1 S_env as the Ingression Space
Levin’s ingression space — the structured mathematical possibility space within which morphogenetic forms exist prior to their physical instantiation — is S_env specified. It has three components that map directly onto our S/{0,1}/i framework:
Levin Component
AM0 Component
Our Framework
Evidence
Ingression space (full possibility field)
S_env (mathematical space candidate)
S as condition of articulation
□ Levin 2025 preprint
Morphogenetic constraint field C_morph
Constraint structure within S_env
C: structure of permitted differences
✓ Levin 2021 bioelectric patterns
Target morphology / attractor
A_d: dispositional attractor
A: stable basin toward which systems tend
✓ Planarian regeneration
Current organism configuration
S_bio state at time t
i: realised distinction within S
✓ Established biology


This means S_env is not one substrate among others at the same level as S_bio. S_env is the ingression space — the field of possibility within which S_bio configurations arise, persist, and are governed. S_env is C within S. S_bio states are i within C within S.
[EXT] [□→✓?] S_env specified as Levin ingression space: structured mathematical possibility field governing morphogenetic constraint structure C_morph and attractor A. Evidence: Levin (2021) ✓, Levin (2025) □. Status upgrades from □ Formal to ? Partial pending Levin (2025) peer review.
4.2 K_arch Re-specified via Ingression
AM0 defines K_arch (✓ Confirmed) as the constructor implementing bioelectric circuit self-organisation toward attractor states, citing Levin (2021). Our framework specifies the mechanism more precisely: K_arch is the constructor that performs attractor-navigation within C_morph — the morphogenetic constraint field of S_env.
Crucially: K_arch does not construct the target morphology from scratch. It navigates toward A, a pre-existing attractor in the ingression space. The organism doesn’t build its form — it recognises it. K_arch is the biological implementation of T_enact_G_F at the morphogenetic level.
K_arch := constructor performing T_enact_G_planarian
       = bioelectric navigation toward A in C_morph
       = morphogenetic Re-cognition
This is the Levin-Abhinavagupta identity stated in AM0 terms: K_arch (biological) and K_path (phenomenological) are both constructors performing variants of T_rec at different levels of complexity of i within S.
[EXT] [✓] K_arch re-specified as attractor-navigation in Levin ingression space. Confirms existing AM0 status. Adds theoretical grounding: K_arch = morphogenetic T_rec. Evidence: Levin (2021) ✓.




5. The Bardo as Uninstantiated i: Extending T_boundary
AM0’s T_boundary (□ Formal) is the most underdetermined component of the cross-life transfer sequence. Our conversation, integrating the Tibetan Book of the Dead with the Levin ingression space and the bhavanga model, provides the most complete available specification of T_boundary’s mechanism.
5.1 The Bardo as i Without Gross Instantiation
The Tibetan model describes the bardo consciousness as a mental body: not a physical body, but a structured intentional field that retains the form of the previous life while lacking gross physical substrate. In AM0 terms:
m_bardo = (e_subtle, p_bardo, h_karmic, ∅, o_subtle, ¬Sv(O)??)
The buffer b = ∅ (no active gross-body processing). The history h_karmic is the full accumulated karmic trace — the dispositional structure C_karmic carried across the death boundary. The intentional object o_subtle is the subtle-body’s field of intentionality — not mediated by sensory processing T_init but operating directly within S_env.
This is i without gross C instantiation — a karmic stream navigating S_env directly, without the filtering/localising constraint of S_bio. The bardo being’s reported clairvoyance and freedom of movement follow formally: without the localising constraint of S_bio, the stream operates at the level of C within S_env, where locality constraints are absent.
5.2 T_boundary Mechanism Specified
The mechanism of T_boundary — how C_karmic selects a specific S_embryo — is structural resonance between the karmic constraint structure and the embryonic morphogenetic field:
T_boundary : {S_env with C_karmic}
          → {S_embryo with C_morph ≈_θ C_karmic}
where ≈_θ denotes resonance-compatibility: the embryo whose ingression-space attractor A_morph is most consonant with the karmic stream’s C_karmic. This is not volitional selection. It is structural match — the same mechanism by which a morphogenetic field organises an embryo, now operating at the cross-life level.
The Tibetan description — consciousness drawn toward specific couples “by desire or revulsion” — is the phenomenology of this structural resonance from the inside of the bardo stream. Desire and revulsion are the experiential correlates of positive and negative attractor-resonance between C_karmic and C_morph.
This provides mechanism candidates for AM0’s requirements R2–R4:
AM0 Requirement
Specification from Our Framework
Status
R2: Physical channel carries individual-specific information-structure
C_karmic as structured mathematical constraint persisting in S_env (Levin ingression space) postmortem
□ Formally coherent; depends on Levin (2025)
R3: Selective addressing mechanism
Structural resonance ≈_θ between C_karmic and C_morph of candidate embryos
□ Mechanism specified; empirically undemonstrated
R4: Pattern-embryo matching criteria
Resonance-compatibility: A_morph of embryo matches C_karmic of stream within tolerance θ
□ Formal; θ undefined; research direction identified


[EXT] [□] T_boundary mechanism specified as structural resonance between C_karmic (karmic constraint structure) and C_morph (embryonic morphogenetic field) within S_env. Provides AM0 requirements R2–R4 with first formal specification. Evidence status unchanged (□) pending empirical demonstration.
5.3 The Three Tibetan Minds as AM0 Substrate Levels
The Tibetan three-mind model maps onto AM0’s substrate hierarchy precisely, resolving what AM0 leaves implicit:
Tibetan Level
AM0 Substrate
Our Framework
Function
Gross mind (ordinary cognition)
S_bio ⊕ S_neural: full bioelectric/neural substrate
i at coarse level; full C instantiation
Ordinary vitīhi processing; T_init, T_sens, T_act, T_reg
Subtle mind (karmic stream)
S_env: ingression space; C_karmic field
i without gross instantiation; C_karmic as structured constraint
Bhavaṅga continuity; cross-life transmission; bardo navigation
Very subtle mind / rigpa
S itself: condition of articulation
S prior to any C; disclosed when all localising constraint dissolves
T_rec target; σ = ¬Sv(O); pratyabhijñā; Dzogchen recognition


The brain as localising constraint — AM0’s S_bio/S_neural — is the mechanism by which the very subtle mind (S) is contracted into gross dualistic experience. This is the transmission model of consciousness stated in AM0 terms: the brain does not generate M. It constrains S into a specific C, producing the gross mind as a localised attractor within the ingression space.
Terminal lucidity (Nahm 2009) follows immediately: when S_bio is severely degraded, the localising constraint weakens. The subtle mind — C_karmic operating in S_env — is no longer being overridden by a distorted gross filter. Clarity returns not despite brain damage but because the damaged S_bio has ceased to impose its distorted C on the underlying stream.
[NEW] [?] Brain as localising constraint on S, implementing the three-tier substrate hierarchy (gross/subtle/very subtle) in AM0 terms. Physical candidate: S_bio activity as filtering/constraining mechanism on S_env. Partial evidence: terminal lucidity (Nahm 2009), NDE under cardiac arrest (van Lommel 2001). Status: ? Partial.




6. The Bhavaṅga as S_env Resting State
AM0 Section 9 defines the bhavaṅga as passive baseline state with physical candidates including DMN baseline activity and bioelectric resting states. Our framework adds a third candidate that upgrades the formal status:
T_bhavaṅga : (e_base, p, h, ∅, o_subtle) → (e_base, p, h, ∅, o_subtle)
The bhavaṅga is the resting state of C_karmic within S_env — the baseline configuration of the karmic stream when no gross-body processing (vitīhi) is occurring. It is not the absence of mind. It is the subtle-mind substrate persisting in its ground state.
This means the bhavaṅga’s intentional object o_subtle is the subtle attractor A of the stream — what the Tibetan tradition calls the ‘residual self-image’ of the bardo being, the form the karmic stream takes when not instantiated in a gross body. At death, the bhavaṅga’s o_subtle becomes the morphogenetic seed seeking a new C_morph-compatible S_embryo.
[EXT] [□→?] Bhavaṅga third physical candidate: resting state of C_karmic in S_env (Levin ingression space). This provides the cross-life continuity substrate: bhavaṅga is the subtle-mind ground state within S_env, persisting through and beyond S_bio dissolution. Status upgrades to ? Partial given Levin (2021) bioelectric resting states ✓.




7. Remote Viewing and Nonlocal Cognition as σ-Dependent Access
Our conversation raised remote viewing and nonlocal cognition as a potential consequence of T_rec. This can now be stated precisely within AM0.
7.1 Locality as S_bio Constraint
Ordinary cognition in AM0 operates on M ⊕ X: the composite substrate of mental states and external input. X is necessarily local — stimulus input arrives through S_bio’s sensory apparatus, which constrains access to the local S_bio environment.
When σ = Sv(O), O operates as a localised configuration within S_bio. Information access is bounded by the physical locality of S_bio. This is the normal operating condition of the gross mind.
When σ = ¬Sv(O) — T_rec has fired — O is no longer identifying as a localised S_bio configuration. O is recognising itself as S expressing through this particular C. The question is then: does this σ-shift have consequences for what information is accessible to O?
7.2 Three Levels of Claim
We must be precise about the strength of the claim:
Claim 1 [✓ Formal]: When σ = ¬Sv(O), the topology of experience shifts. The same content o is experienced as i within S rather than as independently real. This is structural, not epistemic — no new information is acquired, but the framing of all information changes. Follows directly from the formal definition of T_rec.
Claim 2 [□ Formal]: If S_bio functions as a localising constraint on access to S_env, then reduction of S_bio’s constraining function — whether through T_rec, deep absorption (T_jhāna), or S_bio disruption (NDE, terminal lucidity) — may permit access to information structures in S_env that are normally filtered. Physical candidate: K_boundary as S_env-access channel. Mechanism coherent but empirically undemonstrated.
Claim 3 [✗ Unsupported]: T_rec as practised by a meditator in an intact S_bio fully dissolves the locality constraint, enabling remote viewing as consistent reliable access to arbitrary S_env information. This requires the σ-shift to constitute a genuine reduction in S_bio’s localising function in a physically measurable way. Currently unsupported.
Remote viewing, if real, would be evidence for Claim 2: that S_bio normally filters S_env access and that this filter is penetrable under specific conditions. AM0’s K_boundary constructor (□ Formal) is exactly the mechanism that would implement this. T_rec may be one route to activating K_boundary.
[NEW] [□] K_boundary as S_env-access channel activated by σ-shift (T_rec), deep absorption (T_jhāna), or S_bio disruption. Provides formal grounding for nonlocal cognition claims. Status: □ Formal. Empirical test: compare S_env-access in T_rec vs control states.




8. Updated Evidence Status Table
Summary of status changes our framework introduces to AM0:
AM0 Component
Original Status
Updated Status
Basis
S_env (substrate)
□ Formal
? Partial
Levin (2025) ingression space provides precise structure
K_arch (constructor)
✓ Confirmed
✓ Extended
Re-specified as morphogenetic T_rec; adds theoretical grounding
Bhavaṅga (Section 9)
□/✓ partial
? Partial
Third candidate: C_karmic resting state in S_env
T_boundary mechanism
□ Formal
□ Specified
R2–R4 given first formal specification via resonance ≈_θ
K_path physical basis
□ Formal
□ Specified
K_path(1st) = T_rec = T_enact_G_F; σ-flip constructor
m = (e,p,h,b,o)
Definition
Extended
Sixth component σ ∈ {Sv, ¬Sv} proposed
Three-mind hierarchy
[absent]
□ New
Gross/subtle/very subtle ↔ S_bio/S_env/S substrate levels
Brain as filter
[absent]
? Partial
Localising constraint model; terminal lucidity evidence
Gödel limit on Π
[absent]
□ New
Π(T_complete_A) = ×; AM0 contains G_A
K_boundary activation
□ Formal
□ Specified
σ-shift as candidate activation mechanism





9. Open Research Directions
The mapping identifies the following empirical research directions, ordered by tractability:
Immediate (tractable with existing methods)
RD1 [✓→?] Characterise σ-parameter in neural correlates. Hypothesis: σ = ¬Sv(O) correlates with specific self-referential network topology distinct from ordinary self-awareness. Candidate: default mode network decoupling combined with maintained global workspace coherence. Method: advanced meditators during reported FR states vs controls.
RD2 [✓] Test K_arch as ingression-space navigation (Levin). Hypothesis: planarian morphogenetic targeting is not local computation but field-navigation. Method: Levin’s existing bioelectric perturbation paradigm with information-theoretic analysis of attractor geometry.
RD3 [?] Terminal lucidity as S_bio-constraint reduction. Hypothesis: terminal lucidity events correlate with specific patterns of S_bio activity reduction (not increase) in regions associated with self-referential processing. Method: longitudinal neural monitoring in dementia patients with consent protocols.
Medium-term (require new experimental paradigms)
RD4 [□] T_boundary via EM field mechanism (M2). Hypothesis: structured EM fields from dying organisms bias embryonic bioelectric patterning in species-specific ways. Method: controlled postmortem EM field measurement + embryo exposure assay.
RD5 [□] Resonance-compatibility ≈_θ as measurable parameter. Hypothesis: Stevenson-type reincarnation cases show measurable bioelectric or dispositional resonance between terminal state of previous individual and developmental trajectory of claiming child. Method: bioelectric profiling of Stevenson subjects.
RD6 [□] K_boundary activation by T_rec. Hypothesis: verified T_rec (by RD1 criteria) increases access to S_env information beyond S_bio locality. Method: remote viewing protocols with meditators stratified by RD1 neural signature.
Long-term (require theoretical advances)
RD7 [□] Formalise θ (resonance tolerance) in T_boundary. Requires: information-theoretic measure of C_karmic/C_morph compatibility. Candidate: structural similarity metric on attractor geometries in the Levin ingression space.
RD8 [□] Hilbert space representation of M with σ component (AM0 Section 11.3 extension). Map m = (e,p,h,b,o,σ) to vector in ℋ with σ as global phase parameter governing operator algebra.




10. Conclusion
The S/{0,1}/i framework, the pratyabhijñā formalization, Gödel’s incompleteness applied to physical reality, Levin’s ingression space, and the Tibetan bardo model do not merely illustrate AM0. They ground, extend, and partially specify its most underdetermined components.
The core contributions are:
S as the prior condition of all AM0 substrates — the articulation condition that makes any substrate distinction possible.
T_rec as a formally definable task: the σ-flip from Sv(O) to ¬Sv(O), identical to pratyabhijñā and to enactment of G_F.
K_arch re-specified as morphogenetic T_rec — the same formal structure as K_path at a different level of i within S.
T_boundary mechanism specified via structural resonance ≈_θ between C_karmic and C_morph within S_env (Levin ingression space).
The three-mind hierarchy (gross/subtle/very subtle) instantiated as AM0’s substrate levels (S_bio / S_env / S).
Gödelian limit on Π: AM0 is itself a configuration of S and cannot prove its own completeness from within A.
The final formal chain:
D(0,1) → S
D(0,1) → Dep(0) ∧ Dep(1) → E(0) ∧ E(1) → ¬Sv(0) ∧ ¬Sv(1)
O → Dep(O) → E(O) → ¬Sv(O)
FR = T_rec = T_enact_G_F = pratyabhijñā
   = K_path(1st) = σ-flip in AM0 mental state tuple
K_arch = T_enact_G_planarian = morphogenetic pratyabhijñā
T_boundary ≈_θ : C_karmic → C_morph within S_env
S_env = Levin ingression space = C within S
Gross mind = S_bio ⊕ S_neural = localised i
Subtle mind = C_karmic in S_env = i without gross instantiation
Very subtle mind = S itself = condition of D(0,1)
Rebirth = C_karmic finding ≈_θ-compatible C_morph in S_env
Liberation = permanent σ = ¬Sv(O) = Π(T_reopen_σ) = ×


Sources
AM0 Formalization (document provided). Borjigin et al. (2023) PNAS. Chowdhury et al. (2025) NeuroImage. Deutsch & Marletto (2015) Proc. R. Soc. A. Driscoll et al. (2022) Nature Reviews Neuroscience. Kiefer, C. (2024) Gödel’s incompleteness theorems and physics. Levin, M. (2021) Cell. Levin, M. (2025) Forms of life, forms of mind [preprint]. Nahm, M. & Greyson, B. (2009) Journal of Near-Death Studies. Nahm, M. (2021) Climbing Mount Evidence [BICS]. Stevenson, I. (1997) Reincarnation and Biology. Tung & Levin (2020) Developmental Biology. van Lommel et al. (2001) Lancet. Abhinavagupta, Tantrāloka; Pratyabhijñāhṛdayam. Bardo Thodol (tr. Coleman, Jinpa, Dorje 2007). Bhikkhu Bodhi, Comprehensive Manual of Abhidhamma.
