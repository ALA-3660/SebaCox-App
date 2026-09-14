# SebaCox Phase 8: Concurrency Control & Race Condition Prevention
## “ম্যাচ থেকে প্রস্তাব”

**মূল স্লোগান:** “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”  
**ছোট পরিচিতি:** “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”

---

## 1. Concurrency Challenges in Offer Negotiation

Offer management in high-concurrency environments faces two critical race condition hazards:
1. **Concurrent Acceptance**: Two competing offers for the same demand accepted simultaneously.
2. **Conflicting Counter vs. Accept**: One party attempting to accept an offer while the other concurrently counters or cancels it.

---

## 2. Mitigation Strategies & Implementation

### 2.1 Database Row Locking (`select_for_update`)
All mutation operations (`accept_offer`, `counter_offer`, `cancel_offer`, `reject_offer`) execute inside an atomic transaction:
```python
@transaction.atomic
def accept_offer(cls, offer_id: int, user) -> Offer:
    offer = Offer.objects.select_for_update().filter(id=offer_id).first()
    ...
```

### 2.2 Demand-Level Locking on Acceptance
When accepting an offer, the parent `Demand` row is also locked to ensure that no two offers for the same Demand can both reach `ACCEPTED` status concurrently:
```python
demand = Demand.objects.select_for_update().filter(id=offer.demand_id).first()
# Check if any accepted offer already exists
existing_accepted = Offer.objects.filter(
    demand_id=demand.id,
    status=OfferStatus.ACCEPTED
).exists()
if existing_accepted:
    raise ValidationError("এই চাহিদার জন্য ইতোমধ্যে একটি প্রস্তাব গ্রহণ করা হয়েছে।")
```

### 2.3 Terminal State Check Inside Lock
Before applying state changes, the code checks if the status is still `PENDING`. If an interlacing thread changed it to `SUPERSEDED`, `CANCELLED`, or `EXPIRED`, the operation aborts gracefully.
