from urllib.parse import urlparse


def get_hostname(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]  # Remove 'www.' from the beginning if present
    # Split the domain into its parts
    domains = []
    domain_parts = domain.split('.')
    # Adding domains to list and detect if the link is form subdomain
    if len(domain_parts) > 2:
        parent_domain = '.'.join(domain_parts[-2:])
        domains.append(parent_domain)
        domains.append(domain)
    else:
        domains.append(domain)
    if len(domains) == 1:
        domains.append(None)
    # Returning the def
    return domains
