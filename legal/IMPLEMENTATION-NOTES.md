# Legal Implementation Notes

**Last Updated:** April 20, 2026

This note explains how to publish and surface legal documents in product interfaces.

## Where to Link What

- **Footer links on websites and app shells:**
  - Product Privacy Policy
  - Product Terms
  - Product Acceptable Use (if applicable)
  - Umbrella Outer-Void docs as secondary references when useful

- **Signup, onboarding, or account creation flows:**
  - Product Terms of Service / Terms of Use
  - Product Privacy Policy
  - Any product-specific high-risk disclaimer (AI, moderation, wellness, safety)

- **Telegram bot menus (TheResolverBot):**
  - Terms of Service
  - Privacy Policy
  - Bot & Platform Disclaimer
  - Moderation & Enforcement Policy

- **Community-driven products (DevBoard, IVRP communities, TheResolverBot-managed groups):**
  - Community Guidelines
  - Content/User Conduct policy
  - Moderation & Enforcement policy

## Precedence Rule for Maintainers

When both umbrella and product-level terms exist, the product-level terms control for product behavior, feature usage, and user interactions in that product.

## Operational Review Triggers

Update legal docs whenever you introduce or materially change:
- New user accounts or authentication flows
- New categories of user data collection
- Paid features, subscriptions, or billing logic
- Moderation automation, scoring, or enforcement systems
- AI model usage or third-party model routing
- Crisis-sensitive positioning in wellness or caregiving contexts

## Legal Review Recommendation

Before production launch at scale, have licensed counsel review jurisdiction, consumer rights, content liability, and platform-specific risk language.
