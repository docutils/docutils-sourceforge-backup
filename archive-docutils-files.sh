set -euxo pipefail

rm -rf ./docutils-archives
mkdir -p ./docutils-archives
cd ./docutils-archives

# Get Docutils release tarballs from SourceForge
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.1/docutils-0.1.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.2/docutils-0.2.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.3/docutils-0.3.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.3.3-alpha/docutils-0.3.3-alpha.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.3.5/docutils-0.3.5.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.3.7/docutils-0.3.7.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.3.9/docutils-0.3.9.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.4/docutils-0.4.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.5/docutils-0.5.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.6/docutils-0.6.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.7/docutils-0.7.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.8/docutils-0.8.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.8.1/docutils-0.8.1.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.9/docutils-0.9.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.9.1/docutils-0.9.1.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.10/docutils-0.10.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.11/docutils-0.11.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.12/docutils-0.12.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.13.1/docutils-0.13.1.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.14rc1/docutils-0.14rc1.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.14rc2/docutils-0.14rc2.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.14/docutils-0.14.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.15/docutils-0.15.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.16/docutils-0.16.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.17/docutils-0.17.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.17.1/docutils-0.17.1.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.18/docutils-0.18.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.18.1/docutils-0.18.1.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.19/docutils-0.19.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.20/docutils-0.20.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.20.1/docutils-0.20.1.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.21/docutils-0.21.post1.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.21.1/docutils-0.21.1.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.21.2/docutils-0.21.2.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.22/docutils-0.22.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.22.1/docutils-0.22.1.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.22.2/docutils-0.22.2.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.22.3/docutils-0.22.3.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docutils/docutils/0.22.4/docutils-0.22.4.tar.gz"

cd ../
rm -rf ./docutils-archives-unpacked
mkdir -p ./docutils-archives-unpacked
cd ./docutils-archives-unpacked

# unpack every archive
tar -xzf ../docutils-archives/docutils-0.1.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.2.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.3.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.3.3-alpha.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.3.5.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.3.7.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.3.9.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.4.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.5.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.6.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.7.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.8.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.8.1.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.9.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.9.1.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.10.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.11.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.12.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.13.1.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.14rc1.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.14rc2.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.14.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.15.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.16.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.17.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.17.1.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.18.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.18.1.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.19.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.20.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.20.1.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.21.post1.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.21.1.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.21.2.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.22.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.22.1.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.22.2.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.22.3.tar.gz --strip-components=0
tar -xzf ../docutils-archives/docutils-0.22.4.tar.gz --strip-components=0
