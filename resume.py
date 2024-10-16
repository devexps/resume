#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Build script for my resume
#
# This sources the "resume.yaml" and produces the resume in several formats
# from Jinja2 templates, including HTML, plain text, Markdown, and Gemini.
# -----------------------------------------------------------------------------
from jinja2 import Environment, FileSystemLoader, select_autoescape
import yaml
import json
import markdown
import datetime
import os
import re
import sys

# -----------------------------------------------------------------------------
# Config
# Environment variables with defaults.
# -----------------------------------------------------------------------------


class Config(dict):
    """Config class."""

    def __getattr__(self, attr):
        if attr in self:
            item = self[attr]
            if isinstance(item, dict):
                return Config(item)
            return item
        raise AttributeError(f"Config has no attribute {attr}")


config = Config({
    'template_dir': os.environ.get('RESUME_TEMPLATE_DIR', 'templates'),
    'resume_yaml': os.environ.get('RESUME_YAML', 'resume.yaml'),
    'html': {
        'template': os.environ.get('RESUME_HTML_TEMPLATE', 'resume.html'),
        'out': os.environ.get('RESUME_HTML_OUT', 'docs/index.html'),
        'css_src': os.environ.get('RESUME_CSS_TEMPLATE', 'style.css'),
    },
    'markdown': {
        'template': os.environ.get('RESUME_MD_TEMPLATE', 'resume.md'),
        'out': os.environ.get('RESUME_MD_OUT', 'README.md'),
    },
    'txt': {
        'template': os.environ.get('RESUME_TXT_TEMPLATE', 'resume.txt'),
        'out': os.environ.get('RESUME_TXT_OUT', 'docs/thangn.txt'),
        'narrow_template': os.environ.get('RESUME_TXT_NARROW_TEMPLATE',
                                          'resume-narrow.txt'),
        'narrow_out': os.environ.get('RESUME_TXT_NARROW_OUT',
                                     'docs/thangn-narrow.txt'),
    },
    'json': {
        'out': os.environ.get('RESUME_JSON_OUT', 'docs/thangn.json'),
    },
})

# -----------------------------------------------------------------------------

# Helpers
base_dir = os.path.dirname(os.path.realpath(__file__))
tag_remove = re.compile(r'<.*?>')

# Current date
current_date_time = datetime.datetime.now()
date = current_date_time.date()
year = date.strftime("%Y")


def md_strip(string: str):
    """Returns a string with Markdown URLs and emphasis removed.

    Args:
        string (str): The string to parse
    Returns:
        _s (str): A string with Markdown removed
    """
    _s = re.sub(r"\[([\w\s]+)\]\([\w\d\/\-\.:]+\)", "\\1", string)
    _s = re.sub(r"(\s+)__?(.*)__?(\s+)?", "\\1\\2\\3", _s)
    return _s


def resume(theformat='plain'):
    """Parses resume YAML, munges, and returns it as a dict.

    Args:
        theformat (str): The format to return the resume in
    Returns:
        resume_content (dict): The resume content read from YAML as a dict
    """
    with open(config.resume_yaml, 'r') as file:
        resume_content = yaml.safe_load(file)

        if theformat != 'html':
            resume_text = json.dumps(resume_content)

            if theformat == "md":
                resume_text = resume_text.replace("<b>", "**").replace("</b>", "**")
            
            return json.loads(tag_remove.sub('', resume_text))

    return resume_content


def css():
    """Loads CSS source file and returns it as a string.

    Returns:
        css_content (str): The CSS content as a string
    """
    css_file = os.path.join(config.template_dir, config.html.css_src)
    with open(css_file, 'r') as _file:
        css_content = _file.read()
    _file.close()
    return css_content


def build_template(**kwargs):
    """Compile Jinja2 template and return it as a string.

    Returns:
        src_file.render (str): The rendered template as a string
    Keyword Arguments:
        source (str): The source template file
    """
    src_dir = FileSystemLoader(config.template_dir)
    env = Environment(loader=src_dir,
                      autoescape=select_autoescape(
                          enabled_extensions=('html')
                      ))
    src_file = env.get_template(kwargs['source'])

    return src_file.render(
        resume=resume(theformat=kwargs['theformat']), css=css(), year=year
    )


def write_out(**kwargs):
    """Write a file to disk.

    Keyword Arguments:
        target (str): The target file to write
        content (str): The content to write to the target file
    """
    file_out = os.path.join(base_dir, kwargs['target'])
    with open(file_out, 'w') as _file:
        _file.write(kwargs['content'])
    _file.close()
    print(f"-> Wrote {kwargs['target']}")


def gen_html():
    """Generate HTML file from Jina2 template.

    The HTML file is written to the `docs` directory.
    """
    html = build_template(source=config.html.template, theformat='html')
    write_out(target=config.html.out, content=html)


def gen_markdown():
    """Generate Markdown file from Jina2 template."""
    md = build_template(source=config.markdown.template,
                        autoescape=True, theformat='md')
    write_out(target=config.markdown.out, content=md)

def gen_txt():
    """Generate plain text files from Jina2 template.

    A regular-width (<70 chars) and a narrow-width (<45 chars) file is created.
    """
    txt = build_template(source=config.txt.template, theformat='plain')
    write_out(target=config.txt.out, content=txt)

    narrow_txt = build_template(
        source=config.txt.narrow_template, theformat='plain')
    write_out(target=config.txt.narrow_out, content=narrow_txt)


def gen_json():
    """Generate JSON from converting the YAML source."""
    the_json = json.dumps(resume(theformat='plain'), indent=2)
    write_out(target=config.json.out, content=the_json)


def print_usage(formats=None):
    """Print script usage."""
    print(f"{sys.argv[0]} [ " + " | ".join(formats) + " ]")


def build_all():
    """Build everything."""
    gen_html()
    gen_markdown()
    gen_txt()
    gen_json()


def main():
    actions = {
        'all': build_all,
        'html': gen_html,
        'md': gen_markdown,
        'markdown': gen_markdown,
        'txt': gen_txt,
        'text': gen_txt,
        'json': gen_json,
    }

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in actions:
            actions[arg]()
        elif arg in ['-h', '--help', 'help']:
            print_usage(actions.keys())
        else:
            print(f"Unknown argument: {arg}")
            print_usage(actions.keys())
    else:
        print("Building everything")
        build_all()


if __name__ == '__main__':
    main()
