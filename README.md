# A Blog by Mitja Martini

## Categories

- The Basics
- Practical AI Use Cases
- Amazing Ideas (planned)
- Playground
- Working with AI (planned)
- Creating Custom GPTs (planned)
- Building AI Apps (planned)
- Today I Learned (planned)
- Excel is all you need
- Walkable AI (planned)
- Kubecademy (planned)

## Installation

On windows:

- [Install Jekyll](https://jekyllrb.com/docs/installation/windows/)
- cd into this repo
- run `bundle install`
- start server (see below)

## Usage

- create a draft in _drafts
- store image in a proper subfolder in `/assets/blog/`
- start server with live reload: `bundle exec jekyll s -l`
- start server with drafts: `bundle exec jekyll s -D -l`
- remove all generated files: `bundle exec jekyll clean`
- output deprecation or config issues: `bundle exec jekyll doctor`
- Jekyll documentation about [pages](https://jekyllrb.com/docs/pages/)
- Jekyll documentation about [front matter](https://jekyllrb.com/docs/front-matter/)
- manually build and deploy: `JEKYLL_ENV=production bundle exec jekyll b`

Unless you specified the output path, the generated site files will be placed in folder `_site` of the project’s root directory. Now you should upload those files to the target server.

See: [Jekyll](https://jekyllrb.com)

## Images

Image:

```markdown
![Alt text ](assets/logo.png)
```

Image with link:

```markdown
[![Alt text ](assets/logo.png)](https://example.com)
```

## Open in Colab Button

Create a link with a button here:

https://openincolab.com/

## Information from the Chirpy Starter Template

This blog uses the Cirpy theme and is based on the Chirpy Starter template. Here is the information from the Chirpy Starter template.

[![Gem Version](https://img.shields.io/gem/v/jekyll-theme-chirpy)][gem]&nbsp;
[![GitHub license](https://img.shields.io/github/license/cotes2020/chirpy-starter.svg?color=blue)][mit]

When installing the [**Chirpy**][chirpy] theme through [RubyGems.org][gem], Jekyll can only read files in the folders
`_data`, `_layouts`, `_includes`, `_sass` and `assets`, as well as a small part of options of the `_config.yml` file
from the theme's gem. If you have ever installed this theme gem, you can use the command
`bundle info --path jekyll-theme-chirpy` to locate these files.

The Jekyll team claims that this is to leave the ball in the user’s court, but this also results in users not being
able to enjoy the out-of-the-box experience when using feature-rich themes.

To fully use all the features of **Chirpy**, you need to copy the other critical files from the theme's gem to your
Jekyll site. The following is a list of targets:

```shell
.
├── _config.yml
├── _plugins
├── _tabs
└── index.html
```

To save you time, and also in case you lose some files while copying, we extract those files/configurations of the
latest version of the **Chirpy** theme and the [CD][CD] workflow to here, so that you can start writing in minutes.

### Prerequisites

Follow the instructions in the [Jekyll Docs](https://jekyllrb.com/docs/installation/) to complete the installation of
the basic environment. [Git](https://git-scm.com/) also needs to be installed.

### Installation

Sign in to GitHub and [**use this template**][use-template] to generate a brand new repository and name it
`USERNAME.github.io`, where `USERNAME` represents your GitHub username.

Then clone it to your local machine and run:

```console
$ bundle
```

### Usage

Please see the [theme's docs](https://github.com/cotes2020/jekyll-theme-chirpy#documentation).

## License

At the moment, I have not yet decided on a license for the content and thus all rights are reserved.

The Chirpy theme is published under [MIT][mit] License.

[gem]: https://rubygems.org/gems/jekyll-theme-chirpy
[chirpy]: https://github.com/cotes2020/jekyll-theme-chirpy/
[use-template]: https://github.com/cotes2020/chirpy-starter/generate
[CD]: https://en.wikipedia.org/wiki/Continuous_deployment
[mit]: https://github.com/cotes2020/chirpy-starter/blob/master/LICENSE
