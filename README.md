# fugashi-plus

[![Current PyPI packages](https://badge.fury.io/py/fugashi-plus.svg)](https://pypi.org/project/fugashi-plus/)
![Test Status](https://github.com/tsukumijima/fugashi-plus/workflows/test-manylinux/badge.svg)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/fugashi-plus)](https://pypi.org/project/fugashi-plus/)
![Supported Platforms](https://img.shields.io/badge/platforms-linux%20macosx%20windows-blue)

fugashi-plus は、主に Windows 対応や MeCab の [ikegami-yukino/mecab](https://github.com/ikegami-yukino/mecab) への移行などコードのメンテナンスを目的とした、[fugashi](https://github.com/polm/fugashi) の派生ライブラリです。

## Changes in this fork

- **パッケージ名を `fugashi-plus` に変更**
  - ライブラリ名は `fugashi` から変更されておらず、[fugashi](https://github.com/polm/fugashi) 本家同様に `import fugashi` でインポートできる
  - [fugashi](https://github.com/polm/fugashi) 本家のドロップイン代替として利用できる
- **明示的に Python 3.13 をサポート対象に追加**
  - CI 対象の Python バージョンにも 3.13 を追加した
- **Cython を 3.0 系に更新**
  - https://github.com/cython/cython/issues/5982 の通り、Python 3.13 では一部の非推奨 C API が削除されている
  - Cython 0.x 系では Python 3.13 以降のビルドに失敗するため、Cython 3.0 系に更新した
- **Cython モジュールに型ヒント (Type Hints) を追加**
  - fugashi 本家には型ヒントが同梱されておらず、また fugashi はほぼ 100% Cython で書かれているため、Pylance などでのコード補完や型チェックが全く効かない
  - fugashi-plus では Cython モジュールに型ヒントを追加したことで、コード補完や型チェックが効くようになっている
- **MeCab を現在もメンテナンスが続けられている [ikegami-yukino/mecab](https://github.com/ikegami-yukino/mecab) に移行**
  - **オリジナルの Mecab ([taku910/mecab](https://github.com/taku910/mecab)) は、2020 年以降メンテナンスが放棄されている**
    - 大元の設計から Windows での使用を想定していないようで、Windows のサポートは不十分
    - fugashi 本家では Windows 向け wheel のみ Windows 向けの修正を施した [chezou/mecab](https://github.com/chezou/mecab) が使われているが、2018 年以降メンテナンスが放棄されている
  - **一方 [ikegami-yukino/mecab](https://github.com/ikegami-yukino/mecab) は現在でもメンテナンスが続けられており、Windows 64bit でも比較的容易にビルドできる**
    - ただし、Visual Studio 2022 (Build Tools v143) では非推奨の一部 C++ 標準ライブラリが削除されている関係で、ビルドに失敗する
    - このため、GitHub Actions のビルド環境では明示的に Build Tools v142 (Visual Studio 2019 相当) でビルドを行っている
  - **[ikegami-yukino/mecab](https://github.com/ikegami-yukino/mecab) に移行することで、UniDic 2.3.0 以降でユーザー辞書のビルドに失敗する問題が修正される**
    - 参考資料:
      - https://github.com/taku910/mecab/issues/10
      - https://github.com/polm/fugashi/issues/75
      - https://ja.stackoverflow.com/a/74219/48588
      - https://zenn.dev/zagvym/articles/28056236903369
      - https://qiita.com/CookieBox26/items/a607d9e25f3b18d209ea
    - 結局 MeCab 側の実装ミスかそれとも UniDic の作成不備かは釈然としないが、UniDic 側の作成不備だとすると 3.1.0 や最新版でも修正されていないのは不可解
    - [ikegami-yukino/mecab](https://github.com/ikegami-yukino/mecab) ではこの問題を解決する https://github.com/taku910/mecab/pull/70 での修正内容が独自にマージされており、ユーザー辞書のビルドに失敗する問題が修正されている
    - 上記プルリクエストでの修正を取り込まない場合、巨大な UniDic を手元で再ビルドするか、値決め打ちで UniDic の辞書データのバイナリを書き換えるしかなくなり、どちらの方法も実運用上非常に問題がある
- **Windows 環境において、システム辞書・ユーザー辞書の保存先パス指定が正常に機能しない問題を修正**
  - fugashi 本家では `GenericTagger` クラス・`build_dictionary()` の両方で MeCab に渡す引数の分割に `shlex.split()` が使われていたが、shlex は Windows パスを正しく解釈しない
  - fugashi-plus では、Windows のみ shlex を使わず独自に引数解析を行うことで、ライブラリユーザー側でワークアラウンドを挟むことなく、正常にシステム辞書・ユーザー辞書の保存先パスを指定できるようにしている
- **`Tagger` クラスのコンストラクタで、`unidic` / `unidic-lite` パッケージのインストール有無に関わらず、引数に指定されたシステム辞書を利用するよう変更**
  - fugashi 本家では `unidic` / `unidic-lite` パッケージがインストール済みの環境だと、`Tagger` クラスのコンストラクタ引数 (`arg`) に独自にシステム辞書のパスを指定しても、常に `unidic` / `unidic-lite` パッケージ内蔵の UniDic が優先して利用されてしまっていた
  - fugashi-plus では、コンストラクタ引数 (`arg`) の文字列内に `-r` や `-d` オプションが含まれない場合にのみ、`unidic` / `unidic-lite` パッケージに内蔵の UniDic を検出するロジックに変更している
- **その他コードのクリーンアップなど**

## Installation

下記コマンドを実行して、ライブラリをインストールできます。

```bash
pip install fugashi-plus
```

下記のドキュメントは、[fugashi](https://github.com/polm/fugashi) 本家のドキュメントを改変なしでそのまま引き継いでいます。  
これらのドキュメントの内容が fugashi-plus にも通用するかは保証されません。

-------

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fugashi.streamlit.app)
[![Current PyPI packages](https://badge.fury.io/py/fugashi.svg)](https://pypi.org/project/fugashi/)
![Test Status](https://github.com/polm/fugashi/workflows/test-manylinux/badge.svg)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/fugashi)](https://pypi.org/project/fugashi/)
![Supported Platforms](https://img.shields.io/badge/platforms-linux%20macosx%20windows-blue)

# fugashi

<img src="https://github.com/polm/fugashi/raw/main/fugashi.png" width=125 height=125 alt="fugashi by Irasutoya" />

fugashi is a Cython wrapper for [MeCab](https://taku910.github.io/mecab/), a
Japanese tokenizer and morphological analysis tool.  Wheels are provided for
Linux, OSX (Intel), and Win64, and UniDic is [easy to install](#installing-a-dictionary).

**issueを英語で書く必要はありません。**

Check out the [interactive demo][], see the [blog post](https://www.dampfkraft.com/nlp/fugashi.html) for background
on why fugashi exists and some of the design decisions, or see [this
guide][guide] for a basic introduction to Japanese tokenization.

[guide]: https://www.dampfkraft.com/nlp/how-to-tokenize-japanese.html
[interactive demo]: https://fugashi.streamlit.app

If you are on a platform for which wheels are not provided, you'll need to
install MeCab first. It's recommended you install [from
source](https://github.com/taku910/mecab). If you need to build from source on
Windows, [@chezou's fork](https://github.com/chezou/mecab) is recommended; see
[issue #44](https://github.com/polm/fugashi/issues/44#issuecomment-954426115)
for an explanation of the problems with the official repo.

Known platforms without wheels:

- musl-based distros like alpine [#77](https://github.com/polm/fugashi/issues/77)
- PowerPC
- Windows 32bit

## Usage

```python
from fugashi import Tagger

tagger = Tagger('-Owakati')
text = "麩菓子は、麩を主材料とした日本の菓子。"
tagger.parse(text)
# => '麩 菓子 は 、 麩 を 主材 料 と し た 日本 の 菓子 。'
for word in tagger(text):
    print(word, word.feature.lemma, word.pos, sep='\t')
    # "feature" is the Unidic feature data as a named tuple
```

## Installing a Dictionary

fugashi requires a dictionary. [UniDic](https://unidic.ninjal.ac.jp/) is
recommended, and two easy-to-install versions are provided.

  - [unidic-lite](https://github.com/polm/unidic-lite), a slightly modified version 2.1.2 of Unidic (from 2013) that's relatively small
  - [unidic](https://github.com/polm/unidic-py), the latest UniDic 3.1.0, which is 770MB on disk and requires a separate download step

If you just want to make sure things work you can start with `unidic-lite`, but
for more serious processing `unidic` is recommended. For production use you'll
generally want to generate your own dictionary too; for details see the [MeCab
documentation](https://taku910.github.io/mecab/learn.html).

To get either of these dictionaries, you can install them directly using `pip`
or do the below:

```sh
pip install 'fugashi[unidic-lite]'

# The full version of UniDic requires a separate download step
pip install 'fugashi[unidic]'
python -m unidic download
```

For more information on the different MeCab dictionaries available, see [this article](https://www.dampfkraft.com/nlp/japanese-tokenizer-dictionaries.html).

## Dictionary Use

fugashi is written with the assumption you'll use Unidic to process Japanese,
but it supports arbitrary dictionaries. 

If you're using a dictionary besides Unidic you can use the GenericTagger like this:

```python
from fugashi import GenericTagger
tagger = GenericTagger()

# parse can be used as normal
tagger.parse('something')
# features from the dictionary can be accessed by field numbers
for word in tagger(text):
    print(word.surface, word.feature[0])
```

You can also create a dictionary wrapper to get feature information as a named tuple. 

```python
from fugashi import GenericTagger, create_feature_wrapper
CustomFeatures = create_feature_wrapper('CustomFeatures', 'alpha beta gamma')
tagger = GenericTagger(wrapper=CustomFeatures)
for word in tagger.parseToNodeList(text):
    print(word.surface, word.feature.alpha)
```

## Citation

If you use fugashi in research, it would be appreciated if you cite this paper. You can read it at [the ACL Anthology](https://www.aclweb.org/anthology/2020.nlposs-1.7/) or [on Arxiv](https://arxiv.org/abs/2010.06858).

    @inproceedings{mccann-2020-fugashi,
        title = "fugashi, a Tool for Tokenizing {J}apanese in Python",
        author = "McCann, Paul",
        booktitle = "Proceedings of Second Workshop for NLP Open Source Software (NLP-OSS)",
        month = nov,
        year = "2020",
        address = "Online",
        publisher = "Association for Computational Linguistics",
        url = "https://www.aclweb.org/anthology/2020.nlposs-1.7",
        pages = "44--51",
        abstract = "Recent years have seen an increase in the number of large-scale multilingual NLP projects. However, even in such projects, languages with special processing requirements are often excluded. One such language is Japanese. Japanese is written without spaces, tokenization is non-trivial, and while high quality open source tokenizers exist they can be hard to use and lack English documentation. This paper introduces fugashi, a MeCab wrapper for Python, and gives an introduction to tokenizing Japanese.",
    }

## Alternatives

If you have a problem with fugashi feel free to open an issue. However, there
are some cases where it might be better to use a different library.

- If you don't want to deal with installing MeCab at all, try [SudachiPy](https://github.com/WorksApplications/sudachi.rs).
- If you need to work with Korean, try [pymecab-ko](https://github.com/NoUnique/pymecab-ko) or [KoNLPy](https://konlpy.org/en/latest/).

## License and Copyright Notice

fugashi is released under the terms of the [MIT license](./LICENSE). Please
copy it far and wide.

fugashi is a wrapper for MeCab, and fugashi wheels include MeCab binaries.
MeCab is copyrighted free software by Taku Kudo `<taku@chasen.org>` and Nippon
Telegraph and Telephone Corporation, and is redistributed under the [BSD
License](./LICENSE.mecab).
