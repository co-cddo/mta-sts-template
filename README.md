# mta-sts-template

This templated repository automatically deploys a GitHub Pages site for hosting a `mta-sts.txt` file.
You should be configuring a `mta-sts.txt` deployment for every domain you recieve emails with.

When [using this template](https://github.com/new?template_name=mta-sts-template&template_owner=co-cddo) you need to set the new name to the mta-sts fully qualified domain name, like `mta-sts.gc3.security.gov.uk`, this is to ensure the auto-discovery and deployment of Pages works appropriately. You can alternatively set the `MTASTS_DOMAIN` environment variable in the workflow.

By default, this repo looks up your MX records and sets the mta-sts to `testing` mode using the [configure](.github/workflows/configure.yml) workflow.

## Steps
1. Publish a TLS-RPT record, like `_smtp._tls 300 TXT "v=TLSRPTv1;rua=mailto:tls-rua@mailcheck.service.ncsc.gov.uk"`
2. Use [this template](https://github.com/new?template_name=mta-sts-template&template_owner=co-cddo), making sure to set the new repository name to the full mta-sts domain, like `mta-sts.gc3.security.gov.uk`
3. Observe the [Actions](../../actions) to make sure [configure.yml](../../actions/workflows/configure.yml) and [gh-pages.yml](../../actions/workflows/gh-pages.yml) deploy correctly
    - Make sure the build and deployment source is set to GitHub Actions in [Settings → Pages](../../settings/pages)
    - You may need to select the `main` branch and `/ root` in [Settings → Pages](../../settings/pages)
5. Configure [your DNS to point to GitHub](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
    - If deploying in [co-cddo](https://github.com/co-cddo), use the CNAME `co-cddo.github.io` (`mta-sts 60 CNAME co-cddo.github.io.`)
6. Check the `Custom domain` in [Settings → Pages](../../settings/pages) and ensure `Enforce HTTPS` is checked (this can take a few hours)
7. Check your deployment by visiting the domain, where you should get automatically redirected to `/.well-known/mta-sts.txt` (e.g. <https://mta-sts.gc3.security.gov.uk>)
8. Set your `_mta-sts` TXT record, like `_mta-sts 60 TXT "v=STSv1; id=20240215"` (where the id value is set to the current date, you'll need to change this if `mta-sts.txt` is updated)

## More information
You can find more about MTA-STS here: 
- https://www.security.gov.uk/guidance/email-guidance/mta-sts/
- https://www.ncsc.gov.uk/collection/email-security-and-anti-spoofing/using-mta-sts-to-protect-the-privacy-of-your-emails

## Example deployments
- <https://github.com/co-cddo/mta-sts.gc3.security.gov.uk>
- <https://github.com/co-cddo/mta-sts.digital.cabinet-office.gov.uk>
- <https://github.com/cabinetoffice/mta-sts.cabinetoffice.gov.uk>
