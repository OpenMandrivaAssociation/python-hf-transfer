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
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(maturin)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(wheel)

%description
Rust-backed download/upload helper used by the Hugging Face Hub
client (and Unsloth) when HF_HUB_ENABLE_HF_TRANSFER=1.

%prep -a
tar xf %{SOURCE1}
# Crates are already vendored. rust-packaging pulls python-rust2rpm, which
# still requires Python 3.14.
rm -f Cargo.toml.orig
mkdir -p .cargo
cat > .cargo/config.toml << 'EOF'
[net]
offline = true

[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build -p
export CARGO_HOME=$PWD/.cargo
export CARGO_NET_OFFLINE=true
# pyo3 0.23 targets abi3-py38 and otherwise rejects a newer interpreter.
export PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1
# rust-openssl 0.10 does not know cooker OpenSSL; use the vendored copy.
unset OPENSSL_NO_VENDOR

%build -a
cargo tree --locked --offline --edges no-build,no-dev,no-proc-macro \
	--prefix none --format '{l}: {p}' \
	| sed -e "s: ($(pwd)[^)]*)::g" -e 's: / :/:g' -e 's:/: OR :g' \
	| sort -u > LICENSES.dependencies

%files
%doc README.md
%license LICENSE LICENSES.dependencies
%{python_sitearch}/hf_transfer
%{python_sitearch}/hf_transfer-*.*-info
