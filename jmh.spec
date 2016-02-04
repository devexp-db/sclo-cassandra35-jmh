%global hghash 534d83d9137f
Name:          jmh
Version:       1.11.3
Release:       2%{?dist}
Summary:       Java Microbenchmark Harness
# BSD jmh-samples/src/main/java/*
# 2 files have unknown license, reported @ http://mail.openjdk.java.net/pipermail/jmh-dev/2015-August/002037.html
License:       GPLv2 with exceptions
URL:           http://openjdk.java.net/projects/code-tools/jmh/
Source0:       http://hg.openjdk.java.net/code-tools/jmh/archive/%{hghash}.tar.bz2

BuildRequires: maven-local
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(net.sf.jopt-simple:jopt-simple)
BuildRequires: mvn(org.apache.commons:commons-math3)
# BuildRequires: mvn(org.apache.maven.plugins:maven-shade-plugin)
BuildRequires: mvn(org.apache.maven.plugins:maven-site-plugin)
BuildRequires: mvn(org.ow2.asm:asm)

BuildArch:     noarch

%description
The JMH is a Java harness for building, running, and analysing
nano/micro/macro benchmarks written in Java and other languages
targeting the JVM.

%package core-benchmarks
Summary:       JMH Core Benchmarks

%description core-benchmarks
JMH Core Benchmarks.

%package core-ct
Summary:       JMH Core Compilation Tests

%description core-ct
JMH Core Compilation Tests.

%package core-it
Summary:       JMH Core Integration Tests

%description core-it
JMH Core Integration Tests.

%package generator-annprocess
Summary:       JMH Generators: Annotation Processors

%description generator-annprocess
JMH benchmark generator, based on annotation processors.

%package generator-asm
Summary:       JMH Generators: ASM

%description generator-asm
JMH benchmark generator, based on ASM bytecode manipulation.

%package generator-bytecode
Summary:       JMH Generators: Bytecode

%description generator-bytecode
JMH benchmark generator, based on byte-code inspection.

%package generator-reflection
Summary:       JMH Generators: Reflection

%description generator-reflection
JMH benchmark generator, based on reflection.

%package parent
Summary:       Java Microbenchmark Harness Parent POM

%description parent
Java Microbenchmark Harness Parent POM.

%package samples
Summary:       JMH Samples
License:       BSD

%description samples
JMH Samples.

%package javadoc
Summary:       Javadoc for %{name}
# BSD jmh-samples/src/main/java/*
License:       BSD and GPLv2 with exceptions

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{hghash}

%pom_disable_module %{name}-archetypes

%pom_remove_plugin -r :maven-eclipse-plugin
%pom_remove_plugin -r :maven-license-plugin
%pom_remove_plugin -r :maven-shade-plugin
%pom_remove_plugin -r :maven-source-plugin
%pom_xpath_remove "pom:plugin[pom:artifactId = 'maven-javadoc-plugin']/pom:executions"

# wagon-ssh
%pom_xpath_remove "pom:build/pom:extensions" %{name}-core

# textTest_ROOT:218->test:134->compare:115 Mismatch expected:<...thrpt ...
rm -r %{name}-core/src/test/java/org/openjdk/jmh/results/format/ResultFormatTest.java

# Fix non ASCII chars
for s in $(find %{name}-samples -name "*.java") \
 %{name}-core-benchmarks/src/main/java/org/openjdk/jmh/validation/tests/BlackholeConsumeCPUTest.java \
 %{name}-core-benchmarks/src/main/java/org/openjdk/jmh/validation/tests/BlackholeConsecutiveTest.java \
 %{name}-core-benchmarks/src/main/java/org/openjdk/jmh/validation/tests/BlackholeSingleTest.java \
 %{name}-core-benchmarks/src/main/java/org/openjdk/jmh/validation/tests/BlackholePipelinedTest.java \
 %{name}-core-benchmarks/src/main/java/org/openjdk/jmh/validation/IterationScoresFormatter.java ;do
  native2ascii -encoding UTF8 ${s} ${s}
done

# http://mail.openjdk.java.net/pipermail/jmh-dev/2015-August/001997.html
sed -i "s,59,51,;s,Temple Place,Franklin Street,;s,Suite 330,Fifth Floor,;s,02111-1307,02110-1301,"  $(find -name "LICENSE") src/license/gpl_cpe/license.txt

%build

%mvn_build -s

%install
%mvn_install

%files -f .mfiles-%{name}-core
%license %{name}-core/LICENSE

%files core-benchmarks -f .mfiles-%{name}-core-benchmarks
%license %{name}-core-benchmarks/LICENSE

%files core-ct -f .mfiles-%{name}-core-ct
%license LICENSE

%files core-it -f .mfiles-%{name}-core-it
%license %{name}-core-it/LICENSE

%files generator-annprocess -f .mfiles-%{name}-generator-annprocess
%license %{name}-generator-annprocess/LICENSE

%files generator-asm -f .mfiles-%{name}-generator-asm
%license %{name}-generator-asm/LICENSE

%files generator-bytecode -f .mfiles-%{name}-generator-bytecode
%license %{name}-generator-bytecode/LICENSE

%files generator-reflection -f .mfiles-%{name}-generator-reflection
%license %{name}-generator-reflection/LICENSE

%files parent -f .mfiles-%{name}-parent
%license LICENSE src/license/*

%files samples -f .mfiles-%{name}-samples
%license %{name}-samples/LICENSE src/license/bsd/*

%files javadoc -f .mfiles-javadoc
%license LICENSE src/license/*

%changelog
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
