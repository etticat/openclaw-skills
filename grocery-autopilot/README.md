# 🛒 Grocery Autopilot

**Your AI orders your groceries every week.**

Configure your store, shopping list, and delivery preferences once. Every Sunday, your AI logs in, books a slot, fills the basket, and checks out. You get a confirmation with the order number and total.

Currently supports **Tesco** (UK). Adaptable to any store with web ordering.

## How it works

1. **Login** — opens your grocery store, authenticates
2. **Book slot** — reserves delivery for your preferred day and time
3. **Build basket** — searches and adds each item from your list, prefers loyalty prices
4. **Review** — checks total is under budget
5. **Checkout** — confirms with your saved payment method
6. **Confirm** — sends you: order number, total, savings, delivery details

## Safety

- Credentials stored in encrypted secrets file — never hardcoded
- Uses the store's saved payment card — never handles card details
- Snapshots the order review before confirming
- **Alerts immediately on any payment failure** — never retries charges silently

## What you need

- [OpenClaw](https://github.com/openclaw/openclaw) with browser automation
- A grocery store account with a saved payment method

No API keys. No additional costs beyond your groceries.

## Setup

See **[setup.md](./setup.md)**. Three things to configure:

1. Store credentials (`~/.openclaw/secrets/grocery_credentials.json`)
2. Delivery address and time preferences
3. Your shopping list with budget allocations

After the first manual order, the AI can use your Favourites list for faster reordering.

## Adapting to other stores

The SKILL.md is written for Tesco but the pattern works for any grocery store with web ordering. You'll need to update: login flow, URL structure, navigation workarounds, and checkout steps.

Tested/adaptable: Tesco · Sainsbury's · Ocado · Instacart · Amazon Fresh
