set -euxo pipefail

rm -rf ./cvs
mkdir -p ./cvs
cd ./cvs

# Get CVS snapshots from SourceForge
wget --no-verbose "https://sourceforge.net/code-snapshots/cvs/d/do/docstring.zip"
wget --no-verbose "https://sourceforge.net/code-snapshots/cvs/s/st/structuredtext.zip"

# Get pre-CVS release archives for incorporation into history
# Note: The CVS history begins at the 0.3 archives
wget --no-verbose "https://master.dl.sourceforge.net/project/docstring/dps/0.1/dps-0.1.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docstring/dps/0.2/dps.0.2.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docstring/dps/0.3/dps.0.3.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/docstring/dps/0.4/dps-0.4.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/structuredtext/restructuredtext/0.1/rst-0.1.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/structuredtext/restructuredtext/0.2/rst.0.2.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/structuredtext/restructuredtext/0.3/rst.0.3.tar.gz"
wget --no-verbose "https://master.dl.sourceforge.net/project/structuredtext/restructuredtext/0.4/restructuredtext-0.4.tar.gz"

# unpack every archive
tar -xzf ./dps-0.1.tar.gz --one-top-level=dps-0.1 --strip-components=0
tar -xzf ./dps.0.2.tar.gz --one-top-level=dps-0.2 --strip-components=1
tar -xzf ./dps.0.3.tar.gz --one-top-level=dps-0.3 --strip-components=1
tar -xzf ./dps-0.4.tar.gz --one-top-level=dps-0.4 --strip-components=1
tar -xzf ./rst-0.1.tar.gz --one-top-level=rst-0.1 --strip-components=0
tar -xzf ./rst.0.2.tar.gz --one-top-level=rst-0.2 --strip-components=1
tar -xzf ./rst.0.3.tar.gz --one-top-level=rst-0.3 --strip-components=1
tar -xzf ./restructuredtext-0.4.tar.gz --one-top-level=rst-0.4 --strip-components=1
unzip docstring.zip -d ./
unzip structuredtext.zip -d ./
