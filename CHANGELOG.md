# 0.4.0

- Revamp decorator so it only evaluates and signs on subscription

# 0.3.1

## Added

- Subaccount to subaccount transfer
- User universal transfer
- Subaccount to master transfer

# 0.3.0

## Changed

- Account information http now also handles cross margin, separately from isolated
- Margin Listen key can be called with symbol (isolated) or without (cross margin)

### Breaking

- Framework methods renamed from `isolated_margin_XXX_listen_key_http_factory` to `margin_XXX_listen_key_http_factory`
- Signature of `get_account_information_http` changed to include `is_margin` boolean

# 0.2.7

## Added

- Margin available inventory

# 0.2.6

## Added

- Hourly future interest API
- Interest history API

# 0.2.4

## Added

- Max Borrowable API

# 0.2.2

## Added

- Raise API's text when available

# 0.2.0

## Added

- Symbol book ticker


# 0.1.8

## Added

- List of trades http request


# 0.1.4

## Added

- Margin borrow and repay functionalities


# 0.1.3

## Added

- Ability to create orders for margin/isolated by using the same REST function as Spot.

