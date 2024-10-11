#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Build script for my resume
#
# -----------------------------------------------------------------------------
import yaml
import os
import sys

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
    'resume_data_yaml': os.environ.get('RESUME_DATA_YAML', 'data.yaml'),
    'resume_yaml': os.environ.get('RESUME_YAML', 'resume.yaml'),
})

# -----------------------------------------------------------------------------


class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)


# -----------------------------------------------------------------------------


def main():
    with open(config.resume_data_yaml, 'r') as file:
        resume_content = yaml.safe_load(file)

        with open(config.resume_yaml, 'w') as outfile:
            outfile.write("---\n\n")
            yaml.dump(resume_content, outfile, Dumper=Dumper, sort_keys=False, indent=2, width=60)


if __name__ == '__main__':
    main()
