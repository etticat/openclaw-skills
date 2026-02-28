---
name: grocery-autopilot
description: Automated recurring grocery ordering via browser automation. Configure your store, shopping list, budget, and delivery preferences — then let your AI order weekly on autopilot.
---

# Grocery Autopilot

Automated weekly grocery ordering via browser automation. Your AI logs into your grocery store, fills a basket from your configured shopping list, books a delivery slot, and checks out — all hands-free.

Currently supports **Tesco** (UK). The pattern is adaptable to any grocery store with a web interface.

## Prerequisites

- OpenClaw with browser automation enabled
- A grocery store account with saved payment method
- Credentials stored securely (see setup)

## Configuration

### 1. Store Credentials

Create `~/.openclaw/secrets/grocery_credentials.json`:

```json
{
  "store": "tesco",
  "email": "your@email.com",
  "password": "your-password",
  "loyalty_card": "your-clubcard-number",
  "loyalty_verification_digits": ["X", "X", "X", "X"]
}
```

### 2. Delivery Details

Edit `references/delivery-config.json`:

```json
{
  "address": "Your delivery address",
  "contact_name": "Reception / Your Name",
  "phone": "+1...",
  "instructions": "Leave at reception",
  "preferred_day": "monday",
  "preferred_time": "morning",
  "book_ahead_weeks": 2
}
```

### 3. Shopping List

Edit `references/shopping-list.md` with your recurring order. See the template for the format.

## Browser Automation Flow

### Critical: Tesco Navigation

Tesco's site intercepts normal link clicks. **Always use JavaScript navigation:**

```javascript
window.location.href = 'https://www.tesco.com/groceries/en-GB/trolley'
```

### Key URLs (Tesco)

| Page | URL |
|------|-----|
| Trolley | `https://www.tesco.com/groceries/en-GB/trolley` |
| Slots | `https://www.tesco.com/groceries/en-GB/slots` |
| Checkout | `https://www.tesco.com/groceries/en-GB/checkout` |
| Favourites | `https://www.tesco.com/groceries/en-GB/favorites` |
| Orders | `https://www.tesco.com/groceries/en-GB/orders` |

### Workflow

#### 1. Login Check
```
Navigate to store homepage
Snapshot — check if logged in (look for account name in header)
If not logged in → navigate to login, enter credentials
```

#### 2. Book Delivery Slot
```
Navigate to slots page (use JS navigation)
Snapshot — find preferred day/time slot N weeks ahead
Click to reserve slot
Confirm booking
```

#### 3. Build Basket
For each item in shopping list:
```
Use search box → type item name → wait for results
Snapshot results → find best match (prefer loyalty price items)
Click "Add" → verify added to basket
```

**Tip:** After first order, use Favourites for faster reordering.

#### 4. Review & Adjust
```
Navigate to trolley
Snapshot — verify:
  - Total under budget
  - Good variety
  - Loyalty prices applied
Adjust quantities if needed
```

#### 5. Checkout
```
Step 1: Verify delivery address
Step 2: Skip offers/recommendations
Step 3: Review order
Step 4: Confirm payment (uses saved card)
Capture order confirmation number
```

#### 6. Confirmation
Send confirmation message:
```
✅ Grocery Order Confirmed!

📦 Order #[NUMBER]
📅 Delivery: [DAY] [DATE], [TIME]
📍 [ADDRESS]
💰 Total: £[AMOUNT]
🏷️ Loyalty savings: £[SAVINGS]

[ITEM COUNT] items ordered.
```

## Error Handling

| Error | Action |
|-------|--------|
| Not logged in | Login with saved credentials |
| Session expired | Re-login, restart |
| Preferred slot unavailable | Try adjacent times, then next day |
| Over budget | Remove lowest-priority items first |
| Item unavailable | Search for alternative, note in report |
| Payment fails | **Alert user immediately** — never retry payment |
| Page errors | Retry with JS navigation |

## Cron Configuration

```json
{
  "name": "Weekly Grocery Order",
  "schedule": { "kind": "cron", "expr": "0 18 * * 0", "tz": "YOUR_TIMEZONE" },
  "payload": {
    "kind": "agentTurn",
    "message": "Read and follow skills/grocery-autopilot/SKILL.md. Place the weekly grocery order.",
    "timeoutSeconds": 600
  }
}
```

## Adapting to Other Stores

The pattern works for any grocery store with web ordering:

1. Update the credential format
2. Map the key URLs (trolley, slots, checkout)
3. Update the navigation workarounds (JS vs direct links)
4. Adjust the search → add-to-basket flow for the store's UI
5. Update the checkout step sequence

Stores tested/adaptable: Tesco (UK), Sainsbury's (UK), Ocado (UK), Instacart (US), Amazon Fresh.

## Safety

- **Never stores payment details** — uses the store's saved card
- **Credentials in secrets file** — never hardcoded
- **Always confirms before payment** — snapshots the final review step
- **Alerts on any payment failure** — never retries charges silently
