Name:       glslopt-test
Summary:    An example glslopt rust crate for build process testing
Version:    1.0
Release:    1
Group:      System/Libraries
License:    MIT license
URL:        https://github.com/llewelld/glslopt
Source0:    %{name}-%{version}.tar.bz2
BuildRequires:  rust
BuildRequires:  rust-std-static
BuildRequires:  cargo
BuildRequires:  cbindgen
BuildRequires:  llvm
BuildRequires:  clang-devel

%description
%{summary}.

# Build output directory.
%define BUILD_DIR "$PWD"/../build

%prep
%autosetup -p1 -n %{name}-%{version}/glslopt

%ifarch %arm
%define SB2_TARGET armv7-unknown-linux-gnueabihf
%endif
%ifarch aarch64
%define SB2_TARGET aarch64-unknown-linux-gnu
%endif
%ifarch %ix86
%define SB2_TARGET i686-unknown-linux-gnu
%endif

echo "Target is %SB2_TARGET"

# Add `.cargo-checksum.json` for each dependency
find -L ../vendor -mindepth 2 -maxdepth 2 -type f -name Cargo.toml \
  -exec sh -c 'echo "{\"files\":{ },\"package\":\"\"}" > "$(dirname $0)/.cargo-checksum.json"' '{}' \;

%build

mkdir -p "%BUILD_DIR"

# Create a link to the stdc++ include directory
%ifarch %arm
echo Creating include link in "%BUILD_DIR"/include
if [ ! -L "%BUILD_DIR"/include ] ; then ln -s /usr/include/c++/8.3.0/ "%BUILD_DIR"/include; fi
%endif

echo "Target include contents"
ls -l "%BUILD_DIR"/include/
echo "Tooling include contents"
SBOX_DISABLE_MAPPING=1 ls -l "%BUILD_DIR"/include/

echo "Check for cc1plus in the target"
echo "/usr"
find /usr -iname "cc1plus" 2>/dev/null
echo "/srv"
find /srv -iname "cc1plus" 2>/dev/null
echo "Check completed"
echo "Check for cc1plus in the toolings"
echo "/usr"
SBOX_DISABLE_MAPPING=1 find /usr -iname "cc1plus" 2>/dev/null
echo "/srv"
SBOX_DISABLE_MAPPING=1 find /srv -iname "cc1plus" 2>/dev/null
echo "Check completed"

# Build the crate
SB2_TARGET="%SB2_TARGET" RUST_BACKTRACE=1 CARGO_TARGET_DIR="%BUILD_DIR" cargo --offline build --release -vv

# Build the test c++ file
#host-g++ -isystem "%BUILD_DIR"/include/ ../test/test.cpp -o "%BUILD_DIR"/test

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/rust/
cp "%BUILD_DIR"/release/libglslopt.rlib %{buildroot}%{_libdir}/rust/
#mkdir -p %{buildroot}%{_bindir}/test
#cp "%BUILD_DIR"/test %{buildroot}%{_bindir}/test/

%files
%defattr(-,root,root,-)
%dir %{_libdir}/rust
%{_libdir}/rust/libglslopt.rlib
#%dir %{_bindir}/test
#{_bindir}/test/test

