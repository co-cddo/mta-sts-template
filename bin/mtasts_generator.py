import dns.resolver
import smtplib
import ssl
import os

SKIP_TLS_CHECK = os.getenv("SKIP_TLS_CHECK", "true").lower()[0] in ["t", "1"]


def check_mail_server(mail_server: str):
    if SKIP_TLS_CHECK:
        return True

    res = False
    server = smtplib.SMTP_SSL(timeout=3)
    for port in [587, 465, 25, 2525]:
        if not res:
            try:
                server.connect(mail_server.strip(".") + ".", port=port)
                server.starttls()
                print(port, server)
                cert = ssl.DER_cert_to_PEM_cert(
                    server.sock.getpeercert(binary_form=True)
                )
                print(port, cert)
                res = True
            except Exception as err:
                print(
                    "check_mail_server: server:",
                    mail_server,
                    "port:",
                    port,
                    "error:",
                    err,
                )
    return res


def get_mail_servers(domain: str):
    mail_servers = []
    if domain and type(domain) == str and "." in domain:
        try:
            mx_records = dns.resolver.resolve(domain, "MX")
            for mx_record in mx_records:
                mail_server = str(mx_record.exchange).strip().strip(".")
                if mail_server and mail_server not in mail_servers:
                    if check_mail_server(mail_server):
                        mail_servers.append(mail_server)
        except Exception as e:
            print("get_mail_servers: error:", e)
    return sorted(mail_servers)


def get_current_txt_file(filepath: str):
    lines = []
    f = open(filepath, "r")
    for line in f:
        line = line.strip()
        if line:
            lines.append(line)
    f.close()
    return lines


def get_new_txt_lines(
    domain: str, current_txt_path: str = "../.well-known/mta-sts.txt"
):
    current_lines = get_current_txt_file(current_txt_path)
    mail_servers = get_mail_servers(domain)

    if not current_lines or not mail_servers:
        return []

    new_lines = []
    for line in current_lines:
        if not line.startswith("mx:"):
            new_lines.append(line)

    for mail_server in mail_servers:
        new_lines.append(f"mx: {mail_server}")

    return new_lines


def write_txt_lines(lines: list, txt_path: str = "../.well-known/mta-sts.txt"):
    success = False
    if lines:
        try:
            f = open(txt_path, "w")
            f.write("\n".join(lines))
            f.close()
            success = True
        except Exception as e:
            print("write_txt_lines: error:", e)
    return success
