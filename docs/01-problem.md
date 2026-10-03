---
doc_id: SLH-PRB-001
title: SiltHaul problem statement
project: SiltHaul
doc_type: Problem statement
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 2 update; first co-design candidate named (SLH-DDR-001); questions for the first trials
---

# SiltHaul problem statement

Flood mud is heavy, wet and contaminated, and it sits in the places hardest to reach with machines: ground-floor rooms, narrow lanes and drains. Clearing it is left to people with shovels and buckets.

## The problem

Mud has to be dug, lifted, carried out and dumped, often through a single door. OSHA lists back, knee and shoulder injuries from manual lifting among the main risks for flood clean-up workers and recommends teams for heavy items ([OSHA](https://www.osha.gov/flood/response)). The longer people spend in the mud, the longer they are exposed to contaminated water; after the Kerala floods, officials linked leptospirosis risk to contact with water contaminated by animal urine and urged clean-up volunteers to take preventive medicine ([Mongabay, 2018](https://india.mongabay.com/2018/09/leptospirosis-outbreak-causes-concern-in-kerala-after-the-floods/)).

Mechanical options exist but do not fit. Mines use powered double-drum scraper hoists, or slushers, that drag a scraper box on a pull rope and return it on a tail rope ([Mining History Association](https://www.mininghistoryassociation.org/Journal/MHJ-v22-2015-Reynolds.pdf)); a recent Sulzer design uses electric motors inside the drums and has ceased without grant ([WO2017216731A1](https://patents.google.com/patent/WO2017216731A1/en)). These are heavy, powered and built for mine drives. Excavators and loaders cannot enter homes or narrow lanes. There is no portable, hand-powered slusher for flood recovery.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Householders and volunteers | Get mud out of rooms faster and with less lifting and less time in the mud | Ground floors of homes, shops and places of worship after a flood |
| Relief NGOs and community groups | A kit that is cheap, portable, needs no fuel and can be used by untrained volunteers after a short briefing | Many sites, poor road access, limited power |
| Municipal drain and sanitation crews | Clear silted drains and lanes where machines cannot reach | Narrow streets, open drains, culverts |
| Local fabricators | Drawings using stock steel, rope and pulleys | Workshops near flood-prone areas |

## Operating environment

- Wet silt and mud of varying depth, from a thin layer to deep deposits; mixed with debris, rubbish and sometimes sewage.
- Ground-floor rooms with doorways about 0.7 to 0.9 m (28 to 35 in) wide (estimate), steps and thresholds.
- Lanes and open drains in dense neighbourhoods.
- Walls that may be weakened and wet after the flood.
- Hot, humid conditions, or cold and wet in temperate regions; no power.

## Constraints

- Prototype parts budget: USD 2,000 or less.
- Hand powered only.
- Fits through a standard doorway and into a car or small pickup.
- Anchors must not rely on flood-damaged walls; the tail sheave needs its own anchoring option.
- Buildable with hand tools and a small welder from stock steel, rope and commercial pulleys.
- Open design: hardware under CERN-OHL-S-2.0, any calculators under MIT.

## Out of scope

- Pumping standing water.
- Removing large debris such as furniture, vehicles or fallen structures.
- Motorised versions.
- Disposal and treatment of the removed mud.

## Prior work

| Prior work | What it does | Gap for these users | Source |
| --- | --- | --- | --- |
| Mine slusher (tugger-scraper) | Powered two-drum hoist drags a scraper along a mine floor and returns it by tail rope through a sheave | Compressed-air or electric, heavy, built for mines | [link](https://www.mininghistoryassociation.org/Journal/MHJ-v22-2015-Reynolds.pdf) |
| US2588657A, slusher bucket (expired) | Scraper bucket worked by lead, return and tail ropes on a portable hoist | Mining equipment for a powered hoist | [link](https://patents.google.com/patent/US2588657A/en) |
| US3532170A, slusher scraper bucket and blade assembly (expired) | Scraper bucket and blade design for slushers | Mining equipment for a powered hoist | [link](https://patents.google.com/patent/US3532170A/en) |
| WO2017216731A1, scraper winch (Sulzer, ceased) | Double-drum scraper winch with electric motors inside the drums and remote control | Powered mine winch; no hand operation | [link](https://patents.google.com/patent/WO2017216731A1/en) |

## Co-design

A disaster relief NGO, a municipal disaster management unit or a volunteer fire service with regular flood clean-up experience, who can supply realistic mud and building conditions and test the kit with volunteers. First candidate to approach (not agreed): the Kerala State Disaster Management Authority and its civil defence volunteers, since Kerala's 2018 clean-up is the case that sparked the idea (SLH-DDR-001).

## Safety

> **Safety:** Any tool that moves mud by rope puts volunteers near ropes and anchors under tension, in buildings that may be damaged and in mud that may carry sewage and disease. The design answers are in SLH-PRC-001, Safety; the clean-up hazards themselves (structure, electricity, contamination) stay with the users and local health advice.

## Questions for the first trials

These are settled by trials (TRL 4), not by design decisions:

- How well does the box fill and drag in different muds, from liquid slurry to stiff clay?
- How often is the floor slab sound enough for the tail block's drilled anchors (the only tail anchor used, SLH-DDR-001)?
- Can one capstan serve several rooms in turn without re-anchoring outside?
- How does the rope get past steps and turns in the building? The doorway ramp covers thresholds up to 110 mm; turns are out of scope for the prototype.
- Is a smaller drain version, pulled along an open channel, worth a separate variant?
