# ECOSIRE Fleet API — Contacts Sync Guide (MuK REST)

This guide explains how to sync Contact records (`res.partner`) between your external system and Odoo using the MuK REST API. It includes exact field mappings, payload examples, and recommended API calls.

## 1) Target Model
- Model: `res.partner`
- Purpose: Odoo Contacts (companies and individuals)

## 2) Field Mapping (External → Odoo technical)
- `first_name` → `firstname` (only if split names feature is enabled), otherwise merge into `name`
- `last_name` → `lastname` (only if split names feature is enabled), otherwise merge into `name`
- `email` → `email`
- `phone_number` → `phone`
- `contact_person_number` → `mobile`
- `address` → `street` (optionally also `street2`, `zip`, `state_id`, `country_id`)
- `vat` → `vat`
- `commercial_registration` → `commercial_registration` (custom field added by this module)
- `latitude` → `partner_latitude`
- `longitude` → `partner_longitude`
- `city_id` → Prefer `city` (Char). If you have IDs, use `state_id` (Many2one to `res.country.state`) and `country_id` (Many2one to `res.country`).

Notes:
- Full name: If split names are not enabled, send a single `name` like "John Doe". If split is enabled, you may send `firstname` and `lastname` (Odoo computes `name`).
- Location: `partner_latitude` and `partner_longitude` are built-in and editable. `location_display` is computed/read-only and not required in payloads.

## 3) Example Payloads

### 3.1 Without split names (default installations)
```json
{
  "name": "John Doe",
  "email": "johndoe@example.com",
  "phone": "+1234567890",
  "mobile": "+9876543210",
  "street": "123 Street",
  "city": "City",
  "vat": "VAT123456",
  "commercial_registration": "CR987654",
  "partner_latitude": 24.7136,
  "partner_longitude": 46.6753,
  "is_company": false
}
```

### 3.2 With split names enabled
```json
{
  "firstname": "John",
  "lastname": "Doe",
  "name": "John Doe",
  "email": "johndoe@example.com",
  "phone": "+1234567890",
  "mobile": "+9876543210",
  "street": "123 Street",
  "city": "City",
  "vat": "VAT123456",
  "commercial_registration": "CR987654",
  "partner_latitude": 24.7136,
  "partner_longitude": 46.6753,
  "is_company": false
}
```

### 3.3 With country/state IDs (recommended for clean data)
```json
{
  "name": "John Doe",
  "street": "123 Street",
  "city": "Riyadh",
  "zip": "11564",
  "state_id": 999,
  "country_id": 183,
  "vat": "VAT123456",
  "commercial_registration": "CR987654",
  "partner_latitude": 24.7136,
  "partner_longitude": 46.6753
}
```

## 4) MuK REST API Usage
MuK REST provides OAuth2 auth and an endpoint builder. After installing and configuring MuK REST:

1. Create/confirm an OAuth2 client and obtain a Bearer token.
2. Create an endpoint for model `res.partner` (MuK REST → Endpoints) and allow GET/POST/PUT/PATCH.
3. Whitelist the fields you need to read/write.
4. Use the auto-generated documentation page (MuK → Documentation) for exact URLs.

Typical request patterns (replace `{BASE_URL}` and `{YOUR_ENDPOINT}` with your values):

- Create:
```http
POST {BASE_URL}/{YOUR_ENDPOINT}/res.partner
Authorization: Bearer <token>
Content-Type: application/json

{ ...payload from section 3... }
```

- Read by ID:
```http
GET {BASE_URL}/{YOUR_ENDPOINT}/res.partner/{id}
Authorization: Bearer <token>
```

- Search:
```http
GET {BASE_URL}/{YOUR_ENDPOINT}/res.partner?domain=[["commercial_registration","=","CR987654"]]
Authorization: Bearer <token>
```

- Update:
```http
PUT {BASE_URL}/{YOUR_ENDPOINT}/res.partner/{id}
Authorization: Bearer <token>
Content-Type: application/json

{ "commercial_registration": "CR000111" }
```

## 5) Practical Mapping From External Sample
External sample:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "johndoe@example.com",
  "phone_number": "+1234567890",
  "contact_person_number": "+9876543210",
  "address": "123 Street, City",
  "vat": "VAT123456",
  "commercial_registration": "CR987654",
  "latitude": 24.7136,
  "longitude": 46.6753,
  "city_id": 22
}
```

Mapped to Odoo (no split names):
```json
{
  "name": "John Doe",
  "email": "johndoe@example.com",
  "phone": "+1234567890",
  "mobile": "+9876543210",
  "street": "123 Street",
  "city": "City",
  "vat": "VAT123456",
  "commercial_registration": "CR987654",
  "partner_latitude": 24.7136,
  "partner_longitude": 46.6753
}
```

If you truly need `city_id`, replace with `state_id`/`country_id` IDs or keep `city` as text.

## 6) Tips & Validation
- Ensure proper access rights on `res.partner` for API user.
- Use domains to find existing partners (email or `commercial_registration`) before creating new ones to avoid duplicates.
- Latitude/Longitude precision in Odoo is 10,7; send floats accordingly.
- `location_display` is computed; do not send it in write requests.
- For companies: set `is_company: true` and optionally `company_type: "company"`.

## 7) Troubleshooting
- 400/403 errors: check OAuth token, endpoint permissions, and field whitelist.
- 404 on model path: verify the endpoint path in MuK REST documentation screen.
- Write errors: check field types and required fields (`name` or split names).
- If views change but you can’t see fields: upgrade module `ecosire_fleet_api`.

---
For changes to mapping or additional fields, update this module and re-upgrade.
