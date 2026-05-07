import ipaddress
import logging

logger = logging.getLogger(__name__)


def _parse_allowed(allowed: str) -> list[ipaddress.IPv4Network | ipaddress.IPv6Network | ipaddress.IPv4Address | ipaddress.IPv6Address]:
    if not (allowed or "").strip():
        return []
    out: list = []
    for part in allowed.split(","):
        p = part.strip()
        if not p:
            continue
        try:
            if "/" in p:
                out.append(ipaddress.ip_network(p, strict=False))
            else:
                out.append(ipaddress.ip_address(p))
        except ValueError:
            logger.warning("Ignored invalid IP/CIDR in at_webhook_allowed_ips: %s", p)
    return out


def client_ip_in_allowlist(client_host: str | None, allowed_raw: str) -> bool:
    allowed = _parse_allowed(allowed_raw)
    if not allowed:
        return True
    if not client_host:
        logger.warning("Webhook client IP missing; deny because allowlist is configured")
        return False
    try:
        addr = ipaddress.ip_address(client_host)
    except ValueError:
        logger.warning("Webhook client IP not parseable: %s", client_host)
        return False

    for entry in allowed:
        if isinstance(entry, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
            if addr in entry:
                return True
        elif addr == entry:
            return True
    return False


def validate_at_webhook_request(client_host: str | None, allowed_ips_csv: str, token_header: str | None, expected_token: str | None) -> tuple[bool, str | None]:
    """
    Returns (ok, error_detail). Token wins when configured; otherwise optional IP allowlist.
    """
    if expected_token:
        if token_header != expected_token:
            return False, "invalid webhook token"
        return True, None
    if allowed_ips_csv.strip():
        if not client_ip_in_allowlist(client_host, allowed_ips_csv):
            return False, "origin not allowed"
    return True, None
