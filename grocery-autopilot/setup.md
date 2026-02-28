# Setup — Grocery Autopilot

## 1. Create your store account

Make sure you have:
- A grocery store account (Tesco, Sainsbury's, etc.)
- A saved payment method on the account
- A verified delivery address

## 2. Store credentials

```bash
mkdir -p ~/.openclaw/secrets
cat > ~/.openclaw/secrets/grocery_credentials.json << 'EOF'
{
  "store": "tesco",
  "email": "your@email.com",
  "password": "your-password",
  "loyalty_card": "your-card-number",
  "loyalty_verification_digits": ["digit1", "digit2", "digit3", "digit4"]
}
EOF
```

## 3. Configure delivery

Copy and edit `references/delivery-config-template.json` → `references/delivery-config.json`

## 4. Set up your shopping list

Copy and edit `references/shopping-list-template.md` → `references/shopping-list.md`

**Tips:**
- Group by category with budget allocation percentages
- List specific products by name (helps the AI find them in search)
- Include exclusions — what should NEVER be ordered
- After your first manual order, the AI can use Favourites for faster reordering

## 5. Test manually first

Ask your AI: "Do a Tesco order following the grocery-autopilot skill"

Watch it work through the browser automation. Intervene if needed. The first order teaches the AI the store's quirks.

## 6. Set up the weekly cron

```bash
openclaw cron create \
  --name "Weekly Grocery Order" \
  --expr "0 18 * * 0" \
  --tz "YOUR_TIMEZONE" \
  --message "Read and follow skills/grocery-autopilot/SKILL.md. Place the weekly grocery order." \
  --timeout 600
```

## Cost

Just your groceries. No additional API costs.
