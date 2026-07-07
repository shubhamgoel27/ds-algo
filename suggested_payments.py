"""
Suggested Payments — simplified Splitwise  (Pinterest MLE screen, 2026-07-07)
============================================================================
Asked as `getSuggestedPayments`. Each transaction: a payer pays `amount`, split
EQUALLY across `payees` (the payee list may include the payer). Return who
should pay whom to settle up.

    getSuggestedPayments([
      {payer:'Alice',   amount:4000, payees:['Bob','Alice','Charlie','Daisy']},
      {payer:'Charlie', amount:2000, payees:['Alice','Charlie']},
    ])
    -> [ {payer:'Bob',   amount:1000, payees:['Alice']},
         {payer:'Daisy', amount:1000, payees:['Alice']} ]

Pattern: this is the "settle expenses between friends" family (LC 465, Optimal
Account Balancing). Two levels:
  1. Compute NET balance per person: +amount when you pay, -amount/len(payees)
     for each share you owe. Balances always sum to zero.
  2. Settle. A simple GREEDY (match debtors to creditors) gives a VALID
     settlement with at most (#people - 1) transfers in O(n log n). The
     MINIMUM-number-of-transfers version is NP-hard and needs backtracking over
     the non-zero balances (see min_transfers below) — but a phone screen wants
     the greedy, which is what was asked here.
"""
from collections import defaultdict
from typing import List, Dict


def get_suggested_payments(transactions: List[Dict]) -> List[Dict]:
    # 1. net balance: +paid, -share owed
    balance = defaultdict(float)
    for t in transactions:
        payees = t["payees"]
        share = t["amount"] / len(payees)
        balance[t["payer"]] += t["amount"]
        for p in payees:
            balance[p] -= share

    # 2. split into creditors (owed money, +) and debtors (owe money, |.|)
    EPS = 1e-9
    creditors = sorted([[p, b] for p, b in balance.items() if b > EPS])
    debtors = sorted([[p, -b] for p, b in balance.items() if b < -EPS])

    # 3. greedy two-pointer settle: each debtor pays creditors until square
    result = []
    i = j = 0
    while i < len(debtors) and j < len(creditors):
        pay = min(debtors[i][1], creditors[j][1])
        result.append({"payer": debtors[i][0], "amount": _clean(pay),
                       "payees": [creditors[j][0]]})
        debtors[i][1] -= pay
        creditors[j][1] -= pay
        if debtors[i][1] <= EPS:
            i += 1
        if creditors[j][1] <= EPS:
            j += 1
    return result


def _clean(x):
    r = round(x, 2)
    return int(r) if r == int(r) else r


# ---- Optional: the OPTIMAL (fewest transfers) version = LC 465, backtracking --
def min_transfers(transactions: List[Dict]) -> int:
    """Minimum number of transfers to settle. NP-hard; backtrack over the
    non-zero net balances. Returns the count (the interview's greedy does NOT
    minimize this, but usually isn't asked to)."""
    balance = defaultdict(float)
    for t in transactions:
        share = t["amount"] / len(t["payees"])
        balance[t["payer"]] += t["amount"]
        for p in t["payees"]:
            balance[p] -= share
    debts = [round(b, 2) for b in balance.values() if abs(b) > 1e-9]

    def dfs(i):
        while i < len(debts) and debts[i] == 0:
            i += 1
        if i == len(debts):
            return 0
        best = float("inf")
        for j in range(i + 1, len(debts)):
            if debts[j] * debts[i] < 0:                 # opposite signs can cancel
                debts[j] += debts[i]
                best = min(best, 1 + dfs(i + 1))
                debts[j] -= debts[i]
        return best
    return dfs(0)


def run_tests():
    txns = [
        {"payer": "Alice", "amount": 4000, "payees": ["Bob", "Alice", "Charlie", "Daisy"]},
        {"payer": "Charlie", "amount": 2000, "payees": ["Alice", "Charlie"]},
    ]
    out = get_suggested_payments(txns)
    expected = [
        {"payer": "Bob", "amount": 1000, "payees": ["Alice"]},
        {"payer": "Daisy", "amount": 1000, "payees": ["Alice"]},
    ]
    assert out == expected, f"got {out}"

    # settlement validity: applying result must zero every net balance
    def net(txns):
        b = defaultdict(float)
        for t in txns:
            s = t["amount"] / len(t["payees"])
            b[t["payer"]] += t["amount"]
            for p in t["payees"]:
                b[p] -= s
        return b
    b = net(txns)
    for s in out:
        b[s["payer"]] += s["amount"]      # debtor pays out
        b[s["payees"][0]] -= s["amount"]  # creditor receives
    assert all(abs(v) < 1e-6 for v in b.values()), f"unsettled: {dict(b)}"

    # single payer covering the whole group evenly
    out2 = get_suggested_payments([{"payer": "A", "amount": 300, "payees": ["A", "B", "C"]}])
    assert out2 == [{"payer": "B", "amount": 100, "payees": ["A"]},
                    {"payer": "C", "amount": 100, "payees": ["A"]}], out2

    assert min_transfers(txns) == 2
    print("All test cases passed!")


run_tests()

# Hints:
# 1. Reduce to NET balance per person first (+paid, -share). Balances sum to 0.
# 2. Greedy: sort creditors and debtors, two-pointer, pay min(debt, credit).
#    Valid settlement, <= (#people-1) transfers, O(n log n). This is the ask.
# 3. Minimum transfers (LC465) is NP-hard -> backtracking over non-zero debts.
