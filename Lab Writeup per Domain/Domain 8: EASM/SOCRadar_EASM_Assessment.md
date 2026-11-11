# External Attack Surface Discovery and Exposure Analysis using SOCRadar

## 1. Objective

The objective of this assessment was to identify publicly visible assets associated with the target domain using the free edition of SOCRadar External Attack Surface Management (EASM).

The assessment focused on identifying externally visible subdomains, IP addresses, exposed network services, and technology fingerprints. The results provide an initial view of the domain's external attack surface and highlight areas that may require further security validation.

## 2. Assessment Details

| Item | Details |
|---|---|
| Tool | SOCRadar EASM – Free Edition |
| Target domain | `iiitsurat.ac.in` |
| Target URL | `https://iiitsurat.ac.in/` |
| Scan date | 11 July 2026 |
| Primary IP address | `144.16.144.17` |
| ASN | ERNET India |
| Location code | IN |

## 3. Key Findings

### 3.1 External Asset Discovery and Subdomain Enumeration

The report displayed three subdomains associated with the primary domain:

| Subdomain | IP address |
|---|---|
| `verify.iiitsurat.ac.in` | `64.29.17.65` |
| `tnp.iiitsurat.ac.in` | `199.36.158.100` |
| `alumni.iiitsurat.ac.in` | `199.36.158.100` |

**Observation:** The scan identified externally visible subdomains associated with verification, training and placement (TNP), and alumni services.

**Security relevance:** An organization's external attack surface extends beyond its primary website. Each subdomain may host a different service or application and should therefore be included in asset inventory and security reviews. The TNP and alumni subdomains were both mapped to `199.36.158.100`; this is an infrastructure relationship worth recording, but it does not by itself indicate a vulnerability.

### 3.2 Exposed Network Service and Vulnerability Indicators

The report listed the following result for the primary IP address:

| Open port | IP address | Vulnerability count reported |
|---|---|---:|
| `443` | `144.16.144.17` | 95 |

**Observation:** TCP port 443, commonly used for HTTPS, was reported as open on the primary IP address. SOCRadar also displayed 95 vulnerability indicators associated with this IP address.

**Security relevance:** Internet-facing services should be reviewed to ensure that they are securely configured and maintained. Scanner-reported vulnerability indicators can help identify areas for further investigation and patch assessment.

**Validation note:** The report does not provide the CVE identifiers, severity ratings, affected software versions, or validation evidence for the 95 entries. They should therefore be described as *scanner-reported vulnerability indicators*, not as 95 confirmed exploitable vulnerabilities.

### 3.3 Technology Fingerprinting

The report identified the following technologies against the primary IP address:

- Apache httpd
- Apache HTTP Server
- Express

**Observation:** The scan returned Apache HTTP Server and Express technology fingerprints.

**Security relevance:** Identifying externally visible technologies helps security teams determine which software components may need version verification, patch assessment, and configuration review.

**Validation note:** The report does not specify exact versions or establish that the identified technologies are outdated or vulnerable. The fingerprints should be treated as preliminary technology identification.

### 3.4 Infrastructure and Hosting Footprint

The primary IP address was associated with the following information:

| Attribute | Reported value |
|---|---|
| IP address | `144.16.144.17` |
| Location code | `IN` |
| ASN | ERNET India |

**Observation:** The scan mapped the primary domain to an externally visible IP address associated with ERNET India.

**Security relevance:** Mapping IP addresses and autonomous system information helps build an inventory of an organization's visible infrastructure and provides context for understanding its external footprint.

### 3.5 Related Domain Discovery

The report's **Related Domain Findings** section displayed **No Result Found**.

**Observation:** The free-edition scan did not return additional related domains in this section.

**Limitation:** This result does not prove that no other related domains exist. It only reflects what the tool returned within the scope and discovery coverage of this scan.

## 4. Summary of Findings

| Assessment area | Result |
|---|---|
| Primary domain | `iiitsurat.ac.in` |
| Primary IP mapping | `144.16.144.17` |
| Subdomains displayed | 3 |
| Exposed port reported | TCP 443 |
| Vulnerability indicators | 95 reported by the tool |
| Technology fingerprints | Apache httpd, Apache HTTP Server, Express |
| ASN | ERNET India |
| Related domain findings | No result found |

## 5. Security Recommendations

Based on the observations in the report, the following follow-up activities are recommended:

1. **Maintain an external asset inventory:** Record the primary domain, discovered subdomains, IP addresses, and associated services. Review the inventory periodically for changes.
2. **Verify discovered subdomains:** Confirm that each subdomain is active, belongs to the organization, and has an identified owner and business purpose.
3. **Review exposed services:** Confirm that externally reachable services are required and that HTTPS configurations and associated services are maintained securely.
4. **Validate vulnerability indicators:** Obtain the underlying CVE identifiers, affected components, severity information, and evidence before assigning risk or claiming that a vulnerability is confirmed.
5. **Verify technology fingerprints:** Where possible, establish the actual software products and versions before making conclusions about patch status or exposure.
6. **Reassess the external attack surface:** Repeat discovery periodically and investigate newly identified assets, changes in IP mappings, and unexpected services.

## 6. Scope and Limitations

This assessment is based on the seven-page SOCRadar EASM free-edition report generated on 11 July 2026.

The report provides a snapshot of externally visible asset and technology information. It does not, by itself, establish that the listed assets are vulnerable or exploitable. In particular:

- The report does not provide details for the 95 vulnerability indicators, such as CVE identifiers, severity, affected versions, or proof of exploitability.
- Exact versions of the detected technologies are not provided.
- The report lists port 443 but does not provide a complete service or TLS configuration assessment.
- The absence of related-domain findings is not proof that no other related domains exist.
- The findings represent the scan's output on the stated date and may change over time.

No exploitation or intrusive validation is claimed as part of this assessment.

## 7. Conclusion

The SOCRadar EASM free-edition scan provided an initial view of the target domain's external attack surface. It identified three subdomains, mapped the primary domain to an IP address associated with ERNET India, reported HTTPS on port 443, displayed 95 vulnerability indicators, and identified Apache and Express technology fingerprints.

The results demonstrate the value of external attack surface discovery in identifying internet-visible assets and potential areas for further review. The next step would be to validate the discovered assets and investigate the scanner-reported indicators before drawing conclusions about their security impact.

---

**Source:** SOCRadar EASM scan report for `iiitsurat.ac.in`, scan date 11 July 2026.
