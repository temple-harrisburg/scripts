<#
    .SYNOPSIS
    Import a potentially invalid TLS certificate to the host's root 
    certificate store from a remote URL.

    .DESCRIPTION
    Download and install a TLS certificate without checking its validity. 
    Intentinally not checking the certificate's validity is necessary in cases 
    where the the certificate may be self-signed, e.g. from Unifi hardware on
    the local area network. This script SHOULD NOT be used to install 
    certificates from the WAN (internet).

    .PARAMETER URL
    URL to the remote host. Default is https://unifi.local.
#>
Import-Module pki

param (
    [Parameter(Position = 0)]
    [string]$URL = "https://unifi.local"
)

Add-Type @"
using System;
using System.Net.Http;
public class SelfSignedCert 
{
    private string _certdata;
    public string GetCert(string uri)
    {
        var handler = new HttpClientHandler();
        handler.ServerCertificateCustomValidationCallback = (msg, cert, chain, err) => { _certdata = cert?.ExportCertificatePem(); return true; };
        var client = new HttpClient(handler);
        HttpResponseMessage res = client.GetAsync(uri).GetAwaiter().GetResult();
        return _certdata;
    }
}
"@

$certFile = New-TemporaryFile;
$getcert = [SelfSignedCert]::new()
$getcert.GetCert($URL) | Out-File $certFile

Import-Certificate -FilePath $certFile -CertStoreLocation "Cert:\LocalMachine\Root"
