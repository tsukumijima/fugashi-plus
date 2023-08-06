#!/bin/bash

FLAGS="--enable-utf8-only"
X86_TRIPLET=x86_64-apple-macos10.9
ARM_TRIPLET=arm64-apple-macos11


git clone --depth=1 https://github.com/taku910/mecab.git
cd mecab/mecab

rm -rf src/.libs-arm64 src/.libs-x86_64 src/.libs.combined

./configure $FLAGS CXX="clang++ -target $ARM_TRIPLET" CC="clang" CXXFLAGS="-target $ARM_TRIPLET" CPPFLAGS="-target $ARM_TRIPLET" LDFLAGS="-target $ARM_TRIPLET"

make clean
make -j$(nproc)

mv src/.libs src/.libs-arm64

./configure $FLAGS CXX="clang++ -target $X86_TRIPLET" CC="clang" CXXFLAGS="-target $X86_TRIPLET" CPPFLAGS="-target $X86_TRIPLET" LDFLAGS="-target $X86_TRIPLET"

make clean
make -j$(nproc)

mv src/.libs src/.libs-x86_64

rm -rf src/.libs.combined
mkdir src/.libs.combined

lipo -create src/.libs-arm64/libmecab.2.dylib src/.libs-x86_64/libmecab.2.dylib -output src/.libs.combined/libmecab.2.dylib

lipo -create src/.libs-arm64/libmecab.a src/.libs-x86_64/libmecab.a -output src/.libs.combined/libmecab.a

cp src/.libs-arm64/libmecab.lai src/.libs.combined/libmecab.lai

ls src/.libs-arm64/*.o src/.libs-arm64/mecab* | while read line; do
    echo $line
    lipo -create $line src/.libs-x86_64/$(basename $line) -output src/.libs.combined/$(basename $line)
done

cd src/.libs.combined
ln -s ../libmecab.la libmecab.la
ln -s libmecab.2.dylib libmecab.dylib
cd ../..
mv src/.libs.combined src/.libs

sudo make install
cd ../..

python -m pip install --upgrade setuptools wheel pip setuptools-scm
python -m pip install cibuildwheel==2.3.1
pip install -r requirements.txt

python -m cibuildwheel --platform macos --archs x86_64 --output-dir dist
python -m cibuildwheel --platform macos --archs arm64 --output-dir dist
python -m cibuildwheel --platform macos --archs universal2 --output-dir dist
