# Legal_ledger
3D ULPIN Legal Ledger &amp; Property Rights Management System —  backend for managing parties, spatial units, BAUnits, RRRs, source documents, mutations, ownership history, audit trails, and legal property summaries.

# Legal Record & Property Rights Management

Group 4 is the legal-record backend for **SIH26011: 3D ULPIN Generation and Vertical Property Mapping System**.

It manages the legal information associated with every parcel or 3D property unit, connecting the 3D-ULPIN with parties, rights, restrictions, responsibilities, source documents, mutations, ownership history, and audit records.

The main purpose of Group 4 is to answer:

> **"Who has what legal right over this 3D property?"**

## What Group 4 manages

- Party records
- 3D Spatial Unit records
- BAUnit records
- Rights, Restrictions and Responsibilities (RRR)
- Source document records
- RRR-document relationships
- Property mutations
- Mutation state management
- Ownership transfers
- Ownership history
- Mutation audit history
- Legal validation
- Consolidated legal property summaries

## Legal model

Group 4 follows concepts from **ISO 19152 LADM** for representing land-administration information.

The main concepts are:

- **Party** — person or organization involved with the property.
- **Spatial Unit** — the 3D property or spatial unit.
- **BAUnit** — the legal/administrative unit associated with the property.
- **RRR** — Rights, Restrictions and Responsibilities associated with the property.
- **Document** — source evidence supporting legal records.
- **Mutation** — transfer or change of legal ownership.
- **Mutation History** — historical record of mutation state changes.

## Party

A Party represents a person or organization involved with a property.

Examples:

- Individual owner
- Company
- Bank
- Municipal authority

Party records are associated with legal rights and property mutations.

## Spatial Unit

A Spatial Unit represents the 3D property identified by a 3D-ULPIN.

The system stores:

- 3D-ULPIN
- Unit type
- Geometry version
- Geometry hash
- Conflict status
- Effective time

The additional spatial metadata provides the basic handoff from the Group 3 spatial engine to the Group 4 legal layer.

## BAUnit

A BAUnit represents the legal/administrative unit associated with a spatial property.

Example:

```text
BAUnit: BAU-0001
3D-ULPIN: B3-1-001
Status: ACTIVE
