import re
import os
import __main__ as main

from mtasts_generator import get_new_txt_lines, write_txt_lines

mtasts_domain = os.getenv("MTASTS_DOMAIN", None)

if not mtasts_domain:
    filename = main.__file__
    fileparts = re.split(r"[\\\/]", filename)
    mtasts_domain = fileparts[-3]

if not mtasts_domain:
    raise Exception(
        "Could not discover domain name, can be set with environment variable MTASTS_DOMAIN"
    )

mtasts_domain = mtasts_domain.lower()

domain_regex = r"^mta-sts\.(?P<domain>[a-z0-9\-\.]+\.[a-z0-9]+)$"
domain_match = re.match(domain_regex, mtasts_domain)
if not domain_match:
    raise Exception(
        "Invalid domain name - ensure format is 'mta-sts.FQDN', replacing 'FQDN' with domain where MX records are present"
    )

mail_domain = domain_match.group("domain")

print("-" * 20)
print("Using mta-sts domain name:", mtasts_domain)
print("Generating txt file using:", mail_domain)

lines = get_new_txt_lines(domain=mail_domain)
if not lines:
    raise Exception("mta-sts.txt not generated")

print("-" * 20)
print("New mta-sts.txt contents:")
print("\n".join(lines))
print("-" * 20)

write_success = write_txt_lines(lines)
if not write_success:
    raise Exception("Writing mta-sts.txt failed")

print("Successfully updated mta-sts.txt")
print("-" * 20)

f = open("../CNAME", "w")
f.write(mtasts_domain)
f.close()
print("Successfully updated CNAME with", mtasts_domain)
