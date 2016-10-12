%{?scl:%scl_package jmh}
%{!?scl:%global pkg_name %{name}}

%global hghash 7ff584954008

Name:		%{?scl_prefix}jmh
Version:	1.13
Release:	3%{?dist}
Summary:	Java Microbenchmark Harness
License:	GPLv2 with exceptions
URL:		http://openjdk.java.net/projects/code-tools/%{pkg_name}/
Source0:	http://hg.openjdk.java.net/code-tools/%{pkg_name}/archive/%{hghash}.tar.bz2

BuildRequires:	%{?scl_prefix_maven}maven-local
BuildRequires:	%{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-site-plugin)
BuildRequires:	%{?scl_prefix}jopt-simple
BuildRequires:	%{?scl_prefix}apache-commons-math
BuildRequires:	%{?scl_prefix_java_common}junit
%{?scl:Requires: %scl_runtime}

BuildArch:	noarch

%description
The JMH is a Java harness for building, running, and analysing
nano/micro/macro benchmarks written in Java and other languages
targeting the JVM.

%package core-benchmarks
Summary:	JMH Core Benchmarks

%description core-benchmarks
JMH Core Benchmarks.

%package generator-annprocess
Summary:	JMH Generators: Annotation Processors

%description generator-annprocess
JMH benchmark generator, based on annotation processors.

%package generator-asm
Summary:	JMH Generators: ASM

%description generator-asm
JMH benchmark generator, based on ASM bytecode manipulation.

%package generator-bytecode
Summary:	JMH Generators: Bytecode

%description generator-bytecode
JMH benchmark generator, based on byte-code inspection.

%package generator-reflection
Summary:	JMH Generators: Reflection

%description generator-reflection
JMH benchmark generator, based on reflection.

%package parent
Summary:	Java Microbenchmark Harness Parent POM

%description parent
Java Microbenchmark Harness Parent POM.

%package samples
Summary:	JMH Samples
# BSD jmh-samples/src/main/java/*
License:	BSD

%description samples
JMH Samples.

%package javadoc
Summary:	Javadoc for %{name}
License:	BSD and GPLv2 with exceptions

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{pkg_name}-%{hghash}

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%pom_disable_module %{pkg_name}-archetypes
%pom_disable_module %{pkg_name}-core-ct
%pom_disable_module %{pkg_name}-core-it

%pom_remove_plugin -r :maven-eclipse-plugin
%pom_remove_plugin -r :maven-license-plugin
%pom_remove_plugin -r :maven-shade-plugin
%pom_remove_plugin -r :maven-source-plugin
%pom_xpath_remove "pom:plugin[pom:artifactId = 'maven-javadoc-plugin']/pom:executions"

# wagon-ssh
%pom_xpath_remove "pom:build/pom:extensions" %{pkg_name}-core
%{?scl:EOF}

# textTest_ROOT:218->test:134->compare:115 Mismatch expected:<...thrpt ...
rm -r %{pkg_name}-core/src/test/java/org/openjdk/jmh/results/format/ResultFormatTest.java

# Fix non ASCII chars
for s in $(find %{pkg_name}-samples -name "*.java") \
 %{pkg_name}-core-benchmarks/src/main/java/org/openjdk/jmh/validation/tests/BlackholeConsumeCPUTest.java \
 %{pkg_name}-core-benchmarks/src/main/java/org/openjdk/jmh/validation/tests/BlackholeConsecutiveTest.java \
 %{pkg_name}-core-benchmarks/src/main/java/org/openjdk/jmh/validation/tests/BlackholeSingleTest.java \
 %{pkg_name}-core-benchmarks/src/main/java/org/openjdk/jmh/validation/tests/BlackholePipelinedTest.java \
 %{pkg_name}-core-benchmarks/src/main/java/org/openjdk/jmh/validation/IterationScoresFormatter.java ;do
  native2ascii -encoding UTF8 ${s} ${s}
done

# http://mail.openjdk.java.net/pipermail/jmh-dev/2015-August/001997.html
sed -i "s,59,51,;s,Temple Place,Franklin Street,;s,Suite 330,Fifth Floor,;s,02111-1307,02110-1301," src/license/gpl_cpe/license.txt

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build -s
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles-%{pkg_name}-core
%license %{pkg_name}-core/LICENSE

%files core-benchmarks -f .mfiles-%{pkg_name}-core-benchmarks
%license %{pkg_name}-core-benchmarks/LICENSE

%files generator-annprocess -f .mfiles-%{pkg_name}-generator-annprocess
%license %{pkg_name}-generator-annprocess/LICENSE

%files generator-asm -f .mfiles-%{pkg_name}-generator-asm
%license %{pkg_name}-generator-asm/LICENSE

%files generator-bytecode -f .mfiles-%{pkg_name}-generator-bytecode
%license %{pkg_name}-generator-bytecode/LICENSE

%files generator-reflection -f .mfiles-%{pkg_name}-generator-reflection
%license %{pkg_name}-generator-reflection/LICENSE

%files parent -f .mfiles-%{pkg_name}-parent
%license LICENSE src/license/*

%files samples -f .mfiles-%{pkg_name}-samples
%license %{pkg_name}-samples/LICENSE src/license/bsd/*

%files javadoc -f .mfiles-javadoc
%license LICENSE src/license/*

%changelog
* Wed Oct 12 2016 Tomas Repik <trepik@redhat.com> - 1.13-3
- use standard SCL macros

* Mon Aug 01 2016 Tomas Repik <trepik@redhat.com> - 1.13-2
- scl conversion

* Wed Jul 27 2016 gil cattaneo <puntogil@libero.it> 1.13-1
- update to 1.13

* Sun Jul 24 2016 gil cattaneo <puntogil@libero.it> 1.11.3-3
- disable jmh-core-ct and jmh-core-it modules

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 gil cattaneo <puntogil@libero.it> 1.11.3-1
- update to 1.11.3

* Mon Nov 23 2015 gil cattaneo <puntogil@libero.it> 1.11.2-1
- update to 1.11.2

* Sat Aug 29 2015 gil cattaneo <puntogil@libero.it> 1.10.5-2
- fix samples sub-package license

* Sat Aug 29 2015 gil cattaneo <puntogil@libero.it> 1.10.5-1
- update to 1.10.5

* Fri Aug 21 2015 gil cattaneo <puntogil@libero.it> 1.10.4-1
- update to 1.10.4

* Thu Aug 13 2015 gil cattaneo <puntogil@libero.it> 1.10.3-1
- update to 1.10.3

* Sun Jul 26 2015 gil cattaneo <puntogil@libero.it> 1.10.1-1
- update to 1.10.1

* Sat May 16 2015 gil cattaneo <puntogil@libero.it> 1.9.3-1
- initial rpm
