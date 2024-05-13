import sublist3r
import requests
from concurrent.futures import ThreadPoolExecutor

# Function to get subdomains using sublist3r
def get_subdomains(domain):
    subdomains = sublist3r.main(domain, 40, None, ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)
    return subdomains

# Function to check if a URL is working
def is_link_working(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        return False
    return False

# Function to check links on subdomains
def check_subdomain_links(subdomain, working_subdomains):
    urls_to_check = [f"http://{subdomain}", f"https://{subdomain}"]
    for url in urls_to_check:
        if is_link_working(url):
            print(f"Working: {url}")
            working_subdomains.append(url)
            break  # No need to check both http and https if one is working

# Main function
def main(domain):
    subdomains = get_subdomains(domain)
    print(f"Found {len(subdomains)} subdomains")

    working_subdomains = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_subdomain_links, subdomain, working_subdomains) for subdomain in subdomains]
        for future in futures:
            future.result()  # Ensure all threads have completed

    # Output the working subdomains
    print("\nWorking subdomains:")
    for subdomain in working_subdomains:
        print(subdomain)

if __name__ == '__main__':
    target_domain = input("Enter the domain to check for subdomains: ")
    main(target_domain)
