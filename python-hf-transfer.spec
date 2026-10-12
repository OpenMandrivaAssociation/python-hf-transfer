%undefine _debugsource_packages

# Recreate the vendor archive after a version bump:
#   tar xf hf_transfer-VERSION.tar.gz
#   cd hf_transfer-VERSION
#   cargo vendor --locked
#   tar czf python-hf-transfer-VERSION-vendor.tar.gz vendor
#   abb store python-hf-transfer-VERSION-vendor.tar.gz

Name:		python-hf-transfer
Version:	0.1.9
Release:	2
Summary:	Fast file transfers for the Hugging Face Hub
License:	Apache-2.0
Group:		Development/Python
URL:		https://github.com/huggingface/hf_transfer
Source0:	https://files.pythonhosted.org/packages/source/h/hf_transfer/hf_transfer-%{version}.tar.gz
Source1:	%{name}-%{version}-vendor.tar.gz

BuildSystem:	python
BuildRequires:	cargo
BuildRequires:	make
BuildRequires:	perl
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(maturin)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	rust-packaging

%description
Rust-backed download/upload helper used by the Hugging Face Hub
client (and Unsloth) when HF_HUB_ENABLE_HF_TRANSFER=1.

%prep -a
tar xf %{SOURCE1}
%cargo_prep -v vendor

%build -p
export CARGO_HOME=$PWD/.cargo
export CARGO_NET_OFFLINE=true
# rust-openssl 0.10 does not know cooker OpenSSL; use the vendored copy.
unset OPENSSL_NO_VENDOR

%build -a
%cargo_license_summary
%{cargo_license} > LICENSES.dependencies

%files
%doc README.md
%license LICENSE LICENSES.dependencies
%{python_sitearch}/hf_transfer
%{python_sitearch}/hf_transfer-*.*-info
