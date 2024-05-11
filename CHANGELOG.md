# 0.4.6

## Added

- Account status via websocket
- Fetaure from 0.4.5 "Don't emit new websocket on connection failure (websocket was never opened)" modified slightly; instead of looking at error code, we keep a boolean flag to confirm that socket was ever connected

## Changed

- Don't emit new websocket on connection failure (websocket was never opened)
- Skip utf8 validation to reduce load on websocket read

# 0.4.5

## Changed

- Don't emit new websocket on connection failure (websocket was never opened)
- Skip utf8 validation to reduce load on websocket read

# 0.4.4

## Added

- "Special" margin key create, delete, list, get information and edit ip restrictions

# 0.4.3

## Added

- Errors caught from a `400` response are now raised as a `BinanceError` which contains the body of the error as `exc.body` for easier catch of common issues

# 0.4.2

## Changed

- Don't log headers on failure anymore as they may leak API key into logs

# 0.4.1

## Added

- Margin query max transfer out amount endpoint

# 0.4.0

## Changed

- Revamp decorator so it only evaluates and signs requests on subscription, thus fixing issues with "timestamp out of recvWindow" errors

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

