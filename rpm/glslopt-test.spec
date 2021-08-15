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

%description
%{summary}.

# Build output directory.
%define BUILD_DIR "$PWD"/../build

%prep
%autosetup -p1 -n %{name}-%{version}/glslopt

%build

mkdir -p "%BUILD_DIR"

# Create a link to the stdc++ include directory
%ifarch %arm
echo Creating include link in "%BUILD_DIR"/include
if [ ! -L "%BUILD_DIR"/include ] ; then ln -s /usr/include/c++/8.3.0/ "%BUILD_DIR"/include; fi
%endif

# Build the crate
CARGO_TARGET_DIR="%BUILD_DIR" cargo --offline build --release -vv

# Build the test c++ file
#host-g++ -isystem "%BUILD_DIR"/include/ ../test/test.cpp -o "%BUILD_DIR"/test

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/rust/
cp "%BUILD_DIR"/release/libglslopt.rlib %{buildroot}%{_libdir}/rust/
mkdir -p %{buildroot}%{_bindir}/test
cp "%BUILD_DIR"/test %{buildroot}%{_bindir}/test/

%files
%defattr(-,root,root,-)
%dir %{_libdir}/rust
%{_libdir}/rust/libglslopt.rlib
#%dir %{_bindir}/test
#{_bindir}/test/test

